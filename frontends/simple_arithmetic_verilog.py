"""
Simple Arithmetic Verilog Parser

Supports:
 - Vector declarations: [3:0] a, b
 - Arithmetic operations: +, -, *, /
 - Bitwise operations: &, |, ^, ~
"""

import re
import os
import sys
from typing import Dict, List, Tuple, Union

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def parse_arithmetic_verilog_simple(path: str) -> Dict:
    """Parse Verilog file with arithmetic support using regex."""
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
    
    # Extract module name
    module_match = re.search(r'module\s+(\w+)', src)
    if module_match:
        net['name'] = module_match.group(1)
    
    # Extract vector inputs
    input_matches = re.findall(r'input\s+\[(\d+):(\d+)\]\s+([^;]+)', src)
    for msb, lsb, signals_str in input_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            net['inputs'].append(signal)
            net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar inputs
    scalar_inputs = re.findall(r'input\s+(\w+)', src)
    for signal in scalar_inputs:
        if signal not in net['inputs']:
            net['inputs'].append(signal)
            net['attrs']['vector_widths'][signal] = 1
    
    # Extract vector outputs
    output_matches = re.findall(r'output\s+\[(\d+):(\d+)\]\s+([^;]+)', src)
    for msb, lsb, signals_str in output_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            net['outputs'].append(signal)
            net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar outputs
    scalar_outputs = re.findall(r'output\s+(\w+)', src)
    for signal in scalar_outputs:
        if signal not in net['outputs']:
            net['outputs'].append(signal)
            net['attrs']['vector_widths'][signal] = 1
    
    # Extract assign statements with arithmetic operations
    assign_matches = re.findall(r'assign\s+(\w+)\s*=\s*([^;]+);', src)
    node_counter = 0
    
    for lhs, rhs in assign_matches:
        # Parse arithmetic expression
        if '+' in rhs:
            # Addition
            operands = [op.strip() for op in rhs.split('+')]
            if len(operands) == 2:
                a, b = operands
                # Create ADD node
                add_id = f"add_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": add_id,
                    "type": "ADD",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[add_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '-' in rhs:
            # Subtraction
            operands = [op.strip() for op in rhs.split('-')]
            if len(operands) == 2:
                a, b = operands
                # Create SUB node
                sub_id = f"sub_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": sub_id,
                    "type": "SUB",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[sub_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '*' in rhs:
            # Multiplication
            operands = [op.strip() for op in rhs.split('*')]
            if len(operands) == 2:
                a, b = operands
                # Create MULT node
                mult_id = f"mult_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": mult_id,
                    "type": "MULT",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[mult_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '/' in rhs:
            # Division
            operands = [op.strip() for op in rhs.split('/')]
            if len(operands) == 2:
                a, b = operands
                # Create DIV node
                div_id = f"div_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": div_id,
                    "type": "DIV",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[div_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '&' in rhs:
            # Bitwise AND
            operands = [op.strip() for op in rhs.split('&')]
            if len(operands) == 2:
                a, b = operands
                # Create AND node
                and_id = f"and_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": and_id,
                    "type": "AND",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[and_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '|' in rhs:
            # Bitwise OR
            operands = [op.strip() for op in rhs.split('|')]
            if len(operands) == 2:
                a, b = operands
                # Create OR node
                or_id = f"or_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": or_id,
                    "type": "OR",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[or_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif '^' in rhs:
            # Bitwise XOR
            operands = [op.strip() for op in rhs.split('^')]
            if len(operands) == 2:
                a, b = operands
                # Create XOR node
                xor_id = f"xor_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": xor_id,
                    "type": "XOR",
                    "fanins": [[a, False], [b, False]]
                })
                
                # Create BUF node for output
                buf_id = f"buf_{node_counter}"
                node_counter += 1
                net['nodes'].append({
                    "id": buf_id,
                    "type": "BUF",
                    "fanins": [[xor_id, False]]
                })
                
                # Store output mapping
                if 'output_mapping' not in net['attrs']:
                    net['attrs']['output_mapping'] = {}
                net['attrs']['output_mapping'][lhs] = buf_id
        
        elif rhs.strip().startswith('~'):
            # Bitwise NOT
            operand = rhs.strip()[1:].strip()
            # Create NOT node
            not_id = f"not_{node_counter}"
            node_counter += 1
            net['nodes'].append({
                "id": not_id,
                "type": "NOT",
                "fanins": [[operand, False]]
            })
            
            # Create BUF node for output
            buf_id = f"buf_{node_counter}"
            node_counter += 1
            net['nodes'].append({
                "id": buf_id,
                "type": "BUF",
                "fanins": [[not_id, False]]
            })
            
            # Store output mapping
            if 'output_mapping' not in net['attrs']:
                net['attrs']['output_mapping'] = {}
            net['attrs']['output_mapping'][lhs] = buf_id
    
    return net


def get_arithmetic_stats(netlist: Dict) -> Dict[str, any]:
    """Get statistics for arithmetic netlist."""
    stats = {
        'name': netlist.get('name', 'unknown'),
        'total_inputs': len(netlist.get('inputs', [])),
        'total_outputs': len(netlist.get('outputs', [])),
        'total_wires': len(netlist.get('wires', [])),
        'total_nodes': len(netlist.get('nodes', [])),
        'vector_widths': netlist.get('attrs', {}).get('vector_widths', {}),
        'has_vector_io': bool(netlist.get('attrs', {}).get('vector_widths', {}))
    }
    
    # Count gate types
    gate_counts = {}
    for node in netlist.get('nodes', []):
        gate_type = node.get('type', 'UNKNOWN')
        gate_counts[gate_type] = gate_counts.get(gate_type, 0) + 1
    
    stats['gate_counts'] = gate_counts
    return stats


if __name__ == "__main__":
    # Test arithmetic Verilog parsing
    print("=== Testing Simple Arithmetic Verilog Parser ===")
    
    # Test files
    test_files = [
        "examples/arithmetic_operations.v",
        "examples/complex_arithmetic.v",
        "examples/bitwise_operations.v"
    ]
    
    for file_path in test_files:
        print(f"\\nTesting {file_path}:")
        try:
            if os.path.exists(file_path):
                netlist = parse_arithmetic_verilog_simple(file_path)
                stats = get_arithmetic_stats(netlist)
                
                print(f"  [OK] Parsed successfully")
                print(f"  Name: {stats['name']}")
                print(f"  Inputs: {stats['total_inputs']}")
                print(f"  Outputs: {stats['total_outputs']}")
                print(f"  Nodes: {stats['total_nodes']}")
                print(f"  Vector widths: {stats['vector_widths']}")
                print(f"  Gate counts: {stats['gate_counts']}")
            else:
                print(f"  [WARNING] File not found: {file_path}")
        except Exception as e:
            print(f"  [ERROR] Parsing failed: {e}")
    
    print("\\n[OK] Simple arithmetic Verilog parser test completed")
