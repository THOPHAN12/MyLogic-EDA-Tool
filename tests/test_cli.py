"""
Tests for MyLogic CLI (Command Line Interface).

This module contains tests for:
- CLI smoke tests (--help, --version, --check-deps)
- read() command functionality
- simulate() command functionality
- write_json() command functionality
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, Any

import pytest

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from cli.vector_shell import VectorShell
from parsers import parse_verilog
from core.simulation.arithmetic_simulation import simulate_arithmetic_netlist, VectorValue


class TestCLISmoke:
    """Smoke tests for CLI entry point."""

    def test_cli_help(self, capsys):
        """Test CLI --help command."""
        from mylogic import main
        import sys
        
        # Save original argv
        original_argv = sys.argv.copy()
        try:
            sys.argv = ["mylogic.py", "--help"]
            try:
                main()
            except SystemExit:
                pass  # argparse calls sys.exit(0) after --help
            output = capsys.readouterr().out
            assert "MyLogic" in output or "EDA" in output or "usage" in output.lower()
        finally:
            sys.argv = original_argv

    def test_cli_version(self, capsys):
        """Test CLI --version command."""
        from mylogic import main
        import sys
        
        original_argv = sys.argv.copy()
        try:
            sys.argv = ["mylogic.py", "--version"]
            try:
                main()
            except SystemExit:
                pass  # argparse calls sys.exit(0) after --version
            output = capsys.readouterr().out
            assert "2.0.0" in output or "version" in output.lower()
        finally:
            sys.argv = original_argv

    def test_cli_check_deps(self, capsys):
        """Test CLI --check-deps command."""
        from mylogic import check_dependencies
        
        check_dependencies()
        output = capsys.readouterr().out
        assert "Checking dependencies" in output or "NumPy" in output


class TestReadCommand:
    """Tests for read() command."""

    def test_read_file_valid_verilog(self):
        """Test reading a valid Verilog file."""
        shell = VectorShell()
        
        # Use existing example file
        example_file = project_root / "examples" / "full_adder.v"
        if not example_file.exists():
            pytest.skip(f"Example file not found: {example_file}")
        
        # Test read command
        shell._read_file(["read", str(example_file)])
        
        assert shell.netlist is not None
        assert isinstance(shell.netlist, dict)
        assert "nodes" in shell.netlist
        assert shell.filename == str(example_file)

    def test_read_file_invalid_path(self, capsys):
        """Test reading a non-existent file."""
        shell = VectorShell()
        
        shell._read_file(["read", "nonexistent_file.v"])
        
        output = capsys.readouterr().out
        assert "ERROR" in output or "Failed" in output
        assert shell.netlist is None

    def test_read_file_no_argument(self, capsys):
        """Test read command without file argument."""
        shell = VectorShell()
        
        shell._read_file(["read"])
        
        output = capsys.readouterr().out
        assert "ERROR" in output or "Usage" in output

    def test_read_file_empty_netlist(self):
        """Test reading file that produces empty netlist."""
        shell = VectorShell()
        
        # Create a minimal valid Verilog file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as f:
            f.write("""
module empty_module();
endmodule
""")
            temp_file = f.name
        
        try:
            shell._read_file(["read", temp_file])
            assert shell.netlist is not None
            assert shell.netlist.get("name") == "empty_module"
        finally:
            os.unlink(temp_file)


class TestSimulateCommand:
    """Tests for simulate() command."""

    @pytest.fixture
    def simple_netlist(self):
        """Create a simple netlist for testing."""
        return {
            "name": "test_module",
            "inputs": ["a", "b"],
            "outputs": ["sum"],
            "nodes": [
                {
                    "id": "add_0",
                    "type": "ADD",
                    "inputs": ["a", "b"],
                    "output": "sum"
                }
            ],
            "wires": [],
            "attrs": {
                "vector_widths": {"a": 4, "b": 4, "sum": 4}
            }
        }

    def test_simulate_no_netlist(self, capsys):
        """Test simulate command without loaded netlist."""
        shell = VectorShell()
        
        shell._simulate_unified()
        
        output = capsys.readouterr().out
        assert "ERROR" in output or "No netlist" in output

    def test_simulate_with_valid_netlist(self, simple_netlist, monkeypatch):
        """Test simulate command with valid netlist."""
        shell = VectorShell()
        shell.netlist = simple_netlist
        shell.current_netlist = simple_netlist
        
        # Mock input to provide test values
        inputs = iter(["5", "3"])
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        
        # Capture output
        from io import StringIO
        import sys
        old_stdout = sys.stdout
        sys.stdout = captured_output = StringIO()
        
        try:
            shell._simulate_unified()
        finally:
            sys.stdout = old_stdout
        
        output = captured_output.getvalue()
        assert "Outputs" in output or "sum" in output

    def test_simulate_arithmetic_netlist_function(self, simple_netlist):
        """Test simulate_arithmetic_netlist function directly."""
        vec = {
            "a": VectorValue(5, 4),
            "b": VectorValue(3, 4)
        }
        
        result = simulate_arithmetic_netlist(simple_netlist, vec)
        
        assert "sum" in result
        assert isinstance(result["sum"], VectorValue)


class TestWriteJsonCommand:
    """Tests for write_json() command."""

    @pytest.fixture
    def sample_netlist(self):
        """Create a sample netlist for testing."""
        return {
            "name": "test_module",
            "inputs": ["a", "b"],
            "outputs": ["sum"],
            "nodes": [
                {
                    "id": "add_0",
                    "type": "ADD",
                    "inputs": ["a", "b"],
                    "output": "sum"
                }
            ],
            "wires": [],
            "attrs": {}
        }

    def test_write_json_no_netlist(self, capsys):
        """Test write_json command without loaded netlist."""
        shell = VectorShell()
        
        shell._export_json(["export_json"])
        
        output = capsys.readouterr().out
        assert "No netlist" in output

    def test_write_json_default_filename(self, sample_netlist, tmp_path):
        """Test write_json with default filename."""
        shell = VectorShell()
        shell.current_netlist = sample_netlist
        shell.filename = "test.v"
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            shell._export_json(["export_json"])
            
            # Check if file was created
            json_file = tmp_path / "test_netlist.json"
            assert json_file.exists()
            
            # Validate JSON content
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "metadata" in data
            assert "netlist" in data
            assert data["netlist"]["name"] == "test_module"
        finally:
            os.chdir(original_cwd)

    def test_write_json_custom_filename(self, sample_netlist, tmp_path):
        """Test write_json with custom filename."""
        shell = VectorShell()
        shell.current_netlist = sample_netlist
        
        # Change to temp directory
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            custom_filename = "custom_output.json"
            shell._export_json(["export_json", custom_filename])
            
            # Check if file was created
            json_file = tmp_path / custom_filename
            assert json_file.exists()
            
            # Validate JSON content
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "metadata" in data
            assert "netlist" in data
            assert data["netlist"]["name"] == "test_module"
            assert data["metadata"]["tool"] == "MyLogic EDA Tool v2.0.0"
        finally:
            os.chdir(original_cwd)

    def test_write_json_file_content(self, sample_netlist, tmp_path):
        """Test that write_json creates valid JSON with correct structure."""
        shell = VectorShell()
        shell.current_netlist = sample_netlist
        shell.filename = "test.v"
        
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        
        try:
            shell._export_json(["export_json"])
            
            json_file = tmp_path / "test_netlist.json"
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validate structure
            assert "metadata" in data
            assert "netlist" in data
            
            metadata = data["metadata"]
            assert "tool" in metadata
            assert "export_time" in metadata
            assert "source_file" in metadata
            assert "version" in metadata
            
            netlist = data["netlist"]
            assert netlist["name"] == "test_module"
            assert "nodes" in netlist
            assert "inputs" in netlist
            assert "outputs" in netlist
        finally:
            os.chdir(original_cwd)


class TestReadSimulateWriteFlow:
    """Integration tests for read → simulate → write_json flow."""

    def test_complete_flow(self, tmp_path):
        """Test complete flow: read → simulate → write_json."""
        # Create a simple Verilog file
        verilog_file = tmp_path / "test_design.v"
        verilog_file.write_text("""
module test_design(a, b, sum);
    input [3:0] a, b;
    output [4:0] sum;
    assign sum = a + b;
endmodule
""", encoding='utf-8')
        
        shell = VectorShell()
        
        # Step 1: Read
        shell._read_file(["read", str(verilog_file)])
        assert shell.netlist is not None
        assert shell.filename == str(verilog_file)
        
        # Step 2: Simulate (skip interactive input in automated test)
        # This would normally require user input, so we test the function directly
        netlist = shell.netlist
        vec = {
            "a": VectorValue(5, 4),
            "b": VectorValue(3, 4)
        }
        result = simulate_arithmetic_netlist(netlist, vec)
        assert "sum" in result
        
        # Step 3: Write JSON
        original_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            shell._export_json(["export_json", "output.json"])
            
            output_file = tmp_path / "output.json"
            assert output_file.exists()
            
            with open(output_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            assert "netlist" in data
            assert data["netlist"]["name"] == "test_design"
        finally:
            os.chdir(original_cwd)

