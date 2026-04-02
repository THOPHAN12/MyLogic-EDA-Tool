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


def _split_function_args(args_str: str) -> List[str]:
    args: List[str] = []
    current: List[str] = []
    depth = 0
    for ch in args_str:
        if ch == "," and depth == 0:
            arg = "".join(current).strip()
            if arg:
                args.append(arg)
            current = []
            continue
        if ch == "(":
            depth += 1
        elif ch == ")" and depth > 0:
            depth -= 1
        current.append(ch)
    tail = "".join(current).strip()
    if tail:
        args.append(tail)
    return args


def _function_to_verilog_expr(function: str) -> str | None:
    s = (function or "").strip()
    if not s:
        return None
    if s == "CONST0":
        return "1'b0"
    if s == "CONST1":
        return "1'b1"
    if s in ("0", "1") or "'" in s:
        return s

    match = re.match(r"^(\w+)\((.*)\)$", s)
    if not match:
        return s

    op = match.group(1).upper()
    args = _split_function_args(match.group(2))
    rendered = []
    for arg in args:
        expr = _function_to_verilog_expr(arg)
        if expr is None:
            return None
        rendered.append(expr)

    if op == "BUF" and len(rendered) == 1:
        return rendered[0]
    if op == "NOT" and len(rendered) == 1:
        return f"~({rendered[0]})"
    if op == "AND" and len(rendered) >= 2:
        return "(" + " & ".join(rendered) + ")"
    if op == "OR" and len(rendered) >= 2:
        return "(" + " | ".join(rendered) + ")"
    if op == "XOR" and len(rendered) >= 2:
        return "(" + " ^ ".join(rendered) + ")"
    if op == "NAND" and len(rendered) >= 2:
        return "~(" + " & ".join(rendered) + ")"
    if op == "NOR" and len(rendered) >= 2:
        return "~(" + " | ".join(rendered) + ")"
    if op == "XNOR" and len(rendered) >= 2:
        return "~(" + " ^ ".join(rendered) + ")"
    return None


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

    primitive_gates = {"and", "or", "xor", "xnor", "nand", "nor", "not", "buf"}

    # Build assigns and explicit cell instances.
    assigns: List[str] = []
    instances: List[str] = []
    for n in nodes:
        t = str(n.get("type", "") or "").upper()
        raw_type = str(n.get("type", "") or "").strip()
        out = str(n.get("output", "") or "").strip()
        ins = [str(x).strip() for x in (n.get("inputs") or [])]
        input_pins = [str(x).strip() for x in (n.get("input_pins") or []) if str(x).strip()]
        output_pins = [str(x).strip() for x in (n.get("output_pins") or []) if str(x).strip()]
        node_id = str(n.get("id", "") or f"inst_{len(instances)}").strip()
        inst_name = f"u_{node_id}"
        function_str = str(n.get("function", "") or "").strip()
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
            # Verilog primitive gates use positional ports: gate inst (Y, A, B, ...).
            if raw_type.lower() in primitive_gates:
                primitive_ports = [out, *ins]
                if primitive_ports:
                    instances.append(f"{raw_type.lower()} {inst_name} ({', '.join(primitive_ports)});")
            # For mapped technology cells, emit named-port instances so the
            # generated netlist does not depend on module port declaration order.
            elif raw_type and input_pins and output_pins:
                port_conns: List[str] = []
                for pin_name, sig in zip(input_pins, ins):
                    port_conns.append(f".{pin_name}({sig})")
                for pin_name in output_pins:
                    port_conns.append(f".{pin_name}({out})")
                instances.append(f"{raw_type} {inst_name} ({', '.join(port_conns)});")
            # Fallback to assign if no pin metadata exists.
            elif function_str:
                expr = _function_to_verilog_expr(function_str)
                if expr is not None:
                    assigns.append(f"assign {out} = {expr};")
            elif len(ins) == 1:
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
    if instances:
        body.append("")
        body.extend([f"  {inst}" for inst in instances])
    body.append("endmodule")
    body.append("")
    return "\n".join(body)

