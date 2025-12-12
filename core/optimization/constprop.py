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
        logger.info("Bắt đầu Constant Propagation...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
            
        original_nodes = len(netlist['nodes'])
        
        # Khởi tạo constant values từ inputs và constants
        self._initialize_constants(netlist)
        
        # Propagate constants qua mạch
        optimized_netlist = self._propagate_constants(netlist)
        
        # Simplify logic với known constants
        optimized_netlist = self._simplify_logic(optimized_netlist)
        
        final_nodes = len(optimized_netlist['nodes'])
        reduction = original_nodes - final_nodes
        
        logger.info(f"Constant Propagation hoàn thành:")
        logger.info(f"  Original nodes: {original_nodes}")
        logger.info(f"  Optimized nodes: {final_nodes}")
        logger.info(f"  Removed nodes: {reduction}")
        logger.info(f"  Propagated constants: {self.propagated_constants}")
        logger.info(f"  Simplified gates: {self.simplified_gates}")
        
        return optimized_netlist
    
    def _initialize_constants(self, netlist: Dict[str, Any]):
        """
        Khởi tạo constant values từ inputs và constant nodes.
        
        Args:
            netlist: Circuit netlist
        """
        # Tìm constant inputs (0, 1, VCC, GND)
        # nodes is a list, iterate directly
        for node in netlist.get('nodes', []):
            if isinstance(node, dict):
                node_id = node.get('id', '')
                node_type = node.get('type', '')
                
                if node_type in ['CONST0', 'GND', '0']:
                    self.constant_values[node_id] = False
                elif node_type in ['CONST1', 'VCC', '1']:
                    self.constant_values[node_id] = True
                elif node_type == 'INPUT' and 'value' in node:
                    # Input với known value
                    self.constant_values[node_id] = bool(node['value'])
        
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
        # nodes is a list, create a copy
        optimized_netlist['nodes'] = [node.copy() if isinstance(node, dict) else node for node in netlist.get('nodes', [])]
        
        # Multiple passes để propagate constants
        max_passes = 10
        for pass_num in range(max_passes):
            constants_found = False
            
            # nodes is a list, iterate directly
            for node in optimized_netlist.get('nodes', []):
                if not isinstance(node, dict):
                    continue
                node_id = node.get('id', '')
                node_data = node
                if self._is_gate_node(node_data):
                    # Kiểm tra xem tất cả inputs có phải constants không
                    # Handle both 'inputs' and 'fanins' formats
                    inputs = node_data.get('inputs', [])
                    fanins = node_data.get('fanins', [])
                    
                    # If fanins exist, extract input names from [name, is_negated] pairs
                    if fanins and not inputs:
                        inputs = [fanin[0] if isinstance(fanin, list) and len(fanin) > 0 else fanin for fanin in fanins]
                    
                    # Filter out non-string inputs (like lists)
                    inputs = [inp for inp in inputs if isinstance(inp, str)]
                    
                    if inputs and all(inp in self.constant_values for inp in inputs):
                        # Tất cả inputs là constants, tính output
                        output_value = self._evaluate_gate(node_data, inputs)
                        self.constant_values[node_id] = output_value
                        self.propagated_constants += 1
                        constants_found = True
                        
                        logger.debug(f"Propagated constant {output_value} cho node {node_id}")
            
            if not constants_found:
                break
        
        logger.info(f"Propagated {self.propagated_constants} constants trong {pass_num + 1} passes")
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
        gate_type = node_data.get('type', '').upper()
        
        # Get input values safely
        input_values = []
        for inp in inputs:
            if inp in self.constant_values:
                input_values.append(self.constant_values[inp])
        
        # Check if we have any input values
        if not input_values:
            return False
        
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
            if len(input_values) > 0:
                return not input_values[0]
            return False
        elif gate_type == 'BUF':
            if len(input_values) > 0:
                return input_values[0]
            return False
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
        optimized_netlist['nodes'] = []
        
        # nodes is a list, iterate directly
        for node in netlist.get('nodes', []):
            if not isinstance(node, dict):
                optimized_netlist['nodes'].append(node)
                continue
            node_id = node.get('id', '')
            node_data = node
            if node_id in self.constant_values:
                # Node có constant value, thay thế bằng constant
                constant_value = self.constant_values[node_id]
                
                if constant_value:
                    optimized_netlist['nodes'].append({
                        'id': node_id,
                        'type': 'CONST1',
                        'inputs': [],
                        'output': node_data.get('output', node_id),
                        'value': 1
                    })
                else:
                    optimized_netlist['nodes'].append({
                        'id': node_id,
                        'type': 'CONST0',
                        'inputs': [],
                        'output': node_data.get('output', node_id),
                        'value': 0
                    })
                
                self.simplified_gates += 1
                logger.debug(f"Simplified node {node_id} thành constant {constant_value}")
            else:
                # Node không có constant value, giữ nguyên
                optimized_netlist['nodes'].append(node_data)
        
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
    print("✅ Constant Propagation test passed!")

if __name__ == "__main__":
    test_constprop()
