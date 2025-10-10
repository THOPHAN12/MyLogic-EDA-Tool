### CLI - Command Line Interface

Cung cấp shell tương tác để điều khiển toàn bộ workflow: đọc thiết kế, mô phỏng vector, tối ưu hóa logic, chạy flow tổng hợp với Yosys, và các tính năng VLSI CAD.

### File chính
- `vector_shell.py`: Shell tương tác.
  - Ưu tiên mô phỏng vector (n-bit) bằng `core/simulation/arithmetic_simulation.py`.
  - Tự tích hợp lệnh Yosys nếu môi trường có Yosys/ABC.
  - Lưu trữ `netlist`/`current_netlist`, `history`, cấu hình shell.

### Lệnh hỗ trợ
- **Cơ bản**:
  - `read <file>`: nạp Verilog; parser mặc định là `frontends/simple_arithmetic_verilog.py`.
  - `stats`: thống kê mạch (IO, nodes, vector widths).
  - `simulate`: tự nhận diện, mô phỏng vector/scalar (ưu tiên vector).
  - `vsimulate`: mô phỏng vector (legacy, alias qua simulate).
  - `history`, `clear`, `help`, `exit`.
- **Tối ưu hóa nội bộ (ABC-inspired)**:
  - `strash`, `dce <level>`, `cse`, `constprop`, `balance`, `synthesis <level>`.
- **VLSI CAD**:
  - `bdd <op>`, `sat <op>`, `verify <type>`, `place <algo>`, `route <algo>`, `timing`, `techmap <strategy>`.
- **Yosys (nếu khả dụng)**:
  - `yosys_synth`, `yosys_opt`, `yosys_stat`, `yosys_flow`, `yosys_help`.
  - Xuất định dạng: `write_verilog`, `write_json`, `write_blif`, `write_edif`, `write_spice`, `write_dot`, `write_liberty`, `write_systemverilog`.

### Cách dùng nhanh
- Khởi chạy shell:
  - `python mylogic.py`
- Nạp và mô phỏng:
  - `read examples/arithmetic_operations.v`
  - `simulate`
- Chạy Yosys flow (cần Yosys/ABC):
  - `yosys_flow examples/arithmetic_operations.v balanced`
  - `yosys_stat examples/arithmetic_operations.v`

### Tích hợp Yosys
- Kiểm tra tự động khi mở shell; nếu không có Yosys/ABC, các lệnh `yosys_*` bị vô hiệu.
- Kết quả tổng hợp và tệp đầu ra nằm trong thư mục `outputs/`.

### Ghi chú và giới hạn
- Parser mặc định cho `.v` là `simple_arithmetic_verilog.py` (dựa trên regex, chưa hỗ trợ precedence/ngoặc phức tạp). Với biểu thức logic phức tạp, cân nhắc dùng `frontends/verilog.py`.
- Cần thống nhất format netlist: khuyến nghị `nodes` là danh sách các node (list of dicts) xuyên suốt pipeline.
- Phát hiện vector trong `mylogic.py` hiện đơn giản; với các khai báo `[msb:lsb]` không điển hình có thể cần nâng cấp regex.

### Liên kết
- Parser: `frontends/`
- Mô phỏng: `core/simulation/`
- Tối ưu hóa: `core/optimization/`, `core/synthesis/`
- Yosys: `integrations/yosys/`
- Ví dụ: `examples/`


