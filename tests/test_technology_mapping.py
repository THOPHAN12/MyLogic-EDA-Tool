#!/usr/bin/env python3
"""
Tests for Technology Mapping.

Kiểm tra xem technology mapping có hoạt động đúng hay không:
- Library loading
- Cell mapping
- Different strategies (area, delay, balanced)
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.technology_mapping.technology_mapping import (
    TechnologyLibrary, LibraryCell, TechnologyMapper, LogicNode,
    create_standard_library, normalize_function
)

CHECK = "[OK]"
CROSS = "[X]"


class TestTechnologyMapping:
    """Test suite for Technology Mapping."""
    
    def test_library_creation(self):
        """Test technology library creation."""
        library = TechnologyLibrary("test_library")
        assert library is not None
        assert library.name == "test_library"
        assert len(library.cells) == 0
        
    def test_cell_creation(self):
        """Test library cell creation."""
        cell = LibraryCell("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"])
        assert cell.name == "AND2"
        assert cell.function == "AND(A,B)"
        assert cell.area == 1.5
        assert cell.delay == 0.2
        
    def test_library_add_cell(self):
        """Test adding cells to library."""
        library = TechnologyLibrary("test_library")
        cell = LibraryCell("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"])
        library.add_cell(cell)
        
        assert len(library.cells) == 1
        assert "AND2" in library.cells
        assert cell in library.cells.values()
        
    def test_normalize_function(self):
        """Test function normalization."""
        # Test basic normalization
        assert normalize_function("AND(A,B)") == "AND(A,B)"
        assert normalize_function("OR(C,D)") == "OR(A,B)"
        assert normalize_function("XOR(temp1,temp2)") == "XOR(A,B)"
        assert normalize_function("NOT(X)") == "NOT(A)"
        
        # Test 3-input
        assert normalize_function("AND(A,B,C)") == "AND(A,B,C)"
        assert normalize_function("OR(X,Y,Z)") == "OR(A,B,C)"
        
    def test_library_function_mapping(self):
        """Test function mapping in library."""
        library = TechnologyLibrary("test_library")
        
        # Add cells with same function but different implementations
        cell1 = LibraryCell("AND2_FAST", "AND(A,B)", 2.0, 0.1, ["A", "B"], ["Y"])
        cell2 = LibraryCell("AND2_SMALL", "AND(A,B)", 1.0, 0.3, ["A", "B"], ["Y"])
        
        library.add_cell(cell1)
        library.add_cell(cell2)
        
        # Test function lookup
        cells = library.get_cells_for_function("AND(C,D)")  # Should normalize to AND(A,B)
        assert len(cells) == 2
        assert cell1 in cells or cell2 in cells
        
    def test_get_best_cell_area(self):
        """Test getting best cell for area optimization."""
        library = TechnologyLibrary("test_library")
        
        cell1 = LibraryCell("AND2_FAST", "AND(A,B)", 2.0, 0.1, ["A", "B"], ["Y"])
        cell2 = LibraryCell("AND2_SMALL", "AND(A,B)", 1.0, 0.3, ["A", "B"], ["Y"])
        
        library.add_cell(cell1)
        library.add_cell(cell2)
        
        best_cell = library.get_best_cell_for_function("AND(X,Y)", "area")
        assert best_cell is not None
        assert best_cell.name == "AND2_SMALL"  # Smaller area
        
    def test_get_best_cell_delay(self):
        """Test getting best cell for delay optimization."""
        library = TechnologyLibrary("test_library")
        
        cell1 = LibraryCell("AND2_FAST", "AND(A,B)", 2.0, 0.1, ["A", "B"], ["Y"])
        cell2 = LibraryCell("AND2_SMALL", "AND(A,B)", 1.0, 0.3, ["A", "B"], ["Y"])
        
        library.add_cell(cell1)
        library.add_cell(cell2)
        
        best_cell = library.get_best_cell_for_function("AND(X,Y)", "delay")
        assert best_cell is not None
        assert best_cell.name == "AND2_FAST"  # Faster delay
        
    def test_logic_node_creation(self):
        """Test logic node creation."""
        node = LogicNode("n1", "AND(A,B)", ["a", "b"], "out1")
        assert node.name == "n1"
        assert node.function == "AND(A,B)"
        assert node.inputs == ["a", "b"]
        assert node.output == "out1"
        assert node.mapped_cell is None
        
    def test_technology_mapper_creation(self):
        """Test technology mapper creation."""
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        assert mapper is not None
        assert mapper.library == library
        assert len(mapper.logic_network) == 0
        
    def test_area_optimal_mapping(self):
        """Test area-optimal technology mapping."""
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        
        # Create logic network
        node1 = LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1")
        node2 = LogicNode("n2", "OR(A,B)", ["c", "d"], "temp2")
        node3 = LogicNode("n3", "XOR(A,B)", ["temp1", "temp2"], "out")
        
        mapper.add_logic_node(node1)
        mapper.add_logic_node(node2)
        mapper.add_logic_node(node3)
        
        # Perform mapping
        results = mapper.perform_technology_mapping("area_optimal")
        
        assert results is not None
        assert results['strategy'] == 'area_optimal'
        assert results['total_nodes'] == 3
        assert results['mapped_nodes'] >= 0
        assert 'total_area' in results
        assert results['mapping_success_rate'] >= 0
        
        # Verify nodes are mapped
        assert node1.mapped_cell is not None
        assert node2.mapped_cell is not None
        assert node3.mapped_cell is not None
        
    def test_delay_optimal_mapping(self):
        """Test delay-optimal technology mapping."""
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        
        # Create logic network
        node1 = LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1")
        node2 = LogicNode("n2", "OR(A,B)", ["c", "d"], "temp2")
        
        mapper.add_logic_node(node1)
        mapper.add_logic_node(node2)
        
        # Perform mapping
        results = mapper.perform_technology_mapping("delay_optimal")
        
        assert results is not None
        assert results['strategy'] == 'delay_optimal'
        assert results['total_nodes'] == 2
        assert 'total_delay' in results
        
    def test_balanced_mapping(self):
        """Test balanced technology mapping."""
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        
        # Create logic network
        node1 = LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1")
        mapper.add_logic_node(node1)
        
        # Perform mapping
        results = mapper.perform_technology_mapping("balanced")
        
        assert results is not None
        assert results['strategy'] == 'balanced'
        assert 'total_area' in results
        assert 'total_delay' in results
        
    def test_mapping_statistics(self):
        """Test mapping statistics."""
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        
        node1 = LogicNode("n1", "AND(A,B)", ["a", "b"], "temp1")
        mapper.add_logic_node(node1)
        
        # Perform mapping
        mapper.perform_technology_mapping("area_optimal")
        
        # Get statistics
        stats = mapper.get_mapping_statistics()
        
        assert stats is not None
        assert 'total_nodes' in stats
        assert 'mapped_nodes' in stats
        assert 'mapping_success_rate' in stats
        assert 'cell_usage' in stats
        
    def test_standard_library_creation(self):
        """Test standard library creation."""
        library = create_standard_library()
        
        assert library is not None
        assert len(library.cells) > 0
        
        # Check for common gates
        assert "AND2" in library.cells
        assert "OR2" in library.cells
        assert "NOT" in library.cells or "INV" in library.cells
        
    def test_mapping_with_real_examples(self):
        """Test mapping with synthesized netlist."""
        from parsers import parse_verilog
        from core.synthesis.synthesis_flow import run_complete_synthesis
        
        # Parse and synthesize a simple example
        example_path = project_root / "examples" / "full_adder.v"
        if not example_path.exists():
            pytest.skip(f"Example file not found: {example_path}")
        
        # Parse
        netlist = parse_verilog(str(example_path))
        
        # Synthesize
        synthesized = run_complete_synthesis(netlist, "basic")
        
        # Create library and mapper
        library = create_standard_library()
        mapper = TechnologyMapper(library)
        
        # Convert netlist nodes to LogicNodes
        nodes_data = synthesized.get('nodes', [])
        if isinstance(nodes_data, list):
            for node_data in nodes_data:
                node_type = node_data.get('type', '')
                node_id = node_data.get('id', '')
                
                # Skip non-gate nodes
                if node_type not in ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF']:
                    continue
                
                # Get inputs
                fanins = node_data.get('fanins', [])
                inputs = [f[0] for f in fanins] if fanins else []
                
                # Create function string
                if node_type == 'NOT':
                    function = f"NOT(A)"
                elif node_type == 'BUF':
                    function = f"BUF(A)"
                elif len(inputs) == 2:
                    function = f"{node_type}(A,B)"
                elif len(inputs) >= 3:
                    function = f"{node_type}(A,B,C)"
                else:
                    continue
                
                # Create LogicNode
                logic_node = LogicNode(node_id, function, inputs, node_id)
                mapper.add_logic_node(logic_node)
        
        # Perform mapping
        if len(mapper.logic_network) > 0:
            results = mapper.perform_technology_mapping("area_optimal")
            assert results is not None
            assert results['mapped_nodes'] > 0
            print(f"\n{CHECK} Mapped {results['mapped_nodes']} nodes from {example_path.name}")
        else:
            pytest.skip("No mappable nodes found in netlist")


if __name__ == "__main__":
    print("=" * 70)
    print(" TESTING TECHNOLOGY MAPPING")
    print("=" * 70)
    
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
