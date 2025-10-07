#!/usr/bin/env python3
"""
Common Subexpression Elimination (CSE) Algorithm Implementation

Dựa trên các khái niệm VLSI CAD Part 1 cho tối ưu hóa logic.
CSE tìm và loại bỏ các subexpressions trùng lặp trong mạch.
"""

import sys
import os
from typing import Dict, List, Set, Any, Tuple, Optional
import logging

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class CSEOptimizer:
    """
    Common Subexpression Elimination optimizer.
    
    Tìm và loại bỏ các subexpressions trùng lặp bằng cách
    tạo shared nodes và cập nhật connections.
    """
    
    def __init__(self):
        self.subexpression_table: Dict[str, str] = {}  # expression -> node_id
        self.shared_nodes: Dict[str, str] = {}  # original_node -> shared_node
        self.removed_nodes = 0
        self.created_shared_nodes = 0
        
    def optimize(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Áp dụng Common Subexpression Elimination cho netlist.
        
        Args:
            netlist: Circuit netlist với nodes, inputs, outputs
            
        Returns:
            Optimized netlist với shared subexpressions
        """
        logger.info("Bắt đầu Common Subexpression Elimination...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
            
        original_nodes = len(netlist['nodes'])
        
        # Tìm common subexpressions
        subexpressions = self._find_common_subexpressions(netlist)
        
        if not subexpressions:
            logger.info("Không tìm thấy common subexpressions")
            return netlist
        
        # Tạo shared nodes
        optimized_netlist = self._create_shared_nodes(netlist, subexpressions)
        
        # Cập nhật connections
        optimized_netlist = self._update_connections(optimized_netlist)
        
        final_nodes = len(optimized_netlist['nodes'])
        reduction = original_nodes - final_nodes
        
        logger.info(f"CSE optimization hoàn thành:")
        logger.info(f"  Original nodes: {original_nodes}")
        logger.info(f"  Optimized nodes: {final_nodes}")
        logger.info(f"  Removed nodes: {reduction}")
        logger.info(f"  Created shared nodes: {self.created_shared_nodes}")
        logger.info(f"  Reduction: {(reduction/original_nodes)*100:.1f}%")
        
        return optimized_netlist
    
    def _find_common_subexpressions(self, netlist: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Tìm các common subexpressions trong netlist.
        
        Args:
            netlist: Circuit netlist
            
        Returns:
            Dictionary mapping expression -> list of node IDs
        """
        expression_count: Dict[str, List[str]] = {}
        
        for node_id, node_data in netlist['nodes'].items():
            if self._is_computational_node(node_data):
                # Tạo expression signature
                expression = self._create_expression_signature(node_data)
                
                if expression in expression_count:
                    expression_count[expression].append(node_id)
                else:
                    expression_count[expression] = [node_id]
        
        # Chỉ giữ lại expressions xuất hiện nhiều hơn 1 lần
        common_expressions = {
            expr: nodes for expr, nodes in expression_count.items() 
            if len(nodes) > 1
        }
        
        logger.info(f"Tìm thấy {len(common_expressions)} common subexpressions")
        for expr, nodes in common_expressions.items():
            logger.debug(f"Expression '{expr}' xuất hiện {len(nodes)} lần: {nodes}")
        
        return common_expressions
    
    def _is_computational_node(self, node_data: Dict[str, Any]) -> bool:
        """Kiểm tra xem node có phải là computational node không."""
        computational_types = ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'ADD', 'SUB', 'MUL']
        return node_data.get('type', '') in computational_types
    
    def _create_expression_signature(self, node_data: Dict[str, Any]) -> str:
        """
        Tạo signature cho expression.
        
        Args:
            node_data: Node data
            
        Returns:
            Expression signature string
        """
        gate_type = node_data.get('type', '')
        inputs = node_data.get('inputs', [])
        
        # Sort inputs để đảm bảo canonical form
        sorted_inputs = sorted(inputs)
        
        # Tạo signature
        signature = f"{gate_type}({','.join(sorted_inputs)})"
        return signature
    
    def _create_shared_nodes(self, netlist: Dict[str, Any], subexpressions: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Tạo shared nodes cho common subexpressions.
        
        Args:
            netlist: Original netlist
            subexpressions: Common subexpressions mapping
            
        Returns:
            Netlist với shared nodes
        """
        optimized_netlist = netlist.copy()
        optimized_netlist['nodes'] = netlist['nodes'].copy()
        
        for expression, node_list in subexpressions.items():
            if len(node_list) < 2:
                continue
            
            # Tạo shared node ID
            shared_node_id = f"shared_{self.created_shared_nodes}"
            self.created_shared_nodes += 1
            
            # Lấy node data từ node đầu tiên
            first_node = node_list[0]
            shared_node_data = optimized_netlist['nodes'][first_node].copy()
            
            # Cập nhật output name
            shared_node_data['output'] = f"shared_{expression.replace('(', '_').replace(')', '').replace(',', '_')}"
            
            # Thêm shared node vào netlist
            optimized_netlist['nodes'][shared_node_id] = shared_node_data
            
            # Lưu mapping cho các nodes cần thay thế
            for node_id in node_list:
                self.shared_nodes[node_id] = shared_node_id
                # Loại bỏ original node (sẽ được thay thế)
                del optimized_netlist['nodes'][node_id]
                self.removed_nodes += 1
            
            logger.debug(f"Tạo shared node {shared_node_id} cho expression '{expression}'")
        
        return optimized_netlist
    
    def _update_connections(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cập nhật connections sau khi tạo shared nodes.
        
        Args:
            netlist: Netlist với shared nodes
            
        Returns:
            Netlist với updated connections
        """
        # Cập nhật wire connections
        if 'wires' in netlist:
            updated_wires = {}
            for wire_id, wire_data in netlist['wires'].items():
                updated_wire = wire_data.copy()
                
                # Cập nhật source
                if 'source' in updated_wire:
                    source = updated_wire['source']
                    if source in self.shared_nodes:
                        updated_wire['source'] = self.shared_nodes[source]
                
                # Cập nhật destination
                if 'destination' in updated_wire:
                    destination = updated_wire['destination']
                    if destination in self.shared_nodes:
                        updated_wire['destination'] = self.shared_nodes[destination]
                
                updated_wires[wire_id] = updated_wire
            
            netlist['wires'] = updated_wires
        
        # Cập nhật node input connections
        for node_id, node_data in netlist['nodes'].items():
            if 'inputs' in node_data:
                updated_inputs = []
                for input_node in node_data['inputs']:
                    if input_node in self.shared_nodes:
                        updated_inputs.append(self.shared_nodes[input_node])
                    else:
                        updated_inputs.append(input_node)
                node_data['inputs'] = updated_inputs
        
        return netlist
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về optimization."""
        return {
            'removed_nodes': self.removed_nodes,
            'created_shared_nodes': self.created_shared_nodes,
            'subexpressions_found': len(self.subexpression_table),
            'optimization_type': 'common_subexpression_elimination'
        }

def apply_cse(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function để áp dụng Common Subexpression Elimination.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Optimized netlist
    """
    optimizer = CSEOptimizer()
    return optimizer.optimize(netlist)

# Test function
def test_cse():
    """Test Common Subexpression Elimination với simple circuit."""
    # Tạo test netlist với common subexpressions
    test_netlist = {
        'name': 'test_cse_circuit',
        'inputs': ['a', 'b', 'c', 'd'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp2'},  # Common subexpression
            'n3': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out1'},
            'n4': {'type': 'OR', 'inputs': ['temp2', 'd'], 'output': 'out2'}
        },
        'wires': {
            'w1': {'source': 'n1', 'destination': 'n3'},
            'w2': {'source': 'n2', 'destination': 'n4'},
            'w3': {'source': 'c', 'destination': 'n3'},
            'w4': {'source': 'd', 'destination': 'n4'}
        }
    }
    
    print("Original netlist:")
    print(f"  Nodes: {len(test_netlist['nodes'])}")
    print("  Common subexpressions: AND(a,b) appears 2 times")
    
    # Apply CSE
    optimized = apply_cse(test_netlist)
    
    print("\nOptimized netlist:")
    print(f"  Nodes: {len(optimized['nodes'])}")
    
    # Verify optimization
    assert len(optimized['nodes']) < len(test_netlist['nodes']), "CSE should reduce nodes"
    print("CSE test passed!")

if __name__ == "__main__":
    test_cse()
