#!/usr/bin/env python3
"""
Advanced BDD Operations - Inspired by ABC (YosysHQ/abc)

Tham khảo từ ABC BDD implementation để cải thiện MyLogic BDD.
Các operations nâng cao từ src/bdd/bdd.c trong ABC.

ABC Reference: https://github.com/YosysHQ/abc/tree/8827bafb7f288de6749dc6e30fa452f2040949c0
"""

from typing import Dict, List, Set, Any, Optional, Tuple
import logging
from .bdd import BDD, BDDNode

logger = logging.getLogger(__name__)

class AdvancedBDD(BDD):
    """
    Advanced BDD với các operations từ ABC.
    
    Mở rộng BDD cơ bản với:
    - Existential quantification (∃)
    - Universal quantification (∀)
    - Function composition
    - Variable reordering
    - Advanced optimization
    """
    
    def __init__(self):
        super().__init__()
        # ABC-inspired computed table
        self.computed_table: Dict[Tuple[str, int, int], int] = {}
        self.unique_table: Dict[Tuple[int, int, int], int] = {}
        self.operation_cache: Dict[Tuple[str, int, int], int] = {}
        
    def exist_quantification(self, f: BDDNode, var: str) -> BDDNode:
        """
        Existential quantification ∃x.f(x) - inspired by ABC BDD.
        
        ABC Reference: Bdd_Exist() in src/bdd/bdd.c
        ∃x.f(x) = f(0) ∨ f(1)
        
        Args:
            f: BDD function
            var: Variable to quantify
            
        Returns:
            BDD representing ∃x.f(x)
        """
        if var not in self.var_to_id:
            raise ValueError(f"Variable {var} not found")
        
        var_id = self.var_to_id[var]
        
        # Check computed table first (ABC optimization)
        cache_key = ("EXIST", hash(f), var_id)
        if cache_key in self.computed_table:
            return self.nodes[self.computed_table[cache_key]]
        
        # Implementation: ∃x.f(x) = f(0) ∨ f(1)
        f_0 = self.restrict(f, var, False)
        f_1 = self.restrict(f, var, True)
        result = self.apply_operation("OR", f_0, f_1)
        
        # Cache result (ABC optimization)
        self.computed_table[cache_key] = hash(result)
        
        logger.debug(f"Existential quantification ∃{var}.f = {result}")
        return result
    
    def forall_quantification(self, f: BDDNode, var: str) -> BDDNode:
        """
        Universal quantification ∀x.f(x) - inspired by ABC BDD.
        
        ABC Reference: Bdd_Forall() in src/bdd/bdd.c
        ∀x.f(x) = f(0) ∧ f(1)
        
        Args:
            f: BDD function
            var: Variable to quantify
            
        Returns:
            BDD representing ∀x.f(x)
        """
        if var not in self.var_to_id:
            raise ValueError(f"Variable {var} not found")
        
        var_id = self.var_to_id[var]
        
        # Check computed table first (ABC optimization)
        cache_key = ("FORALL", hash(f), var_id)
        if cache_key in self.computed_table:
            return self.nodes[self.computed_table[cache_key]]
        
        # Implementation: ∀x.f(x) = f(0) ∧ f(1)
        f_0 = self.restrict(f, var, False)
        f_1 = self.restrict(f, var, True)
        result = self.apply_operation("AND", f_0, f_1)
        
        # Cache result (ABC optimization)
        self.computed_table[cache_key] = hash(result)
        
        logger.debug(f"Universal quantification ∀{var}.f = {result}")
        return result
    
    def compose(self, f: BDDNode, g: BDDNode, var: str) -> BDDNode:
        """
        Function composition f(g) - inspired by ABC BDD.
        
        ABC Reference: Bdd_Compose() in src/bdd/bdd.c
        Replace variable var in f with function g
        
        Args:
            f: Function to compose
            g: Function to substitute
            var: Variable to replace
            
        Returns:
            BDD representing f(g)
        """
        if var not in self.var_to_id:
            raise ValueError(f"Variable {var} not found")
        
        var_id = self.var_to_id[var]
        
        # Check computed table first (ABC optimization)
        cache_key = ("COMPOSE", hash(f), hash(g))
        if cache_key in self.computed_table:
            return self.nodes[self.computed_table[cache_key]]
        
        # Implementation: f(g) = f with var replaced by g
        result = self._compose_recursive(f, g, var_id)
        
        # Cache result (ABC optimization)
        self.computed_table[cache_key] = hash(result)
        
        logger.debug(f"Function composition f(g) = {result}")
        return result
    
    def _compose_recursive(self, f: BDDNode, g: BDDNode, var_id: int) -> BDDNode:
        """
        Recursive implementation of function composition.
        
        ABC-inspired recursive decomposition.
        """
        if f.var_id == 0:  # Terminal node
            return f
        
        if f.var_id == var_id:
            # Replace variable with function g
            return g
        
        # Continue recursion
        low = self._compose_recursive(f.low, g, var_id)
        high = self._compose_recursive(f.high, g, var_id)
        return self.create_node(f.var_id, low, high)
    
    def variable_reordering(self, f: BDDNode, new_order: List[str]) -> BDDNode:
        """
        Variable reordering - inspired by ABC BDD.
        
        ABC Reference: Bdd_Reorder() in src/bdd/bddReorder.c
        Reorder variables to minimize BDD size
        
        Args:
            f: BDD function
            new_order: New variable order
            
        Returns:
            Reordered BDD
        """
        logger.info(f"Reordering variables: {self.var_order} -> {new_order}")
        
        # Update variable order
        old_order = self.var_order.copy()
        self.var_order = new_order
        
        # Rebuild variable mappings
        self.var_to_id = {var: i+1 for i, var in enumerate(new_order)}
        self.id_to_var = {i+1: var for i, var in enumerate(new_order)}
        
        # Rebuild BDD with new order
        result = self._reorder_recursive(f, old_order, new_order)
        
        logger.info(f"Variable reordering completed")
        return result
    
    def _reorder_recursive(self, f: BDDNode, old_order: List[str], new_order: List[str]) -> BDDNode:
        """Recursive variable reordering implementation."""
        if f.var_id == 0:  # Terminal node
            return f
        
        # Get variable name
        var_name = self.id_to_var[f.var_id]
        
        # Find new position
        new_pos = new_order.index(var_name) + 1
        
        # Recurse on children
        low = self._reorder_recursive(f.low, old_order, new_order)
        high = self._reorder_recursive(f.high, old_order, new_order)
        
        return self.create_node(new_pos, low, high)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Enhanced statistics with ABC-inspired metrics."""
        stats = super().get_statistics()
        stats.update({
            'computed_table_size': len(self.computed_table),
            'operation_cache_size': len(self.operation_cache),
            'unique_table_size': len(self.unique_table),
            'abc_optimizations': True
        })
        return stats

def test_advanced_bdd():
    """Test advanced BDD operations inspired by ABC."""
    print("Testing Advanced BDD Operations (ABC-inspired)...")
    
    # Create advanced BDD
    bdd = AdvancedBDD()
    
    # Create variables
    a = bdd.create_variable("a")
    b = bdd.create_variable("b")
    c = bdd.create_variable("c")
    
    # Create functions
    f1 = bdd.apply_operation("AND", a, b)  # a AND b
    f2 = bdd.apply_operation("OR", a, b)   # a OR b
    
    print(f"Created functions:")
    print(f"f1 = a AND b: {f1}")
    print(f"f2 = a OR b: {f2}")
    
    # Test existential quantification
    print(f"\nTesting Existential Quantification:")
    f_exist = bdd.exist_quantification(f1, "b")  # ∃b.(a AND b) = a
    print(f"∃b.(a AND b) = {f_exist}")
    
    # Test universal quantification
    print(f"\nTesting Universal Quantification:")
    f_forall = bdd.forall_quantification(f2, "b")  # ∀b.(a OR b) = a
    print(f"∀b.(a OR b) = {f_forall}")
    
    # Test function composition
    print(f"\nTesting Function Composition:")
    f_compose = bdd.compose(f1, c, "a")  # (a AND b) with a=c = c AND b
    print(f"(a AND b) with a=c = {f_compose}")
    
    # Test variable reordering
    print(f"\nTesting Variable Reordering:")
    f_reorder = bdd.variable_reordering(f1, ["b", "a"])  # Reorder b, a
    print(f"Reordered (a AND b) = {f_reorder}")
    
    # Get enhanced statistics
    stats = bdd.get_statistics()
    print(f"\nAdvanced BDD Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print("✅ Advanced BDD test completed!")

if __name__ == "__main__":
    test_advanced_bdd()
