from __future__ import annotations

import re
from typing import Any, Dict, List, Set, Tuple


def _nodes_list(netlist: Dict[str, Any]) -> List[Dict[str, Any]]:
    nodes = netlist.get("nodes", {})
    if isinstance(nodes, dict):
        return [n for n in nodes.values() if isinstance(n, dict)]
    if isinstance(nodes, list):
        return [n for n in nodes if isinstance(n, dict)]
    return []


def _bus_base_and_bit(sig: str) -> Tuple[str, int] | None:
    m = re.match(r"^([A-Za-z_]\w*)\[(\d+)\]$", sig.strip())
    if not m:
        return None
    return m.group(1), int(m.group(2))


def netlist_to_verilog(netlist: Dict[str, Any], module_name: str | None = None) -> str:
    """
    Convert a synthesized netlist dictionary (AIG->netlist) into structural Verilog.
    Supported node types: AND, NOT, BUF, CONST0, CONST1.
    Also tolerates OR/XOR/NAND/NOR/XNOR as assign operators if present.
    """
    module_name = module_name or netlist.get("name") or "design"
    inputs: List[str] = list(netlist.get("inputs", []) or [])
    outputs: List[str] = list(netlist.get("outputs", []) or [])
    vw = (netlist.get("attrs", {}) or {}).get("vector_widths", {}) or {}
    nodes = _nodes_list(netlist)

    # Infer bus widths from any indexed signal usage (ports included).
    inferred_bus: Dict[str, int] = {}
    for n in nodes:
        out = str(n.get("output", "") or "")
        ins = n.get("inputs") or []
        for s in [out, *[str(x) for x in ins]]:
            bb = _bus_base_and_bit(str(s))
            if bb:
                base, bit = bb
                inferred_bus[base] = max(inferred_bus.get(base, 0), bit + 1)

    def width_of(sig: str) -> int:
        if sig in vw and isinstance(vw[sig], int):
            return int(vw[sig])
        if sig in inferred_bus:
            return inferred_bus[sig]
        return 1

    # Collect internal nets (excluding ports and their bits)
    port_set: Set[str] = set(inputs) | set(outputs)
    internal_scalars: Set[str] = set()
    internal_buses: Dict[str, int] = {}

    def mark_sig(s: str):
        s = s.strip()
        if not s:
            return
        # constants
        if s in ("0", "1") or "'" in s:
            return
        bb = _bus_base_and_bit(s)
        if bb:
            base, bit = bb
            if base in port_set:
                return
            internal_buses[base] = max(internal_buses.get(base, 0), bit + 1)
            return
        if s in port_set:
            return
        internal_scalars.add(s)

    for n in nodes:
        out = str(n.get("output", "") or "")
        ins = n.get("inputs") or []
        for i in ins:
            mark_sig(str(i))
        mark_sig(out)

    # Build assigns
    assigns: List[str] = []
    for n in nodes:
        t = str(n.get("type", "") or "").upper()
        out = str(n.get("output", "") or "").strip()
        ins = [str(x).strip() for x in (n.get("inputs") or [])]
        if not out:
            continue

        if t == "BUF":
            if len(ins) >= 1:
                if ins[0] != out:
                    assigns.append(f"assign {out} = {ins[0]};")
        elif t == "NOT":
            if len(ins) >= 1:
                assigns.append(f"assign {out} = ~{ins[0]};")
        elif t == "AND":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = {ins[0]} & {ins[1]};")
        elif t == "OR":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = {ins[0]} | {ins[1]};")
        elif t == "XOR":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = {ins[0]} ^ {ins[1]};")
        elif t == "NAND":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = ~({ins[0]} & {ins[1]});")
        elif t == "NOR":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = ~({ins[0]} | {ins[1]});")
        elif t == "XNOR":
            if len(ins) >= 2:
                assigns.append(f"assign {out} = ~({ins[0]} ^ {ins[1]});")
        elif t == "CONST0":
            assigns.append(f"assign {out} = 1'b0;")
        elif t == "CONST1":
            assigns.append(f"assign {out} = 1'b1;")
        else:
            # Unknown node type: emit comment-like safe assignment if possible
            if len(ins) == 1:
                if ins[0] != out:
                    assigns.append(f"assign {out} = {ins[0]};")

    # Header ports
    port_lines: List[str] = []
    for i, inp in enumerate(inputs):
        w = width_of(inp)
        if w > 1:
            port_lines.append(f"  input  wire [{w-1}:0] {inp}")
        else:
            port_lines.append(f"  input  wire {inp}")
    for outp in outputs:
        w = width_of(outp)
        if w > 1:
            port_lines.append(f"  output wire [{w-1}:0] {outp}")
        else:
            port_lines.append(f"  output wire {outp}")

    # Internal declarations
    decls: List[str] = []
    for base, w in sorted(internal_buses.items()):
        decls.append(f"  wire [{w-1}:0] {base};")
    for s in sorted(internal_scalars):
        decls.append(f"  wire {s};")

    body: List[str] = []
    body.append(f"module {module_name}(")
    body.append(",\n".join(port_lines))
    body.append(");")
    if decls:
        body.append("")
        body.extend(decls)
    if assigns:
        body.append("")
        body.extend([f"  {a}" for a in assigns])
    body.append("endmodule")
    body.append("")
    return "\n".join(body)

