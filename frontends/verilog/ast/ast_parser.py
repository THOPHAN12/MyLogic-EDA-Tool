from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple, Union

from core.utils.error_handling import ParserError


_FORBIDDEN = ("initial", "for", "while", "casex", "casez")


def _precheck_forbidden(source: str, path: str) -> None:
    lowered = source.lower()
    for kw in _FORBIDDEN:
        if re.search(rf"\\b{re.escape(kw)}\\b", lowered):
            raise ParserError(f"Syntax error: forbidden keyword '{kw}' in {path}")


@dataclass
class MyVModule:
    name: str
    inputs: Dict[str, int]
    outputs: Dict[str, int]
    regs: Dict[str, int]
    wires: Dict[str, int]
    assigns: List[Tuple[str, str]]  # (lhs, rhs as source slice)
    always_comb: List[str]  # body source for always @(*)
    always_seq: List[Tuple[str, str]]  # (clk, body source) for posedge
    params: Dict[str, int]


def _width_from_range(msb: int, lsb: int) -> int:
    return abs(msb - lsb) + 1


def parse_myverilog_ast(source: str, path: str = "<string>") -> MyVModule:
    """
    Parse MyVerilog subset into a lightweight AST summary.
    This does NOT build a full expression AST; expressions are kept as source strings
    and later lowered using existing expression/dispatch in the project.
    """
    _precheck_forbidden(source, path)

    try:
        from lark import Lark, Tree, Token
    except Exception as e:
        raise ParserError(
            "Lark is required for AST parser. Install with: pip install lark"
        ) from e

    grammar_path = os.path.join(os.path.dirname(__file__), "myverilog.lark")
    with open(grammar_path, "r", encoding="utf-8") as f:
        grammar = f.read()

    parser = Lark(grammar, start="start", parser="lalr", propagate_positions=True)

    try:
        tree = parser.parse(source)
    except Exception as e:
        raise ParserError(f"Syntax error (MyVerilog AST) in {path}: {e}") from e

    # Walk and collect declarations + statement texts (simple, educational)
    text_lines = source.splitlines()

    def slice_text(meta) -> str:
        if not meta:
            return ""
        # Lark uses 1-based line/column
        sl, sc = meta.line - 1, meta.column - 1
        el, ec = meta.end_line - 1, meta.end_column - 1
        if sl == el:
            return text_lines[sl][sc:ec]
        parts = [text_lines[sl][sc:]]
        for i in range(sl + 1, el):
            parts.append(text_lines[i])
        parts.append(text_lines[el][:ec])
        return "\n".join(parts)

    # Minimal collector via Tree traversal
    name = None
    inputs: Dict[str, int] = {}
    outputs: Dict[str, int] = {}
    regs: Dict[str, int] = {}
    wires: Dict[str, int] = {}
    assigns: List[Tuple[str, str]] = []
    always_comb: List[str] = []
    always_seq: List[Tuple[str, str]] = []
    params: Dict[str, int] = {}

    def eval_int(expr: str) -> int:
        expr = expr.strip()
        if re.fullmatch(r"[0-9]+", expr):
            return int(expr)
        # Replace params
        for k, v in params.items():
            expr = re.sub(rf"\\b{k}\\b", str(v), expr)
        if not re.match(r"^[0-9+\\-*/%\\s()]+$", expr):
            raise ParserError(f"Unsafe integer expression {expr!r} in {path}")
        return int(eval(expr, {"__builtins__": None}, {}))

    def collect(t: Tree):
        nonlocal name
        if t.data == "module":
            name = str(t.children[0])
        elif t.data == "param":
            pname = str(t.children[0])
            pexpr = slice_text(t.meta)  # "parameter X = expr"
            # extract rhs
            rhs = pexpr.split("=", 1)[1].strip()
            params[pname] = eval_int(rhs)
        elif t.data == "port_decl":
            # port_decl: dir type? signed? range? NAME
            parts = [c for c in t.children]
            # In this grammar, port_dir produces a Tree with no token; use first word in slice
            decl_text = slice_text(t.meta)
            mdir = re.match(r"\s*(input|output)\b", decl_text, flags=re.IGNORECASE)
            direction = (mdir.group(1).lower() if mdir else "input")
            pname = str(parts[-1])
            rng = None
            for c in parts:
                if isinstance(c, Tree) and c.data == "range":
                    rng = c
            width = 1
            if rng:
                # range: "[" expr ":" expr "]"
                msb_s = slice_text(rng.children[0].meta) or str(rng.children[0])
                lsb_s = slice_text(rng.children[1].meta) or str(rng.children[1])
                width = _width_from_range(eval_int(msb_s), eval_int(lsb_s))
            if direction == "input":
                inputs[pname] = width
            else:
                outputs[pname] = width
        elif t.data == "decl":
            decl_text = slice_text(t.meta)
            kind = decl_text.strip().split()[0]
            # parse width from any range [...] present
            width = 1
            m = re.search(r"\\[([^:]+):([^\\]]+)\\]", decl_text)
            if m:
                width = _width_from_range(eval_int(m.group(1)), eval_int(m.group(2)))
            names = re.findall(r"\\b([A-Za-z_]\\w*)\\b", decl_text)
            # names includes 'wire'/'reg' etc; keep last tokens after kind
            for n in names:
                if n in ("wire", "reg", "signed", "unsigned"):
                    continue
                if kind == "wire":
                    wires.setdefault(n, width)
                else:
                    regs.setdefault(n, width)
        elif t.data == "assign_stmt":
            stmt = slice_text(t.meta)
            # "assign lhs = rhs"
            _, rest = stmt.split("assign", 1)
            lhs, rhs = rest.split("=", 1)
            assigns.append((lhs.strip(), rhs.strip()))
        elif t.data == "always_stmt":
            sens_tree = t.children[0]
            body_tree = t.children[1]
            body_src = slice_text(body_tree.meta)
            if isinstance(sens_tree, Tree) and sens_tree.data == "sens_all":
                always_comb.append(body_src)
            elif isinstance(sens_tree, Tree) and sens_tree.data == "sens_posedge":
                clk = str(sens_tree.children[0])
                always_seq.append((clk, body_src))

        for c in t.children:
            if isinstance(c, Tree):
                collect(c)

    collect(tree)

    if not name:
        raise ParserError(f"Syntax error: cannot find module name in {path}")

    return MyVModule(
        name=name,
        inputs=inputs,
        outputs=outputs,
        regs=regs,
        wires=wires,
        assigns=assigns,
        always_comb=always_comb,
        always_seq=always_seq,
        params=params,
    )

