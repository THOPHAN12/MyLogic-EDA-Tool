#!/usr/bin/env python3
"""
Quine-McCluskey Algorithm Implementation

Thuật toán Quine-McCluskey là một phương pháp Boolean minimization,
tương tự như   nhưng đảm bảo tìm được minimal form.

Dựa trên các khái niệm VLSI CAD Part I - Boolean minimization.

Reference:
- Quine-McCluskey algorithm for two-level logic minimization
- Tương tự Espresso nhưng exact (không phải heuristic)
"""

from typing import Dict, List, Set, Tuple, Optional, Any
import logging

logger = logging.getLogger(__name__)

class Minterm:
    """Represents a minterm in truth table."""
    
    def __init__(self, value: int, num_vars: int, covered: bool = False):
        """
        Initialize minterm.
        
        Args:
            value: Decimal value of minterm (0 to 2^num_vars - 1)
            num_vars: Number of variables
            covered: Whether this minterm is covered by a prime implicant
        """
        self.value = value
        self.num_vars = num_vars
        self.covered = covered
        self.binary = self._to_binary(value, num_vars)
        self.ones = self.binary.count('1')
        self.covered_minterms = {value}  # Track which minterms this represents
    
    def _to_binary(self, value: int, num_vars: int) -> str:
        """Convert to binary string."""
        return format(value, f'0{num_vars}b')
    
    def __repr__(self):
        return f"M({self.value}:{self.binary})"
    
    def __eq__(self, other):
        return isinstance(other, Minterm) and self.value == other.value
    
    def __hash__(self):
        return hash(self.value)


class Implicant:
    """Represents a prime implicant."""
    
    def __init__(self, minterms: Set[int], num_vars: int):
        """
        Initialize implicant.
        
        Args:
            minterms: Set of minterm values covered by this implicant
            num_vars: Number of variables
        """
        self.minterms = minterms
        self.num_vars = num_vars
        self.covered_minterms = set()
        self.essential = False
    
    def get_binary_representation(self) -> str:
        """Get binary representation with '-' for don't cares."""
        if not self.minterms:
            return ""
        
        # Get binary representations
        binaries = [format(m, f'0{self.num_vars}b') for m in self.minterms]
        
        # Find common pattern
        result = list(binaries[0])
        for i in range(1, len(binaries)):
            for j in range(len(result)):
                if result[j] != binaries[i][j]:
                    result[j] = '-'
        
        return ''.join(result)
    
    def covers(self, minterm: int) -> bool:
        """Check if this implicant covers a minterm."""
        return minterm in self.minterms
    
    def __repr__(self):
        binary = self.get_binary_representation()
        return f"PI({binary}, covers={self.minterms})"
    
    def __eq__(self, other):
        return isinstance(other, Implicant) and self.minterms == other.minterms
    
    def __hash__(self):
        return hash(tuple(sorted(self.minterms)))


class QuineMcCluskey:
    """
    Quine-McCluskey Algorithm for Boolean Minimization.
    
    Tìm minimal sum-of-products (SOP) form cho một hàm Boolean.
    """
    
    def __init__(self):
        """Initialize Quine-McCluskey solver."""
        self.variable_names = []
        self.minterms = []
        self.dont_cares = []
        self.prime_implicants = []
        self.essential_implicants = []
    
    def minimize(self, minterms: List[int], 
                 num_vars: int,
                 variable_names: Optional[List[str]] = None,
                 dont_cares: Optional[List[int]] = None) -> Dict[str, Any]:
        """
        Minimize Boolean function using Quine-McCluskey algorithm.
        
        Args:
            minterms: List of minterm values (e.g., [0, 1, 3, 5])
            num_vars: Number of variables
            variable_names: Optional list of variable names (e.g., ['a', 'b', 'c'])
            dont_cares: Optional list of don't care minterms
            
        Returns:
            Dictionary with minimized expression and statistics
        """
        self.num_vars = num_vars
        self.variable_names = variable_names or [f"x{i}" for i in range(num_vars)]
        self.minterms = minterms
        self.dont_cares = dont_cares or []
        
        # Step 1: Find all prime implicants
        self.prime_implicants = self._find_prime_implicants()
        
        # Step 2: Find essential prime implicants
        self.essential_implicants = self._find_essential_implicants()
        
        # Step 3: Cover remaining minterms
        minimal_cover = self._cover_minterms()
        
        # Step 4: Generate expression
        expression = self._generate_expression(minimal_cover)
        
        return {
            'expression': expression,
            'prime_implicants': len(self.prime_implicants),
            'essential_implicants': len(self.essential_implicants),
            'minimal_implicants': len(minimal_cover),
            'minterms': len(minterms),
            'num_vars': num_vars,
            'coverage': self._calculate_coverage(minimal_cover)
        }
    
    def _find_prime_implicants(self) -> List[Implicant]:
        """Find all prime implicants."""
        # Group minterms by number of 1s
        groups = {}
        all_minterms = set(self.minterms) | set(self.dont_cares)
        
        for m in all_minterms:
            minterm = Minterm(m, self.num_vars)
            ones = minterm.ones
            if ones not in groups:
                groups[ones] = []
            groups[ones].append(minterm)
        
        # Iteratively combine groups
        prime_implicants = []
        current_groups = groups
        used = set()
        
        while True:
            next_groups = {}
            new_implicants = []
            
            # Try to combine adjacent groups
            sorted_keys = sorted(current_groups.keys())
            for i in range(len(sorted_keys) - 1):
                key1 = sorted_keys[i]
                key2 = sorted_keys[i + 1]
                
                if key2 - key1 != 1:
                    continue
                
                group1 = current_groups[key1]
                group2 = current_groups[key2]
                
                # Try to combine each pair
                for m1 in group1:
                    for m2 in group2:
                        combined = self._combine_minterms(m1, m2)
                        if combined is not None:
                            # Mark as used
                            used.add(m1.value)
                            used.add(m2.value)
                            
                            # Create implicant
                            implicant_minterms = {m1.value, m2.value}
                            if combined not in next_groups:
                                next_groups[combined] = set()
                            next_groups[combined].update(implicant_minterms)
            
            # Add unused minterms as prime implicants
            for key, group in current_groups.items():
                for m in group:
                    if m.value not in used:
                        implicant = Implicant({m.value}, self.num_vars)
                        if implicant not in prime_implicants:
                            prime_implicants.append(implicant)
            
            if not next_groups:
                break
            
            # Merge implicants with same binary representation
            merged_groups = {}
            for binary, minterms in next_groups.items():
                if binary not in merged_groups:
                    merged_groups[binary] = set()
                merged_groups[binary].update(minterms)
            
            # Create implicants for next iteration
            current_groups = {}
            for binary, minterms in merged_groups.items():
                ones = binary.count('1')
                if ones not in current_groups:
                    current_groups[ones] = []
                # Create a dummy minterm for grouping
                dummy = Minterm(0, self.num_vars)
                dummy.binary = binary
                dummy.ones = ones
                # Store both dummy and minterms for later use
                current_groups[ones].append((dummy, minterms))
            
            # Convert back to simple minterm list for next iteration
            # But we need to track which minterms are combined
            # For now, create a simpler structure
            next_iteration_groups = {}
            for ones, items in current_groups.items():
                next_iteration_groups[ones] = []
                for dummy, minterms_set in items:
                    # Create a representative minterm for each combined group
                    # Use the first minterm value as representative
                    rep_value = min(minterms_set)
                    rep_minterm = Minterm(rep_value, self.num_vars)
                    rep_minterm.binary = dummy.binary
                    rep_minterm.ones = dummy.ones
                    rep_minterm.covered_minterms = minterms_set  # Store original minterms
                    next_iteration_groups[ones].append(rep_minterm)
            
            current_groups = next_iteration_groups
            
            # Reset used set for next iteration
            used = set()
        
        return prime_implicants
    
    def _combine_minterms(self, m1: Minterm, m2: Minterm) -> Optional[str]:
        """Try to combine two minterms. Returns combined binary or None."""
        diff_count = 0
        diff_pos = -1
        
        for i in range(self.num_vars):
            if m1.binary[i] != m2.binary[i]:
                diff_count += 1
                diff_pos = i
        
        if diff_count == 1:
            # Can combine - replace differing bit with '-'
            combined = list(m1.binary)
            combined[diff_pos] = '-'
            return ''.join(combined)
        
        return None
    
    def _find_essential_implicants(self) -> List[Implicant]:
        """Find essential prime implicants."""
        essential = []
        minterm_coverage = {m: [] for m in self.minterms}
        
        # Count coverage for each minterm
        for pi in self.prime_implicants:
            for m in self.minterms:
                if pi.covers(m):
                    minterm_coverage[m].append(pi)
        
        # Find minterms covered by only one PI
        for m, covering_pis in minterm_coverage.items():
            if len(covering_pis) == 1:
                pi = covering_pis[0]
                if pi not in essential:
                    essential.append(pi)
                    pi.essential = True
        
        return essential
    
    def _cover_minterms(self) -> List[Implicant]:
        """Cover remaining minterms using minimal set of PIs."""
        # Start with essential implicants
        cover = list(self.essential_implicants)
        covered_minterms = set()
        
        for pi in cover:
            for m in self.minterms:
                if pi.covers(m):
                    covered_minterms.add(m)
        
        # Cover remaining minterms
        remaining_minterms = set(self.minterms) - covered_minterms
        
        if not remaining_minterms:
            return cover
        
        # Greedy selection: pick PI that covers most uncovered minterms
        available_pis = [pi for pi in self.prime_implicants if pi not in cover]
        
        while remaining_minterms:
            best_pi = None
            best_coverage = 0
            
            for pi in available_pis:
                coverage = len([m for m in remaining_minterms if pi.covers(m)])
                if coverage > best_coverage:
                    best_coverage = coverage
                    best_pi = pi
            
            if best_pi:
                cover.append(best_pi)
                for m in remaining_minterms.copy():
                    if best_pi.covers(m):
                        remaining_minterms.remove(m)
                available_pis.remove(best_pi)
            else:
                # No more coverage possible
                break
        
        return cover
    
    def _generate_expression(self, implicants: List[Implicant]) -> str:
        """Generate Boolean expression from implicants."""
        terms = []
        
        for pi in implicants:
            binary = pi.get_binary_representation()
            term_parts = []
            
            for i, bit in enumerate(binary):
                if bit == '1':
                    term_parts.append(self.variable_names[i])
                elif bit == '0':
                    term_parts.append(f"!{self.variable_names[i]}")
                # bit == '-' means don't care, skip
            
            if term_parts:
                terms.append(' & '.join(term_parts))
        
        return ' | '.join(terms) if terms else "0"
    
    def _calculate_coverage(self, implicants: List[Implicant]) -> float:
        """Calculate coverage percentage."""
        covered = set()
        for pi in implicants:
            for m in self.minterms:
                if pi.covers(m):
                    covered.add(m)
        
        return len(covered) / len(self.minterms) * 100 if self.minterms else 0.0


# Example usage and testing
if __name__ == "__main__":
    qm = QuineMcCluskey()
    
    # Example 1: Simple 2-variable function
    # f(a,b) = Σ(0, 1, 3) = a'b' + a'b + ab
    print("Example 1: f(a,b) = Σ(0, 1, 3)")
    result1 = qm.minimize([0, 1, 3], num_vars=2, variable_names=['a', 'b'])
    print(f"Minimized expression: {result1['expression']}")
    print(f"Prime implicants: {result1['prime_implicants']}")
    print(f"Essential implicants: {result1['essential_implicants']}")
    print(f"Minimal implicants: {result1['minimal_implicants']}")
    print()
    
    # Example 2: 3-variable function
    # f(a,b,c) = Σ(0, 2, 5, 6, 7)
    print("Example 2: f(a,b,c) = Σ(0, 2, 5, 6, 7)")
    result2 = qm.minimize([0, 2, 5, 6, 7], num_vars=3, variable_names=['a', 'b', 'c'])
    print(f"Minimized expression: {result2['expression']}")
    print(f"Prime implicants: {result2['prime_implicants']}")
    print(f"Essential implicants: {result2['essential_implicants']}")
    print(f"Minimal implicants: {result2['minimal_implicants']}")
    print()
    
    # Example 3: With don't cares
    print("Example 3: f(a,b,c) = Σ(0, 1, 2, 5, 6) + d(3, 7)")
    result3 = qm.minimize([0, 1, 2, 5, 6], num_vars=3, 
                          variable_names=['a', 'b', 'c'],
                          dont_cares=[3, 7])
    print(f"Minimized expression: {result3['expression']}")
    print(f"Coverage: {result3['coverage']:.1f}%")

