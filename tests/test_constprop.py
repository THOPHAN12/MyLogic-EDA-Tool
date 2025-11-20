"""
Tests for Constant Propagation algorithm.
"""

import pytest
from core.optimization.constprop import ConstPropOptimizer, apply_constprop


class TestConstProp:
    """Test suite for Constant Propagation."""
    
    def test_basic_constprop(self, constant_netlist):
        """Test basic constant propagation."""
        optimizer = ConstPropOptimizer()
        optimized = optimizer.optimize(constant_netlist)
        
        assert isinstance(optimized, dict)
        assert 'nodes' in optimized
    
    def test_constprop_no_constants(self, sample_netlist):
        """Test constprop with no constants."""
        original_nodes = len(sample_netlist['nodes'])
        
        optimizer = ConstPropOptimizer()
        optimized = optimizer.optimize(sample_netlist)
        
        # Should not increase nodes
        assert len(optimized['nodes']) <= original_nodes
    
    def test_apply_constprop_function(self, constant_netlist):
        """Test convenience function apply_constprop."""
        result = apply_constprop(constant_netlist)
        
        assert isinstance(result, dict)
        assert 'nodes' in result
    
    def test_constprop_preserves_outputs(self, constant_netlist):
        """Test that constprop preserves all outputs."""
        optimizer = ConstPropOptimizer()
        optimized = optimizer.optimize(constant_netlist)
        
        assert 'outputs' in optimized
        assert 'out' in optimized['outputs']
    
    def test_constprop_empty_netlist(self):
        """Test constprop with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        optimizer = ConstPropOptimizer()
        result = optimizer.optimize(empty_netlist)
        
        assert len(result['nodes']) == 0

