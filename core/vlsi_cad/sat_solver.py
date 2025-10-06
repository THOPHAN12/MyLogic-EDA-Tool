#!/usr/bin/env python3
"""
SAT Solver Implementation

Dựa trên các khái niệm VLSI CAD Part 1 cho kiểm tra Boolean satisfiability.
"""

from typing import List, Set, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class CNFClause:
    """CNF Clause representation."""
    
    def __init__(self, literals: List[int]):
        """
        Initialize CNF clause.
        
        Args:
            literals: List of literals (positive integers for variables, 
                     negative for negated variables)
        """
        self.literals = list(set(literals))  # Remove duplicates
        self.satisfied = False
        
    def is_satisfied_by(self, assignment: Dict[int, bool]) -> bool:
        """Check if clause is satisfied by assignment."""
        for literal in self.literals:
            var = abs(literal)
            value = literal > 0
            
            if var in assignment and assignment[var] == value:
                return True
        return False
    
    def is_unit_clause(self, assignment: Dict[int, bool]) -> Tuple[bool, int, bool]:
        """
        Check if clause is unit clause and return the unassigned literal.
        
        Returns:
            (is_unit, variable, value)
        """
        unassigned_literals = []
        
        for literal in self.literals:
            var = abs(literal)
            value = literal > 0
            
            if var not in assignment:
                unassigned_literals.append((var, value))
            elif assignment[var] == value:
                # Clause is already satisfied
                return False, 0, False
        
        if len(unassigned_literals) == 1:
            var, value = unassigned_literals[0]
            return True, var, value
        
        return False, 0, False
    
    def __repr__(self):
        return f"({' ∨ '.join(map(str, self.literals))})"

class SATSolver:
    """
    SAT Solver using DPLL algorithm with improvements.
    
    Based on VLSI CAD Part 1 concepts for Boolean satisfiability.
    """
    
    def __init__(self):
        self.clauses: List[CNFClause] = []
        self.variables: Set[int] = set()
        self.assignment: Dict[int, bool] = {}
        self.decision_stack: List[Tuple[int, bool]] = []
        self.conflict_count = 0
        self.backtrack_count = 0
        
    def add_clause(self, literals: List[int]) -> None:
        """Add clause to CNF formula."""
        clause = CNFClause(literals)
        self.clauses.append(clause)
        
        # Update variables set
        for literal in literals:
            self.variables.add(abs(literal))
    
    def add_clauses_from_formula(self, formula: List[List[int]]) -> None:
        """Add multiple clauses from formula."""
        for clause_literals in formula:
            self.add_clause(clause_literals)
    
    def solve(self) -> Tuple[bool, Optional[Dict[int, bool]]]:
        """
        Solve the SAT problem using DPLL algorithm.
        
        Returns:
            (is_satisfiable, satisfying_assignment)
        """
        logger.info(f"Solving SAT problem with {len(self.clauses)} clauses and {len(self.variables)} variables")
        
        # Reset state
        self.assignment = {}
        self.decision_stack = []
        self.conflict_count = 0
        self.backtrack_count = 0
        
        # Check for empty clause (unsatisfiable)
        if any(len(clause.literals) == 0 for clause in self.clauses):
            return False, None
        
        # Check for empty formula (satisfiable)
        if len(self.clauses) == 0:
            return True, {}
        
        # Main DPLL loop
        while True:
            # Unit propagation
            if not self._unit_propagation():
                return False, None
            
            # Check if all clauses are satisfied
            if self._all_clauses_satisfied():
                return True, self.assignment.copy()
            
            # Choose next variable to assign
            next_var = self._choose_variable()
            if next_var is None:
                # All variables assigned but some clauses not satisfied
                return False, None
            
            # Try assigning True first
            self._make_decision(next_var, True)
    
    def _unit_propagation(self) -> bool:
        """Perform unit propagation."""
        while True:
            unit_found = False
            
            for clause in self.clauses:
                if clause.is_satisfied_by(self.assignment):
                    continue
                
                is_unit, var, value = clause.is_unit_clause(self.assignment)
                if is_unit:
                    # Found unit clause, assign the literal
                    self.assignment[var] = value
                    self.decision_stack.append((var, value))
                    unit_found = True
                    logger.debug(f"Unit propagation: {var} = {value}")
                    break
            
            if not unit_found:
                break
        
        return True
    
    def _all_clauses_satisfied(self) -> bool:
        """Check if all clauses are satisfied."""
        for clause in self.clauses:
            if not clause.is_satisfied_by(self.assignment):
                return False
        return True
    
    def _choose_variable(self) -> Optional[int]:
        """Choose next unassigned variable."""
        for var in self.variables:
            if var not in self.assignment:
                return var
        return None
    
    def _make_decision(self, var: int, value: bool) -> bool:
        """Make a decision assignment."""
        self.assignment[var] = value
        self.decision_stack.append((var, value))
        logger.debug(f"Decision: {var} = {value}")
        
        # Recursive call to continue solving
        if self._solve_recursive():
            return True
        
        # Backtrack
        self.assignment.pop(var)
        self.decision_stack.pop()
        self.backtrack_count += 1
        
        # Try opposite value
        self.assignment[var] = not value
        self.decision_stack.append((var, not value))
        logger.debug(f"Backtrack decision: {var} = {not value}")
        
        return self._solve_recursive()
    
    def _solve_recursive(self) -> bool:
        """Recursive part of DPLL algorithm."""
        # Unit propagation
        if not self._unit_propagation():
            self.conflict_count += 1
            return False
        
        # Check if all clauses satisfied
        if self._all_clauses_satisfied():
            return True
        
        # Choose next variable
        next_var = self._choose_variable()
        if next_var is None:
            return False
        
        # Try True first
        if self._make_decision(next_var, True):
            return True
        
        return False
    
    def get_statistics(self) -> Dict[str, int]:
        """Get solver statistics."""
        return {
            'variables': len(self.variables),
            'clauses': len(self.clauses),
            'decisions': len(self.decision_stack),
            'conflicts': self.conflict_count,
            'backtracks': self.backtrack_count
        }

class SATBasedVerifier:
    """
    SAT-based verification for logic circuits.
    
    Converts circuit verification problems to SAT instances.
    """
    
    def __init__(self):
        self.solver = SATSolver()
        
    def verify_equivalence(self, circuit1: Dict, circuit2: Dict) -> Tuple[bool, Optional[Dict]]:
        """
        Verify if two circuits are equivalent using SAT.
        
        Args:
            circuit1, circuit2: Circuit representations
            
        Returns:
            (are_equivalent, counterexample_if_not_equivalent)
        """
        # Create miter circuit (XOR of outputs)
        # If circuits are equivalent, miter should never be true
        
        # This is a simplified implementation
        # In practice, you'd need to convert circuit to CNF
        
        logger.info("Verifying circuit equivalence using SAT")
        
        # For demonstration, create a simple miter
        # In real implementation, you'd convert circuits to CNF
        miter_clauses = self._create_miter_cnf(circuit1, circuit2)
        
        self.solver = SATSolver()
        self.solver.add_clauses_from_formula(miter_clauses)
        
        is_sat, assignment = self.solver.solve()
        
        if is_sat:
            # Found counterexample - circuits are not equivalent
            return False, assignment
        else:
            # No counterexample found - circuits are equivalent
            return True, None
    
    def _create_miter_cnf(self, circuit1: Dict, circuit2: Dict) -> List[List[int]]:
        """
        Create CNF for miter circuit.
        
        This is a simplified implementation.
        """
        # For demonstration, create simple CNF
        # In practice, you'd use Tseitin transformation
        
        clauses = []
        
        # Example: XOR of two outputs
        # out1 XOR out2 = (out1 OR out2) AND (NOT out1 OR NOT out2)
        
        # Assuming outputs are variables 1 and 2
        clauses.append([1, 2])      # out1 OR out2
        clauses.append([-1, -2])    # NOT out1 OR NOT out2
        
        return clauses
    
    def verify_property(self, circuit: Dict, property_expr: str) -> Tuple[bool, Optional[Dict]]:
        """
        Verify a property of a circuit using SAT.
        
        Args:
            circuit: Circuit representation
            property_expr: Property expression
            
        Returns:
            (property_holds, counterexample_if_not)
        """
        logger.info(f"Verifying property: {property_expr}")
        
        # Convert circuit and property to CNF
        clauses = self._circuit_and_property_to_cnf(circuit, property_expr)
        
        self.solver = SATSolver()
        self.solver.add_clauses_from_formula(clauses)
        
        is_sat, assignment = self.solver.solve()
        
        if is_sat:
            # Property violated
            return False, assignment
        else:
            # Property holds
            return True, None
    
    def _circuit_and_property_to_cnf(self, circuit: Dict, property_expr: str) -> List[List[int]]:
        """Convert circuit and property to CNF."""
        # Simplified implementation
        # In practice, you'd use proper Tseitin transformation
        
        clauses = []
        
        # Example property: output should never be true when input is false
        # NOT (input = false AND output = true)
        # = NOT input OR NOT output
        clauses.append([-1, -2])  # NOT input OR NOT output
        
        return clauses

# Example usage and testing
if __name__ == "__main__":
    # Create SAT solver
    solver = SATSolver()
    
    # Example 1: Simple 2-SAT problem
    # (a OR b) AND (NOT a OR c) AND (NOT b OR NOT c)
    solver.add_clause([1, 2])      # a OR b
    solver.add_clause([-1, 3])     # NOT a OR c
    solver.add_clause([-2, -3])    # NOT b OR NOT c
    
    print("SAT Solver Example:")
    print("Formula: (a OR b) AND (NOT a OR c) AND (NOT b OR NOT c)")
    
    is_sat, assignment = solver.solve()
    
    if is_sat:
        print(f"Satisfiable! Assignment: {assignment}")
    else:
        print("Unsatisfiable!")
    
    print(f"Solver statistics: {solver.get_statistics()}")
    
    # Example 2: Unsatisfiable formula
    print("\n" + "="*50)
    solver2 = SATSolver()
    solver2.add_clause([1])        # a
    solver2.add_clause([-1])       # NOT a
    
    print("Formula: a AND NOT a")
    is_sat2, assignment2 = solver2.solve()
    
    if is_sat2:
        print(f"Satisfiable! Assignment: {assignment2}")
    else:
        print("Unsatisfiable!")
    
    print(f"Solver statistics: {solver2.get_statistics()}")
