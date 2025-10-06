"""
Verilog Output Generator

Tạo Verilog output từ optimized netlist.
"""

import os
import sys
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class VerilogGenerator:
    """Verilog output generator."""
    
    def __init__(self):
        """Initialize Verilog generator."""
        self.output_dir = "outputs"
        
    def generate_verilog(self, netlist: Dict[str, Any], 
                        output_file: str,
                        top_module: Optional[str] = None) -> str:
        """
        Generate Verilog output from netlist.
        
        Args:
            netlist: Optimized netlist
            output_file: Output file path
            top_module: Top module name
            
        Returns:
            Generated Verilog content
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        output_path = os.path.join(self.output_dir, output_file)
        
        # Generate Verilog content
        verilog_content = self._generate_module_header(netlist, top_module)
        verilog_content += self._generate_ports(netlist)
        verilog_content += self._generate_wires(netlist)
        verilog_content += self._generate_instances(netlist)
        verilog_content += "endmodule\n"
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(verilog_content)
            
        return verilog_content
    
    def _generate_module_header(self, netlist: Dict[str, Any], 
                               top_module: Optional[str]) -> str:
        """Generate module header."""
        module_name = top_module or "top_module"
        return f"module {module_name} (\n"
    
    def _generate_ports(self, netlist: Dict[str, Any]) -> str:
        """Generate port declarations."""
        ports = []
        for port in netlist.get('ports', []):
            direction = port.get('direction', 'input')
            name = port.get('name', '')
            width = port.get('width', 1)
            if width > 1:
                ports.append(f"    {direction} [{width-1}:0] {name}")
            else:
                ports.append(f"    {direction} {name}")
        return ";\n".join(ports) + ";\n"
    
    def _generate_wires(self, netlist: Dict[str, Any]) -> str:
        """Generate wire declarations."""
        wires = []
        for wire in netlist.get('wires', []):
            name = wire.get('name', '')
            width = wire.get('width', 1)
            if width > 1:
                wires.append(f"    wire [{width-1}:0] {name};")
            else:
                wires.append(f"    wire {name};")
        return "\n".join(wires) + "\n" if wires else ""
    
    def _generate_instances(self, netlist: Dict[str, Any]) -> str:
        """Generate instance declarations."""
        instances = []
        for instance in netlist.get('instances', []):
            cell_type = instance.get('cell_type', '')
            instance_name = instance.get('name', '')
            connections = instance.get('connections', {})
            
            # Generate connections
            conn_list = []
            for port, signal in connections.items():
                conn_list.append(f".{port}({signal})")
            
            instances.append(f"    {cell_type} {instance_name} ({', '.join(conn_list)});")
        
        return "\n".join(instances) + "\n" if instances else ""

if __name__ == "__main__":
    generator = VerilogGenerator()
    print("Verilog Generator initialized.")
