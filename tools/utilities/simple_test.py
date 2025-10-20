#!/usr/bin/env python3
"""
Simple test for Yosys JSON format
"""

import json
import sys

def test_json_format(json_file):
    """Test JSON format compatibility."""
    
    print(f"Testing: {json_file}")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("[OK] JSON is valid")
    except Exception as e:
        print(f"[ERROR] JSON invalid: {e}")
        return False
    
    # Check structure
    if 'creator' not in data:
        print("[ERROR] Missing creator field")
        return False
    print("[OK] Has creator field")
    
    if 'modules' not in data:
        print("[ERROR] Missing modules field")
        return False
    print("[OK] Has modules field")
    
    # Check modules
    modules = data['modules']
    if not modules:
        print("[ERROR] No modules found")
        return False
    
    for module_name, module_data in modules.items():
        print(f"[OK] Module: {module_name}")
        
        # Check cells
        cells = module_data.get('cells', {})
        print(f"  Cells: {len(cells)}")
        
        for cell_id, cell_info in cells.items():
            cell_type = cell_info.get('type', 'unknown')
            connections = cell_info.get('connections', {})
            print(f"    {cell_id}: {cell_type}")
            
            # Check connections are numeric
            for port, bits in connections.items():
                if not isinstance(bits, list):
                    print(f"[ERROR] {cell_id} port {port} not a list")
                    return False
                for bit in bits:
                    if not isinstance(bit, int):
                        print(f"[ERROR] {cell_id} port {port} bit {bit} not numeric")
                        return False
                print(f"      {port}: {bits}")
    
    print("[OK] All checks passed!")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python simple_test.py <json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    if test_json_format(json_file):
        print("\n[SUCCESS] JSON format is compatible!")
    else:
        print("\n[FAILED] JSON format has issues")
        sys.exit(1)
