#!/usr/bin/env python3
"""Debug script for DCE issue"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

from parsers import parse_verilog
from core.synthesis.strash import apply_strash
from core.optimization.dce import apply_dce

print("="*60)
print("TESTING DCE DEBUG")
print("="*60)

# Step 1: Parse
print("\n1. PARSING...")
netlist = parse_verilog('examples/full_adder.v')
print(f"   Nodes: {len(netlist.get('nodes', []))}")
print(f"   Outputs: {netlist.get('outputs', [])}")
print(f"   Output mapping: {netlist.get('attrs', {}).get('output_mapping', {})}")

# Show first few nodes
nodes = netlist.get('nodes', [])
print("\n   First 5 nodes:")
for i, n in enumerate(nodes[:5]):
    if isinstance(n, dict):
        print(f"   [{i}] id={n.get('id')}, type={n.get('type')}, output={n.get('output')}")
        print(f"       inputs={n.get('inputs', [])}, fanins={n.get('fanins', [])}")
        print(f"       all keys: {list(n.keys())}")

# Step 2: Strash
print("\n2. STRASH...")
netlist_after_strash = apply_strash(netlist)
strash_nodes = netlist_after_strash.get('nodes', {})
strash_count = len(strash_nodes) if isinstance(strash_nodes, dict) else len(strash_nodes) if isinstance(strash_nodes, list) else 0
print(f"   Nodes after strash: {strash_count}")
print(f"   Output mapping after strash: {netlist_after_strash.get('attrs', {}).get('output_mapping', {})}")

# Check format
if isinstance(strash_nodes, dict):
    print("   Format: DICT")
    print("   First 5 nodes:")
    for i, (key, node) in enumerate(list(strash_nodes.items())[:5]):
        if isinstance(node, dict):
            print(f"   [{key}] id={node.get('id')}, type={node.get('type')}, output={node.get('output')}, inputs={node.get('inputs', [])}")
elif isinstance(strash_nodes, list):
    print("   Format: LIST")
    print("   First 5 nodes:")
    for i, node in enumerate(strash_nodes[:5]):
        if isinstance(node, dict):
            print(f"   [{i}] id={node.get('id')}, type={node.get('type')}, output={node.get('output')}, inputs={node.get('inputs', [])}")

# Step 3: DCE
print("\n3. DCE...")
print("   Running DCE with detailed logging...")
netlist_after_dce = apply_dce(netlist_after_strash, level="standard")

dce_nodes = netlist_after_dce.get('nodes', {})
dce_count = len(dce_nodes) if isinstance(dce_nodes, dict) else len(dce_nodes) if isinstance(dce_nodes, list) else 0
print(f"\n   Nodes after DCE: {dce_count}")

if isinstance(dce_nodes, dict):
    print("   Format: DICT")
    print("   All nodes:")
    for key, node in dce_nodes.items():
        if isinstance(node, dict):
            print(f"   [{key}] id={node.get('id')}, type={node.get('type')}, output={node.get('output')}")
elif isinstance(dce_nodes, list):
    print("   Format: LIST")
    print("   All nodes:")
    for i, node in enumerate(dce_nodes):
        if isinstance(node, dict):
            print(f"   [{i}] id={node.get('id')}, type={node.get('type')}, output={node.get('output')}")

print("\n" + "="*60)
print("TEST COMPLETE")
print("="*60)

