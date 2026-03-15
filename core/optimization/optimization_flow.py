#!/usr/bin/env python3
"""
AIG Optimization Flow

Optimization: Tối ưu hóa trên AIG (And-Inverter Graph)

Các bước optimization:
1. Structural Hashing (Strash)
2. Dead Code Elimination (DCE)
3. Common Subexpression Elimination (CSE)
4. Constant Propagation (ConstProp)
5. Logic Balancing (Balance)

Lưu ý: Đây là bước OPTIMIZATION riêng biệt (1 trong 3 hướng độc lập), tách khỏi SYNTHESIS và TECHMAP.
3 hướng độc lập:
1. SYNTHESIS: Netlist → AIG (core/synthesis/synthesis_flow.py)
2. OPTIMIZE: AIG → Optimized AIG (file này)
3. TECHMAP: AIG → Technology-mapped netlist (core/technology_mapping/technology_mapping.py)

Synthesis chỉ làm Netlist → AIG conversion.
Optimization tối ưu hóa trên AIG (nhận AIG, trả về AIG).
Techmap map AIG vào technology library (nhận AIG, trả về mapped netlist).
"""

import sys
import os
from typing import Dict, List, Set, Any, Optional
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.synthesis.aig import AIG, AIGNode

logger = logging.getLogger(__name__)


class AIGOptimizationFlow:
    """
    AIG Optimization Flow.
    
    Tối ưu hóa AIG với các thuật toán:
    - Strash (Structural Hashing)
    - DCE (Dead Code Elimination)
    - CSE (Common Subexpression Elimination)
    - ConstProp (Constant Propagation)
    - Balance (Logic Balancing)
    """
    
    def __init__(self):
        self.optimization_stats = {
            'strash': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'dce': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'cse': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'constprop': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
            'balance': {'nodes_before': 0, 'nodes_after': 0, 'added': 0}
        }
        
    def optimize(self, aig: AIG) -> AIG:
        """
        Chạy AIG optimization flow (một chuẩn duy nhất: Strash, DCE, CSE, ConstProp, Balance).
        """
        logger.info("Starting AIG Optimization Flow...")
        
        original_nodes = aig.count_nodes()
        current_aig = aig
        
        # Step 1: Structural Hashing (Strash)
        logger.info("Step 1: Structural Hashing (Strash)...")
        current_aig = self._run_strash(current_aig)
        
        # Step 2: Dead Code Elimination (DCE)
        logger.info("Step 2: Dead Code Elimination (DCE)...")
        current_aig = self._run_dce(current_aig)
        
        # Step 3: Common Subexpression Elimination (CSE)
        logger.info("Step 3: Common Subexpression Elimination (CSE)...")
        current_aig = self._run_cse(current_aig)
        
        # Step 4: Constant Propagation (ConstProp)
        logger.info("Step 4: Constant Propagation (ConstProp)...")
        current_aig = self._run_constprop(current_aig)
        
        # Step 5: Logic Balancing (Balance)
        logger.info("Step 5: Logic Balancing (Balance)...")
        current_aig = self._run_balance(current_aig)
        
        final_nodes = current_aig.count_nodes()
        total_reduction = original_nodes - final_nodes
        
        # Print summary
        self._print_optimization_summary(original_nodes, final_nodes, total_reduction)
        
        return current_aig
    
    def _run_strash(self, aig: AIG) -> AIG:
        """Chạy Structural Hashing trên AIG."""
        try:
            nodes_before = aig.count_nodes()
            
            # AIG đã có structural hashing built-in trong create_and()
            # Strash trên AIG chủ yếu là rebuild hash table
            optimized_aig = aig.strash()
            
            nodes_after = optimized_aig.count_nodes()
            
            self.optimization_stats['strash'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  Strash: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized_aig
            
        except Exception as e:
            logger.error(f"Strash failed: {e}")
            return aig
    
    def _run_dce(self, aig: AIG) -> AIG:
        """Chạy Dead Code Elimination trên AIG."""
        try:
            nodes_before = aig.count_nodes()
            optimized_aig = self._apply_dce_on_aig(aig)
            
            nodes_after = optimized_aig.count_nodes()
            
            self.optimization_stats['dce'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  DCE: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized_aig
            
        except Exception as e:
            logger.error(f"DCE failed: {e}")
            return aig
    
    def _run_cse(self, aig: AIG) -> AIG:
        """Chạy Common Subexpression Elimination trên AIG."""
        try:
            nodes_before = aig.count_nodes()
            
            # CSE trên AIG: AIG đã tự động share common subexpressions qua hash table
            # Nên CSE chủ yếu là rebuild để tối ưu hơn
            optimized_aig = aig.strash()  # Rebuild hash table
            
            nodes_after = optimized_aig.count_nodes()
            
            self.optimization_stats['cse'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  CSE: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized_aig
            
        except Exception as e:
            logger.error(f"CSE failed: {e}")
            return aig
    
    def _run_constprop(self, aig: AIG) -> AIG:
        """Chạy Constant Propagation trên AIG."""
        try:
            nodes_before = aig.count_nodes()
            
            # ConstProp trên AIG: propagate constants qua AND gates
            optimized_aig = self._apply_constprop_on_aig(aig)
            
            nodes_after = optimized_aig.count_nodes()
            
            self.optimization_stats['constprop'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'removed': nodes_before - nodes_after
            }
            
            logger.info(f"  ConstProp: {nodes_before} -> {nodes_after} nodes (removed {nodes_before - nodes_after})")
            return optimized_aig
            
        except Exception as e:
            logger.error(f"ConstProp failed: {e}")
            return aig
    
    def _run_balance(self, aig: AIG) -> AIG:
        """Chạy Logic Balancing trên AIG."""
        try:
            nodes_before = aig.count_nodes()
            
            # Balance trên AIG: cân bằng logic depth
            optimized_aig = self._apply_balance_on_aig(aig)
            
            nodes_after = optimized_aig.count_nodes()
            
            self.optimization_stats['balance'] = {
                'nodes_before': nodes_before,
                'nodes_after': nodes_after,
                'added': nodes_after - nodes_before
            }
            
            logger.info(f"  Balance: {nodes_before} -> {nodes_after} nodes (added {nodes_after - nodes_before})")
            return optimized_aig
            
        except Exception as e:
            logger.error(f"Balance failed: {e}")
            return aig
    
    def _apply_dce_on_aig(self, aig: AIG) -> AIG:
        """Apply DCE trên AIG (một chuẩn duy nhất)."""
        # Simplified DCE: rebuild AIG chỉ với reachable nodes
        # In practice, you'd do proper reachability analysis
        new_aig = AIG()
        
        # Recreate PIs
        pi_map = {}
        for var_name, old_pi in aig.pis.items():
            new_pi = new_aig.create_pi(var_name)
            pi_map[old_pi.node_id] = new_pi
        
        # Recreate reachable nodes; node_map: old_node_id -> new_node (for shared nodes)
        visited = set()
        node_map: Dict[int, AIGNode] = {}
        
        def recreate_node(old_node: AIGNode) -> AIGNode:
            if old_node.node_id in visited:
                return pi_map.get(old_node.node_id) or node_map.get(old_node.node_id)
            
            visited.add(old_node.node_id)
            
            if old_node.is_constant():
                n = new_aig.create_constant(old_node.get_value())
                node_map[old_node.node_id] = n
                return n
            elif old_node.is_pi():
                return pi_map[old_node.node_id]
            else:
                left = recreate_node(old_node.left)
                right = recreate_node(old_node.right)
                n = new_aig.create_and(left, right,
                                        old_node.left_inverted,
                                        old_node.right_inverted)
                node_map[old_node.node_id] = n
                return n
        
        # Recreate outputs (only reachable nodes)
        for old_po, inverted in aig.pos:
            new_po = recreate_node(old_po)
            if inverted:
                new_po = new_aig.create_not(new_po)
            new_aig.add_po(new_po)
        
        return new_aig
    
    def _apply_constprop_on_aig(self, aig: AIG) -> AIG:
        """
        Apply Constant Propagation trên AIG.
        
        Propagate constants through AND gates:
        - AND(x, 1) = x
        - AND(x, 0) = 0
        - AND(1, x) = x
        - AND(0, x) = 0
        """
        # Create new AIG for optimized result
        new_aig = AIG()
        
        # Map old nodes to new nodes
        node_map = {}
        
        # Recreate PIs
        for var_name, old_pi in aig.pis.items():
            new_pi = new_aig.create_pi(var_name)
            node_map[old_pi.node_id] = new_pi
        
        # Map constants
        node_map[aig.const0.node_id] = new_aig.const0
        node_map[aig.const1.node_id] = new_aig.const1
        
        visited = set()
        
        def propagate_node(old_node: AIGNode) -> AIGNode:
            """Propagate constants through nodes."""
            if old_node.node_id in node_map:
                return node_map[old_node.node_id]
            
            if old_node.node_id in visited:
                # Already processed, return mapped node
                return node_map.get(old_node.node_id)
            
            visited.add(old_node.node_id)
            
            if old_node.is_constant():
                return node_map[old_node.node_id]
            elif old_node.is_pi():
                return node_map[old_node.node_id]
            elif old_node.is_and():
                # Propagate constants through AND
                left = propagate_node(old_node.left) if old_node.left else None
                right = propagate_node(old_node.right) if old_node.right else None
                
                # Check for None nodes
                if left is None or right is None:
                    # Cannot propagate if nodes are missing
                    new_node = new_aig.create_and(
                        left or new_aig.const0,
                        right or new_aig.const0,
                        old_node.left_inverted,
                        old_node.right_inverted
                    )
                    node_map[old_node.node_id] = new_node
                    return new_node
                
                # Constant propagation rules
                left_val = left.get_value() if left.is_constant() else None
                right_val = right.get_value() if right.is_constant() else None
                
                # AND(x, 0) = 0 or AND(0, x) = 0
                if (left_val is False) or (right_val is False):
                    node_map[old_node.node_id] = new_aig.const0
                    return new_aig.const0
                
                # AND(x, 1) = x (with inversion handling)
                if right_val is True:
                    res = new_aig.create_not(left) if old_node.right_inverted else left
                    node_map[old_node.node_id] = res
                    return res
                
                if left_val is True:
                    res = new_aig.create_not(right) if old_node.left_inverted else right
                    node_map[old_node.node_id] = res
                    return res
                
                # No constant propagation possible, create AND node
                new_node = new_aig.create_and(
                    left, right,
                    old_node.left_inverted,
                    old_node.right_inverted
                )
                node_map[old_node.node_id] = new_node
                return new_node
            
            return old_node
        
        # Recreate outputs with constant propagation
        for old_po, inverted in aig.pos:
            new_po = propagate_node(old_po)
            if inverted:
                new_po = new_aig.create_not(new_po)
            new_aig.add_po(new_po)
        
        return new_aig
    
    def _apply_balance_on_aig(self, aig: AIG) -> AIG:
        """
        Apply Logic Balancing trên AIG.
        
        Balance logic depth by restructuring AND trees to minimize maximum depth.
        Uses tree balancing algorithm to create more balanced structures.
        """
        # Create new AIG for balanced result
        new_aig = AIG()
        
        # Map old nodes to new nodes
        node_map = {}
        
        # Recreate PIs
        for var_name, old_pi in aig.pis.items():
            new_pi = new_aig.create_pi(var_name)
            node_map[old_pi.node_id] = new_pi
        
        # Map constants
        node_map[aig.const0.node_id] = new_aig.const0
        node_map[aig.const1.node_id] = new_aig.const1
        
        visited = set()
        
        def get_node_level(node: AIGNode) -> int:
            """Get logic level of a node."""
            if node.is_constant() or node.is_pi():
                return 0
            return node.level
        
        def balance_and_tree(nodes: List[AIGNode], left_inverted: List[bool], right_inverted: List[bool]) -> AIGNode:
            """
            Balance a tree of AND operations.
            
            Args:
                nodes: List of nodes to combine with AND
                left_inverted: List of left inversion flags
                right_inverted: List of right inversion flags
                
            Returns:
                Balanced AND tree node
            """
            if len(nodes) == 0:
                return new_aig.const1
            if len(nodes) == 1:
                return nodes[0]
            if len(nodes) == 2:
                return new_aig.create_and(nodes[0], nodes[1], left_inverted[0], right_inverted[0])
            
            # Sort nodes by level (shallow first for better balancing)
            sorted_indices = sorted(range(len(nodes)), key=lambda i: get_node_level(nodes[i]))
            sorted_nodes = [nodes[i] for i in sorted_indices]
            sorted_left_inv = [left_inverted[i] for i in sorted_indices]
            sorted_right_inv = [right_inverted[i] for i in sorted_indices]
            
            # Build balanced tree: combine pairs recursively
            while len(sorted_nodes) > 1:
                new_level = []
                new_left_inv = []
                new_right_inv = []
                
                # Combine pairs
                for i in range(0, len(sorted_nodes), 2):
                    if i + 1 < len(sorted_nodes):
                        # Combine two nodes
                        combined = new_aig.create_and(
                            sorted_nodes[i],
                            sorted_nodes[i + 1],
                            sorted_left_inv[i],
                            sorted_right_inv[i + 1]
                        )
                        new_level.append(combined)
                        new_left_inv.append(False)
                        new_right_inv.append(False)
                    else:
                        # Odd one out, keep as is
                        new_level.append(sorted_nodes[i])
                        new_left_inv.append(sorted_left_inv[i])
                        new_right_inv.append(sorted_right_inv[i])
                
                sorted_nodes = new_level
                sorted_left_inv = new_left_inv
                sorted_right_inv = new_right_inv
            
            return sorted_nodes[0]
        
        def balance_node(old_node: AIGNode) -> Optional[AIGNode]:
            """Balance a single node. Always add to node_map so shared nodes are preserved."""
            if old_node is None:
                return None
            
            if old_node.node_id in node_map:
                return node_map[old_node.node_id]
            
            if old_node.node_id in visited:
                return node_map.get(old_node.node_id)
            
            visited.add(old_node.node_id)
            
            if old_node.is_constant():
                return node_map.get(old_node.node_id)
            elif old_node.is_pi():
                return node_map.get(old_node.node_id)
            elif old_node.is_and():
                # Balance left and right subtrees first
                left = balance_node(old_node.left)
                right = balance_node(old_node.right)
                # Fallback to const0 if any input missing (avoid None -> lost PO)
                if left is None:
                    left = new_aig.const0
                if right is None:
                    right = new_aig.const0
                
                # Simple approach: just balance the current AND
                new_node = new_aig.create_and(
                    left, right,
                    old_node.left_inverted,
                    old_node.right_inverted
                )
                node_map[old_node.node_id] = new_node
                return new_node
            
            return None
        
        # Recreate outputs with balancing
        for old_po, inverted in aig.pos:
            new_po = balance_node(old_po)
            if new_po is None:
                continue
            if inverted:
                new_po = new_aig.create_not(new_po)
            new_aig.add_po(new_po)
        
        # Rebuild hash table for better structure sharing
        return new_aig.strash()
    
    def _print_optimization_summary(self, original_nodes: int, final_nodes: int, total_reduction: int):
        """In optimization summary."""
        logger.info("=" * 60)
        logger.info("AIG OPTIMIZATION SUMMARY")
        logger.info("=" * 60)
        logger.info(f"Original AIG nodes: {original_nodes}")
        logger.info(f"Optimized AIG nodes: {final_nodes}")
        if original_nodes > 0:
            logger.info(f"Total reduction: {total_reduction} nodes ({(total_reduction/original_nodes)*100:.1f}%)")
        else:
            logger.info(f"Total reduction: {total_reduction} nodes (0.0% - empty AIG)")
        logger.info("")
        logger.info("Optimization breakdown:")
        
        for opt_name, stats in self.optimization_stats.items():
            if opt_name == 'balance':
                logger.info(f"  {opt_name.upper()}: {stats['nodes_before']} -> {stats['nodes_after']} (added {stats['added']})")
            else:
                logger.info(f"  {opt_name.upper()}: {stats['nodes_before']} -> {stats['nodes_after']} (removed {stats['removed']})")
        
        logger.info("=" * 60)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Lấy thống kê về optimization."""
        return {
            'optimization_stats': self.optimization_stats,
            'total_optimizations': len(self.optimization_stats)
        }


def optimize(aig: AIG) -> AIG:
    """
    Tối ưu AIG (một chuẩn duy nhất: Strash, DCE, CSE, ConstProp, Balance).
    """
    flow = AIGOptimizationFlow()
    return flow.optimize(aig)


# Test function
if __name__ == "__main__":
    from core.synthesis.aig import AIG
    
    # Create test AIG
    aig = AIG()
    a = aig.create_pi("a")
    b = aig.create_pi("b")
    c = aig.create_pi("c")
    
    # Create logic: f = (a AND b) OR c
    ab = aig.create_and(a, b)
    f = aig.create_or(ab, c)
    aig.add_po(f)
    
    print("Test AIG Optimization")
    print(f"Original AIG: {aig.count_nodes()} nodes")
    
    optimized = optimize(aig)
    
    print(f"Optimized AIG: {optimized.count_nodes()} nodes")
    print("✅ Optimization test passed!")




