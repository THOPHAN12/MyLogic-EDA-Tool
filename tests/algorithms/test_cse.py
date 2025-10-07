#!/usr/bin/env python3
"""
Test Common Subexpression Elimination (CSE) Algorithm

Kiểm tra thuật toán CSE có loại bỏ các biểu thức con trùng lặp đúng cách không.
"""

import sys
import os
import unittest
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.optimization.cse import CSEOptimizer
from frontends.verilog import parse_verilog_file

class TestCSE(unittest.TestCase):
    """Test cases for Common Subexpression Elimination algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = CSEOptimizer()
        
    def test_simple_cse(self):
        """Test elimination of simple common subexpressions."""
        # Create test netlist with common subexpressions
        netlist = {
            'name': 'test_cse',
            'inputs': ['a', 'b'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                # Common subexpression: a & b
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                
                'out1': {'type': 'BUF', 'fanins': [['n1', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n2', False]]}
            }
        }
        
        # Apply CSE optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check that common subexpressions are eliminated
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Original nodes: {len(netlist['nodes'])}")
        print(f"Optimized nodes: {len(optimized['nodes'])}")
        
        # Check that only one instance of common subexpression remains
        and_nodes = [node for node in optimized['nodes'].values() if node['type'] == 'AND']
        self.assertEqual(len(and_nodes), 1)
        
    def test_complex_cse(self):
        """Test elimination of complex common subexpressions."""
        # Create test netlist with complex common subexpressions
        netlist = {
            'name': 'test_complex_cse',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2', 'out3'],
            'nodes': {
                # Common subexpression: (a & b) | c
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'OR', 'fanins': [['n1', False], ['c', False]]},
                
                # Duplicate: (a & b) | c
                'n3': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                'n4': {'type': 'OR', 'fanins': [['n3', False], ['c', False]]},  # Duplicate
                
                # Another duplicate: (a & b) | c
                'n5': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                'n6': {'type': 'OR', 'fanins': [['n5', False], ['c', False]]},  # Duplicate
                
                'out1': {'type': 'BUF', 'fanins': [['n2', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n4', False]]},
                'out3': {'type': 'BUF', 'fanins': [['n6', False]]}
            }
        }
        
        # Apply CSE optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check that common subexpressions are eliminated
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Complex CSE - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
        # Check that only one instance of each common subexpression remains
        and_nodes = [node for node in optimized['nodes'].values() if node['type'] == 'AND']
        or_nodes = [node for node in optimized['nodes'].values() if node['type'] == 'OR']
        self.assertEqual(len(and_nodes), 1)  # Only one (a & b)
        self.assertEqual(len(or_nodes), 1)   # Only one (a & b) | c
        
    def test_no_common_subexpressions(self):
        """Test that all nodes are preserved when no common subexpressions exist."""
        # Create test netlist without common subexpressions
        netlist = {
            'name': 'test_no_cse',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'OR', 'fanins': [['a', False], ['c', False]]},
                'out1': {'type': 'BUF', 'fanins': [['n1', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n2', False]]}
            }
        }
        
        # Apply CSE optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check that all nodes are preserved
        self.assertEqual(len(optimized['nodes']), len(netlist['nodes']))
        print("No common subexpressions test - All nodes preserved")

def run_cse_tests():
    """Run all CSE tests."""
    print("=" * 50)
    print("RUNNING COMMON SUBEXPRESSION ELIMINATION (CSE) TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCSE)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("CSE TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_cse_tests()
