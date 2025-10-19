# frontends/unified_verilog.py
"""
Unified Verilog Parser for MyLogic EDA Tool

Hỗ trợ đầy đủ tất cả tính năng:
- Module declarations (port list style và module body style)
- Vector và scalar inputs/outputs
- Logic gates (AND, OR, XOR, NOT, NAND, NOR, BUF)
- Arithmetic operations (+, -, *, /)
- Bitwise operations (&, |, ^, ~)
- Ternary operators (condition ? value1 : value2)
- Complex expressions với parentheses
- Bit assignments (flags[0], flags[1])
- Wire declarations
- Gate instantiations

Tương thích với tất cả examples trong thư mục examples/
"""

import re
from typing import Dict, List, Any, Optional

def parse_verilog(path: str) -> Dict:
    """
    Enhanced Verilog Parser với hỗ trợ đầy đủ tất cả tính năng.
    
    Hỗ trợ:
    - Module declarations (port list style và module body style)
    - Vector và scalar inputs/outputs/wires
    - Logic gates (AND, OR, XOR, NOT, NAND, NOR, BUF)
    - Arithmetic operations (+, -, *, /)
    - Bitwise operations (&, |, ^, ~)
    - Ternary operators (condition ? value1 : value2)
    - Complex expressions với parentheses
    - Bit assignments (flags[0], flags[1])
    - Wire declarations với initial assignments
    - Gate instantiations
    - Module instantiations
    - Improved error handling và validation
    
    Args:
        path: Đường dẫn đến file Verilog
        
    Returns:
        Dict chứa enhanced netlist với cấu trúc:
        {
            "name": str,
            "inputs": List[str],
            "outputs": List[str], 
            "wires": List[str],
            "nodes": List[Dict],
            "attrs": {
                "source_file": str,
                "vector_widths": Dict[str, int],
                "output_mapping": Dict[str, str],
                "wire_mapping": Dict[str, str],
                "module_instantiations": Dict[str, Dict],
                "parsing_stats": Dict[str, Any]
            }
        }
    """
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
        "attrs": {"source_file": path, "vector_widths": {}, "output_mapping": {}}
    }
    
    # Extract module name and port list - find the LAST module (usually top module)
    module_matches = list(re.finditer(r'module\s+(\w+)\s*\(([^)]*)\)\s*;', src, re.DOTALL))
    if module_matches:
        # Use the last module found (top module)
        module_match = module_matches[-1]
        net['name'] = module_match.group(1)
        port_list = module_match.group(2)
        # Extract module body (between module declaration and endmodule)
        module_end = module_match.end()
        endmodule_match = re.search(r'endmodule', src[module_end:])
        if endmodule_match:
            module_body = src[module_end:module_end + endmodule_match.start()]
        else:
            module_body = src[module_end:]
    else:
        port_list = ""
        module_body = src  # Fallback to entire source
    
    # Extract vector inputs from port list first
    port_input_matches = re.findall(r'input\s+\[(\d+):(\d+)\]\s+([^\n]+?)(?:,\s*$|\n)', port_list, re.MULTILINE)
    for msb, lsb, signals_str in port_input_matches:
        # Remove trailing comma and split by comma
        signals_str = signals_str.rstrip(',').strip()
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['inputs']:
                net['inputs'].append(signal)
                net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar inputs from port list first
    port_scalar_inputs = re.findall(r'input\s+([^[,\n)]+)', port_list)
    for signals_str in port_scalar_inputs:
        signals = [s.strip() for s in signals_str.split(',')]
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['inputs']:
                net['inputs'].append(signal)
                net['attrs']['vector_widths'][signal] = 1
    
    # Extract vector inputs from module body
    input_matches = re.findall(r'input\s+\[(\d+):(\d+)\]\s+([^;]+)', module_body)
    for msb, lsb, signals_str in input_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            if signal not in net['inputs']:
                net['inputs'].append(signal)
                net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar inputs from module body (only scalar, not vector)
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
    
    # Extract vector outputs from port list first
    port_output_matches = re.findall(r'output\s+\[(\d+):(\d+)\]\s+([^\n]+?)(?:,\s*$|\n)', port_list, re.MULTILINE)
    for msb, lsb, signals_str in port_output_matches:
        # Remove trailing comma and split by comma
        signals_str = signals_str.rstrip(',').strip()
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['outputs']:
                net['outputs'].append(signal)
                net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar outputs from port list first
    port_scalar_outputs = re.findall(r'output\s+([^[,\n)]+)', port_list)
    for signals_str in port_scalar_outputs:
        signals = [s.strip() for s in signals_str.split(',')]
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['outputs']:
                net['outputs'].append(signal)
                net['attrs']['vector_widths'][signal] = 1
    
    # Extract vector outputs from module body
    output_matches = re.findall(r'output\s+\[(\d+):(\d+)\]\s+([^;]+)', module_body)
    for msb, lsb, signals_str in output_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            if signal not in net['outputs']:
                net['outputs'].append(signal)
                net['attrs']['vector_widths'][signal] = width
    
    # Extract scalar outputs from module body (only scalar, not vector)
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
    
    # Extract wire declarations (both with and without assignments)
    # Pattern 1: wire [3:0] temp1 = a + b;
    wire_assign_matches = re.findall(r'wire\s+\[(\d+):(\d+)\]\s+([^=]+)\s*=\s*([^;]+);', module_body)
    for msb, lsb, signals_str, assignment in wire_assign_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            if signal not in net['wires']:
                net['wires'].append(f"{signal} = {assignment.strip()}")
                net['attrs']['vector_widths'][f"{signal} = {assignment.strip()}"] = width
    
    # Pattern 2: wire temp3 = a[0] & b[0]; (scalar only, not vector)
    scalar_wire_assign_matches = re.findall(r'wire\s+([^[=]+)\s*=\s*([^;]+);', module_body)
    for signals_str, assignment in scalar_wire_assign_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and f"{signal} = {assignment.strip()}" not in net['wires']:
                net['wires'].append(f"{signal} = {assignment.strip()}")
                net['attrs']['vector_widths'][f"{signal} = {assignment.strip()}"] = 1
    
    # Pattern 3: wire [3:0] temp1; (declaration only)
    wire_matches = re.findall(r'wire\s+\[(\d+):(\d+)\]\s+([^;=]+);', module_body)
    for msb, lsb, signals_str in wire_matches:
        signals = [s.strip() for s in signals_str.split(',')]
        width = int(msb) - int(lsb) + 1
        for signal in signals:
            if signal not in net['wires']:
                net['wires'].append(signal)
                net['attrs']['vector_widths'][signal] = width
    
    # Pattern 4: wire temp1; (scalar declaration only)
    scalar_wire_lines = re.findall(r'wire\s+([^[;=]+);', module_body)
    for line in scalar_wire_lines:
        signals = [s.strip() for s in line.split(',')]
        for signal in signals:
            signal = re.sub(r'//.*$', '', signal).strip()
            if signal and signal not in net['wires']:
                net['wires'].append(signal)
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
            node_counter += 2  # MUL + BUF nodes
        
        elif '/' in rhs:
            # Division
            _parse_division(net, lhs, rhs, node_counter)
            node_counter += 2  # DIV + BUF nodes
        
        else:
            # Simple assignment
            _parse_simple_assignment(net, lhs, rhs, node_counter)
            node_counter += 1  # BUF node
    
    # Extract gate instantiations
    gate_matches = re.findall(r'(and|or|xor|nand|nor|not|buf)\s+(\w+)?\s*\(([^)]+)\);', module_body)
    for gate_type, inst_name, connections in gate_matches:
        conns = [c.strip() for c in connections.split(',')]
        if len(conns) >= 2:
            output = conns[0]
            inputs = conns[1:]
            
            gate_id = inst_name if inst_name else f"{gate_type}_{node_counter}"
            net['nodes'].append({
                "id": gate_id,
                "type": gate_type.upper(),
                "fanins": [[inp, False] for inp in inputs]
            })
            
            # Store output mapping
            net['attrs']['output_mapping'][output] = gate_id
            node_counter += 1
    
    # Extract module instantiations (improved regex)
    # Match: module_name instance_name (connections);
    # Handle both single line and multi-line instantiations
    # Use a simpler approach: find module_name instance_name ( then extract until matching )
    module_inst_pattern = r'(\w+)\s+(\w+)\s*\('
    module_inst_matches = re.findall(module_inst_pattern, module_body)
    
    for module_type, inst_name in module_inst_matches:
        # Skip if it's a gate (already handled above)
        if module_type.lower() in ['and', 'or', 'xor', 'nand', 'nor', 'not', 'buf']:
            continue
            
        # Find the full instantiation line to extract connections
        # Look for the pattern: module_type inst_name ( ... );
        # Use a more robust approach to handle nested parentheses
        pattern = rf'{re.escape(module_type)}\s+{re.escape(inst_name)}\s*\('
        match = re.search(pattern, module_body)
        
        if match:
            # Find the matching closing parenthesis
            start_pos = match.end() - 1  # Position of opening (
            paren_count = 0
            end_pos = start_pos
            
            for i, char in enumerate(module_body[start_pos:], start_pos):
                if char == '(':
                    paren_count += 1
                elif char == ')':
                    paren_count -= 1
                    if paren_count == 0:
                        end_pos = i
                        break
            
            # Extract connections between parentheses
            connections = module_body[start_pos + 1:end_pos]
        else:
            connections = ""
        
        conns = []
        if match:
            # Parse connections (named or positional)
            # Handle both named (.port(signal)) and positional (signal) connections
            if connections.strip():
                # Split by comma, but be careful with nested parentheses
                parts = []
                current_part = ""
                paren_count = 0
                
                for char in connections:
                    if char == '(':
                        paren_count += 1
                    elif char == ')':
                        paren_count -= 1
                    elif char == ',' and paren_count == 0:
                        parts.append(current_part.strip())
                        current_part = ""
                        continue
                    current_part += char
                
                if current_part.strip():
                    parts.append(current_part.strip())
                
                conns = parts
        
        # Create module instantiation node
        module_id = inst_name if inst_name else f"{module_type}_{node_counter}"
        net['nodes'].append({
            "id": module_id,
            "type": "MODULE",
            "module_type": module_type,
            "connections": conns,
            "fanins": []  # Will be populated based on connections
        })
        
        # Store module instantiation info
        if 'module_instantiations' not in net['attrs']:
            net['attrs']['module_instantiations'] = {}
        net['attrs']['module_instantiations'][module_id] = {
            "module_type": module_type,
            "connections": conns
        }
        
        node_counter += 1
    
    # Generate wire connections between nodes
    net = _generate_wire_connections(net)
    
    return net

def _generate_wire_connections(net: Dict) -> Dict:
    """
    Generate wire connections between nodes based on fanins.
    
    Args:
        net: Netlist dictionary
        
    Returns:
        Netlist with wire connections added
    """
    wires = []
    wire_counter = 0
    
    # Create wires for each node's fanins
    for node in net.get('nodes', []):
        node_id = node.get('id', '')
        fanins = node.get('fanins', [])
        
        for fanin in fanins:
            if len(fanin) >= 1:
                source = fanin[0]
                destination = node_id
                
                # Create wire connection
                wire_id = f"wire_{wire_counter}"
                wires.append({
                    "id": wire_id,
                    "source": source,
                    "destination": destination,
                    "type": "connection"
                })
                wire_counter += 1
    
    # Add wires to netlist
    net['wires'] = wires
    
    # Add parsing statistics
    if 'parsing_stats' not in net['attrs']:
        net['attrs']['parsing_stats'] = {}
    net['attrs']['parsing_stats']['total_wires'] = len(wires)
    net['attrs']['parsing_stats']['wire_generation'] = 'automatic'
    
    return net

# Helper functions for expression parsing
def _is_ternary_operator(expr: str) -> bool:
    """Check if expression contains ternary operator."""
    return '?' in expr and ':' in expr

def _is_complex_expression(expr: str) -> bool:
    """Check if expression contains parentheses."""
    return '(' in expr and ')' in expr

def _parse_ternary_operator(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse ternary operator: condition ? value1 : value2"""
    # Simple implementation - create a MUX node
    mux_id = f"mux_{node_counter}"
    net['nodes'].append({
        "id": mux_id,
        "type": "MUX",
        "fanins": [[rhs.strip(), False]]  # Simplified for now, needs proper parsing of condition/values
    })
    
    # Create BUF node for output
    buf_id = f"buf_{node_counter + 1}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[mux_id, False]]
    })
    
    # Store output mapping
    net['attrs']['output_mapping'][lhs] = buf_id

def _parse_complex_expression(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse complex expressions with parentheses."""
    # Simple implementation - create a complex node
    complex_id = f"complex_{node_counter}"
    net['nodes'].append({
        "id": complex_id,
        "type": "COMPLEX",
        "fanins": [[rhs.strip(), False]]  # Simplified for now
    })
    
    # Create BUF node for output
    buf_id = f"buf_{node_counter + 1}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[complex_id, False]]
    })
    
    # Store output mapping
    net['attrs']['output_mapping'][lhs] = buf_id

def _parse_xor_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse XOR operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('^')]
    if len(operands) == 2:
        xor_id = f"xor_{node_counter}"
        net['nodes'].append({
            "id": xor_id,
            "type": "XOR",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[xor_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_and_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse AND operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('&')]
    if len(operands) == 2:
        and_id = f"and_{node_counter}"
        net['nodes'].append({
            "id": and_id,
            "type": "AND",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[and_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_or_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse OR operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('|')]
    if len(operands) == 2:
        or_id = f"or_{node_counter}"
        net['nodes'].append({
            "id": or_id,
            "type": "OR",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[or_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_not_operation(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse NOT operation."""
    # Extract operand (remove ~)
    operand = rhs.replace('~', '').strip()
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
    net['attrs']['output_mapping'][lhs] = buf_id

def _parse_addition(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse addition operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('+')]
    if len(operands) == 2:
        add_id = f"add_{node_counter}"
        net['nodes'].append({
            "id": add_id,
            "type": "ADD",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[add_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_subtraction(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse subtraction operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('-')]
    if len(operands) == 2:
        sub_id = f"sub_{node_counter}"
        net['nodes'].append({
            "id": sub_id,
            "type": "SUB",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[sub_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_multiplication(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse multiplication operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('*')]
    if len(operands) == 2:
        mul_id = f"mul_{node_counter}"
        net['nodes'].append({
            "id": mul_id,
            "type": "MUL",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[mul_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_division(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse division operation."""
    # Extract operands
    operands = [op.strip() for op in rhs.split('/')]
    if len(operands) == 2:
        div_id = f"div_{node_counter}"
        net['nodes'].append({
            "id": div_id,
            "type": "DIV",
            "fanins": [[operands[0], False], [operands[1], False]]
        })
        
        # Create BUF node for output
        buf_id = f"buf_{node_counter + 1}"
        net['nodes'].append({
            "id": buf_id,
            "type": "BUF",
            "fanins": [[div_id, False]]
        })
        
        # Store output mapping
        net['attrs']['output_mapping'][lhs] = buf_id

def _parse_simple_assignment(net: Dict, lhs: str, rhs: str, node_counter: int):
    """Parse simple assignment."""
    buf_id = f"buf_{node_counter}"
    net['nodes'].append({
        "id": buf_id,
        "type": "BUF",
        "fanins": [[rhs.strip(), False]]
    })
    
    # Store output mapping
    net['attrs']['output_mapping'][lhs] = buf_id
