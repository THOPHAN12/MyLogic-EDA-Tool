#!/usr/bin/env python3
"""
Basic test script for MyLogic EDA Tool
Tests core functionality on Linux
"""

import sys
import os

# Add project root to path (go up 2 levels from tests/unit/)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

def test_imports():
    """Test basic imports"""
    print("=" * 60)
    print("Test 1: Import Modules")
    print("=" * 60)
    
    try:
        from constants import PROJECT_VERSION, PROJECT_NAME
        print(f"✅ Constants: {PROJECT_NAME} v{PROJECT_VERSION}")
    except Exception as e:
        print(f"❌ Constants import failed: {e}")
        return False
    
    try:
        import core
        print("✅ Core module imported")
    except Exception as e:
        print(f"❌ Core import failed: {e}")
        return False
    
    try:
        from core.optimization import dce, cse, constprop, balance
        from core.synthesis import strash
        print("✅ Optimization modules imported")
    except Exception as e:
        print(f"❌ Optimization import failed: {e}")
        return False
    
    try:
        from core.simulation import arithmetic_simulation, logic_simulation
        print("✅ Simulation modules imported")
    except Exception as e:
        print(f"❌ Simulation import failed: {e}")
        return False
    
    try:
        from frontends import unified_verilog
        print("✅ Frontend modules imported")
    except Exception as e:
        print(f"❌ Frontend import failed: {e}")
        return False
    
    return True

def test_examples():
    """Test example files exist"""
    print("\n" + "=" * 60)
    print("Test 2: Example Files")
    print("=" * 60)
    
    examples = [
        "examples/full_adder.v",
        "examples/arithmetic_operations.v",
        "examples/priority_encoder.v",
        "examples/comprehensive_combinational.v"
    ]
    
    all_exist = True
    for example in examples:
        if os.path.exists(example):
            size = os.path.getsize(example)
            print(f"✅ {example} ({size} bytes)")
        else:
            print(f"❌ {example} - NOT FOUND")
            all_exist = False
    
    return all_exist

def test_verilog_parser():
    """Test Verilog parser"""
    print("\n" + "=" * 60)
    print("Test 3: Verilog Parser")
    print("=" * 60)
    
    try:
        from frontends.unified_verilog import parse_verilog
        
        # Test with simple example
        test_file = "examples/full_adder.v"
        if os.path.exists(test_file):
            result = parse_verilog(test_file)
            if result and 'name' in result:
                print(f"✅ Parsed {test_file} successfully")
                print(f"   Module: {result.get('name', 'N/A')}")
                print(f"   Inputs: {len(result.get('inputs', []))}")
                print(f"   Outputs: {len(result.get('outputs', []))}")
                return True
            else:
                print(f"⚠️  Parser returned invalid result")
                return False
        else:
            print(f"⚠️  Test file not found: {test_file}")
            return False
    except Exception as e:
        print(f"❌ Parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_simulation():
    """Test simulation engine"""
    print("\n" + "=" * 60)
    print("Test 4: Simulation Engine")
    print("=" * 60)
    
    try:
        from core.simulation.arithmetic_simulation import VectorValue, vector_add
        
        # Create simple test
        a = VectorValue(3, 4)  # value=3, width=4
        b = VectorValue(5, 4)  # value=5, width=4
        result = vector_add(a, b)
        
        print("✅ VectorValue and vector_add imported")
        print(f"   Test: {a.to_int()} + {b.to_int()} = {result.to_int()}")
        
        if result.to_int() == 8:
            print("✅ Basic arithmetic test passed (3 + 5 = 8)")
            return True
        else:
            print(f"⚠️  Arithmetic test failed: expected 8, got {result.to_int()}")
            return False
    except Exception as e:
        print(f"❌ Simulation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("MyLogic EDA Tool - Basic Test Suite")
    print("=" * 60)
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print()
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Examples", test_examples()))
    results.append(("Parser", test_verilog_parser()))
    results.append(("Simulation", test_simulation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Project is working correctly on Linux.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please check errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

