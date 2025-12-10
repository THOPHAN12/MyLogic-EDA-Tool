"""
Verilog Parser - Main Parser Logic

File này tổng hợp tất cả các modules lại:
- tokenizer: Làm sạch và tokenize code
- node_builder: Tạo nodes và connections
- operations/*: Parse từng loại operation

Flow:
1. Tokenize source code
2. Extract ports và wires
3. Parse assign statements
4. Parse gate/module instantiations
5. Generate wire connections
6. Compute statistics

Author: MyLogic Team
Version: 2.0.0 (Refactored)
"""

from typing import Dict, Any, List
import re

from .tokenizer import (
    VerilogTokenizer,
    split_signal_list,
    calculate_vector_width,
    remove_inline_comments
)
from .node_builder import NodeBuilder, WireGenerator
from .constants import *
from ..operations import *
from .expression_parser import parse_complex_expression


def parse_verilog(path: str) -> Dict[str, Any]:
    """
    Parse file Verilog thành netlist dictionary.
    
    Đây là entry point chính của parser. Function này:
    1. Đọc file Verilog
    2. Tokenize và làm sạch code
    3. Extract module info, ports, wires
    4. Parse tất cả statements
    5. Generate connections
    6. Tính statistics
    
    Args:
        path: Đường dẫn đến file Verilog
        
    Returns:
        Dictionary chứa netlist với cấu trúc:
        {
            "name": str,              # Tên module
            "inputs": List[str],      # Danh sách inputs
            "outputs": List[str],     # Danh sách outputs
            "wires": List[Dict],      # Danh sách wire connections
            "nodes": List[Dict],      # Danh sách nodes (operations)
            "attrs": {                # Attributes bổ sung
                "source_file": str,
                "vector_widths": Dict,
                "output_mapping": Dict,
                "parsing_stats": Dict
            }
        }
        
    Raises:
        ValueError: Nếu path invalid
        FileNotFoundError: Nếu file không tồn tại
    """
    # Validate input
    if not path or not isinstance(path, str):
        raise ValueError("Path phải là string không rỗng")
    
    # Đọc file - nâng cấp error handling giống YosysHQ
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            source_code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file: {path}")
    except UnicodeDecodeError as e:
        # Thử với encoding khác nếu UTF-8 fail
        try:
            with open(path, 'r', encoding='latin-1') as f:
                source_code = f.read()
        except Exception:
            raise ValueError(f"Không thể đọc file {path}: encoding error - {e}")
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file {path}: {e}")
    
    # Khởi tạo netlist structure
    netlist = _initialize_netlist(path)
    
    # Bước 1: Tokenize
    tokenizer = VerilogTokenizer(source_code, path)
    tokens = tokenizer.tokenize()
    
    # Bước 2: Extract module info
    netlist['name'] = tokens['module_name']
    
    # Bước 3: Parse ports và wires
    _parse_port_declarations(netlist, tokens)
    _parse_wire_declarations(netlist, tokens['module_body'])
    
    # Bước 3.5: Parse parameters và localparams
    _parse_parameters(netlist, tokens['module_body'])
    
    # Bước 4: Parse assign statements, always blocks, và gates
    node_builder = NodeBuilder()
    _parse_always_blocks(netlist, tokens['module_body'], node_builder)
    _parse_assign_statements(netlist, tokens['module_body'], node_builder)
    _parse_gate_instantiations(netlist, tokens['module_body'], node_builder)
    _parse_module_instantiations(netlist, tokens['module_body'], node_builder)
    
    # Bước 5: Lấy nodes từ builder
    netlist['nodes'] = node_builder.get_nodes()
    netlist['attrs']['output_mapping'].update(node_builder.get_output_mapping())
    
    # Bước 6: Generate wire connections
    if AUTO_GENERATE_WIRES:
        wires = WireGenerator.generate_wires(netlist['nodes'])
        netlist['wires'] = wires
        WireGenerator.add_wire_statistics(netlist, wires)
    
    # Bước 7: Compute statistics
    if COMPUTE_STATISTICS:
        _compute_statistics(netlist)
    
    # Bước 8: Ensure output mapping
    _ensure_output_mapping(netlist)
    
    return netlist


# ============================================================================
# INITIALIZATION
# ============================================================================

def _initialize_netlist(source_file: str) -> Dict[str, Any]:
    """
    Khởi tạo netlist structure rỗng.
    
    Args:
        source_file: Path đến file nguồn
        
    Returns:
        Netlist dictionary với structure cơ bản
    """
    return {
        "name": "",
        "inputs": [],
        "outputs": [],
        "wires": [],
        "nodes": [],
        "attrs": {
            "source_file": source_file,
            "vector_widths": {},
            "output_mapping": {},
            "parsing_stats": {}
        }
    }


# ============================================================================
# PORT DECLARATIONS PARSING
# ============================================================================

def _parse_port_declarations(netlist: Dict, tokens: Dict):
    """
    Parse input/output declarations từ port list và module body.
    
    Hỗ trợ:
    - Vector ports: input [3:0] a, b;
    - Scalar ports: input clk, reset;
    - Port list style: module test(input a, output b);
    - Module body style: input a; output b;
    
    Args:
        netlist: Netlist dictionary để update
        tokens: Tokens từ tokenizer
    """
    port_list = tokens['port_list']
    module_body = tokens['module_body']
    
    # Parse inputs
    _parse_input_ports(netlist, port_list, module_body)
    
    # Parse outputs
    _parse_output_ports(netlist, port_list, module_body)


def _parse_input_ports(netlist: Dict, port_list: str, module_body: str):
    """Parse input ports (cả vector và scalar)."""
    
    # 1. Vector inputs từ port list
    for match in PORT_INPUT_VECTOR_PATTERN.finditer(port_list):
        msb, lsb, signals_str = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['inputs']:
                netlist['inputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
    
    # 2. Scalar inputs từ port list
    for match in PORT_INPUT_SCALAR_PATTERN.finditer(port_list):
        signals_str = match.group(1)
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['inputs']:
                netlist['inputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1
    
    # 3. Vector inputs từ module body
    for match in INPUT_VECTOR_PATTERN.finditer(module_body):
        msb, lsb, signals_str = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            if signal not in netlist['inputs']:
                netlist['inputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
    
    # 4. Scalar inputs từ module body
    for match in INPUT_SCALAR_PATTERN.finditer(module_body):
        signals_str = match.group(1)
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['inputs']:
                netlist['inputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1


def _parse_output_ports(netlist: Dict, port_list: str, module_body: str):
    """Parse output ports (cả vector và scalar)."""
    
    # 1. Vector outputs từ port list
    for match in PORT_OUTPUT_VECTOR_PATTERN.finditer(port_list):
        msb, lsb, signals_str = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['outputs']:
                netlist['outputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
    
    # 2. Scalar outputs từ port list
    for match in PORT_OUTPUT_SCALAR_PATTERN.finditer(port_list):
        signals_str = match.group(1)
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['outputs']:
                netlist['outputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1
    
    # 3. Vector outputs từ module body
    for match in OUTPUT_VECTOR_PATTERN.finditer(module_body):
        msb, lsb, signals_str = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            if signal not in netlist['outputs']:
                netlist['outputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
    
    # 4. Scalar outputs từ module body
    for match in OUTPUT_SCALAR_PATTERN.finditer(module_body):
        signals_str = match.group(1)
        for signal in split_signal_list(signals_str):
            if signal and signal not in netlist['outputs']:
                netlist['outputs'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1


# ============================================================================
# PARAMETER & LOCALPARAM PARSING
# ============================================================================

def _parse_parameters(netlist: Dict, module_body: str):
    """
    Parse parameter và localparam declarations.
    
    Hỗ trợ:
    - parameter WIDTH = 8;
    - parameter DEPTH = 16, ADDR_WIDTH = 4;
    - localparam MAX = 255;
    - parameter [7:0] DATA = 8'hFF;
    
    Args:
        netlist: Netlist dictionary để update
        module_body: Module body content
    """
    from .constants import PARAMETER_PATTERN, LOCALPARAM_PATTERN
    
    parameters = netlist['attrs'].setdefault('parameters', {})
    
    # Parse parameters
    for match in PARAMETER_PATTERN.finditer(module_body):
        param_name = match.group(1).strip()
        param_value = match.group(2).strip()
        parameters[param_name] = param_value
    
    # Parse localparams
    for match in LOCALPARAM_PATTERN.finditer(module_body):
        param_name = match.group(1).strip()
        param_value = match.group(2).strip()
        parameters[param_name] = param_value
        parameters[f'localparam_{param_name}'] = param_value  # Mark as localparam


# ============================================================================
# WIRE DECLARATIONS PARSING
# ============================================================================

def _parse_wire_declarations(netlist: Dict, module_body: str):
    """
    Parse wire declarations - nâng cấp giống YosysHQ.
    
    Hỗ trợ:
    - wire [3:0] temp;
    - wire [3:0] temp = a + b;
    - wire clk;
    - wire ready = enable & valid;
    - Multiple declarations: wire a, b, c;
    - Mixed vector và scalar: wire [7:0] data; wire clk;
    """
    from .constants import (
        WIRE_VECTOR_ASSIGN_PATTERN, WIRE_SCALAR_ASSIGN_PATTERN,
        WIRE_VECTOR_PATTERN, WIRE_SCALAR_PATTERN
    )
    
    # Pattern 1: wire [3:0] temp = assignment;
    for match in WIRE_VECTOR_ASSIGN_PATTERN.finditer(module_body):
        msb, lsb, signals_str, assignment = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                wire_entry = f"{signal} = {assignment.strip()}"
                if wire_entry not in netlist['wires']:
                    netlist['wires'].append(wire_entry)
                    netlist['attrs']['vector_widths'][wire_entry] = width
                    netlist['attrs']['vector_widths'][signal] = width  # Also store signal width
    
    # Pattern 2: wire temp = assignment; (scalar)
    for match in WIRE_SCALAR_ASSIGN_PATTERN.finditer(module_body):
        signals_str, assignment = match.groups()
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                wire_entry = f"{signal} = {assignment.strip()}"
                if wire_entry not in netlist['wires']:
                    netlist['wires'].append(wire_entry)
                    netlist['attrs']['vector_widths'][wire_entry] = 1
                    netlist['attrs']['vector_widths'][signal] = 1
    
    # Pattern 3: wire [3:0] temp; (declaration only)
    for match in WIRE_VECTOR_PATTERN.finditer(module_body):
        msb, lsb, signals_str = match.groups()
        width = calculate_vector_width(msb, lsb)
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal and signal not in netlist['wires']:
                netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
    
    # Pattern 4: wire temp; (scalar declaration)
    for match in WIRE_SCALAR_PATTERN.finditer(module_body):
        signals_str = match.group(1)
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal and signal not in netlist['wires']:
                netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1
    
    # Pattern 5: reg declarations (giống wire)
    for match in REG_PATTERN.finditer(module_body):
        msb, lsb, signals_str = match.groups() if len(match.groups()) >= 3 else (None, None, match.group(1) if match.group(1) else "")
        if msb and lsb:
            width = calculate_vector_width(msb, lsb)
        else:
            width = 1
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                # Regs có thể không là wires, nhưng vẫn cần track
                if signal not in netlist['wires']:
                    netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
                netlist['attrs'].setdefault('reg_signals', []).append(signal)


# ============================================================================
# ALWAYS BLOCKS PARSING (SEQUENTIAL CIRCUITS)
# ============================================================================

def _parse_always_blocks(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse always blocks cho sequential circuits.
    
    Hỗ trợ:
    - always @(posedge clk) { ... }
    - always @(negedge clk) { ... }
    - Non-blocking assignments (<=)
    - Blocking assignments (=) trong always blocks
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        node_builder: NodeBuilder instance
    """
    from .constants import (
        ALWAYS_PATTERN, EDGE_PATTERN, POSEDGE_PATTERN, NEGEDGE_PATTERN,
        NON_BLOCKING_ASSIGN_PATTERN, BLOCKING_ASSIGN_PATTERN, BEGIN_END_PATTERN
    )
    
    # Tìm tất cả always blocks
    for match in ALWAYS_PATTERN.finditer(module_body):
        sensitivity_list = match.group(1).strip()
        # Group 2 là begin...end content, group 3 là {...} content
        block_content = (match.group(2) or match.group(3) or '').strip()
        
        # Parse edge sensitivity (posedge/negedge)
        clock_signal = None
        edge_type = None
        
        posedge_match = POSEDGE_PATTERN.search(sensitivity_list)
        negedge_match = NEGEDGE_PATTERN.search(sensitivity_list)
        
        if posedge_match:
            clock_signal = posedge_match.group(1)
            edge_type = 'posedge'
        elif negedge_match:
            clock_signal = negedge_match.group(1)
            edge_type = 'negedge'
        else:
            # Combinational always block (@(*) hoặc không có edge)
            # Parse như combinational logic (blocking assignments)
            _parse_always_combinational(block_content, node_builder)
            continue
        
        # Sequential always block với clock edge
        # Extract begin-end content nếu có
        begin_match = BEGIN_END_PATTERN.search(block_content)
        if begin_match:
            block_content = begin_match.group(1).strip()
        
        # Parse non-blocking assignments (<=) - Sequential logic
        _parse_always_sequential(block_content, clock_signal, edge_type, node_builder)


def _parse_always_sequential(
    block_content: str,
    clock_signal: str,
    edge_type: str,
    node_builder: NodeBuilder
):
    """
    Parse sequential always block với clock edge.
    
    Args:
        block_content: Nội dung của always block
        clock_signal: Clock signal name
        edge_type: 'posedge' hoặc 'negedge'
        node_builder: NodeBuilder instance
    """
    from .constants import NON_BLOCKING_ASSIGN_PATTERN
    from .expression_parser import parse_complex_expression
    
    # Tìm tất cả non-blocking assignments (<=)
    for match in NON_BLOCKING_ASSIGN_PATTERN.finditer(block_content):
        output_signal = match.group(1).strip()
        input_expression = match.group(2).strip()
        
        # Tạo DFF node cho sequential assignment
        dff_node_id = node_builder.create_sequential_node(
            node_type='DFF',
            data_input=input_expression,
            clock_signal=clock_signal,
            edge_type=edge_type,
            output_signal=output_signal
        )


def _parse_always_combinational(block_content: str, node_builder: NodeBuilder):
    """
    Parse combinational always block (@(*) hoặc không có edge).
    
    Args:
        block_content: Nội dung của always block
        node_builder: NodeBuilder instance
    """
    from .constants import BLOCKING_ASSIGN_PATTERN
    from .expression_parser import parse_complex_expression
    
    # Extract begin-end content nếu có
    from .constants import BEGIN_END_PATTERN
    begin_match = BEGIN_END_PATTERN.search(block_content)
    if begin_match:
        block_content = begin_match.group(1).strip()
    
    # Tìm tất cả blocking assignments (=)
    for match in BLOCKING_ASSIGN_PATTERN.finditer(block_content):
        output_signal = match.group(1).strip()
        input_expression = match.group(2).strip()
        
        # Parse expression như combinational logic
        parse_complex_expression(node_builder, output_signal, input_expression)


# ============================================================================
# ASSIGN STATEMENTS PARSING
# ============================================================================

def _parse_assign_statements(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse tất cả assign statements.
    
    Assign statements có format:
        assign output = expression;
        
    Expression có thể là:
    - Arithmetic: a + b, a - b, a * b, a / b, a % b
    - Bitwise: a & b, a | b, a ^ b, ~a
    - Logical: a && b, a || b, !a
    - Comparison: a == b, a != b, a < b, a > b
    - Shift: a << 2, a >> 1
    - Special: cond ? a : b, {a, b}, a[3:0]
    - Simple: wire = signal
    """
    
    for match in ASSIGN_PATTERN.finditer(module_body):
        lhs, rhs = match.groups()
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        # Dispatch đến parser thích hợp dựa trên operators
        _dispatch_assign_parser(lhs, rhs, node_builder)


def _dispatch_assign_parser(lhs: str, rhs: str, node_builder: NodeBuilder):
    """
    Dispatch assignment đến parser thích hợp.
    
    Kiểm tra operators theo thứ tự ưu tiên.
    """
    from ..operations.arithmetic import detect_arithmetic_operator
    from ..operations.bitwise import detect_bitwise_operator
    from ..operations.logical import detect_logical_operator
    from ..operations.comparison import detect_comparison_operator
    from ..operations.shift import detect_shift_operator
    
    # 1. Special operations (check trước vì phức tạp nhất)
    if is_ternary(rhs):
        parse_ternary_operation(node_builder, lhs, rhs)
        return
    
    if is_concatenation(rhs):
        parse_concatenation(node_builder, lhs, rhs)
        return
    
    if is_slice(rhs):
        parse_slice(node_builder, lhs, rhs)
        return
    
    # 2. Complex expressions với parentheses
    # Check trước các simple operators
    if '(' in rhs and ')' in rhs:
        # Có parentheses - có thể là complex expression
        # Check xem có nhiều operators không
        has_multiple_ops = sum([
            rhs.count('&'), rhs.count('|'), rhs.count('^'),
            rhs.count('+'), rhs.count('-')
        ]) > 1
        
        if has_multiple_ops:
            # Complex expression, dùng expression parser
            parse_complex_expression(node_builder, lhs, rhs)
            return
    
    # 3. Shift operations (check trước comparison vì >> có thể nhầm với >)
    shift_op = detect_shift_operator(rhs)
    if shift_op:
        from ..operations.shift import parse_shift_operation
        parse_shift_operation(node_builder, shift_op, lhs, rhs)
        return
    
    # 4. Comparison operations
    comp_op = detect_comparison_operator(rhs)
    if comp_op:
        from ..operations.comparison import parse_comparison_operation
        parse_comparison_operation(node_builder, comp_op, lhs, rhs)
        return
    
    # 5. Logical operations  
    logical_op = detect_logical_operator(rhs)
    if logical_op:
        from ..operations.logical import parse_logical_operation
        parse_logical_operation(node_builder, logical_op, lhs, rhs)
        return
    
    # 6. Bitwise operations
    bitwise_op = detect_bitwise_operator(rhs)
    if bitwise_op:
        from ..operations.bitwise import parse_bitwise_operation
        parse_bitwise_operation(node_builder, bitwise_op, lhs, rhs)
        return
    
    # 7. Arithmetic operations
    arith_op = detect_arithmetic_operator(rhs)
    if arith_op:
        from ..operations.arithmetic import parse_arithmetic_operation
        parse_arithmetic_operation(node_builder, arith_op, lhs, rhs)
        return
    
    # 8. Simple assignment (fallback)
    node_builder.create_simple_assignment(lhs, rhs)


# ============================================================================
# GATE & MODULE INSTANTIATIONS
# ============================================================================

def _parse_gate_instantiations(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """Parse gate instantiations (and, or, xor, etc.)."""
    
    for match in GATE_PATTERN.finditer(module_body):
        gate_type, inst_name, connections = match.groups()
        
        # Parse connections
        conns = [c.strip() for c in connections.split(',')]
        if len(conns) >= 2:
            output = conns[0]
            inputs = conns[1:]
            
            # Tạo gate node
            node_builder.create_gate_node(gate_type, inst_name, inputs, output)


def _parse_module_instantiations(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse module instantiations với hỗ trợ đầy đủ như YosysHQ.
    
    Hỗ trợ:
    - Ordered ports: module_inst inst1 (a, b, c);
    - Named ports: module_inst inst1 (.port1(a), .port2(b));
    - Mixed: module_inst inst1 (a, .port2(b), c);
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        node_builder: NodeBuilder instance
    """
    from .constants import (
        MODULE_INST_PATTERN, NAMED_PORT_PATTERN, STANDARD_GATES
    )
    
    for match in MODULE_INST_PATTERN.finditer(module_body):
        module_type = match.group(1).strip()
        inst_name = match.group(2).strip() if match.group(2) else None
        port_list = match.group(3).strip() if match.group(3) else ""
        
        # Skip nếu là gate (đã được parse bởi _parse_gate_instantiations)
        if module_type.lower() in STANDARD_GATES:
            continue
        
        # Parse port connections
        connections = {}
        ordered_ports = []
        
        # Check if có named ports (.port(signal))
        has_named_ports = NAMED_PORT_PATTERN.search(port_list)
        
        if has_named_ports:
            # Parse named ports
            for port_match in NAMED_PORT_PATTERN.finditer(port_list):
                port_name = port_match.group(1).strip()
                port_signal = port_match.group(2).strip()
                connections[port_name] = port_signal
            
            # Parse ordered ports (nếu có - mixed mode)
            # Remove named ports từ port_list để tìm ordered ports
            remaining = NAMED_PORT_PATTERN.sub('', port_list)
            # Split by comma và filter
            ordered_candidates = [p.strip() for p in remaining.split(',') if p.strip() and not p.strip().startswith('.')]
            ordered_ports = [p for p in ordered_candidates if p]
        else:
            # Chỉ có ordered ports
            ordered_ports = [p.strip() for p in port_list.split(',') if p.strip()]
            # Create connections với index-based keys
            for i, signal in enumerate(ordered_ports):
                connections[f'port_{i}'] = signal
        
        # Generate instance name nếu không có
        if not inst_name:
            instance_counter = len([k for k in netlist.get('attrs', {}).get('module_instantiations', {})])
            inst_name = f"{module_type}_inst_{instance_counter}"
        
        # Create module instance node
        module_id = node_builder.create_module_instance_node(
            module_type=module_type,
            inst_name=inst_name,
            connections=connections
        )
        
        # Store trong netlist attributes
        if 'module_instantiations' not in netlist['attrs']:
            netlist['attrs']['module_instantiations'] = {}
        
        netlist['attrs']['module_instantiations'][module_id] = {
            "module_type": module_type,
            "instance_name": inst_name,
            "connections": connections,
            "ordered_ports": ordered_ports if not has_named_ports else None,
            "has_named_ports": has_named_ports is not None
        }


# ============================================================================
# STATISTICS & FINALIZATION
# ============================================================================

def _compute_statistics(netlist: Dict):
    """Tính toán statistics cho netlist."""
    nodes = netlist.get('nodes', [])
    
    # Count node types
    type_counts = {}
    for node in nodes:
        node_type = node.get('type', 'UNKNOWN')
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    # Group by categories
    category_counts = {cat: 0 for cat in NODE_CATEGORIES}
    for node_type, count in type_counts.items():
        for category, members in NODE_CATEGORIES.items():
            if node_type in members:
                category_counts[category] += count
    
    # Store statistics
    netlist['attrs']['operator_summary'] = {
        'type_counts': type_counts,
        'category_counts': category_counts,
        'total_nodes': len(nodes)
    }
    
    # Mirror to parsing_stats
    stats = netlist['attrs'].setdefault('parsing_stats', {})
    stats.update({
        'total_nodes': len(nodes),
        'logic_nodes': category_counts['logic'],
        'arith_nodes': category_counts['arith'],
        'shift_nodes': category_counts['shift'],
        'compare_nodes': category_counts['compare'],
        'logical_nodes': category_counts['logical'],
        'struct_nodes': category_counts['struct']
    })


def _ensure_output_mapping(netlist: Dict):
    """Ensure mọi output đều có mapping."""
    out_map = netlist['attrs'].setdefault('output_mapping', {})
    
    for node in netlist.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        # Bind output name to node if matching
        for out_name in netlist.get('outputs', []):
            if out_name not in out_map and out_name == node_id:
                out_map[out_name] = node_id

