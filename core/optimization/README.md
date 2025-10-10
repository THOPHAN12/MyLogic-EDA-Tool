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

## 📚 Tài liệu tham khảo
- VLSI CAD textbooks (logic optimization)
- ABC/Yosys documentation (inspiration/algorithms)
- Academic papers về logic optimization, technology mapping

---

Ngày cập nhật: 2025-10-10  
Tác giả: MyLogic EDA Tool Team  
Phiên bản: 1.1
