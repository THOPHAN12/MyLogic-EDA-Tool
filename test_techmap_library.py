#!/usr/bin/env python3
"""Test technology library cells"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.technology_mapping.technology_mapping import create_standard_library

print("="*60)
print("TECHNOLOGY LIBRARY ANALYSIS")
print("="*60)

library = create_standard_library()

print(f"\nLibrary: {library.name}")
print(f"Total cells: {len(library.cells)}")
print(f"\nAll cells in library:")

for i, (cell_name, cell) in enumerate(library.cells.items(), 1):
    print(f"  {i:2}. {cell_name:8} - Function: {cell.function:20} - Area: {cell.area:.2f}, Delay: {cell.delay:.2f}")

print(f"\nFunction mapping (normalized):")
for func, cell_names in library.function_map.items():
    print(f"  {func:25} -> {cell_names}")

print(f"\nUnique functions: {len(library.function_map)}")
print(f"Total cells: {len(library.cells)}")
print("="*60)

