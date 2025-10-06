#!/usr/bin/env python3
"""
Test cases for arithmetic simulation engine.
"""

import sys
import os
import unittest

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.simulation.arithmetic_simulation import VectorValue, vector_add, vector_multiply

class TestArithmeticSimulation(unittest.TestCase):
    """Test cases for arithmetic simulation."""
    
    def test_vector_value_creation(self):
        """Test VectorValue creation and basic operations."""
        v1 = VectorValue(5, 4)  # 5 in 4-bit = 0101
        self.assertEqual(v1.to_int(), 5)
        self.assertEqual(v1.to_binary(), "0101")
        self.assertEqual(v1.width, 4)
    
    def test_vector_addition(self):
        """Test vector addition."""
        a = VectorValue(3, 4)  # 3 in 4-bit
        b = VectorValue(5, 4)  # 5 in 4-bit
        result = vector_add(a, b)
        self.assertEqual(result.to_int(), 8)
        self.assertEqual(result.width, 5)  # +1 for carry
    
    def test_vector_multiplication(self):
        """Test vector multiplication."""
        a = VectorValue(3, 4)  # 3 in 4-bit
        b = VectorValue(2, 4)  # 2 in 4-bit
        result = vector_multiply(a, b)
        self.assertEqual(result.to_int(), 6)
        self.assertEqual(result.width, 8)  # 4 + 4 bits

if __name__ == '__main__':
    unittest.main()
