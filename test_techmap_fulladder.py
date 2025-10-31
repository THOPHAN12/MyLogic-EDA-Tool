#!/usr/bin/env python3
"""Test technology mapping với full adder sau khi sửa DCE"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from parsers import parse_verilog
from core.synthesis.strash import apply_strash
from core.optimization.dce import apply_dce
from core.technology_mapping.technology_mapping import TechnologyMapper, LogicNode, create_standard_library

print("="*60)
print("TECHNOLOGY MAPPING TEST - FULL ADDER")
print("="*60)

# Parse and synthesize
netlist = parse_verilog('examples/full_adder.v')
netlist = apply_strash(netlist)
netlist = apply_dce(netlist, 'standard')

print(f"\nNodes after DCE: {len(netlist.get('nodes', []))}")
nodes = netlist.get('nodes', [])
if isinstance(nodes, dict):
    nodes = list(nodes.values())

# Show nodes
print("\nNodes to map:")
for i, node_data in enumerate(nodes):
    if isinstance(node_data, dict):
        node_type = node_data.get('type', 'UNKNOWN')
        node_id = node_data.get('id', f'node_{i}')
        fanins = node_data.get('fanins', [])
        inputs = node_data.get('inputs', [])
        
        # Extract input signals
        input_signals = []
        if fanins:
            for fanin in fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                    input_signals.append(str(fanin[0]))
        elif inputs:
            input_signals = [str(inp) for inp in inputs]
        
        print(f"  {i+1}. {node_id}: {node_type} with inputs {input_signals}")

# Create mapper
library = create_standard_library()
mapper = TechnologyMapper(library)

# Convert to LogicNodes
for i, node_data in enumerate(nodes):
    if not isinstance(node_data, dict):
        continue
    
    node_id = node_data.get('id', f'node_{i}')
    node_type = node_data.get('type', 'UNKNOWN')
    
    # Get inputs/fanins
    inputs = node_data.get('inputs', [])
    fanins = node_data.get('fanins', [])
    
    # Extract input signals
    input_signals = []
    if fanins:
        for fanin in fanins:
            if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                input_signals.append(str(fanin[0]))
    elif inputs:
        input_signals = [str(inp) for inp in inputs]
    
    # Create function
    if len(input_signals) >= 2:
        function = f"{node_type}({','.join(input_signals[:2])})"
    elif len(input_signals) == 1:
        function = f"{node_type}({input_signals[0]})"
    else:
        function = node_type
    
    output = node_data.get('output', node_id)
    logic_node = LogicNode(str(node_id), function, input_signals, str(output))
    mapper.add_logic_node(logic_node)

print(f"\nLogic nodes created: {len(mapper.logic_network)}")

# Run mapping
print("\nRunning technology mapping (area optimal)...")
results = mapper.perform_technology_mapping("area_optimal")

# Print report
mapper.print_mapping_report(results)

# Check cell usage
stats = mapper.get_mapping_statistics()
print(f"\nCell Usage Summary:")
print(f"  Unique cell types used: {stats['unique_cells_used']}")
print(f"  Total cell instances: {stats['mapped_nodes']}")
print(f"  Cells: {stats['cell_usage']}")

print("\n" + "="*60)

