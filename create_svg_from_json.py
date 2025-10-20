#!/usr/bin/env python3
"""
Tạo file SVG từ Yosys JSON format
"""

import json
import sys
import os
import subprocess

def create_svg_from_yosys_json(json_file, output_svg=None):
    """Tạo SVG từ Yosys JSON format."""
    
    if not os.path.exists(json_file):
        print(f"[ERROR] File not found: {json_file}")
        return False
    
    # Tạo tên file output nếu không được chỉ định
    if output_svg is None:
        base_name = json_file.replace('.json', '')
        output_svg = f"{base_name}.svg"
    
    print(f"Converting: {json_file} -> {output_svg}")
    
    # Kiểm tra netlistsvg có sẵn không
    try:
        # Test netlistsvg command
        result = subprocess.run(['netlistsvg', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode != 0:
            print("[WARNING] netlistsvg not working properly")
            return create_svg_manually(json_file, output_svg)
    except FileNotFoundError:
        print("[INFO] netlistsvg not found, creating SVG manually")
        return create_svg_manually(json_file, output_svg)
    except Exception as e:
        print(f"[WARNING] netlistsvg error: {e}")
        return create_svg_manually(json_file, output_svg)
    
    # Sử dụng netlistsvg nếu có
    try:
        result = subprocess.run(['netlistsvg', json_file, '-o', output_svg], 
                              capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            print(f"[SUCCESS] Created SVG with netlistsvg: {output_svg}")
            if os.path.exists(output_svg):
                file_size = os.path.getsize(output_svg)
                print(f"  File size: {file_size} bytes")
            return True
        else:
            print(f"[ERROR] netlistsvg failed: {result.stderr}")
            return create_svg_manually(json_file, output_svg)
    except subprocess.TimeoutExpired:
        print("[ERROR] netlistsvg timed out")
        return create_svg_manually(json_file, output_svg)
    except Exception as e:
        print(f"[ERROR] netlistsvg error: {e}")
        return create_svg_manually(json_file, output_svg)

def create_svg_manually(json_file, output_svg):
    """Tạo SVG thủ công từ JSON."""
    
    print("[INFO] Creating SVG manually...")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot read JSON: {e}")
        return False
    
    # Lấy thông tin module
    modules = data.get('modules', {})
    if not modules:
        print("[ERROR] No modules found in JSON")
        return False
    
    module_name = list(modules.keys())[0]
    module_data = modules[module_name]
    
    # Tạo SVG content
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <style>
      .module-box {{ fill: #e1f5fe; stroke: #01579b; stroke-width: 2; }}
      .port-box {{ fill: #f3e5f5; stroke: #4a148c; stroke-width: 1; }}
      .cell-box {{ fill: #fff3e0; stroke: #e65100; stroke-width: 1; }}
      .text {{ font-family: Arial, sans-serif; font-size: 12px; }}
      .title {{ font-size: 16px; font-weight: bold; }}
      .port-text {{ font-size: 10px; }}
    </style>
  </defs>
  
  <!-- Background -->
  <rect width="800" height="600" fill="#fafafa"/>
  
  <!-- Title -->
  <text x="400" y="30" text-anchor="middle" class="text title" fill="#1976d2">
    Circuit Diagram: {module_name}
  </text>
  
  <!-- Module Box -->
  <rect x="50" y="60" width="700" height="500" class="module-box" rx="10"/>
  <text x="400" y="85" text-anchor="middle" class="text title" fill="#01579b">
    {module_name}
  </text>
"""
    
    # Thêm ports
    ports = module_data.get('ports', {})
    y_pos = 120
    for port_name, port_info in ports.items():
        direction = port_info.get('direction', 'unknown')
        bits = port_info.get('bits', [])
        color = "#4caf50" if direction == "input" else "#f44336"
        
        svg_content += f"""
  <!-- Port: {port_name} -->
  <rect x="70" y="{y_pos}" width="100" height="30" class="port-box" fill="{color}"/>
  <text x="120" y="{y_pos + 20}" text-anchor="middle" class="text port-text" fill="white">
    {port_name} ({direction})
  </text>
  <text x="180" y="{y_pos + 20}" class="text port-text" fill="#666">
    bits: {bits}
  </text>
"""
        y_pos += 40
    
    # Thêm cells
    cells = module_data.get('cells', {})
    y_pos = 300
    for cell_id, cell_info in cells.items():
        cell_type = cell_info.get('type', 'unknown')
        connections = cell_info.get('connections', {})
        
        svg_content += f"""
  <!-- Cell: {cell_id} -->
  <rect x="200" y="{y_pos}" width="150" height="40" class="cell-box"/>
  <text x="275" y="{y_pos + 15}" text-anchor="middle" class="text" fill="#e65100">
    {cell_id}
  </text>
  <text x="275" y="{y_pos + 30}" text-anchor="middle" class="text" fill="#e65100">
    {cell_type}
  </text>
"""
        
        # Thêm connections info
        conn_text = ""
        for port, bits in connections.items():
            conn_text += f"{port}:{bits} "
        
        svg_content += f"""
  <text x="370" y="{y_pos + 20}" class="text port-text" fill="#666">
    {conn_text.strip()}
  </text>
"""
        y_pos += 60
    
    # Thêm netnames
    netnames = module_data.get('netnames', {})
    y_pos = 500
    svg_content += """
  <!-- Netnames -->
  <text x="70" y="480" class="text" fill="#1976d2">Netnames:</text>
"""
    
    for net_name, net_info in netnames.items():
        bits = net_info.get('bits', [])
        hide_name = net_info.get('hide_name', 0)
        display_name = f"${net_name}$" if hide_name else net_name
        
        svg_content += f"""
  <text x="70" y="{y_pos}" class="text port-text" fill="#666">
    {display_name}: {bits}
  </text>
"""
        y_pos += 15
    
    svg_content += """
</svg>"""
    
    # Ghi file SVG
    try:
        with open(output_svg, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        print(f"[SUCCESS] Created manual SVG: {output_svg}")
        
        if os.path.exists(output_svg):
            file_size = os.path.getsize(output_svg)
            print(f"  File size: {file_size} bytes")
        return True
    except Exception as e:
        print(f"[ERROR] Cannot write SVG: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_svg_from_json.py <yosys_json_file> [output_svg]")
        sys.exit(1)
    
    json_file = sys.argv[1]
    output_svg = sys.argv[2] if len(sys.argv) > 2 else None
    
    if create_svg_from_yosys_json(json_file, output_svg):
        print("\n[SUCCESS] SVG file created successfully!")
    else:
        print("\n[FAILED] Failed to create SVG file")
        sys.exit(1)

if __name__ == "__main__":
    main()
