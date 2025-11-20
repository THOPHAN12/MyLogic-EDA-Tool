#!/usr/bin/env python3
"""
Test script for examples directory.

Tự động test tất cả các file .v trong thư mục examples:
- Parse Verilog files
- Run synthesis flow
- Verify results
"""

import os
import sys
import json
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        import io
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
            sys.stderr.reconfigure(encoding='utf-8')
        else:
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
            sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass

# Use ASCII-safe symbols
CHECK = "[OK]"
CROSS = "[X]"
SKIP = "[SKIP]"

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis

def test_example_file(example_path: str, optimization_level: str = "basic"):
    """
    Test một file example.
    
    Args:
        example_path: Đường dẫn đến file .v
        optimization_level: Mức độ optimization (basic, standard, aggressive)
        
    Returns:
        dict với kết quả test
    """
    result = {
        'file': example_path,
        'status': 'UNKNOWN',
        'error': None,
        'original_nodes': 0,
        'final_nodes': 0,
        'reduction': 0,
        'reduction_percent': 0.0
    }
    
    try:
        # 1. Parse Verilog
        print(f"\n[1/3] Parsing: {example_path}")
        netlist = parse_verilog(example_path)
        original_nodes = len(netlist.get('nodes', []))
        result['original_nodes'] = original_nodes
        
        if original_nodes == 0:
            result['status'] = 'SKIPPED'
            result['error'] = 'No nodes found after parsing'
            return result
        
        print(f"  {CHECK} Parsed successfully: {original_nodes} nodes")
        
        # 2. Run synthesis
        print(f"[2/3] Running synthesis ({optimization_level})...")
        synthesized = run_complete_synthesis(netlist, optimization_level)
        final_nodes = len(synthesized.get('nodes', []))
        result['final_nodes'] = final_nodes
        result['reduction'] = original_nodes - final_nodes
        result['reduction_percent'] = (result['reduction'] / original_nodes * 100) if original_nodes > 0 else 0.0
        
        print(f"  {CHECK} Synthesis completed: {original_nodes} -> {final_nodes} nodes")
        
        # 3. Verify results
        print(f"[3/3] Verifying results...")
        
        # Verify netlist structure
        assert isinstance(synthesized, dict), "Synthesized netlist must be a dict"
        assert 'nodes' in synthesized, "Synthesized netlist must have 'nodes'"
        assert 'inputs' in synthesized, "Synthesized netlist must have 'inputs'"
        assert 'outputs' in synthesized, "Synthesized netlist must have 'outputs'"
        
        # Verify outputs are preserved
        original_outputs = set(netlist.get('outputs', []))
        final_outputs = set(synthesized.get('outputs', []))
        assert original_outputs == final_outputs, f"Outputs mismatch: {original_outputs} vs {final_outputs}"
        
        print(f"  {CHECK} All checks passed!")
        
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

def test_all_examples(optimization_level: str = "basic"):
    """
    Test tất cả các file .v trong thư mục examples.
    
    Args:
        optimization_level: Mức độ optimization
    """
    examples_dir = project_root / "examples"
    
    if not examples_dir.exists():
        print(f"ERROR: Examples directory not found: {examples_dir}")
        return []
    
    # Tìm tất cả file .v
    verilog_files = list(examples_dir.glob("*.v"))
    
    if not verilog_files:
        print(f"ERROR: No .v files found in {examples_dir}")
        return []
    
    print("=" * 70)
    print(" TESTING EXAMPLES")
    print("=" * 70)
    print(f"Examples directory: {examples_dir}")
    print(f"Found {len(verilog_files)} Verilog files")
    print(f"Optimization level: {optimization_level}")
    print("=" * 70)
    
    results = []
    passed = 0
    failed = 0
    skipped = 0
    
    for verilog_file in sorted(verilog_files):
        print(f"\n{'=' * 70}")
        print(f"Testing: {verilog_file.name}")
        print('=' * 70)
        
        result = test_example_file(str(verilog_file), optimization_level)
        results.append(result)
        
        if result['status'] == 'PASSED':
            passed += 1
        elif result['status'] == 'FAILED':
            failed += 1
        else:
            skipped += 1
    
    result = test_example_file(str(verilog_file), optimization_level)
    results.append(result)
    
    if result['status'] == 'PASSED':
        passed += 1
    elif result['status'] == 'FAILED':
        failed += 1
    else:
        skipped += 1
    
    # Print summary
    print("\n" + "=" * 70)
    print(" TEST SUMMARY")
    print("=" * 70)
    print(f"Total files: {len(verilog_files)}")
    print(f"  {CHECK} Passed: {passed}")
    print(f"  {CROSS} Failed: {failed}")
    print(f"  {SKIP} Skipped: {skipped}")
    print("=" * 70)
    
    # Print detailed results
    if results:
        print("\nDETAILED RESULTS:")
        print("-" * 70)
        for result in results:
            status_symbol = CHECK if result['status'] == 'PASSED' else CROSS if result['status'] == 'FAILED' else SKIP
            file_name = os.path.basename(result['file'])
            print(f"{status_symbol} {file_name}")
            if result['status'] == 'PASSED':
                print(f"   Nodes: {result['original_nodes']} -> {result['final_nodes']} "
                      f"({result['reduction_percent']:.1f}% reduction)")
            elif result['error']:
                print(f"   Error: {result['error']}")
        print("-" * 70)
    
    return results

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test examples directory")
    parser.add_argument("--level", "-l", 
                       choices=["basic", "standard", "aggressive"],
                       default="basic",
                       help="Optimization level")
    parser.add_argument("--file", "-f",
                       help="Test specific file only")
    
    args = parser.parse_args()
    
    if args.file:
        # Test single file
        if not os.path.exists(args.file):
            print(f"ERROR: File not found: {args.file}")
            sys.exit(1)
        
        result = test_example_file(args.file, args.level)
        if result['status'] == 'PASSED':
            print(f"\n{CHECK} TEST PASSED")
            sys.exit(0)
        else:
            print(f"\n{CROSS} TEST FAILED: {result.get('error', 'Unknown error')}")
            sys.exit(1)
    else:
        # Test all examples
        results = test_all_examples(args.level)
        
        # Exit code based on results
        if any(r['status'] == 'FAILED' for r in results):
            sys.exit(1)
        elif any(r['status'] == 'PASSED' for r in results):
            sys.exit(0)
        else:
            sys.exit(2)  # All skipped
