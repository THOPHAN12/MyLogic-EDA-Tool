#!/usr/bin/env python3
"""Debug ConstProp issue"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers import parse_verilog
from core.synthesis.strash import apply_strash
from core.optimization.dce import apply_dce
from core.optimization.constprop import apply_constprop

print("="*60)
print("DEBUG CONSTPROP ISSUE")
print("="*60)

# Parse and synthesize
netlist = parse_verilog('examples/full_adder.v')
print(f"\n1. After parse: {len(netlist.get('nodes', []))} nodes")

netlist = apply_strash(netlist)
print(f"2. After strash: {len(netlist.get('nodes', {}))} nodes")

netlist = apply_dce(netlist, 'standard')
nodes_after_dce = netlist.get('nodes', [])
if isinstance(nodes_after_dce, dict):
    nodes_after_dce = list(nodes_after_dce.values())
print(f"3. After DCE: {len(nodes_after_dce)} nodes")
print("\n   Nodes after DCE:")
for i, n in enumerate(nodes_after_dce):
    if isinstance(n, dict):
        print(f"   [{i}] id={n.get('id')}, type={n.get('type')}")
        print(f"       fanins={n.get('fanins', [])}")
        print(f"       inputs={n.get('inputs', [])}")

# Now run ConstProp
print("\n4. Running ConstProp...")
netlist_constprop = apply_constprop(netlist)

nodes_after_constprop = netlist_constprop.get('nodes', [])
if isinstance(nodes_after_constprop, dict):
    nodes_after_constprop = list(nodes_after_constprop.values())
print(f"   After ConstProp: {len(nodes_after_constprop)} nodes")
print("\n   Nodes after ConstProp:")
for i, n in enumerate(nodes_after_constprop):
    if isinstance(n, dict):
        print(f"   [{i}] id={n.get('id')}, type={n.get('type')}")

print("\n" + "="*60)

