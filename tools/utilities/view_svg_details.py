#!/usr/bin/env python3
"""
Hiển thị chi tiết về file SVG
"""

import os
import re

def view_svg_details(svg_file):
    """Hiển thị chi tiết về file SVG."""
    
    if not os.path.exists(svg_file):
        print(f"[ERROR] File not found: {svg_file}")
        return
    
    print(f"=== SVG FILE DETAILS: {svg_file} ===")
    print()
    
    # File size
    file_size = os.path.getsize(svg_file)
    print(f"File size: {file_size} bytes")
    print()
    
    # Read and analyze content
    with open(svg_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Count elements
    line_count = content.count('<line')
    rect_count = content.count('<rect')
    text_count = content.count('<text')
    marker_count = content.count('<marker')
    circle_count = content.count('<circle')
    polygon_count = content.count('<polygon')
    
    print("ELEMENTS:")
    print(f"  Lines: {line_count}")
    print(f"  Rectangles: {rect_count}")
    print(f"  Text: {text_count}")
    print(f"  Markers: {marker_count}")
    print(f"  Circles: {circle_count}")
    print(f"  Polygons: {polygon_count}")
    print()
    
    # Extract title
    title_match = re.search(r'<title[^>]*>(.*?)</title>', content)
    if title_match:
        title = title_match.group(1)
        print(f"Title: {title}")
    else:
        print("Title: Not found")
    print()
    
    # Extract module name
    module_match = re.search(r'Circuit Diagram: (\w+)', content)
    if module_match:
        module_name = module_match.group(1)
        print(f"Module: {module_name}")
    else:
        print("Module: Not found")
    print()
    
    # Extract ports
    port_matches = re.findall(r'(\w+) \(input\)|(\w+) \(output\)', content)
    inputs = [match[0] for match in port_matches if match[0]]
    outputs = [match[1] for match in port_matches if match[1]]
    
    print("PORTS:")
    print(f"  Inputs: {inputs}")
    print(f"  Outputs: {outputs}")
    print()
    
    # Extract cells
    cell_matches = re.findall(r'(\$mylogic\$\d+)', content)
    print(f"CELLS: {len(cell_matches)}")
    for cell in cell_matches:
        print(f"  - {cell}")
    print()
    
    # Extract connections
    connection_matches = re.findall(r'(\w+) → (\w+)', content)
    print(f"CONNECTIONS: {len(connection_matches)}")
    for conn in connection_matches:
        print(f"  - {conn[0]} -> {conn[1]}")
    print()
    
    # SVG dimensions
    width_match = re.search(r'width="(\d+)"', content)
    height_match = re.search(r'height="(\d+)"', content)
    if width_match and height_match:
        width = width_match.group(1)
        height = height_match.group(1)
        print(f"DIMENSIONS: {width}x{height}")
    print()
    
    # Color usage
    colors = re.findall(r'fill="([^"]+)"', content)
    unique_colors = list(set(colors))
    print(f"COLORS USED: {len(unique_colors)}")
    for color in unique_colors:
        print(f"  - {color}")
    print()
    
    # Check for interactive features
    has_hover = 'hover' in content.lower()
    has_click = 'click' in content.lower()
    has_animation = 'animate' in content.lower()
    
    print("INTERACTIVE FEATURES:")
    print(f"  Hover effects: {'Yes' if has_hover else 'No'}")
    print(f"  Click handlers: {'Yes' if has_click else 'No'}")
    print(f"  Animations: {'Yes' if has_animation else 'No'}")
    print()
    
    # SVG version and namespace
    svg_match = re.search(r'<svg[^>]*xmlns="([^"]+)"', content)
    if svg_match:
        namespace = svg_match.group(1)
        print(f"SVG Namespace: {namespace}")
    print()

def main():
    # Show details for all SVG files
    svg_files = [
        "examples/priority_encoder_circuit.svg",
        "examples/priority_encoder_with_connections.svg", 
        "examples/priority_encoder_yosys.svg",
        "examples/priority_encoder_yosys_fixed.svg"
    ]
    
    for svg_file in svg_files:
        if os.path.exists(svg_file):
            view_svg_details(svg_file)
            print("=" * 60)
            print()

if __name__ == "__main__":
    main()
