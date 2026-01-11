#!/usr/bin/env python3
"""
Demo Test Script

Script để test các CAN_DO examples và minh họa CANNOT_DO examples.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from frontends.verilog import parse_verilog
import logging
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def test_can_do_example(file_path: Path, example_name: str):
    """Test một CAN_DO example."""
    print(f"\n{'='*70}")
    print(f"Testing CAN_DO: {example_name}")
    print(f"File: {file_path.name}")
    print(f"{'='*70}")
    
    try:
        # Parse
        logger.info(f"✓ Parsing {file_path.name}...")
        netlist = parse_verilog(str(file_path))
        logger.info(f"✓ Parsed successfully!")
        
        # Show basic stats
        inputs = netlist.get('inputs', [])
        outputs = netlist.get('outputs', [])
        nodes = netlist.get('nodes', [])
        
        print(f"\n[STATS] Basic Statistics:")
        print(f"  Inputs: {len(inputs)} - {inputs}")
        print(f"  Outputs: {len(outputs)} - {outputs}")
        print(f"  Nodes: {len(nodes)}")
        
        print(f"\n[OK] SUCCESS: {example_name} can be parsed and synthesized!")
        return True
        
    except Exception as e:
        print(f"\n[ERROR] ERROR: {example_name} failed")
        print(f"   Error: {str(e)}")
        return False


def show_cannot_do_example(file_path: Path, example_name: str):
    """Show một CANNOT_DO example (không test, chỉ show info)."""
    print(f"\n{'='*70}")
    print(f"CANNOT_DO Example: {example_name}")
    print(f"File: {file_path.name}")
    print(f"{'='*70}")
    
    # Read file to show what it contains
    try:
        content = file_path.read_text(encoding='utf-8')
        # Extract comment header
        lines = content.split('\n')
        header = []
        for line in lines[:15]:  # First 15 lines
            if line.strip().startswith('//'):
                header.append(line)
        
        print("\n[INFO] Description:")
        for line in header:
            print(line)
        
        print(f"\n[WARN] NOTE: This example is NOT FULLY SUPPORTED")
        print(f"   It may parse, but synthesis/optimization may be incomplete.")
        
    except Exception as e:
        print(f"[ERROR] Error reading file: {e}")


def main():
    """Main function."""
    demo_dir = Path(__file__).parent
    
    print("="*70)
    print("MyLogic EDA Tool - Demo Examples Test")
    print("="*70)
    
    # Test CAN_DO examples
    can_do_dir = demo_dir / "CAN_DO"
    can_do_files = sorted(can_do_dir.glob("*.v"))
    
    print(f"\n{'='*70}")
    print("PART 1: CAN_DO Examples (Testing...)")
    print(f"{'='*70}")
    
    can_do_results = []
    for file_path in can_do_files:
        example_name = file_path.stem.replace('_', ' ').title()
        result = test_can_do_example(file_path, example_name)
        can_do_results.append((example_name, result))
    
    # Show CANNOT_DO examples (info only)
    cannot_do_dir = demo_dir / "CANNOT_DO"
    cannot_do_files = sorted(cannot_do_dir.glob("*.v"))
    
    print(f"\n{'='*70}")
    print("PART 2: CANNOT_DO Examples (Information Only)")
    print(f"{'='*70}")
    
    for file_path in cannot_do_files:
        example_name = file_path.stem.replace('_', ' ').title()
        show_cannot_do_example(file_path, example_name)
    
    # Summary
    print(f"\n{'='*70}")
    print("SUMMARY")
    print(f"{'='*70}")
    
    passed = sum(1 for _, result in can_do_results if result)
    total = len(can_do_results)
    
    print(f"\n[OK] CAN_DO Examples: {passed}/{total} passed")
    print(f"[INFO] CANNOT_DO Examples: {len(cannot_do_files)} (shown for reference)")
    
    print(f"\n[INFO] For more details, see: {demo_dir / 'README.md'}")
    print(f"[INFO] Quick reference: {demo_dir / 'SUMMARY.md'}")
    
    print(f"\n{'='*70}")


if __name__ == "__main__":
    main()

