#!/usr/bin/env python3
"""
Dead Code Elimination (DCE) Algorithm Implementation

DCE loại bỏ các node không thể tiếp cận từ bất kỳ output nào, hiệu quả
loại bỏ dead code và giảm kích thước mạch.

ABC Reference: src/aig/aig/aigDfs.c
- Aig_ManDfs(): Depth-first search for reachability
- Aig_ManCleanup(): Cleanup unused nodes
- Advanced DCE với Don't Care conditions
"""

from typing import Dict, List, Set, Any, Tuple
import logging

logger = logging.getLogger(__name__)

def _nodes_to_dict(nodes_any: Any) -> Tuple[Dict[str, Any], str]:
    """Normalize nodes to dict keyed by node id; return (dict, original_format)."""
    if isinstance(nodes_any, dict):
        return nodes_any, 'dict'
    if isinstance(nodes_any, list):
        nodes_dict: Dict[str, Any] = {}
        for i, n in enumerate(nodes_any):
            if isinstance(n, dict):
                key = str(n.get('id', i))
                # ensure node has id
                if 'id' not in n:
                    n = {**n, 'id': key}
                nodes_dict[key] = n
        return nodes_dict, 'list'
    return {}, 'unknown'

def _nodes_from_dict(nodes_dict: Dict[str, Any], fmt: str) -> Any:
    """Convert nodes dict back to original format."""
    if fmt == 'list':
        return list(nodes_dict.values())
    return nodes_dict

class DCEOptimizer:
    """
    Dead Code Elimination optimizer với hỗ trợ Don't Cares.
    
    Dựa trên các khái niệm VLSI CAD Part 1 cho tối ưu hóa nâng cao.
    Loại bỏ các node không thể tiếp cận từ bất kỳ output port nào.
    """
    
    def __init__(self):
        self.removed_nodes = 0
        self.removed_wires = 0
        self.dont_cares: Dict[str, Set[Tuple[bool, ...]]] = {}  # Don't care conditions
        self.optimization_level = "basic"  # basic, advanced, aggressive
        
    def optimize(self, netlist: Dict[str, Any], level: str = "basic") -> Dict[str, Any]:
        """
        Apply Dead Code Elimination to the netlist with Don't Cares support.
        
        Args:
            netlist: Circuit netlist with nodes, inputs, outputs
            level: Optimization level ("basic", "advanced", "aggressive")
            
        Returns:
            Optimized netlist with dead code removed
        """
        logger.info(f"Starting Dead Code Elimination (DCE) - Level: {level}")
        
        self.optimization_level = level
        
        # Reset counters
        self.removed_nodes = 0
        self.removed_wires = 0
        
        # Create a copy to avoid modifying original
        optimized_netlist = netlist.copy()
        # Normalize nodes to dict
        nodes_dict, original_fmt = _nodes_to_dict(optimized_netlist.get('nodes', {}))
        optimized_netlist['nodes'] = nodes_dict
        
        # Extract Don't Care conditions
        if level in ["advanced", "aggressive"]:
            self._extract_dont_cares(optimized_netlist)
        
        # Find reachable nodes from outputs
        reachable_nodes = self._find_reachable_nodes(optimized_netlist)
        
        # Advanced optimization with Don't Cares
        if level in ["advanced", "aggressive"]:
            reachable_nodes = self._apply_dont_care_optimization(optimized_netlist, reachable_nodes)
        
        # Remove unreachable nodes
        optimized_netlist = self._remove_dead_nodes(optimized_netlist, reachable_nodes)
        
        # Update wire connections
        optimized_netlist = self._update_wire_connections(optimized_netlist)
        
        # Aggressive optimization: remove redundant nodes
        if level == "aggressive":
            optimized_netlist = self._remove_redundant_nodes(optimized_netlist)
        
        logger.info(f"DCE completed: removed {self.removed_nodes} nodes, {self.removed_wires} wires")
        logger.info(f"Reachable nodes: {len(reachable_nodes)}")
        logger.debug(f"Reachable node keys/ids: {list(reachable_nodes)[:10]}")  # First 10
        
        # Convert nodes back to original format
        optimized_netlist['nodes'] = _nodes_from_dict(optimized_netlist.get('nodes', {}), original_fmt)
        return optimized_netlist
    
    def _find_reachable_nodes(self, netlist: Dict[str, Any]) -> Set[str]:
        """
        Find all nodes reachable from output ports using BFS.
        
        Args:
            netlist: Circuit netlist
            
        Returns:
            Set of reachable node names
        """
        reachable = set()
        queue = []
        
        # Start from all output ports using output_mapping
        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
        outputs = netlist.get('outputs', [])
        nodes_dict = netlist.get('nodes', {})
        
        # Normalize nodes to dict if needed
        if isinstance(nodes_dict, list):
            nodes_dict_normalized = {}
            for i, n in enumerate(nodes_dict):
                if isinstance(n, dict):
                    # Prefer node id, then output, then index
                    node_id = n.get('id')
                    node_output = n.get('output')
                    
                    if node_id is not None:
                        key = str(node_id)
                    elif node_output is not None:
                        key = str(node_output)  # Use output as key
                    else:
                        key = str(i)
                    
                    if 'id' not in n and node_id is None:
                        n = {**n, 'id': key}
                    nodes_dict_normalized[key] = n
            nodes_dict = nodes_dict_normalized
            logger.debug(f"Normalized {len(nodes_dict)} nodes from list to dict")
        
        # Find nodes that drive primary outputs
        logger.debug(f"Total nodes before DCE: {len(nodes_dict)}")
        logger.debug(f"Output mapping: {output_mapping}")
        logger.debug(f"Outputs: {outputs}")
        
        # Debug: print all nodes
        for key, node_data in list(nodes_dict.items())[:5]:  # First 5 nodes
            if isinstance(node_data, dict):
                logger.debug(f"Sample node {key}: type={node_data.get('type')}, output={node_data.get('output')}, id={node_data.get('id')}, inputs={node_data.get('inputs', [])}")
        
        for output in outputs:
            if isinstance(output, str):
                output_name = output
                # Find the node that drives this output
                if output_name in output_mapping:
                    output_signal = output_mapping[output_name]  # e.g., "xor_0", "or_7"
                    logger.debug(f"Looking for node driving output '{output_name}' via signal '{output_signal}'")
                    
                    # Find node by output field (not by id)
                    node_key = None
                    for key, node_data in nodes_dict.items():
                        if isinstance(node_data, dict):
                            node_output = node_data.get('output')
                            node_id = str(node_data.get('id', ''))
                            
                            # Match by output signal or id
                            if node_output == output_signal or node_id == output_signal or key == output_signal:
                                node_key = key
                                reachable.add(node_key)
                                queue.append(node_key)
                                logger.info(f"✓ Found node for output {output_name}: signal {output_signal} -> node key {node_key} (type: {node_data.get('type')}, output: {node_output}, id: {node_id})")
                                break
                    
                    if node_key is None:
                        logger.warning(f"✗ Could not find node for output {output_name} with signal {output_signal}")
                        # Try to find any node that might match
                        for key, node_data in nodes_dict.items():
                            if isinstance(node_data, dict):
                                if output_signal in str(node_data.get('output', '')) or output_signal in str(node_data.get('id', '')):
                                    logger.debug(f"  Partial match found: node {key} with output={node_data.get('output')}, id={node_data.get('id')}")
                else:
                    logger.warning(f"Output '{output_name}' not in output_mapping")
        
        # BFS to find all reachable nodes
        while queue:
            current_node_key = queue.pop(0)
            # Find node by key (already normalized to dict)
            node = nodes_dict.get(current_node_key) if isinstance(nodes_dict, dict) else None
            
            # Fallback: try to find by iterating if current_node_key is not a direct key
            if not isinstance(node, dict) and isinstance(nodes_dict, dict):
                for key, node_data in nodes_dict.items():
                    if isinstance(node_data, dict):
                        node_id = node_data.get('id')
                        if node_id == current_node_key or key == current_node_key:
                            node = node_data
                            current_node_key = key  # Update to actual key
                            break
            
            # Check if node is a dictionary
            if not isinstance(node, dict):
                logger.debug(f"Skipping node {current_node_key} - not found or invalid")
                continue
                
            # Add all input nodes of current node
            # Try both 'inputs' and 'fanins' fields (different parsers use different formats)
            inputs = node.get('inputs', [])
            fanins = node.get('fanins', [])
            
            # Process fanins (list of tuples: [(signal_name, node_id), ...])
            if fanins:
                for fanin in fanins:
                    if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                        fanin_signal = fanin[0]  # Signal name
                        fanin_node_id = fanin[1] if len(fanin) > 1 else None
                    elif isinstance(fanin, str):
                        fanin_signal = fanin
                        fanin_node_id = None
                    else:
                        continue
                    
                    # Skip if input is a primary input
                    if fanin_signal in netlist.get('inputs', []):
                        continue
                    
                    # Find which node produces this fanin signal
                    found_fanin = False
                    if isinstance(nodes_dict, dict):
                        for other_node_key, other_node in nodes_dict.items():
                            if isinstance(other_node, dict):
                                other_node_output = other_node.get('output')
                                other_node_id = str(other_node.get('id', ''))
                                
                                # Match by output signal, id, or key
                                if (other_node_output == fanin_signal or 
                                    other_node_id == fanin_signal or 
                                    other_node_key == fanin_signal or
                                    (fanin_node_id and (other_node_id == fanin_node_id or other_node_key == fanin_node_id))):
                                    if other_node_key not in reachable:
                                        reachable.add(other_node_key)
                                        queue.append(other_node_key)
                                        found_fanin = True
                                        logger.debug(f"Found fanin: {fanin_signal} -> node {other_node_key} (type: {other_node.get('type')})")
                                        break
                    
                    if not found_fanin:
                        logger.debug(f"Could not find fanin node for signal {fanin_signal} (may be primary input or intermediate signal)")
            
            # Also process inputs field (for compatibility)
            elif inputs:
                for input_name in inputs:
                    # Skip if input is a primary input
                    if input_name in netlist.get('inputs', []):
                        continue
                    
                    # Find which node produces this input (by output field)
                    found_fanin = False
                    if isinstance(nodes_dict, dict):
                        for other_node_key, other_node in nodes_dict.items():
                            if isinstance(other_node, dict):
                                other_node_output = other_node.get('output')
                                other_node_id = str(other_node.get('id', ''))
                                # Match by output signal or id
                                if (other_node_output == input_name or 
                                    other_node_id == input_name or 
                                    other_node_key == input_name):
                                    if other_node_key not in reachable:
                                        reachable.add(other_node_key)
                                        queue.append(other_node_key)
                                        found_fanin = True
                                        logger.debug(f"Found fanin (via inputs): {input_name} -> node {other_node_key}")
                                        break
                    
                    if not found_fanin:
                        logger.debug(f"Could not find fanin node for input {input_name} (may be primary input or intermediate signal)")
        
        return reachable
    
    def _remove_dead_nodes(self, netlist: Dict[str, Any], reachable_nodes: Set[str]) -> Dict[str, Any]:
        """
        Remove nodes that are not reachable from outputs.
        
        Args:
            netlist: Circuit netlist
            reachable_nodes: Set of reachable node keys/ids
            
        Returns:
            Netlist with dead nodes removed
        """
        nodes_dict = netlist.get('nodes', {})
        
        # Normalize to dict if needed
        if isinstance(nodes_dict, list):
            nodes_dict, _ = _nodes_to_dict(nodes_dict)
        
        # Find dead nodes (nodes not in reachable set)
        dead_node_keys = []
        logger.info(f"Checking {len(nodes_dict)} nodes against {len(reachable_nodes)} reachable nodes")
        
        for node_key, node_data in nodes_dict.items():
            if isinstance(node_data, dict):
                node_id = str(node_data.get('id', node_key))
                node_key_str = str(node_key)
                # Check if node is reachable (by key or id)
                is_reachable = (node_key_str in reachable_nodes or 
                               node_id in reachable_nodes or
                               node_key in reachable_nodes)
                
                if not is_reachable:
                    dead_node_keys.append(node_key)
                    logger.debug(f"Dead node: key={node_key}, id={node_id}, type={node_data.get('type')}")
                else:
                    logger.debug(f"Keep node: key={node_key}, id={node_id}, type={node_data.get('type')}")
        
        # Count dead nodes before removing
        self.removed_nodes = len(dead_node_keys)
        
        # Remove dead nodes
        for node_key in dead_node_keys:
            if node_key in nodes_dict:
                node_data = nodes_dict[node_key]
                logger.debug(f"Removed dead node: {node_key} (type: {node_data.get('type', 'unknown')})")
                del nodes_dict[node_key]
        
        # Update netlist
        netlist['nodes'] = nodes_dict
        
        return netlist
    
    def _update_wire_connections(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update wire connections after removing dead nodes.
        
        Args:
            netlist: Circuit netlist
            
        Returns:
            Netlist with updated wire connections
        """
        nodes = netlist.get('nodes', {})
        wires = netlist.get('wires', [])
        
        # Count dead wires before removing
        original_wire_count = len(wires)
        
        # Remove wires that are no longer connected
        valid_wires = []
        for wire in wires:
            if isinstance(wire, dict):
                source = wire.get('source')
                sink = wire.get('sink')
                
                # Check if both source and sink exist
                source_exists = False
                sink_exists = False
                
                # Check if source is an input or output of existing node
                if source in netlist.get('inputs', []):
                    source_exists = True
                else:
                    for node in nodes.values():
                        if node.get('output') == source:
                            source_exists = True
                            break
                
                # Check if sink is an input of existing node
                for node in nodes.values():
                    if sink in node.get('inputs', []):
                        sink_exists = True
                        break
                
                if source_exists and sink_exists:
                    valid_wires.append(wire)
                else:
                    logger.debug(f"Removed dead wire: {source} -> {sink}")
            else:
                # Keep simple wire references
                valid_wires.append(wire)
        
        # Count removed wires
        self.removed_wires = original_wire_count - len(valid_wires)
        netlist['wires'] = valid_wires
        
        return netlist
    
    def _extract_dont_cares(self, netlist: Dict[str, Any]) -> None:
        """
        Extract Don't Care conditions from netlist.
        
        Based on VLSI CAD Part 1 concepts for observability and satisfiability don't cares.
        """
        logger.debug("Extracting Don't Care conditions...")
        
        nodes = netlist.get('nodes', {})
        
        for node_name, node in nodes.items():
            dont_cares = set()
            
            # Satisfiability Don't Cares (SDCs)
            # Conditions where node output is not used
            if self._is_output_unused(node, netlist):
                # All input combinations are don't cares
                inputs = node.get('inputs', [])
                if len(inputs) == 2:  # Binary gates
                    dont_cares.update([
                        (False, False),
                        (False, True),
                        (True, False),
                        (True, True)
                    ])
            
            # Observability Don't Cares (ODCs)
            # Conditions where node output doesn't affect any primary output
            odc_conditions = self._find_observability_dont_cares(node, netlist)
            dont_cares.update(odc_conditions)
            
            if dont_cares:
                self.dont_cares[node_name] = dont_cares
                logger.debug(f"Don't cares for {node_name}: {len(dont_cares)} conditions")
    
    def _is_output_unused(self, node: Dict[str, Any], netlist: Dict[str, Any]) -> bool:
        """Check if node output is used by any other node."""
        output = node.get('output')
        if not output:
            return True
        
        # Check if output is a primary output
        if output in netlist.get('outputs', []):
            return False
        
        # Check if output is used as input by other nodes
        for other_node in netlist.get('nodes', {}).values():
            if output in other_node.get('inputs', []):
                return False
        
        return True
    
    def _find_observability_dont_cares(self, node: Dict[str, Any], netlist: Dict[str, Any]) -> Set[Tuple[bool, ...]]:
        """
        Find Observability Don't Care conditions.
        
        Simplified implementation - in practice, this would use more sophisticated algorithms.
        """
        dont_cares = set()
        
        # Simple heuristic: if node output has multiple fanouts with different functions,
        # some input combinations might be don't cares
        
        output = node.get('output')
        if not output:
            return dont_cares
        
        # Find fanout nodes
        fanout_nodes = []
        for other_node in netlist.get('nodes', {}).values():
            if output in other_node.get('inputs', []):
                fanout_nodes.append(other_node)
        
        # If multiple fanouts, analyze for potential don't cares
        if len(fanout_nodes) > 1:
            # This is a simplified analysis
            # In practice, you'd use more sophisticated algorithms
            pass
        
        return dont_cares
    
    def _apply_dont_care_optimization(self, netlist: Dict[str, Any], reachable_nodes: Set[str]) -> Set[str]:
        """
        Apply Don't Care optimization to expand reachable nodes.
        
        Uses Don't Care conditions to identify additional nodes that can be removed.
        """
        logger.debug("Applying Don't Care optimization...")
        
        nodes = netlist.get('nodes', {})
        additional_removable = set()
        
        for node_name, node in nodes.items():
            if node_name in reachable_nodes:
                continue
            
            # Check if node can be removed due to don't cares
            if node_name in self.dont_cares:
                dont_care_conditions = self.dont_cares[node_name]
                
                # If all possible input combinations are don't cares, node can be removed
                inputs = node.get('inputs', [])
                total_combinations = 2 ** len(inputs)
                
                if len(dont_care_conditions) >= total_combinations:
                    additional_removable.add(node_name)
                    logger.debug(f"Node {node_name} removable due to don't cares")
        
        # Update reachable nodes (nodes that should NOT be removed)
        all_nodes = set(nodes.keys())
        removable_nodes = all_nodes - reachable_nodes - additional_removable
        final_reachable = all_nodes - removable_nodes
        
        return final_reachable
    
    def _remove_redundant_nodes(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove redundant nodes in aggressive optimization mode.
        
        Identifies and removes nodes that are functionally equivalent.
        """
        logger.debug("Removing redundant nodes...")
        
        nodes = netlist.get('nodes', {})
        redundant_pairs = []
        
        # Find functionally equivalent nodes
        for node1_name, node1 in list(nodes.items()):
            for node2_name, node2 in list(nodes.items()):
                if node1_name >= node2_name:  # Avoid duplicate checks
                    continue
                
                if self._are_nodes_equivalent(node1, node2, netlist):
                    redundant_pairs.append((node1_name, node2_name))
        
        # Remove redundant nodes (keep the first one)
        for node1_name, node2_name in redundant_pairs:
            if node2_name in nodes:
                del nodes[node2_name]
                self.removed_nodes += 1
                logger.debug(f"Removed redundant node: {node2_name} (equivalent to {node1_name})")
        
        netlist['nodes'] = nodes
        return netlist
    
    def _are_nodes_equivalent(self, node1: Dict[str, Any], node2: Dict[str, Any], netlist: Dict[str, Any]) -> bool:
        """
        Check if two nodes are functionally equivalent.
        
        Simplified implementation - in practice, this would use more sophisticated algorithms.
        """
        # Same gate type and inputs
        if (node1.get('type') == node2.get('type') and 
            node1.get('inputs') == node2.get('inputs')):
            return True
        
        # Additional equivalence checks could be added here
        # such as checking for logical equivalence using SAT solver
        
        return False
    
    def get_stats(self) -> Dict[str, int]:
        """
        Get optimization statistics.
        
        Returns:
            Dictionary with optimization statistics
        """
        return {
            'removed_nodes': self.removed_nodes,
            'removed_wires': self.removed_wires
        }

def dead_code_elimination(netlist: Dict[str, Any], level: str = "basic") -> Dict[str, Any]:
    """
    Apply Dead Code Elimination to a netlist.
    
    Args:
        netlist: Circuit netlist
        level: Optimization level ("basic", "advanced", "aggressive")
        
    Returns:
        Optimized netlist with dead code removed
    """
    optimizer = DCEOptimizer()
    return optimizer.optimize(netlist, level)

def apply_dce(netlist: Dict[str, Any], level: str = "basic") -> Dict[str, Any]:
    """Alias wrapper to match synthesis_flow usage."""
    optimizer = DCEOptimizer()
    return optimizer.optimize(netlist, level)

def dce_analysis(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyze netlist for dead code without removing it.
    
    Args:
        netlist: Circuit netlist
        
    Returns:
        Analysis results showing dead nodes and wires
    """
    optimizer = DCEOptimizer()
    
    # Find reachable nodes
    reachable_nodes = optimizer._find_reachable_nodes(netlist)
    
    # Find dead nodes
    nodes = netlist.get('nodes', {})
    dead_nodes = [name for name in nodes if name not in reachable_nodes]
    
    # Find dead wires
    dead_wires = []
    wires = netlist.get('wires', [])
    for wire in wires:
        if isinstance(wire, dict):
            source = wire.get('source')
            sink = wire.get('sink')
            
            # Check if wire is dead
            source_dead = True
            sink_dead = True
            
            # Check source
            if source in netlist.get('inputs', []):
                source_dead = False
            else:
                for node in nodes.values():
                    if node.get('output') == source and node.get('name') in reachable_nodes:
                        source_dead = False
                        break
            
            # Check sink
            for node in nodes.values():
                if sink in node.get('inputs', []) and node.get('name') in reachable_nodes:
                    sink_dead = False
                    break
            
            if source_dead or sink_dead:
                dead_wires.append(wire)
    
    return {
        'total_nodes': len(nodes),
        'reachable_nodes': len(reachable_nodes),
        'dead_nodes': dead_nodes,
        'dead_wires': dead_wires,
        'optimization_potential': len(dead_nodes) + len(dead_wires)
    }

# Example usage and testing
if __name__ == "__main__":
    # Example netlist with dead code
    example_netlist = {
        'name': 'test_circuit',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': {
            'n1': {
                'type': 'AND',
                'inputs': ['a', 'b'],
                'output': 'temp1',
                'name': 'n1'
            },
            'n2': {
                'type': 'OR',
                'inputs': ['a', 'b'],
                'output': 'temp2',
                'name': 'n2'
            },
            'n3': {
                'type': 'XOR',
                'inputs': ['temp1', 'temp2'],
                'output': 'out',
                'name': 'n3'
            },
            'n4': {  # Dead node - not connected to output
                'type': 'AND',
                'inputs': ['temp1', 'temp2'],
                'output': 'dead_out',
                'name': 'n4'
            }
        },
        'wires': [
            {'source': 'a', 'sink': 'n1'},
            {'source': 'b', 'sink': 'n1'},
            {'source': 'a', 'sink': 'n2'},
            {'source': 'b', 'sink': 'n2'},
            {'source': 'temp1', 'sink': 'n3'},
            {'source': 'temp2', 'sink': 'n3'},
            {'source': 'temp1', 'sink': 'n4'},  # Dead wire
            {'source': 'temp2', 'sink': 'n4'}   # Dead wire
        ]
    }
    
    print("Original netlist:")
    print(f"Nodes: {len(example_netlist['nodes'])}")
    print(f"Wires: {len(example_netlist['wires'])}")
    
    # Analyze dead code
    analysis = dce_analysis(example_netlist)
    print(f"\nDCE Analysis:")
    print(f"Dead nodes: {analysis['dead_nodes']}")
    print(f"Dead wires: {len(analysis['dead_wires'])}")
    print(f"Optimization potential: {analysis['optimization_potential']}")
    
    # Apply DCE
    optimized = apply_dce(example_netlist)
    print(f"\nAfter DCE:")
    print(f"Nodes: {len(optimized['nodes'])}")
    print(f"Wires: {len(optimized['wires'])}")
    
    # Show removed nodes
    removed_nodes = set(example_netlist['nodes'].keys()) - set(optimized['nodes'].keys())
    print(f"Removed nodes: {list(removed_nodes)}")
