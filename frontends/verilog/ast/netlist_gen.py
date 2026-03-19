from __future__ import annotations

import re
from typing import Any, Dict, List

from core.utils.error_handling import ParserError
from frontends.verilog.core.node_builder import NodeBuilder, WireGenerator
from frontends.verilog.core.tokenizer import remove_inline_comments
from frontends.verilog.core.parser import _dispatch_assign_parser  # reuse existing lowering

from .ast_parser import MyVModule, parse_myverilog_ast


def parse_verilog_ast(path: str, strict: bool = True) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        src = f.read()
    mod = parse_myverilog_ast(src, path)
    return ast_to_netlist(mod, path, strict=strict)


def _eval_int_simple(expr: str, params: Dict[str, int]) -> int:
    expr = expr.strip()
    for k, v in params.items():
        expr = re.sub(rf"\\b{k}\\b", str(v), expr)
    if not re.match(r"^[0-9+\\-*/%\\s()]+$", expr):
        raise ParserError(f"Unsafe integer expression {expr!r}")
    return int(eval(expr, {"__builtins__": None}, {}))


def ast_to_netlist(mod: MyVModule, path: str, strict: bool = True) -> Dict[str, Any]:
    """
    Elaborate (params + widths) and generate netlist nodes using existing operation dispatch.
    Educational choices:
    - Width mismatch: error except constants (will be extended/truncated later in synthesis).
    - Implicit wire: forbidden if strict=True (default for AST frontend).
    """
    netlist: Dict[str, Any] = {
        "name": mod.name,
        "inputs": list(mod.inputs.keys()),
        "outputs": list(mod.outputs.keys()),
        "nodes": [],
        "wires": [],
        "attrs": {
            "source_file": path,
            "vector_widths": {},
            "output_mapping": {},
            "parameters": {k: str(v) for k, v in mod.params.items()},
            "reg_signals": list(mod.regs.keys()),
            "signed_signals": [],
        },
    }

    vw = netlist["attrs"]["vector_widths"]
    for n, w in {**mod.inputs, **mod.outputs, **mod.wires, **mod.regs}.items():
        vw[n] = w

    declared = set(vw.keys())

    def check_declared(expr: str):
        if not strict:
            return
        # find identifiers (very small heuristic; AST already parsed)
        ids = re.findall(r"\\b[A-Za-z_]\\w*\\b", expr)
        for i in ids:
            if i in ("assign", "wire", "reg", "input", "output", "begin", "end", "if", "else", "posedge", "always"):
                continue
            if i in declared:
                continue
            # constants like d/h/b/o are not identifiers here
            raise ParserError(f"Error: Signal {i!r} is used but not explicitly declared in {path}")

    nb = NodeBuilder()

    # Continuous assigns
    for lhs, rhs in mod.assigns:
        check_declared(rhs)
        _dispatch_assign_parser(lhs, rhs, nb, mod.params)

    # always @(*) blocks: support a subset
    for body in mod.always_comb:
        cleaned = remove_inline_comments(body)
        # handle simple blocking assigns and if/else by translating to dispatch per assignment
        # blocking: x = expr;
        for m in re.finditer(r"(\\w+)\\s*=\\s*([^;]+);", cleaned):
            lhs = m.group(1).strip()
            rhs = m.group(2).strip()
            check_declared(rhs)
            _dispatch_assign_parser(lhs, rhs, nb, mod.params)

    # always @(posedge clk): create DFF nodes but do not elaborate FSM/timing
    for clk, body in mod.always_seq:
        cleaned = remove_inline_comments(body)
        for m in re.finditer(r"(\\w+)\\s*<=\\s*([^;]+);", cleaned):
            q = m.group(1).strip()
            d = m.group(2).strip()
            check_declared(d)
            seq_id = nb.create_sequential_node(
                node_type="DFF",
                data_input=d,
                clock_signal=clk,
                edge_type="posedge",
                output_signal=q,
            )
            netlist["attrs"]["output_mapping"][q] = seq_id

    netlist["nodes"] = nb.get_nodes()
    netlist["attrs"]["output_mapping"].update(nb.get_output_mapping())
    # wires (auto)
    wires = WireGenerator.generate_wires(netlist["nodes"])
    netlist["wires"] = wires
    return netlist

