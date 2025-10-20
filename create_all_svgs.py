#!/usr/bin/env python3
"""
Tạo SVG cho tất cả các file JSON trong thư mục examples
"""

import os
import glob
import subprocess
import sys

def create_svg_for_all_json():
    """Tạo SVG cho tất cả file JSON."""
    
    print("=== CREATING SVG FILES FOR ALL JSON ===")
    
    # Tìm tất cả file JSON trong examples
    json_files = glob.glob("examples/*.json")
    
    if not json_files:
        print("[ERROR] No JSON files found in examples/")
        return False
    
    print(f"Found {len(json_files)} JSON files:")
    for json_file in json_files:
        print(f"  - {json_file}")
    print()
    
    success_count = 0
    
    for json_file in json_files:
        print(f"Processing: {json_file}")
        
        # Tạo tên file SVG
        base_name = json_file.replace('.json', '')
        svg_file = f"{base_name}.svg"
        
        try:
            # Sử dụng script create_svg_from_json.py
            result = subprocess.run([
                sys.executable, 'create_svg_from_json.py', 
                json_file, svg_file
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"  [SUCCESS] Created: {svg_file}")
                success_count += 1
            else:
                print(f"  [ERROR] Failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"  [ERROR] Timeout for {json_file}")
        except Exception as e:
            print(f"  [ERROR] Exception: {e}")
        
        print()
    
    print(f"=== SUMMARY ===")
    print(f"Total JSON files: {len(json_files)}")
    print(f"Successfully created SVG: {success_count}")
    print(f"Failed: {len(json_files) - success_count}")
    
    return success_count > 0

def main():
    if create_svg_for_all_json():
        print("\n[SUCCESS] SVG creation completed!")
    else:
        print("\n[FAILED] SVG creation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
