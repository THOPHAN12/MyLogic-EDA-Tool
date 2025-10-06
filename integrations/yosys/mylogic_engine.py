"""
MyLogic Synthesis Engine

Triển khai synthesis flow của Yosys cho mạch logic tổ hợp.
Dựa trên các lệnh synthesis của Yosys cho tối ưu hóa logic tổ hợp.
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, List, Optional, Tuple

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class MyLogicSynthesisEngine:
    """MyLogic Synthesis Engine cho mạch logic tổ hợp."""
    
    def __init__(self):
        self.yosys_path = "yosys"
        self.abc_path = "abc"
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        """Check if Yosys and ABC are available."""
        try:
            # Check Yosys
            result = subprocess.run([self.yosys_path, "-V"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                return False
            
            # Check ABC
            result = subprocess.run([self.abc_path, "-h"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def get_supported_commands(self) -> List[str]:
        """Get list of supported Yosys synthesis commands."""
        return [
            "read_verilog",      # Read Verilog files
            "hierarchy",         # Hierarchy processing
            "proc",             # Process combinational logic
            "opt",              # Optimization
            "memory",           # Memory processing
            "techmap",          # Technology mapping
            "abc",              # ABC optimization
            "clean",            # Clean up
            "write_verilog",    # Write output
            "write_json",       # Write JSON
            "write_blif",       # Write BLIF
            "stat",             # Statistics
            "show",             # Show design
        ]
    
    def run_combinational_synthesis(self, 
                                  verilog_file: str,
                                  output_file: Optional[str] = None,
                                  optimization_level: str = "balanced") -> Dict[str, any]:
        """
        Run complete combinational synthesis flow.
        
        Args:
            verilog_file: Input Verilog file
            output_file: Output file (optional)
            optimization_level: "fast", "balanced", or "thorough"
            
        Returns:
            Dictionary with synthesis results and statistics
        """
        if not self.available:
            raise RuntimeError("Yosys or ABC not available")
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(mode='w', suffix='.v', delete=False) as tmp_v:
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_json:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.blif', delete=False) as tmp_blif:
                    tmp_v_path = tmp_v.name
                    tmp_json_path = tmp_json.name
                    tmp_blif_path = tmp_blif.name
        
        try:
            # Generate Yosys script
            script = self._generate_synthesis_script(
                verilog_file, tmp_v_path, tmp_json_path, tmp_blif_path, optimization_level
            )
            
            # Run Yosys
            result = self._run_yosys_script(script)
            
            # Parse results
            stats = self._parse_synthesis_results(result)
            
            # Copy output if specified
            if output_file:
                import shutil
                shutil.copy2(tmp_v_path, output_file)
                stats['output_file'] = output_file
            
            return stats
            
        finally:
            # Clean up temporary files
            for path in [tmp_v_path, tmp_json_path, tmp_blif_path]:
                try:
                    os.unlink(path)
                except:
                    pass
    
    def _generate_synthesis_script(self, 
                                  input_file: str,
                                  output_verilog: str,
                                  output_json: str,
                                  output_blif: str,
                                  optimization_level: str) -> str:
        """Generate Yosys synthesis script for combinational logic."""
        
        # Optimization settings based on level
        opt_settings = {
            "fast": {
                "opt_passes": ["opt_expr", "opt_clean"],
                "abc_script": "strash; ifraig; refactor; rewrite; balance;"
            },
            "balanced": {
                "opt_passes": ["opt_expr", "opt_clean", "opt_muxtree", "opt_reduce"],
                "abc_script": "strash; ifraig; refactor; rewrite; balance; map;"
            },
            "thorough": {
                "opt_passes": ["opt_expr", "opt_clean", "opt_muxtree", "opt_reduce", "opt_merge"],
                "abc_script": "strash; ifraig; refactor; rewrite; balance; map;"
            }
        }
        
        settings = opt_settings.get(optimization_level, opt_settings["balanced"])
        
        script = f"""
# Yosys Combinational Synthesis Script
# Generated for combinational logic optimization

# Read input Verilog
read_verilog {input_file}

# Hierarchy processing
hierarchy -check -top

# Process combinational logic
proc

# Initial optimization
opt_expr
opt_clean
opt_muxtree
opt_reduce

# Memory processing (for combinational logic)
memory

# Additional optimization
opt

# Technology mapping
techmap

# ABC optimization for combinational logic
abc -script +{settings['abc_script']}

# Final cleanup
clean

# Statistics
stat

# Write outputs
write_verilog {output_verilog}
write_json {output_json}
write_blif {output_blif}

# Show final design
show
"""
        return script
    
    def _run_yosys_script(self, script: str) -> str:
        """Run Yosys with the given script."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ys', delete=False) as script_file:
            script_file.write(script)
            script_file.flush()
            
            try:
                result = subprocess.run(
                    [self.yosys_path, "-s", script_file.name],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                if result.returncode != 0:
                    raise RuntimeError(f"Yosys failed: {result.stderr}")
                
                return result.stdout
                
            finally:
                os.unlink(script_file.name)
    
    def _parse_synthesis_results(self, output: str) -> Dict[str, any]:
        """Parse Yosys synthesis results."""
        stats = {
            'success': True,
            'output': output,
            'modules': 0,
            'cells': 0,
            'wires': 0,
            'processes': 0,
            'memory': 0,
            'optimization_level': 'balanced'
        }
        
        # Parse statistics from output
        lines = output.split('\n')
        for line in lines:
            if 'Number of modules:' in line:
                stats['modules'] = int(line.split(':')[1].strip())
            elif 'Number of cells:' in line:
                stats['cells'] = int(line.split(':')[1].strip())
            elif 'Number of wires:' in line:
                stats['wires'] = int(line.split(':')[1].strip())
            elif 'Number of processes:' in line:
                stats['processes'] = int(line.split(':')[1].strip())
            elif 'Number of memories:' in line:
                stats['memory'] = int(line.split(':')[1].strip())
        
        return stats
    
    def get_optimization_passes(self) -> List[str]:
        """Get list of available optimization passes."""
        return [
            "opt_expr",      # Expression optimization
            "opt_clean",     # Clean up
            "opt_muxtree",   # Multiplexer tree optimization
            "opt_reduce",    # Reduction optimization
            "opt_merge",     # Merge optimization
            "wreduce",       # Wire reduction
            "peepopt",       # Peephole optimization
            "opt_dff",       # DFF optimization
            "opt_mem",       # Memory optimization
        ]
    
    def run_optimization_pass(self, 
                            verilog_file: str,
                            pass_name: str,
                            output_file: Optional[str] = None) -> Dict[str, any]:
        """Run a specific optimization pass."""
        if not self.available:
            raise RuntimeError("Yosys not available")
        
        script = f"""
read_verilog {verilog_file}
hierarchy -check -top
proc
{pass_name}
clean
stat
"""
        
        if output_file:
            script += f"write_verilog {output_file}\n"
        
        result = self._run_yosys_script(script)
        return self._parse_synthesis_results(result)


def demo_yosys_combinational():
    """Demonstrate Yosys combinational synthesis."""
    print("=" * 60)
    print("Yosys Combinational Logic Synthesis Demo")
    print("=" * 60)
    
    synthesizer = YosysCombinationalSynthesizer()
    
    if not synthesizer.available:
        print("[ERROR] Yosys or ABC not available")
        print("Please install Yosys and ABC to use synthesis features")
        return
    
    print("[OK] Yosys and ABC available")
    print(f"Supported commands: {', '.join(synthesizer.get_supported_commands())}")
    print(f"Optimization passes: {', '.join(synthesizer.get_optimization_passes())}")
    
    # Test with example file
    test_file = "examples/arithmetic_operations.v"
    if os.path.exists(test_file):
        print(f"\nTesting synthesis with {test_file}")
        try:
            result = synthesizer.run_combinational_synthesis(
                test_file, 
                optimization_level="balanced"
            )
            print(f"Synthesis completed successfully")
            print(f"Modules: {result['modules']}")
            print(f"Cells: {result['cells']}")
            print(f"Wires: {result['wires']}")
        except Exception as e:
            print(f"Synthesis failed: {e}")
    else:
        print(f"Test file {test_file} not found")


if __name__ == "__main__":
    demo_yosys_combinational()
