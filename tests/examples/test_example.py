#!/usr/bin/env python3
"""
MyLogic EDA Tool - Test Examples

Ví dụ cách sử dụng các thuật toán trong MyLogic EDA Tool.
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from frontends.verilog import parse_verilog_file
from core.synthesis.strash import StrashOptimizer
from core.optimization.dce import DCEOptimizer
from core.optimization.cse import CSEOptimizer
from core.synthesis.synthesis_flow import run_complete_synthesis

def example_strash():
    """Ví dụ sử dụng Structural Hashing."""
    print("=" * 50)
    print("STRUCTURAL HASHING (STRASH) EXAMPLE")
    print("=" * 50)
    
    # Parse Verilog file
    netlist = parse_verilog_file("tests/test_data/duplicate_nodes.v")
    print(f"Original netlist: {len(netlist['nodes'])} nodes")
    
    # Apply Strash optimization
    optimizer = StrashOptimizer()
    optimized = optimizer.optimize(netlist)
    print(f"Optimized netlist: {len(optimized['nodes'])} nodes")
    print(f"Removed: {len(netlist['nodes']) - len(optimized['nodes'])} duplicate nodes")
    
    return optimized

def example_dce():
    """Ví dụ sử dụng Dead Code Elimination."""
    print("=" * 50)
    print("DEAD CODE ELIMINATION (DCE) EXAMPLE")
    print("=" * 50)
    
    # Parse Verilog file
    netlist = parse_verilog_file("tests/test_data/dead_code.v")
    print(f"Original netlist: {len(netlist['nodes'])} nodes")
    
    # Apply DCE optimization
    optimizer = DCEOptimizer()
    optimized = optimizer.optimize(netlist, "advanced")
    print(f"Optimized netlist: {len(optimized['nodes'])} nodes")
    print(f"Removed: {len(netlist['nodes']) - len(optimized['nodes'])} dead nodes")
    
    return optimized

def example_cse():
    """Ví dụ sử dụng Common Subexpression Elimination."""
    print("=" * 50)
    print("COMMON SUBEXPRESSION ELIMINATION (CSE) EXAMPLE")
    print("=" * 50)
    
    # Parse Verilog file
    netlist = parse_verilog_file("tests/test_data/common_subexpressions.v")
    print(f"Original netlist: {len(netlist['nodes'])} nodes")
    
    # Apply CSE optimization
    optimizer = CSEOptimizer()
    optimized = optimizer.optimize(netlist)
    print(f"Optimized netlist: {len(optimized['nodes'])} nodes")
    print(f"Removed: {len(netlist['nodes']) - len(optimized['nodes'])} duplicate subexpressions")
    
    return optimized

def example_complete_synthesis():
    """Ví dụ sử dụng Complete Synthesis Flow."""
    print("=" * 50)
    print("COMPLETE SYNTHESIS FLOW EXAMPLE")
    print("=" * 50)
    
    # Parse Verilog file
    netlist = parse_verilog_file("tests/test_data/complex_expression.v")
    print(f"Original netlist: {len(netlist['nodes'])} nodes")
    
    # Run complete synthesis flow
    optimized = run_complete_synthesis(netlist, "standard")
    print(f"Optimized netlist: {len(optimized['nodes'])} nodes")
    print(f"Total reduction: {len(netlist['nodes']) - len(optimized['nodes'])} nodes")
    print(f"Optimization rate: {((len(netlist['nodes']) - len(optimized['nodes'])) / len(netlist['nodes']) * 100):.1f}%")
    
    return optimized

def run_all_examples():
    """Chạy tất cả các ví dụ."""
    print("MYLOGIC EDA TOOL - ALGORITHM EXAMPLES")
    print("=" * 60)
    
    try:
        # Run examples
        example_strash()
        print()
        
        example_dce()
        print()
        
        example_cse()
        print()
        
        example_complete_synthesis()
        print()
        
        print("=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"Error running examples: {e}")
        return False
    
    return True

if __name__ == "__main__":
    run_all_examples()
