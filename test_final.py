#!/usr/bin/env python3
"""Final test of DCE fix"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import SynthesisFlow

print("="*60)
print("FINAL DCE TEST")
print("="*60)

# Parse
netlist = parse_verilog('examples/full_adder.v')
print(f"\nOriginal nodes: {len(netlist.get('nodes', []))}")

# Run complete synthesis
flow = SynthesisFlow()
result = flow.run_complete_synthesis(netlist, "standard")

# Check result
final_nodes = result.get('nodes', [])
node_count = len(final_nodes) if isinstance(final_nodes, (list, dict)) else 0

print(f"\nFinal nodes: {node_count}")

if isinstance(final_nodes, list):
    node_types = {}
    for n in final_nodes:
        if isinstance(n, dict):
            node_type = n.get('type', 'UNKNOWN')
            node_types[node_type] = node_types.get(node_type, 0) + 1
    print(f"Node types: {node_types}")
    
    # Check if we have correct structure
    expected = {'XOR': 2, 'AND': 2, 'OR': 1}
    print(f"\nExpected: {expected}")
    
    if node_types.get('XOR', 0) == 2 and node_types.get('AND', 0) == 2 and node_types.get('OR', 0) == 1:
        print("SUCCESS! Full adder has correct structure!")
    else:
        print("FAILED! Structure not correct.")
        print(f"Got: {node_types}")

print("\n" + "="*60)

