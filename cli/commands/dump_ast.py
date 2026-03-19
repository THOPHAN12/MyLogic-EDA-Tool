from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _print_expression_tree(
    node: Dict[str, Any],
    nodes: List[Dict[str, Any]],
    signal_to_node: Dict[str, Dict[str, Any]],
    node_by_id: Dict[str, Dict[str, Any]],
    node_outputs: Dict[str, str],
    all_signals: Set[str],
    indent: str = "",
) -> None:
    node_type = node.get("type", "UNKNOWN")
    node_id = node.get("id", "")
    inputs = node.get("inputs", [])
    fanins = node.get("fanins", [])

    input_signals: List[str] = []
    if fanins:
        for fanin in fanins:
            if isinstance(fanin, (list, tuple)) and len(fanin) > 0:
                input_signals.append(str(fanin[0]))
            else:
                input_signals.append(str(fanin))
    elif inputs:
        input_signals = [str(inp) for inp in inputs]

    ast_type_map = {
        "AND": "NETLIST_BIT_AND",
        "OR": "NETLIST_BIT_OR",
        "XOR": "NETLIST_BIT_XOR",
        "NAND": "NETLIST_BIT_NAND",
        "NOR": "NETLIST_BIT_NOR",
        "XNOR": "NETLIST_BIT_XNOR",
        "NOT": "NETLIST_BIT_NOT",
        "BUF": "NETLIST_BUF",
        "ADD": "NETLIST_ADD",
        "SUB": "NETLIST_SUB",
        "MUL": "NETLIST_MUL",
        "DIV": "NETLIST_DIV",
        "EQ": "NETLIST_EQ",
        "MUX": "NETLIST_MUX",
    }
    ast_type = ast_type_map.get(node_type, f"NETLIST_{node_type}")

    if input_signals:
        print(f"{indent}{ast_type} <{node_id}>")
        for input_signal in input_signals:
            if input_signal in signal_to_node:
                child = signal_to_node[input_signal]
                _print_expression_tree(
                    child,
                    nodes,
                    signal_to_node,
                    node_by_id,
                    node_outputs,
                    all_signals,
                    indent=indent + "  ",
                )
            elif input_signal in node_by_id:
                # Some netlists use node_id directly as a "signal" name (e.g. mux_2)
                child = node_by_id[input_signal]
                _print_expression_tree(
                    child,
                    nodes,
                    signal_to_node,
                    node_by_id,
                    node_outputs,
                    all_signals,
                    indent=indent + "  ",
                )
            elif input_signal in all_signals:
                if input_signal in ["const_True", "const_False", "1", "0"]:
                    const_val = "1" if input_signal in ["const_True", "1"] else "0"
                    print(f"{indent}  NETLIST_CONSTANT <{const_val}>")
                else:
                    print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
            else:
                print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
    else:
        if node_type in ["CONST0", "CONST1"]:
            const_val = "1" if node_type == "CONST1" else "0"
            print(f"{indent}NETLIST_CONSTANT <{const_val}>")
        else:
            print(f"{indent}{ast_type} <{node_id}>")


def _cmd_dump_ast(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    netlist_to_show = shell.current_netlist if shell.current_netlist else shell.netlist
    if not netlist_to_show:
        print("[ERROR] No netlist loaded. Use 'read <file>' first.")
        return
    if not isinstance(netlist_to_show, dict):
        print("[ERROR] Invalid netlist format.")
        return

    module_name = netlist_to_show.get("name", "unknown")
    inputs = netlist_to_show.get("inputs", [])
    outputs = netlist_to_show.get("outputs", [])
    nodes_any = netlist_to_show.get("nodes", [])
    output_mapping = netlist_to_show.get("attrs", {}).get("output_mapping", {}) or {}

    nodes: List[Dict[str, Any]]
    if isinstance(nodes_any, dict):
        nodes = list(nodes_any.values())
    elif isinstance(nodes_any, list):
        nodes = nodes_any
    else:
        nodes = []

    print("Dumping Netlist AST Structure:")
    print("=" * 70)
    print(f"\nNETLIST_MODULE <{module_name}>")

    for inp in inputs:
        print(f"  NETLIST_WIRE <{inp}> input port")
    for out in outputs:
        print(f"  NETLIST_WIRE <{out}> output port")

    signal_to_node: Dict[str, Dict[str, Any]] = {}  # signal name -> driving node
    node_by_id: Dict[str, Dict[str, Any]] = {}      # node id -> node
    node_outputs: Dict[str, str] = {}               # node id -> representative output signal
    all_signals: Set[str] = set(inputs)

    for node in nodes:
        node_id = node.get("id", "")
        out_sig = node.get("output", "")
        node_by_id[node_id] = node
        if out_sig:
            # Some nodes may carry explicit 'output' field (not always present)
            signal_to_node[out_sig] = node
            node_outputs[node_id] = out_sig
            all_signals.add(out_sig)

    # Populate signal_to_node using attrs.output_mapping (parser's primary source of drivers)
    for sig, mapped_node_id in output_mapping.items():
        if not isinstance(sig, str) or not sig:
            continue
        if not isinstance(mapped_node_id, str) or not mapped_node_id:
            continue
        n = node_by_id.get(mapped_node_id)
        if n:
            signal_to_node[sig] = n
            all_signals.add(sig)
            # Prefer first discovered representative output per node id
            node_outputs.setdefault(mapped_node_id, sig)

    for output_name in outputs:
        print(f"\n  NETLIST_ASSIGN <{output_name}>")
        node_id = output_mapping.get(output_name, "")
        node = None
        if node_id and node_id in node_by_id:
            node = node_by_id[node_id]
        elif output_name in signal_to_node:
            node = signal_to_node[output_name]
        else:
            for n in nodes:
                if n.get("output") == output_name:
                    node = n
                    break

        if node:
            _print_expression_tree(
                node,
                nodes,
                signal_to_node,
                node_by_id,
                node_outputs,
                all_signals,
                indent="    ",
            )
        else:
            print(f"    NETLIST_IDENTIFIER <{output_name}>")

    print("\n--- END OF AST DUMP ---")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "dump": lambda parts=None: _cmd_dump_ast(shell, parts),
        "dump_ast": lambda parts=None: _cmd_dump_ast(shell, parts),
    }

