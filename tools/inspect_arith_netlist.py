from __future__ import annotations

import os
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, REPO_ROOT)

from frontends.verilog import parse_verilog


def main() -> None:
    path = r"D:\KHOA_LUAN_TOT_NGHIEP\Mylogic\demo\CAN_DO\06_arithmetic_operations.v"
    nl = parse_verilog(path)
    print("name:", nl.get("name"))
    print("inputs:", nl.get("inputs"))
    print("outputs:", nl.get("outputs"))
    print("attrs.vector_widths:", (nl.get("attrs", {}) or {}).get("vector_widths"))
    nodes = nl.get("nodes", {})
    node_list = list(nodes.values()) if isinstance(nodes, dict) else (nodes or [])
    print("\n--- nodes of interest ---")
    for n in node_list:
        if not isinstance(n, dict):
            continue
        out = n.get("output")
        if out in {"carry_out", "sum0", "sum1", "sum2", "sum3", "diff", "add_result"} or (
            isinstance(out, str) and out.startswith("add_result")
        ):
            print("id:", n.get("id"), "type:", n.get("type"), "output:", out, "fanins:", n.get("fanins") or n.get("inputs"))


if __name__ == "__main__":
    main()

