# Logic Balancing

## Mục tiêu
- Cân bằng độ sâu logic để cải thiện timing (giảm critical path).

## Ý tưởng chính
- Levelization toàn mạng → chọn node cần cân bằng (level cao, fanout nhiều).
- Phân rã inputs thành cây cân bằng sử dụng cổng liên kết (AND/OR/XOR…).

## Thuật toán rút gọn
```text
1) Tính logic level cho toàn bộ nodes
2) Chọn nodes đích (top-levels)
3) Tạo cây cân bằng inputs (thêm intermediate nodes khi cần)
```

## API (code)
- Class: `core.optimization.balance.BalanceOptimizer`
- Convenience: `apply_balance(netlist) -> netlist`

## Ghi chú
- Cải thiện depth; số node có thể tăng nhẹ do tạo intermediate nodes.
