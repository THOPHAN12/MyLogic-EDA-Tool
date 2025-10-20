#!/usr/bin/env python3
"""
Hiển thị thông tin về các file SVG đã tạo
"""

import os
import glob

def show_svg_info():
    """Hiển thị thông tin về các file SVG."""
    
    print("=== SVG FILES INFORMATION ===")
    
    # Tìm tất cả file SVG
    svg_files = glob.glob("examples/*.svg")
    
    if not svg_files:
        print("No SVG files found in examples/")
        return
    
    print(f"Found {len(svg_files)} SVG files:")
    print()
    
    for svg_file in sorted(svg_files):
        try:
            file_size = os.path.getsize(svg_file)
            file_name = os.path.basename(svg_file)
            
            print(f"File: {file_name}")
            print(f"  Path: {svg_file}")
            print(f"  Size: {file_size} bytes")
            
            # Đọc một phần nội dung để xem thông tin
            with open(svg_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Tìm title
            if '<title>' in content:
                title_start = content.find('<title>') + 7
                title_end = content.find('</title>')
                if title_start < title_end:
                    title = content[title_start:title_end]
                    print(f"  Title: {title}")
            
            # Tìm module name
            if 'Circuit Diagram:' in content:
                start = content.find('Circuit Diagram:') + 17
                end = content.find('</text>', start)
                if start < end:
                    module_name = content[start:end].strip()
                    print(f"  Module: {module_name}")
            
            # Đếm elements
            rect_count = content.count('<rect')
            text_count = content.count('<text')
            print(f"  Elements: {rect_count} rectangles, {text_count} text elements")
            
        except Exception as e:
            print(f"  [ERROR] Cannot read file: {e}")
        
        print()

def main():
    show_svg_info()

if __name__ == "__main__":
    main()
