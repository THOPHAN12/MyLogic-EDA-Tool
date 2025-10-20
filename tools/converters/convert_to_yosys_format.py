#!/usr/bin/env python3
"""
Converter từ MyLogic JSON format sang Yosys JSON format
"""

import json
import sys
from datetime import datetime

def convert_mylogic_to_yosys(mylogic_json_path, output_path=None):
    """Convert MyLogic JSON to Yosys JSON format."""
    
    # Load MyLogic JSON
    with open(mylogic_json_path, 'r', encoding='utf-8') as f:
        mylogic_data = json.load(f)
    
    netlist = mylogic_data['netlist']
    metadata = mylogic_data['metadata']
    
    # Create Yosys format
    yosys_data = {
        "creator": f"MyLogic EDA Tool {metadata['version']}",
        "modules": {
            netlist['name']: {
                "attributes": {
                    "top": "00000000000000000000000000000001",
                    "src": f"{metadata['source_file']}:1.1-{len(netlist.get('nodes', []))}.10"
                },
                "ports": {},
                "cells": {},
                "netnames": {}
            }
        }
    }
    
    module = yosys_data["modules"][netlist['name']]
    
    # Convert inputs to ports
    for i, input_name in enumerate(netlist.get('inputs', [])):
        vector_width = netlist.get('attrs', {}).get('vector_widths', {}).get(input_name, 1)
        bits = list(range(i*100 + 1, i*100 + vector_width + 1))
        module["ports"][input_name] = {
            "direction": "input",
            "bits": bits
        }
    
    # Convert outputs to ports
    for i, output_name in enumerate(netlist.get('outputs', [])):
        vector_width = netlist.get('attrs', {}).get('vector_widths', {}).get(output_name, 1)
        bits = list(range(1000 + i*100 + 1, 1000 + i*100 + vector_width + 1))
        module["ports"][output_name] = {
            "direction": "output", 
            "bits": bits
        }
    
    # Convert nodes to cells
    cell_counter = 0
    bit_counter = 2000  # Start from high bit numbers to avoid conflicts
    for node in netlist.get('nodes', []):
        cell_id = f"$mylogic${cell_counter}"
        cell_counter += 1
        
        node_type = node.get('type', 'UNKNOWN')
        fanins = node.get('fanins', [])
        
        # Map MyLogic node types to Yosys cell types
        yosys_type_map = {
            'AND': '$_AND_',
            'OR': '$_OR_', 
            'XOR': '$_XOR_',
            'NAND': '$_NAND_',
            'NOR': '$_NOR_',
            'NOT': '$_NOT_',
            'BUF': '$_BUF_',
            'ADD': '$_ADD_',
            'SUB': '$_SUB_',
            'MUL': '$_MUL_',
            'DIV': '$_DIV_',
            'MUX': '$_MUX_'
        }
        
        yosys_type = yosys_type_map.get(node_type, f'$_{node_type}_')
        
        # Create cell with proper connections
        cell = {
            "hide_name": 1,
            "type": yosys_type,
            "parameters": {},
            "attributes": {},
            "port_directions": {},
            "connections": {}
        }
        
        # Handle different node types with proper connections
        if node_type in ['AND', 'OR', 'XOR', 'NAND', 'NOR']:
            cell["port_directions"] = {
                "A": "input",
                "B": "input", 
                "Y": "output"
            }
            # Use numeric bit indices for connections
            cell["connections"] = {
                "A": [bit_counter + 1],
                "B": [bit_counter + 2],
                "Y": [bit_counter + 3]
            }
            bit_counter += 4
        
        elif node_type in ['NOT', 'BUF']:
            cell["port_directions"] = {
                "A": "input",
                "Y": "output"
            }
            # Use numeric bit indices for connections
            cell["connections"] = {
                "A": [bit_counter + 1],
                "Y": [bit_counter + 2]
            }
            bit_counter += 3
        
        elif node_type == 'MUX':
            cell["port_directions"] = {
                "A": "input",
                "B": "input",
                "S": "input", 
                "Y": "output"
            }
            # Use numeric bit indices for connections
            cell["connections"] = {
                "A": [bit_counter + 1],
                "B": [bit_counter + 2],
                "S": [bit_counter + 3],
                "Y": [bit_counter + 4]
            }
            bit_counter += 5
        
        module["cells"][cell_id] = cell
    
    # Add netnames for inputs/outputs
    bit_counter = 1
    for input_name in netlist.get('inputs', []):
        vector_width = netlist.get('attrs', {}).get('vector_widths', {}).get(input_name, 1)
        bits = list(range(bit_counter, bit_counter + vector_width))
        module["netnames"][input_name] = {
            "hide_name": 0,
            "bits": bits,
            "attributes": {
                "src": f"{metadata['source_file']}:2.15-2.17"
            }
        }
        bit_counter += vector_width
    
    for output_name in netlist.get('outputs', []):
        vector_width = netlist.get('attrs', {}).get('vector_widths', {}).get(output_name, 1)
        bits = list(range(bit_counter, bit_counter + vector_width))
        module["netnames"][output_name] = {
            "hide_name": 0,
            "bits": bits,
            "attributes": {
                "src": f"{metadata['source_file']}:3.16-3.19"
            }
        }
        bit_counter += vector_width
    
    # Save Yosys format
    if output_path is None:
        output_path = mylogic_json_path.replace('.json', '_yosys.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(yosys_data, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Converted MyLogic JSON to Yosys format: {output_path}")
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python convert_to_yosys_format.py <mylogic_json_file> [output_file]")
        sys.exit(1)
    
    mylogic_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_mylogic_to_yosys(mylogic_file, output_file)
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
