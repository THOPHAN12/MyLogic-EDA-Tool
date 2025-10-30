# Logic Synthesis - Lý Thuyết Chi Tiết

## 1. Structural Hashing (Strash)

### 1.1. Định Nghĩa Formal

**Structural equivalence:**
Hai nodes u, v là structurally equivalent nếu:
- `type(u) = type(v)`
- `fanins(u) = fanins(v)` (với order không quan trọng cho commutative ops)

**Hash function:**
```
h(node) = hash(type, sort(fanins))
```

### 1.2. Algorithm

```python
def strash(netlist):
    hash_table = {}
    new_netlist = {}
    
    for node in topological_order(netlist):
        key = compute_hash(node.type, sort(node.fanins))
        
        if key in hash_table:
            # Structural duplicate found
            representative = hash_table[key]
            redirect_fanouts(node, representative)
        else:
            # New structure
            hash_table[key] = node
            new_netlist.add(node)
    
    return new_netlist
```

### 1.3. Correctness

**Theorem 1 (Soundness):**
Structural hashing preserves circuit functionality.

**Proof:**
- Equivalent structures compute same function
- Fanout redirection maintains connectivity
- No feedback loops introduced (DAG property maintained)
∴ F(C) = F(strash(C))

**Theorem 2 (Optimality):**
Strash finds all structural redundancies within single pass.

### 1.4. Complexity Analysis

**Time:**
- Sort fanins: O(k log k) per node
- Hash lookup: O(1) average
- Total: O(|V| × k log k)

**Space:**
- Hash table: O(|V|)
- Temporary: O(|V|)

### 1.5. Extensions

**Buffer elimination:**
```
If node is BUF with single fanin:
  Replace all fanouts with fanin directly
```

**Inverter pairing:**
```
NOT(NOT(x)) → x
```

## 2. And-Inverter Graph (AIG)

### 2.1. Definition

AIG là DAG chỉ dùng:
- 2-input AND gates
- Inverters (edge attributes)

**Normal Form:**
```
Any Boolean function → AIG representation
```

### 2.2. Conversion Rules

**OR to AND:**
```
a ∨ b = ¬(¬a ∧ ¬b)   (De Morgan)
```

**XOR to AND:**
```
a ⊕ b = (a ∧ ¬b) ∨ (¬a ∧ b)
      = ¬(¬(a ∧ ¬b) ∧ ¬(¬a ∧ b))
```

**NAND/NOR:**
```
NAND(a,b) = ¬(a ∧ b)
NOR(a,b) = ¬(a ∨ b) = ¬¬(¬a ∧ ¬b) = ¬a ∧ ¬b
```

### 2.3. AIG Minimization

**Algebraic Methods:**
- Rewriting: local pattern matching
- Refactoring: extract common factors
- Balancing: tree restructuring

**Example:**
```
Original: (a ∧ b) ∨ (a ∧ c)
Factored: a ∧ (b ∨ c)
AIG:      a ∧ ¬(¬b ∧ ¬c)
```

### 2.4. AIG Complexity

**Size metrics:**
- Node count: |AIG|
- Level count: depth(AIG)
- Literal count: 2 × |AND nodes| + |inverters|

**Optimal AIG:**
Minimum size AIG for function F

**Theorem:**
Finding optimal AIG is NP-hard.

**Heuristics:**
- Local rewriting (polynomial time)
- Iterative improvement
- Random perturbations

## 3. Technology-Independent Optimization

### 3.1. Boolean Network

**Definition:**
BN = (G, Φ) where:
- G = (V, E): DAG
- Φ: V → Boolean functions

**Each node:**
```
v: f_v(fanins(v))
```

### 3.2. Algebraic Division

**Literal division:**
```
F = G × Q + R
where G is divisor, Q is quotient, R is remainder
```

**Kernel extraction:**
```
Kernel K of F: cube-free divisor with cube-free quotient
```

**Example:**
```
F = a·b + a·c + b·c
Kernels: {a+c, b+c}
Quotient for a+c: b
```

### 3.3. Factorization

**Algebraic factorization:**
```
F = ab + ac + ad = a(b + c + d)
```

**Boolean factorization:**
```
F = a·b + a·c + b·c
  = (a+b)(a+c)(b+c)  (POS form)
```

### 3.4. Substitution and Simplification

**Algebraic substitution:**
```
If H appears in F and G:
  Create new node: v = H
  Replace H in F and G with v
```

**Benefit:**
- Reduced literal count
- Potential for further optimization

## 4. Multi-Level Logic Optimization

### 4.1. Two-Level vs Multi-Level

**Two-level (SOP/POS):**
- Fast evaluation (2 gate delays)
- Large area (many literals)

**Multi-level:**
- Slower evaluation (multiple levels)
- Smaller area (shared logic)

### 4.2. Trade-offs

**Area-Delay Product:**
```
ADP = Area × Delay
```

Optimize for minimum ADP.

**Example:**
```
Two-level:   F = abc + abd + acd + bcd
             Literals = 12, Delay = 2

Multi-level: F = ab(c+d) + cd(a+b)
                = (ab+cd)(c+d+a+b)
             Literals = 8, Delay = 3
```

### 4.3. Collapse and Decompose

**Collapse:**
```
Substitute node functions into fanouts
Result: fewer nodes, more literals per node
```

**Decompose:**
```
Extract common subexpressions
Result: more nodes, fewer literals per node
```

**Strategy:**
Iterate collapse/decompose to find sweet spot.

## 5. Equivalence Checking

### 5.1. Problem Definition

**Given:** Circuits C₁ and C₂
**Question:** ∀ input x, C₁(x) = C₂(x)?

### 5.2. Combinational Equivalence Checking (CEC)

**Miter Construction:**
```
Miter(C₁, C₂):
  Connect same inputs
  XOR corresponding outputs
  OR all XORs
  If result = 0, circuits equivalent
```

**SAT-based:**
```
If Miter is UNSAT → circuits equivalent
If Miter is SAT → counterexample found
```

### 5.3. Random Simulation

**Algorithm:**
```
for i = 1 to N:
    x = random_input()
    if C₁(x) ≠ C₂(x):
        return INEQUIVALENT, x
return LIKELY_EQUIVALENT
```

**Limitation:** Cannot prove equivalence

### 5.4. Formal Verification

**BDD-based:**
```
Build BDD₁ for C₁
Build BDD₂ for C₂
If BDD₁ = BDD₂ (canonical) → equivalent
```

**SAT-based:**
```
CNF = Miter(C₁, C₂)
If SAT(CNF) → inequivalent
If UNSAT(CNF) → equivalent
```

## 6. Resubstitution

### 6.1. Definition

**Resubstitution:**
Replace node function with equivalent using existing nodes as building blocks.

### 6.2. Algorithm

```python
def resubstitute(node, candidates):
    f = function(node)
    for subset in power_set(candidates):
        for op in [AND, OR, XOR, ...]:
            g = construct_function(subset, op)
            if equivalent(f, g):
                replace(node, g)
                return True
    return False
```

### 6.3. Don't Care Sets

**ODC (Observability Don't Cares):**
Conditions where node output doesn't affect circuit output.

**SDC (Satisfiability Don't Cares):**
Input combinations that never occur.

**Combined:**
```
DC = ODC ∪ SDC
```

**Resubstitution with DCs:**
```
f can be replaced with g if:
  f = g on ON-set
  f = g on DC-set (don't care)
```

## 7. Retiming

### 7.1. Definition

**Retiming:**
Move registers (flip-flops) to optimize clock period while preserving functionality.

### 7.2. Constraints

**Legal retiming:**
- No negative register count on any edge
- Preserve I/O latency

**Objective:**
Minimize clock period Φ

### 7.3. Linear Programming Formulation

**Variables:**
```
r(v): retiming value of node v
```

**Constraints:**
```
For each edge (u,v) with delay d(u,v):
  r(v) - r(u) ≤ w(u,v)  (register count)

For each path p with delay D(p):
  D(p) ≤ Φ  (clock constraint)
```

### 7.4. Leiserson-Saxe Algorithm

**Polynomial-time algorithm** for optimal retiming.

**Complexity:** O(|V|³)

## 8. Synthesis Flow Integration

### 8.1. Complete Flow

```
RTL
  ↓ [Parse]
Logic Network
  ↓ [Strash]
AIG
  ↓ [Algebraic Optimization]
Optimized AIG
  ↓ [Technology-Independent Opt]
Multi-level Network
  ↓ [Technology Mapping]
Gate-level Netlist
  ↓ [Post-mapping Opt]
Final Netlist
```

### 8.2. Optimization Loop

```
repeat until convergence:
    Strash
    DCE
    CSE
    ConstProp
    Resubstitution
    Balance
```

### 8.3. Quality Metrics

**QoR (Quality of Results):**
- Area: gate count, cell area
- Delay: critical path, WNS (worst negative slack)
- Power: dynamic + static
- Routability: congestion metrics

**PPA (Power-Performance-Area):**
Optimize trade-off between three metrics.

## 9. Advanced Topics

### 9.1. Sequential Synthesis

**Retiming:** Move registers
**Register minimization:** Reduce register count
**State encoding:** Optimize FSM encoding

### 9.2. High-Level Synthesis (HLS)

**Behavioral to RTL:**
- Scheduling: assign operations to clock cycles
- Binding: assign operations to resources
- Allocation: determine resource quantities

### 9.3. Physical Synthesis

**Timing-driven synthesis:**
- Consider placement
- Consider routing congestion
- Optimize critical paths

## 10. References

### Seminal Papers:
- "Multi-Level Logic Minimization" - Brayton et al., 1984
- "Optimal Retiming" - Leiserson & Saxe, 1991
- "DAG-Aware AIG Rewriting" - Mishchenko et al., 2006

### Books:
- "Synthesis and Optimization of Digital Circuits" - De Micheli
- "Logic Synthesis" - Hachtel & Somenzi
- "The Art of Logic Synthesis" - ABC Team

---

**Version:** 1.0  
**Date:** 2025-10-30

