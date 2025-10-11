# Common Subexpression Elimination (CSE)

## Mục tiêu
- Loại bỏ các biểu thức con trùng lặp bằng cách chia sẻ node (shared nodes).

## Ý tưởng chính
- Chữ ký chuẩn (canonical signature) theo gate_type + sorted(inputs).
- Gom nhóm cùng chữ ký → tạo 1 shared node → cập nhật connections.

## Thuật toán rút gọn
```text
1) Duyệt node tính toán → tạo signature
2) Nhóm signature xuất hiện > 1
3) Tạo shared node, thay thế các node trùng
4) Cập nhật wires và inputs
```

## API (code)
- Class: `core.optimization.cse.CSEOptimizer`
- Convenience: `apply_cse(netlist) -> netlist`

## Độ phức tạp
- ~O(N log N) với hash + sắp xếp input; phụ thuộc netlist.

## Ví dụ
- (a AND b) lặp 2 lần → `shared_AND(a,b)`.
