#!/usr/bin/env python3
"""Test full synthesis flow"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import SynthesisFlow

print("="*60)
print("FULL SYNTHESIS FLOW TEST")
print("="*60)

netlist = parse_verilog('examples/full_adder.v')
print(f"\nOriginal nodes: {len(netlist.get('nodes', []))}")

flow = SynthesisFlow()
result = flow.run_complete_synthesis(netlist, 'standard')

# Count nodes correctly
nodes = result.get('nodes', [])
node_count = len(nodes) if isinstance(nodes, (dict, list)) else 0

print(f"\nFinal nodes: {node_count}")

# Show node types
if isinstance(nodes, dict):
    node_list = list(nodes.values())
elif isinstance(nodes, list):
    node_list = nodes
else:
    node_list = []

print("\nNode types:")
types = {}
for n in node_list:
    if isinstance(n, dict):
        node_type = n.get('type', 'UNKNOWN')
        types[node_type] = types.get(node_type, 0) + 1

for node_type, count in sorted(types.items()):
    print(f"  {node_type}: {count}")

print("\n" + "="*60)

