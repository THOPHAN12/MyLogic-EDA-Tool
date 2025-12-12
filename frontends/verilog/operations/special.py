"""
Special Operations Parser - Các phép toán đặc biệt

Hỗ trợ:
1. Ternary Operator (?:): condition ? true_value : false_value
2. Concatenation ({}): {a, b, c}
3. Bit Slice ([]): signal[msb:lsb] hoặc signal[bit]

Đây là các operations phức tạp hơn, không phải arithmetic/bitwise đơn giản.
"""

import re
from typing import List, Dict, Optional
from ..core.node_builder import NodeBuilder


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
    rhs: str,
    params: Dict[str, int] = None
) -> None:
    """
    Parse bit concatenation: {a, b, c, ...} với hỗ trợ replication bên trong.
    
    Nối các signals thành một signal lớn hơn.
    
    Example:
        assign result = {a[3:0], b[3:0]};
        Nếu a=4'b1010, b=4'b0011 -> result=8'b10100011
        assign padded = {a, {4{1'b0}}, b};  # Replication trong concatenation
        
    Bit order: Signal đầu tiên là MSB
        {a, b} -> [a_bits, b_bits]
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Concatenation expression {a, b, ...}
        params: Dictionary chứa parameter values (cho replication bên trong)
    """
    import re
    from ..core.tokenizer import _eval_int_simple
    
    params = params or {}
    rhs = rhs.strip()
    
    # Loại bỏ dấu ngoặc {} ngoài cùng
    inner = rhs[1:-1].strip()
    
    # Parse parts, xử lý nested braces (replication)
    parts = []
    i = 0
    while i < len(inner):
        if inner[i].isspace() or inner[i] == ',':
            i += 1
            continue
        
        # Check xem có phải replication không: {n{...}}
        if inner[i] == '{':
            # Tìm closing brace tương ứng
            brace_count = 0
            start = i
            j = i
            while j < len(inner):
                if inner[j] == '{':
                    brace_count += 1
                elif inner[j] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        # Tìm thấy closing brace
                        replication_expr = inner[start:j+1]
                        # Check xem có phải replication không
                        if is_replication(replication_expr):
                            # Expand replication
                            rep_match = re.match(r'\{([^}]+)\{(.+)\}\}', replication_expr)
                            if rep_match:
                                count_expr = rep_match.group(1).strip()
                                content = rep_match.group(2).strip()
                                try:
                                    count = _eval_int_simple(count_expr, params)
                                    # Expand thành n lần content
                                    for _ in range(count):
                                        parts.append(content)
                                except Exception:
                                    # Không thể eval, giữ nguyên
                                    parts.append(replication_expr)
                        else:
                            # Nested concatenation, giữ nguyên
                            parts.append(replication_expr)
                        i = j + 1
                        break
                j += 1
            else:
                # Không tìm thấy closing brace, lấy đến hết
                parts.append(inner[i:])
                break
        else:
            # Regular part, tìm đến comma hoặc end
            start = i
            while i < len(inner) and inner[i] != ',':
                i += 1
            part = inner[start:i].strip()
            if part:
                parts.append(part)
            i += 1
    
    # Tạo CONCAT node với expanded parts
    concat_id = node_builder.create_operation_node(
        node_type='CONCAT',
        operands=parts,
        extra_attrs={'expanded_parts': len(parts)}
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(concat_id, lhs)


# ============================================================================
# BIT SLICE/INDEX - Truy cập bit
# ============================================================================

def is_slice(expression: str) -> bool:
    """
    Check xem expression có phải bit slice/index hoặc array index không.
    
    Formats:
        signal[bit]       - Single bit
        signal[msb:lsb]   - Bit range
        signal[N-1:0]     - Parameterized range
        mem[addr]         - Array/memory index
        mem[addr][bit]    - Array index với bit select
        
    Example:
        data[7:0]     -> True
        flags[3]      -> True
        addr[WIDTH-1:0] -> True
        mem[addr]     -> True (array index)
        mem[addr][0]  -> True (array index với bit select)
        a + b         -> False
        {a, b}        -> False (concatenation, không phải slice)
    """
    expr = expression.strip()
    # Không phải concatenation (bắt đầu bằng {)
    if expr.startswith('{'):
        return False
    # Check pattern: signal[index] hoặc signal[msb:lsb] hoặc mem[addr]
    return bool(re.search(r'\w+\s*\[[^\]]+\]', expr))


def parse_slice(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str,
    params: Dict[str, int] = None
) -> None:
    """
    Parse bit slice/index hoặc array index với chi tiết đầy đủ.
    
    Formats:
        signal[bit]       - Truy cập 1 bit
        signal[msb:lsb]   - Truy cập dải bit
        signal[N-1:0]     - Parameterized range
        mem[addr]         - Array/memory index
        mem[addr][bit]    - Array index với bit select
        
    Example:
        assign lsb = data[0];        # Bit 0
        assign high = data[7:4];     # Bits 7-4
        assign addr = bus[WIDTH-1:0]; # Parameterized
        assign val = mem[addr];      # Memory read
        assign bit = mem[addr][0];   # Memory read với bit select
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Slice expression (ví dụ: "data[7:0]" hoặc "mem[addr]")
        params: Dictionary chứa parameter values (cho parameterized indices)
    """
    import re
    from ..core.tokenizer import _eval_int_simple
    
    params = params or {}
    rhs = rhs.strip()
    
    # Pattern: signal[msb:lsb] hoặc signal[index] hoặc mem[addr][bit]
    # Match signal name và indices
    match = re.match(r'(\w+)\s*\[([^\]]+)\](?:\s*\[([^\]]+)\])?', rhs)
    if not match:
        # Fallback: tạo SLICE node đơn giản
        slice_id = node_builder.create_operation_node(
            node_type='SLICE',
            operands=[rhs],
            extra_attrs={'raw_slice': rhs}
        )
        node_builder.create_buffer_node(slice_id, lhs)
        return
    
    signal_name = match.group(1)
    first_index = match.group(2).strip()
    second_index = match.group(3) if match.group(3) else None
    
    # Check xem có phải array index (mem[addr]) hay bit slice (signal[msb:lsb])
    # Array index thường không có ':' trong index đầu tiên
    is_array_index = ':' not in first_index
    
    if second_index:
        # mem[addr][bit] - Array index với bit select
        # Tạo ARRAY_INDEX node cho mem[addr], sau đó SLICE cho [bit]
        array_id = node_builder.create_operation_node(
            node_type='ARRAY_INDEX',
            operands=[signal_name, first_index],
            extra_attrs={
                'signal': signal_name,
                'index': first_index,
                'is_memory': True
            }
        )
        # Tạo intermediate signal cho array access
        array_signal = f"_array_{signal_name}_{first_index}"
        node_builder.create_buffer_node(array_id, array_signal)
        
        # Parse bit select
        bit_index = second_index.strip()
        bit_index_val = None
        try:
            bit_index_val = _eval_int_simple(bit_index, params)
        except Exception:
            pass
        
        # Tạo SLICE node cho bit select
        slice_id = node_builder.create_operation_node(
            node_type='SLICE',
            operands=[array_signal, bit_index, bit_index],
            extra_attrs={
                'signal': array_signal,
                'index': bit_index,
                'index_val': bit_index_val,
                'width': 1,
                'is_array_bit_select': True
            }
        )
    elif is_array_index:
        # mem[addr] - Array/memory index
        index_val = None
        try:
            index_val = _eval_int_simple(first_index, params)
        except Exception:
            pass  # Không thể eval (có thể là expression)
        
        # Tạo ARRAY_INDEX node
        slice_id = node_builder.create_operation_node(
            node_type='ARRAY_INDEX',
            operands=[signal_name, first_index],
            extra_attrs={
                'signal': signal_name,
                'index': first_index,
                'index_val': index_val,
                'is_memory': True
            }
        )
    else:
        # Range: signal[msb:lsb]
        range_match = re.match(r'([^:]+)\s*:\s*(.+)', first_index)
        if range_match:
            msb_expr = range_match.group(1).strip()
            lsb_expr = range_match.group(2).strip()
            
            # Tính width nếu có thể
            width = None
            try:
                msb_val = _eval_int_simple(msb_expr, params)
                lsb_val = _eval_int_simple(lsb_expr, params)
                width = abs(msb_val - lsb_val) + 1
            except Exception:
                pass
            
            # Tạo SLICE node với chi tiết
            slice_id = node_builder.create_operation_node(
                node_type='SLICE',
                operands=[signal_name, msb_expr, lsb_expr],
                extra_attrs={
                    'signal': signal_name,
                    'msb': msb_expr,
                    'lsb': lsb_expr,
                    'width': width
                }
            )
        else:
            # Single index: signal[index]
            index_val = None
            try:
                index_val = _eval_int_simple(first_index, params)
            except Exception:
                pass
            
            # Tạo SLICE node cho single bit
            slice_id = node_builder.create_operation_node(
                node_type='SLICE',
                operands=[signal_name, first_index, first_index],
                extra_attrs={
                    'signal': signal_name,
                    'index': first_index,
                    'index_val': index_val,
                    'width': 1
                }
            )
    
    # Tạo buffer node
    node_builder.create_buffer_node(slice_id, lhs)


# ============================================================================
# REPLICATION - Nhân bản bit
# ============================================================================

def is_replication(expression: str) -> bool:
    """
    Check xem có phải replication không.
    
    Format: {count{signal}} hoặc {count{expr}}
    
    Example:
        {4{1'b1}}     -> 4'b1111
        {3{a}}        -> {a, a, a}
        {N{signal}}   -> Parameterized replication
        
    Note: Phải check trước concatenation vì replication cũng dùng {}
    """
    import re
    expr = expression.strip()
    
    # Pattern: {count{...}}
    # Match: {number{...}} hoặc {identifier{...}}
    match = re.match(r'\{([^}]+)\{', expr)
    if not match:
        return False
    
    # Check xem có closing braces tương ứng
    count_expr = match.group(1).strip()
    # Đếm số { và } để đảm bảo match đúng
    open_braces = expr.count('{')
    close_braces = expr.count('}')
    
    # Replication phải có format: {count{content}}
    # Tức là có ít nhất 2 { và 2 }
    if open_braces >= 2 and close_braces >= 2:
        # Check xem count_expr có phải số hoặc identifier không
        if re.match(r'^[\w\s+\-*/()]+$', count_expr):
            return True
    
    return False


def parse_replication(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str,
    params: Dict[str, int] = None
) -> None:
    """
    Parse bit replication: {count{signal}} và expand thành CONCAT.
    
    Nhân bản signal n lần thành concatenation.
    
    Example:
        assign zeros = {4{1'b0}};  # Expand thành {1'b0, 1'b0, 1'b0, 1'b0}
        assign rep = {3{a}};       # Expand thành {a, a, a}
        assign pad = {N{1'b0}};    # Parameterized replication
        
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Replication expression (ví dụ: "{4{1'b0}}")
        params: Dictionary chứa parameter values (cho parameterized count)
    """
    import re
    from ..core.tokenizer import _eval_int_simple
    
    params = params or {}
    rhs = rhs.strip()
    
    # Parse: {count{content}}
    # Tìm count và content
    match = re.match(r'\{([^}]+)\{(.+)\}\}', rhs)
    if not match:
        # Fallback: tạo CONCAT node đơn giản
        rep_id = node_builder.create_operation_node(
            node_type='CONCAT',
            operands=[rhs],
            extra_attrs={'replication': True, 'raw_replication': rhs}
        )
        node_builder.create_buffer_node(rep_id, lhs)
        return
    
    count_expr = match.group(1).strip()
    content = match.group(2).strip()
    
    # Eval count
    count = None
    try:
        count = _eval_int_simple(count_expr, params)
    except Exception:
        # Không thể eval (có thể là parameter chưa biết)
        # Tạo CONCAT node với replication flag
        rep_id = node_builder.create_operation_node(
            node_type='CONCAT',
            operands=[content],
            extra_attrs={
                'replication': True,
                'count_expr': count_expr,
                'content': content
            }
        )
        node_builder.create_buffer_node(rep_id, lhs)
        return
    
    # Expand replication thành concatenation
    # {n{content}} -> {content, content, ..., content} (n lần)
    concat_parts = [content] * count
    
    # Tạo CONCAT node với expanded parts
    concat_id = node_builder.create_operation_node(
        node_type='CONCAT',
        operands=concat_parts,
        extra_attrs={
            'replication': True,
            'original_count': count,
            'count_expr': count_expr,
            'expanded': True
        }
    )
    
    # Tạo buffer node
    node_builder.create_buffer_node(concat_id, lhs)


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

