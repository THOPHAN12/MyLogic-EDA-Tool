"""
Verilog Operations Parsers

Module này chứa các parser cho từng loại operation trong Verilog:
- arithmetic.py: Phép toán số học (+, -, *, /, %)
- bitwise.py: Phép toán bitwise (&, |, ^, ~, NAND, NOR, XNOR)
- logical.py: Phép toán logic (&&, ||, !)
- comparison.py: Phép so sánh (==, !=, <, >, <=, >=)
- shift.py: Phép dịch bit (<<, >>, <<<, >>>)
- special.py: Operators đặc biệt (ternary, concat, slice)

Tất cả parsers đều sử dụng NodeBuilder để tạo nodes.
"""

from .arithmetic import parse_arithmetic_operation
from .bitwise import parse_bitwise_operation
from .logical import parse_logical_operation
from .comparison import parse_comparison_operation
from .shift import parse_shift_operation
from .special import (
    parse_ternary_operation,
    parse_concatenation,
    parse_slice,
    is_ternary,
    is_concatenation,
    is_slice,
)

__all__ = [
    'parse_arithmetic_operation',
    'parse_bitwise_operation',
    'parse_logical_operation',
    'parse_comparison_operation',
    'parse_shift_operation',
    'parse_ternary_operation',
    'parse_concatenation',
    'parse_slice',
    'is_ternary',
    'is_concatenation',
    'is_slice',
]

