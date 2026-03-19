from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union

from parsers import parse_verilog

if TYPE_CHECKING:
    from cli.mylogic_shell import MyLogicShell


def _nodes_list(netlist: Dict[str, Any]) -> List[Dict[str, Any]]:
    nodes = netlist.get("nodes", [])
    if isinstance(nodes, dict):
        return list(nodes.values())
    if isinstance(nodes, list):
        return [n for n in nodes if isinstance(n, dict)]
    return []


def _update_metadata_stats(netlist: Dict[str, Any]) -> Dict[str, Any]:
    if not netlist or "nodes" not in netlist:
        return netlist

    nodes_list = _nodes_list(netlist)

    type_counts: Dict[str, int] = {}
    category_counts = {
        "logic": 0,
        "arith": 0,
        "shift": 0,
        "compare": 0,
        "logical": 0,
        "struct": 0,
        "sequential": 0,
    }

    for node in nodes_list:
        node_type = node.get("type", "UNKNOWN")
        type_counts[node_type] = type_counts.get(node_type, 0) + 1

        if node_type in ["AND", "OR", "XOR", "NAND", "NOR", "XNOR", "NOT", "BUF"]:
            category_counts["logic"] += 1
        elif node_type in ["ADD", "SUB", "MUL", "DIV", "MOD"]:
            category_counts["arith"] += 1
        elif node_type in ["SHL", "SHR", "ASHL", "ASHR"]:
            category_counts["shift"] += 1
        elif node_type in ["EQ", "NE", "LT", "LE", "GT", "GE"]:
            category_counts["compare"] += 1
        elif node_type in ["ANDL", "ORL", "NOTL"]:
            category_counts["logical"] += 1
        elif node_type in ["DFF", "LATCH"]:
            category_counts["sequential"] += 1

    netlist.setdefault("attrs", {})
    netlist["attrs"]["operator_summary"] = {
        "type_counts": type_counts,
        "category_counts": category_counts,
        "total_nodes": len(nodes_list),
    }

    stats = netlist["attrs"].setdefault("parsing_stats", {})
    stats.update(
        {
            "total_nodes": len(nodes_list),
            "logic_nodes": category_counts["logic"],
            "arith_nodes": category_counts["arith"],
            "shift_nodes": category_counts["shift"],
            "compare_nodes": category_counts["compare"],
            "logical_nodes": category_counts["logical"],
            "struct_nodes": category_counts["struct"],
        }
    )
    return netlist


def _auto_export_json(shell: "MyLogicShell") -> None:
    if not shell.current_netlist:
        return

    if shell.filename:
        base_name = os.path.splitext(os.path.basename(shell.filename))[0]
        output_dir = "outputs"
        filename = os.path.join(output_dir, f"{base_name}_parsed.json") if os.path.exists(output_dir) else f"{base_name}_parsed.json"
    else:
        filename = "netlist_parsed.json"

    try:
        export_netlist = json.loads(json.dumps(shell.current_netlist))
        export_netlist = _update_metadata_stats(export_netlist)
        export_data = {
            "metadata": {
                "tool": "MyLogic EDA Tool v2.0.0",
                "export_time": datetime.now().isoformat(),
                "source_file": shell.filename or "unknown",
                "version": "2.0.0",
                "auto_exported": True,
            },
            "netlist": export_netlist,
        }

        out_dir = os.path.dirname(filename) if os.path.dirname(filename) else "."
        if out_dir == "outputs" and not os.path.exists(out_dir):
            os.makedirs(out_dir, exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        print(f"[INFO] Auto-exported JSON to: {filename}")
    except Exception:
        # silent to avoid breaking flow
        pass


def _cmd_read(shell: "MyLogicShell", parts: List[str]) -> None:
    if len(parts) < 2:
        print("[ERROR] Usage: read <file> [--loose]")
        return

    # Ghép parts[1:] để hỗ trợ đường dẫn có khoảng trắng (vd: D:\KHÓA LUẬN TỐT NGHIỆP\...)
    loose = False
    if "--loose" in parts:
        loose = True
        parts = [p for p in parts if p != "--loose"]
    path = " ".join(parts[1:]).strip()
    try:
        # Educational default: strict parsing to catch undeclared signals/typos
        shell.netlist = parse_verilog(path, strict=(not loose))
        shell.current_netlist = shell.netlist
        shell.filename = path
        n_nodes = len(shell.netlist.get("nodes", [])) if isinstance(shell.netlist, dict) else 0
        print(f"[OK] Loaded netlist with {n_nodes} nodes.")

        if shell.auto_export_json and shell.current_netlist:
            _auto_export_json(shell)
    except Exception as e:
        msg = str(e)
        if "Syntax error" in msg:
            print(f"ERROR SYNTAX: {msg}")
        else:
            print(f"[ERROR] Failed to read file: {msg}")


def _cmd_export(shell: "MyLogicShell", parts: Optional[List[str]] = None) -> None:
    if not shell.current_netlist:
        print("No netlist loaded. Use 'read <file>' first.")
        return

    parts = parts or []
    if len(parts) > 1:
        filename = parts[1]
        if not filename.endswith(".json"):
            filename += ".json"
    else:
        if shell.filename:
            base_name = shell.filename.replace(".v", "").replace(".logic", "")
            filename = f"{base_name}_netlist.json"
        else:
            filename = "netlist.json"

    try:
        export_netlist = json.loads(json.dumps(shell.current_netlist))
        export_netlist = _update_metadata_stats(export_netlist)

        nodes = export_netlist.get("nodes", [])
        node_count = len(nodes) if isinstance(nodes, (dict, list)) else 0

        export_data = {
            "metadata": {
                "tool": "MyLogic EDA Tool v2.0.0",
                "export_time": datetime.now().isoformat(),
                "source_file": shell.filename or "unknown",
                "version": "2.0.0",
                "auto_exported": False,
            },
            "netlist": export_netlist,
        }

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        print(f"[OK] Successfully exported netlist to: {filename}")
        print(f"[INFO] File contains:")
        print(f"   - {node_count} nodes")
        print(f"   - {len(export_netlist.get('wires', []))} wires")
        print(f"   - {len(export_netlist.get('inputs', []))} inputs")
        print(f"   - {len(export_netlist.get('outputs', []))} outputs")
    except Exception as e:
        print(f"[ERROR] Error exporting JSON: {e}")


def register(shell: "MyLogicShell") -> Dict[str, Callable]:
    return {
        "read": lambda parts: _cmd_read(shell, parts),
        "export": lambda parts=None: _cmd_export(shell, parts),
        "export_json": lambda parts=None: _cmd_export(shell, parts),
    }

