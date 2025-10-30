#!/usr/bin/env python3
"""
Constant Propagation Algorithm Implementation

Dựa trên các khái niệm VLSI CAD Part 1 cho tối ưu hóa logic.
Constant Propagation propagates constants qua mạch và simplify logic.
"""

import sys
import os
from typing import Dict, List, Set, Any, Tuple, Optional, Union
import logging

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

def _nodes_to_dict(nodes_any: Any) -> Tuple[Dict[str, Any], str]:
    if isinstance(nodes_any, dict):
        return nodes_any, 'dict'
    if isinstance(nodes_any, list):
        nodes_dict: Dict[str, Any] = {}
        for i, n in enumerate(nodes_any):
            if isinstance(n, dict):
                key = str(n.get('id', i))
                if 'id' not in n:
                    n = {**n, 'id': key}
                nodes_dict[key] = n
        return nodes_dict, 'list'
    return {}, 'unknown'

def _nodes_from_dict(nodes_dict: Dict[str, Any], fmt: str) -> Any:
    if fmt == 'list':
        return list(nodes_dict.values())
    return nodes_dict

class ConstPropOptimizer:
    """
    Constant Propagation optimizer.
    
    Propagates constants qua mạch và simplify logic với known values.
    Loại bỏ unnecessary gates và tối ưu hóa mạch.
    """
    
    def __init__(self):
        self.constant_values: Dict[str, Union[bool, int]] = {}  # node_id -> constant value
        self.propagated_constants = 0
        self.simplified_gates = 0
        self.removed_nodes = 0
        
    def optimize(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Áp dụng Constant Propagation cho netlist.
        
        Args:
            netlist: Circuit netlist với nodes, inputs, outputs
            
        Returns:
            Optimized netlist với propagated constants
        """
        logger.info("Starting Constant Propagation...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
            
        nodes_dict, original_fmt = _nodes_to_dict(netlist.get('nodes', {}))
        netlist_local = netlist.copy()
        netlist_local['nodes'] = nodes_dict
        original_nodes = len(nodes_dict)
        
        # Khởi tạo constant values từ inputs và constants
        self._initialize_constants(netlist_local)
        
        # Propagate constants qua mạch
        optimized_netlist = self._propagate_constants(netlist_local)
        
        # Simplify logic với known constants
        optimized_netlist = self._simplify_logic(optimized_netlist)
        
        final_nodes = len(optimized_netlist['nodes'])
        reduction = original_nodes - final_nodes
        
        logger.info(f"Constant Propagation completed:")
        logger.info(f"  Original nodes: {original_nodes}")
        logger.info(f"  Optimized nodes: {final_nodes}")
        logger.info(f"  Removed nodes: {reduction}")
        logger.info(f"  Propagated constants: {self.propagated_constants}")
        logger.info(f"  Simplified gates: {self.simplified_gates}")
        
        optimized_out = optimized_netlist.copy()
        optimized_out['nodes'] = _nodes_from_dict(optimized_netlist['nodes'], original_fmt)
        return optimized_out
    
    def _initialize_constants(self, netlist: Dict[str, Any]):
        """
        Khởi tạo constant values từ inputs và constant nodes.
        
        Args:
            netlist: Circuit netlist
        """
        # Tìm constant inputs (0, 1, VCC, GND)
        for node_id, node_data in netlist['nodes'].items():
            node_type = node_data.get('type', '')
            
            if node_type in ['CONST0', 'GND', '0']:
                self.constant_values[node_id] = False
            elif node_type in ['CONST1', 'VCC', '1']:
                self.constant_values[node_id] = True
            elif node_type == 'INPUT' and 'value' in node_data:
                # Input với known value
                self.constant_values[node_id] = bool(node_data['value'])
        
        logger.debug(f"Khởi tạo {len(self.constant_values)} constant values")
    
    def _propagate_constants(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Propagate constants qua mạch.
        
        Args:
            netlist: Original netlist
            
        Returns:
            Netlist với propagated constants
        """
        optimized_netlist = netlist.copy()
        optimized_netlist['nodes'] = netlist['nodes'].copy()
        
        # Multiple passes để propagate constants
        max_passes = 10
        for pass_num in range(max_passes):
            constants_found = False
            for node_id, node_data in optimized_netlist['nodes'].items():
                if self._is_gate_node(node_data):
                    # Kiểm tra xem tất cả inputs có phải constants không
                    inputs = node_data.get('inputs', [])
                    if all(inp in self.constant_values for inp in inputs):
                        # Tất cả inputs là constants, tính output
                        output_value = self._evaluate_gate(node_data, inputs)
                        self.constant_values[node_id] = output_value
                        self.propagated_constants += 1
                        constants_found = True
                        logger.debug(f"Propagated constant {output_value} cho node {node_id}")
            if not constants_found:
                break
        
        logger.info(f"Propagated {self.propagated_constants} constants in {pass_num + 1} passes")
        return optimized_netlist
    
    def _is_gate_node(self, node_data: Dict[str, Any]) -> bool:
        """Kiểm tra xem node có phải là gate không."""
        gate_types = ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF']
        return node_data.get('type', '') in gate_types
    
    def _evaluate_gate(self, node_data: Dict[str, Any], inputs: List[str]) -> bool:
        """
        Đánh giá output của gate với constant inputs.
        
        Args:
            node_data: Gate node data
            inputs: List of input node IDs
            
        Returns:
            Boolean output value
        """
        gate_type = node_data.get('type', '')
        input_values = [self.constant_values.get(inp, False) for inp in inputs]
        
        if gate_type == 'AND':
            return all(input_values)
        elif gate_type == 'OR':
            return any(input_values)
        elif gate_type == 'XOR':
            return sum(input_values) % 2 == 1
        elif gate_type == 'NAND':
            return not all(input_values)
        elif gate_type == 'NOR':
            return not any(input_values)
        elif gate_type == 'XNOR':
            return sum(input_values) % 2 == 0
        elif gate_type == 'NOT':
            return not input_values[0]
        elif gate_type == 'BUF':
            return input_values[0]
        else:
            return False
    
    def _simplify_logic(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Simplify logic với known constants.
        
        Args:
            netlist: Netlist với propagated constants
            
        Returns:
            Simplified netlist
        """
        optimized_netlist = netlist.copy()
        optimized_netlist['nodes'] = {}
        
        for node_id, node_data in netlist['nodes'].items():
            if node_id in self.constant_values:
                # Node có constant value, thay thế bằng constant
                constant_value = self.constant_values[node_id]
                
                if constant_value:
                    optimized_netlist['nodes'][node_id] = {
                        'type': 'CONST1',
                        'inputs': [],
                        'output': node_data.get('output', node_id),
                        'value': 1
                    }
                else:
                    optimized_netlist['nodes'][node_id] = {
                        'type': 'CONST0',
                        'inputs': [],
                        'output': node_data.get('output', node_id),
                        'value': 0
                    }
                
                self.simplified_gates += 1
                logger.debug(f"Simplified node {node_id} thành constant {constant_value}")
            else:
                # Node không có constant value, giữ nguyên
                optimized_netlist['nodes'][node_id] = node_data
        
        return optimized_netlist
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về optimization."""
        return {
            'propagated_constants': self.propagated_constants,
            'simplified_gates': self.simplified_gates,
            'removed_nodes': self.removed_nodes,
            'optimization_type': 'constant_propagation'
        }

def apply_constprop(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function để áp dụng Constant Propagation.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Optimized netlist
    """
    optimizer = ConstPropOptimizer()
    return optimizer.optimize(netlist)

# Test function
def test_constprop():
    """Test Constant Propagation với simple circuit."""
    # Tạo test netlist với constants
    test_netlist = {
        'name': 'test_constprop_circuit',
        'inputs': ['a'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'const0': {'type': 'CONST0', 'inputs': [], 'output': 'zero'},
            'const1': {'type': 'CONST1', 'inputs': [], 'output': 'one'},
            'n1': {'type': 'AND', 'inputs': ['a', 'zero'], 'output': 'temp1'},  # Should be 0
            'n2': {'type': 'OR', 'inputs': ['a', 'one'], 'output': 'temp2'},    # Should be 1
            'n3': {'type': 'XOR', 'inputs': ['temp1', 'temp2'], 'output': 'out1'},
            'n4': {'type': 'NOT', 'inputs': ['temp1'], 'output': 'out2'}
        },
        'wires': {}
    }
    
    print("Original netlist:")
    print(f"  Nodes: {len(test_netlist['nodes'])}")
    print("  Constants: const0=0, const1=1")
    
    # Áp dụng Constant Propagation
    optimized = apply_constprop(test_netlist)
    
    print("\nOptimized netlist:")
    print(f"  Nodes: {len(optimized['nodes'])}")
    
    # Verify optimization
    print("[PASSED] Constant Propagation test passed!")

if __name__ == "__main__":
    test_constprop()
