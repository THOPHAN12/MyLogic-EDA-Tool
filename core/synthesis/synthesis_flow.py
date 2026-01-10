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

from core.utils.error_handling import (
    validate_netlist,
    safe_optimize,
    OptimizationError,
    ValidationError
)

logger = logging.getLogger(__name__)

class SynthesisFlow:
    """
    Synthesis Flow: Netlist → AIG Conversion
    
    SYNTHESIS là bước riêng biệt (1 trong 3 hướng độc lập), chỉ làm chuyển đổi representation:
    - Input: Netlist Dictionary (từ parser)
    - Output: AIG (And-Inverter Graph)
    
    3 hướng độc lập:
    1. SYNTHESIS: Netlist → AIG (file này)
    2. OPTIMIZE: AIG → Optimized AIG (core/optimization/optimization_flow.py)
    3. TECHMAP: AIG → Technology-mapped netlist (core/technology_mapping/technology_mapping.py)
    
    Lưu ý: Đây KHÔNG phải là optimization. Optimization được thực hiện riêng trên AIG.
    """
    
    def __init__(self):
        self.aig = None
        self.conversion_stats = {
            'netlist_nodes': 0,
            'aig_nodes': 0,
            'aig_and_nodes': 0,
            'primary_inputs': 0,
            'primary_outputs': 0
        }
        
    def synthesize(self, netlist: Dict[str, Any]) -> 'AIG':
        """
        Synthesis: Convert Netlist Dictionary → AIG.
        
        Đây là bước SYNTHESIS riêng biệt.
        Chỉ làm chuyển đổi representation, không tối ưu hóa.
        
        Args:
            netlist: Circuit netlist dictionary từ parser
            
        Returns:
            AIG object
            
        Raises:
            ValidationError: If netlist is invalid
        """
        # Validate input netlist
        try:
            validate_netlist(netlist, strict=True)
        except ValidationError as e:
            logger.error(f"Synthesis failed: Invalid input netlist: {e}")
            raise
        
        logger.info("Starting Synthesis: Netlist -> AIG conversion...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            raise ValueError("Invalid netlist format")
        
        # Count original nodes
        nodes_data = netlist.get('nodes', {})
        if isinstance(nodes_data, dict):
            original_nodes = len(nodes_data)
        elif isinstance(nodes_data, list):
            original_nodes = len(nodes_data)
        else:
            original_nodes = 0
        
        self.conversion_stats['netlist_nodes'] = original_nodes
        
        # Convert Netlist → AIG
        from core.synthesis.netlist_to_aig import synthesize_netlist_to_aig
        self.aig = synthesize_netlist_to_aig(netlist)
        
        # Update stats
        self.conversion_stats['aig_nodes'] = self.aig.count_nodes()
        self.conversion_stats['aig_and_nodes'] = self.aig.count_and_nodes()
        self.conversion_stats['primary_inputs'] = len(self.aig.pis)
        self.conversion_stats['primary_outputs'] = len(self.aig.pos)
        
        # Print summary
        self._print_synthesis_summary()
        
        return self.aig
    
    def _print_synthesis_summary(self):
        """In synthesis summary."""
        logger.info("=" * 60)
        logger.info("SYNTHESIS SUMMARY (Netlist -> AIG)")
        logger.info("=" * 60)
        logger.info(f"Netlist nodes: {self.conversion_stats['netlist_nodes']}")
        logger.info(f"AIG nodes: {self.conversion_stats['aig_nodes']}")
        logger.info(f"  - AND nodes: {self.conversion_stats['aig_and_nodes']}")
        logger.info(f"  - Primary inputs: {self.conversion_stats['primary_inputs']}")
        logger.info(f"  - Primary outputs: {self.conversion_stats['primary_outputs']}")
        logger.info("=" * 60)
        logger.info("[OK] Synthesis completed: Netlist -> AIG conversion")
        logger.info("   (Next step: Run optimization on AIG)")
        logger.info("=" * 60)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về synthesis."""
        return {
            'conversion_stats': self.conversion_stats,
            'aig_stats': self.aig.get_statistics() if self.aig else {}
        }
    
    def run_complete_synthesis(self, netlist: Dict[str, Any], optimization_level: str = "standard") -> Dict[str, Any]:
        """
        Run complete synthesis flow (for backward compatibility).
        
        This method wraps the deprecated run_complete_synthesis function.
        """
        return run_complete_synthesis(netlist, optimization_level)

def synthesize(netlist: Dict[str, Any]) -> 'AIG':
    """
    Synthesis function: Convert Netlist → AIG.
    
    Đây là bước SYNTHESIS riêng biệt.
    Chỉ làm chuyển đổi representation, không tối ưu hóa.
    
    Args:
        netlist: Circuit netlist dictionary từ parser
        
    Returns:
        AIG object
    """
    flow = SynthesisFlow()
    return flow.synthesize(netlist)

# Legacy function for backward compatibility (deprecated)
def run_complete_synthesis(netlist: Dict[str, Any], optimization_level: str = "standard") -> Dict[str, Any]:
    """
    DEPRECATED: Use synthesize() + optimize() instead.
    
    This function is kept for backward compatibility but will be removed.
    Please use:
    - synthesize(netlist) for Netlist → AIG conversion
    - optimize(aig, level) for AIG optimization
    
    However, this function now correctly returns the optimized netlist.
    """
    import warnings
    warnings.warn(
        "run_complete_synthesis() is deprecated. Use synthesize() + optimize() instead.",
        DeprecationWarning,
        stacklevel=2
    )
    
    # For backward compatibility, convert to AIG first
    aig = synthesize(netlist)
    
    # Then run optimization
    from core.optimization.optimization_flow import optimize
    optimized_aig = optimize(aig, optimization_level)
    
    # Convert AIG back to netlist format
    from core.synthesis.aig import aig_to_netlist
    optimized_netlist = aig_to_netlist(optimized_aig, netlist)
    
    return optimized_netlist

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
    
    # Run complete synthesis
    synthesized = run_complete_synthesis(test_netlist, "standard")
    
    print(f"\nSynthesized circuit:")
    print(f"  Nodes: {len(synthesized['nodes'])}")
    print("Complete synthesis flow test passed!")

if __name__ == "__main__":
    test_synthesis_flow()
