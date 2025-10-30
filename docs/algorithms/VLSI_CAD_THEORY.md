# VLSI CAD Algorithms - Lý Thuyết Chi Tiết

## 1. Binary Decision Diagrams (BDD)

### 1.1. Định Nghĩa

**BDD:** Directed acyclic graph representation of Boolean function

**Structure:**
- Internal nodes: variables
- Terminal nodes: 0, 1
- Edges: low (dashed), high (solid)

**Shannon Expansion:**
```
f(x₁,...,xₙ) = x₁ · f_x₁ + x̄₁ · f_x̄₁
```

### 1.2. Reduced Ordered BDD (ROBDD)

**Ordering:** Variables appear in same order on all paths

**Reduction Rules:**
1. **Merge equivalent nodes:**
   ```
   If low(v₁) = low(v₂) and high(v₁) = high(v₂)
   Then merge v₁ and v₂
   ```

2. **Eliminate redundant tests:**
   ```
   If low(v) = high(v) = w
   Then redirect edges to v directly to w
   ```

**Canonical Property:**
Given variable ordering, ROBDD is unique for each Boolean function.

### 1.3. BDD Operations

**Apply Operation:**
```
Apply(op, F, G):
  if F and G are terminals:
    return op(F, G)
  if (op, F, G) in cache:
    return cache[(op, F, G)]
  
  x = top_variable(F, G)
  F_low, F_high = cofactors(F, x)
  G_low, G_high = cofactors(G, x)
  
  low = Apply(op, F_low, G_low)
  high = Apply(op, F_high, G_high)
  
  result = make_node(x, low, high)
  cache[(op, F, G)] = result
  return result
```

**Complexity:**
- Best case: O(|F|) or O(|G|)
- Worst case: O(|F| × |G|)
- With caching: O(|F| × |G|) guaranteed

### 1.4. Variable Ordering

**Problem:** Find ordering minimizing BDD size

**NP-Complete:** Finding optimal ordering

**Heuristics:**
- Static ordering:
  - Depth-First Search (DFS)
  - Breadth-First Search (BFS)
  - Circuit-based (topological)
  
- Dynamic reordering:
  - Sifting: try all positions for each variable
  - Window permutation: optimize small windows
  - Simulated annealing

**Sifting Algorithm:**
```
for each variable v:
    best_position = current_position
    best_size = BDD_size
    
    for each position p in [1, n]:
        move v to position p
        if BDD_size < best_size:
            best_position = p
            best_size = BDD_size
    
    move v to best_position
```

### 1.5. Applications

**Equivalence Checking:**
```
F ≡ G ⟺ BDD(F) = BDD(G)
```

**Satisfiability:**
```
F is SAT ⟺ BDD(F) ≠ 0
```

**Counting Solutions:**
```
Count(F) = Count(F_x) + Count(F_x̄)
```

## 2. SAT Solving

### 2.1. DPLL (Davis-Putnam-Logemann-Loveland)

**Core Algorithm:**
```
DPLL(F):
  // Base cases
  if F is empty: return SAT
  if F contains empty clause: return UNSAT
  
  // Unit propagation
  while exists unit clause {l}:
    F = simplify(F, l)
  
  // Pure literal elimination
  while exists pure literal l:
    F = simplify(F, l)
  
  // Branching
  l = choose_literal(F)
  if DPLL(F ∧ l): return SAT
  return DPLL(F ∧ ¬l)
```

### 2.2. Conflict-Driven Clause Learning (CDCL)

**Enhancements over DPLL:**
1. Learn conflict clauses
2. Non-chronological backtracking
3. Watched literals
4. Restarts
5. Clause deletion

**Implication Graph:**
- Nodes: assignments
- Edges: implications
- Conflict: analyze to learn clause

**Conflict Analysis:**
```
analyze_conflict(conflict):
  clause = {}
  level = decision_level
  
  while more than one literal at current level:
    antecedent = reason(conflict_var)
    clause = resolve(clause, antecedent)
    conflict_var = next_var_at_level(clause, level)
  
  return clause, backtrack_level
```

**1UIP (First Unique Implication Point):**
Closest conflict node reachable from decision.

### 2.3. Watched Literals

**Idea:** Watch 2 literals per clause for efficiency

**Invariant:**
```
Clause is satisfied or has ≥ 2 unassigned literals
```

**Benefit:**
- No need to iterate all clauses on each assignment
- Only update when watched literal assigned

### 2.4. Clause Learning Strategies

**Resolution:**
```
C₁ ∨ x, C₂ ∨ ¬x ⊢ C₁ ∨ C₂
```

**Learned Clause Properties:**
- Asserting: forces assignment at backtrack level
- Smaller: remove redundant literals
- Relevant: relates to conflict

### 2.5. Preprocessing

**Techniques:**
- Variable elimination
- Clause subsumption
- Failed literal probing
- Binary implication graph analysis

## 3. Placement Algorithms

### 3.1. Objective Functions

**Half-Perimeter Wire Length (HPWL):**
```
HPWL(net) = (max_x - min_x) + (max_y - min_y)
```

**Quadratic Wire Length:**
```
WL(net) = Σ_{(i,j) ∈ edges} [(x_i - x_j)² + (y_i - y_j)²]
```

**Overlap:**
```
Overlap = Σ_{cells i,j} overlap_area(i, j)
```

### 3.2. Analytic Placement

**Force-Directed:**
```
F_net(cell) = Σ_{pins in net} k · (pos_pin - pos_cell)
```

**Quadratic Optimization:**
```
Minimize: Σ_nets Σ_{edges} ½ · weight · distance²
Subject to: no overlap constraints
```

**Linear System:**
```
Ax = b
```
where A is connectivity matrix.

**Solving:**
- Conjugate Gradient
- Gauss-Seidel
- Successive Over-Relaxation (SOR)

### 3.3. Simulated Annealing

**Energy Function:**
```
E = α · HPWL + β · overlap
```

**Acceptance Probability:**
```
P(accept) = {
  1,                    if ΔE < 0
  exp(-ΔE/T),          if ΔE ≥ 0
}
```

**Cooling Schedule:**
```
T(k+1) = α · T(k)     (geometric)
T(k+1) = T(0)/(1+βk)  (logarithmic)
```

**Parameters:**
- T₀ = initial temperature (calibrate for ~90% acceptance)
- α = cooling rate (0.85 - 0.95)
- Inner loop length: 10n - 100n moves
- Frozen condition: no improvement in k iterations

### 3.4. Partitioning-Based Placement

**Recursive Bisection:**
```
partition(region, cells):
  if |cells| < threshold:
    place_cells_analytically(region, cells)
    return
  
  (left_cells, right_cells) = bisect(cells)
  (left_region, right_region) = split(region)
  
  partition(left_region, left_cells)
  partition(right_region, right_cells)
```

**Min-Cut Objective:**
Minimize nets crossing partition boundary.

**FM (Fiduccia-Mattheyses) Algorithm:**
```
initialize(cells, partition)
while improvement:
  for each move:
    cell = best_gain_cell()
    move cell to other partition
    lock cell
    update gains
  
  find best prefix of moves
  apply best prefix
  unlock cells
```

**Complexity:** O(P) per pass, P = total pins

### 3.5. Legalization

**Problem:** Remove overlaps while minimizing displacement

**Techniques:**
- Tetris legalization: place cells left-to-right
- Network flow: model as min-cost flow
- Linear Programming: optimize positions

## 4. Routing Algorithms

### 4.1. Maze Routing (Lee's Algorithm)

**Wave Propagation:**
```
queue = {source}
distance[source] = 0

while queue not empty:
  current = queue.pop()
  if current = target:
    return backtrace(current, source)
  
  for neighbor in neighbors(current):
    if not visited[neighbor]:
      distance[neighbor] = distance[current] + 1
      queue.push(neighbor)
      parent[neighbor] = current
```

**Complexity:** O(grid_size)

**Guarantee:** Finds shortest path if exists

### 4.2. A* Search

**Heuristic Function:**
```
f(n) = g(n) + h(n)
```
- g(n): actual cost from source to n
- h(n): estimated cost from n to target (Manhattan distance)

**Admissibility:**
```
h(n) ≤ actual_cost(n, target)
```

**A* Algorithm:**
```
open = {source}
g[source] = 0
f[source] = h(source)

while open not empty:
  current = open.extract_min(f)
  
  if current = target:
    return reconstruct_path(current)
  
  for neighbor in neighbors(current):
    tentative_g = g[current] + cost(current, neighbor)
    if tentative_g < g[neighbor]:
      g[neighbor] = tentative_g
      f[neighbor] = g[neighbor] + h(neighbor)
      parent[neighbor] = current
      open.add(neighbor)
```

**Optimality:** Finds optimal path with admissible heuristic

### 4.3. Global Routing

**Problem:** Route all nets through routing regions

**Representation:**
- Global routing graph (GRG)
- Nodes: routing regions
- Edges: boundaries with capacities

**ILP Formulation:**
```
Minimize: Σ_nets Σ_edges weight · usage
Subject to:
  - Flow conservation
  - Edge capacity constraints
  - Net connectivity
```

**Heuristics:**
- Sequential routing
- Rip-up and reroute
- Negotiation-based (PathFinder)

### 4.4. Detailed Routing

**Problem:** Assign exact tracks and vias

**Track Assignment:**
- Left-edge algorithm (channel routing)
- Over-the-cell routing
- Multi-layer assignment

**Via Minimization:**
Prefer same-layer routing to reduce vias.

### 4.5. Multi-Net Routing

**Net Ordering:**
- Critical nets first
- Congested regions prioritized
- Random with restarts

**PathFinder Algorithm:**
```
repeat:
  for each net:
    rip_up(net)
    route(net) with congestion cost
  
  update edge costs based on congestion
until converged or max iterations
```

**Cost Function:**
```
cost(edge) = base + history · overflow
```

## 5. Static Timing Analysis

### 5.1. Timing Graph

**Nodes:**
- Pin nodes
- Gate nodes

**Edges:**
- Arc delay: gate delay
- Wire delay: interconnect delay

### 5.2. Arrival Time Computation

**Forward Traversal:**
```
AT(PI) = 0

for each gate in topological order:
  for each output pin p:
    AT(p) = max{AT(input) + delay(input, p)}
```

### 5.3. Required Arrival Time

**Backward Traversal:**
```
RAT(PO) = T_clock

for each gate in reverse topological order:
  for each input pin p:
    RAT(p) = min{RAT(output) - delay(p, output)}
```

### 5.4. Slack and Critical Path

**Slack:**
```
Slack(pin) = RAT(pin) - AT(pin)
```

**Critical Path:**
Path with minimum (usually zero) slack.

**Timing Violation:**
```
Setup: Slack < 0
Hold: AT(capture) < AT(launch) + hold_time
```

### 5.5. Statistical STA (SSTA)

**Uncertainty Sources:**
- Process variation
- Temperature variation
- Voltage variation

**Model:**
```
delay ~ Normal(μ, σ²)
```

**Max Operation:**
```
max(X, Y) where X ~ N(μ_x, σ_x), Y ~ N(μ_y, σ_y)
```

Approximate with Tightness Probability.

## 6. Power Analysis

### 6.1. Dynamic Power

**Switching Power:**
```
P_dynamic = α · C · V² · f
```
- α: switching activity
- C: load capacitance
- V: supply voltage
- f: clock frequency

### 6.2. Static Power

**Leakage:**
```
P_static = V · I_leakage
```

**Components:**
- Subthreshold leakage
- Gate oxide leakage
- Junction leakage

### 6.3. Activity Estimation

**Probability-Based:**
```
P(signal = 1) = probability
α = P(0→1 transition)
```

**Simulation-Based:**
Count transitions over typical inputs.

## 7. Design Rule Checking (DRC)

### 7.1. Geometric Rules

**Minimum Width:**
```
width(shape) ≥ min_width
```

**Minimum Spacing:**
```
distance(shape1, shape2) ≥ min_spacing
```

**Minimum Area:**
```
area(shape) ≥ min_area
```

### 7.2. Algorithm

**Scanline:**
```
sort events by x-coordinate
for each event:
  update active shapes
  check spacing violations
```

**Complexity:** O(n log n + k) where k = violations

## 8. References

### Books:
- "VLSI Physical Design" - Kahng et al.
- "Electronic Design Automation" - Wang et al.
- "Timing" - Rubin & Gerez

### Tools:
- Cadence Innovus (place & route)
- Synopsys IC Compiler
- OpenROAD (open-source)

---

**Version:** 1.0  
**Date:** 2025-10-30

