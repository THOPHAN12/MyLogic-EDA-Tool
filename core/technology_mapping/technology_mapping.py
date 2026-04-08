#!/usr/bin/env python3
"""
Technology mapping — mạch tổ hợp (combinational), mức cơ bản / minh họa đề tài.

Phạm vi đề tài:
    - Không triển khai techmap công nghiệp (cut enumeration, mapper ABC, …).
    - Luồng: AIG → LogicNode (chuỗi hàm Boolean) → tra ``function_map`` sau
      ``normalize_function`` → chọn cell; shell/complete_flow cố định ``area_optimal``.
    - Mạch tuần tự: không map DFF/latch sang thư viện tại đây.

Nạp thư viện (SkyWater PDK, Liberty, JSON, …): ``library_loader.py``.
"""

from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)

def normalize_function(function: str) -> str:
    """
    Normalize function string by replacing variable names with canonical names.
    Also handles nested expressions by extracting simple input signals.
    
    Examples:
        normalize_function("OR(C,D)") -> "OR(A,B)"
        normalize_function("XOR(temp1,temp2)") -> "XOR(A,B)"
        normalize_function("AND(A,B)") -> "AND(A,B)"
        normalize_function("NOT(X)") -> "NOT(A)"
        normalize_function("NOT((a & b))") -> "NOT(A)"  # Extract first input from nested expr
        normalize_function("NOT(a)") -> "NOT(A)"
    
    Args:
        function: Function string like "OR(C,D)", "AND(A,B)", "NOT((a & b))", etc.
        
    Returns:
        Normalized function string with canonical variable names (A, B, C, ...)
    """
    if not function or '(' not in function:
        return function
    
    # Extract function name and arguments
    match = re.match(r'^(\w+)\((.*)\)$', function)
    if not match:
        return function
    
    func_name = match.group(1)
    args_str = match.group(2).strip()
    
    if not args_str:
        # No arguments (like CONST0, CONST1)
        return function
    
    # Canonicalize common AIG-derived patterns before generic normalization.
    canonical = _canonicalize_aig_pattern(function.strip())
    if canonical != function.strip():
        return canonical

    # Handle nested expressions: extract simple input signals
    # For functions like NOT((a & b)), we need to extract the input signal
    # Strategy: If argument contains operators (&, |, ^, etc.), try to extract first signal
    args = []
    
    # Check if args_str contains nested expressions (has operators)
    if any(op in args_str for op in ['&', '|', '^', '+', '-', '*', '/', '(', ')']):
        # Nested expression - try to extract input signals
        # For NOT((a & b)), we can't easily extract, so use first argument as-is
        # But we'll try to find simple signal names
        import re as re_module
        # Try to find simple signal names (alphanumeric + underscore)
        signal_pattern = r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'
        signals = re_module.findall(signal_pattern, args_str)
        if signals:
            # Use first signal found (for NOT, only need one input)
            if func_name == 'NOT':
                args = [signals[0]]
            else:
                # For other functions, use first 2 signals
                args = signals[:2] if len(signals) >= 2 else signals
        else:
            # No signals found, use original argument
            args = [args_str]
    else:
        # Simple arguments - split by comma
        args = [arg.strip() for arg in args_str.split(',')]
    
    # Generate canonical variable names (A, B, C, D, ...)
    canonical_args = [chr(65 + i) for i in range(len(args))]  # A=65, B=66, C=67, ...
    
    # Reconstruct normalized function
    normalized = f"{func_name}({','.join(canonical_args)})"
    
    return normalized


def _canonicalize_aig_pattern(function: str) -> str:
    """
    Collapse common raw AIG patterns into simple Boolean operators.

    Examples:
        AND(x,CONST1) -> BUF(A)
        AND(NOT(x),CONST1) -> NOT(A)
        AND(CONST1,x) -> BUF(A)
        AND(CONST1,NOT(x)) -> NOT(A)
    """
    match = re.match(r'^(\w+)\((.*)\)$', function)
    if not match:
        return function

    func_name = match.group(1).upper()
    args_str = match.group(2).strip()
    if func_name != "AND" or not args_str:
        return function

    args = _split_args(args_str)
    if len(args) != 2:
        return function

    left, right = args[0].strip(), args[1].strip()
    const_tokens = {"CONST1", "1'b1", "1"}

    if left in const_tokens and right in const_tokens:
        return "BUF(A)"
    if left in const_tokens:
        return _canonicalize_buffer_like_arg(right)
    if right in const_tokens:
        return _canonicalize_buffer_like_arg(left)

    return function


def _canonicalize_buffer_like_arg(arg: str) -> str:
    arg = arg.strip()
    not_match = re.match(r'^NOT\((.*)\)$', arg)
    if not_match:
        return "NOT(A)"
    return "BUF(A)"


def _split_args(args_str: str) -> List[str]:
    """Split function arguments while preserving nested calls."""
    args: List[str] = []
    current: List[str] = []
    depth = 0
    for ch in args_str:
        if ch == ',' and depth == 0:
            arg = ''.join(current).strip()
            if arg:
                args.append(arg)
            current = []
            continue
        if ch == '(':
            depth += 1
        elif ch == ')' and depth > 0:
            depth -= 1
        current.append(ch)
    tail = ''.join(current).strip()
    if tail:
        args.append(tail)
    return args

class LibraryCell:
    """Đại diện cho một cell trong thư viện công nghệ."""
    
    def __init__(self, name: str, function: str, area: float, delay: float, 
                 input_pins: List[str], output_pins: List[str], 
                 input_load: float = 1.0, output_drive: float = 1.0):
        self.name = name
        self.function = function  # Hàm Boolean
        self.area = area
        self.delay = delay
        self.input_pins = input_pins
        self.output_pins = output_pins
        self.input_load = input_load
        self.output_drive = output_drive
        
    def __repr__(self):
        return f"LibraryCell({self.name}, {self.function}, area={self.area}, delay={self.delay})"

class TechnologyLibrary:
    """Danh mục cell: ``cells`` + ``function_map`` (hàm đã chuẩn hóa → tên cell)."""
    
    def __init__(self, name: str):
        self.name = name
        self.cells: Dict[str, LibraryCell] = {}
        self.function_map: Dict[str, List[str]] = {}  # function -> list of cell names
        
    def add_cell(self, cell: LibraryCell):
        """Add a cell to the library."""
        self.cells[cell.name] = cell
        
        # Normalize function for mapping
        normalized_func = normalize_function(cell.function)
        
        # Update function mapping with normalized function
        if normalized_func not in self.function_map:
            self.function_map[normalized_func] = []
        self.function_map[normalized_func].append(cell.name)
    
    def get_cells_for_function(self, function: str) -> List[LibraryCell]:
        """Get all cells that implement a given function."""
        # Normalize the function to match library entries
        normalized_func = normalize_function(function)
        
        if normalized_func in self.function_map:
            return [self.cells[name] for name in self.function_map[normalized_func]]
        return []
    
    def get_best_cell_for_function(self, function: str, optimization_target: str = "area") -> Optional[LibraryCell]:
        """Get the best cell for a function based on optimization target."""
        cells = self.get_cells_for_function(function)
        if not cells:
            return None
        
        if optimization_target == "area":
            return min(cells, key=lambda c: c.area)
        elif optimization_target == "delay":
            return min(cells, key=lambda c: c.delay)
        elif optimization_target == "balanced":
            # Weighted combination of area and delay
            return min(cells, key=lambda c: c.area + c.delay * 10)
        
        return cells[0]

class LogicNode:
    """Represents a node in the logic network."""
    
    def __init__(self, name: str, function: str, inputs: List[str], output: str):
        self.name = name
        self.function = function
        self.inputs = inputs
        self.output = output
        self.mapped_cell: Optional[LibraryCell] = None
        self.mapping_cost = float('inf')
        
    def __repr__(self):
        mapped_info = f" -> {self.mapped_cell.name}" if self.mapped_cell else " (unmapped)"
        return f"LogicNode({self.name}, {self.function}{mapped_info})"

class TechnologyMapper:
    """
    Technology mapping engine (ánh xạ thiết kế sang thư viện standard cells).
    """
    
    def __init__(self, library: TechnologyLibrary):
        self.library = library
        self.logic_network: Dict[str, LogicNode] = {}
        self.mapping_results = {}
        
    def add_logic_node(self, node: LogicNode):
        """Add a logic node to the network."""
        self.logic_network[node.name] = node
    
    def perform_technology_mapping(self, strategy: str = "area_optimal") -> Dict[str, Any]:
        """
        Perform technology mapping.
        
        Args:
            strategy: "area_optimal", "delay_optimal", "balanced"
        """
        logger.info(f"Starting technology mapping with {strategy} strategy...")
        
        if strategy == "area_optimal":
            return self._area_optimal_mapping()
        elif strategy == "delay_optimal":
            return self._delay_optimal_mapping()
        elif strategy == "balanced":
            return self._balanced_mapping()
        else:
            return self._area_optimal_mapping()
    
    def _area_optimal_mapping(self) -> Dict[str, Any]:
        """Perform area-optimal technology mapping."""
        logger.debug("Performing area-optimal mapping...")
        
        total_area = 0.0
        mapped_nodes = 0
        
        for node_name, node in self.logic_network.items():
            # Find best cell for this function
            best_cell = self.library.get_best_cell_for_function(node.function, "area")
            
            if best_cell:
                node.mapped_cell = best_cell
                node.mapping_cost = best_cell.area
                total_area += best_cell.area
                mapped_nodes += 1
                logger.debug(f"Mapped {node_name} -> {best_cell.name} (area: {best_cell.area})")
            else:
                logger.warning(f"No suitable cell found for {node_name} with function {node.function}")
        
        return {
            'strategy': 'area_optimal',
            'total_area': total_area,
            'mapped_nodes': mapped_nodes,
            'total_nodes': len(self.logic_network),
            'mapping_success_rate': mapped_nodes / len(self.logic_network) if self.logic_network else 0
        }
    
    def _delay_optimal_mapping(self) -> Dict[str, Any]:
        """Perform delay-optimal technology mapping."""
        logger.debug("Performing delay-optimal mapping...")
        
        total_delay = 0.0
        mapped_nodes = 0
        
        for node_name, node in self.logic_network.items():
            # Find best cell for this function
            best_cell = self.library.get_best_cell_for_function(node.function, "delay")
            
            if best_cell:
                node.mapped_cell = best_cell
                node.mapping_cost = best_cell.delay
                total_delay += best_cell.delay
                mapped_nodes += 1
                logger.debug(f"Mapped {node_name} -> {best_cell.name} (delay: {best_cell.delay})")
            else:
                logger.warning(f"No suitable cell found for {node_name} with function {node.function}")
        
        return {
            'strategy': 'delay_optimal',
            'total_delay': total_delay,
            'mapped_nodes': mapped_nodes,
            'total_nodes': len(self.logic_network),
            'mapping_success_rate': mapped_nodes / len(self.logic_network) if self.logic_network else 0
        }
    
    def _balanced_mapping(self) -> Dict[str, Any]:
        """Perform balanced technology mapping."""
        logger.debug("Performing balanced mapping...")
        
        total_area = 0.0
        total_delay = 0.0
        mapped_nodes = 0
        
        for node_name, node in self.logic_network.items():
            # Find best cell for this function
            best_cell = self.library.get_best_cell_for_function(node.function, "balanced")
            
            if best_cell:
                node.mapped_cell = best_cell
                node.mapping_cost = best_cell.area + best_cell.delay * 10  # Weighted cost
                total_area += best_cell.area
                total_delay += best_cell.delay
                mapped_nodes += 1
                logger.debug(f"Mapped {node_name} -> {best_cell.name} (area: {best_cell.area}, delay: {best_cell.delay})")
            else:
                logger.warning(f"No suitable cell found for {node_name} with function {node.function}")
        
        return {
            'strategy': 'balanced',
            'total_area': total_area,
            'total_delay': total_delay,
            'mapped_nodes': mapped_nodes,
            'total_nodes': len(self.logic_network),
            'mapping_success_rate': mapped_nodes / len(self.logic_network) if self.logic_network else 0
        }
    
    def get_mapping_statistics(self) -> Dict[str, Any]:
        """Get technology mapping statistics."""
        mapped_nodes = sum(1 for node in self.logic_network.values() if node.mapped_cell)
        total_nodes = len(self.logic_network)
        
        # Count cells used
        cell_usage = {}
        for node in self.logic_network.values():
            if node.mapped_cell:
                cell_name = node.mapped_cell.name
                cell_usage[cell_name] = cell_usage.get(cell_name, 0) + 1
        
        return {
            'total_nodes': total_nodes,
            'mapped_nodes': mapped_nodes,
            'unmapped_nodes': total_nodes - mapped_nodes,
            'mapping_success_rate': mapped_nodes / total_nodes if total_nodes > 0 else 0,
            'cell_usage': cell_usage,
            'unique_cells_used': len(cell_usage)
        }
    
    def print_mapping_report(self, results: Dict[str, Any]):
        """Print technology mapping report."""
        print("\n" + "="*60)
        print("TECHNOLOGY MAPPING REPORT")
        print("="*60)
        
        print(f"Mapping Strategy: {results['strategy']}")
        print(f"Total Nodes: {results['total_nodes']}")
        print(f"Mapped Nodes: {results['mapped_nodes']}")
        print(f"Mapping Success Rate: {results['mapping_success_rate']*100:.1f}%")
        
        if 'total_area' in results:
            print(f"Total Area: {results['total_area']:.2f}")
        if 'total_delay' in results:
            print(f"Total Delay: {results['total_delay']:.2f}")
        
        stats = self.get_mapping_statistics()
        
        # Library information
        total_library_cells = len(self.library.cells)
        unique_functions = len(self.library.function_map)
        print(f"\nLibrary Information:")
        print(f"  Total cells in library: {total_library_cells}")
        print(f"  Unique functions: {unique_functions}")
        print(f"  Cells used: {stats['unique_cells_used']} out of {total_library_cells} available")
        
        print(f"\nCell Usage ({stats['unique_cells_used']} types, {stats['mapped_nodes']} instances):")
        if stats['cell_usage']:
            for cell_name, count in sorted(stats['cell_usage'].items()):
                percentage = (count / stats['mapped_nodes'] * 100) if stats['mapped_nodes'] > 0 else 0
                print(f"  {cell_name}: {count} instances ({percentage:.1f}%)")
        else:
            print("  No cells mapped")
        
        print(f"\nNode Mapping Details:")
        print(f"{'Node':<15} {'Function':<25} {'Mapped Cell':<15} {'Cost':<8}")
        print("-" * 65)
        
        for node_name, node in self.logic_network.items():
            mapped_cell = node.mapped_cell.name if node.mapped_cell else "None"
            cost = f"{node.mapping_cost:.2f}" if node.mapping_cost != float('inf') else "N/A"
            function_str = node.function[:24] if len(node.function) > 24 else node.function
            print(f"{node_name:<15} {function_str:<25} {mapped_cell:<15} {cost:<8}")

def create_standard_library() -> TechnologyLibrary:
    """
    Create a standard technology library with common gates.
    
    This is a fallback function. For better results, use load_library()
    to load from techlibs/ folder.
    """
    library = TechnologyLibrary("standard_cells")
    
    # Basic gates
    gates = [
        ("INV", "NOT", 1.0, 0.1, ["A"], ["Y"]),
        ("BUF", "BUF", 1.0, 0.05, ["A"], ["Y"]),
        
        # 2-input gates
        ("NAND2", "NAND(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("NOR2", "NOR(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        ("OR2", "OR(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        ("XOR2", "XOR(A,B)", 2.0, 0.25, ["A", "B"], ["Y"]),
        ("XNOR2", "XNOR(A,B)", 2.0, 0.25, ["A", "B"], ["Y"]),
        
        # 3-input gates
        ("NAND3", "NAND(A,B,C)", 1.8, 0.2, ["A", "B", "C"], ["Y"]),
        ("NOR3", "NOR(A,B,C)", 1.8, 0.2, ["A", "B", "C"], ["Y"]),
        ("AND3", "AND(A,B,C)", 2.2, 0.25, ["A", "B", "C"], ["Y"]),
        ("OR3", "OR(A,B,C)", 2.2, 0.25, ["A", "B", "C"], ["Y"]),
        ("XOR3", "XOR(A,B,C)", 2.5, 0.3, ["A", "B", "C"], ["Y"]),
        
        # 4-input gates
        ("AND4", "AND(A,B,C,D)", 2.8, 0.3, ["A", "B", "C", "D"], ["Y"]),
        ("OR4", "OR(A,B,C,D)", 2.8, 0.3, ["A", "B", "C", "D"], ["Y"]),
        ("NAND4", "NAND(A,B,C,D)", 2.5, 0.28, ["A", "B", "C", "D"], ["Y"]),
        ("NOR4", "NOR(A,B,C,D)", 2.5, 0.28, ["A", "B", "C", "D"], ["Y"]),
        
        # Complex gates (AOI - And-Or-Invert, OAI - Or-And-Invert)
        ("AOI21", "NOT(OR(AND(A,B),C))", 2.5, 0.3, ["A", "B", "C"], ["Y"]),
        ("OAI21", "NOT(AND(OR(A,B),C))", 2.5, 0.3, ["A", "B", "C"], ["Y"]),
        ("AOI22", "NOT(OR(AND(A,B),AND(C,D)))", 3.0, 0.35, ["A", "B", "C", "D"], ["Y"]),
        ("OAI22", "NOT(AND(OR(A,B),OR(C,D)))", 3.0, 0.35, ["A", "B", "C", "D"], ["Y"]),
        ("AOI211", "NOT(OR(AND(A,B),C,D))", 3.2, 0.38, ["A", "B", "C", "D"], ["Y"]),
        ("OAI211", "NOT(AND(OR(A,B),C,D))", 3.2, 0.38, ["A", "B", "C", "D"], ["Y"]),
    ]
    
    for name, function, area, delay, inputs, outputs in gates:
        cell = LibraryCell(name, function, area, delay, inputs, outputs)
        library.add_cell(cell)
    
    return library


def _merge_libraries(primary: TechnologyLibrary, fallback: TechnologyLibrary) -> TechnologyLibrary:
    """Merge a provided library with fallback combinational cells."""
    merged = TechnologyLibrary(f"{primary.name}+{fallback.name}")

    for cell in primary.cells.values():
        merged.add_cell(cell)
    for cell in fallback.cells.values():
        if cell.name not in merged.cells:
            merged.add_cell(cell)

    return merged


def aig_to_logic_nodes(aig) -> List[LogicNode]:
    """
    Convert AIG to LogicNodes for technology mapping.
    
    Đây là hàm hỗ trợ để convert AIG → LogicNodes.
    Convert từng AIG node thành LogicNode với function string tương ứng.
    
    Args:
        aig: AIG object (từ synthesis hoặc optimize)
        
    Returns:
        List of LogicNode objects
    """
    logic_nodes = []
    node_name_map = {}  # Map AIG node_id -> LogicNode name
    
    # Helper function to get node name string
    def get_node_name(node) -> str:
        """Get string representation for AIG node."""
        if node.is_constant():
            return "CONST0" if not node.get_value() else "CONST1"
        elif node.is_pi():
            return node.var_name or f"pi_{node.node_id}"
        else:
            return f"node_{node.node_id}"
    
    # Helper function to get input name for LogicNode
    def get_input_name(node) -> str:
        """Get input signal name for LogicNode."""
        if node.is_constant():
            return "CONST0" if not node.get_value() else "CONST1"
        elif node.is_pi():
            return node.var_name or f"pi_{node.node_id}"
        else:
            return f"node_{node.node_id}"
    
    # Process nodes in topological order (visit children first)
    visited = set()
    
    def process_node(node) -> str:
        """Process AIG node and return its name."""
        if node.node_id in visited:
            return get_node_name(node)
        
        visited.add(node.node_id)
        
        # Handle constants
        if node.is_constant():
            const_value = node.get_value()
            const_name = "CONST0" if not const_value else "CONST1"
            node_name_map[node.node_id] = const_name
            return const_name
        
        # Handle primary inputs
        if node.is_pi():
            pi_name = node.var_name or f"pi_{node.node_id}"
            node_name_map[node.node_id] = pi_name
            return pi_name
        
        # Handle AND nodes - process children first
        left_name = process_node(node.left) if node.left else None
        right_name = process_node(node.right) if node.right else None
        
        # Determine function based on inversions
        # AIG represents: (left^left_inv) & (right^right_inv)
        # Convert to standard gate functions
        
        node_name = f"node_{node.node_id}"
        left_input = get_input_name(node.left) if node.left else None
        right_input = get_input_name(node.right) if node.right else None
        
        # Build function string based on inversions
        if node.left_inverted and node.right_inverted:
            # !left & !right = NOR(left, right)
            function = f"NOR({left_input},{right_input})" if left_input and right_input else "AND(NOT(A),NOT(B))"
        elif node.left_inverted:
            # !left & right = AND(NOT(left), right)
            function = f"AND(NOT({left_input}),{right_input})" if left_input and right_input else "AND(NOT(A),B)"
        elif node.right_inverted:
            # left & !right = AND(left, NOT(right))
            function = f"AND({left_input},NOT({right_input}))" if left_input and right_input else "AND(A,NOT(B))"
        else:
            # left & right = AND(left, right)
            function = f"AND({left_input},{right_input})" if left_input and right_input else "AND(A,B)"
        
        # Create LogicNode
        inputs_list = []
        if left_input:
            inputs_list.append(left_input)
        if right_input:
            inputs_list.append(right_input)
        
        logic_node = LogicNode(node_name, function, inputs_list, node_name)
        logic_nodes.append(logic_node)
        node_name_map[node.node_id] = node_name
        
        return node_name
    
    # Process all nodes reachable from outputs
    for po_node, po_inverted in aig.pos:
        output_name = process_node(po_node)
        
        # If output is inverted, create a NOT LogicNode for it
        if po_inverted:
            not_node_name = f"output_not_{po_node.node_id}"
            function = f"NOT({output_name})"
            logic_node = LogicNode(not_node_name, function, [output_name], not_node_name)
            logic_nodes.append(logic_node)
    
    # If no logic nodes were created (e.g., outputs are just primary inputs),
    # create BUF nodes to represent the direct connections
    if len(logic_nodes) == 0 and len(aig.pos) > 0:
        logger.info("No complex logic nodes found. Creating BUF nodes for direct connections.")
        for po_node, po_inverted in aig.pos:
            output_name = get_node_name(po_node)
            buf_node_name = f"buf_{po_node.node_id}"
            
            if po_inverted:
                function = f"NOT({output_name})"
            else:
                function = f"BUF({output_name})"
            
            logic_node = LogicNode(buf_node_name, function, [output_name], buf_node_name)
            logic_nodes.append(logic_node)
    
    return logic_nodes


def techmap(
    aig,
    library: TechnologyLibrary,
    strategy: str = "area_optimal",
    *,
    merge_standard_library: bool = True,
) -> Dict[str, Any]:
    """
    Technology mapping: AIG → Technology-mapped netlist (combinational, function-match).

    Args:
        aig: AIG object (từ synthesis hoặc optimize)
        library: Technology library (đã nạp, ví dụ SkyWater qua ``library_loader``)
        strategy: ``area_optimal``, ``delay_optimal``, ``balanced``
        merge_standard_library: Nếu True (mặc định), gộp thêm ``create_standard_library()``
            để có gate generic khi thư viện ngoài thiếu khớp hàm. Nếu False, chỉ dùng
            đúng ``library`` đã truyền (ví dụ chỉ cell Sky130 — phù hợp báo cáo đề tài).

    Returns:
        Dictionary chứa mapping results và statistics (kèm ``merge_standard_library``).
    """
    logger.info(f"Starting technology mapping: AIG -> Technology-mapped netlist")
    logger.info(f"  Strategy: {strategy}")
    logger.info(f"  Library: {library.name} ({len(library.cells)} cells)")

    if merge_standard_library:
        # Bổ sung gate generic khi thư viện PDK không có đủ biểu thức khớp normalize().
        library = _merge_libraries(library, create_standard_library())
        logger.info(f"  Effective library (merged): {library.name} ({len(library.cells)} cells)")
    else:
        logger.info(f"  Effective library (no merge): {library.name} ({len(library.cells)} cells)")
    
    # Convert AIG → LogicNodes
    logger.info("Converting AIG -> LogicNodes...")
    logic_nodes = aig_to_logic_nodes(aig)
    logger.info(f"  Converted {len(logic_nodes)} LogicNodes from AIG")
    
    # Create TechnologyMapper
    mapper = TechnologyMapper(library)
    
    # Add LogicNodes to mapper
    for logic_node in logic_nodes:
        mapper.add_logic_node(logic_node)
    
    # Perform technology mapping
    results = mapper.perform_technology_mapping(strategy)
    
    # Add additional statistics
    results['input_aig_nodes'] = aig.count_nodes()
    results['input_aig_and_nodes'] = aig.count_and_nodes()
    results['converted_logic_nodes'] = len(logic_nodes)
    results['library_name'] = library.name
    results['merge_standard_library'] = merge_standard_library

    # Store mapper object for later conversion to netlist (for verification)
    # Note: This is a reference to the mapper, which contains logic_network with mapped cells
    results['_mapper'] = mapper  # Internal use only (starts with _)
    results['_aig'] = aig  # Store AIG for output mapping
    
    logger.info(f"Technology mapping completed:")
    logger.info(f"  Mapped nodes: {results['mapped_nodes']}/{results['total_nodes']}")
    logger.info(f"  Success rate: {results['mapping_success_rate']*100:.1f}%")
    
    return results


def convert_mapped_logic_network_to_netlist(
    mapper: TechnologyMapper,
    aig,
    original_netlist: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert mapped LogicNode network back to netlist format for verification.
    
    This function converts the technology-mapped logic network (with mapped cells)
    back to a netlist dictionary format that can be used for Verilog generation
    and ModelSim verification.
    
    Args:
        mapper: TechnologyMapper object after technology mapping (contains mapped logic_network)
        aig: AIG object (to get primary inputs/outputs)
        original_netlist: Original netlist to get structure (inputs, outputs names)
    
    Returns:
        Dictionary with netlist format:
        {
            'inputs': [...],
            'outputs': [...],
            'nodes': [
                {
                    'id': 'node_id',
                    'type': 'NAND2',  # mapped cell name or function
                    'inputs': [...],
                    'output': 'output_signal',
                    ...
                },
                ...
            ]
        }
    """
    logger.debug("Converting mapped logic network to netlist format...")
    
    # Get inputs and outputs from original netlist or AIG
    inputs = original_netlist.get('inputs', [])
    outputs = original_netlist.get('outputs', [])
    
    # If not available in original, try to extract from AIG
    if not inputs and hasattr(aig, 'pis'):
        inputs = [pi.var_name or f"pi_{pi.node_id}" for pi in aig.pis if pi.var_name]
    
    if not outputs and hasattr(aig, 'pos'):
        # Get output names from AIG (may need mapping)
        outputs = [f"out{i}" for i in range(len(aig.pos))]
        # Try to get from original netlist's output_mapping if available
        if 'attrs' in original_netlist and 'output_mapping' in original_netlist['attrs']:
            output_mapping = original_netlist['attrs']['output_mapping']
            outputs = list(output_mapping.keys()) if output_mapping else outputs
    
    mapped_netlist = {
        'inputs': inputs,
        'outputs': outputs,
        'nodes': []
    }
    
    def _signal_name_from_aig_node(node) -> str:
        if node.is_constant():
            return "CONST0" if not node.get_value() else "CONST1"
        if node.is_pi():
            return node.var_name or f"pi_{node.node_id}"
        return f"node_{node.node_id}"
    
    # Convert each LogicNode in mapper.logic_network to netlist node format
    for node_name, logic_node in mapper.logic_network.items():
        node_dict = {
            'id': logic_node.name,
            'output': logic_node.output,
            'inputs': logic_node.inputs,
        }
        
        if logic_node.mapped_cell:
            # If mapped to a library cell, use cell name as type
            node_dict['type'] = logic_node.mapped_cell.name  # e.g., 'NAND2', 'NOR2', 'AND2'
            node_dict['cell_name'] = logic_node.mapped_cell.name
            node_dict['function'] = logic_node.function
            node_dict['input_pins'] = list(logic_node.mapped_cell.input_pins or [])
            node_dict['output_pins'] = list(logic_node.mapped_cell.output_pins or [])
            # Store mapping information
            node_dict['mapped'] = True
            if hasattr(logic_node.mapped_cell, 'area'):
                node_dict['area'] = logic_node.mapped_cell.area
            if hasattr(logic_node.mapped_cell, 'delay'):
                node_dict['delay'] = logic_node.mapped_cell.delay
        else:
            # If not mapped, extract gate type from function
            # e.g., "AND(A,B)" -> "AND"
            function_parts = logic_node.function.split('(')
            gate_type = function_parts[0] if function_parts else logic_node.function
            node_dict['type'] = gate_type
            node_dict['function'] = logic_node.function
            node_dict['mapped'] = False
        
        mapped_netlist['nodes'].append(node_dict)

    # Preserve primary outputs by adding explicit BUF/NOT/CONST drivers from AIG outputs.
    if hasattr(aig, 'pos') and aig.pos:
        for idx, (po_node, po_inverted) in enumerate(aig.pos):
            if idx >= len(outputs):
                break

            output_name = outputs[idx]
            source_signal = _signal_name_from_aig_node(po_node)

            if po_node.is_constant():
                mapped_netlist['nodes'].append({
                    'id': f"po_const_{idx}",
                    'type': "CONST1" if (po_node.get_value() ^ bool(po_inverted)) else "CONST0",
                    'output': output_name,
                    'inputs': [],
                    'mapped': False,
                })
                continue

            if po_inverted:
                mapped_netlist['nodes'].append({
                    'id': f"po_not_{idx}",
                    'type': "NOT",
                    'output': output_name,
                    'inputs': [source_signal],
                    'function': f"NOT({source_signal})",
                    'mapped': False,
                })
            elif source_signal != output_name:
                mapped_netlist['nodes'].append({
                    'id': f"po_buf_{idx}",
                    'type': "BUF",
                    'output': output_name,
                    'inputs': [source_signal],
                    'function': f"BUF({source_signal})",
                    'mapped': False,
                })
    
    logger.debug(f"Converted {len(mapped_netlist['nodes'])} nodes to netlist format")
    
    return mapped_netlist


def load_library_from_file(file_path: str, library_type: Optional[str] = None) -> TechnologyLibrary:
    """
    Load technology library from file.
    
    Wrapper function to load from techlibs/ folder.
    
    Args:
        file_path: Path to library file (.lib, .json, or .v)
        library_type: Optional type hint ("liberty", "json", "verilog")
        
    Returns:
        TechnologyLibrary object
        
    Examples:
        >>> library = load_library_from_file("techlibs/asic/standard_cells.lib")
        >>> library = load_library_from_file("techlibs/custom_library.json")
    """
    try:
        from .library_loader import load_library
        return load_library(file_path, library_type)
    except ImportError:
        logger.warning("library_loader not available, using standard library")
        return create_standard_library()

# Example usage and testing
if __name__ == "__main__":
    # Create technology library
    library = create_standard_library()
    
    # Create technology mapper
    mapper = TechnologyMapper(library)
    
    # Create logic network
    logic_nodes = [
        LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1"),
        LogicNode("n2", "OR(C,D)", ["c", "d"], "temp2"),
        LogicNode("n3", "XOR(temp1,temp2)", ["temp1", "temp2"], "out"),
    ]
    
    for node in logic_nodes:
        mapper.add_logic_node(node)
    
    print("Technology Mapping Demo:")
    print("=" * 50)
    
    # Test different mapping strategies
    print("\n1. Area-Optimal Mapping:")
    results1 = mapper.perform_technology_mapping("area_optimal")
    mapper.print_mapping_report(results1)
    
    # Reset for next test
    for node in mapper.logic_network.values():
        node.mapped_cell = None
        node.mapping_cost = float('inf')
    
    print("\n2. Delay-Optimal Mapping:")
    results2 = mapper.perform_technology_mapping("delay_optimal")
    mapper.print_mapping_report(results2)
    
    # Reset for next test
    for node in mapper.logic_network.values():
        node.mapped_cell = None
        node.mapping_cost = float('inf')
    
    print("\n3. Balanced Mapping:")
    results3 = mapper.perform_technology_mapping("balanced")
    mapper.print_mapping_report(results3)
