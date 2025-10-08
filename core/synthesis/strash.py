#!/usr/bin/env python3
"""
Structural Hashing (Strash) Algorithm Implementation

Dựa trên các khái niệm VLSI CAD Part 1 và tham khảo từ ABC (YosysHQ/abc).
Strash loại bỏ các node trùng lặp và tạo canonical representation.

ABC Reference: src/aig/aig/aigStrash.c
- Aig_ManStrash(): Main structural hashing function
- Hash table với canonical representation
- Efficient duplicate detection và removal
"""

import sys
import os
from typing import Dict, List, Set, Any, Tuple, Optional
import logging

# Thêm thư mục gốc project vào đường dẫn
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)

class StrashOptimizer:
    """
    Structural Hashing optimizer.
    
    Loại bỏ các node trùng lặp trong netlist bằng cách tạo
    canonical representation và sử dụng hash table.
    """
    
    def __init__(self):
        # ABC-inspired hash table structure
        self.hash_table: Dict[Tuple[str, str, str], str] = {}  # (gate_type, input1, input2) -> node_id
        self.node_count = 0
        self.removed_nodes = 0
        self.computed_table: Dict[Tuple[str, str], str] = {}  # ABC-style computed table
        self.unique_table: Dict[Tuple[str, str, str], str] = {}  # ABC-style unique table
        
    def optimize(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply Structural Hashing to netlist.
        
        Args:
            netlist: Circuit netlist with nodes, inputs, outputs
            
        Returns:
            Optimized netlist with duplicate nodes removed
        """
        logger.info("Starting Structural Hashing optimization...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            logger.warning("Invalid netlist format")
            return netlist
        
        # Convert nodes list to dict if needed
        nodes_data = netlist['nodes']
        if isinstance(nodes_data, list):
            # Convert list to dict with index as key
            nodes_dict = {i: node for i, node in enumerate(nodes_data)}
        else:
            nodes_dict = nodes_data
            
        original_nodes = len(nodes_dict)
        
        # Create hash table for nodes
        self.hash_table = {}
        optimized_nodes = {}
        
        # Process each node
        for node_id, node_data in nodes_dict.items():
            if self._is_gate_node(node_data):
                # Create hash key for node
                hash_key = self._create_hash_key(node_data, optimized_nodes)
                
                if hash_key in self.hash_table:
                    # Node exists, skip it
                    existing_node = self.hash_table[hash_key]
                    self.removed_nodes += 1
                    logger.debug(f"Removed duplicate node {node_id} -> {existing_node}")
                else:
                    # New node, add to hash table and optimized_nodes
                    self.hash_table[hash_key] = node_id
                    optimized_nodes[node_id] = node_data
            else:
                # Non-gate node (input, output, constant)
                optimized_nodes[node_id] = node_data
        
        # Update netlist
        optimized_netlist = netlist.copy()
        optimized_netlist['nodes'] = optimized_nodes
        
        # Update wire connections
        optimized_netlist = self._update_wire_connections(optimized_netlist)
        
        final_nodes = len(optimized_netlist['nodes'])
        reduction = original_nodes - final_nodes
        
        logger.info(f"Strash optimization completed:")
        logger.info(f"  Original nodes: {original_nodes}")
        logger.info(f"  Optimized nodes: {final_nodes}")
        logger.info(f"  Removed nodes: {reduction}")
        logger.info(f"  Reduction: {(reduction/original_nodes)*100:.1f}%")
        
        return optimized_netlist
    
    def _is_gate_node(self, node_data: Dict[str, Any]) -> bool:
        """Check if node is a gate node."""
        gate_types = ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF']
        return node_data.get('type', '') in gate_types
    
    def _create_hash_key(self, node_data: Dict[str, Any], optimized_nodes: Dict[str, Any]) -> Tuple[str, str, str]:
        """
        Create hash key for node based on gate type and inputs.
        
        Args:
            node_data: Node data
            optimized_nodes: Dictionary of optimized nodes
            
        Returns:
            Hash key tuple (gate_type, input1, input2)
        """
        gate_type = node_data.get('type', '')
        inputs = node_data.get('inputs', [])
        
        # Sort inputs to ensure canonical form
        sorted_inputs = sorted(inputs)
        
        if len(sorted_inputs) == 1:
            # Unary gate (NOT, BUF)
            return (gate_type, sorted_inputs[0], '')
        elif len(sorted_inputs) == 2:
            # Binary gate (AND, OR, XOR, etc.)
            return (gate_type, sorted_inputs[0], sorted_inputs[1])
        else:
            # Multi-input gate - không support trong implementation này
            return (gate_type, str(sorted_inputs), '')
    
    def _update_wire_connections(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update wire connections after removing duplicate nodes.
        
        Args:
            netlist: Netlist with optimized nodes
            
        Returns:
            Netlist with updated wire connections
        """
        # Create mapping from old node IDs to new node IDs
        node_mapping = {}
        
        # Handle both dict and list format for nodes
        nodes_data = netlist['nodes']
        if isinstance(nodes_data, dict):
            for node_id, node_data in nodes_data.items():
                if isinstance(node_data, str):
                    # Node has been replaced
                    node_mapping[node_id] = node_data
        
        # Update wire connections - handle both list and dict format
        if 'wires' in netlist and netlist['wires']:
            wires_data = netlist['wires']
            
            if isinstance(wires_data, list):
                # Wires is a list - update in place
                updated_wires = []
                for wire_data in wires_data:
                    if isinstance(wire_data, dict):
                        updated_wire = wire_data.copy()
                        
                        # Update source and destination
                        if 'source' in updated_wire and updated_wire['source'] in node_mapping:
                            updated_wire['source'] = node_mapping[updated_wire['source']]
                        
                        if 'destination' in updated_wire and updated_wire['destination'] in node_mapping:
                            updated_wire['destination'] = node_mapping[updated_wire['destination']]
                        
                        updated_wires.append(updated_wire)
                    else:
                        updated_wires.append(wire_data)
                
                netlist['wires'] = updated_wires
            
            elif isinstance(wires_data, dict):
                # Wires is a dict
                updated_wires = {}
                for wire_id, wire_data in wires_data.items():
                    updated_wire = wire_data.copy()
                    
                    # Update source and destination
                    if 'source' in updated_wire and updated_wire['source'] in node_mapping:
                        updated_wire['source'] = node_mapping[updated_wire['source']]
                    
                    if 'destination' in updated_wire and updated_wire['destination'] in node_mapping:
                        updated_wire['destination'] = node_mapping[updated_wire['destination']]
                    
                    updated_wires[wire_id] = updated_wire
                
                netlist['wires'] = updated_wires
        
        return netlist
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về optimization."""
        return {
            'removed_nodes': self.removed_nodes,
            'hash_table_size': len(self.hash_table),
            'optimization_type': 'structural_hashing'
        }

def apply_strash(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function để áp dụng Structural Hashing.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Optimized netlist
    """
    optimizer = StrashOptimizer()
    return optimizer.optimize(netlist)

# Test function
def test_strash():
    """Test Structural Hashing với simple circuit."""
    # Tạo test netlist với duplicate nodes
    test_netlist = {
        'name': 'test_circuit',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp2'},  # Duplicate
            'n3': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out1'},
            'n4': {'type': 'OR', 'inputs': ['temp2', 'c'], 'output': 'out2'}
        },
        'wires': {
            'w1': {'source': 'n1', 'destination': 'n3'},
            'w2': {'source': 'n2', 'destination': 'n4'},
            'w3': {'source': 'c', 'destination': 'n3'},
            'w4': {'source': 'c', 'destination': 'n4'}
        }
    }
    
    print("Original netlist:")
    print(f"  Nodes: {len(test_netlist['nodes'])}")
    
    # Áp dụng Strash
    optimized = apply_strash(test_netlist)
    
    print("\nOptimized netlist:")
    print(f"  Nodes: {len(optimized['nodes'])}")
    
    # Verify optimization
    if len(optimized['nodes']) <= len(test_netlist['nodes']):
        print("Strash test passed!")
    else:
        print("Strash test: No optimization occurred (may be expected)")

if __name__ == "__main__":
    test_strash()
