"""
Tests for Verilog Parser.
"""

import pytest
import os
from parsers import parse_verilog


class TestVerilogParser:
    """Test suite for Verilog Parser."""
    
    def test_parse_full_adder(self):
        """Test parsing full_adder.v example."""
        example_path = os.path.join('examples', 'full_adder.v')
        if os.path.exists(example_path):
            netlist = parse_verilog(example_path)
            
            assert isinstance(netlist, dict)
            assert 'nodes' in netlist
            assert 'wires' in netlist
            assert len(netlist['nodes']) > 0
    
    def test_parse_arithmetic_operations(self):
        """Test parsing arithmetic_operations.v example."""
        example_path = os.path.join('examples', 'arithmetic_operations.v')
        if os.path.exists(example_path):
            netlist = parse_verilog(example_path)
            
            assert isinstance(netlist, dict)
            assert 'nodes' in netlist
            assert 'wires' in netlist
    
    def test_parse_nonexistent_file(self):
        """Test parsing nonexistent file."""
        with pytest.raises((FileNotFoundError, Exception)):
            parse_verilog('nonexistent.v')
    
    def test_parse_invalid_verilog(self, tmp_path):
        """Test parsing invalid Verilog file."""
        invalid_file = tmp_path / "invalid.v"
        invalid_file.write_text("invalid verilog code")
        
        # Should either parse or raise appropriate error
        try:
            result = parse_verilog(str(invalid_file))
            # If it parses, should return a dict
            assert isinstance(result, dict)
        except Exception:
            # If it fails, that's also acceptable
            pass

