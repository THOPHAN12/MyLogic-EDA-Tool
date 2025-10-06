"""
DOT Graph Output Generator

Tạo DOT graph output từ optimized netlist.
"""

import os
import sys
from typing import Dict, List, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class DOTGenerator:
    """DOT graph output generator."""
    
    def __init__(self):
        """Initialize DOT generator."""
        self.output_dir = "outputs"
        
    def generate_dot(self, netlist: Dict[str, Any], 
                   output_file: str) -> str:
        """
        Generate DOT graph output from netlist.
        
        Args:
            netlist: Optimized netlist
            output_file: Output file path
            
        Returns:
            Generated DOT content
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
        output_path = os.path.join(self.output_dir, output_file)
        
        # Generate DOT content
        dot_content = self._generate_dot_header()
        dot_content += self._generate_nodes(netlist)
        dot_content += self._generate_edges(netlist)
        dot_content += "}\n"
        
        # Write to file
        with open(output_path, 'w') as f:
            f.write(dot_content)
            
        return dot_content
    
    def _generate_dot_header(self) -> str:
        """Generate DOT header."""
        return "digraph netlist {\n    rankdir=LR;\n    node [shape=box];\n"
    
    def _generate_nodes(self, netlist: Dict[str, Any]) -> str:
        """Generate node declarations."""
        nodes = []
        for node in netlist.get('nodes', []):
            name = node.get('name', '')
            node_type = node.get('type', 'gate')
            nodes.append(f'    {name} [label="{name}\\n{node_type}"];')
        return "\n".join(nodes) + "\n" if nodes else ""
    
    def _generate_edges(self, netlist: Dict[str, Any]) -> str:
        """Generate edge declarations."""
        edges = []
        for connection in netlist.get('connections', []):
            source = connection.get('source', '')
            target = connection.get('target', '')
            edges.append(f"    {source} -> {target};")
        return "\n".join(edges) + "\n" if edges else ""

if __name__ == "__main__":
    generator = DOTGenerator()
    print("DOT Generator initialized.")
