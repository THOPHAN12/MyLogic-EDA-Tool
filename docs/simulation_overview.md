# Simulation Overview

## VectorValue & Quy tắc width/mask
- VectorValue(value, width) luôn mask: `value & ((1 << width) - 1)`.
- Quy tắc width kết quả:
  - add/sub: max(widths) + 1, mul: sum(widths), div: giữ width(a), bitwise: max(widths), not: giữ width(a).

## API chính (arithmetic_simulation.py)
- vector_add/subtract/multiply/divide
- vector_and/or/xor/not
- simulate_arithmetic_netlist(netlist, inputs) -> Dict[str, VectorValue]

## Luồng mô phỏng
1) Chuẩn hóa inputs → VectorValue
2) Thực thi nodes theo thứ tự hợp lệ
3) Trả về map output → VectorValue

## Edge cases
- Division by zero → raise ValueError
- Overflow/underflow → luôn mask theo width
- Độ rộng không đồng nhất → theo quy tắc width ở trên
