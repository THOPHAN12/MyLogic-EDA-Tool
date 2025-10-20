#!/usr/bin/env python3
"""
Hiển thị cấu trúc Yosys JSON đã chuyển đổi
"""

import json
import sys

def show_yosys_structure(json_file):
    """Hiển thị cấu trúc Yosys JSON."""
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print("=== YOSYS JSON STRUCTURE ===")
    print(f"Creator: {data['creator']}")
    print()
    
    for module_name, module_data in data['modules'].items():
        print(f"Module: {module_name}")
        print(f"  Top: {module_data['attributes']['top']}")
        print(f"  Source: {module_data['attributes']['src']}")
        print()
        
        print("  Ports:")
        for port_name, port_info in module_data['ports'].items():
            direction = port_info['direction']
            bits = port_info['bits']
            print(f"    {port_name} ({direction}): {bits}")
        print()
        
        print("  Cells:")
        for cell_id, cell_info in module_data['cells'].items():
            cell_type = cell_info['type']
            connections = cell_info.get('connections', {})
            print(f"    {cell_id}: {cell_type}")
            if connections:
                for port, bits in connections.items():
                    print(f"      {port}: {bits}")
        print()
        
        print("  Netnames:")
        for net_name, net_info in module_data['netnames'].items():
            bits = net_info['bits']
            hide_name = net_info['hide_name']
            print(f"    {net_name}: {bits} (hide: {hide_name})")
        print()

def main():
    if len(sys.argv) < 2:
        print("Usage: python show_yosys_structure.py <yosys_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    try:
        show_yosys_structure(json_file)
    except Exception as e:
        print(f"[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
