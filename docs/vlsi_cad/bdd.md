# BDD (Binary Decision Diagrams)

## Mục tiêu
- Biểu diễn và thao tác hàm Boolean hiệu quả để phục vụ verification/optimization.

## Nền tảng lý thuyết (rút gọn)
- ROBDD: dạng chuẩn tối thiểu theo thứ tự biến cố định; giảm lặp nhờ unique table.
- Phép toán trên BDD: AND/OR/XOR/NAND/NOR/XNOR; bổ sung complement, restrict.

## Kiến trúc mã nguồn
- File: `core/vlsi_cad/bdd.py`
- Lớp chính:
  - `BDDNode`: nút (var_id, low, high, value cho terminal): đại diện 0/1 và các biến.
  - `BDD`: quản lý unique table, order biến, cache áp dụng phép toán.

### API chính
- Quản lý biến & nút
  - `get_var_id(var_name: str) -> int`
  - `create_variable(var_name: str) -> BDDNode`
  - `create_constant(value: bool) -> BDDNode`
  - `make_node(var_id: int, low: BDDNode, high: BDDNode) -> BDDNode`
- Phép toán & truy vấn
  - `apply_operation(op: str, left: BDDNode, right: BDDNode) -> BDDNode`
  - `complement(node: BDDNode) -> BDDNode`
  - `restrict(node: BDDNode, var_id: int, value: bool) -> BDDNode`
  - `evaluate(node: BDDNode, assignment: Dict[str, bool]) -> bool`
  - `get_support(node: BDDNode) -> Set[str]`
  - `count_nodes(node: BDDNode) -> int`
  - `to_verilog(node: BDDNode, output_name: str) -> str`

### Dòng chảy thực thi (apply_operation)
1) Bảng ánh xạ phép toán Boolean (op_table)
2) Đệ quy `_apply_recursive`: xử lý trường hợp terminal, chia nhỏ theo var_id nhỏ hơn
3) Tạo node với `make_node` để đảm bảo chia sẻ cấu trúc và tránh lặp

## Ví dụ
```python
from core.vlsi_cad.bdd import BDD
bdd = BDD()
a = bdd.create_variable("a")
b = bdd.create_variable("b")
f_and = bdd.apply_operation("AND", a, b)
print(bdd.evaluate(f_and, {"a": True, "b": False}))  # False
print(bdd.count_nodes(f_and))
print(bdd.to_verilog(f_and, "out"))
```

## Ghi chú thực hành
- Thứ tự biến ảnh hưởng kích thước BDD.
- `to_verilog` hiện đơn giản; with multi-variable function nên cải tiến nếu cần.
