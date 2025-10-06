#!/usr/bin/env python3
"""
Yosys Demo for MyLogic EDA Tool
Simple demonstration of Yosys integration
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class YosysDemo:
    """Simple Yosys demonstration."""
    
    def __init__(self):
        self.yosys_path = "yosys"
        self.available = self._check_yosys()
    
    def _check_yosys(self) -> bool:
        """Check if Yosys is available."""
        try:
            result = subprocess.run([self.yosys_path, "-V"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def create_simple_script(self, verilog_file: str) -> str:
        """Create simple Yosys script."""
        return f"""# Simple Yosys script for MyLogic
read_verilog {verilog_file}
hierarchy -check
proc
opt
stat
write_verilog outputs/simple_synth.v
write_json outputs/simple_synth.json
"""
    
    def run_simple_synthesis(self, verilog_file: str) -> Dict[str, Any]:
        """Run simple synthesis."""
        if not self.available:
            return {
                'success': False,
                'error': 'Yosys not available',
                'message': 'Install Yosys from https://github.com/YosysHQ/yosys'
            }
        
        try:
            # Create script
            script_content = self.create_simple_script(verilog_file)
            
            # Write to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.ys', delete=False) as f:
                f.write(script_content)
                script_path = f.name
            
            # Run Yosys
            result = subprocess.run(
                [self.yosys_path, script_path],
                capture_output=True, text=True, timeout=30
            )
            
            # Clean up
            os.unlink(script_path)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Synthesis failed'
            }
    
    def get_yosys_commands(self) -> Dict[str, str]:
        """Get common Yosys commands."""
        return {
            'read_verilog': 'Read Verilog file',
            'hierarchy': 'Process hierarchy',
            'proc': 'Convert behavioral to structural',
            'opt': 'Optimize design',
            'stat': 'Show statistics',
            'write_verilog': 'Write Verilog output',
            'write_json': 'Write JSON netlist',
            'write_blif': 'Write BLIF format',
            'write_dot': 'Write DOT graph',
            'show': 'Show design structure'
        }
    
    def get_best_practices(self) -> Dict[str, str]:
        """Get Yosys best practices."""
        return {
            'optimization': 'Use opt_expr, opt_clean, opt_muxtree for best results',
            'technology_mapping': 'Use techmap for target technology',
            'abc_optimization': 'Use abc for area/delay optimization',
            'verification': 'Use stat to check results',
            'output_formats': 'Use multiple output formats for different tools'
        }

def main():
    """Demo Yosys functionality."""
    demo = YosysDemo()
    
    print("=== MyLogic Yosys Demo ===")
    print(f"Yosys available: {demo.available}")
    
    if demo.available:
        print("Running simple synthesis...")
        result = demo.run_simple_synthesis("examples/arithmetic_operations.v")
        print(f"Success: {result['success']}")
        if result['success']:
            print("Synthesis completed successfully!")
        else:
            print(f"Error: {result['error']}")
    else:
        print("Yosys not available. Please install Yosys.")
        print("Download from: https://github.com/YosysHQ/yosys")
    
    print("\nCommon Yosys commands:")
    commands = demo.get_yosys_commands()
    for cmd, desc in commands.items():
        print(f"  {cmd}: {desc}")
    
    print("\nBest practices:")
    practices = demo.get_best_practices()
    for topic, advice in practices.items():
        print(f"  {topic}: {advice}")

if __name__ == "__main__":
    main()
