"""
Logical Operations Parser - Phép toán logic

Hỗ trợ các phép toán:
- LAND (&&): Logical AND
- LOR (||): Logical OR
- LNOT (!): Logical NOT

Khác biệt với Bitwise:
- Logical operators trả về 1-bit result (true/false)
- Bitwise operators làm việc trên từng bit

Example:
    4'b1010 && 4'b0011 = 1'b1  (cả 2 đều khác 0)
    4'b1010 & 4'b0011 = 4'b0010 (AND từng bit)
"""

from ..core.node_builder import NodeBuilder


def parse_logical_operation(
    node_builder: NodeBuilder,
    operator: str,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse phép toán logic.
    
    Args:
        node_builder: NodeBuilder instance
        operator: Toán tử (&&, ||, !)
        lhs: Output signal
        rhs: Expression
    """
    # Map operator sang node type
    op_map = {
        '&&': 'LAND',
        '||': 'LOR',
        '!': 'LNOT'
    }
    
    node_type = op_map.get(operator)
    if not node_type:
        raise ValueError(f"Invalid logical operator: {operator}")
    
    # NOT là unary operator
    if operator == '!':
        operand = rhs.lstrip('!').strip()
        operands = [operand]
    else:
        # AND, OR là binary operators
        operands = [op.strip() for op in rhs.split(operator)]
        
        if len(operands) != 2:
            raise ValueError(f"Logical {operator} requires 2 operands")
    
    # Tạo operation node + buffer
    node_builder.create_operation_with_buffer(
        node_type=node_type,
        operands=operands,
        output_signal=lhs
    )


def parse_logical_and(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Logical AND (&&).
    
    Example:
        assign valid = enable && ready;
        -> Tạo LAND node với inputs [enable, ready]
        
    Kết quả:
        - 1 nếu cả 2 operands != 0
        - 0 nếu ít nhất 1 operand = 0
    """
    parse_logical_operation(node_builder, '&&', lhs, rhs)


def parse_logical_or(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Logical OR (||).
    
    Example:
        assign flag = error || warning;
        -> Tạo LOR node với inputs [error, warning]
        
    Kết quả:
        - 1 nếu ít nhất 1 operand != 0
        - 0 nếu cả 2 operands = 0
    """
    parse_logical_operation(node_builder, '||', lhs, rhs)


def parse_logical_not(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Logical NOT (!).
    
    Example:
        assign not_ready = !ready;
        -> Tạo LNOT node với input [ready]
        
    Kết quả:
        - 1 nếu operand = 0
        - 0 nếu operand != 0
    """
    parse_logical_operation(node_builder, '!', lhs, rhs)


def detect_logical_operator(expression: str) -> str:
    """
    Phát hiện logical operator trong expression.
    
    Thứ tự check:
    1. && và || (multi-char)
    2. ! (single-char)
    
    Args:
        expression: Expression cần check
        
    Returns:
        Operator string nếu tìm thấy, None nếu không có
    """
    # Check multi-char operators first
    if '&&' in expression:
        return '&&'
    if '||' in expression:
        return '||'
    
    # Check unary NOT
    # Phải cẩn thận vì ! cũng có thể là != (not equal)
    if '!' in expression and '!=' not in expression:
        # Check xem ! có ở đầu không (unary)
        stripped = expression.strip()
        if stripped.startswith('!'):
            return '!'
    
    return None


def has_logical_operator(expression: str) -> bool:
    """Check xem có logical operator không."""
    return detect_logical_operator(expression) is not None


def is_pure_logical(expression: str) -> bool:
    """
    Check xem expression có phải pure logical không.
    
    Returns:
        True nếu chỉ có logical operators, không có arithmetic/bitwise
    """
    has_logical = has_logical_operator(expression)
    has_other = any(op in expression for op in [
        '+', '-', '*', '/', '%',  # Arithmetic
        '&', '|', '^', '~'          # Bitwise (nhưng cần check kỹ vì && và ||)
    ])
    
    # Special check: && và || không phải là & và |
    if '&&' in expression or '||' in expression:
        has_other = any(op in expression for op in ['+', '-', '*', '/', '%', '^', '~'])
    
    return has_logical and not has_other

