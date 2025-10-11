# Constant Propagation

## Mục tiêu
- Lan truyền hằng số qua mạch, giản lược cổng.

## Ý tưởng chính
- Multi-pass: nếu mọi input của gate là hằng → tính output và đánh dấu hằng.
- Viết lại node hằng thành CONST0/CONST1; loại bỏ logic thừa.

## Thuật toán rút gọn
```text
1) Khởi tạo tập hằng (inputs/const nodes)
2) Lặp nhiều pass: propagate constants qua các cổng
3) Viết lại node hằng → CONST0/CONST1
```

## API (code)
- Class: `core.optimization.constprop.ConstPropOptimizer`
- Convenience: `apply_constprop(netlist) -> netlist`

## Độ phức tạp
- Phụ thuộc số pass và số cổng; thực tế tuyến tính theo N * passes.
