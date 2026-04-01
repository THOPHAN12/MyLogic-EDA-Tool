from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Set, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _nodes_list(netlist: Dict[str, Any]) -> List[Dict[str, Any]]:
    nodes_any = netlist.get("nodes", [])
    if isinstance(nodes_any, dict):
        return [n for n in nodes_any.values() if isinstance(n, dict)]
    if isinstance(nodes_any, list):
        return [n for n in nodes_any if isinstance(n, dict)]
    return []


def _is_constant(sig: str) -> bool:
    s = (sig or "").strip()
    if s in ("0", "1"):
        return True
    if "'" in s:
        # e.g., 8'd0, 1'b1, 'b1
        return True
    return False


def _print_cone(
    output_sig: str,
    inputs: List[str],
    drivers: Dict[str, Dict[str, Any]],
    visited_nodes: Set[str],
    indent: str = "",
) -> None:
    # If this signal is driven by a node, print it and recurse on its inputs.
    if output_sig in drivers:
        node = drivers[output_sig]
        node_id = str(node.get("id", ""))
        # Prevent infinite recursion on self-alias loops:
        # if the node id was printed already, still show its input fanins but do not recurse.
        fin_for_print: List[str] = []
        fin = node.get("inputs", []) or []
        for f in fin:
            if isinstance(f, (list, tuple)) and f:
                fin_for_print.append(str(f[0]))
            else:
                fin_for_print.append(str(f))

        ntype = node.get("type", "CELL")
        if node_id and node_id in visited_nodes:
            print(f"{indent}{ntype} <{node_id}>  output={output_sig} (visited)  fanins=({', '.join(fin_for_print)})")
            return

        if node_id:
            visited_nodes.add(node_id)

        print(f"{indent}{ntype} <{node_id}>  output={output_sig}")
        for s in fin_for_print:
            if s in inputs:
                print(f"{indent}  INPUT <{s}>")
            elif _is_constant(s):
                print(f"{indent}  CONST <{s}>")
            else:
                _print_cone(s, inputs, drivers, visited_nodes, indent=indent + "  ")
        return

    # Otherwise, it is a primary input or an internal wire with no driver in netlist.
    if output_sig in inputs:
        print(f"{indent}INPUT <{output_sig}>")
    elif _is_constant(output_sig):
        print(f"{indent}CONST <{output_sig}>")
    else:
        # Missing driver: show it to help debugging.
        print(f"{indent}IDENTIFIER <{output_sig}> (no driver in synthesized netlist)")


def _cmd_dump_synth(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_aig or not shell.current_netlist:
        print("[ERROR] No synthesized AIG available. Run 'synthesis' first.")
        return

    # Build synthesized netlist directly from AIG so it matches the exported synthesis JSON.
    from core.synthesis.aig import aig_to_netlist

    # For comparisons: avoid rewriting AND(x,1)=x during AIG->netlist export.
    # This makes "synthesis vs optimize" differences visible in cell counts and cones.
    synth_netlist = aig_to_netlist(shell.current_aig, shell.current_netlist, simplify_and_with_const1=False)

    module_name = synth_netlist.get("name", "design")
    inputs = synth_netlist.get("inputs", []) or []
    outputs = synth_netlist.get("outputs", []) or []
    nodes = _nodes_list(synth_netlist)

    drivers: Dict[str, Dict[str, Any]] = {}
    for n in nodes:
        out = n.get("output", "")
        if isinstance(out, str) and out:
            drivers[out] = n

    print(f"Dumping SYNTHESIZED netlist (AIG->netlist) for <{module_name}>")
    print("=" * 70)
    print(f"Inputs : {', '.join(inputs) if inputs else '(none)'}")
    print(f"Outputs: {', '.join(outputs) if outputs else '(none)'}")
    print(f"Cells  : {len(nodes)}")
    print()

    # Optional: dump just one output cone: dump_synth <out_signal>
    out_sig: Optional[str] = None
    if parts and len(parts) >= 2:
        out_sig = parts[1]

    if out_sig:
        if out_sig not in outputs and out_sig not in drivers:
            print(f"[WARN] Output '{out_sig}' not listed as PO. Will try to dump cone by driver mapping.")
        print(f"--- CONE for {out_sig} ---")
        visited: Set[str] = set()
        _print_cone(out_sig, inputs, drivers, visited, indent="  ")
        print("--- END CONE ---")
        return

    # Default: print a simple cell list + then cones for all outputs (compact).
    print("[CELLS]")
    for n in nodes:
        ntype = n.get("type", "CELL")
        nid = n.get("id", "")
        out = n.get("output", "")
        fin = n.get("inputs", []) or []
        fanins = []
        for f in fin:
            if isinstance(f, (list, tuple)) and f:
                fanins.append(str(f[0]))
            else:
                fanins.append(str(f))
        print(f"- {ntype} <{nid}>: ({', '.join(fanins)}) -> {out}")

    print()
    print("[OUTPUT CONES]")
    for o in outputs:
        print(f"\n== {o} ==")
        visited = set()
        _print_cone(o, inputs, drivers, visited, indent="  ")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "dump_synth": lambda parts=None: _cmd_dump_synth(shell, parts),
        "dump_synthesis": lambda parts=None: _cmd_dump_synth(shell, parts),
    }

