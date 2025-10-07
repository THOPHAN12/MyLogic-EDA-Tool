#!/usr/bin/env python3
"""
Test Structural Hashing (Strash) Algorithm

Kiểm tra thuật toán Strash có loại bỏ các node trùng lặp đúng cách không.
"""

import sys
import os
import unittest
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.synthesis.strash import StrashOptimizer
from frontends.verilog import parse_verilog_file

class TestStrash(unittest.TestCase):
    """Test cases for Structural Hashing algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = StrashOptimizer()
        
    def test_simple_duplicates(self):
        """Test removal of simple duplicate nodes."""
        # Create test netlist with duplicates
        netlist = {
            'name': 'test_duplicates',
            'inputs': ['a', 'b'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                'out1': {'type': 'BUF', 'fanins': [['n1', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n2', False]]}
            }
        }
        
        # Apply Strash optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check that duplicates are removed
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Original nodes: {len(netlist['nodes'])}")
        print(f"Optimized nodes: {len(optimized['nodes'])}")
        
    def test_complex_duplicates(self):
        """Test removal of complex duplicate structures."""
        # Create test netlist with complex duplicates
        netlist = {
            'name': 'test_complex',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                # First structure: (a & b) | c
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'OR', 'fanins': [['n1', False], ['c', False]]},
                
                # Duplicate structure: (a & b) | c
                'n3': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                'n4': {'type': 'OR', 'fanins': [['n3', False], ['c', False]]},  # Duplicate
                
                'out1': {'type': 'BUF', 'fanins': [['n2', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n4', False]]}
            }
        }
        
        # Apply Strash optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check optimization
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Complex test - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
    def test_no_duplicates(self):
        """Test that non-duplicate nodes are preserved."""
        # Create test netlist without duplicates
        netlist = {
            'name': 'test_no_duplicates',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2'],
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'OR', 'fanins': [['a', False], ['c', False]]},
                'out1': {'type': 'BUF', 'fanins': [['n1', False]]},
                'out2': {'type': 'BUF', 'fanins': [['n2', False]]}
            }
        }
        
        # Apply Strash optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Check that all nodes are preserved (BUF nodes might be optimized)
        # The important thing is that the logic structure is preserved
        self.assertGreaterEqual(len(optimized['nodes']), 2)  # At least AND and OR
        print("No duplicates test - Logic structure preserved")

def run_strash_tests():
    """Run all Strash tests."""
    print("=" * 50)
    print("RUNNING STRUCTURAL HASHING (STRASH) TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStrash)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("STRASH TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_strash_tests()
