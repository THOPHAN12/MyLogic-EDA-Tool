#!/usr/bin/env python3
"""
Test Complete Flow: Synthesis → Optimization → Technology Mapping

Test để đảm bảo complete flow chạy đúng cả 3 bước.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.complete_flow import run_complete_flow


def test_complete_flow_basic():
    """Test complete flow với netlist đơn giản."""
    print("=" * 70)
    print("TEST 1: Complete Flow - Basic")
    print("=" * 70)
    
    # Create test netlist
    test_netlist = {
        'name': 'test_and_gate',
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
            optimization_level="standard",
            techmap_strategy="area_optimal",
            enable_optimization=True,
            enable_techmap=True
        )
        
        # Check synthesis results
        assert 'synthesis' in results, "Missing synthesis results"
        assert 'aig' in results['synthesis'], "Missing AIG in synthesis results"
        assert results['synthesis']['aig'].count_nodes() > 0, "AIG should have nodes"
        
        # Check optimization results
        assert 'optimization' in results, "Missing optimization results"
        assert results['optimization']['enabled'] == True, "Optimization should be enabled"
        assert 'aig' in results['optimization'], "Missing optimized AIG"
        
        # Check techmap results
        assert 'techmap' in results, "Missing techmap results"
        assert results['techmap']['enabled'] == True, "Techmap should be enabled"
        assert 'results' in results['techmap'], "Missing techmap results"
        
        print("\n[PASS] TEST 1 PASSED: Complete flow works correctly")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_flow_no_optimization():
    """Test complete flow với optimization disabled."""
    print("\n" + "=" * 70)
    print("TEST 2: Complete Flow - Without Optimization")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_or_gate',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'OR', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'AND', 'inputs': ['temp1', 'c'], 'output': 'out'},
        },
        'wires': {}
    }
    
    try:
        results = run_complete_flow(
            test_netlist,
            optimization_level="standard",
            techmap_strategy="area_optimal",
            enable_optimization=False,
            enable_techmap=True
        )
        
        assert results['optimization']['enabled'] == False, "Optimization should be disabled"
        assert 'aig' in results['optimization'], "Should still have AIG (from synthesis)"
        
        print("\n[PASS] TEST 2 PASSED: Complete flow works without optimization")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_flow_no_techmap():
    """Test complete flow với techmap disabled."""
    print("\n" + "=" * 70)
    print("TEST 3: Complete Flow - Without Techmap")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_xor_gate',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'XOR', 'inputs': ['a', 'b'], 'output': 'out'},
        },
        'wires': {}
    }
    
    try:
        results = run_complete_flow(
            test_netlist,
            optimization_level="standard",
            enable_optimization=True,
            enable_techmap=False
        )
        
        assert results['techmap']['enabled'] == False, "Techmap should be disabled"
        
        print("\n[PASS] TEST 3 PASSED: Complete flow works without techmap")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_flow_optimization_levels():
    """Test complete flow với các optimization levels khác nhau."""
    print("\n" + "=" * 70)
    print("TEST 4: Complete Flow - Different Optimization Levels")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_complex',
        'inputs': ['a', 'b', 'c', 'd'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'OR', 'inputs': ['c', 'd'], 'output': 'temp2'},
            'n3': {'type': 'XOR', 'inputs': ['temp1', 'temp2'], 'output': 'out1'},
            'n4': {'type': 'AND', 'inputs': ['temp1', 'temp2'], 'output': 'out2'},
        },
        'wires': {}
    }
    
    levels = ['basic', 'standard', 'aggressive']
    results_all = []
    
    try:
        for level in levels:
            print(f"\nTesting with optimization level: {level}")
            results = run_complete_flow(
                test_netlist,
                optimization_level=level,
                techmap_strategy="area_optimal",
                enable_optimization=True,
                enable_techmap=False  # Disable techmap for faster testing
            )
            results_all.append((level, results))
            
            assert 'optimization' in results, f"Missing optimization for level {level}"
            assert results['optimization']['enabled'] == True, f"Optimization should be enabled for {level}"
        
        print("\n[PASS] TEST 4 PASSED: All optimization levels work correctly")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 4 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_complete_flow_techmap_strategies():
    """Test complete flow với các techmap strategies khác nhau."""
    print("\n" + "=" * 70)
    print("TEST 5: Complete Flow - Different Techmap Strategies")
    print("=" * 70)
    
    test_netlist = {
        'name': 'test_multi_gate',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out'},
        },
        'wires': {}
    }
    
    strategies = ['area_optimal', 'delay_optimal', 'balanced']
    
    try:
        for strategy in strategies:
            print(f"\nTesting with techmap strategy: {strategy}")
            results = run_complete_flow(
                test_netlist,
                optimization_level="basic",  # Use basic for faster testing
                techmap_strategy=strategy,
                enable_optimization=False,  # Disable optimization for faster testing
                enable_techmap=True
            )
            
            assert 'techmap' in results, f"Missing techmap for strategy {strategy}"
            assert results['techmap']['enabled'] == True, f"Techmap should be enabled for {strategy}"
            assert 'results' in results['techmap'], f"Missing techmap results for {strategy}"
        
        print("\n[PASS] TEST 5 PASSED: All techmap strategies work correctly")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] TEST 5 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("COMPLETE FLOW AUTOMATED TESTS")
    print("=" * 70)
    
    tests = [
        ("Basic Complete Flow", test_complete_flow_basic),
        ("Complete Flow without Optimization", test_complete_flow_no_optimization),
        ("Complete Flow without Techmap", test_complete_flow_no_techmap),
        ("Different Optimization Levels", test_complete_flow_optimization_levels),
        ("Different Techmap Strategies", test_complete_flow_techmap_strategies),
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
