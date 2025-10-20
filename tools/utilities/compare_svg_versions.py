#!/usr/bin/env python3
"""
So sánh các phiên bản SVG khác nhau
"""

import os
import glob

def compare_svg_versions():
    """So sánh các file SVG."""
    
    print("=== SVG VERSIONS COMPARISON ===")
    
    # Tìm tất cả file SVG
    svg_files = glob.glob("examples/*.svg")
    
    if not svg_files:
        print("No SVG files found")
        return
    
    print(f"Found {len(svg_files)} SVG files:")
    print()
    
    for svg_file in sorted(svg_files):
        try:
            file_size = os.path.getsize(svg_file)
            file_name = os.path.basename(svg_file)
            
            print(f"File: {file_name}")
            print(f"  Size: {file_size} bytes")
            
            # Đọc nội dung để phân tích
            with open(svg_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Đếm các elements
            line_count = content.count('<line')
            rect_count = content.count('<rect')
            text_count = content.count('<text')
            marker_count = content.count('<marker')
            
            print(f"  Elements:")
            print(f"    Lines: {line_count}")
            print(f"    Rectangles: {rect_count}")
            print(f"    Text: {text_count}")
            print(f"    Markers: {marker_count}")
            
            # Kiểm tra connections
            if 'connection-line' in content:
                print(f"  [HAS CONNECTIONS] ✅")
            else:
                print(f"  [NO CONNECTIONS] ❌")
            
            # Kiểm tra arrows
            if 'arrowhead' in content:
                print(f"  [HAS ARROWS] ✅")
            else:
                print(f"  [NO ARROWS] ❌")
            
            # Kiểm tra positioning
            if 'port_positions' in content or 'cell_positions' in content:
                print(f"  [HAS POSITIONING] ✅")
            else:
                print(f"  [NO POSITIONING] ❌")
            
        except Exception as e:
            print(f"  [ERROR] Cannot analyze: {e}")
        
        print()

def main():
    compare_svg_versions()

if __name__ == "__main__":
    main()
