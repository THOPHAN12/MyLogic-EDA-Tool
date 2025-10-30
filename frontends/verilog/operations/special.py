"""
Special Operations Parser - Các phép toán đặc biệt

Hỗ trợ:
1. Ternary Operator (?:): condition ? true_value : false_value
2. Concatenation ({}): {a, b, c}
3. Bit Slice ([]): signal[msb:lsb] hoặc signal[bit]

Đây là các operations phức tạp hơn, không phải arithmetic/bitwise đơn giản.
"""

import re
from typing import List
from ..node_builder import NodeBuilder


# ============================================================================
# TERNARY OPERATOR - Toán tử ba ngôi
# ============================================================================

def is_ternary(expression: str) -> bool:
    """
    Check xem expression có phải ternary operator không.
    
    Format: condition ? true_value : false_value
    
    Example:
        (a > b) ? a : b  -> True
        a + b            -> False
    """
    return '?' in expression and ':' in expression


def parse_ternary_operation(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse ternary operator: condition ? value1 : value2.
    
    Tạo MUX (multiplexer) node:
    - Condition quyết định chọn value1 hay value2
    - Output = value1 nếu condition = true
    - Output = value2 nếu condition = false
    
    Example:
        assign max = (a > b) ? a : b;
        -> MUX: select=(a>b), inputs=[a, b]
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Ternary expression
    """
    # Parse ternary: condition ? true_val : false_val
    # Simplified implementation: tạo MUX node
    
    mux_id = node_builder.create_operation_node(
        node_type='MUX',
        operands=[rhs.strip()],  # Lưu toàn bộ expression
        extra_attrs={'ternary': True}
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(mux_id, lhs)


# ============================================================================
# CONCATENATION - Nối bit
# ============================================================================

def is_concatenation(expression: str) -> bool:
    """
    Check xem expression có phải concatenation không.
    
    Format: {signal1, signal2, ...}
    
    Example:
        {a, b, c}    -> True
        {4'b1010, b} -> True
        a + b        -> False
    """
    expr = expression.strip()
    return expr.startswith('{') and expr.endswith('}')


def parse_concatenation(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse bit concatenation: {a, b, c, ...}.
    
    Nối các signals thành một signal lớn hơn.
    
    Example:
        assign result = {a[3:0], b[3:0]};
        Nếu a=4'b1010, b=4'b0011 -> result=8'b10100011
        
    Bit order: Signal đầu tiên là MSB
        {a, b} -> [a_bits, b_bits]
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Concatenation expression {a, b, ...}
    """
    # Loại bỏ dấu ngoặc {} và split bởi comma
    inner = rhs.strip()[1:-1].strip()
    
    # Split by comma (không xử lý nested braces - simplified)
    parts = [p.strip() for p in inner.split(',') if p.strip()]
    
    # Tạo CONCAT node
    concat_id = node_builder.create_operation_node(
        node_type='CONCAT',
        operands=parts
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(concat_id, lhs)


# ============================================================================
# BIT SLICE/INDEX - Truy cập bit
# ============================================================================

def is_slice(expression: str) -> bool:
    """
    Check xem expression có phải bit slice/index không.
    
    Formats:
        signal[bit]       - Single bit
        signal[msb:lsb]   - Bit range
        
    Example:
        data[7:0]  -> True
        flags[3]   -> True
        a + b      -> False
    """
    return bool(re.search(r'\w+\s*\[[^\]]+\]', expression))


def parse_slice(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse bit slice/index.
    
    Formats:
        signal[bit]       - Truy cập 1 bit
        signal[msb:lsb]   - Truy cập dải bit
        
    Example:
        assign lsb = data[0];        # Bit 0
        assign high = data[7:4];     # Bits 7-4
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Slice expression
    """
    # Tạo SLICE node
    slice_id = node_builder.create_operation_node(
        node_type='SLICE',
        operands=[rhs.strip()]
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(slice_id, lhs)


# ============================================================================
# REPLICATION - Nhân bản bit
# ============================================================================

def is_replication(expression: str) -> bool:
    """
    Check xem có phải replication không.
    
    Format: {count{signal}}
    
    Example:
        {4{1'b1}}  -> 4'b1111
        {3{a}}     -> {a, a, a}
    """
    return bool(re.match(r'\{\d+\{.+\}\}', expression.strip()))


def parse_replication(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse bit replication: {count{signal}}.
    
    Nhân bản signal n lần.
    
    Example:
        assign zeros = {4{1'b0}};  # 4'b0000
        assign rep = {3{a}};       # {a, a, a}
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Replication expression
    """
    # Tạo REPLICATION node (hoặc có thể expand thành CONCAT)
    rep_id = node_builder.create_operation_node(
        node_type='CONCAT',
        operands=[rhs.strip()],
        extra_attrs={'replication': True}
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(rep_id, lhs)


# ============================================================================
# COMPLEX EXPRESSIONS - Biểu thức phức tạp
# ============================================================================

def is_complex_expression(expression: str) -> bool:
    """
    Check xem expression có phải complex expression không (có parentheses).
    
    Example:
        (a & b) | (c & d)  -> True
        a + b              -> False
    """
    return '(' in expression and ')' in expression


def parse_complex_expression(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse complex expression với parentheses.
    
    Đây là fallback cho các expressions phức tạp không match
    các patterns cụ thể khác.
    
    Example:
        assign out = (a & b) | (c & d);
        -> Tạo COMPLEX node để xử lý sau
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Complex expression
    """
    # Tạo COMPLEX node
    complex_id = node_builder.create_operation_node(
        node_type='COMPLEX',
        operands=[rhs.strip()],
        extra_attrs={'expression': rhs.strip()}
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(complex_id, lhs)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def extract_ternary_parts(expression: str) -> tuple:
    """
    Extract các parts từ ternary expression.
    
    Returns:
        (condition, true_value, false_value)
        
    Example:
        "(a > b) ? a : b" -> ("a > b", "a", "b")
    """
    # Simplified implementation
    # Trong thực tế cần xử lý nested ternary và parentheses
    parts = expression.split('?')
    if len(parts) != 2:
        return (None, None, None)
    
    condition = parts[0].strip()
    values = parts[1].split(':')
    
    if len(values) != 2:
        return (None, None, None)
    
    true_val = values[0].strip()
    false_val = values[1].strip()
    
    return (condition, true_val, false_val)


def extract_slice_range(expression: str) -> tuple:
    """
    Extract signal name và range từ slice expression.
    
    Returns:
        (signal, msb, lsb) hoặc (signal, bit, None) cho single bit
        
    Example:
        "data[7:0]" -> ("data", "7", "0")
        "flags[3]"  -> ("flags", "3", None)
    """
    match = re.match(r'(\w+)\[([^\]]+)\]', expression.strip())
    if not match:
        return (None, None, None)
    
    signal = match.group(1)
    index_part = match.group(2)
    
    if ':' in index_part:
        # Range slice
        parts = index_part.split(':')
        return (signal, parts[0].strip(), parts[1].strip())
    else:
        # Single bit
        return (signal, index_part.strip(), None)

