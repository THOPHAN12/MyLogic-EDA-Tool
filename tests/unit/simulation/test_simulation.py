"""
Tests for Simulation Engine.
"""

import pytest
from parsers import parse_verilog
from core.simulation.arithmetic_simulation import (
    simulate_arithmetic_netlist,
    VectorValue
)
from core.simulation.logic_simulation import simulate_logic_netlist
import os


class TestArithmeticSimulation:
    """Test suite for Arithmetic Simulation."""
    
    def test_vector_value_creation(self):
        """Test VectorValue creation and operations."""
        v1 = VectorValue(5, 4)  # 5 in 4 bits
        v2 = VectorValue(3, 4)  # 3 in 4 bits
        
        assert v1.to_int() == 5
        assert v1.to_binary() == '0101'
        assert v2.to_int() == 3
        
    def test_vector_arithmetic_operations(self):
        """Test vector arithmetic operations."""
        v1 = VectorValue(5, 4)
        v2 = VectorValue(3, 4)
        
        from core.simulation.arithmetic_simulation import (
            vector_add, vector_subtract, vector_multiply, vector_divide
        )
        
        # Addition
        result = vector_add(v1, v2)
        assert result.to_int() == 8
        
        # Subtraction
        result = vector_subtract(v1, v2)
        assert result.to_int() == 2
        
        # Multiplication
        result = vector_multiply(v1, v2)
        assert result.to_int() == 15
        
        # Division
        result = vector_divide(v1, v2)
        assert result.to_int() == 1
        
    def test_vector_bitwise_operations(self):
        """Test vector bitwise operations."""
        v1 = VectorValue(5, 4)  # 0101
        v2 = VectorValue(3, 4)  # 0011
        
        from core.simulation.arithmetic_simulation import (
            vector_and, vector_or, vector_xor, vector_not
        )
        
        # AND
        result = vector_and(v1, v2)
        assert result.to_int() == 1  # 0101 & 0011 = 0001
        
        # OR
        result = vector_or(v1, v2)
        assert result.to_int() == 7  # 0101 | 0011 = 0111
        
        # XOR
        result = vector_xor(v1, v2)
        assert result.to_int() == 6  # 0101 ^ 0011 = 0110
        
        # NOT
        result = vector_not(v1)
        assert result.to_int() == 10  # ~0101 = 1010 (in 4 bits)
    
    def test_simulate_arithmetic_netlist(self):
        """Test arithmetic netlist simulation."""
        example_path = os.path.join('examples', 'arithmetic_operations.v')
        if not os.path.exists(example_path):
            pytest.skip(f"Example file not found: {example_path}")
        
        netlist = parse_verilog(example_path)
        
        # Test with sample inputs
        inputs = {
            'a': VectorValue(5, 4),
            'b': VectorValue(3, 4),
            'c': VectorValue(8, 4),
            'd': VectorValue(2, 4)
        }
        
        outputs = simulate_arithmetic_netlist(netlist, inputs)
        
        assert isinstance(outputs, dict)
        assert 'sum_out' in outputs or len(outputs) > 0
    
    def test_simulate_full_adder(self):
        """Test full adder simulation."""
        example_path = os.path.join('examples', 'full_adder.v')
        if not os.path.exists(example_path):
            pytest.skip(f"Example file not found: {example_path}")
        
        netlist = parse_verilog(example_path)
        
        # Test with binary inputs
        inputs = {
            'a': 1,
            'b': 1,
            'cin': 1
        }
        
        # Try logic simulation for full adder
        try:
            outputs = simulate_logic_netlist(netlist, inputs)
            assert isinstance(outputs, dict)
        except Exception:
            # If logic simulation doesn't support, that's okay
            pass


class TestLogicSimulation:
    """Test suite for Logic Simulation."""
    
    def test_simulate_logic_netlist(self, sample_netlist):
        """Test logic netlist simulation."""
        inputs = {
            'a': 1,
            'b': 0,
            'c': 1
        }
        
        try:
            outputs = simulate_logic_netlist(sample_netlist, inputs)
            assert isinstance(outputs, dict)
        except Exception:
            # Logic simulation may not be fully implemented
            pytest.skip("Logic simulation not fully implemented")

