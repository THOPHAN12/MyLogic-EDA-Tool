#!/usr/bin/env python3
"""
Technology Mapping for VLSI Physical Design

Dựa trên các khái niệm VLSI CAD Part 2 và tham khảo từ ABC (YosysHQ/abc).
Technology mapping và library binding với cut enumeration.

ABC Reference: src/map/mapper.c
- Cut enumeration algorithms
- Area-optimal mapping
- Delay-optimal mapping
- LUT-based mapping
"""

from typing import Dict, List, Set, Any, Tuple, Optional
import logging
import re

logger = logging.getLogger(__name__)

def normalize_function(function: str) -> str:
    """
    Normalize function string by replacing variable names with canonical names.
    
    Examples:
        normalize_function("OR(C,D)") -> "OR(A,B)"
        normalize_function("XOR(temp1,temp2)") -> "XOR(A,B)"
        normalize_function("AND(A,B)") -> "AND(A,B)"
        normalize_function("NOT(X)") -> "NOT(A)"
    
    Args:
        function: Function string like "OR(C,D)", "AND(A,B)", etc.
        
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
    
    # Split arguments by comma
    args = [arg.strip() for arg in args_str.split(',')]
    
    # Generate canonical variable names (A, B, C, D, ...)
    canonical_args = [chr(65 + i) for i in range(len(args))]  # A=65, B=66, C=67, ...
    
    # Reconstruct normalized function
    normalized = f"{func_name}({','.join(canonical_args)})"
    
    return normalized

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
    """Represents a technology library with available cells."""
    
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
    Technology mapping engine.
    
    Based on VLSI CAD Part 2 concepts for technology mapping.
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
