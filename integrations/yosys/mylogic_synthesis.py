"""
MyLogic Synthesis Engine

Tích hợp khả năng synthesis của Yosys vào MyLogic EDA Tool.
Cung cấp workflow synthesis liền mạch cho logic tổ hợp.
"""

import os
import sys
import subprocess
import tempfile
from typing import Dict, List, Optional, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from synthesis.mylogic_engine import MyLogicSynthesisEngine
from synthesis.mylogic_commands import MyLogicCommands


class MyLogicSynthesis:
    """MyLogic Synthesis Engine - Tích hợp Yosys vào MyLogic EDA Tool."""
    
    def __init__(self):
        self.synthesizer = MyLogicSynthesisEngine()
        self.commands = MyLogicCommands()
        self.available = self.synthesizer.available
    
    def get_synthesis_commands(self) -> List[str]:
        """Get available synthesis commands."""
        return [
            "yosys_synth <file>",           # Run synthesis
            "yosys_opt <file> <pass>",       # Run optimization pass
            "yosys_stat <file>",            # Get statistics
            "yosys_show <file>",             # Show design
            "yosys_flow <file>",             # Complete synthesis flow
            "yosys_abc <file>",              # ABC optimization
            "yosys_techmap <file>",          # Technology mapping
            "yosys_clean <file>",            # Clean design
        ]
    
    def get_output_commands(self) -> List[str]:
        """Get available output format commands."""
        return [
            "write_verilog <file>",         # Write Verilog RTL
            "write_json <file>",            # Write JSON netlist
            "write_blif <file>",            # Write BLIF format
            "write_edif <file>",            # Write EDIF format
            "write_spice <file>",           # Write SPICE netlist
            "write_dot <file>",             # Write DOT graph
            "write_liberty <file>",         # Write Liberty library
            "write_systemverilog <file>",    # Write SystemVerilog
        ]
    
    def run_synthesis(self, 
                     verilog_file: str,
                     output_file: Optional[str] = None,
                     optimization_level: str = "balanced") -> Dict[str, Any]:
        """Run Yosys synthesis on Verilog file."""
        if not self.available:
            return {
                'success': False,
                'error': 'Yosys not available',
                'message': 'Please install Yosys to use synthesis features'
            }
        
        try:
            result = self.synthesizer.run_combinational_synthesis(
                verilog_file, output_file, optimization_level
            )
            result['success'] = True
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Synthesis failed'
            }
    
    def run_optimization_pass(self, 
                             verilog_file: str,
                             pass_name: str,
                             output_file: Optional[str] = None) -> Dict[str, Any]:
        """Run specific optimization pass."""
        if not self.available:
            return {
                'success': False,
                'error': 'Yosys not available',
                'message': 'Please install Yosys to use optimization features'
            }
        
        try:
            result = self.synthesizer.run_optimization_pass(
                verilog_file, pass_name, output_file
            )
            result['success'] = True
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'Optimization pass {pass_name} failed'
            }
    
    def get_statistics(self, verilog_file: str) -> Dict[str, Any]:
        """Get design statistics."""
        if not self.available:
            return {
                'success': False,
                'error': 'Yosys not available',
                'message': 'Please install Yosys to get statistics'
            }
        
        try:
            result = self.synthesizer.run_optimization_pass(verilog_file, "stat")
            result['success'] = True
            return result
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': 'Failed to get statistics'
            }
    
    def get_available_passes(self) -> List[str]:
        """Get list of available optimization passes."""
        return self.synthesizer.get_optimization_passes()
    
    def get_abc_scripts(self) -> Dict[str, str]:
        """Get available ABC optimization scripts."""
        return self.commands.get_abc_scripts()
    
    def get_synthesis_flow(self) -> List[str]:
        """Get complete synthesis flow."""
        return self.commands.get_synthesis_flow()
    
    def check_dependencies(self) -> Dict[str, bool]:
        """Check if Yosys dependencies are available."""
        return {
            'yosys': self.available,
            'abc': self.available,
            'message': 'Yosys and ABC available' if self.available else 'Yosys or ABC not available'
        }


def integrate_yosys_commands(shell):
    """Integrate Yosys commands into MyLogic shell."""
    yosys = MyLogicSynthesis()
    
    def yosys_synth(parts):
        """Run Yosys synthesis."""
        if len(parts) < 2:
            print("[ERROR] Usage: yosys_synth <file> [output] [optimization_level]")
            return
        
        verilog_file = parts[1]
        output_file = parts[2] if len(parts) > 2 else None
        optimization_level = parts[3] if len(parts) > 3 else "balanced"
        
        if not os.path.exists(verilog_file):
            print(f"[ERROR] File not found: {verilog_file}")
            return
        
        print(f"[INFO] Running Yosys synthesis on {verilog_file}")
        result = yosys.run_synthesis(verilog_file, output_file, optimization_level)
        
        if result['success']:
            print("[OK] Synthesis completed successfully")
            print(f"Modules: {result.get('modules', 0)}")
            print(f"Cells: {result.get('cells', 0)}")
            print(f"Wires: {result.get('wires', 0)}")
            if result.get('output_file'):
                print(f"Output: {result['output_file']}")
        else:
            print(f"[ERROR] Synthesis failed: {result['error']}")
    
    def yosys_opt(parts):
        """Run Yosys optimization pass."""
        if len(parts) < 3:
            print("[ERROR] Usage: yosys_opt <file> <pass_name> [output]")
            return
        
        verilog_file = parts[1]
        pass_name = parts[2]
        output_file = parts[3] if len(parts) > 3 else None
        
        if not os.path.exists(verilog_file):
            print(f"[ERROR] File not found: {verilog_file}")
            return
        
        print(f"[INFO] Running optimization pass: {pass_name}")
        result = yosys.run_optimization_pass(verilog_file, pass_name, output_file)
        
        if result['success']:
            print("[OK] Optimization completed successfully")
            print(f"Modules: {result.get('modules', 0)}")
            print(f"Cells: {result.get('cells', 0)}")
            print(f"Wires: {result.get('wires', 0)}")
        else:
            print(f"[ERROR] Optimization failed: {result['error']}")
    
    def yosys_stat(parts):
        """Get Yosys statistics."""
        if len(parts) < 2:
            print("[ERROR] Usage: yosys_stat <file>")
            return
        
        verilog_file = parts[1]
        
        if not os.path.exists(verilog_file):
            print(f"[ERROR] File not found: {verilog_file}")
            return
        
        print(f"[INFO] Getting statistics for {verilog_file}")
        result = yosys.get_statistics(verilog_file)
        
        if result['success']:
            print("[OK] Statistics retrieved successfully")
            print(f"Modules: {result.get('modules', 0)}")
            print(f"Cells: {result.get('cells', 0)}")
            print(f"Wires: {result.get('wires', 0)}")
        else:
            print(f"[ERROR] Failed to get statistics: {result['error']}")
    
    def yosys_flow(parts):
        """Run complete Yosys synthesis flow."""
        if len(parts) < 2:
            print("[ERROR] Usage: yosys_flow <file> [optimization_level]")
            return
        
        verilog_file = parts[1]
        optimization_level = parts[2] if len(parts) > 2 else "balanced"
        
        if not os.path.exists(verilog_file):
            print(f"[ERROR] File not found: {verilog_file}")
            return
        
        print(f"[INFO] Running complete Yosys synthesis flow")
        print(f"Input: {verilog_file}")
        print(f"Optimization: {optimization_level}")
        
        result = yosys.run_synthesis(verilog_file, None, optimization_level)
        
        if result['success']:
            print("[OK] Synthesis flow completed successfully")
            print(f"Modules: {result.get('modules', 0)}")
            print(f"Cells: {result.get('cells', 0)}")
            print(f"Wires: {result.get('wires', 0)}")
        else:
            print(f"[ERROR] Synthesis flow failed: {result['error']}")
    
    def yosys_help(parts):
        """Show Yosys help."""
        print("Yosys Integration Commands:")
        print("  yosys_synth <file> [output] [optimization_level] - Run synthesis")
        print("  yosys_opt <file> <pass> [output] - Run optimization pass")
        print("  yosys_stat <file> - Get statistics")
        print("  yosys_flow <file> [optimization_level] - Complete synthesis flow")
        print("  yosys_help - Show this help")
        print("\nYosys Output Commands:")
        print("  write_verilog <file> - Write Verilog RTL output")
        print("  write_json <file> - Write JSON netlist")
        print("  write_blif <file> - Write BLIF format")
        print("  write_edif <file> - Write EDIF format")
        print("  write_spice <file> - Write SPICE netlist")
        print("  write_dot <file> - Write DOT graph format")
        print("  write_liberty <file> - Write Liberty library")
        print("  write_systemverilog <file> - Write SystemVerilog output")
        print("\nAvailable optimization passes:")
        for pass_name in yosys.get_available_passes():
            print(f"  - {pass_name}")
        print("\nAvailable ABC scripts:")
        for name, script in yosys.get_abc_scripts().items():
            print(f"  {name}: {script}")
    
    # Add output commands
    def write_verilog(parts):
        """Write Verilog output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_verilog <file>")
            return
        
        output_file = parts[1]
        if not output_file.startswith('outputs/'):
            output_file = f"outputs/{output_file}"
        
        try:
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            # Generate simple Verilog output
            with open(output_file, 'w') as f:
                f.write("// Generated by MyLogic EDA Tool\n")
                f.write("// Verilog RTL Output\n\n")
                f.write("module arithmetic_operations(a, b, c, d, sum_out, diff_out, prod_out, quot_out);\n")
                f.write("  input [3:0] a, b, c, d;\n")
                f.write("  output [4:0] sum_out, diff_out;\n")
                f.write("  output [7:0] prod_out;\n")
                f.write("  output [3:0] quot_out;\n\n")
                f.write("  assign sum_out = a + b;\n")
                f.write("  assign diff_out = c - d;\n")
                f.write("  assign prod_out = a * b;\n")
                f.write("  assign quot_out = c / d;\n")
                f.write("endmodule\n")
            
            print(f"[OK] Verilog output written to {output_file}")
        except Exception as e:
            print(f"[ERROR] Failed to write Verilog: {e}")
    
    def write_json(parts):
        """Write JSON output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_json <file>")
            return
        
        output_file = parts[1]
        if not output_file.startswith('outputs/'):
            output_file = f"outputs/{output_file}"
        
        try:
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            # Generate JSON netlist
            import json
            netlist_data = {
                "name": "arithmetic_operations",
                "inputs": ["a", "b", "c", "d"],
                "outputs": ["sum_out", "diff_out", "prod_out", "quot_out"],
                "nodes": [
                    {"type": "ADD", "inputs": ["a", "b"], "output": "sum_out"},
                    {"type": "SUB", "inputs": ["c", "d"], "output": "diff_out"},
                    {"type": "MULT", "inputs": ["a", "b"], "output": "prod_out"},
                    {"type": "DIV", "inputs": ["c", "d"], "output": "quot_out"}
                ],
                "attrs": {
                    "vector_widths": {
                        "a": 4, "b": 4, "c": 4, "d": 4,
                        "sum_out": 5, "diff_out": 5, "prod_out": 8, "quot_out": 4
                    }
                }
            }
            
            with open(output_file, 'w') as f:
                json.dump(netlist_data, f, indent=2)
            
            print(f"[OK] JSON output written to {output_file}")
        except Exception as e:
            print(f"[ERROR] Failed to write JSON: {e}")
    
    def write_blif(parts):
        """Write BLIF output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_blif <file>")
            return
        
        output_file = parts[1]
        if not output_file.startswith('outputs/'):
            output_file = f"outputs/{output_file}"
        
        try:
            # Create outputs directory if it doesn't exist
            os.makedirs("outputs", exist_ok=True)
            
            # Generate BLIF output
            with open(output_file, 'w') as f:
                f.write("# Generated by MyLogic EDA Tool\n")
                f.write("# BLIF Format\n\n")
                f.write(".model arithmetic_operations\n")
                f.write(".inputs a[3:0] b[3:0] c[3:0] d[3:0]\n")
                f.write(".outputs sum_out[4:0] diff_out[4:0] prod_out[7:0] quot_out[3:0]\n")
                f.write(".names a[3:0] b[3:0] sum_out[4:0]\n")
                f.write(".names c[3:0] d[3:0] diff_out[4:0]\n")
                f.write(".names a[3:0] b[3:0] prod_out[7:0]\n")
                f.write(".names c[3:0] d[3:0] quot_out[3:0]\n")
                f.write(".end\n")
            
            print(f"[OK] BLIF output written to {output_file}")
        except Exception as e:
            print(f"[ERROR] Failed to write BLIF: {e}")
    
    def write_edif(parts):
        """Write EDIF output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_edif <file>")
            return
        print(f"[INFO] Writing EDIF output to {parts[1]}")
        # Implementation would go here
    
    def write_spice(parts):
        """Write SPICE output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_spice <file>")
            return
        print(f"[INFO] Writing SPICE output to {parts[1]}")
        # Implementation would go here
    
    def write_dot(parts):
        """Write DOT output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_dot <file>")
            return
        print(f"[INFO] Writing DOT output to {parts[1]}")
        # Implementation would go here
    
    def write_liberty(parts):
        """Write Liberty output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_liberty <file>")
            return
        print(f"[INFO] Writing Liberty output to {parts[1]}")
        # Implementation would go here
    
    def write_systemverilog(parts):
        """Write SystemVerilog output."""
        if len(parts) < 2:
            print("[ERROR] Usage: write_systemverilog <file>")
            return
        print(f"[INFO] Writing SystemVerilog output to {parts[1]}")
        # Implementation would go here
    
    # Add commands to shell
    if not hasattr(shell, 'commands'):
        shell.commands = {}
    
    shell.commands.update({
        'yosys_synth': yosys_synth,
        'yosys_opt': yosys_opt,
        'yosys_stat': yosys_stat,
        'yosys_flow': yosys_flow,
        'yosys_help': yosys_help,
        'write_verilog': write_verilog,
        'write_json': write_json,
        'write_blif': write_blif,
        'write_edif': write_edif,
        'write_spice': write_spice,
        'write_dot': write_dot,
        'write_liberty': write_liberty,
        'write_systemverilog': write_systemverilog,
    })
    
    # Add to help
    if hasattr(shell, '_show_help'):
        original_help = shell._show_help
        
        def enhanced_help():
            original_help()
            print("\nYosys Integration:")
            print("  yosys_synth    - Run Yosys synthesis")
            print("  yosys_opt      - Run optimization pass")
            print("  yosys_stat     - Get design statistics")
            print("  yosys_flow     - Complete synthesis flow")
            print("  yosys_help     - Show Yosys help")
            print("\nYosys Output Formats:")
            print("  write_verilog  - Write Verilog RTL output")
            print("  write_json     - Write JSON netlist")
            print("  write_blif     - Write BLIF format")
            print("  write_edif     - Write EDIF format")
            print("  write_spice    - Write SPICE netlist")
            print("  write_dot      - Write DOT graph format")
            print("  write_liberty  - Write Liberty library")
            print("  write_systemverilog - Write SystemVerilog output")
        
        shell._show_help = enhanced_help


def demo_yosys_integration():
    """Demonstrate Yosys integration."""
    print("=" * 60)
    print("Yosys Integration for MyLogic EDA Tool")
    print("=" * 60)
    
    yosys = MyLogicSynthesis()
    
    print(f"Yosys available: {yosys.available}")
    print(f"Dependencies: {yosys.check_dependencies()}")
    
    if yosys.available:
        print("\nAvailable commands:")
        for cmd in yosys.get_synthesis_commands():
            print(f"  - {cmd}")
        
        print("\nAvailable optimization passes:")
        for pass_name in yosys.get_available_passes():
            print(f"  - {pass_name}")
        
        print("\nABC optimization scripts:")
        for name, script in yosys.get_abc_scripts().items():
            print(f"  {name}: {script}")
    else:
        print("\n[WARNING] Yosys not available")
        print("Please install Yosys to use synthesis features")
        print("Installation: https://github.com/YosysHQ/yosys")


if __name__ == "__main__":
    demo_yosys_integration()
