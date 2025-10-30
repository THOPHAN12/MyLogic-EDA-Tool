"""
Bitwise Operations Parser - Phép toán bitwise

Hỗ trợ các phép toán:
- AND (&): Phép AND từng bit
- OR (|): Phép OR từng bit  
- XOR (^): Phép XOR từng bit
- NOT (~): Phép NOT (đảo bit)
- NAND (~&): Phép NAND
- NOR (~|): Phép NOR
- XNOR (~^ hoặc ^~): Phép XNOR

Lưu ý:
- Các phép 2 toán tử: &, |, ^, ~&, ~|, ~^, ^~
- Phép 1 toán tử: ~
- XOR có thể chain: a ^ b ^ c
"""

from typing import List
from ..core.node_builder import NodeBuilder


def parse_bitwise_operation(
    node_builder: NodeBuilder,
    operator: str,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse phép toán bitwise (2 operands).
    
    Args:
        node_builder: NodeBuilder instance
        operator: Toán tử (&, |, ^, ~&, ~|, ~^, ^~)
        lhs: Output signal
        rhs: Expression
    """
    # Map operator sang node type
    op_map = {
        '&': 'AND',
        '|': 'OR',
        '^': 'XOR',
        '~&': 'NAND',
        '~|': 'NOR',
        '~^': 'XNOR',
        '^~': 'XNOR'
    }
    
    node_type = op_map.get(operator)
    if not node_type:
        raise ValueError(f"Invalid bitwise operator: {operator}")
    
    # Split operands
    operands = [op.strip() for op in rhs.split(operator)]
    
    if len(operands) < 2:
        raise ValueError(f"Bitwise operation requires at least 2 operands")
    
    # Xử lý XOR chain (a ^ b ^ c)
    if operator == '^' and len(operands) > 2:
        _parse_xor_chain(node_builder, lhs, operands)
    else:
        # Normal binary operation
        node_builder.create_operation_with_buffer(
            node_type=node_type,
            operands=operands[:2],  # Lấy 2 operands đầu
            output_signal=lhs
        )


def parse_and_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép AND (&).
    
    Example:
        assign out = a & b;
        -> Tạo AND node với inputs [a, b]
    """
    parse_bitwise_operation(node_builder, '&', lhs, rhs)


def parse_or_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép OR (|).
    
    Example:
        assign out = a | b;
        -> Tạo OR node với inputs [a, b]
    """
    parse_bitwise_operation(node_builder, '|', lhs, rhs)


def parse_xor_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép XOR (^).
    
    Hỗ trợ cả XOR chain: a ^ b ^ c
    
    Example:
        assign out = a ^ b;
        assign sum = a ^ b ^ cin;  # XOR chain
    """
    parse_bitwise_operation(node_builder, '^', lhs, rhs)


def parse_not_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép NOT (~).
    
    Đây là phép unary (1 operand).
    
    Example:
        assign out = ~a;
        -> Tạo NOT node với input [a]
    """
    # Loại bỏ ~ và lấy operand
    operand = rhs.replace('~', '').strip()
    
    # Tạo NOT node + buffer
    node_builder.create_operation_with_buffer(
        node_type='NOT',
        operands=[operand],
        output_signal=lhs
    )


def parse_nand_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """Parse phép NAND (~&)."""
    parse_bitwise_operation(node_builder, '~&', lhs, rhs)


def parse_nor_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """Parse phép NOR (~|)."""
    parse_bitwise_operation(node_builder, '~|', lhs, rhs)


def parse_xnor_operation(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép XNOR (~^ hoặc ^~).
    
    Verilog hỗ trợ cả 2 cú pháp cho XNOR.
    """
    # Tìm operator nào được dùng
    if '~^' in rhs:
        operator = '~^'
    elif '^~' in rhs:
        operator = '^~'
    else:
        raise ValueError("No XNOR operator found in expression")
    
    parse_bitwise_operation(node_builder, operator, lhs, rhs)


def _parse_xor_chain(
    node_builder: NodeBuilder,
    output: str,
    operands: List[str]
) -> None:
    """
    Parse XOR chain (a ^ b ^ c ^ ...).
    
    XOR chain thường xuất hiện trong:
    - Parity generators
    - Checksums
    - Full adders (sum = a ^ b ^ cin)
    
    Args:
        node_builder: NodeBuilder instance
        output: Output signal
        operands: List tất cả operands trong chain
    """
    # Tạo XOR chain node với tất cả operands
    node_builder.create_operation_with_buffer(
        node_type='XOR',
        operands=operands,
        output_signal=output,
        extra_attrs={'chain': True}  # Đánh dấu là chain operation
    )


def detect_bitwise_operator(expression: str) -> str:
    """
    Phát hiện bitwise operator trong expression.
    
    Kiểm tra theo thứ tự:
    1. Multi-char operators (~&, ~|, ~^, ^~)
    2. Single-char operators (~, &, |, ^)
    
    Args:
        expression: Expression cần check
        
    Returns:
        Operator string nếu tìm thấy, None nếu không có
    """
    # Check multi-char operators first
    multi_char_ops = ['~&', '~|', '~^', '^~']
    for op in multi_char_ops:
        if op in expression:
            return op
    
    # Check single-char operators
    single_char_ops = ['~', '&', '|', '^']
    for op in single_char_ops:
        if op in expression:
            return op
    
    return None


def has_bitwise_operator(expression: str) -> bool:
    """Check xem có bitwise operator không."""
    return detect_bitwise_operator(expression) is not None


def is_pure_bitwise(expression: str) -> bool:
    """
    Check xem expression có phải pure bitwise không (không có arithmetic).
    
    Returns:
        True nếu chỉ có bitwise operators, không có +, -, *, /, %
    """
    has_bitwise = has_bitwise_operator(expression)
    has_arithmetic = any(op in expression for op in ['+', '-', '*', '/', '%'])
    
    return has_bitwise and not has_arithmetic

