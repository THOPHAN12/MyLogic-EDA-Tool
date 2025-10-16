"""
Enhanced Verilog Parser with Logic Gates Support

Supports:
 - Vector declarations: [3:0] a, b
 - Arithmetic operations: +, -, *, /
 - Logic gates: &, |, ^, ~
 - Complex expressions with parentheses
 - Ternary operators (basic support)
"""

import re
import os
import sys
from typing import Dict, List, Tuple, Union

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_enhanced_verilog(path: str) -> Dict:
    """Parse Verilog file with enhanced support for logic gates and complex expressions."""
    if not path or not isinstance(path, str):
        raise ValueError("Path must be a non-empty string")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            src = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    
    # Remove comments
    src = re.sub(r'//.*$', '', src, flags=re.MULTILINE)
    src = re.sub(r'/\*.*?\*/', '', src, flags=re.DOTALL)
    
    # Initialize netlist
    net = {
        "name": "",
        "inputs": [],
        "outputs": [],
        "wires": [],
        "nodes": [],
        "attrs": {"source_file": path, "vector_widths": {}}
    }
    
    # Extract module name and body
    module_match = re.search(r'module\s+(\w+)\s*\([^)]*\)\s*;', src, re.DOTALL)
    if module_match:
        net['name'] = module_match.group(1)
        # Extract module body (between module declaration and endmodule)
        module_end = module_match.end()
        endmodule_match = re.search(r'endmodule', src[module_end:])
        if endmodule_match:
            module_body = src[module_end:module_end + endmodule_match.start()]
        else:
            module_body = src[module_end:]
    else:
        module_body = src  # Fallback to entire source
    
    # Extract vector inputs from module body only
    input_matches = re.findall(r'input\s+\[(\d+):(\d+)\]\s+([^;]+)', module_body)
    for msb, lsb, signals_str in input_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            net['inputs'].append(signal)
            net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar inputs (only scalar, not vector)
    scalar_input_lines = re.findall(r'input\s+([^[;]+);', module_body)
    for line in scalar_input_lines:
        # Split by comma and clean up
        signals = [s.strip() for s in line.split(',')]
        for signal in signals:
            # Remove any extra whitespace or comments
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['inputs']:
                net['inputs'].append(signal)
                net['attrs']['vector_widths'][signal] = 1
    
    # Extract vector outputs
    output_matches = re.findall(r'output\s+\[(\d+):(\d+)\]\s+([^;]+)', module_body)
    for msb, lsb, signals_str in output_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            net['outputs'].append(signal)
            net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar outputs (only scalar, not vector)
    scalar_output_lines = re.findall(r'output\s+([^[;]+);', module_body)
    for line in scalar_output_lines:
        # Split by comma and clean up
        signals = [s.strip() for s in line.split(',')]
        for signal in signals:
            # Remove any extra whitespace or comments
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['outputs']:
                net['outputs'].append(signal)
                net['attrs']['vector_widths'][signal] = 1
    
    # Extract assign statements with enhanced parsing
    assign_matches = re.findall(r'assign\s+([^=]+)\s*=\s*([^;]+);', module_body)
    node_counter = 0
    
    for lhs, rhs in assign_matches:
        # Clean up LHS (remove extra whitespace)
        lhs = lhs.strip()
        
        # Handle bit assignments like flags[0], flags[1]
        if '[' in lhs and ']' in lhs:
            # Extract signal name from bit assignment
            signal_name = lhs.split('[')[0]
            # For bit assignments, we'll create a simple BUF node
            buf_id = f"buf_{node_counter}"
            net['nodes'].append({
                "id": buf_id,
                "type": "BUF",
                "fanins": [[rhs.strip(), False]]
            })
            
            # Store output mapping for the bit
            if 'output_mapping' not in net['attrs']:
                net['attrs']['output_mapping'] = {}
            net['attrs']['output_mapping'][lhs] = buf_id
            node_counter += 1
            continue
        
        # Parse different types of expressions
        if _is_ternary_operator(rhs):
            # Handle ternary operator: condition ? value1 : value2
            _parse_ternary_operator(net, lhs, rhs, node_counter)
            node_counter += 2  # MUX + BUF nodes
        
        elif _is_complex_expression(rhs):
            # Handle complex expressions with parentheses
            _parse_complex_expression(net, lhs, rhs, node_counter)
            node_counter += 2  # Complex + BUF nodes
        
        elif '^' in rhs and not any(op in rhs for op in ['+', '-', '*', '/']):
            # XOR operation
            _parse_xor_operation(net, lhs, rhs, node_counter)
            node_counter += 2  # XOR + BUF nodes
        
        elif '&' in rhs and not any(op in rhs for op in ['+', '-', '*', '/', '^']):
            # AND operation
            _parse_and_operation(net, lhs, rhs, node_counter)
            node_counter += 2  # AND + BUF nodes
        
        elif '|' in rhs and not any(op in rhs for op in ['+', '-', '*', '/', '^', '&']):
            # OR operation
            _parse_or_operation(net, lhs, rhs, node_counter)
            node_counter += 2  # OR + BUF nodes
        
        elif '~' in rhs and not any(op in rhs for op in ['+', '-', '*', '/', '^', '&', '|']):
            # NOT operation
            _parse_not_operation(net, lhs, rhs, node_counter)
            node_counter += 2  # NOT + BUF nodes
        
        elif '+' in rhs:
            # Addition
            _parse_addition(net, lhs, rhs, node_counter)
            node_counter += 2  # ADD + BUF nodes
        
        elif '-' in rhs:
            # Subtraction
            _parse_subtraction(net, lhs, rhs, node_counter)
            node_counter += 2  # SUB + BUF nodes
        
        elif '*' in rhs:
            # Multiplication
            _parse_multiplication(net, lhs, rhs, node_counter)
            node_counter += 2  # MULT + BUF nodes
        
        elif '/' in rhs:
            # Division
            _parse_division(net, lhs, rhs, node_counter)
            node_counter += 2  # DIV + BUF nodes
        
        else:
            # Simple assignment
            _parse_simple_assignment(net, lhs, rhs, node_counter)
            node_counter += 1  # BUF node
    
    return net


def _is_ternary_operator(expression: str) -> bool:
    """Check if expression is a ternary operator."""
    return '?' in expression and ':' in expression


def _is_complex_expression(expression: str) -> bool:
    """Check if expression has parentheses."""
    return '(' in expression and ')' in expression


def _parse_ternary_operator(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse ternary operator: condition ? value1 : value2"""
    # Simple implementation - create a MUX node
    mux_id = f"mux_{node_counter}"
    net['nodes'].append({
        "id": mux_id,
        "type": "MUX",
        "fanins": [[rhs.strip(), False]]
    })
    
    # Create BUF node for output
    buf_id = f"buf_{node_counter + 1}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[mux_id, False]]
    })
    
    # Store output mapping
    if 'output_mapping' not in net['attrs']:
        net['attrs']['output_mapping'] = {}
    net['attrs']['output_mapping'][lhs] = buf_id


def _parse_complex_expression(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse complex expressions with parentheses"""
    # Simple implementation - create a COMPLEX node
    complex_id = f"complex_{node_counter}"
    net['nodes'].append({
        "id": complex_id,
        "type": "COMPLEX",
        "fanins": [[rhs.strip(), False]]
    })
    
    # Create BUF node for output
    buf_id = f"buf_{node_counter + 1}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[complex_id, False]]
    })
    
    # Store output mapping
    if 'output_mapping' not in net['attrs']:
        net['attrs']['output_mapping'] = {}
    net['attrs']['output_mapping'][lhs] = buf_id


def _parse_xor_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse XOR operation"""
    operands = [op.strip() for op in rhs.split('^')]
    if len(operands) >= 2:
        # Create XOR nodes for multiple operands
        current_id = operands[0]
        for i in range(1, len(operands)):
            xor_id = f"xor_{node_counter}"
            net['nodes'].append({
                "id": xor_id,
                "type": "XOR",
                "fanins": [[current_id, False], [operands[i], False]]
            })
            current_id = xor_id
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[current_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_and_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse AND operation"""
    operands = [op.strip() for op in rhs.split('&')]
    if len(operands) >= 2:
        # Create AND nodes for multiple operands
        current_id = operands[0]
        for i in range(1, len(operands)):
            and_id = f"and_{node_counter}"
            net['nodes'].append({
                "id": and_id,
                "type": "AND",
                "fanins": [[current_id, False], [operands[i], False]]
            })
            current_id = and_id
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[current_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_or_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse OR operation"""
    operands = [op.strip() for op in rhs.split('|')]
    if len(operands) >= 2:
        # Create OR nodes for multiple operands
        current_id = operands[0]
        for i in range(1, len(operands)):
            or_id = f"or_{node_counter}"
            net['nodes'].append({
                "id": or_id,
                "type": "OR",
                "fanins": [[current_id, False], [operands[i], False]]
            })
            current_id = or_id
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[current_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_not_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse NOT operation"""
    operand = rhs.replace('~', '').strip()
    # Create NOT node
    not_id = f"not_{node_counter}"
    net['nodes'].append({
        "id": not_id,
        "type": "NOT",
        "fanins": [[operand, False]]
    })
    
    # Create BUF node for output
    buf_id = f"buf_{node_counter + 1}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[not_id, False]]
    })
    
    # Store output mapping
    if 'output_mapping' not in net['attrs']:
        net['attrs']['output_mapping'] = {}
    net['attrs']['output_mapping'][lhs] = buf_id


def _parse_addition(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse addition operation"""
    operands = [op.strip() for op in rhs.split('+')]
    if len(operands) == 2:
        a, b = operands
        # Create ADD node
        add_id = f"add_{node_counter}"
        net['nodes'].append({
            "id": add_id,
            "type": "ADD",
            "fanins": [[a, False], [b, False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[add_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_subtraction(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse subtraction operation"""
    operands = [op.strip() for op in rhs.split('-')]
    if len(operands) == 2:
        a, b = operands
        # Create SUB node
        sub_id = f"sub_{node_counter}"
        net['nodes'].append({
            "id": sub_id,
            "type": "SUB",
            "fanins": [[a, False], [b, False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[sub_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_multiplication(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse multiplication operation"""
    operands = [op.strip() for op in rhs.split('*')]
    if len(operands) == 2:
        a, b = operands
        # Create MULT node
        mult_id = f"mult_{node_counter}"
        net['nodes'].append({
            "id": mult_id,
            "type": "MULT",
            "fanins": [[a, False], [b, False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[mult_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_division(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse division operation"""
    operands = [op.strip() for op in rhs.split('/')]
    if len(operands) == 2:
        a, b = operands
        # Create DIV node
        div_id = f"div_{node_counter}"
        net['nodes'].append({
            "id": div_id,
            "type": "DIV",
            "fanins": [[a, False], [b, False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[div_id, False]]
        })
        
        # Store output mapping
        if 'output_mapping' not in net['attrs']:
            net['attrs']['output_mapping'] = {}
        net['attrs']['output_mapping'][lhs] = buf_id


def _parse_simple_assignment(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse simple assignment"""
    # Create BUF node for simple assignment
    buf_id = f"buf_{node_counter}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[rhs.strip(), False]]
    })
    
    # Store output mapping
    if 'output_mapping' not in net['attrs']:
        net['attrs']['output_mapping'] = {}
    net['attrs']['output_mapping'][lhs] = buf_id
