"""
Tests for Dead Code Elimination (DCE) algorithm.
"""

import pytest
from core.optimization.dce import DCEOptimizer, apply_dce


class TestDCE:
    """Test suite for Dead Code Elimination."""
    
    def test_basic_dce(self, dead_code_netlist):
        """Test basic dead code elimination."""
        original_nodes = len(dead_code_netlist['nodes'])
        
        optimizer = DCEOptimizer()
        optimized = optimizer.optimize(dead_code_netlist, level='basic')
        
        assert len(optimized['nodes']) <= original_nodes
        assert 'n4' not in optimized['nodes'] or optimized['nodes'].get('n4', {}).get('output') != 'dead_out'
    
    def test_dce_preserves_reachable_nodes(self, sample_netlist):
        """Test that DCE preserves all reachable nodes."""
        optimizer = DCEOptimizer()
        optimized = optimizer.optimize(sample_netlist, level='basic')
        
        # All nodes in sample_netlist are reachable
        assert len(optimized['nodes']) == len(sample_netlist['nodes'])
    
    def test_dce_advanced_level(self, dead_code_netlist):
        """Test DCE with advanced optimization level."""
        optimizer = DCEOptimizer()
        optimized = optimizer.optimize(dead_code_netlist, level='advanced')
        
        assert len(optimized['nodes']) <= len(dead_code_netlist['nodes'])
    
    def test_dce_aggressive_level(self, dead_code_netlist):
        """Test DCE with aggressive optimization level."""
        optimizer = DCEOptimizer()
        optimized = optimizer.optimize(dead_code_netlist, level='aggressive')
        
        assert len(optimized['nodes']) <= len(dead_code_netlist['nodes'])
    
    def test_apply_dce_function(self, dead_code_netlist):
        """Test convenience function apply_dce."""
        result = apply_dce(dead_code_netlist, level='basic')
        
        assert isinstance(result, dict)
        assert 'nodes' in result
    
    def test_dce_empty_netlist(self):
        """Test DCE with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        optimizer = DCEOptimizer()
        result = optimizer.optimize(empty_netlist)
        
        assert len(result['nodes']) == 0
    
    def test_dce_preserves_outputs(self, dead_code_netlist):
        """Test that DCE preserves all outputs."""
        optimizer = DCEOptimizer()
        optimized = optimizer.optimize(dead_code_netlist)
        
        assert 'outputs' in optimized
        assert 'out' in optimized['outputs']

