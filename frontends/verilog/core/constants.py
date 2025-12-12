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

# Module patterns (hỗ trợ optional parameter list #(...) và ports)
MODULE_PATTERN = re.compile(
    r'module\s+(\w+)\s*(?:#\s*\(([^)]*)\))?\s*\(([^)]*)\)\s*;',
    re.DOTALL
)
ENDMODULE_PATTERN = re.compile(r'endmodule')

# Port declarations - Vector (hỗ trợ signed/unsigned và parameterized widths)
INPUT_VECTOR_PATTERN = re.compile(r'input\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^;]+)', re.MULTILINE)
OUTPUT_VECTOR_PATTERN = re.compile(r'output\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^;]+)', re.MULTILINE)
PORT_INPUT_VECTOR_PATTERN = re.compile(r'input\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^\n]+?)(?:,\s*$|\n)', re.MULTILINE)
PORT_OUTPUT_VECTOR_PATTERN = re.compile(r'output\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^\n]+?)(?:,\s*$|\n)', re.MULTILINE)

# Port declarations - Scalar (hỗ trợ signed/unsigned)
INPUT_SCALAR_PATTERN = re.compile(r'input\s+(?:signed\s+|unsigned\s+)?([^[;]+);')
OUTPUT_SCALAR_PATTERN = re.compile(r'output\s+(?:signed\s+|unsigned\s+)?([^[;]+);')
PORT_INPUT_SCALAR_PATTERN = re.compile(r'input\s+(?:signed\s+|unsigned\s+)?([^[,\n)]+)')
PORT_OUTPUT_SCALAR_PATTERN = re.compile(r'output\s+(?:signed\s+|unsigned\s+)?([^[,\n)]+)')

# Wire declarations (hỗ trợ signed/unsigned và parameterized widths)
WIRE_VECTOR_ASSIGN_PATTERN = re.compile(r'wire\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^=]+)\s*=\s*([^;]+);')
WIRE_SCALAR_ASSIGN_PATTERN = re.compile(r'wire\s+(?:signed\s+|unsigned\s+)?([^[=]+)\s*=\s*([^;]+);')
WIRE_VECTOR_PATTERN = re.compile(r'wire\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^;=]+);')
WIRE_SCALAR_PATTERN = re.compile(r'wire\s+(?:signed\s+|unsigned\s+)?([^[;=]+);')

# Reg declarations (sequential elements) - hỗ trợ signed/unsigned và parameterized widths
REG_VECTOR_PATTERN = re.compile(r'reg\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+([^;=]+);')
REG_SCALAR_PATTERN = re.compile(r'reg\s+(?:signed\s+|unsigned\s+)?([^[;=]+);')
REG_PATTERN = re.compile(r'reg\s+(?:signed\s+|unsigned\s+)?(?:\[([^\]]+):([^\]]+)\]\s+)?([^;=]+);')

# Memory declarations: reg [width-1:0] mem [depth-1:0];
# Hỗ trợ parameterized: reg [WIDTH-1:0] mem [DEPTH-1:0];
MEMORY_PATTERN = re.compile(
    r'reg\s+(?:signed\s+|unsigned\s+)?\[([^\]]+):([^\]]+)\]\s+(\w+)\s+\[([^\]]+):([^\]]+)\]\s*;',
    re.IGNORECASE
)

# Array indexing: mem[addr] hoặc mem[addr][bit]
ARRAY_INDEX_PATTERN = re.compile(r'(\w+)\s*\[([^\]]+)\](?:\s*\[([^\]]+)\])?')

# Assign statements
ASSIGN_PATTERN = re.compile(r'assign\s+([^=]+)\s*=\s*([^;]+);')

# Always blocks (Sequential circuits)
# Hỗ trợ cả begin...end và {...}
ALWAYS_PATTERN = re.compile(
    r'always\s+@\s*\(([^)]+)\)\s*(?:begin\s*(.*?)\s*end|\{(.*?)\})',
    re.DOTALL | re.MULTILINE
)

# Edge sensitivity patterns
POSEDGE_PATTERN = re.compile(r'posedge\s+(\w+)')
NEGEDGE_PATTERN = re.compile(r'negedge\s+(\w+)')
EDGE_PATTERN = re.compile(r'(?:posedge|negedge)\s+(\w+)')

# Non-blocking assignments (<=)
NON_BLOCKING_ASSIGN_PATTERN = re.compile(r'(\w+)\s*<=\s*([^;]+);')

# Blocking assignments (=) trong always blocks
BLOCKING_ASSIGN_PATTERN = re.compile(r'(\w+)\s*=\s*([^;]+);')

# Begin-end blocks
BEGIN_END_PATTERN = re.compile(r'begin\s*(.*?)\s*end', re.DOTALL)

# Gate instantiations
GATE_PATTERN = re.compile(r'(and|or|xor|nand|nor|not|buf)\s+(\w+)?\s*\(([^)]+)\);')

# Module instantiations
# Hỗ trợ cả ordered và named ports
MODULE_INST_PATTERN = re.compile(
    r'(\w+)\s+(\w+)?\s*\(([^)]+)\)\s*;',
    re.DOTALL
)
# Named port connections: .port_name(signal_name) hoặc .port_name({a, b}) hoặc .port_name(expr)
# Cải thiện để hỗ trợ nested parentheses và expressions phức tạp
NAMED_PORT_PATTERN = re.compile(r'\.(\w+)\s*\(([^)]+(?:\([^)]*\)[^)]*)*)\)')
# Ordered port (simple signal name hoặc expression)
ORDERED_PORT_PATTERN = re.compile(r'([^,]+?)(?:\s*,\s*|$)')

# Comments
SINGLE_LINE_COMMENT = re.compile(r'//.*$', re.MULTILINE)
MULTI_LINE_COMMENT = re.compile(r'/\*.*?\*/', re.DOTALL)

# Bit slice/index (hỗ trợ parameterized indices)
BIT_INDEX_PATTERN = re.compile(r'(\w+)\[(\d+)\]')
BIT_SLICE_PATTERN = re.compile(r'(\w+)\s*\[([^\]]+)\]')
# Bit slice với range: signal[msb:lsb]
BIT_SLICE_RANGE_PATTERN = re.compile(r'(\w+)\s*\[([^\]]+):([^\]]+)\]')
# Bit index đơn: signal[index]
BIT_INDEX_SINGLE_PATTERN = re.compile(r'(\w+)\s*\[([^\]]+)\]')

# Concatenation
CONCAT_PATTERN = re.compile(r'^\{.*\}$')

# Parameters & Localparams (hỗ trợ biểu thức số học)
PARAMETER_PATTERN = re.compile(r'parameter\s+(?:\[[^\]]+\]\s+)?(\w+)\s*=\s*([^;]+);')
LOCALPARAM_PATTERN = re.compile(r'localparam\s+(?:\[[^\]]+\]\s+)?(\w+)\s*=\s*([^;]+);')

# Signed/Unsigned keywords
SIGNED_KEYWORD = re.compile(r'\bsigned\b')
UNSIGNED_KEYWORD = re.compile(r'\bunsigned\b')

# Integer/Real/Time/Realtime
INTEGER_PATTERN = re.compile(r'integer\s+([^;]+);')
REAL_PATTERN = re.compile(r'real\s+([^;]+);')
TIME_PATTERN = re.compile(r'time\s+([^;]+);')
REALTIME_PATTERN = re.compile(r'realtime\s+([^;]+);')

# If-Else statements
IF_PATTERN = re.compile(
    r'if\s*\(([^)]+)\)\s*(?:begin\s*(.*?)\s*end|\s*([^;]+);)',
    re.DOTALL
)
IF_ELSE_PATTERN = re.compile(
    r'if\s*\(([^)]+)\)\s*(?:begin\s*(.*?)\s*end|\s*([^;]+);)\s*else\s*(?:begin\s*(.*?)\s*end|\s*([^;]+);)',
    re.DOTALL
)

# Case statements (hỗ trợ case, casex, casez)
CASE_PATTERN = re.compile(
    r'case\s*(x|z)?\s*\(([^)]+)\)\s*(.*?)\s*endcase',
    re.DOTALL | re.IGNORECASE
)
# Case item pattern: hỗ trợ single value, range, default
# Examples: 4'b1010: ..., 4:7: ..., default: ...
CASE_ITEM_PATTERN = re.compile(
    r'(default|\d+\s*:\s*\d+|\d+\'[bdhx]\w+|\d+|\w+)\s*:\s*([^;]+);',
    re.IGNORECASE
)
# Case item với begin-end block
CASE_ITEM_BLOCK_PATTERN = re.compile(
    r'(default|\d+\s*:\s*\d+|\d+\'[bdhx]\w+|\d+|\w+)\s*:\s*begin\s*(.*?)\s*end',
    re.DOTALL | re.IGNORECASE
)

# For loops
FOR_PATTERN = re.compile(
    r'for\s*\(\s*([^;]+);\s*([^;]+);\s*([^)]+)\)\s*(?:begin\s*(.*?)\s*end|\s*([^;]+);)',
    re.DOTALL
)

# While loops
WHILE_PATTERN = re.compile(
    r'while\s*\(([^)]+)\)\s*(?:begin\s*(.*?)\s*end|\s*([^;]+);)',
    re.DOTALL
)

# Functions & Tasks (hỗ trợ parameterized widths và signed)
FUNCTION_PATTERN = re.compile(
    r'function\s+(?:automatic\s+)?(?:signed\s+|unsigned\s+)?(?:\[([^\]]+):([^\]]+)\]\s+)?(\w+)\s*;.*?endfunction',
    re.DOTALL | re.IGNORECASE
)
TASK_PATTERN = re.compile(
    r'task\s+(?:automatic\s+)?(\w+)\s*;.*?endtask',
    re.DOTALL | re.IGNORECASE
)

# Function/Task calls: func_name(args) hoặc task_name(args);
FUNCTION_CALL_PATTERN = re.compile(r'(\w+)\s*\(([^)]*)\)')
TASK_CALL_PATTERN = re.compile(r'(\w+)\s*\(([^)]*)\)\s*;')

# Generate blocks
GENERATE_PATTERN = re.compile(
    r'generate\s*(.*?)\s*endgenerate',
    re.DOTALL
)
GENVAR_PATTERN = re.compile(r'genvar\s+(\w+);')

# Compiler directives
DEFINE_PATTERN = re.compile(r'`define\s+(\w+)\s+(.+)')
INCLUDE_PATTERN = re.compile(r'`include\s+"([^"]+)"')
IFDEF_PATTERN = re.compile(r'`ifdef\s+(\w+)')
IFNDEF_PATTERN = re.compile(r'`ifndef\s+(\w+)')
TIMESCALE_PATTERN = re.compile(r'`timescale\s+(\d+)\s*(\w+)\s*/\s*(\d+)\s*(\w+)')
UNDEF_PATTERN = re.compile(r'`undef\s+(\w+)')

# System tasks & functions
SYSTEM_TASK_PATTERN = re.compile(r'\$(\w+)\s*\(([^)]*)\);')

# Attributes
ATTRIBUTE_PATTERN = re.compile(r'\(\*([^)]+)\*\)')

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
    'sequential': {'DFF', 'REG', 'LATCH', 'DFFR', 'DFFS'},  # Sequential elements
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

