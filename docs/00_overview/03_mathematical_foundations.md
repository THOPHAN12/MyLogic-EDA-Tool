# NỀN TẢNG TOÁN HỌC CHO EDA TOOLS

**Đồ Án Tốt Nghiệp**  
**MyLogic EDA Tool - Công Cụ Tự Động Hóa Thiết Kế Mạch Điện Tử**

---

## THÔNG TIN TÀI LIỆU

**Chủ đề**: Nền tảng toán học cho Electronic Design Automation  
**Tác giả**: MyLogic Development Team  
**Năm**: 2025  
**Phiên bản**: 2.0

---

## TÓM TẮT / ABSTRACT

Tài liệu này trình bày các nền tảng toán học cốt lõi được sử dụng trong công cụ EDA (Electronic Design Automation), bao gồm Boolean Algebra, Graph Theory, Binary Decision Diagrams (BDD), SAT Solving, và các thuật toán optimization. Các khái niệm được trình bày với formal definitions, theorems, và proofs dựa trên các tài liệu nghiên cứu hàng đầu [1], [2], [6], [8].

**Từ khóa**: Boolean algebra, graph theory, BDD, SAT solving, optimization algorithms, complexity theory, EDA

---

## 1. Boolean Algebra Fundamentals

### 1.1. Boolean Functions

**Định nghĩa formal** [1]:
```
Boolean function: F: B^n → B^m
where B = {0, 1}
```

**Basic Operations** [1]:
- AND (∧): x ∧ y
- OR (∨): x ∨ y  
- NOT (¬): ¬x
- XOR (⊕): x ⊕ y = (x ∧ ¬y) ∨ (¬x ∧ y)

**Laws** [1]:
- Commutative: x ∧ y = y ∧ x
- Associative: (x ∧ y) ∧ z = x ∧ (y ∧ z)
- Distributive: x ∧ (y ∨ z) = (x ∧ y) ∨ (x ∧ z)
- De Morgan's: ¬(x ∧ y) = ¬x ∨ ¬y

Các laws này form một Boolean algebra structure với identity elements (0, 1) và complement operation (¬) [1].

### 1.2. Normal Forms

**Sum of Products (SOP)** [1], [14]:
```
F = (a ∧ b ∧ ¬c) ∨ (¬a ∧ c) ∨ (b ∧ c)
```

**Product of Sums (POS)** [1], [14]:
```
F = (a ∨ b ∨ c) ∧ (¬a ∨ b) ∧ (a ∨ ¬c)
```

**Canonical Forms** [1]:
- Minterm canonical form: Σm(...) - unique representation
- Maxterm canonical form: ΠM(...) - dual của minterm form

Brayton et al. [14] chỉ ra rằng two-level minimization (Espresso algorithm) hoạt động trên SOP form để minimize số literals.

## 2. Graph Theory for Circuit Representation

### 2.1. Directed Acyclic Graph (DAG)

**Định nghĩa** [6]:
Circuit được represent bằng DAG G = (V, E):
- V: set of nodes (gates, inputs, outputs)
- E: set of directed edges (wires)
- Acyclic: no cycles (combinational logic)

**Properties** [6]:
- Topological ordering exists
- Can compute node levels
- Support incremental computation

**Theorem (Topological Sort)** [6]:
Mọi DAG có ít nhất một topological ordering. Ordering này có thể tìm được trong O(V + E) time bằng DFS hoặc Kahn's algorithm.

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

**Definition** [8]:
BDD là cấu trúc dữ liệu đại diện Boolean function dưới dạng directed acyclic graph.

**Properties** [8], [9]:
- Unique canonical form (với variable ordering cố định)
- Compact representation for many functions
- Efficient operations (AND, OR, XOR in polynomial time)

**Shannon Expansion** [8]:
```
F(x₁, x₂, ..., xₙ) = x₁ · F(1, x₂, ..., xₙ) + x̄₁ · F(0, x₂, ..., xₙ)
                    = x₁ · F_x₁ + x̄₁ · F_x̄₁
```

Bryant [8] chỉ ra rằng Shannon expansion là foundation cho BDD construction và manipulation.

**Complexity** [8], [9]:
- Best case: O(n) nodes
- Worst case: O(2^n) nodes (depends on variable ordering)
- Operations: O(|F| × |G|) for F op G

**Theorem (Canonicity)** [8]:
Với variable ordering cố định π, mỗi Boolean function F có unique ROBDD representation. Điều này cho phép equivalence checking trong O(1) time (compare pointers).

## 4. Satisfiability (SAT)

### 4.1. Boolean Satisfiability Problem

**Problem Definition** [10]:
Cho công thức Boolean F trong CNF (Conjunctive Normal Form), tìm assignment làm F = 1 hoặc chứng minh không tồn tại.

**CNF Format** [10]:
```
F = (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂) ∧ (x₂ ∨ ¬x₃)
```

**Complexity** [6]:
- NP-complete problem [6, Chapter 34]
- Exponential worst-case time
- Practical solvers efficient for many instances

**Cook's Theorem** [6]:
SAT là NP-complete problem đầu tiên được chứng minh. Mọi problem trong NP có thể reduce về SAT trong polynomial time.

### 4.2. DPLL Algorithm

**Algorithm** [10]:
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

Davis, Logemann, và Loveland [10] giới thiệu DPLL algorithm vào 1962, là foundation cho tất cả modern SAT solvers.

**Enhancements** [11]:
- Conflict-Driven Clause Learning (CDCL) [11]
- Non-chronological backtracking [11]
- Watched literals
- Restart strategies

GRASP [11] là first CDCL solver, introducing conflict analysis và learned clauses, cải thiện performance dramatically so với basic DPLL.

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

---

## 📚 TÀI LIỆU THAM KHẢO / REFERENCES

**Xem chi tiết tại**: [../REFERENCES.md](../REFERENCES.md)

### Tài liệu chính / Primary References:

[1] G. D. Hachtel and F. Somenzi, *Logic Synthesis and Verification Algorithms*, Springer, 1996.

[2] G. De Micheli, *Synthesis and Optimization of Digital Circuits*, McGraw-Hill, 1994.

[4] A. B. Kahng, J. Lienig, I. L. Markov, and J. Hu, *VLSI Physical Design: From Graph Partitioning to Timing Closure*, Springer, 2011.

[5] S. H. Gerez, *Algorithms for VLSI Design Automation*, John Wiley & Sons, 1999.

[6] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 3rd ed., MIT Press, 2009.

[7] J. Kleinberg and É. Tardos, *Algorithm Design*, Addison-Wesley, 2005.

[8] R. E. Bryant, "Graph-Based Algorithms for Boolean Function Manipulation," *IEEE Trans. Computers*, vol. C-35, no. 8, pp. 677-691, 1986.

[9] K. S. Brace, R. L. Rudell, and R. E. Bryant, "Efficient Implementation of a BDD Package," in *Proc. 27th ACM/IEEE DAC*, 1990, pp. 40-45.

[10] M. Davis, G. Logemann, and D. Loveland, "A Machine Program for Theorem-Proving," *Comm. ACM*, vol. 5, no. 7, pp. 394-397, 1962.

[11] J. P. Marques-Silva and K. A. Sakallah, "GRASP: A Search Algorithm for Propositional Satisfiability," *IEEE Trans. Computers*, vol. 48, no. 5, pp. 506-521, 1999.

[14] R. K. Brayton et al., "Logic Minimization Algorithms for VLSI Synthesis," *Proc. IEEE*, vol. 72, no. 10, pp. 1340-1362, 1984.

**Danh sách đầy đủ**: Xem [../REFERENCES.md](../REFERENCES.md) cho toàn bộ tài liệu tham khảo với citations đầy đủ.

---

## KẾT LUẬN / CONCLUSION

Tài liệu này đã trình bày các nền tảng toán học cốt lõi cho EDA tools, từ Boolean algebra cơ bản đến các thuật toán optimization phức tạp. Các khái niệm được present với formal definitions, theorems, và complexity analysis dựa trên các tài liệu nghiên cứu hàng đầu [1], [2], [6], [8].

Hiểu rõ các foundations này là essential cho việc phát triển và sử dụng hiệu quả các EDA tools như MyLogic, cũng như để nghiên cứu và cải tiến các thuật toán synthesis và optimization.

---

**Phiên bản**: 2.0  
**Ngày**: 2025-10-30  
**Tác giả**: MyLogic Development Team  
**Loại tài liệu**: Báo cáo đồ án - Mathematical Foundations
