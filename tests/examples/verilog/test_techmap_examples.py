#!/usr/bin/env python3
"""
Test Technology Mapping với các examples thực tế.

Kiểm tra technology mapping hoạt động với synthesized netlists từ examples.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis
from core.technology_mapping.technology_mapping import (
    TechnologyLibrary, LibraryCell, TechnologyMapper, LogicNode,
    create_standard_library
)
from core.technology_mapping.library_loader import load_library

CHECK = "[OK]"
CROSS = "[X]"


def convert_netlist_to_logic_network(netlist, library_path=None):
    """Convert netlist nodes to LogicNodes for technology mapping."""
    # Try to load from techlibs first, fallback to standard library
    if library_path:
        try:
            library = load_library(library_path)
            print(f"  [OK] Loaded library from: {library_path} ({len(library.cells)} cells)")
        except Exception as e:
            print(f"  [WARNING] Failed to load {library_path}: {e}")
            print(f"  [INFO] Using standard library instead")
            library = create_standard_library()
    else:
        # Try default techlibs location
        default_lib = project_root / "techlibs" / "asic" / "standard_cells.json"
        if default_lib.exists():
            try:
                library = load_library(str(default_lib))
                print(f"  [OK] Loaded library from techlibs: {default_lib} ({len(library.cells)} cells)")
            except Exception as e:
                print(f"  [WARNING] Failed to load {default_lib}: {e}")
                print(f"  [INFO] Using standard library instead")
                library = create_standard_library()
        else:
            library = create_standard_library()
            print(f"  [INFO] Using standard library (techlibs not found)")
    
    mapper = TechnologyMapper(library)
    
    nodes_data = netlist.get('nodes', [])
    if isinstance(nodes_data, list):
        for node_data in nodes_data:
            node_type = node_data.get('type', '')
            node_id = node_data.get('id', '')
            
            # Skip non-gate nodes
            if node_type not in ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF']:
                continue
            
            # Get inputs
            fanins = node_data.get('fanins', [])
            inputs = [f[0] for f in fanins] if fanins else []
            
            # Create function string based on number of inputs
            # For gates with >2 inputs, try to decompose to 2-input gates
            if node_type == 'NOT':
                function = f"NOT(A)"
            elif node_type == 'BUF':
                function = f"BUF(A)"
            elif len(inputs) == 1:
                # Single input gate
                if node_type == 'NOT':
                    function = f"NOT(A)"
                elif node_type == 'BUF':
                    function = f"BUF(A)"
                else:
                    continue
            elif len(inputs) == 2:
                # 2-input gate - most common
                function = f"{node_type}(A,B)"
            elif len(inputs) >= 3:
                # For 3+ inputs, use 3-input version if available
                # Otherwise will need decomposition (future enhancement)
                function = f"{node_type}(A,B,C)"
            else:
                continue
            
            # Create LogicNode
            logic_node = LogicNode(node_id, function, inputs, node_id)
            mapper.add_logic_node(logic_node)
    
    return mapper


def test_techmap_example(example_path: str, strategy: str = "area_optimal"):
    """Test technology mapping với một example file."""
    result = {
        'file': os.path.basename(example_path),
        'status': 'UNKNOWN',
        'error': None,
        'original_nodes': 0,
        'mappable_nodes': 0,
        'mapped_nodes': 0,
        'success_rate': 0.0,
        'total_area': 0.0,
        'total_delay': 0.0
    }
    
    try:
        print(f"\n[1/3] Parsing: {result['file']}")
        
        # Parse Verilog
        netlist = parse_verilog(example_path)
        original_nodes = len(netlist.get('nodes', []))
        result['original_nodes'] = original_nodes
        
        if original_nodes == 0:
            result['status'] = 'SKIPPED'
            result['error'] = 'No nodes found after parsing'
            return result
        
        print(f"  {CHECK} Parsed: {original_nodes} nodes")
        
        # Synthesize
        print(f"[2/3] Running synthesis...")
        synthesized = run_complete_synthesis(netlist, "basic")
        
        # Convert to logic network
        print(f"[3/3] Running technology mapping ({strategy})...")
        # Try to load from techlibs
        library_path = project_root / "techlibs" / "asic" / "standard_cells.json"
        mapper = convert_netlist_to_logic_network(synthesized, str(library_path) if library_path.exists() else None)
        mappable_nodes = len(mapper.logic_network)
        result['mappable_nodes'] = mappable_nodes
        
        if mappable_nodes == 0:
            result['status'] = 'SKIPPED'
            result['error'] = 'No mappable nodes found'
            print(f"  {CHECK} No mappable nodes (may contain only arithmetic operations)")
            return result
        
        # Perform mapping
        mapping_results = mapper.perform_technology_mapping(strategy)
        
        result['mapped_nodes'] = mapping_results['mapped_nodes']
        result['success_rate'] = mapping_results['mapping_success_rate']
        result['total_area'] = mapping_results.get('total_area', 0.0)
        result['total_delay'] = mapping_results.get('total_delay', 0.0)
        
        # Verify results
        assert mapping_results['mapped_nodes'] > 0, "Should map at least one node"
        assert mapping_results['mapping_success_rate'] > 0, "Mapping success rate should be positive"
        
        print(f"  {CHECK} Mapped {result['mapped_nodes']}/{mappable_nodes} nodes ({result['success_rate']*100:.1f}%)")
        print(f"  {CHECK} Total area: {result['total_area']:.2f}, Delay: {result['total_delay']:.2f}")
        
        result['status'] = 'PASSED'
        
    except AssertionError as e:
        result['status'] = 'FAILED'
        result['error'] = f"Assertion error: {str(e)}"
        print(f"  {CROSS} FAILED: {result['error']}")
        
    except Exception as e:
        result['status'] = 'FAILED'
        result['error'] = f"{type(e).__name__}: {str(e)}"
        print(f"  {CROSS} FAILED: {result['error']}")
    
    return result


def test_all_examples_techmap(strategy: str = "area_optimal"):
    """Test technology mapping với tất cả examples."""
    examples_dir = project_root / "examples"
    
    if not examples_dir.exists():
        print(f"ERROR: Examples directory not found: {examples_dir}")
        return []
    
    verilog_files = list(examples_dir.glob("*.v"))
    
    if not verilog_files:
        print(f"ERROR: No .v files found in {examples_dir}")
        return []
    
    print("=" * 70)
    print(" TESTING TECHNOLOGY MAPPING WITH EXAMPLES")
    print("=" * 70)
    print(f"Examples directory: {examples_dir}")
    print(f"Found {len(verilog_files)} Verilog files")
    print(f"Mapping strategy: {strategy}")
    print("=" * 70)
    
    results = []
    passed = 0
    failed = 0
    skipped = 0
    
    for verilog_file in sorted(verilog_files):
        print(f"\n{'=' * 70}")
        print(f"Testing: {verilog_file.name}")
        print('=' * 70)
        
        result = test_techmap_example(str(verilog_file), strategy)
        results.append(result)
        
        if result['status'] == 'PASSED':
            passed += 1
        elif result['status'] == 'FAILED':
            failed += 1
        else:
            skipped += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print(" TECHNOLOGY MAPPING TEST SUMMARY")
    print("=" * 70)
    print(f"Total files: {len(verilog_files)}")
    print(f"  {CHECK} Passed: {passed}")
    print(f"  {CROSS} Failed: {failed}")
    print(f"  [SKIP] Skipped: {skipped}")
    print("=" * 70)
    
    # Print detailed results
    if results:
        print("\nDETAILED RESULTS:")
        print("-" * 70)
        for result in results:
            status_symbol = CHECK if result['status'] == 'PASSED' else CROSS if result['status'] == 'FAILED' else "[SKIP]"
            print(f"{status_symbol} {result['file']}")
            if result['status'] == 'PASSED':
                print(f"   Nodes: {result['original_nodes']} total, {result['mappable_nodes']} mappable")
                print(f"   Mapped: {result['mapped_nodes']} ({result['success_rate']*100:.1f}% success)")
                print(f"   Area: {result['total_area']:.2f}, Delay: {result['total_delay']:.2f}")
            elif result['error']:
                print(f"   Error: {result['error']}")
        print("-" * 70)
    
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test technology mapping with examples")
    parser.add_argument("--strategy", "-s",
                       choices=["area_optimal", "delay_optimal", "balanced"],
                       default="area_optimal",
                       help="Mapping strategy")
    parser.add_argument("--file", "-f",
                       help="Test specific file only")
    
    args = parser.parse_args()
    
    if args.file:
        result = test_techmap_example(args.file, args.strategy)
        if result['status'] == 'PASSED':
            print(f"\n{CHECK} TEST PASSED")
            sys.exit(0)
        else:
            print(f"\n{CROSS} TEST FAILED: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    else:
        results = test_all_examples_techmap(args.strategy)
        
        if any(r['status'] == 'FAILED' for r in results):
            sys.exit(1)
        elif any(r['status'] == 'PASSED' for r in results):
            sys.exit(0)
        else:
            sys.exit(2)  # All skipped

