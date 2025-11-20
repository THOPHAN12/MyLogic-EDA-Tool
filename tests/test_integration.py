"""
Integration tests for complete workflows.
"""

import pytest
import os
from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis


class TestIntegration:
    """Integration test suite."""
    
    def test_full_workflow_full_adder(self):
        """Test complete workflow with full_adder.v."""
        example_path = os.path.join('examples', 'full_adder.v')
        if not os.path.exists(example_path):
            pytest.skip(f"Example file not found: {example_path}")
        
        # Parse
        netlist = parse_verilog(example_path)
        assert isinstance(netlist, dict)
        
        # Synthesize
        synthesized = run_complete_synthesis(netlist, 'basic')
        assert isinstance(synthesized, dict)
        assert len(synthesized['nodes']) <= len(netlist['nodes'])
    
    def test_full_workflow_arithmetic(self):
        """Test complete workflow with arithmetic_operations.v."""
        example_path = os.path.join('examples', 'arithmetic_operations.v')
        if not os.path.exists(example_path):
            pytest.skip(f"Example file not found: {example_path}")
        
        # Parse
        netlist = parse_verilog(example_path)
        assert isinstance(netlist, dict)
        
        # Synthesize
        synthesized = run_complete_synthesis(netlist, 'standard')
        assert isinstance(synthesized, dict)
        assert 'nodes' in synthesized
    
    def test_synthesis_levels_consistency(self):
        """Test that different synthesis levels produce valid results."""
        example_path = os.path.join('examples', 'full_adder.v')
        if not os.path.exists(example_path):
            pytest.skip(f"Example file not found: {example_path}")
        
        netlist = parse_verilog(example_path)
        
        for level in ['basic', 'standard', 'aggressive']:
            result = run_complete_synthesis(netlist, level)
            assert isinstance(result, dict)
            assert 'nodes' in result
            assert 'wires' in result
            assert 'outputs' in result

