"""
Arithmetic Simulation Engine for MyLogic

Hỗ trợ:
 - Các phép toán số học vector: +, -, *, /
 - Các phép toán bitwise: &, |, ^, ~
 - Các biểu thức phức tạp với độ ưu tiên toán tử
"""

import os
import sys
from typing import Dict, List, Union, Any

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Định nghĩa class VectorValue
class VectorValue:
    """Đại diện cho một giá trị vector đa bit."""
    
    def __init__(self, value: int, width: int):
        """Khởi tạo giá trị vector."""
        self.width = width
        self.value = value & ((1 << width) - 1)  # Mask theo độ rộng
    
    def to_int(self) -> int:
        """Chuyển đổi thành số nguyên."""
        return self.value
    
    def to_binary(self) -> str:
        """Chuyển đổi thành chuỗi nhị phân."""
        return format(self.value, f'0{self.width}b')
    
    def __repr__(self):
        return f"VectorValue({self.to_binary()}, width={self.width})"

def vector_add(a: VectorValue, b: VectorValue) -> VectorValue:
    """Cộng hai giá trị vector."""
    result_int = a.to_int() + b.to_int()
    max_width = max(a.width, b.width) + 1  # +1 cho carry
    return VectorValue(result_int, max_width)

def vector_multiply(a: VectorValue, b: VectorValue) -> VectorValue:
    """Nhân hai giá trị vector."""
    result_int = a.to_int() * b.to_int()
    result_width = a.width + b.width
    return VectorValue(result_int, result_width)

def vector_and(a: VectorValue, b: VectorValue) -> VectorValue:
    """Bitwise AND của hai giá trị vector."""
    result_int = a.to_int() & b.to_int()
    max_width = max(a.width, b.width)
    return VectorValue(result_int, max_width)

def vector_or(a: VectorValue, b: VectorValue) -> VectorValue:
    """Bitwise OR của hai giá trị vector."""
    result_int = a.to_int() | b.to_int()
    max_width = max(a.width, b.width)
    return VectorValue(result_int, max_width)

def vector_xor(a: VectorValue, b: VectorValue) -> VectorValue:
    """Bitwise XOR của hai giá trị vector."""
    result_int = a.to_int() ^ b.to_int()
    max_width = max(a.width, b.width)
    return VectorValue(result_int, max_width)


def vector_subtract(a: VectorValue, b: VectorValue) -> VectorValue:
    """Trừ hai giá trị vector."""
    result_int = a.to_int() - b.to_int()
    max_width = max(a.width, b.width) + 1  # +1 cho borrow
    return VectorValue(result_int, max_width)


def vector_divide(a: VectorValue, b: VectorValue) -> VectorValue:
    """Chia hai giá trị vector."""
    if b.to_int() == 0:
        raise ValueError("Division by zero")
    result_int = a.to_int() // b.to_int()
    max_width = a.width  # Độ rộng kết quả chia
    return VectorValue(result_int, max_width)


def vector_not(a: VectorValue) -> VectorValue:
    """Bitwise NOT of a vector value."""
    # Invert within width using masking
    mask = (1 << a.width) - 1
    return VectorValue((~a.to_int()) & mask, a.width)


def simulate_arithmetic_netlist(netlist: Dict[str, Any], inputs: Dict[str, Union[int, str, List[bool], VectorValue]]) -> Dict[str, VectorValue]:
    """
    Simulate arithmetic netlist with full arithmetic operations.
    
    Args:
        netlist: Netlist dictionary with arithmetic information
        inputs: Dictionary mapping input names to values
        
    Returns:
        Dictionary mapping output names to VectorValue objects
    """
    # Convert inputs to VectorValue objects
    vector_inputs = {}
    vector_widths = netlist.get('attrs', {}).get('vector_widths', {})
    
    for name, value in inputs.items():
        if isinstance(value, VectorValue):
            vector_inputs[name] = value
        else:
            # Get width from netlist or default to 1
            width = vector_widths.get(name, 1)
            vector_inputs[name] = VectorValue(value, width)
    
    # Initialize node values
    node_values = {}
    
    # Set input values
    for input_name in netlist.get('inputs', []):
        if input_name in vector_inputs:
            node_values[input_name] = vector_inputs[input_name]
    
    # Process nodes in topological order
    for node in netlist.get('nodes', []):
        node_id = node['id']
        node_type = node['type']
        fanins = node.get('fanins', [])
        
        if node_type == 'CONST':
            # Constant node
            const_value = node.get('value', 0)
            width = 1
            # Try to determine width from context
            for output_name in netlist.get('outputs', []):
                if output_name in vector_widths:
                    width = max(width, vector_widths[output_name])
            node_values[node_id] = VectorValue(const_value, width)
        
        elif node_type == 'MULT':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = vector_not(a_val)
                    if b_inv:
                        b_val = vector_not(b_val)
                    
                    result = vector_multiply(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'ADD':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = vector_not(a_val)
                    if b_inv:
                        b_val = vector_not(b_val)
                    
                    result = vector_add(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'SUB':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = vector_not(a_val)
                    if b_inv:
                        b_val = vector_not(b_val)
                    
                    result = vector_subtract(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'DIV':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = vector_not(a_val)
                    if b_inv:
                        b_val = vector_not(b_val)
                    
                    try:
                        result = vector_divide(a_val, b_val)
                        node_values[node_id] = result
                    except ValueError as e:
                        print(f"[WARNING] Division error: {e}")
                        node_values[node_id] = VectorValue(0, 1)
        
        elif node_type == 'AND':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = vector_not(a_val)
                    if b_inv:
                        b_val = vector_not(b_val)
                    
                    result = vector_and(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'OR':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = VectorValue([not b for b in a_val.bits])
                    if b_inv:
                        b_val = VectorValue([not b for b in b_val.bits])
                    
                    result = vector_or(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'XOR':
            if len(fanins) == 2:
                a_id, a_inv = fanins[0]
                b_id, b_inv = fanins[1]
                
                a_val = node_values.get(a_id)
                b_val = node_values.get(b_id)
                
                if a_val is not None and b_val is not None:
                    # Apply inversions
                    if a_inv:
                        a_val = VectorValue([not b for b in a_val.bits])
                    if b_inv:
                        b_val = VectorValue([not b for b in b_val.bits])
                    
                    result = vector_xor(a_val, b_val)
                    node_values[node_id] = result
        
        elif node_type == 'NOT':
            if len(fanins) == 1:
                input_id, inv = fanins[0]
                input_val = node_values.get(input_id)
                
                if input_val is not None:
                    if inv:
                        result = input_val  # Double inversion
                    else:
                        result = vector_not(input_val)
                    node_values[node_id] = result
        
        elif node_type == 'BUF':
            if len(fanins) == 1:
                input_id, inv = fanins[0]
                input_val = node_values.get(input_id)
                
                if input_val is not None:
                    if inv:
                        result = vector_not(input_val)
                    else:
                        result = input_val
                    node_values[node_id] = result
    
    # Collect outputs
    outputs = {}
    for output_name in netlist.get('outputs', []):
        if output_name in node_values:
            outputs[output_name] = node_values[output_name]
        else:
            # Check if there's an output mapping
            output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
            if output_name in output_mapping:
                mapped_id = output_mapping[output_name]
                if mapped_id in node_values:
                    outputs[output_name] = node_values[mapped_id]
    
    return outputs


def demo_arithmetic_operations():
    """Demonstrate arithmetic operations."""
    print("=== Arithmetic Operations Demo ===")
    
    # Test basic arithmetic
    test_cases = [
        (VectorValue(5, 4), VectorValue(3, 4), "Addition"),
        (VectorValue(8, 4), VectorValue(3, 4), "Subtraction"),
        (VectorValue(4, 4), VectorValue(3, 4), "Multiplication"),
        (VectorValue(12, 4), VectorValue(3, 4), "Division"),
    ]
    
    for a, b, op_name in test_cases:
        print(f"\\n{op_name}:")
        print(f"  a = {a} (int: {a.to_int()})")
        print(f"  b = {b} (int: {b.to_int()})")
        
        try:
            if op_name == "Addition":
                result = vector_add(a, b)
            elif op_name == "Subtraction":
                result = vector_subtract(a, b)
            elif op_name == "Multiplication":
                result = vector_multiply(a, b)
            elif op_name == "Division":
                result = vector_divide(a, b)
            
            print(f"  Result: {result} (int: {result.to_int()})")
            # Calculate expected result
            if op_name == "Addition":
                expected = a.to_int() + b.to_int()
            elif op_name == "Subtraction":
                expected = a.to_int() - b.to_int()
            elif op_name == "Multiplication":
                expected = a.to_int() * b.to_int()
            elif op_name == "Division":
                expected = a.to_int() // b.to_int()
            print(f"  Expected: {expected}")
        except Exception as e:
            print(f"  [ERROR] {op_name} failed: {e}")


if __name__ == "__main__":
    demo_arithmetic_operations()
