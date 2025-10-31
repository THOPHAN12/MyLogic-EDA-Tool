"""
Arithmetic Operations Parser - Phép toán số học

Hỗ trợ các phép toán:
- ADD (+): Phép cộng
- SUB (-): Phép trừ
- MUL (*): Phép nhân
- DIV (/): Phép chia
- MOD (%): Phép chia lấy dư

Mỗi operation tạo ra:
1. Operation node (ADD, SUB, etc.)
2. Buffer node để connect với output
"""

from typing import Dict
from ..core.node_builder import NodeBuilder


def parse_arithmetic_operation(
    node_builder: NodeBuilder,
    operator: str,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse phép toán số học.
    
    Args:
        node_builder: NodeBuilder instance để tạo nodes
        operator: Toán tử (+, -, *, /, %)
        lhs: Left-hand side (output signal)
        rhs: Right-hand side (expression)
    """
    # Map operator sang node type
    op_map = {
        '+': 'ADD',
        '-': 'SUB',
        '*': 'MUL',
        '/': 'DIV',
        '%': 'MOD'
    }
    
    node_type = op_map.get(operator)
    if not node_type:
        raise ValueError(f"Invalid arithmetic operator: {operator}")
    
    # Split operands bởi operator
    operands = [op.strip() for op in rhs.split(operator)]
    
    if len(operands) != 2:
        raise ValueError(f"Arithmetic operation requires 2 operands, got {len(operands)}")
    
    # Tạo operation node trực tiếp (không qua BUF)
    node_builder.create_operation_direct(
        node_type=node_type,
        operands=operands,
        output_signal=lhs
    )


def parse_addition(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép cộng (a + b).
    
    Example:
        assign sum = a + b;
        -> Tạo ADD node với inputs [a, b]
    """
    parse_arithmetic_operation(node_builder, '+', lhs, rhs)


def parse_subtraction(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép trừ (a - b).
    
    Example:
        assign diff = a - b;
        -> Tạo SUB node với inputs [a, b]
    """
    parse_arithmetic_operation(node_builder, '-', lhs, rhs)


def parse_multiplication(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép nhân (a * b).
    
    Example:
        assign prod = a * b;
        -> Tạo MUL node với inputs [a, b]
    """
    parse_arithmetic_operation(node_builder, '*', lhs, rhs)


def parse_division(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép chia (a / b).
    
    Example:
        assign quot = a / b;
        -> Tạo DIV node với inputs [a, b]
    """
    parse_arithmetic_operation(node_builder, '/', lhs, rhs)


def parse_modulo(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép chia lấy dư (a % b).
    
    Example:
        assign remainder = a % b;
        -> Tạo MOD node với inputs [a, b]
    """
    parse_arithmetic_operation(node_builder, '%', lhs, rhs)


def detect_arithmetic_operator(expression: str) -> str:
    """
    Phát hiện arithmetic operator trong expression.
    
    Kiểm tra theo thứ tự ưu tiên:
    1. Modulo (%)
    2. Multiplication (*) và Division (/)
    3. Addition (+) và Subtraction (-)
    
    Args:
        expression: Expression cần check
        
    Returns:
        Operator string nếu tìm thấy, None nếu không có
    """
    # Check modulo first (ít gặp nhất, tránh false positive)
    if '%' in expression:
        return '%'
    
    # Check multiplication và division
    if '*' in expression:
        return '*'
    if '/' in expression:
        return '/'
    
    # Check addition và subtraction cuối cùng
    # (phổ biến nhất, có thể xuất hiện trong nhiều context)
    if '+' in expression:
        return '+'
    if '-' in expression:
        return '-'
    
    return None


def has_arithmetic_operator(expression: str) -> bool:
    """
    Kiểm tra xem expression có chứa arithmetic operator không.
    
    Args:
        expression: Expression cần check
        
    Returns:
        True nếu có arithmetic operator
    """
    return detect_arithmetic_operator(expression) is not None

