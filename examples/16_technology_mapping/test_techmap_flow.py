#!/usr/bin/env python3
"""
Demo Technology Mapping Flow

Script này minh họa toàn bộ flow của technology mapping:
1. Parse Verilog
2. Synthesis
3. Technology Mapping
4. Report
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis
from core.technology_mapping.technology_mapping import (
    TechnologyMapper, 
    load_library_from_file,
    create_standard_library,
    LogicNode
)

def demo_techmap_flow():
    """Demo technology mapping flow."""
    print("=" * 70)
    print(" TECHNOLOGY MAPPING FLOW DEMO")
    print("=" * 70)
    
    # Step 1: Parse Verilog
    print("\n[1/5] Parsing Verilog...")
    verilog_file = project_root / "examples" / "16_technology_mapping" / "test_techmap.v"
    netlist = parse_verilog(str(verilog_file))
    print(f"  Module: {netlist.get('name')}")
    print(f"  Nodes: {len(netlist.get('nodes', []))}")
    print(f"  Inputs: {netlist.get('inputs', [])}")
    print(f"  Outputs: {netlist.get('outputs', [])}")
    
    # Step 2: Synthesis
    print("\n[2/5] Running Synthesis...")
    optimized = run_complete_synthesis(netlist)
    print(f"  Optimized nodes: {len(optimized.get('nodes', []))}")
    
    # Step 3: Load Library
    print("\n[3/5] Loading Technology Library...")
    # Use standard library (có đầy đủ logic gates)
    # cells.lib chỉ có DFF cells, không có logic gates
    library = create_standard_library()
    print(f"  Using standard library: {library.name}")
    print(f"  Total cells: {len(library.cells)}")
    print(f"  Unique functions: {len(library.function_map)}")
    print(f"  Sample cells: {list(library.cells.keys())[:5]}")
    
    # Step 4: Create Mapper and Add Nodes
    print("\n[4/5] Creating Technology Mapper...")
    mapper = TechnologyMapper(library)
    
    # Convert netlist nodes to LogicNode (giống như mylogic_shell.py)
    nodes = optimized.get('nodes', {})
    node_count = 0
    
    # Normalize nodes to list if dict
    if isinstance(nodes, dict):
        nodes_list = list(nodes.values())
    else:
        nodes_list = nodes if isinstance(nodes, list) else []
    
    # Create LogicNodes from netlist
    for i, node_data in enumerate(nodes_list):
        if not isinstance(node_data, dict):
            continue
        
        node_id = node_data.get('id', f'node_{i}')
        node_type = node_data.get('type', 'UNKNOWN')
        
        # Get inputs/fanins
        inputs = node_data.get('inputs', [])
        fanins = node_data.get('fanins', [])
        
        # Extract input signals from fanins (fanins format: [['signal', False], ...])
        input_signals = []
        if fanins:
            for fanin in fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                    input_signals.append(str(fanin[0]))
                elif isinstance(fanin, str):
                    input_signals.append(fanin)
        elif inputs:
            input_signals = [str(inp) for inp in inputs]
        
        # Skip non-logic nodes
        if node_type in ['BUF', 'CONST0', 'CONST1', 'INPUT', 'OUTPUT']:
            continue
        
        # Create function string based on node type and inputs
        if len(input_signals) >= 2:
            # 2+ input gates: AND(A,B), OR(A,B), XOR(A,B), etc.
            function = f"{node_type}({','.join(input_signals[:2])})"  # Use first 2 inputs
        elif len(input_signals) == 1:
            # Single input: NOT(A), BUF(A)
            if node_type == 'NOT':
                function = f"NOT({input_signals[0]})"
            else:
                function = f"{node_type}({input_signals[0]})"
        else:
            # No inputs - skip
            continue
        
        # Get output
        output = node_data.get('output') or node_data.get('name') or str(node_id)
        
        # Create LogicNode
        logic_node = LogicNode(str(node_id), function, input_signals, str(output))
        mapper.add_logic_node(logic_node)
        node_count += 1
    
    print(f"  Added {node_count} logic nodes to mapper")
    
    # Step 5: Perform Mapping
    print("\n[5/5] Performing Technology Mapping...")
    
    strategies = ['area_optimal', 'delay_optimal', 'balanced']
    for strategy in strategies:
        print(f"\n  Strategy: {strategy}")
        results = mapper.perform_technology_mapping(strategy)
        print(f"    Mapped: {results['mapped_nodes']}/{results['total_nodes']} nodes")
        print(f"    Success rate: {results['mapping_success_rate']*100:.1f}%")
        if 'total_area' in results:
            print(f"    Total area: {results['total_area']:.2f}")
        if 'total_delay' in results:
            print(f"    Total delay: {results['total_delay']:.2f}")
        
        # Reset for next strategy
        for node in mapper.logic_network.values():
            node.mapped_cell = None
            node.mapping_cost = float('inf')
    
    # Print detailed report for balanced strategy
    print("\n" + "=" * 70)
    print(" DETAILED MAPPING REPORT (Balanced Strategy)")
    print("=" * 70)
    results = mapper.perform_technology_mapping("balanced")
    mapper.print_mapping_report(results)
    
    print("\n" + "=" * 70)
    print(" TECHNOLOGY MAPPING FLOW COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    try:
        demo_techmap_flow()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

