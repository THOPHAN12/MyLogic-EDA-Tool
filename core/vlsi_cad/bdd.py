#!/usr/bin/env python3
"""
Binary Decision Diagrams (BDD) Implementation

Dựa trên các khái niệm VLSI CAD Part 1 và tham khảo từ ABC (YosysHQ/abc).
Biểu diễn và thao tác logic với BDD structure.

ABC Reference: src/bdd/bdd.c
- Bdd_And(), Bdd_Or(), Bdd_Not(): Basic operations
- Bdd_Exist(), Bdd_Forall(): Quantification operations
- Bdd_Compose(): Function composition
- Variable reordering và optimization
"""

from typing import Dict, List, Set, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class BDDNode:
    """BDD Node representation."""
    
    def __init__(self, var_id: int, low: 'BDDNode' = None, high: 'BDDNode' = None, value: Optional[bool] = None):
        self.var_id = var_id  # Variable ID (0 for terminal nodes)
        self.low = low        # Low (0) child
        self.high = high      # High (1) child
        self.value = value    # Terminal value (for terminal nodes)
        self.ref_count = 0    # Reference count for garbage collection
        
    def is_terminal(self) -> bool:
        """Check if this is a terminal node."""
        return self.var_id == 0
    
    def __repr__(self):
        if self.is_terminal():
            return f"T({self.value})"
        else:
            return f"V{self.var_id}"

class BDD:
    """
    Triển khai Binary Decision Diagram.
    
    Dựa trên các khái niệm VLSI CAD Part 1 để biểu diễn hàm Boolean hiệu quả.
    """
    
    def __init__(self):
        # ABC-inspired BDD structure
        self.nodes: Dict[Tuple[int, 'BDDNode', 'BDDNode'], 'BDDNode'] = {}  # Bảng unique
        self.var_order: List[str] = []  # Thứ tự biến
        self.var_to_id: Dict[str, int] = {}  # Mapping tên biến đến ID
        self.id_to_var: Dict[int, str] = {}  # Mapping ID đến tên biến
        self.next_var_id = 1
        
        # ABC-style computed table for operation caching
        self.computed_table: Dict[Tuple[str, int, int], int] = {}
        self.operation_cache: Dict[Tuple[str, int, int], int] = {}
        
        # Terminal nodes
        self.terminal_true = BDDNode(0, value=True)
        self.terminal_false = BDDNode(0, value=False)
        
    def get_var_id(self, var_name: str) -> int:
        """Lấy hoặc tạo variable ID."""
        if var_name not in self.var_to_id:
            var_id = self.next_var_id
            self.var_to_id[var_name] = var_id
            self.id_to_var[var_id] = var_name
            self.var_order.append(var_name)
            self.next_var_id += 1
        return self.var_to_id[var_name]
    
    def make_node(self, var_id: int, low: 'BDDNode', high: 'BDDNode') -> 'BDDNode':
        """Create or retrieve unique BDD node."""
        # Check if low == high (redundant node)
        if low == high:
            return low
            
        # Check unique table
        key = (var_id, low, high)
        if key in self.nodes:
            return self.nodes[key]
        
        # Create new node
        node = BDDNode(var_id, low, high)
        self.nodes[key] = node
        return node
    
    def create_variable(self, var_name: str) -> 'BDDNode':
        """Create BDD for a single variable."""
        var_id = self.get_var_id(var_name)
        return self.make_node(var_id, self.terminal_false, self.terminal_true)
    
    def create_constant(self, value: bool) -> 'BDDNode':
        """Create BDD for a constant (True or False)."""
        return self.terminal_true if value else self.terminal_false
    
    def apply_operation(self, op: str, left: 'BDDNode', right: 'BDDNode') -> 'BDDNode':
        """Apply binary operation to two BDDs."""
        # Create operation table
        op_table = {
            'AND': lambda a, b: a and b,
            'OR': lambda a, b: a or b,
            'XOR': lambda a, b: a != b,
            'NAND': lambda a, b: not (a and b),
            'NOR': lambda a, b: not (a or b),
            'XNOR': lambda a, b: a == b
        }
        
        if op not in op_table:
            raise ValueError(f"Unsupported operation: {op}")
        
        # Apply operation recursively
        return self._apply_recursive(op_table[op], left, right, {})
    
    def _apply_recursive(self, op_func, left: 'BDDNode', right: 'BDDNode', computed: Dict) -> 'BDDNode':
        """Recursively apply operation to BDDs."""
        # Check if already computed
        key = (id(left), id(right))
        if key in computed:
            return computed[key]
        
        # Handle terminal cases
        if left.is_terminal() and right.is_terminal():
            result = self.create_constant(op_func(left.value, right.value))
            computed[key] = result
            return result
        
        if left.is_terminal():
            # Left is terminal, right is variable
            if left.value:
                # True op right = right (for AND), True (for OR)
                if op_func(True, False) and op_func(True, True):
                    result = self.create_constant(True)
                elif not op_func(True, False) and op_func(True, True):
                    result = right
                else:
                    # Need to create proper BDD
                    var_id = right.var_id
                    low = self._apply_recursive(op_func, left, right.low, computed)
                    high = self._apply_recursive(op_func, left, right.high, computed)
                    result = self.make_node(var_id, low, high)
            else:
                # False op right
                if op_func(False, False) and op_func(False, True):
                    result = self.create_constant(True)
                elif not op_func(False, False) and not op_func(False, True):
                    result = self.create_constant(False)
                else:
                    # Need to create proper BDD
                    var_id = right.var_id
                    low = self._apply_recursive(op_func, left, right.low, computed)
                    high = self._apply_recursive(op_func, left, right.high, computed)
                    result = self.make_node(var_id, low, high)
        elif right.is_terminal():
            # Right is terminal, left is variable
            result = self._apply_recursive(op_func, right, left, computed)
        else:
            # Both are variables
            var_id = min(left.var_id, right.var_id)
            
            # Get children based on variable ordering
            if left.var_id == var_id:
                left_low, left_high = left.low, left.high
            else:
                left_low, left_high = left, left
                
            if right.var_id == var_id:
                right_low, right_high = right.low, right.high
            else:
                right_low, right_high = right, right
            
            # Recursively compute children
            low = self._apply_recursive(op_func, left_low, right_low, computed)
            high = self._apply_recursive(op_func, left_high, right_high, computed)
            
            result = self.make_node(var_id, low, high)
        
        computed[key] = result
        return result
    
    def complement(self, node: 'BDDNode') -> 'BDDNode':
        """Create complement of BDD."""
        if node.is_terminal():
            return self.terminal_false if node.value else self.terminal_true
        else:
            low = self.complement(node.low)
            high = self.complement(node.high)
            return self.make_node(node.var_id, low, high)
    
    def restrict(self, node: 'BDDNode', var_id: int, value: bool) -> 'BDDNode':
        """Restrict BDD by setting variable to constant value."""
        if node.is_terminal():
            return node
        
        if node.var_id == var_id:
            return node.high if value else node.low
        elif node.var_id > var_id:
            return node
        else:
            low = self.restrict(node.low, var_id, value)
            high = self.restrict(node.high, var_id, value)
            return self.make_node(node.var_id, low, high)
    
    def evaluate(self, node: 'BDDNode', assignment: Dict[str, bool]) -> bool:
        """Evaluate BDD with given variable assignment."""
        current = node
        while not current.is_terminal():
            var_name = self.id_to_var[current.var_id]
            if var_name in assignment:
                current = current.high if assignment[var_name] else current.low
            else:
                raise ValueError(f"Missing assignment for variable {var_name}")
        return current.value
    
    def get_support(self, node: 'BDDNode') -> Set[str]:
        """Get set of variables that node depends on."""
        if node.is_terminal():
            return set()
        
        support = {self.id_to_var[node.var_id]}
        support.update(self.get_support(node.low))
        support.update(self.get_support(node.high))
        return support
    
    def count_nodes(self, node: 'BDDNode') -> int:
        """Count number of nodes in BDD."""
        if node.is_terminal():
            return 1
        
        visited = set()
        return self._count_nodes_recursive(node, visited)
    
    def _count_nodes_recursive(self, node: 'BDDNode', visited: Set[int]) -> int:
        """Recursively count nodes."""
        if id(node) in visited or node.is_terminal():
            return 1 if node.is_terminal() else 0
        
        visited.add(id(node))
        count = 1
        count += self._count_nodes_recursive(node.low, visited)
        count += self._count_nodes_recursive(node.high, visited)
        return count
    
    def to_verilog(self, node: 'BDDNode', output_name: str = "out") -> str:
        """Convert BDD to Verilog code."""
        if node.is_terminal():
            return f"assign {output_name} = {'1\'b1' if node.value else '1\'b0'};"
        
        # Generate Verilog using case statement
        support = list(self.get_support(node))
        if not support:
            return self.to_verilog(node, output_name)
        
        # Simple implementation for demonstration
        verilog_code = f"assign {output_name} = "
        
        # This is a simplified conversion - in practice, you'd use more sophisticated methods
        if len(support) == 1:
            var = support[0]
            if node.var_id == self.var_to_id[var]:
                if node.low.is_terminal() and not node.low.value and node.high.is_terminal() and node.high.value:
                    verilog_code += f"{var};"
                else:
                    verilog_code += f"({var} ? {self._terminal_to_verilog(node.high)} : {self._terminal_to_verilog(node.low)});"
            else:
                verilog_code += self._terminal_to_verilog(node) + ";"
        else:
            verilog_code += "complex_expression; // BDD too complex for simple conversion"
        
        return verilog_code
    
    def _terminal_to_verilog(self, node: 'BDDNode') -> str:
        """Convert terminal node to Verilog constant."""
        if node.is_terminal():
            return "1'b1" if node.value else "1'b0"
        else:
            return "complex_expression"

# Example usage and testing
if __name__ == "__main__":
    # Create BDD manager
    bdd = BDD()
    
    # Create variables
    a = bdd.create_variable("a")
    b = bdd.create_variable("b")
    
    # Create simple functions
    f1 = bdd.apply_operation("AND", a, b)  # a AND b
    f2 = bdd.apply_operation("OR", a, b)   # a OR b
    f3 = bdd.apply_operation("XOR", a, b)  # a XOR b
    
    print("BDD Examples:")
    print(f"a AND b: {f1}")
    print(f"a OR b: {f2}")
    print(f"a XOR b: {f3}")
    
    # Evaluate with assignments
    assignment = {"a": True, "b": False}
    print(f"\nEvaluation with a=True, b=False:")
    print(f"a AND b = {bdd.evaluate(f1, assignment)}")
    print(f"a OR b = {bdd.evaluate(f2, assignment)}")
    print(f"a XOR b = {bdd.evaluate(f3, assignment)}")
    
    # Get support
    print(f"\nSupport of a AND b: {bdd.get_support(f1)}")
    print(f"Support of a OR b: {bdd.get_support(f2)}")
    
    # Count nodes
    print(f"\nNode count for a AND b: {bdd.count_nodes(f1)}")
    print(f"Node count for a OR b: {bdd.count_nodes(f2)}")
    
    # Convert to Verilog
    print(f"\nVerilog for a AND b:")
    print(bdd.to_verilog(f1, "out1"))
    print(f"\nVerilog for a OR b:")
    print(bdd.to_verilog(f2, "out2"))
