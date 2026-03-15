#!/usr/bin/env python3
"""
Script để test tất cả các examples trong examples/

Chạy tất cả test cases và tạo report.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis

# Color codes
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}\n")

def test_file(file_path, category):
    """Test một file và trả về kết quả."""
    try:
        # Parse
        netlist = parse_verilog(str(file_path))
        original_nodes = len(netlist.get('nodes', []))
        
        # Synthesize
        synthesized = run_complete_synthesis(netlist)
        final_nodes = len(synthesized.get('nodes', []))
        
        reduction = original_nodes - final_nodes
        reduction_pct = (reduction / original_nodes * 100) if original_nodes > 0 else 0
        
        return {
            'status': 'PASS',
            'module': netlist.get('name', '?'),
            'original_nodes': original_nodes,
            'final_nodes': final_nodes,
            'reduction': reduction,
            'reduction_pct': reduction_pct
        }
    except Exception as e:
        return {
            'status': 'FAIL',
            'error': str(e),
            'module': '?',
            'original_nodes': 0,
            'final_nodes': 0,
            'reduction': 0,
            'reduction_pct': 0
        }

def main():
    """Main function."""
    print_header("Examples Test Suite")
    
    examples_dir = project_root / "examples"
    results = {}
    
    # Test từng category
    categories = [
        "01_parameters",
        "02_always_blocks",
        "03_generate_blocks",
        "04_case_statements",
        "05_bit_manipulation",
        "06_memory_arrays",
        "07_functions_tasks",
        "08_module_instantiation",
        "09_optimization",
        "10_arithmetic",
        "11_bitwise",
        "12_logical",
        "13_comparison",
        "14_shift_operations",
        "15_comprehensive"
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for category in categories:
        category_dir = examples_dir / category
        if not category_dir.exists():
            continue
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}Testing: {category}{Colors.RESET}")
        print("-" * 70)
        
        category_results = []
        
        # Tìm tất cả .v files trong category
        for v_file in category_dir.glob("*.v"):
            total_tests += 1
            result = test_file(v_file, category)
            category_results.append({
                'file': v_file.name,
                'result': result
            })
            
            if result['status'] == 'PASS':
                passed_tests += 1
                print(f"  {Colors.GREEN}[PASS]{Colors.RESET} {v_file.name}")
                print(f"    Module: {result['module']}, Nodes: {result['original_nodes']} -> {result['final_nodes']} ({result['reduction_pct']:.1f}% reduction)")
            else:
                failed_tests += 1
                print(f"  {Colors.RED}[FAIL]{Colors.RESET} {v_file.name}")
                error_msg = result.get('error', 'Unknown error')
                # Remove Unicode characters that cause encoding issues
                error_msg = error_msg.encode('ascii', 'ignore').decode('ascii')
                print(f"    Error: {error_msg}")
        
        results[category] = category_results
    
    # Summary
    print_header("TEST SUMMARY")
    
    print(f"Total tests: {total_tests}")
    print(f"{Colors.GREEN}Passed: {passed_tests}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed_tests}{Colors.RESET}")
    print(f"Success rate: {(passed_tests/total_tests*100) if total_tests > 0 else 0:.1f}%")
    
    print(f"\n{Colors.BOLD}Results by Category:{Colors.RESET}")
    for category, category_results in results.items():
        if not category_results:
            continue
        
        passed = sum(1 for r in category_results if r['result']['status'] == 'PASS')
        total = len(category_results)
        
        status_color = Colors.GREEN if passed == total else Colors.YELLOW
        print(f"  {category:30} {status_color}{passed}/{total} passed{Colors.RESET}")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Unexpected error: {e}{Colors.RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

