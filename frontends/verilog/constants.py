"""
Verilog Parser Constants - Regex Patterns và Hằng Số

File này chứa tất cả các regex patterns và hằng số được sử dụng
trong quá trình parse Verilog code.

Tổ chức:
1. Regex Patterns: Compiled regex cho performance tốt hơn
2. Operator Precedence: Thứ tự ưu tiên của operators
3. Node Type Mapping: Map từ operator sang node type
"""

import re
from typing import Dict, Set, List

# ============================================================================
# REGEX PATTERNS - Compiled để tăng performance
# ============================================================================

# Module patterns
MODULE_PATTERN = re.compile(r'module\s+(\w+)\s*\(([^)]*)\)\s*;', re.DOTALL)
ENDMODULE_PATTERN = re.compile(r'endmodule')

# Port declarations - Vector
INPUT_VECTOR_PATTERN = re.compile(r'input\s+\[(\d+):(\d+)\]\s+([^;]+)', re.MULTILINE)
OUTPUT_VECTOR_PATTERN = re.compile(r'output\s+\[(\d+):(\d+)\]\s+([^;]+)', re.MULTILINE)
PORT_INPUT_VECTOR_PATTERN = re.compile(r'input\s+\[(\d+):(\d+)\]\s+([^\n]+?)(?:,\s*$|\n)', re.MULTILINE)
PORT_OUTPUT_VECTOR_PATTERN = re.compile(r'output\s+\[(\d+):(\d+)\]\s+([^\n]+?)(?:,\s*$|\n)', re.MULTILINE)

# Port declarations - Scalar
INPUT_SCALAR_PATTERN = re.compile(r'input\s+([^[;]+);')
OUTPUT_SCALAR_PATTERN = re.compile(r'output\s+([^[;]+);')
PORT_INPUT_SCALAR_PATTERN = re.compile(r'input\s+([^[,\n)]+)')
PORT_OUTPUT_SCALAR_PATTERN = re.compile(r'output\s+([^[,\n)]+)')

# Wire declarations
WIRE_VECTOR_ASSIGN_PATTERN = re.compile(r'wire\s+\[(\d+):(\d+)\]\s+([^=]+)\s*=\s*([^;]+);')
WIRE_SCALAR_ASSIGN_PATTERN = re.compile(r'wire\s+([^[=]+)\s*=\s*([^;]+);')
WIRE_VECTOR_PATTERN = re.compile(r'wire\s+\[(\d+):(\d+)\]\s+([^;=]+);')
WIRE_SCALAR_PATTERN = re.compile(r'wire\s+([^[;=]+);')

# Assign statements
ASSIGN_PATTERN = re.compile(r'assign\s+([^=]+)\s*=\s*([^;]+);')

# Gate instantiations
GATE_PATTERN = re.compile(r'(and|or|xor|nand|nor|not|buf)\s+(\w+)?\s*\(([^)]+)\);')

# Module instantiations
MODULE_INST_PATTERN = re.compile(r'(\w+)\s+(\w+)\s*\(')

# Comments
SINGLE_LINE_COMMENT = re.compile(r'//.*$', re.MULTILINE)
MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)

# Bit slice/index
BIT_INDEX_PATTERN = re.compile(r'(\w+)\[(\d+)\]')
BIT_SLICE_PATTERN = re.compile(r'\w+\s*\[[^\]]+\]')

# Concatenation
CONCAT_PATTERN = re.compile(r'^\{.*\}$')

# ============================================================================
# OPERATOR SETS - Nhóm operators theo loại
# ============================================================================

# Arithmetic operators (Toán tử số học)
ARITHMETIC_OPS = {'+', '-', '*', '/', '%'}

# Bitwise operators (Toán tử bitwise)
BITWISE_OPS = {'&', '|', '^', '~', '~&', '~|', '~^', '^~'}

# Logical operators (Toán tử logic)
LOGICAL_OPS = {'&&', '||', '!'}

# Comparison operators (Toán tử so sánh)
COMPARISON_OPS = {'==', '!=', '<', '>', '<=', '>='}

# Shift operators (Toán tử dịch bit)
SHIFT_OPS = {'<<', '>>', '<<<', '>>>'}

# Special operators (Toán tử đặc biệt)
SPECIAL_OPS = {'?', ':', '{', '}', '[', ']'}

# All operators (Tất cả toán tử)
ALL_OPERATORS = ARITHMETIC_OPS | BITWISE_OPS | LOGICAL_OPS | COMPARISON_OPS | SHIFT_OPS

# ============================================================================
# OPERATOR PRECEDENCE - Thứ tự ưu tiên (cao -> thấp)
# ============================================================================

OPERATOR_PRECEDENCE = [
    # Precedence 1 (Highest) - Unary operators
    ['!', '~'],
    
    # Precedence 2 - Multiplication, division, modulo
    ['*', '/', '%'],
    
    # Precedence 3 - Addition, subtraction
    ['+', '-'],
    
    # Precedence 4 - Shift operators
    ['<<', '>>', '<<<', '>>>'],
    
    # Precedence 5 - Relational operators
    ['<', '<=', '>', '>='],
    
    # Precedence 6 - Equality operators
    ['==', '!='],
    
    # Precedence 7 - Bitwise AND
    ['&', '~&'],
    
    # Precedence 8 - Bitwise XOR
    ['^', '~^', '^~'],
    
    # Precedence 9 - Bitwise OR
    ['|', '~|'],
    
    # Precedence 10 - Logical AND
    ['&&'],
    
    # Precedence 11 - Logical OR
    ['||'],
    
    # Precedence 12 (Lowest) - Ternary operator
    ['?', ':'],
]

# ============================================================================
# NODE TYPE MAPPING - Map operator -> node type
# ============================================================================

OPERATOR_TO_NODE_TYPE = {
    # Arithmetic
    '+': 'ADD',
    '-': 'SUB',
    '*': 'MUL',
    '/': 'DIV',
    '%': 'MOD',
    
    # Bitwise
    '&': 'AND',
    '|': 'OR',
    '^': 'XOR',
    '~': 'NOT',
    '~&': 'NAND',
    '~|': 'NOR',
    '~^': 'XNOR',
    '^~': 'XNOR',
    
    # Logical
    '&&': 'LAND',
    '||': 'LOR',
    '!': 'LNOT',
    
    # Comparison
    '==': 'EQ',
    '!=': 'NE',
    '<': 'LT',
    '<=': 'LE',
    '>': 'GT',
    '>=': 'GE',
    
    # Shift
    '<<': 'SHL',
    '>>': 'SHR',
    '<<<': 'ASHL',
    '>>>': 'ASHR',
}

# ============================================================================
# GATE TYPES - Standard Verilog gates
# ============================================================================

STANDARD_GATES = {
    'and', 'or', 'xor', 'nand', 'nor', 'not', 'buf',
    'xnor',  # XNOR gate
}

# ============================================================================
# NODE CATEGORIES - Phân loại nodes cho statistics
# ============================================================================

NODE_CATEGORIES = {
    'logic': {'AND', 'OR', 'XOR', 'NAND', 'NOR', 'NOT', 'BUF', 'XNOR'},
    'arith': {'ADD', 'SUB', 'MUL', 'DIV', 'MOD'},
    'shift': {'SHL', 'SHR', 'ASHL', 'ASHR'},
    'compare': {'EQ', 'NE', 'LT', 'LE', 'GT', 'GE'},
    'logical': {'LAND', 'LOR', 'LNOT'},
    'struct': {'MUX', 'CONCAT', 'SLICE', 'MODULE', 'COMPLEX'},
}

# ============================================================================
# PARSING CONFIGURATION
# ============================================================================

# Có tạo BUF node cho mọi output không
CREATE_BUFFER_NODES = True

# Có validate input không
ENABLE_VALIDATION = True

# Có tạo wire connections tự động không
AUTO_GENERATE_WIRES = True

# Có tính toán statistics không
COMPUTE_STATISTICS = True

