#!/usr/bin/env python3
"""
And-Inverter Graph (AIG) Implementation

AIG là một cấu trúc dữ liệu quan trọng trong logic synthesis,
đặc biệt được sử dụng trong ABC (Berkeley Logic Synthesis Tool).

Dựa trên các khái niệm VLSI CAD Part I và tham khảo từ ABC.

ABC Reference: src/aig/aig/aig.h
- Aig_Man: AIG manager
- Aig_Obj: AIG node
- Structural hashing với AIG
"""

from typing import Dict, List, Set, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class AIGNode:
    """
    AIG Node representation.
    
    Mỗi node trong AIG có thể là:
    - Constant 0 (False)
    - Constant 1 (True)
    - Primary input (PI)
    - AND gate với 2 inputs (có thể có inversion)
    """
    
    def __init__(self, node_id: int, node_type: str = 'AND',
                 left: Optional['AIGNode'] = None,
                 right: Optional['AIGNode'] = None,
                 left_inverted: bool = False,
                 right_inverted: bool = False,
                 var_name: Optional[str] = None):
        """
        Initialize AIG node.
        
        Args:
            node_id: Unique node ID
            node_type: 'CONST0', 'CONST1', 'PI' (Primary Input), 'AND'
            left: Left child (for AND nodes)
            right: Right child (for AND nodes)
            left_inverted: Whether left input is inverted
            right_inverted: Whether right input is inverted
            var_name: Variable name (for PI nodes)
        """
        self.node_id = node_id
        self.node_type = node_type
        self.left = left
        self.right = right
        self.left_inverted = left_inverted
        self.right_inverted = right_inverted
        self.var_name = var_name
        self.ref_count = 0
        self.level = 0  # Logic level
    
    def is_constant(self) -> bool:
        """Check if this is a constant node."""
        return self.node_type in ['CONST0', 'CONST1']
    
    def is_pi(self) -> bool:
        """Check if this is a primary input."""
        return self.node_type == 'PI'
    
    def is_and(self) -> bool:
        """Check if this is an AND node."""
        return self.node_type == 'AND'
    
    def get_value(self) -> Optional[bool]:
        """Get constant value if this is a constant."""
        if self.node_type == 'CONST0':
            return False
        elif self.node_type == 'CONST1':
            return True
        return None
    
    def __repr__(self):
        if self.is_constant():
            return f"AIG_{self.node_type}(id={self.node_id})"
        elif self.is_pi():
            return f"AIG_PI({self.var_name}, id={self.node_id})"
        else:
            left_str = f"{'!' if self.left_inverted else ''}L{self.left.node_id if self.left else 'None'}"
            right_str = f"{'!' if self.right_inverted else ''}R{self.right.node_id if self.right else 'None'}"
            return f"AIG_AND(id={self.node_id}, {left_str}, {right_str})"


class AIG:
    """
    And-Inverter Graph (AIG) Manager.
    
    AIG là một cấu trúc dữ liệu để biểu diễn logic circuits chỉ sử dụng
    AND gates và inverters. Đây là canonical form được sử dụng rộng rãi
    trong logic synthesis.
    """
    
    def __init__(self):
        """Initialize AIG manager."""
        # Node storage
        self.nodes: Dict[int, AIGNode] = {}
        self.next_node_id = 0
        
        # Constant nodes (singleton)
        self.const0 = self._create_node('CONST0')
        self.const1 = self._create_node('CONST1')
        
        # Primary inputs
        self.pis: Dict[str, AIGNode] = {}
        
        # Primary outputs
        self.pos: List[Tuple[AIGNode, bool]] = []  # (node, inverted)
        
        # Structural hashing table
        # Key: (left_id, right_id, left_inv, right_inv) -> node_id
        self.hash_table: Dict[Tuple[int, int, bool, bool], int] = {}
        
        # Level information
        self.max_level = 0
    
    def _create_node(self, node_type: str, **kwargs) -> AIGNode:
        """Create a new AIG node."""
        node_id = self.next_node_id
        self.next_node_id += 1
        
        node = AIGNode(node_id, node_type, **kwargs)
        self.nodes[node_id] = node
        
        return node
    
    def create_constant(self, value: bool) -> AIGNode:
        """Create or return constant node."""
        return self.const1 if value else self.const0
    
    def create_pi(self, var_name: str) -> AIGNode:
        """Create primary input node."""
        if var_name in self.pis:
            return self.pis[var_name]
        
        node = self._create_node('PI', var_name=var_name)
        self.pis[var_name] = node
        return node
    
    def create_and(self, left: AIGNode, right: AIGNode,
                   left_inverted: bool = False,
                   right_inverted: bool = False) -> AIGNode:
        """
        Create AND node with structural hashing.
        
        Đây là hàm quan trọng nhất trong AIG - sử dụng structural hashing
        để tránh duplicate nodes.
        """
        # Normalize: ensure left_id <= right_id for canonical form
        left_id = left.node_id
        right_id = right.node_id
        
        if left_id > right_id:
            left, right = right, left
            left_inverted, right_inverted = right_inverted, left_inverted
            left_id, right_id = right_id, left_id
        
        # Check hash table
        key = (left_id, right_id, left_inverted, right_inverted)
        if key in self.hash_table:
            return self.nodes[self.hash_table[key]]
        
        # Check for constant simplifications
        left_val = left.get_value()
        right_val = right.get_value()
        
        if left_val is not None:
            # Left is constant
            if left_val ^ left_inverted:  # Left is True
                return right if not right_inverted else self._create_not(right)
            else:  # Left is False
                return self.const0
        
        if right_val is not None:
            # Right is constant
            if right_val ^ right_inverted:  # Right is True
                return left if not left_inverted else self._create_not(left)
            else:  # Right is False
                return self.const0
        
        # Check for tautology (x AND !x = 0)
        if left == right and left_inverted != right_inverted:
            return self.const0
        
        # Create new AND node
        node = self._create_node('AND', 
                                left=left, right=right,
                                left_inverted=left_inverted,
                                right_inverted=right_inverted)
        
        # Update level
        node.level = max(left.level, right.level) + 1
        self.max_level = max(self.max_level, node.level)
        
        # Store in hash table
        self.hash_table[key] = node.node_id
        
        return node
    
    def _create_not(self, node: AIGNode) -> AIGNode:
        """
        Create NOT by inverting.
        
        Trong AIG, NOT được biểu diễn bằng cách invert input của AND.
        """
        if node.is_constant():
            return self.create_constant(not node.get_value())
        
        # For non-constants, we create AND with constant 1
        # In practice, inversion is handled by flags
        # Here we create a special structure
        return self.create_and(node, self.const1, left_inverted=True)
    
    def create_not(self, node: AIGNode) -> AIGNode:
        """Create NOT node (wrapper for _create_not)."""
        return self._create_not(node)
    
    def create_or(self, left: AIGNode, right: AIGNode) -> AIGNode:
        """Create OR using De Morgan's law: a OR b = !(!a AND !b)."""
        not_left = self.create_not(left)
        not_right = self.create_not(right)
        and_node = self.create_and(not_left, not_right)
        return self.create_not(and_node)
    
    def create_xor(self, left: AIGNode, right: AIGNode) -> AIGNode:
        """Create XOR: a XOR b = (!a AND b) OR (a AND !b)."""
        not_left = self.create_not(left)
        not_right = self.create_not(right)
        term1 = self.create_and(not_left, right)
        term2 = self.create_and(left, not_right)
        return self.create_or(term1, term2)
    
    def add_po(self, node: AIGNode, inverted: bool = False):
        """Add primary output."""
        self.pos.append((node, inverted))
    
    def strash(self) -> 'AIG':
        """
        Structural hashing - loại bỏ duplicate nodes.
        
        Đây là thuật toán tương tự như Strash trong ABC.
        """
        # AIG already uses structural hashing in create_and
        # This method can be used to rebuild hash table after modifications
        new_aig = AIG()
        
        # Recreate PIs
        pi_map = {}
        for var_name, old_pi in self.pis.items():
            new_pi = new_aig.create_pi(var_name)
            pi_map[old_pi.node_id] = new_pi
        
        # Recreate nodes in topological order
        # This is a simplified version - in practice, you'd do proper topological sort
        visited = set()
        
        def recreate_node(old_node: AIGNode) -> AIGNode:
            if old_node.node_id in visited:
                return pi_map.get(old_node.node_id) or new_aig.nodes.get(old_node.node_id)
            
            visited.add(old_node.node_id)
            
            if old_node.is_constant():
                return new_aig.create_constant(old_node.get_value())
            elif old_node.is_pi():
                return pi_map[old_node.node_id]
            else:
                left = recreate_node(old_node.left)
                right = recreate_node(old_node.right)
                return new_aig.create_and(left, right,
                                         old_node.left_inverted,
                                         old_node.right_inverted)
        
        # Recreate outputs
        for old_po, inverted in self.pos:
            new_po = recreate_node(old_po)
            if inverted:
                new_po = new_aig.create_not(new_po)
            new_aig.add_po(new_po)
        
        return new_aig
    
    def count_nodes(self) -> int:
        """Count total number of nodes."""
        return len(self.nodes)
    
    def count_and_nodes(self) -> int:
        """Count number of AND nodes."""
        return sum(1 for node in self.nodes.values() if node.is_and())
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get AIG statistics."""
        return {
            'total_nodes': self.count_nodes(),
            'and_nodes': self.count_and_nodes(),
            'pi_count': len(self.pis),
            'po_count': len(self.pos),
            'max_level': self.max_level,
            'hash_table_size': len(self.hash_table)
        }
    
    def to_verilog(self, module_name: str = "aig_module") -> str:
        """Convert AIG to Verilog code."""
        lines = [f"module {module_name}("]
        
        # Inputs
        pi_names = list(self.pis.keys())
        if pi_names:
            lines.append(f"  input {', '.join(pi_names)},")
        
        # Outputs
        po_names = [f"out{i}" for i in range(len(self.pos))]
        if po_names:
            lines.append(f"  output {', '.join(po_names)}")
        
        lines.append(");")
        lines.append("")
        
        # Wire declarations
        wire_names = {}
        for node_id, node in self.nodes.items():
            if not node.is_constant() and not node.is_pi():
                wire_names[node_id] = f"w{node_id}"
        
        if wire_names:
            lines.append("  // Internal wires")
            for node_id, wire_name in wire_names.items():
                lines.append(f"  wire {wire_name};")
            lines.append("")
        
        # Generate logic
        for node_id, node in self.nodes.items():
            if node.is_constant():
                continue
            elif node.is_pi():
                continue
            elif node.is_and():
                left_expr = self._node_to_expr(node.left, wire_names, node.left_inverted)
                right_expr = self._node_to_expr(node.right, wire_names, node.right_inverted)
                wire_name = wire_names[node_id]
                lines.append(f"  assign {wire_name} = {left_expr} & {right_expr};")
        
        # Outputs
        lines.append("")
        lines.append("  // Outputs")
        for i, (po_node, inverted) in enumerate(self.pos):
            po_expr = self._node_to_expr(po_node, wire_names, inverted)
            lines.append(f"  assign {po_names[i]} = {po_expr};")
        
        lines.append("")
        lines.append("endmodule")
        
        return "\n".join(lines)
    
    def _node_to_expr(self, node: AIGNode, wire_names: Dict[int, str], inverted: bool) -> str:
        """Convert node to Verilog expression."""
        if node.is_constant():
            val = "1'b1" if node.get_value() else "1'b0"
            return f"~{val}" if inverted else val
        elif node.is_pi():
            expr = node.var_name
            return f"~{expr}" if inverted else expr
        else:
            expr = wire_names[node.node_id]
            return f"~{expr}" if inverted else expr


# Example usage and testing
if __name__ == "__main__":
    # Create AIG
    aig = AIG()
    
    # Create inputs
    a = aig.create_pi("a")
    b = aig.create_pi("b")
    c = aig.create_pi("c")
    
    # Create logic: f = (a AND b) OR c
    ab = aig.create_and(a, b)
    f = aig.create_or(ab, c)
    
    # Add as output
    aig.add_po(f)
    
    print("AIG Example:")
    print(f"  Total nodes: {aig.count_nodes()}")
    print(f"  AND nodes: {aig.count_and_nodes()}")
    print(f"  PIs: {len(aig.pis)}")
    print(f"  POs: {len(aig.pos)}")
    print(f"  Max level: {aig.max_level}")
    print()
    
    # Statistics
    stats = aig.get_statistics()
    print("Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    print()
    
    # Verilog output
    print("Verilog:")
    print(aig.to_verilog("example_aig"))

