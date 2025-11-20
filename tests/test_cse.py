"""
Tests for Common Subexpression Elimination (CSE) algorithm.
"""

import pytest
from core.optimization.cse import CSEOptimizer, apply_cse


class TestCSE:
    """Test suite for Common Subexpression Elimination."""
    
    def test_basic_cse(self, duplicate_netlist):
        """Test basic common subexpression elimination."""
        original_nodes = len(duplicate_netlist['nodes'])
        
        optimizer = CSEOptimizer()
        optimized = optimizer.optimize(duplicate_netlist)
        
        assert len(optimized['nodes']) <= original_nodes
    
    def test_cse_no_common_subexpressions(self, sample_netlist):
        """Test CSE with no common subexpressions."""
        original_nodes = len(sample_netlist['nodes'])
        
        optimizer = CSEOptimizer()
        optimized = optimizer.optimize(sample_netlist)
        
        # Should not increase nodes
        assert len(optimized['nodes']) <= original_nodes
    
    def test_apply_cse_function(self, duplicate_netlist):
        """Test convenience function apply_cse."""
        result = apply_cse(duplicate_netlist)
        
        assert isinstance(result, dict)
        assert 'nodes' in result
    
    def test_cse_preserves_outputs(self, duplicate_netlist):
        """Test that CSE preserves all outputs."""
        optimizer = CSEOptimizer()
        optimized = optimizer.optimize(duplicate_netlist)
        
        assert 'outputs' in optimized
        assert set(optimized['outputs']) == set(duplicate_netlist['outputs'])
    
    def test_cse_empty_netlist(self):
        """Test CSE with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        optimizer = CSEOptimizer()
        result = optimizer.optimize(empty_netlist)
        
        assert len(result['nodes']) == 0

