"""
Comparison Operations Parser - Phép toán so sánh

Hỗ trợ các phép toán:
- EQ (==): Equal (bằng)
- NE (!=): Not Equal (khác)
- LT (<): Less Than (nhỏ hơn)
- LE (<=): Less or Equal (nhỏ hơn hoặc bằng)
- GT (>): Greater Than (lớn hơn)
- GE (>=): Greater or Equal (lớn hơn hoặc bằng)

Kết quả: Tất cả trả về 1-bit (1 = true, 0 = false)
"""

from ..node_builder import NodeBuilder


def parse_comparison_operation(
    node_builder: NodeBuilder,
    operator: str,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse phép toán so sánh.
    
    Args:
        node_builder: NodeBuilder instance
        operator: Toán tử (==, !=, <, <=, >, >=)
        lhs: Output signal
        rhs: Expression
    """
    # Map operator sang node type
    op_map = {
        '==': 'EQ',
        '!=': 'NE',
        '<': 'LT',
        '<=': 'LE',
        '>': 'GT',
        '>=': 'GE'
    }
    
    node_type = op_map.get(operator)
    if not node_type:
        raise ValueError(f"Invalid comparison operator: {operator}")
    
    # Split operands
    operands = [op.strip() for op in rhs.split(operator)]
    
    if len(operands) != 2:
        raise ValueError(f"Comparison operation requires 2 operands")
    
    # Tạo comparison node + buffer
    node_builder.create_operation_with_buffer(
        node_type=node_type,
        operands=operands,
        output_signal=lhs
    )


def parse_equality(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Equal (==).
    
    Example:
        assign is_equal = (a == b);
        -> Tạo EQ node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '==', lhs, rhs)


def parse_not_equal(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Not Equal (!=).
    
    Example:
        assign is_different = (a != b);
        -> Tạo NE node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '!=', lhs, rhs)


def parse_less_than(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Less Than (<).
    
    Example:
        assign is_less = (a < b);
        -> Tạo LT node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '<', lhs, rhs)


def parse_less_or_equal(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Less or Equal (<=).
    
    Example:
        assign is_le = (a <= b);
        -> Tạo LE node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '<=', lhs, rhs)


def parse_greater_than(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Greater Than (>).
    
    Example:
        assign is_greater = (a > b);
        -> Tạo GT node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '>', lhs, rhs)


def parse_greater_or_equal(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse phép Greater or Equal (>=).
    
    Example:
        assign is_ge = (a >= b);
        -> Tạo GE node với inputs [a, b]
    """
    parse_comparison_operation(node_builder, '>=', lhs, rhs)


def detect_comparison_operator(expression: str) -> str:
    """
    Phát hiện comparison operator trong expression.
    
    Thứ tự check (từ dài đến ngắn để tránh false positive):
    1. Two-char operators: ==, !=, <=, >=
    2. Single-char operators: <, >
    
    Args:
        expression: Expression cần check
        
    Returns:
        Operator string nếu tìm thấy, None nếu không có
    """
    # Check two-char operators first
    two_char_ops = ['==', '!=', '<=', '>=']
    for op in two_char_ops:
        if op in expression:
            return op
    
    # Check single-char operators
    if '<' in expression:
        return '<'
    if '>' in expression:
        return '>'
    
    return None


def has_comparison_operator(expression: str) -> bool:
    """Check xem có comparison operator không."""
    return detect_comparison_operator(expression) is not None


def is_relational(operator: str) -> bool:
    """
    Check xem có phải relational operator không (<, <=, >, >=).
    
    Khác với equality operators (==, !=).
    """
    return operator in ['<', '<=', '>', '>=']


def is_equality(operator: str) -> bool:
    """Check xem có phải equality operator không (==, !=)."""
    return operator in ['==', '!=']

