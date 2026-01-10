"""
Tests for Logic Balancing algorithm.
"""

import pytest
from core.optimization.balance import BalanceOptimizer, apply_balance


class TestBalance:
    """Test suite for Logic Balancing."""
    
    def test_basic_balance(self, unbalanced_netlist):
        """Test basic logic balancing."""
        optimizer = BalanceOptimizer()
        optimized = optimizer.optimize(unbalanced_netlist)
        
        assert isinstance(optimized, dict)
        assert 'nodes' in optimized
    
    def test_balance_already_balanced(self, sample_netlist):
        """Test balance with already balanced circuit."""
        original_nodes = len(sample_netlist['nodes'])
        
        optimizer = BalanceOptimizer()
        optimized = optimizer.optimize(sample_netlist)
        
        # May add nodes for balancing, but should preserve functionality
        assert 'nodes' in optimized
    
    def test_apply_balance_function(self, unbalanced_netlist):
        """Test convenience function apply_balance."""
        result = apply_balance(unbalanced_netlist)
        
        assert isinstance(result, dict)
        assert 'nodes' in result
    
    def test_balance_preserves_outputs(self, unbalanced_netlist):
        """Test that balance preserves all outputs."""
        optimizer = BalanceOptimizer()
        optimized = optimizer.optimize(unbalanced_netlist)
        
        assert 'outputs' in optimized
        assert 'out' in optimized['outputs']
    
    def test_balance_empty_netlist(self):
        """Test balance with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        optimizer = BalanceOptimizer()
        result = optimizer.optimize(empty_netlist)
        
        assert len(result['nodes']) == 0

