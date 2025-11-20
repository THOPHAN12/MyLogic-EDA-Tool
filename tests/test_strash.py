"""
Tests for Structural Hashing (Strash) algorithm.
"""

import pytest
from core.synthesis.strash import StrashOptimizer, apply_strash


class TestStrash:
    """Test suite for Structural Hashing."""
    
    def test_basic_strash(self, duplicate_netlist):
        """Test basic structural hashing with duplicate nodes."""
        original_nodes = len(duplicate_netlist['nodes'])
        
        optimizer = StrashOptimizer()
        optimized = optimizer.optimize(duplicate_netlist)
        
        assert len(optimized['nodes']) <= original_nodes
        assert 'nodes' in optimized
        assert 'wires' in optimized
    
    def test_strash_no_duplicates(self, sample_netlist):
        """Test strash with no duplicates (should not change)."""
        original_nodes = len(sample_netlist['nodes'])
        
        optimizer = StrashOptimizer()
        optimized = optimizer.optimize(sample_netlist)
        
        # Should not increase nodes
        assert len(optimized['nodes']) <= original_nodes
    
    def test_strash_preserves_outputs(self, duplicate_netlist):
        """Test that strash preserves all outputs."""
        optimizer = StrashOptimizer()
        optimized = optimizer.optimize(duplicate_netlist)
        
        assert 'outputs' in optimized
        assert set(optimized['outputs']) == set(duplicate_netlist['outputs'])
    
    def test_apply_strash_function(self, duplicate_netlist):
        """Test convenience function apply_strash."""
        result = apply_strash(duplicate_netlist)
        
        assert isinstance(result, dict)
        assert 'nodes' in result
        assert 'wires' in result
    
    def test_strash_empty_netlist(self):
        """Test strash with empty netlist."""
        empty_netlist = {
            'name': 'empty',
            'inputs': [],
            'outputs': [],
            'nodes': {},
            'wires': {}
        }
        
        optimizer = StrashOptimizer()
        result = optimizer.optimize(empty_netlist)
        
        assert len(result['nodes']) == 0
    
    def test_strash_complex_duplicates(self):
        """Test strash with complex duplicate structures."""
        netlist = {
            'name': 'complex',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2', 'out3'],
            'nodes': {
                'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 't1', 'name': 'n1'},
                'n2': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 't2', 'name': 'n2'},  # Duplicate
                'n3': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 't3', 'name': 'n3'},  # Duplicate
                'n4': {'type': 'OR', 'inputs': ['t1', 'c'], 'output': 'out1', 'name': 'n4'},
                'n5': {'type': 'OR', 'inputs': ['t2', 'c'], 'output': 'out2', 'name': 'n5'},
                'n6': {'type': 'OR', 'inputs': ['t3', 'c'], 'output': 'out3', 'name': 'n6'}
            },
            'wires': {}
        }
        
        optimizer = StrashOptimizer()
        result = optimizer.optimize(netlist)
        
        # Should reduce from 6 to at most 4 nodes (3 AND duplicates -> 1, 3 ORs)
        assert len(result['nodes']) <= 4

