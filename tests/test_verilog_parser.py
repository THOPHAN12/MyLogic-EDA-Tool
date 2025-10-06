#!/usr/bin/env python3
"""
Test cases for Verilog parser.
"""

import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontends.simple_arithmetic_verilog import parse_arithmetic_verilog_simple

class TestVerilogParser(unittest.TestCase):
    """Test cases for Verilog parser."""
    
    def test_parse_arithmetic_operations(self):
        """Test parsing arithmetic operations file."""
        try:
            netlist = parse_arithmetic_verilog_simple("examples/arithmetic_operations.v")
            self.assertIsNotNone(netlist)
            self.assertIn('nodes', netlist)
            self.assertIn('connections', netlist)
        except FileNotFoundError:
            self.skipTest("Example file not found")
    
    def test_parse_bitwise_operations(self):
        """Test parsing bitwise operations file."""
        try:
            netlist = parse_arithmetic_verilog_simple("examples/bitwise_operations.v")
            self.assertIsNotNone(netlist)
            self.assertIn('nodes', netlist)
        except FileNotFoundError:
            self.skipTest("Example file not found")

if __name__ == '__main__':
    unittest.main()
