"""
Shift Operations Parser - Phép toán dịch bit

Hỗ trợ các phép toán:
- SHL (<<): Logical Shift Left (dịch trái logic)
- SHR (>>): Logical Shift Right (dịch phải logic)
- ASHL (<<<): Arithmetic Shift Left (dịch trái số học)
- ASHR (>>>): Arithmetic Shift Right (dịch phải số học)

Khác biệt:
- Logical shift: Điền 0 vào các bit trống
- Arithmetic shift: Giữ nguyên sign bit (bit dấu) khi dịch phải

Example:
    8'b11000101 >> 2  = 8'b00110001  (logical, điền 0)
    8'sb11000101 >>> 2 = 8'sb11110001 (arithmetic, giữ sign bit 1)
"""

from ..node_builder import NodeBuilder


def parse_shift_operation(
    node_builder: NodeBuilder,
    operator: str,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse phép toán shift.
    
    Args:
        node_builder: NodeBuilder instance
        operator: Toán tử (<<, >>, <<<, >>>)
        lhs: Output signal
        rhs: Expression
    """
    # Map operator sang node type
    op_map = {
        '<<': 'SHL',
        '>>': 'SHR',
        '<<<': 'ASHL',
        '>>>': 'ASHR'
    }
    
    node_type = op_map.get(operator)
    if not node_type:
        raise ValueError(f"Invalid shift operator: {operator}")
    
    # Split operands
    operands = [op.strip() for op in rhs.split(operator)]
    
    if len(operands) != 2:
        raise ValueError(f"Shift operation requires 2 operands (value và shift amount)")
    
    # Tạo shift node + buffer
    node_builder.create_operation_with_buffer(
        node_type=node_type,
        operands=operands,
        output_signal=lhs
    )


def parse_shift_left(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Logical Shift Left (<<).
    
    Dịch trái n bits, điền 0 vào bên phải.
    
    Example:
        assign result = value << 2;
        value = 8'b00001111 -> result = 8'b00111100
    """
    parse_shift_operation(node_builder, '<<', lhs, rhs)


def parse_shift_right(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Logical Shift Right (>>).
    
    Dịch phải n bits, điền 0 vào bên trái.
    
    Example:
        assign result = value >> 2;
        value = 8'b11110000 -> result = 8'b00111100
    """
    parse_shift_operation(node_builder, '>>', lhs, rhs)


def parse_arithmetic_shift_left(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Arithmetic Shift Left (<<<).
    
    Giống như logical shift left trong hầu hết trường hợp.
    
    Example:
        assign result = value <<< 2;
    """
    parse_shift_operation(node_builder, '<<<', lhs, rhs)


def parse_arithmetic_shift_right(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """
    Parse Arithmetic Shift Right (>>>).
    
    Dịch phải nhưng giữ nguyên sign bit (bit dấu).
    Dùng cho signed numbers.
    
    Example:
        assign result = $signed(value) >>> 2;
        value = 8'sb11110000 (-16) -> result = 8'sb11111100 (-4)
    """
    parse_shift_operation(node_builder, '>>>', lhs, rhs)


def detect_shift_operator(expression: str) -> str:
    """
    Phát hiện shift operator trong expression.
    
    Thứ tự check (từ dài đến ngắn):
    1. Three-char operators: <<<, >>>
    2. Two-char operators: <<, >>
    
    Args:
        expression: Expression cần check
        
    Returns:
        Operator string nếu tìm thấy, None nếu không có
    """
    # Check three-char operators first (để tránh nhầm với two-char)
    if '<<<' in expression:
        return '<<<'
    if '>>>' in expression:
        return '>>>'
    
    # Check two-char operators
    if '<<' in expression:
        return '<<'
    if '>>' in expression:
        return '>>'
    
    return None


def has_shift_operator(expression: str) -> bool:
    """Check xem có shift operator không."""
    return detect_shift_operator(expression) is not None


def is_logical_shift(operator: str) -> bool:
    """Check xem có phải logical shift không (<<, >>)."""
    return operator in ['<<', '>>']


def is_arithmetic_shift(operator: str) -> bool:
    """Check xem có phải arithmetic shift không (<<<, >>>)."""
    return operator in ['<<<', '>>>']


def is_left_shift(operator: str) -> bool:
    """Check xem có phải left shift không (<<, <<<)."""
    return operator in ['<<', '<<<']


def is_right_shift(operator: str) -> bool:
    """Check xem có phải right shift không (>>, >>>)."""
    return operator in ['>>', '>>>']

