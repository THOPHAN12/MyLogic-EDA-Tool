# MyLogic - Hướng Dẫn Nhanh (Quick Start)

## 📋 Mục Lục
1. [Giới Thiệu](#giới-thiệu)
2. [Cài Đặt](#cài-đặt)
3. [Cách Chạy Cơ Bản](#cách-chạy-cơ-bản)
4. [Các Tính Năng Chính](#các-tính-năng-chính)
5. [Ví Dụ Thực Tế](#ví-dụ-thực-tế)

---

## 🎯 Giới Thiệu

**MyLogic** là công cụ EDA (Electronic Design Automation) toàn diện cho:
- Parse Verilog HDL
- Tối ưu hóa mạch logic (Synthesis)
- Mô phỏng (Simulation)
- Technology Mapping
- Phân tích timing, placement, routing

---

## 💾 Cài Đặt

### 1. Kiểm Tra Python

```bash
python --version
# Yêu cầu: Python 3.7+
```

### 2. Cài Đặt Dependencies

```bash
cd D:\DO_AN_2\Mylogic
pip install -r requirements.txt
```

### 3. Kiểm Tra Cài Đặt

```bash
python mylogic.py --version
python mylogic.py --check-deps
```

**Output mong đợi:**
```
Checking dependencies...
[OK] NumPy is available
[OK] Matplotlib is available
[WARNING] Graphviz not available - DOT output disabled
```

---

## 🚀 Cách Chạy Cơ Bản

### 📌 Method 1: Chạy Nhanh với File Verilog

```bash
# Parse và xem thống kê
python mylogic.py --file examples/full_adder.v
```

Trong shell, gõ:
```
mylogic> stats
mylogic> exit
```

### 📌 Method 2: Synthesis Tự Động (Khuyến Nghị)

```bash
# Chạy toàn bộ optimization flow
python mylogic.py -f examples/full_adder.v -s standard
```

**Output:**
```
[1/3] Parsing Verilog...
  Loaded 9 nodes

[2/3] Running complete synthesis flow (standard)...
>>> Starting Structural Hashing optimization...
[... optimization logs ...]

[3/3] Exporting results...
  Exported to: outputs\full_adder_synthesized_standard.json

SUMMARY
Original nodes: 9
Optimized nodes: 2
Reduction: 7 nodes (77.8%)
[SUCCESS] Synthesis completed!
```

### 📌 Method 3: Shell Tương Tác (Development Mode)

```bash
python mylogic.py
```

**Trong shell:**
```
mylogic> read examples/full_adder.v
mylogic> stats
mylogic> synthesis standard
mylogic> stats
mylogic> export_json output.json
mylogic> exit
```

---

## 🛠️ Các Tính Năng Chính

### 1. **Parse Verilog**

```bash
# CLI mode
python mylogic.py -f examples/full_adder.v

# Shell mode
mylogic> read examples/full_adder.v
mylogic> stats
```

### 2. **Complete Synthesis Flow** (5 bước)

```bash
# Tự động
python mylogic.py -f examples/full_adder.v -s standard

# Shell
mylogic> read examples/full_adder.v
mylogic> synthesis standard
```

**5 bước optimization:**
1. **Strash** - Loại bỏ nodes trùng lặp
2. **DCE** - Dead Code Elimination
3. **CSE** - Common Subexpression Elimination
4. **ConstProp** - Constant Propagation
5. **Balance** - Logic Balancing

### 3. **Chạy Từng Optimization Riêng**

```bash
# Trong shell
mylogic> read examples/full_adder.v
mylogic> strash          # Structural Hashing
mylogic> stats
mylogic> dce             # Dead Code Elimination
mylogic> stats
mylogic> cse             # Common Subexpression Elimination
mylogic> stats
mylogic> constprop       # Constant Propagation
mylogic> stats
mylogic> balance         # Logic Balancing
mylogic> stats
```

### 4. **Simulation**

```bash
# Shell mode
mylogic> read examples/full_adder.v
mylogic> vsimulate       # Vector simulation
# Nhập test vectors khi được hỏi
```

### 5. **Export Results**

```bash
# CLI mode - tự động export
python mylogic.py -f examples/full_adder.v -s standard
# Kết quả: outputs/full_adder_synthesized_standard.json

# Shell mode - manual export
mylogic> read examples/full_adder.v
mylogic> synthesis standard
mylogic> export_json my_output.json
```

---

## 💡 Ví Dụ Thực Tế

### Ví Dụ 1: Full Adder (Cơ Bản)

```bash
# Chạy synthesis với level standard
python mylogic.py -f examples/full_adder.v -s standard
```

**Kết quả:**
- Input: 9 nodes
- Output: 2 nodes (giảm 77.8%)

### Ví Dụ 2: Comprehensive Combinational (Phức Tạp)

```bash
# Chạy synthesis với level aggressive
python mylogic.py -f examples/comprehensive_combinational.v -s aggressive
```

**Kết quả:**
- Input: 56 nodes
- Output: 2 nodes (giảm 96.4%)

### Ví Dụ 3: Development Workflow

```bash
# Bước 1: Khởi động shell
python mylogic.py

# Bước 2: Load file
mylogic> read examples/full_adder.v

# Bước 3: Xem thông tin ban đầu
mylogic> stats

# Bước 4: Chạy từng optimization
mylogic> strash
mylogic> stats
mylogic> dce
mylogic> stats

# Bước 5: Export kết quả
mylogic> export_json full_adder_optimized.json

# Bước 6: Thoát
mylogic> exit
```

### Ví Dụ 4: Batch Processing

**Windows PowerShell:**
```powershell
Get-ChildItem examples\*.v | ForEach-Object {
    Write-Host "Processing: $($_.Name)"
    python mylogic.py -f $_.FullName -s standard
}
```

**Linux/Mac:**
```bash
for file in examples/*.v; do
    echo "Processing: $file"
    python mylogic.py -f "$file" -s standard
done
```

### Ví Dụ 5: Debug Mode

```bash
# Xem log chi tiết
python mylogic.py -f examples/full_adder.v -s standard --debug
```

---

## 📊 Optimization Levels

Chọn level phù hợp với nhu cầu:

| Level | Tốc độ | Tối ưu | Phù hợp cho |
|-------|--------|--------|-------------|
| `basic` | ⚡⚡⚡ | ⭐ | Circuits nhỏ, test nhanh |
| `standard` | ⚡⚡ | ⭐⭐ | Hầu hết cases (khuyến nghị) |
| `aggressive` | ⚡ | ⭐⭐⭐ | Circuits lớn, cần tối ưu tối đa |

**Ví dụ:**
```bash
python mylogic.py -f examples/full_adder.v -s basic       # Nhanh
python mylogic.py -f examples/full_adder.v -s standard    # Khuyến nghị
python mylogic.py -f examples/full_adder.v -s aggressive  # Tối đa
```

---

## 📂 Cấu Trúc Thư Mục

```
Mylogic/
├── mylogic.py              # Entry point chính
├── examples/               # File Verilog mẫu
│   ├── full_adder.v
│   ├── priority_encoder.v
│   └── comprehensive_combinational.v
├── outputs/                # Kết quả synthesis (tự động tạo)
├── core/                   # Core algorithms
│   ├── optimization/       # DCE, CSE, ConstProp, Balance
│   ├── synthesis/          # Strash, Synthesis Flow
│   ├── simulation/         # Arithmetic Simulation
│   └── vlsi_cad/          # BDD, SAT, Placement, Routing
├── frontends/              # Verilog parser
└── docs/                   # Tài liệu chi tiết
```

---

## 🎓 Tất Cả Lệnh Shell

Sau khi chạy `python mylogic.py`, các lệnh có sẵn:

### File Operations
```
read <file>              - Load Verilog file
export_json <file>       - Export netlist to JSON
```

### Analysis
```
stats                    - Hiển thị thống kê mạch
vectors                  - Xem thông tin vectors
nodes                    - Xem chi tiết nodes
wires                    - Xem chi tiết wires
```

### Simulation
```
simulate                 - Scalar simulation (1-bit)
vsimulate                - Vector simulation (n-bit)
```

### Optimization (Từng bước)
```
strash                   - Structural Hashing
dce                      - Dead Code Elimination
cse                      - Common Subexpression Elimination
constprop                - Constant Propagation
balance                  - Logic Balancing
```

### Synthesis (Toàn bộ)
```
synthesis <level>        - Complete synthesis flow
                          Levels: basic, standard, aggressive
```

### VLSI CAD
```
bdd                      - Binary Decision Diagram
sat                      - SAT Solver
verify                   - Equivalence Checking
place                    - Placement
route                    - Routing
timing                   - Timing Analysis
techmap                  - Technology Mapping
```

### Utility
```
help                     - Hiển thị tất cả lệnh
history                  - Xem lịch sử lệnh
clear                    - Xóa màn hình
exit                     - Thoát shell
```

---

## 🆘 Troubleshooting

### 1. Lỗi: "No module named 'parsers'"

**Giải pháp:**
```bash
# Đảm bảo chạy từ thư mục gốc
cd D:\DO_AN_2\Mylogic
python mylogic.py
```

### 2. Lỗi: "File not found"

**Giải pháp:**
```bash
# Kiểm tra file tồn tại
dir examples\full_adder.v  # Windows
ls examples/full_adder.v   # Linux/Mac

# Dùng đường dẫn đầy đủ
python mylogic.py -f D:\DO_AN_2\Mylogic\examples\full_adder.v -s standard
```

### 3. Lỗi: "No netlist loaded"

**Giải pháp:**
```
# Trong shell, phải load file trước
mylogic> read examples/full_adder.v
mylogic> synthesis standard
```

### 4. Output file không tìm thấy

**Giải pháp:**
```bash
# File được lưu trong outputs/
cd outputs
dir  # Windows
ls   # Linux/Mac
```

---

## 📚 Tài Liệu Thêm

- **SYNTHESIS_GUIDE.md** - Hướng dẫn chi tiết về synthesis flow
- **README.md** - Tổng quan về project
- **docs/** - Tài liệu đầy đủ về algorithms và architecture

---

## 🎯 Workflow Khuyến Nghị

### Cho Người Mới Bắt Đầu:

```bash
# 1. Test với file đơn giản
python mylogic.py -f examples/full_adder.v -s standard

# 2. Kiểm tra output
type outputs\full_adder_synthesized_standard.json

# 3. Thử shell mode
python mylogic.py
mylogic> read examples/full_adder.v
mylogic> stats
mylogic> help
mylogic> exit
```

### Cho Development:

```bash
# 1. Khởi động shell với file
python mylogic.py -f examples/comprehensive_combinational.v

# 2. Chạy từng bước và kiểm tra
mylogic> stats
mylogic> strash
mylogic> stats
mylogic> dce
mylogic> stats

# 3. Export kết quả
mylogic> export_json dev_output.json
```

### Cho Production/Automation:

```bash
# Batch processing với script
for file in examples/*.v; do
    python mylogic.py -f "$file" -s aggressive
done
```

---

## ✅ Checklist Bắt Đầu

- [ ] Cài đặt Python 3.7+
- [ ] Cài đặt dependencies: `pip install -r requirements.txt`
- [ ] Kiểm tra version: `python mylogic.py --version`
- [ ] Chạy test đầu tiên: `python mylogic.py -f examples/full_adder.v -s standard`
- [ ] Xem output file: `type outputs\full_adder_synthesized_standard.json`
- [ ] Thử shell mode: `python mylogic.py` → `help` → `exit`
- [ ] Đọc SYNTHESIS_GUIDE.md để hiểu rõ hơn

---

**Chúc bạn sử dụng MyLogic thành công! 🎉**

Nếu gặp vấn đề, tạo issue trên GitHub hoặc kiểm tra docs/ folder.

