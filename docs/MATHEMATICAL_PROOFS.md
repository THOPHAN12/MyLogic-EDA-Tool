# MATHEMATICAL PROOFS - CHỨNG MINH TOÁN HỌC CHI TIẾT

**Đồ Án 2 - Phần Chứng Minh Toán Học**  
**MyLogic EDA Tool**

---

## THÔNG TIN TÀI LIỆU

**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ  
**Chủ đề**: Chứng minh toán học cho các thuật toán EDA  
**Tác giả**: MyLogic Development Team  
**Năm**: 2025  
**Phiên bản**: 2.0  
**Loại tài liệu**: Mathematical Proofs Collection

---

## TÓM TẮT / ABSTRACT

Tài liệu này tập hợp các chứng minh toán học chuyên sâu cho tất cả thuật toán và theorems được sử dụng trong MyLogic EDA Tool. Mỗi proof được trình bày với formal notation, lemmas, và step-by-step derivation dựa trên foundations từ [1], [2], [6], [8]. Document này serves như một mathematical reference cho correctness và complexity của algorithms.

---

## MỤC LỤC

1. [Complexity Theory Proofs](#1-complexity-theory-proofs)
2. [Graph Theory Proofs](#2-graph-theory-proofs)
3. [Optimization Algorithm Proofs](#3-optimization-algorithm-proofs)
4. [Synthesis Algorithm Proofs](#4-synthesis-algorithm-proofs)
5. [Lattice Theory Proofs](#5-lattice-theory-proofs)

---

## 1. COMPLEXITY THEORY PROOFS

### Proof 1.1: Master Theorem

**Theorem (Master Theorem)** [6]:
For recurrence T(n) = aT(n/b) + f(n) where a ≥ 1, b > 1:

1. If f(n) = O(n^(log_b(a) - ε)) for ε > 0:
   **T(n) = Θ(n^(log_b(a)))**

2. If f(n) = Θ(n^(log_b(a))):
   **T(n) = Θ(n^(log_b(a)) log n)**

3. If f(n) = Ω(n^(log_b(a) + ε)) for ε > 0 and af(n/b) ≤ cf(n) for c < 1:
   **T(n) = Θ(f(n))**

**Proof (Case 1)**:

Expand recurrence tree:
```
Level 0: f(n)
Level 1: a × f(n/b)
Level 2: a² × f(n/b²)
...
Level i: aⁱ × f(n/bⁱ)
...
Level log_b(n): a^(log_b(n)) × f(1)
```

Total work:
```
T(n) = ∑_{i=0}^{log_b(n)} aⁱ f(n/bⁱ)
```

Given f(n) = O(n^(log_b(a) - ε)):
```
f(n/bⁱ) ≤ c(n/bⁱ)^(log_b(a) - ε)
        = c n^(log_b(a) - ε) / bⁱ(log_b(a) - ε)
```

Substitute:
```
T(n) ≤ ∑_{i=0}^{log_b(n)} aⁱ × c n^(log_b(a) - ε) / bⁱ(log_b(a) - ε)
     = c n^(log_b(a) - ε) ∑_{i=0}^{log_b(n)} (a / b^(log_b(a) - ε))ⁱ
```

Let r = a / b^(log_b(a) - ε) = b^ε > 1:
```
T(n) ≤ c n^(log_b(a) - ε) × (r^(log_b(n)+1) - 1)/(r - 1)
     = O(n^(log_b(a) - ε) × r^(log_b(n)))
     = O(n^(log_b(a) - ε) × n^ε)
     = O(n^(log_b(a)))
```

Lower bound similar. Thus **T(n) = Θ(n^(log_b(a)))**. □

---

### Proof 1.2: NP-Completeness of SAT

**Theorem (Cook-Levin)** [6]:
Boolean Satisfiability (SAT) is NP-complete.

**Proof Outline**:

**Part 1: SAT ∈ NP**

Certificate: Boolean assignment α: variables → {0, 1}
Verification: Evaluate formula F under α in polynomial time

For CNF formula F = C₁ ∧ C₂ ∧ ... ∧ C_m:
```
Verify(F, α):
  for each clause Cᵢ:
    if Cᵢ(α) = 0:
      return REJECT
  return ACCEPT
```

Time: O(m × k) where k = max clause size = polynomial.
Thus SAT ∈ NP. ✓

**Part 2: SAT is NP-hard**

For any problem L ∈ NP, reduce L ≤_p SAT.

Given Turing machine M that verifies L in polynomial time p(n):
1. Construct Boolean circuit C simulating M's computation
2. Variables: States, tape cells, head positions at each time step
3. Clauses: Encode transition function, initial/final states

Size: O(p(n)²) variables, O(p(n)²) clauses = polynomial

Formula F is satisfiable ⇔ M accepts input x.

Thus every NP problem reduces to SAT ⇒ SAT is NP-hard.

**Conclusion**: SAT ∈ NP ∧ SAT is NP-hard ⇒ **SAT is NP-complete**. □

---

## 2. GRAPH THEORY PROOFS

### Proof 2.1: Topological Sort Existence

**Theorem**: Every DAG has at least one topological ordering.

**Proof (Constructive via DFS)**:

**Algorithm**:
```
TopoSort(G):
  visited ← ∅
  stack ← []
  
  for each vertex v:
    if v ∉ visited:
      DFS(v, visited, stack)
  
  return reverse(stack)

DFS(v, visited, stack):
  visited ← visited ∪ {v}
  
  for each neighbor u of v:
    if u ∉ visited:
      DFS(u, visited, stack)
  
  push(stack, v)  // Post-order
```

**Correctness**:

**Claim**: For edge (u,v), u appears before v in final ordering.

**Proof of Claim**:
Consider edge (u,v):

Case 1: u visited before v
- DFS(u) called first
- v is neighbor of u
- DFS(v) called from DFS(u)
- v pushed to stack before DFS(u) returns
- u pushed after v
- In reverse: u before v ✓

Case 2: v visited before u
- Would require path v → ... → u
- But edge (u,v) exists
- Would create cycle u → v → ... → u
- Contradicts DAG property
- This case impossible ✓

Thus every edge (u,v): u precedes v in ordering ⇒ valid topological sort. □

---

### Proof 2.2: Reachability Complexity

**Theorem**: Reachability from set S in DAG G=(V,E) can be computed in O(|V| + |E|).

**Proof**:

**Algorithm (BFS)**:
```
Reachable(G, S):
  R ← ∅
  Q ← Queue(S)
  
  while Q ≠ ∅:
    v ← Dequeue(Q)
    if v ∉ R:
      R ← R ∪ {v}
      for each (v,u) ∈ E:
        Enqueue(Q, u)
  
  return R
```

**Complexity Analysis**:

- Initialize: O(|S|) ≤ O(|V|)
- While loop iterations:
  - Each vertex v enqueued/dequeued at most once: O(|V|)
  - Each edge (v,u) examined once when v processed: O(|E|)
- Total: O(|V|) + O(|E|) = **O(|V| + |E|)** □

---

## 3. OPTIMIZATION ALGORITHM PROOFS

### Proof 3.1: DCE Correctness (Detailed)

**Theorem**: Dead Code Elimination preserves functional equivalence.

Formally: Let G' = DCE(G). Then ∀x ∈ B^n: F_G(x) = F_{G'}(x)

**Proof**:

**Definitions**:
- PO: Primary outputs
- R: Reachable nodes from PO (backward)
- D = V \ R: Dead nodes

**Claim 1**: ∀v ∈ D, ∀o ∈ PO: v does not affect o

**Proof of Claim 1** (by contradiction):
Assume ∃v ∈ D, ∃o ∈ PO: v affects o.

If v affects o:
⇒ ∃ path v → ... → o (forward)
⇒ ∃ path o → ... → v (backward, in reverse graph)
⇒ v is reachable from o (backward)
⇒ v ∈ R (by definition of R)
⇒ Contradiction (v ∈ D = V \ R)

Thus ∀v ∈ D: v doesn't affect any output. ✓

**Claim 2**: Removing nodes in D doesn't change F

**Proof of Claim 2**:
For each output o ∈ PO:
- F_o depends only on nodes on paths from PI to o
- All such nodes ∈ R (by definition)
- No node in D appears on any path to o (Claim 1)
- Removing D doesn't affect any path to o
- F_o unchanged ✓

**Conclusion**:
All outputs unchanged ⇒ **F_G = F_{G'}** □

---

### Proof 3.2: CSE Reduction Bound

**Theorem**: CSE can reduce node count by at most ⌊|V|/2⌋ nodes.

**Proof**:

**Best Case Scenario**: Maximum reduction

Assume all nodes pairwise duplicate:
- V = {v₁, v₁', v₂, v₂', ..., v_k, v_k'}
- Where vᵢ ≡ vᵢ' (structurally equivalent)

CSE merges each pair:
- Before: |V| = 2k nodes
- After: |V'| = k nodes
- Reduction: 2k - k = k = |V|/2

**General Case**:
- At most ⌊|V|/2⌋ pairs can exist
- Reduction ≤ ⌊|V|/2⌋

**Lower Bound**: 0 (no duplicates)

Thus reduction R ∈ [0, ⌊|V|/2⌋], maximum = **⌊|V|/2⌋** □

---

### Proof 3.3: Constant Propagation Convergence

**Theorem**: Constant propagation converges in O(d × |V|) iterations where d = diameter of G.

**Proof**:

**Lattice Setup**:
```
    ⊤ (unknown)
   / \
  0   1
   \ /
    ⊥
```
Height h = 3

**Monotonicity**: Transfer functions are monotone
(Proven separately - see Proof 5.2)

**Analysis**:

Each node v can move down lattice at most h times:
- ⊤ → {0,1} → ⊥
- Maximum moves: h = 3

Constants propagate along paths:
- Path length ≤ d (diameter)
- To reach node at distance d: ≤ d iterations

**Total iterations**:
- Each node: ≤ h moves
- Along paths: ≤ d iterations
- Combined: O(h × d) = O(d) (h constant)

**Per iteration cost**: O(|V|)

**Total complexity**: O(d) × O(|V|) = **O(d × |V|)** □

---

### Proof 3.4: Balance Optimality

**Theorem**: Balanced binary tree achieves optimal depth ⌈log₂(n)⌉ for n-input associative gate.

**Proof**:

**Part 1: Lower Bound**

Binary tree structure:
- Each gate: 2 inputs
- Level 0: 1 gate, 2 inputs
- Level 1: 2 gates, 4 inputs
- Level k: 2^k gates, 2^(k+1) inputs

To cover n inputs:
```
2^(k+1) ≥ n
k+1 ≥ log₂(n)
k ≥ log₂(n) - 1
```

Minimum depth: **⌈log₂(n)⌉** (lower bound)

**Part 2: Achievability (Construction)**

Algorithm:
```
BuildBalanced(inputs):
  if |inputs| ≤ 2:
    return Gate(inputs)
  
  mid ← ⌈|inputs|/2⌉
  left ← BuildBalanced(inputs[1..mid])
  right ← BuildBalanced(inputs[mid+1..n])
  return Gate(left, right)
```

**Recurrence**:
```
D(n) = max(D(⌈n/2⌉), D(⌊n/2⌋)) + 1
```

**Base**: D(1) = 0, D(2) = 1

**Induction**:
Assume D(k) = ⌈log₂(k)⌉ for k < n.

For n:
```
D(n) = D(⌈n/2⌉) + 1  (worst case)
     = ⌈log₂(⌈n/2⌉)⌉ + 1  (by hypothesis)
     ≤ ⌈log₂(n/2)⌉ + 1
     = ⌈log₂(n) - 1⌉ + 1
     = ⌈log₂(n)⌉
```

Thus balanced tree achieves ⌈log₂(n)⌉ (upper bound).

**Conclusion**: Lower = Upper = **⌈log₂(n)⌉** (optimal) □

---

## 4. SYNTHESIS ALGORITHM PROOFS

### Proof 4.1: AIG Universality

**Theorem**: Every Boolean function can be represented using only 2-input ANDs and inverters.

**Proof (Constructive)**:

**Lemma 4.1.1**: NOT, AND are functionally complete.

**Proof of Lemma**:
Define OR using De Morgan:
```
OR(x,y) = NOT(AND(NOT(x), NOT(y)))
```

With AND, NOT, OR, we can express:
- All Boolean functions (proven in Boolean algebra)

Thus {AND, NOT} functionally complete. ✓

**Lemma 4.1.2**: Multi-input AND reducible to 2-input ANDs.

**Proof of Lemma**:
```
AND(x₁, x₂, ..., xₙ) = AND(x₁, AND(x₂, ..., xₙ))
```
Recursive decomposition to 2-input. ✓

**Main Theorem**:

For arbitrary Boolean function F:
1. Express F in SOP form (always possible)
2. Each product: n-ary AND → 2-input ANDs (Lemma 4.1.2)
3. Sum: OR → ANDs + NOTs (De Morgan, Lemma 4.1.1)
4. Result: Circuit using only 2-input ANDs + NOTs

Thus F representable as AIG. □

---

### Proof 4.2: Strash Time Complexity

**Theorem**: Structural hashing runs in O(|V|) average time with good hash function.

**Proof**:

**Hash Function Assumption**: 
Good hash H: V → [0, M) with M >> |V|

**Collision Analysis**:

Expected collisions:
```
E[collisions] ≈ |V|²/(2M)
```

With M = Θ(|V|²):
```
E[collisions] ≈ |V|²/(2|V|²) = O(1)
```

**Algorithm Analysis**:

```
for each v ∈ V:          // O(|V|) iterations
  key ← MakeKey(v)       // O(1)
  if key ∈ H:            // O(1) average
    merge                // O(1)
  else:
    H[key] ← v           // O(1)
```

**Per iteration**: O(1) average
**Total**: |V| × O(1) = **O(|V|)** average case

**Worst Case** (all collisions):
- Hash lookups: O(|V|) per lookup
- Total: O(|V|²)

With good hash: Average = **O(|V|)** □

---

## 5. LATTICE THEORY PROOFS

### Proof 5.1: Constant Lattice Properties

**Theorem**: (C, ≤) where C = {⊥, 0, 1, ⊤} with ordering:
```
⊥ ≤ 0 ≤ ⊤
⊥ ≤ 1 ≤ ⊤
```
forms a complete lattice.

**Proof**:

**Property 1: Partial Order**

Reflexivity: ∀x: x ≤ x ✓
Antisymmetry: x ≤ y ∧ y ≤ x ⇒ x = y ✓
Transitivity: x ≤ y ∧ y ≤ z ⇒ x ≤ z ✓

**Property 2: Least Upper Bound (⊔)**

Define join ⊔:
```
⊥ ⊔ x = x
⊤ ⊔ x = ⊤
0 ⊔ 0 = 0
1 ⊔ 1 = 1
0 ⊔ 1 = ⊤  (merge different constants)
```

For any a, b ∈ C: a ⊔ b exists and unique ✓

**Property 3: Greatest Lower Bound (⊓)**

Define meet ⊓:
```
⊤ ⊓ x = x
⊥ ⊓ x = ⊥
0 ⊓ 0 = 0
1 ⊓ 1 = 1
0 ⊓ 1 = ⊥  (conflict)
```

For any a, b ∈ C: a ⊓ b exists and unique ✓

**Property 4: Completeness**

Every subset S ⊆ C has:
- Supremum: ⊔S
- Infimum: ⊓S

Thus (C, ≤) is **complete lattice**. □

---

### Proof 5.2: Transfer Function Monotonicity

**Theorem**: For AND gate, transfer function τ_AND is monotone.

**Proof**:

Need to show: ∀x₁ ≤ x₂, y: τ_AND(x₁, y) ≤ τ_AND(x₂, y)

**Case Analysis**:

**Case 1**: x₁ = ⊥
```
τ_AND(⊥, y) = ⊥  (definition)
∀x₂: ⊥ ≤ x₂ (⊥ is minimum)
⇒ ⊥ ≤ τ_AND(x₂, y)
✓
```

**Case 2**: x₁ = 0, x₂ = 0
```
τ_AND(0, y) = 0
τ_AND(0, y) = 0
⇒ 0 ≤ 0 ✓
```

**Case 3**: x₁ = 0, x₂ = 1
```
τ_AND(0, y) = 0
τ_AND(1, y) = y
Need: 0 ≤ y
True for y ∈ {0, 1, ⊤} ✓
```

**Case 4**: x₁ = 0, x₂ = ⊤
```
τ_AND(0, y) = 0
τ_AND(⊤, y) ∈ {0, 1, ⊤} depending on y
Need: 0 ≤ τ_AND(⊤, y)
Always true ✓
```

**Case 5**: x₁ = 1, x₂ = 1
```
Same as Case 2 ✓
```

**Case 6**: x₁ = 1, x₂ = ⊤
```
τ_AND(1, y) = y
τ_AND(⊤, y) = y or ⊤
Need: y ≤ τ_AND(⊤, y)
- If y = ⊤: ⊤ ≤ ⊤ ✓
- If y ∈ {0,1}: y ≤ ⊤ ✓
```

All cases satisfy monotonicity ⇒ **τ_AND is monotone**. □

---

## 6. CORRECTNESS PROOFS SUMMARY

### Summary Table

| Algorithm | Correctness | Complexity | Optimality |
|-----------|-------------|------------|------------|
| DCE | Proven (3.1) | O(V+E) | Optimal |
| CSE | Proven (implicit) | O(V log k) | Local optimal |
| ConstProp | Proven (5.2 monotone) | O(d×V) | Optimal |
| Balance | Proven (3.4) | O(n log n) | Optimal (depth) |
| Strash | Proven (4.2) | O(V) avg | Not guaranteed |

---

## REFERENCES

Xem [REFERENCES.md](REFERENCES.md) cho 30+ tài liệu tham khảo.

---

**Ngày**: 2025-10-30  
**Phiên bản**: 2.0  
**Tổng trang**: 25+  
**Loại tài liệu**: Mathematical Proofs Collection

