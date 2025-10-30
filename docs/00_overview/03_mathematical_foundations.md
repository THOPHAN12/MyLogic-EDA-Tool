# Nền Tảng Toán Học cho EDA Tools

## 1. Boolean Algebra Fundamentals

### 1.1. Boolean Functions
```
Boolean function: F: B^n → B^m
where B = {0, 1}
```

**Basic Operations:**
- AND (∧): x ∧ y
- OR (∨): x ∨ y  
- NOT (¬): ¬x
- XOR (⊕): x ⊕ y = (x ∧ ¬y) ∨ (¬x ∧ y)

**Laws:**
- Commutative: x ∧ y = y ∧ x
- Associative: (x ∧ y) ∧ z = x ∧ (y ∧ z)
- Distributive: x ∧ (y ∨ z) = (x ∧ y) ∨ (x ∧ z)
- De Morgan's: ¬(x ∧ y) = ¬x ∨ ¬y

### 1.2. Normal Forms

**Sum of Products (SOP):**
```
F = (a ∧ b ∧ ¬c) ∨ (¬a ∧ c) ∨ (b ∧ c)
```

**Product of Sums (POS):**
```
F = (a ∨ b ∨ c) ∧ (¬a ∨ b) ∧ (a ∨ ¬c)
```

**Canonical Forms:**
- Minterm canonical form: Σm(...)
- Maxterm canonical form: ΠM(...)

## 2. Graph Theory for Circuit Representation

### 2.1. Directed Acyclic Graph (DAG)

Circuit được represent bằng DAG G = (V, E):
- V: set of nodes (gates, inputs, outputs)
- E: set of directed edges (wires)
- Acyclic: no cycles (combinational logic)

**Properties:**
- Topological ordering exists
- Can compute node levels
- Support incremental computation

### 2.2. Netlist as Hypergraph

Netlist = Hypergraph H = (V, N):
- V: vertices (pins)
- N: hyperedges (nets connecting multiple pins)

**Metrics:**
- HPWL (Half-Perimeter Wire Length)
- Net degree distribution
- Connectivity matrix

## 3. Binary Decision Diagrams (BDD)

### 3.1. Reduced Ordered BDD (ROBDD)

**Definition:**
BDD là cấu trúc dữ liệu đại diện Boolean function dưới dạng directed acyclic graph.

**Properties:**
- Unique canonical form (với variable ordering cố định)
- Compact representation for many functions
- Efficient operations (AND, OR, XOR in polynomial time)

**Shannon Expansion:**
```
F(x₁, x₂, ..., xₙ) = x₁ · F(1, x₂, ..., xₙ) + x̄₁ · F(0, x₂, ..., xₙ)
                    = x₁ · F_x₁ + x̄₁ · F_x̄₁
```

**Complexity:**
- Best case: O(n) nodes
- Worst case: O(2^n) nodes (depends on variable ordering)
- Operations: O(|F| × |G|) for F op G

## 4. Satisfiability (SAT)

### 4.1. Boolean Satisfiability Problem

**Problem Definition:**
Cho công thức Boolean F trong CNF (Conjunctive Normal Form), tìm assignment làm F = 1 hoặc chứng minh không tồn tại.

**CNF Format:**
```
F = (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂) ∧ (x₂ ∨ ¬x₃)
```

**Complexity:**
- NP-complete problem
- Exponential worst-case time
- Practical solvers efficient for many instances

### 4.2. DPLL Algorithm

```
DPLL(F, assignment):
  if F is empty: return SAT, assignment
  if F contains empty clause: return UNSAT
  
  // Unit propagation
  while exists unit clause (literal l):
    F = simplify(F, l)
    assignment = assignment ∪ {l}
  
  // Pure literal elimination
  for each pure literal l:
    F = simplify(F, l)
    assignment = assignment ∪ {l}
  
  // Choose variable and branch
  x = choose_variable(F)
  if DPLL(F[x=1], assignment ∪ {x}): return SAT
  return DPLL(F[x=0], assignment ∪ {¬x})
```

**Enhancements:**
- Conflict-Driven Clause Learning (CDCL)
- Non-chronological backtracking
- Watched literals
- Restart strategies

## 5. Graph Algorithms for Physical Design

### 5.1. Minimum Spanning Tree (MST)

**Prim's Algorithm:**
```
MST-Prim(G, w, r):
  for each u ∈ V[G]:
    key[u] = ∞
  key[r] = 0
  Q = V[G]  // priority queue
  while Q ≠ ∅:
    u = Extract-Min(Q)
    for each v ∈ Adj[u]:
      if v ∈ Q and w(u,v) < key[v]:
        π[v] = u
        key[v] = w(u,v)
```

**Complexity:** O((V + E) log V) with binary heap

**Application:** Steiner tree approximation for routing

### 5.2. Shortest Path (Dijkstra)

```
Dijkstra(G, w, s):
  for each vertex v:
    dist[v] = ∞
  dist[s] = 0
  Q = all vertices
  while Q ≠ ∅:
    u = Extract-Min(Q)
    for each neighbor v of u:
      if dist[v] > dist[u] + w(u,v):
        dist[v] = dist[u] + w(u,v)
        prev[v] = u
```

**Complexity:** O((V + E) log V)

**Application:** Timing analysis, maze routing

### 5.3. Max Flow / Min Cut

**Ford-Fulkerson Algorithm:**
```
Max-Flow(G, s, t):
  for each edge (u,v):
    f[u,v] = 0
  while exists augmenting path p from s to t:
    c_f(p) = min{c_f(u,v) : (u,v) in p}
    for each edge (u,v) in p:
      f[u,v] += c_f(p)
      f[v,u] -= c_f(p)
  return f
```

**Application:** Circuit partitioning, min-cut placement

## 6. Optimization Theory

### 6.1. Simulated Annealing

**Algorithm:**
```
Simulated-Annealing(s₀, T₀, α):
  s = s₀, T = T₀
  while not frozen:
    for i = 1 to L:
      s' = neighbor(s)
      ΔE = cost(s') - cost(s)
      if ΔE < 0:
        s = s'  // accept improvement
      else:
        if random() < exp(-ΔE/T):
          s = s'  // accept with probability
    T = α × T  // cooling schedule
  return s
```

**Parameters:**
- T₀: initial temperature
- α: cooling rate (0.8 - 0.95)
- L: Markov chain length

**Application:** Placement, routing, technology mapping

### 6.2. Force-Directed Methods

**Force Model:**
```
F_ij = k × (dist_current - dist_ideal)

Total force on node i:
F_i = Σ_j F_ij

Update position:
pos_i(t+1) = pos_i(t) + μ × F_i(t)
```

**Application:** Placement, floorplanning

## 7. Timing Analysis

### 7.1. Static Timing Analysis (STA)

**Arrival Time (AT):**
```
AT(v) = max{AT(u) + delay(u,v) : u ∈ fanins(v)}
AT(PI) = 0  // primary inputs
```

**Required Arrival Time (RAT):**
```
RAT(v) = min{RAT(u) - delay(v,u) : u ∈ fanouts(v)}
RAT(PO) = T_clock  // clock period
```

**Slack:**
```
Slack(v) = RAT(v) - AT(v)
```

**Critical Path:**
Path with minimum slack (usually slack = 0)

### 7.2. False Path Analysis

**False Path:** Path that can never be sensitized (logically impossible)

**Detection:**
- SAT-based analysis
- BDD-based analysis
- Simulation-based heuristics

## 8. Technology Mapping

### 8.1. Covering Problem

**Definition:**
Cho DAG network N và library L, tìm covering C sao cho:
- Mỗi node được covered bởi 1 pattern từ L
- Cost (area, delay) minimize

**Dynamic Programming:**
```
Cost(v) = min{Cost(pattern) + Σ Cost(inputs) : pattern covers v}
```

**Complexity:** O(|V| × |L| × k) với k = max pattern size

### 8.2. LUT Mapping

**K-LUT Mapping:**
Map circuit vào K-input lookup tables

**Algorithm:**
```
For each node v in topological order:
  Find best K-feasible cut C
  Map C to single K-LUT
  Update costs
```

**Cut Enumeration:**
- K-feasible: |inputs| ≤ K
- Minimize area or depth

## 9. Complexity Classes

### 9.1. Problem Classifications

**P (Polynomial):**
- Shortest path
- MST
- BFS/DFS

**NP (Non-deterministic Polynomial):**
- SAT
- Graph coloring
- TSP

**NP-Complete:**
- Technology mapping (general)
- Graph partitioning
- Bin packing

### 9.2. Approximation Algorithms

**Approximation Ratio:**
```
ρ = cost(approximate) / cost(optimal)
```

**Examples:**
- Steiner tree: 2-approximation (MST-based)
- Bin packing: 11/9-approximation
- TSP: 1.5-approximation (metric)

## 10. Data Structures for EDA

### 10.1. Union-Find (Disjoint Set)

**Operations:**
- MakeSet(x): O(1)
- Find(x): O(α(n)) amortized
- Union(x, y): O(α(n)) amortized

α(n) = inverse Ackermann function ≈ constant

**Application:** Connectivity analysis, equivalence checking

### 10.2. Hash Tables

**Collision Resolution:**
- Chaining: O(1) average, O(n) worst
- Open addressing: O(1) average, O(n) worst

**Application:** Node deduplication, structural hashing

### 10.3. Spatial Data Structures

**R-Tree:**
Hierarchical bounding boxes for 2D/3D objects

**Application:** Placement, routing, DRC

**Quadtree:**
Recursive 2D space partitioning

**Application:** Hierarchical placement, area queries

## 11. Numerical Methods

### 11.1. Linear System Solving

**For placement force-directed:**
```
Ax = b
where A is connection matrix, b is force vector
```

**Methods:**
- Gauss-Seidel: iterative
- Conjugate Gradient: faster convergence
- Sparse matrix solvers: exploit connectivity

### 11.2. Eigenvalue Problems

**For partitioning:**
```
Find λ, x such that: Lx = λx
where L is Laplacian matrix
```

**Spectral partitioning:** Use eigenvector corresponding to second smallest eigenvalue (Fiedler vector)

## 12. References

### Textbooks:
- "Introduction to Algorithms" - Cormen et al.
- "Algorithm Design" - Kleinberg & Tardos
- "Logic Synthesis and Verification" - Hachtel & Somenzi
- "VLSI Physical Design" - Kahng et al.

### Papers:
- "Logic Minimization Algorithms for VLSI Synthesis" - Brayton et al.
- "Efficient Implementation of BDDs" - Bryant
- "GRASP: A New Search Algorithm for Satisfiability" - Silva & Sakallah

---

**Phiên bản:** 1.0  
**Ngày:** 2025-10-30

