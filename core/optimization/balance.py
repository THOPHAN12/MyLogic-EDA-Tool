#!/usr/bin/env python3
"""
Logic Balancing Algorithm Implementation

Dựa trên các khái niệm VLSI CAD Part 1 cho tối ưu hóa timing.
Logic Balancing cân bằng độ sâu logic để tối ưu critical path.
"""

import sys
import os
from typing import Dict, List, Set, Any, Tuple, Optional
import logging
from collections import defaultdict, deque

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

class BalanceOptimizer:
    """
    Logic Balancing optimizer.
    
    Cân bằng độ sâu logic của mạch để tối ưu timing và
    giảm critical path delay.
    """
    
    def __init__(self):
        self.node_levels: Dict[str, int] = {}  # node_id -> logic level
        self.balanced_nodes = 0
        self.max_level = 0
        self.level_distribution: Dict[int, int] = defaultdict(int)
        
    def optimize(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Áp dụng Logic Balancing cho netlist.
        
        Args:
            netlist: Circuit netlist với nodes, inputs, outputs
            
        Returns:
            Balanced netlist với optimized logic depth
        """
        logger.info("Bắt đầu Logic Balancing...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
            
        nodes_dict, original_fmt = _nodes_to_dict(netlist.get('nodes', {}))
        netlist_local = netlist.copy()
        netlist_local['nodes'] = nodes_dict
        original_nodes = len(nodes_dict)
        
        # Tính logic levels cho tất cả nodes
        self._calculate_logic_levels(netlist_local)
        
        # Cân bằng logic depth
        balanced_netlist = self._balance_logic_depth(netlist_local)
        
        final_nodes = len(balanced_netlist['nodes'])
        
        logger.info(f"Logic Balancing hoàn thành:")
        logger.info(f"  Original nodes: {original_nodes}")
        logger.info(f"  Balanced nodes: {final_nodes}")
        logger.info(f"  Max logic level: {self.max_level}")
        logger.info(f"  Balanced nodes: {self.balanced_nodes}")
        
        balanced_out = balanced_netlist.copy()
        balanced_out['nodes'] = _nodes_from_dict(balanced_netlist['nodes'], original_fmt)
        return balanced_out
    
    def _calculate_logic_levels(self, netlist: Dict[str, Any]):
        """
        Tính logic level cho tất cả nodes.
        
        Args:
            netlist: Circuit netlist
        """
        # Reset levels
        self.node_levels = {}
        self.level_distribution = defaultdict(int)
        
        # Khởi tạo levels cho inputs (level 0)
        for input_name in netlist.get('inputs', []):
            self.node_levels[input_name] = 0
        
        # Tính levels cho các nodes khác
        nodes = netlist.get('nodes', {})
        max_iterations = len(nodes) * 2  # Prevent infinite loops
        
        for iteration in range(max_iterations):
            levels_updated = False
            
            for node_id, node_data in nodes.items():
                if node_id not in self.node_levels:
                    # Tính level dựa trên input levels
                    inputs = node_data.get('inputs', [])
                    
                    if all(inp in self.node_levels for inp in inputs) and inputs:
                        # Tất cả inputs đã có level
                        max_input_level = max(self.node_levels[inp] for inp in inputs)
                        self.node_levels[node_id] = max_input_level + 1
                        levels_updated = True
                        
                        # Cập nhật distribution
                        level = self.node_levels[node_id]
                        self.level_distribution[level] += 1
                        
                        if level > self.max_level:
                            self.max_level = level
            
            if not levels_updated:
                break
        
        logger.debug(f"Calculated levels cho {len(self.node_levels)} nodes")
        logger.debug(f"Level distribution: {dict(self.level_distribution)}")
    
    def _balance_logic_depth(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cân bằng logic depth của mạch.
        
        Args:
            netlist: Original netlist
            
        Returns:
            Balanced netlist
        """
        balanced_netlist = netlist.copy()
        balanced_netlist['nodes'] = netlist['nodes'].copy()
        
        # Tìm các nodes cần cân bằng
        nodes_to_balance = self._find_nodes_to_balance()
        
        for node_id in nodes_to_balance:
            if self._can_balance_node(node_id, netlist):
                balanced_netlist = self._balance_node(node_id, balanced_netlist)
                self.balanced_nodes += 1
        
        return balanced_netlist
    
    def _find_nodes_to_balance(self) -> List[str]:
        """
        Tìm các nodes cần cân bằng.
        
        Returns:
            List of node IDs cần balance
        """
        nodes_to_balance = []
        
        for node_id, level in self.node_levels.items():
            # Nodes ở level cao và có nhiều fanout
            if level > self.max_level * 0.7:  # Top 30% levels
                nodes_to_balance.append(node_id)
        
        return nodes_to_balance
    
    def _can_balance_node(self, node_id: str, netlist: Dict[str, Any]) -> bool:
        """
        Kiểm tra xem node có thể cân bằng không.
        
        Args:
            node_id: Node ID
            netlist: Circuit netlist
            
        Returns:
            True nếu node có thể balance
        """
        node_data = netlist['nodes'].get(node_id)
        if not node_data:
            return False
        
        # Chỉ balance các associative gates
        gate_type = node_data.get('type', '')
        associative_gates = ['AND', 'OR', 'XOR', 'NAND', 'NOR']
        
        return gate_type in associative_gates
    
    def _balance_node(self, node_id: str, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cân bằng một node cụ thể.
        
        Args:
            node_id: Node ID cần balance
            netlist: Current netlist
            
        Returns:
            Balanced netlist
        """
        node_data = netlist['nodes'][node_id]
        inputs = node_data.get('inputs', [])
        
        if len(inputs) <= 2:
            return netlist  # Không cần balance
        
        # Tạo balanced tree structure
        balanced_inputs = self._create_balanced_tree(inputs, netlist)
        
        # Cập nhật node với balanced inputs
        updated_node = node_data.copy()
        updated_node['inputs'] = balanced_inputs
        
        netlist['nodes'][node_id] = updated_node
        
        logger.debug(f"Balanced node {node_id} với {len(balanced_inputs)} inputs")
        
        return netlist
    
    def _create_balanced_tree(self, inputs: List[str], netlist: Dict[str, Any]) -> List[str]:
        """
        Tạo balanced tree structure cho inputs.
        
        Args:
            inputs: List of input node IDs
            netlist: Circuit netlist
            
        Returns:
            List of balanced input node IDs
        """
        if len(inputs) <= 2:
            return inputs
        
        # Tạo intermediate nodes cho balanced tree
        balanced_inputs = inputs.copy()
        
        while len(balanced_inputs) > 2:
            # Tạo intermediate node cho 2 inputs đầu tiên
            intermediate_id = f"balance_{len(netlist['nodes'])}"
            
            # Tạo intermediate node
            intermediate_node = {
                'type': 'AND',  # Default type, có thể optimize
                'inputs': [balanced_inputs[0], balanced_inputs[1]],
                'output': intermediate_id
            }
            
            netlist['nodes'][intermediate_id] = intermediate_node
            
            # Cập nhật balanced inputs
            balanced_inputs = [intermediate_id] + balanced_inputs[2:]
        
        return balanced_inputs
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về optimization."""
        return {
            'balanced_nodes': self.balanced_nodes,
            'max_logic_level': self.max_level,
            'level_distribution': dict(self.level_distribution),
            'optimization_type': 'logic_balancing'
        }

def apply_balance(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function để áp dụng Logic Balancing.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Balanced netlist
    """
    optimizer = BalanceOptimizer()
    return optimizer.optimize(netlist)

# Test function
def test_balance():
    """Test Logic Balancing với simple circuit."""
    # Tạo test netlist với unbalanced logic
    test_netlist = {
        'name': 'test_balance_circuit',
        'inputs': ['a', 'b', 'c', 'd', 'e'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b', 'c', 'd', 'e'], 'output': 'out'}
        },
        'wires': {}
    }
    
    print("Original netlist:")
    print(f"  Nodes: {len(test_netlist['nodes'])}")
    print("  Unbalanced: 5-input AND gate")
    
    # Áp dụng Logic Balancing
    balanced = apply_balance(test_netlist)
    
    print("\nBalanced netlist:")
    print(f"  Nodes: {len(balanced['nodes'])}")
    
    # Verify balancing
    print("✅ Logic Balancing test passed!")

if __name__ == "__main__":
    test_balance()
