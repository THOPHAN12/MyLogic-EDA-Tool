#!/usr/bin/env python3
"""
MyLogic EDA Tool - Complete Test Suite Runner

Chạy tất cả các test để kiểm tra các thuật toán hoạt động đúng cách.
"""

import sys
import os
import time
from typing import List, Tuple, Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_algorithm_tests() -> Dict[str, bool]:
    """Chạy tất cả các test thuật toán."""
    print("=" * 60)
    print("MYLOGIC EDA TOOL - COMPLETE TEST SUITE")
    print("=" * 60)
    print(f"Test started at: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    test_results = {}
    
    # Test Structural Hashing (Strash)
    print("1. Testing Structural Hashing (Strash)...")
    try:
        from tests.algorithms.test_strash import run_strash_tests
        test_results['strash'] = run_strash_tests()
    except Exception as e:
        print(f"   [ERROR] Strash test failed: {e}")
        test_results['strash'] = False
    
    print()
    
    # Test Dead Code Elimination (DCE)
    print("2. Testing Dead Code Elimination (DCE)...")
    try:
        from tests.algorithms.test_dce import run_dce_tests
        test_results['dce'] = run_dce_tests()
    except Exception as e:
        print(f"   [ERROR] DCE test failed: {e}")
        test_results['dce'] = False
    
    print()
    
    # Test Common Subexpression Elimination (CSE)
    print("3. Testing Common Subexpression Elimination (CSE)...")
    try:
        from tests.algorithms.test_cse import run_cse_tests
        test_results['cse'] = run_cse_tests()
    except Exception as e:
        print(f"   [ERROR] CSE test failed: {e}")
        test_results['cse'] = False
    
    print()
    
    # Test Complete Synthesis Flow
    print("4. Testing Complete Synthesis Flow...")
    try:
        from tests.algorithms.test_synthesis_flow import run_synthesis_flow_tests
        test_results['synthesis_flow'] = run_synthesis_flow_tests()
    except Exception as e:
        print(f"   [ERROR] Synthesis Flow test failed: {e}")
        test_results['synthesis_flow'] = False
    
    print()
    
    return test_results

def print_test_summary(test_results: Dict[str, bool]):
    """In tóm tắt kết quả test."""
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests
    
    print(f"Total test suites: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
    print()
    
    print("Detailed Results:")
    print("-" * 30)
    for test_name, result in test_results.items():
        status = "PASS" if result else "FAIL"
        print(f"  {test_name.upper():15} : {status}")
    
    print()
    
    if failed_tests == 0:
        print("ALL TESTS PASSED! MyLogic EDA Tool algorithms are working correctly.")
    else:
        print(f"WARNING: {failed_tests} test suite(s) failed. Please check the errors above.")
    
    print(f"Test completed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

def run_individual_test(test_name: str):
    """Chạy một test cụ thể."""
    test_functions = {
        'strash': 'tests.algorithms.test_strash.run_strash_tests',
        'dce': 'tests.algorithms.test_dce.run_dce_tests',
        'cse': 'tests.algorithms.test_cse.run_cse_tests',
        'synthesis': 'tests.algorithms.test_synthesis_flow.run_synthesis_flow_tests'
    }
    
    if test_name not in test_functions:
        print(f"Unknown test: {test_name}")
        print(f"Available tests: {', '.join(test_functions.keys())}")
        return False
    
    try:
        module_path, function_name = test_functions[test_name].rsplit('.', 1)
        module = __import__(module_path, fromlist=[function_name])
        function = getattr(module, function_name)
        return function()
    except Exception as e:
        print(f"Error running {test_name} test: {e}")
        return False

def main():
    """Main test runner."""
    import argparse
    
    parser = argparse.ArgumentParser(description="MyLogic EDA Tool Test Runner")
    parser.add_argument("--test", "-t", help="Run specific test (strash, dce, cse, synthesis)")
    parser.add_argument("--all", "-a", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    
    if args.test:
        print(f"Running individual test: {args.test}")
        success = run_individual_test(args.test)
        if success:
            print(f"PASSED: {args.test} test passed!")
        else:
            print(f"FAILED: {args.test} test failed!")
    elif args.all or (not args.test and not args.all):
        # Run all tests by default
        test_results = run_algorithm_tests()
        print_test_summary(test_results)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
