#!/usr/bin/env python3
"""
Boolean Expression Diagrams (BED) Implementation

BED là một cấu trúc dữ liệu để biểu diễn các biểu thức Boolean, tương tự BDD
nhưng linh hoạt hơn trong việc biểu diễn các biểu thức phức tạp.

Dựa trên các khái niệm VLSI CAD và tham khảo từ các công trình nghiên cứu về BED.

Các thuật toán chính:
- MK(): Make node - Tạo node mới
- UP_ONE(): Upward traversal một bước
- UP_ALL(): Upward traversal toàn bộ
"""

from typing import Dict, List, Set, Any, Optional, Tuple, Union
import logging

logger = logging.getLogger(__name__)

class BEDNode:
    """
    BED Node representation.
    
    Mỗi node có thể là:
    - Terminal node (True/False)
    - Variable node (biến Boolean)
    - Operator node (AND, OR, NOT, XOR, etc.)
    """
    
    def __init__(self, node_type: str, 
                 var_name: Optional[str] = None,
                 operator: Optional[str] = None,
                 left: Optional['BEDNode'] = None,
                 right: Optional['BEDNode'] = None,
                 value: Optional[bool] = None):
        """
        Initialize BED node.
        
        Args:
            node_type: 'terminal', 'variable', hoặc 'operator'
            var_name: Tên biến (cho variable node)
            operator: Toán tử (AND, OR, NOT, XOR, etc.)
            left: Node con trái (cho operator node)
            right: Node con phải (cho operator node, None cho NOT)
            value: Giá trị Boolean (cho terminal node)
        """
        self.node_type = node_type
        self.var_name = var_name
        self.operator = operator
        self.left = left
        self.right = right
        self.value = value
        self.node_id = None  # Sẽ được gán bởi BED manager
        
    def is_terminal(self) -> bool:
        """Check if this is a terminal node."""
        return self.node_type == 'terminal'
    
    def is_variable(self) -> bool:
        """Check if this is a variable node."""
        return self.node_type == 'variable'
    
    def is_operator(self) -> bool:
        """Check if this is an operator node."""
        return self.node_type == 'operator'
    
    def __repr__(self):
        if self.is_terminal():
            return f"T({self.value})"
        elif self.is_variable():
            return f"V({self.var_name})"
        else:
            if self.operator == 'NOT':
                return f"NOT({self.left})"
            else:
                return f"{self.operator}({self.left}, {self.right})"
    
    def __eq__(self, other):
        """Equality check for BED nodes."""
        if not isinstance(other, BEDNode):
            return False
        
        if self.node_type != other.node_type:
            return False
        
        if self.is_terminal():
            return self.value == other.value
        elif self.is_variable():
            return self.var_name == other.var_name
        else:
            return (self.operator == other.operator and
                    self.left == other.left and
                    self.right == other.right)
    
    def __hash__(self):
        """Hash for BED nodes (for use in sets/dicts)."""
        if self.is_terminal():
            return hash(('terminal', self.value))
        elif self.is_variable():
            return hash(('variable', self.var_name))
        else:
            return hash(('operator', self.operator, id(self.left), id(self.right)))


class BED:
    """
    Boolean Expression Diagrams (BED) Manager.
    
    BED là một cấu trúc dữ liệu để biểu diễn và thao tác các biểu thức Boolean.
    Khác với BDD, BED không yêu cầu canonical form và linh hoạt hơn.
    """
    
    def __init__(self):
        """Initialize BED manager."""
        # Unique table để tránh duplicate nodes
        self.unique_table: Dict[Tuple, BEDNode] = {}
        
        # Node counter
        self.next_node_id = 1
        
        # Variable mapping
        self.var_to_id: Dict[str, int] = {}
        self.id_to_var: Dict[int, str] = {}
        
        # Terminal nodes (singleton)
        self.terminal_true = BEDNode('terminal', value=True)
        self.terminal_false = BEDNode('terminal', value=False)
        self.terminal_true.node_id = 0
        self.terminal_false.node_id = 1
        
        # Computed table for operation caching
        self.computed_table: Dict[Tuple, BEDNode] = {}
        
    def MK(self, node_type: str, 
           var_name: Optional[str] = None,
           operator: Optional[str] = None,
           left: Optional[BEDNode] = None,
           right: Optional[BEDNode] = None,
           value: Optional[bool] = None) -> BEDNode:
        """
        Make node - Tạo node mới hoặc trả về node đã tồn tại.
        
        Đây là thuật toán MK() chính trong BED.
        """
        # Terminal nodes - return singleton
        if node_type == 'terminal':
            return self.terminal_true if value else self.terminal_false
        
        # Variable nodes - check unique table
        if node_type == 'variable':
            key = ('variable', var_name)
            if key in self.unique_table:
                return self.unique_table[key]
            
            node = BEDNode('variable', var_name=var_name)
            node.node_id = self.next_node_id
            self.next_node_id += 1
            
            # Store in unique table
            self.unique_table[key] = node
            
            # Update variable mapping
            if var_name not in self.var_to_id:
                var_id = len(self.var_to_id) + 1
                self.var_to_id[var_name] = var_id
                self.id_to_var[var_id] = var_name
            
            return node
        
        # Operator nodes - check unique table
        if node_type == 'operator':
            # Normalize operator order (AND, OR are commutative)
            if operator in ['AND', 'OR'] and left and right:
                # Sort children for canonical form
                left_id = id(left)
                right_id = id(right)
                if left_id > right_id:
                    left, right = right, left
            
            key = ('operator', operator, id(left), id(right) if right else None)
            if key in self.unique_table:
                return self.unique_table[key]
            
            node = BEDNode('operator', operator=operator, left=left, right=right)
            node.node_id = self.next_node_id
            self.next_node_id += 1
            
            # Store in unique table
            self.unique_table[key] = node
            
            return node
        
        raise ValueError(f"Unknown node type: {node_type}")
    
    def create_variable(self, var_name: str) -> BEDNode:
        """Create a variable node."""
        return self.MK('variable', var_name=var_name)
    
    def create_constant(self, value: bool) -> BEDNode:
        """Create a terminal node."""
        return self.MK('terminal', value=value)
    
    def create_and(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Create AND operator node."""
        return self.MK('operator', operator='AND', left=left, right=right)
    
    def create_or(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Create OR operator node."""
        return self.MK('operator', operator='OR', left=left, right=right)
    
    def create_not(self, child: BEDNode) -> BEDNode:
        """Create NOT operator node."""
        return self.MK('operator', operator='NOT', left=child, right=None)
    
    def create_xor(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Create XOR operator node."""
        return self.MK('operator', operator='XOR', left=left, right=right)
    
    def UP_ONE(self, node: BEDNode, var_name: str, value: bool) -> BEDNode:
        """
        Upward traversal một bước.
        
        Thay thế một biến bằng giá trị cụ thể và đơn giản hóa biểu thức.
        
        Args:
            node: BED node hiện tại
            var_name: Tên biến cần thay thế
            value: Giá trị để thay thế
            
        Returns:
            BED node sau khi thay thế và đơn giản hóa
        """
        # Check computed table
        key = ('UP_ONE', id(node), var_name, value)
        if key in self.computed_table:
            return self.computed_table[key]
        
        result = None
        
        # Terminal node - return as is
        if node.is_terminal():
            result = node
        
        # Variable node - replace with constant
        elif node.is_variable():
            if node.var_name == var_name:
                result = self.create_constant(value)
            else:
                result = node
        
        # Operator node - recursive traversal
        elif node.is_operator():
            if node.operator == 'NOT':
                child = self.UP_ONE(node.left, var_name, value)
                result = self.create_not(child)
            else:
                left_child = self.UP_ONE(node.left, var_name, value)
                right_child = self.UP_ONE(node.right, var_name, value)
                
                # Simplify based on operator
                if node.operator == 'AND':
                    result = self._simplify_and(left_child, right_child)
                elif node.operator == 'OR':
                    result = self._simplify_or(left_child, right_child)
                elif node.operator == 'XOR':
                    result = self._simplify_xor(left_child, right_child)
                else:
                    result = self.MK('operator', operator=node.operator, 
                                    left=left_child, right=right_child)
        
        # Cache result
        self.computed_table[key] = result
        return result
    
    def UP_ALL(self, node: BEDNode, assignment: Dict[str, bool]) -> BEDNode:
        """
        Upward traversal toàn bộ.
        
        Thay thế tất cả các biến trong assignment và đơn giản hóa hoàn toàn.
        
        Args:
            node: BED node gốc
            assignment: Dictionary mapping variable names to Boolean values
            
        Returns:
            BED node sau khi thay thế tất cả biến và đơn giản hóa
        """
        current = node
        
        # Apply UP_ONE cho từng biến trong assignment
        for var_name, value in assignment.items():
            current = self.UP_ONE(current, var_name, value)
        
        return current
    
    def _simplify_and(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Simplify AND operation."""
        # True AND x = x
        if left == self.terminal_true:
            return right
        if right == self.terminal_true:
            return left
        
        # False AND x = False
        if left == self.terminal_false or right == self.terminal_false:
            return self.terminal_false
        
        # x AND x = x
        if left == right:
            return left
        
        # Create AND node
        return self.create_and(left, right)
    
    def _simplify_or(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Simplify OR operation."""
        # False OR x = x
        if left == self.terminal_false:
            return right
        if right == self.terminal_false:
            return left
        
        # True OR x = True
        if left == self.terminal_true or right == self.terminal_true:
            return self.terminal_true
        
        # x OR x = x
        if left == right:
            return left
        
        # Create OR node
        return self.create_or(left, right)
    
    def _simplify_xor(self, left: BEDNode, right: BEDNode) -> BEDNode:
        """Simplify XOR operation."""
        # x XOR x = False
        if left == right:
            return self.terminal_false
        
        # False XOR x = x
        if left == self.terminal_false:
            return right
        if right == self.terminal_false:
            return left
        
        # True XOR x = NOT x
        if left == self.terminal_true:
            return self.create_not(right)
        if right == self.terminal_true:
            return self.create_not(left)
        
        # Create XOR node
        return self.create_xor(left, right)
    
    def evaluate(self, node: BEDNode, assignment: Dict[str, bool]) -> bool:
        """
        Evaluate BED với assignment cho các biến.
        
        Args:
            node: BED node để evaluate
            assignment: Dictionary mapping variable names to Boolean values
            
        Returns:
            Boolean value của biểu thức
        """
        # Use UP_ALL to simplify and get result
        simplified = self.UP_ALL(node, assignment)
        
        if simplified.is_terminal():
            return simplified.value
        else:
            # If still not terminal, some variables are missing
            raise ValueError(f"Cannot evaluate: missing variables in assignment")
    
    def get_variables(self, node: BEDNode) -> Set[str]:
        """
        Lấy tập hợp tất cả các biến trong BED.
        
        Args:
            node: BED node
            
        Returns:
            Set of variable names
        """
        visited = set()
        variables = set()
        self._collect_variables(node, visited, variables)
        return variables
    
    def _collect_variables(self, node: BEDNode, visited: Set[int], variables: Set[str]):
        """Recursively collect variables."""
        node_id = id(node)
        if node_id in visited:
            return
        
        visited.add(node_id)
        
        if node.is_variable():
            variables.add(node.var_name)
        elif node.is_operator():
            if node.left:
                self._collect_variables(node.left, visited, variables)
            if node.right:
                self._collect_variables(node.right, visited, variables)
    
    def count_nodes(self, node: BEDNode) -> int:
        """Count number of nodes in BED."""
        visited = set()
        return self._count_nodes_recursive(node, visited)
    
    def _count_nodes_recursive(self, node: BEDNode, visited: Set[int]) -> int:
        """Recursively count nodes."""
        node_id = id(node)
        if node_id in visited:
            return 0
        
        visited.add(node_id)
        count = 1
        
        if node.is_operator():
            if node.left:
                count += self._count_nodes_recursive(node.left, visited)
            if node.right:
                count += self._count_nodes_recursive(node.right, visited)
        
        return count
    
    def to_string(self, node: BEDNode) -> str:
        """Convert BED to string representation."""
        if node.is_terminal():
            return "1" if node.value else "0"
        elif node.is_variable():
            return node.var_name
        else:
            if node.operator == 'NOT':
                return f"!({self.to_string(node.left)})"
            else:
                left_str = self.to_string(node.left)
                right_str = self.to_string(node.right)
                op_symbol = {'AND': '&', 'OR': '|', 'XOR': '^'}.get(node.operator, node.operator)
                return f"({left_str} {op_symbol} {right_str})"
    
    def compare_with_bdd(self, bed_node: BEDNode, bdd_manager, bdd_node) -> Dict[str, Any]:
        """
        So sánh BED với BDD tương ứng.
        
        Args:
            bed_node: BED node
            bdd_manager: BDD manager instance
            bdd_node: BDD node tương ứng
            
        Returns:
            Dictionary với các metrics so sánh
        """
        bed_vars = self.get_variables(bed_node)
        bdd_vars = bdd_manager.get_support(bdd_node)
        
        bed_nodes = self.count_nodes(bed_node)
        bdd_nodes = bdd_manager.count_nodes(bdd_node)
        
        return {
            'bed_nodes': bed_nodes,
            'bdd_nodes': bdd_nodes,
            'bed_variables': len(bed_vars),
            'bdd_variables': len(bdd_vars),
            'node_ratio': bed_nodes / bdd_nodes if bdd_nodes > 0 else float('inf'),
            'variables_match': bed_vars == bdd_vars
        }


# Example usage and testing
if __name__ == "__main__":
    # Create BED manager
    bed = BED()
    
    # Create variables
    a = bed.create_variable("a")
    b = bed.create_variable("b")
    c = bed.create_variable("c")
    
    # Create expressions
    # f1 = a AND b
    f1 = bed.create_and(a, b)
    print(f"f1 = a AND b: {f1}")
    print(f"  String: {bed.to_string(f1)}")
    print(f"  Variables: {bed.get_variables(f1)}")
    print(f"  Nodes: {bed.count_nodes(f1)}")
    
    # f2 = a OR b
    f2 = bed.create_or(a, b)
    print(f"\nf2 = a OR b: {f2}")
    print(f"  String: {bed.to_string(f2)}")
    
    # f3 = (a AND b) OR (NOT c)
    f3 = bed.create_or(f1, bed.create_not(c))
    print(f"\nf3 = (a AND b) OR (NOT c): {f3}")
    print(f"  String: {bed.to_string(f3)}")
    print(f"  Variables: {bed.get_variables(f3)}")
    print(f"  Nodes: {bed.count_nodes(f3)}")
    
    # Test UP_ONE
    print(f"\n=== Testing UP_ONE ===")
    f3_up = bed.UP_ONE(f3, "a", True)
    print(f"UP_ONE(f3, a=True): {bed.to_string(f3_up)}")
    
    f3_up2 = bed.UP_ONE(f3_up, "b", False)
    print(f"UP_ONE(previous, b=False): {bed.to_string(f3_up2)}")
    
    # Test UP_ALL
    print(f"\n=== Testing UP_ALL ===")
    assignment = {"a": True, "b": True, "c": False}
    f3_simplified = bed.UP_ALL(f3, assignment)
    print(f"UP_ALL(f3, {assignment}): {bed.to_string(f3_simplified)}")
    print(f"  Result: {f3_simplified.value}")
    
    # Test evaluation
    print(f"\n=== Testing Evaluation ===")
    result = bed.evaluate(f3, assignment)
    print(f"evaluate(f3, {assignment}) = {result}")

