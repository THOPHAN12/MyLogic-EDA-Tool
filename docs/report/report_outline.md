# MyLogic EDA Tool — Report Outline (Detailed)

## 1) Tóm tắt điều hành
- MyLogic EDA Tool là công cụ EDA hợp nhất cho thiết kế mạch số, tối ưu logic, tổng hợp, ánh xạ công nghệ và CAD (BDD, SAT, Placement, Routing, STA).
- Pipeline tối ưu: Strash → DCE → CSE → ConstProp → Balance; tích hợp Yosys/ABC; mô phỏng vector n-bit; tài liệu đầy đủ.
- Kết quả minh hoạ: giảm node đáng kể; STA xác định đường critical và slack để định hướng tối ưu timing.

## 2) Bối cảnh & mục tiêu
- Bối cảnh: EDA học thuật phân mảnh, khó minh họa đầu-cuối và đánh giá định lượng.
- Mục tiêu: dựng pipeline "từ RTL đến công nghệ"; thực thi thuật toán tiêu biểu; tích hợp Yosys/ABC; cung cấp CLI + docs dễ dạy/học.

## 3) Phạm vi & đối tượng
- Phạm vi: Verilog cơ bản/số học; mô phỏng vector; tối ưu logic; technology mapping; CAD (BDD/SAT/Placement/Routing/STA); outputs qua Yosys.
- Ngoài phạm vi: FSM nâng cao, sign-off công nghiệp, P&R thương mại.
- Đối tượng: SV/GV/NCS VLSI/EDA; kỹ sư cần demo nhanh.

## 4) Kiến trúc hệ thống
- CLI: `cli/vector_shell.py` (command registry; `read/simulate/strash/.../yosys_*`).
- Frontends: `frontends/` (parser Verilog cơ bản & arith).
- Core: simulation, optimization & synthesis, technology mapping, vlsi_cad.
- Integrations: `integrations/yosys/` (Yosys engine & commands).
- Techlibs: `techlibs/` (standard cells/LUT); config: `mylogic_config.json`.

## 5) Thuật toán & thiết kế
- Strash: hash chữ ký (gate_type, sorted_inputs) → hợp nhất node trùng.
- DCE: reachability từ outputs + cleanup wires; ODC/SDC (đơn giản).
- CSE: chuẩn hóa biểu thức → shared node + cập nhật connections.
- ConstProp: multi-pass; rewrite CONST0/CONST1 khi có thể.
- Balance: levelization + cân bằng cây (AND/OR/XOR…).
- Technology Mapping: library (area, delay); area/delay/balanced (cost mặc định = area + 10·delay).
- BDD: ROBDD-inspired; unique table; apply ops; evaluate; xuất Verilog đơn giản.
- SAT: DPLL core (unit propagation, decision, backtrack); verification (miter/property-to-CNF đơn giản).
- Placement: random, force-directed, simulated annealing; metric HPWL.
- Routing: maze/Lee (đơn giản), rip-up & reroute; lưới nhiều lớp.
- STA: AT/RAT/Slack; critical paths; báo cáo slack & vi phạm.

## 6) Quy trình xử lý (workflow)
1) Parse Verilog → Netlist
2) Strash → DCE → CSE → ConstProp → Balance
3) Technology Mapping (area/delay/balanced)
4) Verification/CAD: BDD/SAT, Placement/Routing, STA
5) Xuất: Verilog/JSON/BLIF/DOT/EDIF/SPICE/Liberty/SystemVerilog

## 7) Triển khai & tích hợp
- Python 3.8+; NumPy; Graphviz (DOT); Yosys + ABC.
- Yosys: `mylogic_synthesis.py` + `mylogic_commands.py`; lệnh `yosys_*`, `write_*`.
- Techlibs: `create_standard_library()`; Liberty/LUT JSON.
- CLI: nhóm cơ bản, tối ưu, CAD, Yosys; dễ mở rộng qua handler.

## 8) Kế hoạch thử nghiệm
- Unit: Strash/DCE/CSE/flow/simulation/parser; CAD demo (placement/routing/STA).
- Chỉ số: node/level, HPWL, routing success, worst/avg slack, runtime.
- Môi trường: OS/Python/Yosys/ABC.
- Phương pháp: A/B "trước/sau" từng pass; across examples/test_data.

## 9) Kết quả & đánh giá (mẫu)
- Ví dụ: Nodes −35%; Levels −25%; HPWL −14.7%; Routing ~92%; Worst Slack +0.35 ns.
- Nhận xét: Strash+CSE giảm node; Balance giảm depth; ConstProp dọn logic hằng; DCE loại dead code.

## 10) Giới hạn & rủi ro
- Parser đơn giản; CAD heuristic; mapping chưa timing-driven; STA chưa sign-off; phụ thuộc Yosys/ABC.

## 11) Roadmap & đề xuất
- Ngắn hạn: type hints; test > 80%; CI/CD; tối ưu hotspot.
- Dài hạn: GUI; parser SV/VHDL; ISCAS/ITC; mapping timing-driven; STA đa góc; Icarus/GTKWave; paper.

## 12) Kết luận
MyLogic EDA Tool đạt mục tiêu "hợp nhất – minh bạch – có thể dạy/học".

---

### Phụ lục A — Quick Start
- Cài đặt: Python 3.8+; `pip install -r requirements.txt`; Yosys/ABC; Graphviz (tùy chọn).
- Chạy: `python mylogic.py` → `read examples/arithmetic_operations.v` → `simulate` → `yosys_flow ... balanced` → `write_verilog out.v`.

### Phụ lục B — Lệnh CLI chính
- Cơ bản: `read`, `stats`, `simulate`, `help`, `exit`
- Optimization: `strash`, `dce <level>`, `cse`, `constprop`, `balance`, `synthesis <level>`
- Yosys: `yosys_synth`, `yosys_opt`, `yosys_stat`, `yosys_flow`, `write_*`
- CAD: `place <algo>`, `route <algo>`, `timing`, `techmap <strategy>`

### Phụ lục C — Cấu hình & môi trường
- `mylogic_config.json`: prompt/history/paths/default passes.
- `techlibs/`: standard cells/LUT.
- Yosys/ABC: PATH (`yosys -V` / `abc -h`).
