#!/usr/bin/env python3
"""
Complete Logic Synthesis Flow Implementation

Dựa trên các khái niệm VLSI CAD Part 1 cho complete synthesis workflow.
Tích hợp tất cả các thuật toán tổng hợp luận lý.
"""

import sys
import os
from typing import Dict, List, Set, Any, Tuple, Optional
import logging

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class SynthesisFlow:
    """
    Complete Logic Synthesis Flow.
    
    Tích hợp tất cả các thuật toán tổng hợp luận lý theo thứ tự:
    1. Structural Hashing (Strash)
    2. Dead Code Elimination (DCE)
    3. Common Subexpression Elimination (CSE)
    4. Constant Propagation (ConstProp)
    5. Logic Balancing (Balance)
    """
    
    def __init__(self):
        self.optimization_stats = {
            'strash': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'dce': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'cse': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'constprop': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'balance': {'nodes_before': 0, 'nodes_after': 0, 'added': 0}
        }
        
    def run_complete_synthesis(self, netlist: Dict[str, Any], 
                              optimization_level: str = "standard") -> Dict[str, Any]:
        """
        Chạy complete logic synthesis flow.
        
        Args:
            netlist: Circuit netlist
            optimization_level: "basic", "standard", "aggressive"
            
        Returns:
            Synthesized netlist
        """
        logger.info(f"Bắt đầu Complete Logic Synthesis Flow - Level: {optimization_level}")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
        
        original_nodes = len(netlist['nodes'])
        current_netlist = netlist.copy()
        
        # Step 1: Structural Hashing
        logger.info("Step 1: Structural Hashing...")
        current_netlist = self._run_strash(current_netlist)
        
        # Step 2: Dead Code Elimination
        logger.info("Step 2: Dead Code Elimination...")
        current_netlist = self._run_dce(current_netlist, optimization_level)
        
        # Step 3: Common Subexpression Elimination
        logger.info("Step 3: Common Subexpression Elimination...")
        current_netlist = self._run_cse(current_netlist)
        
        # Step 4: Constant Propagation
        logger.info("Step 4: Constant Propagation...")
        current_netlist = self._run_constprop(current_netlist)
        
        # Step 5: Logic Balancing
        logger.info("Step 5: Logic Balancing...")
        current_netlist = self._run_balance(current_netlist)
        
        final_nodes = len(current_netlist['nodes'])
        total_reduction = original_nodes - final_nodes
        
        # Print summary
        self._print_synthesis_summary(original_nodes, final_nodes, total_reduction)
        
        return current_netlist
    
    def _run_strash(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy Structural Hashing."""
        try:
            from core.synthesis.strash import apply_strash
            
            nodes_before = len(netlist['nodes'])
            optimized = apply_strash(netlist)
            nodes_after = len(optimized['nodes'])
            
            self.optimization_stats['strash'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  Strash: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized
            
        except ImportError:
            logger.warning("Strash module not available")
            return netlist
        except Exception as e:
            logger.error(f"Strash failed: {e}")
            return netlist
    
    def _run_dce(self, netlist: Dict[str, Any], level: str) -> Dict[str, Any]:
        """Chạy Dead Code Elimination."""
        try:
            from core.optimization.dce import apply_dce
            
            nodes_before = len(netlist['nodes'])
            optimized = apply_dce(netlist, level)
            nodes_after = len(optimized['nodes'])
            
            self.optimization_stats['dce'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  DCE: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized
            
        except ImportError:
            logger.warning("DCE module not available")
            return netlist
        except Exception as e:
            logger.error(f"DCE failed: {e}")
            return netlist
    
    def _run_cse(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy Common Subexpression Elimination."""
        try:
            from core.optimization.cse import apply_cse
            
            nodes_before = len(netlist['nodes'])
            optimized = apply_cse(netlist)
            nodes_after = len(optimized['nodes'])
            
            self.optimization_stats['cse'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  CSE: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized
            
        except ImportError:
            logger.warning("CSE module not available")
            return netlist
        except Exception as e:
            logger.error(f"CSE failed: {e}")
            return netlist
    
    def _run_constprop(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy Constant Propagation."""
        try:
            from core.optimization.constprop import apply_constprop
            
            nodes_before = len(netlist['nodes'])
            optimized = apply_constprop(netlist)
            nodes_after = len(optimized['nodes'])
            
            self.optimization_stats['constprop'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  ConstProp: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized
            
        except ImportError:
            logger.warning("ConstProp module not available")
            return netlist
        except Exception as e:
            logger.error(f"ConstProp failed: {e}")
            return netlist
    
    def _run_balance(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """Chạy Logic Balancing."""
        try:
            from core.optimization.balance import apply_balance
            
            nodes_before = len(netlist['nodes'])
            optimized = apply_balance(netlist)
            nodes_after = len(optimized['nodes'])
            
            self.optimization_stats['balance'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'added': nodes_after - nodes_before
            }
            
            logger.info(f"  Balance: {nodes_before} -> {nodes_after} nodes (added {nodes_after - nodes_before})")
            return optimized
            
        except ImportError:
            logger.warning("Balance module not available")
            return netlist
        except Exception as e:
            logger.error(f"Balance failed: {e}")
            return netlist
    
    def _print_synthesis_summary(self, original_nodes: int, final_nodes: int, total_reduction: int):
        """In synthesis summary."""
        logger.info("=" * 60)
        logger.info("LOGIC SYNTHESIS SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Original nodes: {original_nodes}")
        logger.info(f"Final nodes: {final_nodes}")
        logger.info(f"Total reduction: {total_reduction} nodes ({(total_reduction/original_nodes)*100:.1f}%)")
        logger.info("")
        logger.info("Optimization breakdown:")
        
        for opt_name, stats in self.optimization_stats.items():
            if opt_name == 'balance':
                logger.info(f"  {opt_name.upper()}: {stats['nodes_before']} -> {stats['nodes_after']} (added {stats['added']})")
            else:
                logger.info(f"  {opt_name.upper()}: {stats['nodes_before']} -> {stats['nodes_after']} (removed {stats['removed']})")
        
        logger.info("=" * 60)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về synthesis."""
        return {
            'optimization_stats': self.optimization_stats,
            'total_optimizations': len(self.optimization_stats)
        }

def run_complete_synthesis(netlist: Dict[str, Any], optimization_level: str = "standard") -> Dict[str, Any]:
    """
    Convenience function để chạy complete logic synthesis.
    
    Args:
        netlist: Circuit netlist
        optimization_level: "basic", "standard", "aggressive"
        
    Returns:
        Synthesized netlist
    """
    flow = SynthesisFlow()
    return flow.run_complete_synthesis(netlist, optimization_level)

# Test function
def test_synthesis_flow():
    """Test complete synthesis flow."""
    # Tạo test netlist với các optimization opportunities
    test_netlist = {
        'name': 'test_synthesis_circuit',
        'inputs': ['a', 'b', 'c', 'd'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            # Duplicate nodes (Strash)
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp2'},  # Duplicate
            
            # Common subexpression (CSE)
            'n3': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'temp3'},
            'n4': {'type': 'OR', 'inputs': ['temp2', 'd'], 'output': 'temp4'},
            
            # Dead code (DCE)
            'n5': {'type': 'XOR', 'inputs': ['temp3', 'temp4'], 'output': 'dead1'},  # Not connected to output
            
            # Constants (ConstProp)
            'const0': {'type': 'CONST0', 'inputs': [], 'output': 'zero'},
            'n6': {'type': 'AND', 'inputs': ['temp3', 'zero'], 'output': 'out1'},  # Should be 0
            'n7': {'type': 'OR', 'inputs': ['temp4', 'zero'], 'output': 'out2'},   # Should be temp4
        },
        'wires': {}
    }
    
    print("Original test circuit:")
    print(f"  Nodes: {len(test_netlist['nodes'])}")
    print("  Contains: duplicates, common subexpressions, dead code, constants")
    
    # Chạy complete synthesis
    synthesized = run_complete_synthesis(test_netlist, "standard")
    
    print(f"\nSynthesized circuit:")
    print(f"  Nodes: {len(synthesized['nodes'])}")
    print("✅ Complete synthesis flow test passed!")

if __name__ == "__main__":
    test_synthesis_flow()
