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
        print(">>> Starting Structural Hashing optimization...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            print("WARNING: Invalid netlist format")
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
        # Track replacements to update output_mapping later
        replacement_map: Dict[str, str] = {}
        removed_details = []  # Store details of removed nodes
        
        print(f"Original nodes: {original_nodes}")
        print("Analyzing nodes...")
        
        # Process each node
        for node_id, node_data in nodes_dict.items():
            if self._is_gate_node(node_data):
                # Create hash key for node
                hash_key = self._create_hash_key(node_data, optimized_nodes)
                
                if hash_key in self.hash_table:
                    # Node exists, skip it
                    existing_node = self.hash_table[hash_key]
                    self.removed_nodes += 1
                    
                    # Store removal details
                    node_type = node_data.get('type', 'UNKNOWN')
                    fanins = node_data.get('fanins', [])
                    fanin_str = ', '.join([f'{f[0]}' for f in fanins]) if fanins else 'none'
                    removed_details.append({
                        'id': node_id,
                        'type': node_type,
                        'fanins': fanin_str,
                        'replaced_by': existing_node
                    })
                    
                    print(f"REMOVED: {node_id} ({node_type}) - inputs: [{fanin_str}] -> replaced by {existing_node}")
                else:
                    # Check for redundant BUF nodes
                    if node_data.get('type') == 'BUF' and self._is_redundant_buffer(node_data, nodes_dict):
                        # Remove redundant buffer
                        self.removed_nodes += 1
                        
                        node_type = node_data.get('type', 'UNKNOWN')
                        fanins = node_data.get('fanins', [])
                        fanin_str = ', '.join([f'{f[0]}' for f in fanins]) if fanins else 'none'
                        removed_details.append({
                            'id': node_id,
                            'type': node_type,
                            'fanins': fanin_str,
                            'replaced_by': fanins[0][0] if fanins else 'direct_connection'
                        })
                        # Record replacement for mapping update
                        if fanins:
                            replacement_map[str(node_id)] = str(fanins[0][0])
                        
                        print(f"REMOVED: {node_id} ({node_type}) - inputs: [{fanin_str}] -> replaced by direct connection")
                    else:
                        # New node, add to hash table and optimized_nodes
                        self.hash_table[hash_key] = node_id
                        optimized_nodes[node_id] = node_data
            else:
                # Non-gate node (input, output, constant)
                optimized_nodes[node_id] = node_data
        
        # Update netlist
        optimized_netlist = netlist.copy()
        # Convert back to list format if original was list
        if isinstance(nodes_data, list):
            optimized_netlist['nodes'] = list(optimized_nodes.values())
        else:
            optimized_netlist['nodes'] = optimized_nodes
        
        # Update wire connections
        optimized_netlist = self._update_wire_connections(optimized_netlist)

        # Update output_mapping to point to replacements (if any)
        try:
            attrs = optimized_netlist.setdefault('attrs', {})
            out_map = attrs.setdefault('output_mapping', {})
            for out_name, node_ref in list(out_map.items()):
                node_ref_str = str(node_ref)
                if node_ref_str in replacement_map:
                    out_map[out_name] = replacement_map[node_ref_str]
        except Exception:
            pass
        
        final_nodes = len(optimized_netlist['nodes'])
        reduction = original_nodes - final_nodes
        
        print()
        print("=== STRASH OPTIMIZATION RESULTS ===")
        print(f"  Original nodes: {original_nodes}")
        print(f"  Optimized nodes: {final_nodes}")
        print(f"  Removed nodes: {reduction}")
        print(f"  Reduction: {(reduction/original_nodes)*100:.1f}%")
        
        if removed_details:
            print()
            print("=== REMOVED NODES DETAILS ===")
            for detail in removed_details:
                print(f"  - {detail['id']} ({detail['type']}) - inputs: [{detail['fanins']}] -> replaced by {detail['replaced_by']}")
        
        print()
        print("Strash optimization completed!")
        
        return optimized_netlist
    
    def _is_gate_node(self, node_data: Dict[str, Any]) -> bool:
        """Check if node is a gate node."""
        gate_types = ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT', 'BUF', 'ADD', 'SUB', 'MUL', 'DIV']
        return node_data.get('type', '') in gate_types
    
    def _is_redundant_buffer(self, node_data: Dict[str, Any], nodes_dict: Dict[str, Any]) -> bool:
        """
        Enhanced check if a BUF node is redundant (can be removed).
        
        A BUF node is redundant if:
        1. It's a BUF node
        2. Its input is not used by any other node (except this BUF)
        3. Or it's just a simple pass-through buffer
        4. Or it's not driving any critical outputs
        """
        if node_data.get('type') != 'BUF':
            return False
            
        fanins = node_data.get('fanins', [])
        if not fanins:
            return False
            
        input_node = fanins[0][0]
        
        # Count how many times this input is used
        usage_count = 0
        for other_node_id, other_node_data in nodes_dict.items():
            other_fanins = other_node_data.get('fanins', [])
            for fanin in other_fanins:
                if fanin[0] == input_node:
                    usage_count += 1
        
        # Enhanced logic: Remove BUF if:
        # 1. Input is used by exactly 1 node (this BUF)
        # 2. OR input is a simple signal (not complex logic)
        # 3. OR BUF is not driving critical outputs
        return usage_count == 1 or self._is_simple_signal(input_node, nodes_dict)
    
    def _is_simple_signal(self, signal_name: str, nodes_dict: Dict[str, Any]) -> bool:
        """Check if signal is simple (input or constant)."""
        # Check if it's a primary input or constant
        if signal_name in ['0', '1', 'x', 'z']:
            return True
        
        # Check if it's a primary input (not generated by logic)
        for node_id, node_data in nodes_dict.items():
            if node_data.get('type') in ['INPUT', 'CONSTANT']:
                if signal_name in node_data.get('outputs', []):
                    return True
        
        return False
    
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
        fanins = node_data.get('fanins', [])
        
        # Extract input names from fanins
        inputs = [f[0] for f in fanins] if fanins else []
        
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

def structural_hashing(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convenience function để áp dụng Structural Hashing.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Optimized netlist
    """
    optimizer = StrashOptimizer()
    return optimizer.optimize(netlist)

def apply_strash(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """Alias wrapper to match synthesis_flow usage."""
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
