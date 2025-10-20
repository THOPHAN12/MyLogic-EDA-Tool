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
    
    # Tạo SVG content với connections
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="800" viewBox="0 0 1000 800">
  <defs>
    <style>
      .module-box {{ fill: #e1f5fe; stroke: #01579b; stroke-width: 2; }}
      .port-box {{ fill: #f3e5f5; stroke: #4a148c; stroke-width: 1; }}
      .cell-box {{ fill: #fff3e0; stroke: #e65100; stroke-width: 1; }}
      .connection-line {{ stroke: #333; stroke-width: 2; fill: none; marker-end: url(#arrowhead); }}
      .connection-text {{ font-family: Arial, sans-serif; font-size: 10px; fill: #666; }}
      .text {{ font-family: Arial, sans-serif; font-size: 12px; }}
      .title {{ font-size: 16px; font-weight: bold; }}
      .port-text {{ font-size: 10px; }}
    </style>
    <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#333" />
    </marker>
  </defs>
  
  <!-- Background -->
  <rect width="1000" height="800" fill="#fafafa"/>
  
  <!-- Title -->
  <text x="500" y="30" text-anchor="middle" class="text title" fill="#1976d2">
    Circuit Diagram: {module_name}
  </text>
  
  <!-- Module Box -->
  <rect x="50" y="60" width="900" height="700" class="module-box" rx="10"/>
  <text x="500" y="85" text-anchor="middle" class="text title" fill="#01579b">
    {module_name}
  </text>
"""
    
    # Thêm ports với positioning tốt hơn
    ports = module_data.get('ports', {})
    port_positions = {}
    
    # Input ports ở bên trái
    input_y = 150
    for port_name, port_info in ports.items():
        if port_info.get('direction') == 'input':
            bits = port_info.get('bits', [])
            svg_content += f"""
  <!-- Input Port: {port_name} -->
  <rect x="80" y="{input_y}" width="120" height="40" class="port-box" fill="#4caf50"/>
  <text x="140" y="{input_y + 15}" text-anchor="middle" class="text port-text" fill="white">
    {port_name} (input)
  </text>
  <text x="140" y="{input_y + 30}" text-anchor="middle" class="text port-text" fill="white">
    bits: {len(bits)}
  </text>
"""
            port_positions[port_name] = (140, input_y + 20)  # Center position
            input_y += 60
    
    # Output ports ở bên phải
    output_y = 150
    for port_name, port_info in ports.items():
        if port_info.get('direction') == 'output':
            bits = port_info.get('bits', [])
            svg_content += f"""
  <!-- Output Port: {port_name} -->
  <rect x="800" y="{output_y}" width="120" height="40" class="port-box" fill="#f44336"/>
  <text x="860" y="{output_y + 15}" text-anchor="middle" class="text port-text" fill="white">
    {port_name} (output)
  </text>
  <text x="860" y="{output_y + 30}" text-anchor="middle" class="text port-text" fill="white">
    bits: {len(bits)}
  </text>
"""
            port_positions[port_name] = (860, output_y + 20)  # Center position
            output_y += 60
    
    # Thêm cells ở giữa với positioning tốt hơn
    cells = module_data.get('cells', {})
    cell_positions = {}
    y_pos = 300
    
    for cell_id, cell_info in cells.items():
        cell_type = cell_info.get('type', 'unknown')
        connections = cell_info.get('connections', {})
        
        # Position cells ở giữa
        cell_x = 400
        cell_y = y_pos
        
        svg_content += f"""
  <!-- Cell: {cell_id} -->
  <rect x="{cell_x}" y="{cell_y}" width="150" height="50" class="cell-box"/>
  <text x="{cell_x + 75}" y="{cell_y + 20}" text-anchor="middle" class="text" fill="#e65100">
    {cell_id}
  </text>
  <text x="{cell_x + 75}" y="{cell_y + 35}" text-anchor="middle" class="text" fill="#e65100">
    {cell_type}
  </text>
"""
        
        # Lưu vị trí cell
        cell_positions[cell_id] = (cell_x + 75, cell_y + 25)  # Center position
        
        y_pos += 80
    
    # Thêm connections giữa ports và cells
    svg_content += """
  <!-- Connections -->
"""
    
    # Kết nối input ports đến cells
    for port_name, (port_x, port_y) in port_positions.items():
        if port_name in ['in']:  # Input ports
            for cell_id, (cell_x, cell_y) in cell_positions.items():
                # Tạo đường kết nối từ input port đến cell
                svg_content += f"""
  <line x1="{port_x}" y1="{port_y}" x2="{cell_x}" y2="{cell_y}" class="connection-line"/>
  <text x="{(port_x + cell_x) // 2}" y="{(port_y + cell_y) // 2}" class="connection-text">
    {port_name} → {cell_id}
  </text>
"""
    
    # Kết nối cells đến output ports
    for cell_id, (cell_x, cell_y) in cell_positions.items():
        for port_name, (port_x, port_y) in port_positions.items():
            if port_name in ['out', 'valid']:  # Output ports
                # Tạo đường kết nối từ cell đến output port
                svg_content += f"""
  <line x1="{cell_x}" y1="{cell_y}" x2="{port_x}" y2="{port_y}" class="connection-line"/>
  <text x="{(cell_x + port_x) // 2}" y="{(cell_y + port_y) // 2}" class="connection-text">
    {cell_id} → {port_name}
  </text>
"""
    
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
