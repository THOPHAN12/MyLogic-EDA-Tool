# SAT Solver (DPLL)

## Mục tiêu
- Kiểm tra tính thỏa mãn của công thức Boolean (CNF) và phục vụ verification.

## Nền tảng lý thuyết (rút gọn)
- DPLL: unit propagation, decision, backtracking; (CDCL là mở rộng, ở đây đơn giản).
- CNF: mệnh đề (clause) là OR các literal; công thức là AND các mệnh đề.

## Kiến trúc mã nguồn
- File: `core/vlsi_cad/sat_solver.py`
- Lớp chính:
  - `CNFClause`: đại diện mệnh đề; kiểm tra satisfied/unit.
  - `SATSolver`: thêm mệnh đề, giải; thống kê decisions/conflicts/backtracks.
  - `SATBasedVerifier`: xây miter CNF để kiểm định tương đương/thuộc tính (đơn giản).

### API chính
- SATSolver:
  - `add_clause(literals: List[int]) -> None`
  - `add_clauses_from_formula(formula: List[List[int]]) -> None`
  - `solve() -> Tuple[bool, Optional[Dict[int, bool]]]`
  - `get_statistics() -> Dict[str, int]`
- SATBasedVerifier:
  - `verify_equivalence(c1: Dict, c2: Dict) -> Tuple[bool, Optional[Dict]]`
  - `verify_property(circ: Dict, prop: str) -> Tuple[bool, Optional[Dict]]`

### Dòng chảy thực thi (solve)
1) Reset trạng thái; kiểm tra empty clause/formula
2) Vòng lặp:
   - Unit propagation → cập nhật assignment
   - Nếu tất cả mệnh đề được thỏa mãn → SAT
   - Chọn biến chưa gán → quyết định (True) → đệ quy giải
   - Nếu thất bại → backtrack và thử giá trị ngược lại

## Ví dụ
```python
from core.vlsi_cad.sat_solver import SATSolver
solver = SATSolver()
solver.add_clause([1, 2])
solver.add_clause([-1, 3])
solver.add_clause([-2, -3])
print(solver.solve())
print(solver.get_statistics())
```

## Ghi chú thực hành
- Với bài toán lớn, cần CDCL/heuristic chọn biến tốt hơn.
- Chuyển mạch sang CNF thực tế nên dùng Tseitin.
