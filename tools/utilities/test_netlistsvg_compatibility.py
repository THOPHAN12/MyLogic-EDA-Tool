#!/usr/bin/env python3
"""
Test netlistsvg compatibility với Yosys JSON format
"""

import json
import subprocess
import sys
import os

def test_netlistsvg_compatibility(json_file):
    """Test if JSON file is compatible with netlistsvg."""
    
    print(f"=== TESTING NETLISTSVG COMPATIBILITY ===")
    print(f"File: {json_file}")
    print()
    
    # Load and validate JSON structure
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print("[OK] JSON file is valid")
    except Exception as e:
        print(f"[ERROR] JSON file is invalid: {e}")
        return False
    
    # Check required fields
    required_fields = ['creator', 'modules']
    for field in required_fields:
        if field not in data:
            print(f"❌ Missing required field: {field}")
            return False
        else:
            print(f"[OK] Found required field: {field}")
    
    # Check modules structure
    modules = data.get('modules', {})
    if not modules:
        print("❌ No modules found")
        return False
    
    print(f"✅ Found {len(modules)} module(s)")
    
    # Check each module
    for module_name, module_data in modules.items():
        print(f"\n--- Module: {module_name} ---")
        
        # Check required module fields
        module_required = ['attributes', 'ports', 'cells', 'netnames']
        for field in module_required:
            if field not in module_data:
                print(f"❌ Module missing field: {field}")
                return False
            else:
                print(f"✅ Module has field: {field}")
        
        # Check ports
        ports = module_data.get('ports', {})
        print(f"  Ports: {len(ports)}")
        for port_name, port_info in ports.items():
            direction = port_info.get('direction', 'unknown')
            bits = port_info.get('bits', [])
            print(f"    {port_name} ({direction}): {len(bits)} bits")
            
            # Validate bits are numbers
            for bit in bits:
                if not isinstance(bit, int):
                    print(f"❌ Port {port_name} has non-numeric bit: {bit}")
                    return False
        
        # Check cells
        cells = module_data.get('cells', {})
        print(f"  Cells: {len(cells)}")
        for cell_id, cell_info in cells.items():
            cell_type = cell_info.get('type', 'unknown')
            connections = cell_info.get('connections', {})
            print(f"    {cell_id}: {cell_type}")
            
            # Validate connections are numeric
            for port, bits in connections.items():
                if not isinstance(bits, list):
                    print(f"❌ Cell {cell_id} port {port} connections not a list")
                    return False
                for bit in bits:
                    if not isinstance(bit, int):
                        print(f"❌ Cell {cell_id} port {port} has non-numeric bit: {bit}")
                        return False
                print(f"      {port}: {bits}")
        
        # Check netnames
        netnames = module_data.get('netnames', {})
        print(f"  Netnames: {len(netnames)}")
        for net_name, net_info in netnames.items():
            bits = net_info.get('bits', [])
            print(f"    {net_name}: {bits}")
            
            # Validate bits are numbers
            for bit in bits:
                if not isinstance(bit, int):
                    print(f"❌ Netname {net_name} has non-numeric bit: {bit}")
                    return False
    
    print("\n✅ All compatibility checks passed!")
    return True

def test_netlistsvg_command(json_file):
    """Test netlistsvg command if available."""
    
    print(f"\n=== TESTING NETLISTSVG COMMAND ===")
    
    # Check if netlistsvg is available
    try:
        result = subprocess.run(['netlistsvg', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ netlistsvg is available")
            print(f"Version: {result.stdout.strip()}")
        else:
            print("❌ netlistsvg command failed")
            return False
    except FileNotFoundError:
        print("❌ netlistsvg not found in PATH")
        return False
    except subprocess.TimeoutExpired:
        print("❌ netlistsvg command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running netlistsvg: {e}")
        return False
    
    # Test with our JSON file
    output_file = json_file.replace('.json', '_test.svg')
    try:
        result = subprocess.run(['netlistsvg', json_file, '-o', output_file], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Successfully generated SVG: {output_file}")
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"   File size: {file_size} bytes")
            return True
        else:
            print(f"❌ netlistsvg failed: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ netlistsvg command timed out")
        return False
    except Exception as e:
        print(f"❌ Error running netlistsvg: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_netlistsvg_compatibility.py <yosys_json_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    
    if not os.path.exists(json_file):
        print(f"❌ File not found: {json_file}")
        sys.exit(1)
    
    # Test compatibility
    if test_netlistsvg_compatibility(json_file):
        print("\n🎉 JSON file is compatible with netlistsvg format!")
        
        # Test netlistsvg command if available
        test_netlistsvg_command(json_file)
    else:
        print("\n❌ JSON file has compatibility issues")
        sys.exit(1)

if __name__ == "__main__":
    main()
