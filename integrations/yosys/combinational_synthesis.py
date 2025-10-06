#!/usr/bin/env python3
"""
Combinational Synthesis Engine for MyLogic EDA Tool
Based on YosysHQ Documentation for combinational circuits
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, List, Optional, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class CombinationalSynthesis:
    """Combinational synthesis engine based on YosysHQ best practices."""
    
    def __init__(self):
        self.yosys_path = "yosys"
        self.available = self._check_yosys()
        self.output_dir = "outputs"
        self._ensure_output_dir()
    
    def _check_yosys(self) -> bool:
        """Check if Yosys is available."""
        try:
            result = subprocess.run([self.yosys_path, "-V"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def _ensure_output_dir(self):
        """Ensure output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def generate_combinational_script(self, 
                                    verilog_file: str,
                                    optimization_level: str = "balanced") -> str:
        """Generate optimized Yosys script for combinational circuits."""
        
        script_content = f"""# MyLogic Combinational Synthesis
# Based on YosysHQ Documentation
# File: {verilog_file}
# Optimization: {optimization_level}

# Read Verilog file
read_verilog {verilog_file}

# Hierarchy processing
hierarchy -check -top arithmetic_operations

# Process combinational logic
proc

# Combinational-specific optimizations
opt_expr          # Expression optimization
opt_clean         # Clean unused signals
opt_muxtree       # Multiplexer tree optimization
opt_reduce        # Reduction optimization
opt_merge         # Merge optimization
opt_dff           # DFF optimization (minimal for combinational)

# Combinational logic optimization
opt               # General optimization

# Technology mapping
techmap
"""
        
        # Add optimization level specific commands
        if optimization_level == "fast":
            script_content += """
# Fast optimization for combinational
abc -script +fast
"""
        elif optimization_level == "balanced":
            script_content += """
# Balanced optimization for combinational
abc -script +strash
abc -script +dch
"""
        elif optimization_level == "thorough":
            script_content += """
# Thorough optimization for combinational
abc -script +strash
abc -script +dch
abc -script +map
abc -script +area
"""
        
        # Add final steps
        script_content += f"""
# Final cleanup
clean

# Show statistics
stat

# Write outputs
write_verilog {self.output_dir}/combinational_synth.v
write_json {self.output_dir}/combinational_synth.json
write_blif {self.output_dir}/combinational_synth.blif
write_dot {self.output_dir}/combinational_synth.dot
"""
        
        return script_content
    
    def run_combinational_synthesis(self, 
                                   verilog_file: str,
                                   optimization_level: str = "balanced") -> Dict[str, Any]:
        """Run combinational synthesis."""
        
        if not self.available:
            return {
                'success': False,
                'error': 'Yosys not available',
                'message': 'Install Yosys from https://yosyshq.readthedocs.io/'
            }
        
        try:
            # Generate script
            script_content = self.generate_combinational_script(
                verilog_file, optimization_level
            )
            
            # Create temporary script file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ys', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            # Run Yosys
            result = subprocess.run(
                [self.yosys_path, script_path],
                capture_output=True, text=True, timeout=60
            )
            
            # Parse results
            stats = self._parse_combinational_stats(result.stdout)
            
            # Clean up
            os.unlink(script_path)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'stats': stats,
                'output_files': self._get_output_files()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Combinational synthesis failed'
            }
    
    def _parse_combinational_stats(self, stdout: str) -> Dict[str, Any]:
        """Parse combinational synthesis statistics."""
        stats = {
            'cells': 0,
            'wires': 0,
            'public_wires': 0,
            'memories': 0,
            'processes': 0,
            'combinational_gates': 0
        }
        
        lines = stdout.split('\n')
        for line in lines:
            if 'Number of cells:' in line:
                stats['cells'] = self._extract_number(line)
            elif 'Number of wires:' in line:
                stats['wires'] = self._extract_number(line)
            elif 'Number of public wires:' in line:
                stats['public_wires'] = self._extract_number(line)
            elif 'Number of memories:' in line:
                stats['memories'] = self._extract_number(line)
            elif 'Number of processes:' in line:
                stats['processes'] = self._extract_number(line)
        
        # Estimate combinational gates (cells - memories - processes)
        stats['combinational_gates'] = max(0, stats['cells'] - stats['memories'] - stats['processes'])
        
        return stats
    
    def _extract_number(self, line: str) -> int:
        """Extract number from statistics line."""
        try:
            return int(line.split(':')[-1].strip())
        except:
            return 0
    
    def _get_output_files(self) -> List[str]:
        """Get generated output files."""
        output_files = []
        if os.path.exists(self.output_dir):
            for file in os.listdir(self.output_dir):
                if file.startswith('combinational_synth'):
                    output_files.append(os.path.join(self.output_dir, file))
        return output_files
    
    def get_combinational_best_practices(self) -> Dict[str, str]:
        """Get best practices for combinational synthesis."""
        return {
            'optimization_flow': 'proc -> opt_expr -> opt_clean -> opt_muxtree -> opt_reduce -> opt_merge -> opt -> techmap -> abc',
            'abc_scripts': {
                'fast': '+fast (for quick synthesis)',
                'balanced': '+strash +dch (balanced area/delay)',
                'thorough': '+strash +dch +map +area (maximum optimization)'
            },
            'combinational_specific': {
                'opt_dff': 'Minimal impact on combinational circuits',
                'opt_muxtree': 'Important for multiplexer optimization',
                'opt_reduce': 'Critical for reduction operations',
                'opt_merge': 'Essential for gate merging'
            },
            'verification': {
                'stat': 'Check cell count and wire count',
                'show': 'Visualize combinational structure',
                'write_verilog': 'Inspect optimized netlist',
                'write_dot': 'Generate circuit diagram'
            }
        }

def main():
    """Demo combinational synthesis."""
    synthesis = CombinationalSynthesis()
    
    print("=== MyLogic Combinational Synthesis ===")
    print(f"Yosys available: {synthesis.available}")
    
    if synthesis.available:
        print("Running combinational synthesis...")
        result = synthesis.run_combinational_synthesis(
            "examples/arithmetic_operations.v",
            optimization_level="balanced"
        )
        
        print(f"Success: {result['success']}")
        if result['success']:
            print("Combinational synthesis completed!")
            print(f"Statistics: {result['stats']}")
            print(f"Output files: {result['output_files']}")
        else:
            print(f"Error: {result['error']}")
    else:
        print("Yosys not available. Please install Yosys.")
        print("Documentation: https://yosyshq.readthedocs.io/")
    
    # Show best practices
    practices = synthesis.get_combinational_best_practices()
    print("\nBest practices for combinational synthesis:")
    for category, advice in practices.items():
        print(f"{category}: {advice}")

if __name__ == "__main__":
    main()
