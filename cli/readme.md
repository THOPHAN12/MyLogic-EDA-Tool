### CLI - Command Line Interface

Cung cấp shell tương tác để điều khiển toàn bộ workflow: đọc thiết kế, mô phỏng vector, tối ưu hóa logic, chạy flow tổng hợp với Yosys, và các tính năng VLSI CAD.

### 1) Thành phần chính
- `cli/vector_shell.py`: Shell tương tác (Vector-first CLI)
  - Ưu tiên mô phỏng vector (n-bit) bằng `core/simulation/arithmetic_simulation.py`.
  - Tự tích hợp lệnh Yosys khi môi trường có Yosys/ABC (qua `integrations/yosys`).
  - Lưu trữ trạng thái: `netlist`, `current_netlist`, `filename`, `history`, và cấu hình shell (prompt, history size, màu…).

### 2) Kiến trúc VectorShell (tóm tắt code)
- Trạng thái quan trọng:
  - `self.netlist`, `self.current_netlist`: netlist đang làm việc
  - `self.filename`: file hiện tại
  - `self.history`: lịch sử lệnh
  - `self.commands`: mapping tên lệnh → handler

- Khởi tạo cấu hình từ `mylogic_config.json`:
  - Prompt, history size, auto-complete, color output

- Vòng lặp `run()`:
  - Đọc input người dùng → tìm handler trong `self.commands` → thực thi → lưu history

### 3) Đăng ký lệnh (command registry)
Các lệnh được đăng ký trong `self.commands`:
- Cơ bản: `read`, `stats`, `simulate`, `vsimulate`, `history`, `clear`, `help`, `exit`
- Tối ưu hóa (ABC-inspired): `strash`, `dce`, `cse`, `constprop`, `balance`, `synthesis`, `abc_info`
- VLSI CAD: `bdd`, `sat`, `verify`, `place`, `route`, `timing`, `techmap`
- Yosys (nếu khả dụng): `yosys_*` + `write_*` (tự integrate qua `integrate_yosys_commands(self)`)

Ví dụ cách thêm 1 lệnh mới:
```python
def _hello(self, *args):
    """Print a friendly greeting."""
    # This is an example command handler
    print("Hello from MyLogic CLI!")

# Somewhere in __init__ after self.commands is created
self.commands["hello"] = self._hello
```

Nguyên tắc handler:
- Tên hàm dạng `_ten_lenh(self, *args)`
- Validate tham số, in lỗi thân thiện nếu sai cú pháp

### 4) Luồng xử lý chính
1. `read <file>` → parse Verilog (mặc định `frontends/simple_arithmetic_verilog.py`) → tạo `netlist`
2. `simulate`/`vsimulate` → hỏi giá trị input → mô phỏng bằng `core/simulation/arithmetic_simulation.py`
3. Tối ưu hóa logic: `strash` → `dce` → `cse` → `constprop` → `balance`
4. (Tùy chọn) Tổng hợp với Yosys: `yosys_flow`, `yosys_opt`, `yosys_stat`, …

### 5) Tích hợp Yosys
- Khi import shell, thử `from integrations.yosys.mylogic_synthesis import ...`
- Nếu thành công: gọi `integrate_yosys_commands(self)` để thêm nhóm lệnh `yosys_*` và `write_*`.
- Mặc định xuất file vào `outputs/`.

Ví dụ lệnh Yosys:
```text
yosys_flow examples/arithmetic_operations.v balanced
yosys_stat examples/arithmetic_operations.v
write_verilog out.v
write_json out.json
```

### 6) Cách dùng nhanh (Quick Start)
- Khởi chạy shell:
  - `python mylogic.py`
- Nạp và mô phỏng:
  - `read examples/arithmetic_operations.v`
  - `simulate`
- Chạy Yosys flow (cần Yosys/ABC):
  - `yosys_flow examples/arithmetic_operations.v balanced`
  - `yosys_stat examples/arithmetic_operations.v`

### 7) Mở rộng CLI (ví dụ nâng cao)
Thêm lệnh tính tổng 2 số integer do người dùng nhập:
```python
def _sum2(self, *args):
    """Read two integers and print their sum."""
    # Example of simple argument parsing
    if len(args) != 2:
        print("Usage: sum2 <a> <b>")
        return
    try:
        a = int(args[0]); b = int(args[1])
        print(f"sum = {a + b}")
    except ValueError:
        print("Invalid integers. Usage: sum2 <a> <b>")

self.commands["sum2"] = self._sum2
```

### 8) Debug & xử lý lỗi
- Dùng `python mylogic.py --debug` để bật logging chi tiết
- Nếu `yosys_*` không hiện: kiểm tra Yosys/ABC đã cài và trong PATH
- Nếu parser lỗi: thử `frontends/verilog.py` với RTL logic cơ bản
- Nếu `outputs/` trống: đảm bảo đã gọi `write_*` hoặc lệnh Yosys tương ứng

### 9) Ghi chú & giới hạn
- Parser mặc định `simple_arithmetic_verilog.py` ưu tiên số học vector; với RTL logic phức tạp dùng `frontends/verilog.py`
- Nên thống nhất format `netlist` trong pipeline để tránh lỗi edge-case
- Phát hiện vector trong `mylogic.py` là heuristic đơn giản; có thể mở rộng khi cần

### 10) Liên kết tham khảo
- Parser: `frontends/`
- Mô phỏng: `core/simulation/`
- Tối ưu hóa: `core/optimization/`, `core/synthesis/`
- Yosys: `integrations/yosys/`
- Ví dụ: `examples/`

