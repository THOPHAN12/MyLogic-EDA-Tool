# frontends/verilog.py
"""
Simple Verilog frontend for combinational modules.

Supports:
 - module <name>(...);
 - input / output / wire declarations (scalar only)
 - assign lhs = expr;   (expr: identifiers, parentheses, ~, &, |, ^, *)
 - gate instantiation:
      and inst_name (out, in1, in2);
      or  inst_name (out, in1, in2);
      xor inst_name (out, in1, in2);
      nand/nor/not/buf
  instance name is optional: and (out, in1, in2);
Returns a dict:
{
  "name": str,
  "inputs": [...],
  "outputs": [...],
  "wires": [...],
  "nodes": [
     {"id":"n1","type":"AND","fanins":[["a",False],["b",False]]}, ...
  ],
  "attrs": {"source_file": path}
}
"""
from __future__ import annotations
import re
from typing import List, Tuple, Dict

# Global id counter for unique temporary node ids
GLOBAL_ID_COUNTER = 0
def _global_new_id(prefix="n"):
    global GLOBAL_ID_COUNTER
    GLOBAL_ID_COUNTER += 1
    return f"{prefix}{GLOBAL_ID_COUNTER}"

# Operator precedence (higher -> binds tighter)
_OP_PRECEDENCE = {
    '~': 6,
    '*': 5,
    '&': 4,
    '^': 3,
    '|': 2,
}

class ParseError(Exception):
    pass

# Token regex: identifiers, single-char ops, parentheses, commas
_TOKEN_RE = re.compile(r'\s*([A-Za-z_]\w*|[~&\|\^\*\(\),;])')

def _remove_comments(src: str) -> str:
    # remove block comments and line comments
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.S)
    src = re.sub(r'//.*?$', '', src, flags=re.M)
    return src

def _tokenize(s: str) -> List[str]:
    tokens = []
    pos = 0
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m:
            # skip whitespace
            if s[pos].isspace():
                pos += 1
                continue
            raise ParseError(f"Unexpected token at pos {pos}: {s[pos:pos+20]!r}")
        tok = m.group(1)
        tokens.append(tok)
        pos = m.end()
    return tokens

# Pratt / precedence-climbing parser for expressions
def _parse_primary(tokens: List[str], i: int = 0):
    if i >= len(tokens):
        raise ParseError("Unexpected end of expression")
    tok = tokens[i]
    if tok == '~':
        node, j = _parse_primary(tokens, i+1)
        return ('NOT', node), j
    if tok == '(':
        node, j = _parse_expr(tokens, i+1, 0)
        if j >= len(tokens) or tokens[j] != ')':
            raise ParseError("Missing closing parenthesis")
        return node, j+1
    if re.match(r'[A-Za-z_]\w*', tok):
        return ('VAR', tok), i+1
    raise ParseError(f"Unexpected token in primary expr: {tok}")

def _parse_expr(tokens: List[str], i: int = 0, min_prec: int = 0):
    left, i = _parse_primary(tokens, i)
    while i < len(tokens):
        op = tokens[i]
        if op not in _OP_PRECEDENCE:
            break
        prec = _OP_PRECEDENCE[op]
        # left-associative for binary ops
        if prec < min_prec:
            break
        # consume op
        i += 1
        # parse right operand with higher precedence (prec+1 for left-assoc)
        right, i = _parse_expr(tokens, i, prec + 1)
        left = (op, left, right)
    return left, i

def _expr_to_nodes(expr, net, id_prefix="e"):
    """
    Convert parsed expr AST to netlist nodes appended into net['nodes'].
    Return the net name (signal id) that holds the expression result.
    AST nodes:
      ('VAR', name)
      ('NOT', sub)
      ('&'|'|'|'^', left, right)
    """
    typ = expr[0]
    if typ == 'VAR':
        return expr[1]
    if typ == 'NOT':
        sub = expr[1]
        sub_id = _expr_to_nodes(sub, net, id_prefix)
        nid = _global_new_id(prefix=id_prefix+"_")
        net['nodes'].append({"id": nid, "type": "NOT", "fanins": [[sub_id, False]]})
        return nid
    if typ in ('&','|','^','*'):
        left = expr[1]
        right = expr[2]
        l_id = _expr_to_nodes(left, net, id_prefix)
        r_id = _expr_to_nodes(right, net, id_prefix)
        nid = _global_new_id(prefix=id_prefix+"_")
        typmap = {'&':'AND','|':'OR','^':'XOR','*':'MULT'}
        net['nodes'].append({"id": nid, "type": typmap[typ], "fanins": [[l_id, False],[r_id, False]]})
        return nid
    raise ParseError(f"Unsupported expr AST: {expr}")

def _strip_semicolon_and_spaces(s: str) -> str:
    return s.strip().rstrip(';').strip()

def parse_verilog_file(path: str) -> Dict:
    """Parse a Verilog file and return a netlist dictionary."""
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except FileNotFoundError:
        raise ParseError(f"File not found: {path}")
    except IOError as e:
        raise ParseError(f"Error reading file '{path}': {e}")

    src = _remove_comments(src)

    m = re.search(r'\bmodule\s+([A-Za-z_]\w*)\s*\((.*?)\)\s*;(.*)\bendmodule\b', src, flags=re.S)
    if not m:
        raise ParseError("No module found or unsupported module syntax")
    module_name = m.group(1)
    port_list = m.group(2)
    body = m.group(3)

    net = {
        "name": module_name,
        "inputs": [],
        "outputs": [],
        "wires": [],
        "nodes": [],
        "attrs": {"source_file": path}
    }

    # parse declarations: input/output/wire (scalar, comma separated)
    for decl in re.finditer(r'\b(input|output|wire)\b\s+([^;]+);', body):
        typ = decl.group(1)
        names = decl.group(2)
        items = [n.strip() for n in names.split(',') if n.strip()]
        if typ == 'input':
            net['inputs'].extend(items)
        elif typ == 'output':
            net['outputs'].extend(items)
        elif typ == 'wire':
            net['wires'].extend(items)

    # parse assign statements
    for am in re.finditer(r'\bassign\b\s+([^;]+);', body):
        stmt = am.group(1).strip()
        if '=' not in stmt:
            continue
        lhs, rhs = stmt.split('=',1)
        lhs = _strip_semicolon_and_spaces(lhs)
        rhs = _strip_semicolon_and_spaces(rhs)
        tokens = _tokenize(rhs)
        tokens = [t for t in tokens if t != ',']
        expr_ast, idx = _parse_expr(tokens, 0, 0)
        # ignore trailing tokens
        result_id = _expr_to_nodes(expr_ast, net, id_prefix="e")
        if result_id != lhs:
            # create BUF node mapping result -> lhs
            net['nodes'].append({"id": lhs, "type": "BUF", "fanins": [[result_id, False]]})

    # parse gate instantiations: gate [inst_name] (out, in1, in2);
    # allow optional instance name
    for gm in re.finditer(r'\b(and|or|xor|nand|nor|not|buf)\b\s*(?:([A-Za-z_]\w*)\s*)?\(\s*([^)]+)\)\s*;', body, flags=re.I):
        gtype = gm.group(1).lower()
        inst = gm.group(2) or "<anon>"
        plist = gm.group(3)
        sigs = [s.strip() for s in re.split(r'\s*,\s*', plist) if s.strip()]
        if len(sigs) < 1:
            continue
        out = sigs[0]
        ins = sigs[1:]
        # build nodes (support multi-input and/or/xor by folding left->right)
        if gtype == 'not':
            if len(ins) != 1:
                raise ParseError(f"not {inst} expects 1 input")
            net['nodes'].append({"id": out, "type": "NOT", "fanins": [[ins[0], False]]})
        elif gtype == 'buf':
            if len(ins) != 1:
                raise ParseError(f"buf {inst} expects 1 input")
            net['nodes'].append({"id": out, "type": "BUF", "fanins": [[ins[0], False]]})
        elif gtype in ('and','or','xor'):
            if len(ins) == 0:
                raise ParseError(f"{gtype} {inst} has no inputs")
            cur = ins[0]
            for k in range(1, len(ins)):
                a = cur
                b = ins[k]
                nid = _global_new_id(prefix=f"g_{inst}_")
                typ = {"and":"AND","or":"OR","xor":"XOR"}[gtype]
                net['nodes'].append({"id": nid, "type": typ, "fanins": [[a, False],[b, False]]})
                cur = nid
            if cur != out:
                net['nodes'].append({"id": out, "type": "BUF", "fanins": [[cur, False]]})
        elif gtype in ('nand','nor'):
            if len(ins) == 0:
                raise ParseError(f"{gtype} {inst} has no inputs")
            cur = ins[0]
            for k in range(1, len(ins)):
                a = cur
                b = ins[k]
                nid = _global_new_id(prefix=f"g_{inst}_")
                typ = "AND" if gtype == "nand" else "OR"
                net['nodes'].append({"id": nid, "type": typ, "fanins": [[a, False],[b, False]]})
                cur = nid
            # output is inverted
            net['nodes'].append({"id": out, "type": "NOT", "fanins": [[cur, False]]})
        else:
            raise ParseError(f"Unsupported gate type {gtype}")

    # dedupe lists preserving order
    for k in ('inputs','outputs','wires'):
        seen = set()
        u = []
        for x in net[k]:
            if x not in seen:
                seen.add(x)
                u.append(x)
        net[k] = u

    return net


def get_verilog_stats(net: Dict) -> Dict[str, any]:
    """Get statistics about the parsed Verilog netlist."""
    nodes = list(net.get("nodes", []))
    gate_counts = {}
    
    for n in nodes:
        gate_type = str(n.get("type", "")).upper()
        gate_counts[gate_type] = gate_counts.get(gate_type, 0) + 1
    
    return {
        "name": net.get("name", "unknown"),
        "total_inputs": len(net.get("inputs", [])),
        "total_outputs": len(net.get("outputs", [])),
        "total_nodes": len(nodes),
        "total_wires": len(net.get("wires", [])),
        "gate_counts": gate_counts,
        "source_file": net.get("attrs", {}).get("source_file", "unknown"),
        "is_valid": True  # If we got here, parsing succeeded
    }


# Quick CLI for debugging
if __name__ == "__main__":
    import json, sys, argparse
    
    parser = argparse.ArgumentParser(prog="verilog-parser")
    parser.add_argument("file", help="Input Verilog file")
    parser.add_argument("--json", action="store_true", help="Print netlist as JSON")
    parser.add_argument("--stats", action="store_true", help="Show parsing statistics")
    args = parser.parse_args()
    
    try:
        nl = parse_verilog_file(args.file)
        
        if args.stats:
            stats = get_verilog_stats(nl)
            print(f"Verilog parse statistics:")
            print(f"  Module: {stats['name']}")
            print(f"  Inputs: {stats['total_inputs']}, Outputs: {stats['total_outputs']}, Nodes: {stats['total_nodes']}")
            print(f"  Wires: {stats['total_wires']}")
            if stats['gate_counts']:
                gate_summary = ", ".join([f"{k}: {v}" for k, v in sorted(stats['gate_counts'].items())])
                print(f"  Gates: {gate_summary}")
            print(f"  Source: {stats['source_file']}")
        
        if args.json:
            print(json.dumps(nl, indent=2))
        else:
            print("Module:", nl['name'])
            print("Inputs:", nl['inputs'])
            print("Outputs:", nl['outputs'])
            print("Wires:", nl['wires'])
            print("Nodes:")
            for n in nl['nodes']:
                print(" ", n)
                
    except ParseError as e:
        print(f"Parse error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
