#!/usr/bin/env python3
"""
Standalone AST Dump Utility

Dump netlist structure dạng AST tree (tương tự Yosys -dump_ast).

Usage:
    python tools/dump_ast.py <verilog_file>
    
Example:
    python tools/dump_ast.py examples/11_bitwise/test_bitwise.v
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from parsers import parse_verilog
from typing import Dict, List, Any


def print_expression_tree(node: Dict[str, Any], all_nodes: List[Dict], 
                         signal_to_node: Dict[str, Dict], node_by_id: Dict[str, Dict],
                         node_outputs: Dict[str, str], all_signals: set, indent: str = ""):
    """
    Print expression tree cho một node (recursive).
    
    Args:
        node: Node dictionary
        all_nodes: List of all nodes
        signal_to_node: Dict mapping output signal names to nodes
        node_by_id: Dict mapping node_id to node
        node_outputs: Dict mapping node_id to output signal name
        all_signals: Set of all valid signal names (inputs + node outputs)
        indent: Current indentation string
    """
    node_type = node.get('type', 'UNKNOWN')
    node_id = node.get('id', '')
    output = node.get('output', '')
    
    # Get inputs
    inputs = node.get('inputs', [])
    fanins = node.get('fanins', [])
    
    # Determine input signals
    input_signals = []
    if fanins:
        for fanin in fanins:
            if isinstance(fanin, (list, tuple)) and len(fanin) > 0:
                input_signals.append(str(fanin[0]))
            else:
                input_signals.append(str(fanin))
    elif inputs:
        input_signals = [str(inp) for inp in inputs]
    
    # Map node type to AST-like format
    ast_type_map = {
        'AND': 'NETLIST_BIT_AND',
        'OR': 'NETLIST_BIT_OR',
        'XOR': 'NETLIST_BIT_XOR',
        'NAND': 'NETLIST_BIT_NAND',
        'NOR': 'NETLIST_BIT_NOR',
        'XNOR': 'NETLIST_BIT_XNOR',
        'NOT': 'NETLIST_BIT_NOT',
        'BUF': 'NETLIST_BUF',
        'ADD': 'NETLIST_ADD',
        'SUB': 'NETLIST_SUB',
        'MUL': 'NETLIST_MUL',
        'DIV': 'NETLIST_DIV',
        'EQ': 'NETLIST_EQ',
        'MUX': 'NETLIST_MUX',
    }
    
    ast_type = ast_type_map.get(node_type, f'NETLIST_{node_type}')
    
    # Print node
    if len(input_signals) > 0:
        print(f"{indent}{ast_type} <{node_id}>")
        
        # Print children (inputs)
        for input_signal in input_signals:
            # Check if this signal is output of another node (including temp signals)
            if input_signal in signal_to_node:
                # This is output of another node - recursive print
                child_node = signal_to_node[input_signal]
                print_expression_tree(
                    child_node, all_nodes, signal_to_node,
                    node_by_id, node_outputs, all_signals,
                    indent=indent + "  "
                )
            elif input_signal in all_signals:
                # Valid signal (input or intermediate) - print as identifier
                if input_signal in ['const_True', 'const_False', '1', '0']:
                    const_val = '1' if input_signal in ['const_True', '1'] else '0'
                    print(f"{indent}  NETLIST_CONSTANT <{const_val}>")
                else:
                    print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
            else:
                # Unknown signal - print as-is
                print(f"{indent}  NETLIST_IDENTIFIER <{input_signal}>")
    else:
        # Leaf node
        if node_type in ['CONST0', 'CONST1']:
            const_val = '1' if node_type == 'CONST1' else '0'
            print(f"{indent}NETLIST_CONSTANT <{const_val}>")
        else:
            print(f"{indent}{ast_type} <{node_id}>")


def dump_ast(verilog_file: str):
    """
    Parse Verilog file và dump AST structure.
    
    Args:
        verilog_file: Path to Verilog file
    """
    if not os.path.exists(verilog_file):
        print(f"[ERROR] File not found: {verilog_file}")
        return
    
    try:
        # Parse Verilog
        netlist = parse_verilog(verilog_file)
        
        # Get netlist data
        module_name = netlist.get('name', 'unknown')
        inputs = netlist.get('inputs', [])
        outputs = netlist.get('outputs', [])
        nodes = netlist.get('nodes', [])
        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
        
        # Convert nodes to list if dict
        if isinstance(nodes, dict):
            nodes = list(nodes.values())
        
        print(f"Executing Verilog-2005 frontend: {os.path.basename(verilog_file)}")
        print(f"\nParsing SystemVerilog input from `{os.path.basename(verilog_file)}' to AST representation.")
        print(f"\nGenerating NETLIST representation for module `\\{module_name}'.\n")
        
        print("Dumping AST structure:\n")
        print(f"    NETLIST_MODULE <{module_name}>")
        
        # Print ports
        for inp in inputs:
            print(f"      NETLIST_WIRE <{inp}> input port")
        
        for out in outputs:
            print(f"      NETLIST_WIRE <{out}> output port")
        
        # Build mappings:
        # 1. signal_to_node: output signal name -> node
        # 2. node_by_id: node_id -> node
        # 3. node_outputs: node_id -> output signal name
        signal_to_node = {}
        node_by_id = {}
        node_outputs = {}
        all_signals = set(inputs)  # Include inputs as valid signals
        
        # First, build node_by_id
        for node in nodes:
            node_id = node.get('id', '')
            node_by_id[node_id] = node
        
        # Then, build signal_to_node using output_mapping
        for signal, mapped_node_id in output_mapping.items():
            if mapped_node_id in node_by_id:
                signal_to_node[signal] = node_by_id[mapped_node_id]
                node_outputs[mapped_node_id] = signal
                all_signals.add(signal)
        
        # Also check for nodes with explicit output field
        for node in nodes:
            node_id = node.get('id', '')
            output = node.get('output', '')
            if output and output not in signal_to_node:
                signal_to_node[output] = node
                node_outputs[node_id] = output
                all_signals.add(output)
        
        # Build output assignments tree
        for output_name in outputs:
            print(f"\n      NETLIST_ASSIGN <{output_name}>")
            
            # Find node that drives this output
            node_id = output_mapping.get(output_name, '')
            node = None
            
            if node_id and node_id in node_by_id:
                node = node_by_id[node_id]
            elif output_name in signal_to_node:
                node = signal_to_node[output_name]
            else:
                # Try to find node by matching output name with node output
                for n in nodes:
                    if n.get('output') == output_name:
                        node = n
                        break
            
            if node:
                print_expression_tree(
                    node, nodes, signal_to_node, node_by_id, node_outputs,
                    all_signals, indent="        "
                )
            else:
                print(f"        NETLIST_IDENTIFIER <{output_name}>")
        
        print("\n--- END OF AST DUMP ---\n")
        print("Successfully finished Verilog frontend.\n")
        
    except Exception as e:
        print(f"[ERROR] Failed to parse or dump AST: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python tools/dump_ast.py <verilog_file>")
        print("\nExample:")
        print("  python tools/dump_ast.py examples/11_bitwise/test_bitwise.v")
        sys.exit(1)
    
    verilog_file = sys.argv[1]
    dump_ast(verilog_file)

