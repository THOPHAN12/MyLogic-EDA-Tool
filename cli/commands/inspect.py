from __future__ import annotations

from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _cmd_stats(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    netlist_to_show = shell.current_netlist if shell.current_netlist else shell.netlist
    if not netlist_to_show:
        print("[WARNING] No netlist loaded.")
        return

    if not isinstance(netlist_to_show, dict):
        print("Circuit statistics:")
        print(f"  Name    : {getattr(shell.netlist, 'name', 'unknown')}")
        print(f"  Inputs  : {len(getattr(shell.netlist, 'inputs', []))}")
        print(f"  Outputs : {len(getattr(shell.netlist, 'outputs', []))}")
        print(f"  Wires   : {len(getattr(shell.netlist, 'wires', []))}")
        print(f"  Nodes   : {len(getattr(shell.netlist, 'nodes', []))}")
        print(f"  Type    : Scalar (1-bit)")
        return

    name = netlist_to_show.get("name", "unknown")
    inputs = netlist_to_show.get("inputs", [])
    outputs = netlist_to_show.get("outputs", [])
    nodes = netlist_to_show.get("nodes", [])
    wires = netlist_to_show.get("wires", [])
    vector_widths = netlist_to_show.get("attrs", {}).get("vector_widths", {})

    print("=== ENHANCED CIRCUIT STATISTICS ===")
    print(f"  Name    : {name}")
    print(f"  Inputs  : {len(inputs)}")
    print(f"  Outputs : {len(outputs)}")
    print(f"  Wires   : {len(wires)}")
    print(f"  Nodes   : {len(nodes)}")

    if vector_widths:
        print("\n  Vector Analysis:")
        width_groups: Dict[int, List[str]] = {}
        for signal, width in vector_widths.items():
            width_groups.setdefault(width, []).append(signal)
        for width in sorted(width_groups.keys(), reverse=True):
            signals = width_groups[width]
            print(f"    {width}-bit ({len(signals)} signals): {', '.join(signals)}")
        print(f"  Summary: {len(vector_widths)} signals across {len(width_groups)} bit widths")

    nodes_list = list(nodes.values()) if isinstance(nodes, dict) else (nodes if isinstance(nodes, list) else [])
    if nodes_list:
        node_types: Dict[str, int] = {}
        for node in nodes_list:
            if isinstance(node, dict):
                t = node.get("type", "UNKNOWN")
                node_types[t] = node_types.get(t, 0) + 1
        print("\n  Node Analysis:")
        for node_type, count in sorted(node_types.items()):
            pct = (count / len(nodes_list)) * 100 if nodes_list else 0
            print(f"    {node_type}: {count} ({pct:.1f}%)")

    if wires:
        print("\n  Wire Analysis:")
        print(f"    Total wires: {len(wires)}")
        wire_types: Dict[str, int] = {}
        for wire in wires:
            if isinstance(wire, dict):
                wt = wire.get("type", "unknown")
                wire_types[wt] = wire_types.get(wt, 0) + 1
            else:
                wire_types["simple"] = wire_types.get("simple", 0) + 1
        for wt, count in wire_types.items():
            print(f"    {wt}: {count}")

    module_insts = netlist_to_show.get("attrs", {}).get("module_instantiations", {})
    if module_insts:
        print("\n  Module Instantiations:")
        print(f"    Total modules: {len(module_insts)}")
        for inst_name, inst_info in module_insts.items():
            module_type = inst_info.get("module_type", "unknown")
            connections = inst_info.get("connections", [])
            print(f"    {inst_name} ({module_type}): {len(connections)} connections")

    print("\n  Type    : Vector (n-bit)")
    print("  Use 'vectors' command for detailed view")
    print("  Use 'nodes' command for node details")
    print("  Use 'wires' command for wire analysis")


def _cmd_vectors(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.netlist:
        print("[WARNING] No netlist loaded.")
        return
    if not isinstance(shell.netlist, dict):
        print("Vector details only available for vector netlists.")
        return
    vector_widths = shell.netlist.get("attrs", {}).get("vector_widths", {})
    if not vector_widths:
        print("No vector information available.")
        return
    print("Detailed Vector Widths:")
    width_groups: Dict[int, List[str]] = {}
    for signal, width in vector_widths.items():
        width_groups.setdefault(width, []).append(signal)
    for width in sorted(width_groups.keys(), reverse=True):
        signals = width_groups[width]
        print(f"\n{width}-bit signals ({len(signals)} total):")
        for i, signal in enumerate(signals, 1):
            print(f"  {i:2d}. {signal}")


def _cmd_nodes(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("No netlist loaded. Use 'read <file>' first.")
        return
    netlist_to_show = shell.current_netlist if shell.current_netlist else shell.netlist
    nodes = netlist_to_show.get("nodes", []) if isinstance(netlist_to_show, dict) else []
    if isinstance(nodes, dict):
        nodes = list(nodes.values())
    if not nodes:
        print("No nodes available.")
        return
    print("Detailed Node Information:")
    print("=" * 50)
    for i, node in enumerate(nodes):
        node_id = node.get("id", f"node_{i}")
        node_type = node.get("type", "UNKNOWN")
        fanins = node.get("fanins", [])
        fanin_str = ", ".join([f"{f[0]}" for f in fanins]) if fanins else "none"
        print(f"\n{i+1:2d}. {node_id} ({node_type})")
        print(f"     Inputs: [{fanin_str}]")
        if "module_type" in node:
            print(f"     Module: {node['module_type']}")
        if "connections" in node:
            print(f"     Connections: {len(node['connections'])}")
    print(f"\nTotal: {len(nodes)} nodes")


def _cmd_wires(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("No netlist loaded. Use 'read <file>' first.")
        return
    netlist_to_show = shell.current_netlist if shell.current_netlist else shell.netlist
    wires = netlist_to_show.get("wires", []) if isinstance(netlist_to_show, dict) else []
    if not wires:
        print("No wires available.")
        return
    print("Detailed Wire Information:")
    print("=" * 50)
    for i, wire in enumerate(wires):
        if isinstance(wire, dict):
            wire_id = wire.get("id", f"wire_{i}")
            wire_type = wire.get("type", "unknown")
            source = wire.get("source", "unknown")
            destination = wire.get("destination", "unknown")
            print(f"\n{i+1:2d}. {wire_id} ({wire_type})")
            print(f"     Source: {source}")
            print(f"     Destination: {destination}")
        else:
            print(f"\n{i+1:2d}. {wire}")
    print(f"\nTotal: {len(wires)} wires")


def _cmd_modules(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("No netlist loaded. Use 'read <file>' first.")
        return
    netlist_to_show = shell.current_netlist if shell.current_netlist else shell.netlist
    module_insts = netlist_to_show.get("attrs", {}).get("module_instantiations", {}) if isinstance(netlist_to_show, dict) else {}
    if not module_insts:
        print("No module instantiations available.")
        return
    print("Detailed Module Instantiation Information:")
    print("=" * 50)
    for i, (inst_name, inst_info) in enumerate(module_insts.items(), 1):
        module_type = inst_info.get("module_type", "unknown")
        connections = inst_info.get("connections", [])
        print(f"\n{i:2d}. {inst_name} ({module_type})")
        print(f"     Connections: {len(connections)}")
        for j, conn in enumerate(connections):
            print(f"       {j+1}. {conn}")
    print(f"\nTotal: {len(module_insts)} module instantiations")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "stats": lambda parts=None: _cmd_stats(shell, parts),
        "vectors": lambda parts=None: _cmd_vectors(shell, parts),
        "nodes": lambda parts=None: _cmd_nodes(shell, parts),
        "wires": lambda parts=None: _cmd_wires(shell, parts),
        "modules": lambda parts=None: _cmd_modules(shell, parts),
    }

