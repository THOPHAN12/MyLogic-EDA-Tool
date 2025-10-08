#!/usr/bin/env python3
"""
Test Dead Code Elimination (DCE) Algorithm

Kiểm tra thuật toán DCE có loại bỏ logic không cần thiết đúng cách không.
"""

import sys
import os
import unittest
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.optimization.dce import DCEOptimizer
from frontends.verilog import parse_verilog_file

class TestDCE(unittest.TestCase):
    """Test cases for Dead Code Elimination algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = DCEOptimizer()
        
    def test_simple_dead_code(self):
        """Test removal of simple dead code."""
        # Create test netlist with dead code
        netlist = {
            'name': 'test_dead_code',
            'inputs': ['a', 'b'],
            'outputs': ['out'],
            'nodes': {
                # Used logic
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]], 'output': 'temp1'},
                'out': {'type': 'BUF', 'fanins': [['n1', False]], 'output': 'out'},
                
                # Dead code - not connected to outputs
                'n2': {'type': 'OR', 'fanins': [['a', False], ['b', False]], 'output': 'dead1'},
                'n3': {'type': 'XOR', 'fanins': [['n2', False], ['a', False]], 'output': 'dead2'}
            }
        }
        
        # Apply DCE optimization
        optimized = self.optimizer.optimize(netlist, "basic")
        
        # Check that dead code is removed
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Original nodes: {len(netlist['nodes'])}")
        print(f"Optimized nodes: {len(optimized['nodes'])}")
        
        # Check that only used logic remains
        remaining_ids = [node['id'] for node in optimized['nodes']]
        self.assertIn('n1', remaining_ids)  # Used node
        self.assertIn('out', remaining_ids)  # Output
        self.assertNotIn('n2', remaining_ids)  # Dead code
        self.assertNotIn('n3', remaining_ids)  # Dead code
        
    def test_complex_dead_code(self):
        """Test removal of complex dead code chains."""
        # Create test netlist with dead code chain
        netlist = {
            'name': 'test_dead_chain',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out'],
            'nodes': {
                # Used logic
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]], 'output': 'temp1'},
                'out': {'type': 'BUF', 'fanins': [['n1', False]], 'output': 'out'},
                
                # Dead code chain
                'n2': {'type': 'OR', 'fanins': [['a', False], ['c', False]], 'output': 'dead1'},
                'n3': {'type': 'XOR', 'fanins': [['n2', False], ['b', False]], 'output': 'dead2'},
                'n4': {'type': 'AND', 'fanins': [['n3', False], ['c', False]], 'output': 'dead3'},
                'n5': {'type': 'OR', 'fanins': [['n4', False], ['a', False]], 'output': 'dead4'}
            }
        }
        
        # Apply DCE optimization
        optimized = self.optimizer.optimize(netlist, "advanced")
        
        # Check that entire dead chain is removed
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Complex dead code - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
        # Check that dead chain is completely removed
        remaining_ids = [node['id'] for node in optimized['nodes']]
        for dead_id in ['n2', 'n3', 'n4', 'n5']:
            self.assertNotIn(dead_id, remaining_ids)
            
    def test_no_dead_code(self):
        """Test that all nodes are preserved when no dead code exists."""
        # Create test netlist without dead code
        netlist = {
            'name': 'test_no_dead',
            'inputs': ['a', 'b'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]], 'output': 'temp1'},
                'n2': {'type': 'OR', 'fanins': [['a', False], ['b', False]], 'output': 'temp2'},
                'out1': {'type': 'BUF', 'fanins': [['n1', False]], 'output': 'out1'},
                'out2': {'type': 'BUF', 'fanins': [['n2', False]], 'output': 'out2'}
            }
        }
        
        # Apply DCE optimization
        optimized = self.optimizer.optimize(netlist, "basic")
        
        # Check that all nodes are preserved
        self.assertEqual(len(optimized['nodes']), len(netlist['nodes']))
        print("No dead code test - All nodes preserved")

def run_dce_tests():
    """Run all DCE tests."""
    print("=" * 50)
    print("RUNNING DEAD CODE ELIMINATION (DCE) TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDCE)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("DCE TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_dce_tests()
