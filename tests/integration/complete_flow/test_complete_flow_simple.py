#!/usr/bin/env python3
"""
Simple Test Complete Flow: Test basic functionality only

Test đơn giản để verify complete flow hoạt động đúng.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.complete_flow import run_complete_flow


def test_synthesis_only():
    """Test chỉ synthesis."""
    print("=" * 70)
    print("TEST 1: Synthesis Only")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_and',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'out'},
        },
        'wires': {}
    }
    
    try:
        results = run_complete_flow(
            test_netlist,
            enable_optimization=False,
            enable_techmap=False
        )
        
        assert 'synthesis' in results, "Missing synthesis results"
        assert 'aig' in results['synthesis'], "Missing AIG"
        assert results['synthesis']['aig'].count_nodes() > 0, "AIG should have nodes"
        
        print("\n[PASS] TEST 1: Synthesis only works correctly")
        print(f"  AIG nodes: {results['synthesis']['aig'].count_nodes()}")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 1: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_synthesis_optimization():
    """Test synthesis + optimization."""
    print("\n" + "=" * 70)
    print("TEST 2: Synthesis + Optimization")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_simple',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'out'},
        },
        'wires': {}
    }
    
    try:
        results = run_complete_flow(
            test_netlist,
            optimization_level="basic",
            enable_optimization=True,
            enable_techmap=False
        )
        
        assert 'synthesis' in results, "Missing synthesis"
        assert 'optimization' in results, "Missing optimization"
        assert results['optimization']['enabled'] == True, "Optimization should be enabled"
        assert 'aig' in results['optimization'], "Missing optimized AIG"
        
        print("\n[PASS] TEST 2: Synthesis + Optimization works correctly")
        print(f"  Synthesis AIG nodes: {results['synthesis']['stats']['aig_nodes']}")
        if 'stats' in results['optimization'] and 'nodes_after' in results['optimization']['stats']:
            print(f"  Optimized AIG nodes: {results['optimization']['stats']['nodes_after']}")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 2: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run tests."""
    print("\n" + "=" * 70)
    print("COMPLETE FLOW SIMPLE TESTS")
    print("=" * 70)
    
    tests = [
        ("Synthesis Only", test_synthesis_only),
        ("Synthesis + Optimization", test_synthesis_optimization),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"\n[FAIL] Test '{test_name}' raised exception: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    # Summary
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    print(f"Total tests: {len(tests)}")
    print(f"Passed: {passed} [PASS]")
    print(f"Failed: {failed} [FAIL]")
    print("=" * 70)
    
    if failed == 0:
        print("\n[SUCCESS] ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n[WARNING] {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())


