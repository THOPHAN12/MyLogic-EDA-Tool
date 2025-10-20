#!/usr/bin/env python3
"""
So sánh format MyLogic JSON vs Yosys JSON
"""

import json
import sys

def compare_formats(mylogic_file, yosys_file):
    """So sánh hai format JSON."""
    
    # Load MyLogic JSON
    with open(mylogic_file, 'r', encoding='utf-8') as f:
        mylogic_data = json.load(f)
    
    # Load Yosys JSON  
    with open(yosys_file, 'r', encoding='utf-8') as f:
        yosys_data = json.load(f)
    
    print("=== FORMAT COMPARISON ===")
    print()
    
    # Metadata comparison
    print("METADATA:")
    print(f"  MyLogic Creator: {mylogic_data['metadata']['tool']}")
    print(f"  Yosys Creator: {yosys_data['creator']}")
    print()
    
    # Module comparison
    mylogic_netlist = mylogic_data['netlist']
    yosys_module = list(yosys_data['modules'].values())[0]
    
    print("MODULE INFO:")
    print(f"  MyLogic Name: {mylogic_netlist['name']}")
    print(f"  Yosys Module: {list(yosys_data['modules'].keys())[0]}")
    print()
    
    # Ports comparison
    print("PORTS:")
    print("  MyLogic Inputs:", mylogic_netlist.get('inputs', []))
    print("  MyLogic Outputs:", mylogic_netlist.get('outputs', []))
    print("  Yosys Ports:")
    for port_name, port_info in yosys_module['ports'].items():
        direction = port_info['direction']
        bits = port_info['bits']
        print(f"    {port_name} ({direction}): {bits}")
    print()
    
    # Nodes/Cells comparison
    print("NODES/CELLS:")
    print(f"  MyLogic Nodes: {len(mylogic_netlist.get('nodes', []))}")
    print(f"  Yosys Cells: {len(yosys_module.get('cells', {}))}")
    print()
    
    print("  MyLogic Node Types:")
    node_types = {}
    for node in mylogic_netlist.get('nodes', []):
        node_type = node.get('type', 'UNKNOWN')
        node_types[node_type] = node_types.get(node_type, 0) + 1
    for node_type, count in node_types.items():
        print(f"    {node_type}: {count}")
    print()
    
    print("  Yosys Cell Types:")
    cell_types = {}
    for cell_id, cell_info in yosys_module.get('cells', {}).items():
        cell_type = cell_info.get('type', 'UNKNOWN')
        cell_types[cell_type] = cell_types.get(cell_type, 0) + 1
    for cell_type, count in cell_types.items():
        print(f"    {cell_type}: {count}")
    print()
    
    # Wires comparison
    print("WIRES:")
    print(f"  MyLogic Wires: {len(mylogic_netlist.get('wires', []))}")
    print(f"  Yosys Netnames: {len(yosys_module.get('netnames', {}))}")
    print()
    
    # Vector widths comparison
    print("VECTOR WIDTHS:")
    vector_widths = mylogic_netlist.get('attrs', {}).get('vector_widths', {})
    print("  MyLogic Vector Widths:")
    for signal, width in vector_widths.items():
        print(f"    {signal}: {width}-bit")
    print()
    
    print("  Yosys Port Bits:")
    for port_name, port_info in yosys_module['ports'].items():
        bits = port_info['bits']
        print(f"    {port_name}: {len(bits)}-bit {bits}")
    print()

def main():
    if len(sys.argv) < 3:
        print("Usage: python compare_formats.py <mylogic_json> <yosys_json>")
        sys.exit(1)
    
    mylogic_file = sys.argv[1]
    yosys_file = sys.argv[2]
    
    try:
        compare_formats(mylogic_file, yosys_file)
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
