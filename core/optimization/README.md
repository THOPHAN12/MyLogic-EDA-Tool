# ⚡ Optimization Module

## 📋 Mô tả
Thư mục chứa các thuật toán tối ưu hóa logic cho MyLogic EDA Tool, tập trung vào giảm số lượng cổng, đơn giản hóa logic, và cải thiện timing.

## 📁 Files

- `dce.py` — Dead Code Elimination (DCE)
  - Loại bỏ logic không thể ảnh hưởng tới bất kỳ output nào (unreachable from outputs)
  - Thuật toán: Reachability (BFS/DFS) + cleanup wires

- `cse.py` — Common Subexpression Elimination (CSE)
  - Chia sẻ các biểu thức con trùng lặp (shared nodes), giảm số node tính toán
  - Thuật toán: Expression canonicalization + grouping

- `constprop.py` — Constant Propagation
  - Lan truyền hằng số qua mạch để đơn giản hóa cổng
  - Thuật toán: Multi-pass propagation + gate evaluation

- `balance.py` — Logic Balancing
  - Cân bằng độ sâu logic nhằm cải thiện timing (giảm critical path)
  - Thuật toán: Levelization + tree rebalancing (associative gates)

---

## 🔍 Giải thích code (tóm tắt API)

### 1) Dead Code Elimination (`dce.py`)
- Class: `DCEOptimizer`
- Hàm chính: `optimize(netlist)` → trả về netlist đã loại bỏ dead nodes/wires
- Hỗ trợ phân tích Don't Cares ở mức cơ bản (ODC/SDC, simplified)

Các bước chính:
```python
# Pseudocode (comments in English)
reachable = find_reachable_from_outputs(netlist)
netlist = remove_nodes_not_in(reachable)
netlist = update_wires_after_removal(netlist)
```

Quick use:
```python
from core.optimization.dce import DCEOptimizer, apply_dce

opt = DCEOptimizer()
netlist2 = opt.optimize(netlist)  # or: netlist2 = apply_dce(netlist, level="basic")
```

### 2) Common Subexpression Elimination (`cse.py`)
- Class: `CSEOptimizer`
- Hàm chính: `optimize(netlist)` → tạo shared nodes, cập nhật connections
- Ý tưởng: chuẩn hóa biểu thức (canonical signature) và nhóm các node trùng biểu thức

Các bước chính:
```python
# Pseudocode
common = find_common_expressions(netlist)  # AND(a,b), OR(x,y), ...
netlist = create_shared_nodes(common)
netlist = rewrite_connections_to_shared(netlist)
```

Quick use:
```python
from core.optimization.cse import CSEOptimizer, apply_cse

opt = CSEOptimizer()
netlist2 = opt.optimize(netlist)  # or: netlist2 = apply_cse(netlist)
```

### 3) Constant Propagation (`constprop.py`)
- Class: `ConstPropOptimizer`
- Hàm chính: `optimize(netlist)` → lan truyền hằng số, thay thế gate bằng CONST0/CONST1 khi có thể

Các bước chính:
```python
# Pseudocode
constants = initialize_constants_from_inputs(netlist)
for pass in range(MAX):
    changed |= propagate_constants_through_gates(netlist, constants)
netlist = rewrite_nodes_with_constants(netlist, constants)
```

Quick use:
```python
from core.optimization.constprop import ConstPropOptimizer, apply_constprop

opt = ConstPropOptimizer()
netlist2 = opt.optimize(netlist)  # or: netlist2 = apply_constprop(netlist)
```

### 4) Logic Balancing (`balance.py`)
- Class: `BalanceOptimizer`
- Hàm chính: `optimize(netlist)` → cân bằng các cổng có nhiều input thành cấu trúc cây cân bằng

Các bước chính:
```python
# Pseudocode
levels = levelize_from_inputs(netlist)  # compute node levels
targets = pick_nodes_to_balance(levels)
for n in targets:
    if can_balance(n):
        netlist = balance_node_inputs_as_tree(netlist, n)
```

Quick use:
```python
from core.optimization.balance import BalanceOptimizer, apply_balance

opt = BalanceOptimizer()
netlist2 = opt.optimize(netlist)  # or: netlist2 = apply_balance(netlist)
```

---

## 🚀 Ví dụ sử dụng chuỗi tối ưu hóa (pipeline)
```python
# Example pipeline (comments in English)
from core.optimization.dce import apply_dce
from core.optimization.cse import apply_cse
from core.optimization.constprop import apply_constprop
from core.optimization.balance import apply_balance

netlist1 = apply_dce(netlist0, level="basic")
netlist2 = apply_cse(netlist1)
netlist3 = apply_constprop(netlist2)
netlist4 = apply_balance(netlist3)
```

---

## 📊 Optimization metrics
- Area: Gate count reduction
- Delay: Critical path/timing improvement
- Power: Switching activity reduction (gián tiếp)
- Structural: Depth/level distribution

---

## 📐 CƠ SỞ LÝ THUYẾT (Theoretical Foundation)

### 1. Logic Optimization trong VLSI CAD

Logic optimization là quá trình biến đổi mạch logic để cải thiện các metrics như diện tích (area), độ trễ (delay), và công suất tiêu thụ (power) mà không thay đổi chức năng của mạch.

**Định nghĩa formal:**
- Cho mạch logic C với hàm Boolean F: B^n → B^m
- Optimization tìm C' sao cho F' = F (equivalent) và Cost(C') < Cost(C)
- Cost function thường là: Area, Delay, Power, hoặc weighted combination

### 2. Dead Code Elimination (DCE) - Lý Thuyết

**Định nghĩa:**
Dead code là các nodes trong mạch không có ảnh hưởng đến bất kỳ output nào.

**Formal definition:**
- Node v là dead nếu không tồn tại path từ v đến bất kỳ primary output nào
- Reachability: R ⊆ V là tập các nodes reachable từ outputs
- Dead nodes: D = V \ R

**Thuật toán:**
```
1. Backward traversal từ outputs (BFS/DFS)
2. Mark các nodes reachable
3. Remove các nodes không được mark
4. Update wires và connections
```

**Complexity:**
- Time: O(|V| + |E|) với V là nodes, E là edges
- Space: O(|V|) cho visited set

**Don't Care Conditions:**
- **Satisfiability Don't Cares (SDC)**: Các input combinations không thể xảy ra
- **Observability Don't Cares (ODC)**: Thay đổi output của node không ảnh hưởng outputs
- DCE nâng cao sử dụng ODC/SDC để remove thêm nodes

**Theorem:**
Nếu node v có ODC(v) = 1 (output không quan sát được), v có thể safely remove.

### 3. Common Subexpression Elimination (CSE) - Lý Thuyết

**Định nghĩa:**
Common subexpression là các biểu thức logic giống nhau xuất hiện nhiều lần trong mạch.

**Formal definition:**
- Expression signature: σ(node) = (type, sorted_inputs)
- Nodes u, v equivalent nếu σ(u) = σ(v)
- CSE merges equivalent nodes

**Thuật toán:**
```
1. Canonical form: Tạo signature cho mỗi node
   - Sort inputs để đảm bảo commutativity (AND(a,b) = AND(b,a))
   - Include gate type
2. Hash table: Group nodes với cùng signature
3. Merge: Chọn 1 representative, redirect fanouts
4. Update connections
```

**Complexity:**
- Time: O(|V| × log(k)) với k là max fanins
- Space: O(|V|) cho hash table

**Properties:**
- **Soundness**: Không thay đổi functionality
- **Optimality**: Local optimal (không guarantee global)
- **Ordering**: Kết quả phụ thuộc thứ tự process nodes

### 4. Constant Propagation - Lý Thuyết

**Định nghĩa:**
Constant propagation lan truyền giá trị constants qua mạch để simplify logic.

**Data Flow Analysis:**
```
Constants[node] = 
  if node is constant input: {value}
  if all fanins have constants: evaluate(gate, fanin_values)
  otherwise: ⊤ (unknown)
```

**Lattice Theory:**
```
    ⊤ (unknown)
   / \
  0   1  (known constants)
   \ /
    ⊥ (unreachable)
```

**Iterative Algorithm:**
```
1. Initialize: Constants = {} (empty)
2. Repeat until fixpoint:
   - For each node v:
     - If all inputs known: compute Constants[v]
     - If Constants[v] = 0 or 1: replace with CONST
3. Simplify gates using known constants
```

**Complexity:**
- Time: O(k × |V|) với k là số iterations (usually k ≤ diameter)
- Space: O(|V|) cho constant map

**Optimizations:**
- **AND(x, 0) → 0**: x bị override
- **AND(x, 1) → x**: identity
- **OR(x, 1) → 1**: x bị override
- **OR(x, 0) → x**: identity

### 5. Logic Balancing - Lý Thuyết

**Định nghĩa:**
Logic balancing tối ưu độ sâu (depth) của mạch để giảm critical path delay.

**Level Assignment:**
- Level(PI) = 0 (primary inputs)
- Level(v) = max{Level(u) : u ∈ fanins(v)} + 1
- Depth = max{Level(v) : v ∈ PO}

**Associativity Property:**
Các gates như AND, OR có tính chất associative:
- (a AND b) AND c = a AND (b AND c)

**Balanced Tree Construction:**
```
Unbalanced:   AND(a, b, c, d, e)  →  depth = 1
Balanced:     
       AND
      /   \
    AND   AND
   /  \    |
  AND  e   d
 /  \
a    b
      \
       c
Depth = ⌈log₂(n)⌉ với n = số inputs
```

**Theorem (Optimal Balancing):**
Cho n-input associative gate:
- Minimum depth = ⌈log₂(n)⌉
- Achieved by balanced binary tree

**Complexity:**
- Time: O(|V| + |E|) cho levelization
- Time: O(n log n) cho rebalancing n-input gate
- Space: O(|V|)

### 6. Complexity Analysis Summary

| Algorithm | Time Complexity | Space Complexity | Quality |
|-----------|----------------|------------------|---------|
| DCE | O(V + E) | O(V) | Optimal |
| CSE | O(V log k) | O(V) | Local optimal |
| ConstProp | O(k × V) | O(V) | Optimal |
| Balance | O(V + E) | O(V) | Optimal (depth) |

### 7. Interaction Between Optimizations

**Optimization Order Matters:**
```
Strash → DCE → CSE → ConstProp → Balance
```

**Why this order?**
1. **Strash first**: Remove obvious duplicates
2. **DCE after Strash**: Remove dead nodes from merging
3. **CSE after DCE**: Find common patterns in cleaner circuit
4. **ConstProp after CSE**: Propagate through shared nodes
5. **Balance last**: Optimize timing on final structure

**Fixed-Point Iteration:**
Lặp lại pipeline cho đến khi không còn thay đổi (fixpoint).

### 8. Metrics và Quality Measurement

**Area Metrics:**
- Gate count: Σ gates
- Literal count: Σ fanins
- Node count: |V|

**Delay Metrics:**
- Level-based delay: max{Level(v)}
- Unit-delay model: mỗi gate = 1 unit
- Technology-mapped delay: actual cell delays

**Power Metrics:**
- Switching activity: α × C × V² × f
- Leakage power: Static current

### 9. Formal Verification of Optimization

**Correctness Criteria:**
- Functional equivalence: F(C) ≡ F(C')
- Structural invariants: maintain netlist structure properties

**Verification Methods:**
- BDD-based equivalence checking
- SAT-based equivalence checking
- Simulation-based validation

**Theorem (Soundness):**
Mỗi optimization pass preserves functional equivalence:
∀ input x: C(x) = C'(x)

## 📚 Tài liệu tham khảo

### Books:
- "Logic Synthesis and Verification Algorithms" - Hachtel & Somenzi
- "Synthesis and Optimization of Digital Circuits" - De Micheli
- "VLSI Physical Design: From Graph Partitioning to Timing Closure" - Kahng et al.

### Papers:
- "Logic Optimization with a Truth Table Lookup" - Mishchenko et al.
- "Fast Boolean Optimization Using Redundancy Addition" - Chatterjee & Brayton

### Tools:
- ABC (Berkeley Logic Synthesis Tool)
- Yosys (Open Synthesis Suite)
- SIS (UC Berkeley Synthesis System)

---

Ngày cập nhật: 2025-10-30  
Tác giả: MyLogic EDA Tool Team  
Phiên bản: 2.0
