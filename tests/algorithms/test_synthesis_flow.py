#!/usr/bin/env python3
"""
Test Complete Synthesis Flow

Kiểm tra quy trình tổng hợp hoàn chỉnh có hoạt động đúng cách không.
"""

import sys
import os
import unittest
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from core.synthesis.synthesis_flow import run_complete_synthesis
from frontends.verilog import parse_verilog_file

class TestSynthesisFlow(unittest.TestCase):
    """Test cases for Complete Synthesis Flow."""
    
    def setUp(self):
        """Set up test fixtures."""
        pass
        
    def test_basic_synthesis(self):
        """Test basic synthesis flow."""
        # Create test netlist with multiple optimization opportunities
        netlist = {
            'name': 'test_basic_synthesis',
            'inputs': ['a', 'b', 'c'],
            'outputs': ['out1', 'out2'],
            'nodes': [
                # Duplicate nodes (for Strash)
                {'id': 'n1', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                {'id': 'n2', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                
                # Common subexpressions (for CSE)
                {'id': 'n3', 'type': 'OR', 'fanins': [['n1', False], ['c', False]]},
                {'id': 'n4', 'type': 'OR', 'fanins': [['n2', False], ['c', False]]},  # Duplicate
                
                # Dead code (for DCE)
                {'id': 'n5', 'type': 'XOR', 'fanins': [['a', False], ['b', False]]},  # Dead
                
                {'id': 'out1', 'type': 'BUF', 'fanins': [['n3', False]]},
                {'id': 'out2', 'type': 'BUF', 'fanins': [['n4', False]]}
            ]
        }
        
        # Run basic synthesis
        optimized = run_complete_synthesis(netlist, "basic")
        
        # Check that optimization occurred
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Basic synthesis - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
    def test_standard_synthesis(self):
        """Test standard synthesis flow."""
        # Create test netlist with complex optimization opportunities
        netlist = {
            'name': 'test_standard_synthesis',
            'inputs': ['a', 'b', 'c', 'd'],
            'outputs': ['out1', 'out2', 'out3'],
            'nodes': [
                # Multiple duplicate structures
                {'id': 'n1', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                {'id': 'n2', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                {'id': 'n3', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                
                # Common subexpressions
                {'id': 'n4', 'type': 'OR', 'fanins': [['n1', False], ['c', False]]},
                {'id': 'n5', 'type': 'OR', 'fanins': [['n2', False], ['c', False]]},  # Duplicate
                {'id': 'n6', 'type': 'OR', 'fanins': [['n3', False], ['c', False]]},  # Duplicate
                
                # Dead code chain
                {'id': 'n7', 'type': 'XOR', 'fanins': [['a', False], ['d', False]]},  # Dead
                {'id': 'n8', 'type': 'AND', 'fanins': [['n7', False], ['b', False]]},  # Dead
                
                {'id': 'out1', 'type': 'BUF', 'fanins': [['n4', False]]},
                {'id': 'out2', 'type': 'BUF', 'fanins': [['n5', False]]},
                {'id': 'out3', 'type': 'BUF', 'fanins': [['n6', False]]}
            ]
        }
        
        # Run standard synthesis
        optimized = run_complete_synthesis(netlist, "standard")
        
        # Check that significant optimization occurred
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Standard synthesis - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
        # Check that dead code is removed
        remaining_ids = [node['id'] for node in optimized['nodes']]
        self.assertNotIn('n7', remaining_ids)  # Dead code
        self.assertNotIn('n8', remaining_ids)  # Dead code
        
    def test_aggressive_synthesis(self):
        """Test aggressive synthesis flow."""
        # Create test netlist with maximum optimization opportunities
        netlist = {
            'name': 'test_aggressive_synthesis',
            'inputs': ['a', 'b', 'c', 'd', 'e'],
            'outputs': ['out1', 'out2'],
            'nodes': [
                # Multiple duplicate structures
                {'id': 'n1', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                {'id': 'n2', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                {'id': 'n3', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                {'id': 'n4', 'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                
                # Complex common subexpressions
                {'id': 'n5', 'type': 'OR', 'fanins': [['n1', False], ['c', False]]},
                {'id': 'n6', 'type': 'OR', 'fanins': [['n2', False], ['c', False]]},  # Duplicate
                {'id': 'n7', 'type': 'OR', 'fanins': [['n3', False], ['c', False]]},  # Duplicate
                {'id': 'n8', 'type': 'OR', 'fanins': [['n4', False], ['c', False]]},  # Duplicate
                
                # Dead code chains
                {'id': 'n9', 'type': 'XOR', 'fanins': [['a', False], ['d', False]]},  # Dead
                {'id': 'n10', 'type': 'AND', 'fanins': [['n9', False], ['e', False]]},  # Dead
                {'id': 'n11', 'type': 'OR', 'fanins': [['n10', False], ['b', False]]},  # Dead
                
                {'id': 'out1', 'type': 'BUF', 'fanins': [['n5', False]]},
                {'id': 'out2', 'type': 'BUF', 'fanins': [['n6', False]]}
            ]
        }
        
        # Run aggressive synthesis
        optimized = run_complete_synthesis(netlist, "aggressive")
        
        # Check that maximum optimization occurred
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        print(f"Aggressive synthesis - Original: {len(netlist['nodes'])}, Optimized: {len(optimized['nodes'])}")
        
        # Check that all dead code is removed
        remaining_ids = [node['id'] for node in optimized['nodes']]
        for dead_id in ['n9', 'n10', 'n11']:
            self.assertNotIn(dead_id, remaining_ids)

def run_synthesis_flow_tests():
    """Run all synthesis flow tests."""
    print("=" * 50)
    print("RUNNING COMPLETE SYNTHESIS FLOW TESTS")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSynthesisFlow)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("SYNTHESIS FLOW TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    run_synthesis_flow_tests()
