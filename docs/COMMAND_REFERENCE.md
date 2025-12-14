# MyLogic EDA Tool - Command Reference

## 📋 Bảng Thống Kê Tất Cả Các Lệnh

### Tổng Quan

MyLogic EDA Tool hỗ trợ **30+ commands** được chia thành 6 categories chính:

| Category | Số Lệnh | Mô Tả |
|----------|---------|-------|
| **File Operations** | 8 | Đọc file, xem thống kê, export |
| **Simulation** | 2 | Mô phỏng mạch (scalar/vector) |
| **Logic Synthesis** | 6 | Tối ưu hóa logic |
| **VLSI CAD Part 1** | 7 | BDD, BED, SAT, Verification, Quine-McCluskey, AIG |
| **VLSI CAD Part 2** | 4 | Placement, Routing, Timing, Technology Mapping |
| **Utility** | 4 | History, Clear, Help, Exit |
| **TOTAL** | **31** | |

---

## 📁 1. File Operations (8 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **read** | `read <file>` | Load file Verilog (.v) hoặc .logic. Tự động export JSON nếu được bật | `read examples/full_adder.v` |
| **stats** | `stats` | Hiển thị thống kê chi tiết về circuit (nodes, wires, vectors, modules) | `stats` |
| **vectors** | `vectors` | Hiển thị chi tiết vector widths (bit widths của tất cả signals) | `vectors` |
| **nodes** | `nodes` | Hiển thị chi tiết tất cả nodes trong netlist | `nodes` |
| **wires** | `wires` | Hiển thị phân tích wires (connections, types) | `wires` |
| **modules** | `modules` | Hiển thị chi tiết module instantiations | `modules` |
| **export** | `export [file]` | Export netlist ra file JSON (manual export) | `export netlist.json` |
| **export_json** | `export_json [file]` | Alias cho `export` | `export_json output.json` |

**Lưu ý:**
- `read` tự động export JSON vào `outputs/` nếu `auto_export_json` được bật
- `stats` hiển thị thống kê từ `current_netlist` (sau optimization)

---

## 🎮 2. Simulation (2 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **simulate** | `simulate` | Mô phỏng tự động phát hiện vector/scalar. Nhập input values khi được prompt | `simulate` |
| **vsimulate** | `vsimulate` | Mô phỏng vector (n-bit, legacy command) | `vsimulate` |

**Cách sử dụng:**
```bash
mylogic> read examples/full_adder.v
mylogic> simulate
  Value for [7:0] a (integer): 5
  Value for [7:0] b (integer): 3
  Value for cin (0/1): 0
  -> Outputs:
    sum: 8 (int: 8)
    cout: 0
```

---

## ⚙️ 3. Logic Synthesis (6 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **strash** | `strash` | Structural Hashing - Loại bỏ duplicate logic structures | `strash` |
| **dce** | `dce [level]` | Dead Code Elimination - Loại bỏ unused logic. Levels: `basic`, `advanced`, `aggressive` | `dce advanced` |
| **cse** | `cse` | Common Subexpression Elimination - Chia sẻ redundant computations | `cse` |
| **constprop** | `constprop` | Constant Propagation - Propagate constant values qua circuit | `constprop` |
| **balance** | `balance` | Logic Balancing - Cân bằng logic depth cho timing optimization | `balance` |
| **synthesis** | `synthesis [level]` | Complete synthesis flow (5 bước). Levels: `basic`, `standard`, `aggressive` | `synthesis standard` |

**Synthesis Flow:**
```
synthesis → Strash → DCE → CSE → ConstProp → Balance
```

**Ví dụ:**
```bash
mylogic> read examples/full_adder.v
mylogic> strash              # Step 1: Remove duplicates
mylogic> dce advanced        # Step 2: Remove unused logic
mylogic> cse                 # Step 3: Share common expressions
mylogic> constprop           # Step 4: Propagate constants
mylogic> balance             # Step 5: Balance logic depth
# Hoặc dùng:
mylogic> synthesis aggressive  # All 5 steps at once
```

---

## 🔬 4. VLSI CAD Part 1 (7 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **bdd** | `bdd <operation>` | Binary Decision Diagrams. Operations: `create`, `analyze`, `convert` | `bdd create` |
| **bed** | `bed <operation>` | Boolean Expression Diagrams. Operations: `create`, `up_one`, `up_all`, `compare` | `bed create` |
| **sat** | `sat <operation>` | SAT Solver. Operations: `solve`, `verify`, `check` | `sat solve` |
| **verify** | `verify <type>` | Circuit verification. Types: `equivalence`, `property`, `functional` | `verify equivalence` |
| **quine** | `quine <minterms> [dont_cares]` | Quine-McCluskey Boolean minimization | `quine 0,1,2,5,6,7` |
| **minimize** | `minimize <minterms> [dont_cares]` | Alias cho `quine` | `minimize 0,1,2,5` |
| **aig** | `aig <operation>` | And-Inverter Graph. Operations: `create`, `strash`, `convert` | `aig create` |

**Ví dụ:**
```bash
mylogic> read examples/full_adder.v
mylogic> bdd create          # Create BDD representation
mylogic> sat solve           # Solve SAT problem
mylogic> quine 0,1,2,5,6,7   # Minimize Boolean function
mylogic> aig create           # Create AIG representation
```

---

## 🏗️ 5. VLSI CAD Part 2 (4 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **place** | `place <algorithm>` | Cell placement algorithms. Algorithms: `random`, `force_directed`, `simulated_annealing` | `place force_directed` |
| **route** | `route <algorithm>` | Wire routing algorithms. Algorithms: `maze`, `lee`, `ripup_reroute` | `route maze` |
| **timing** | `timing` | Static Timing Analysis (STA) - Phân tích timing, critical paths, slacks | `timing` |
| **techmap** | `techmap <strategy> [library]` | Technology mapping. Strategy: `area`, `delay`, `balanced`. Library: `asic`, `fpga_common`, `ice40`, `xilinx`, `auto` | `techmap balanced fpga_common` |

**Technology Mapping Libraries:**
- `asic` - ASIC standard cells
- `fpga_common` - Common FPGA cells (DFF)
- `ice40` - Lattice iCE40 FPGA
- `xilinx` - Xilinx FPGA
- `lattice` - Lattice FPGA
- `intel` - Intel/Altera FPGA
- `gowin` - Gowin FPGA
- `anlogic` - Anlogic FPGA
- `auto` - Auto-detect library

**Ví dụ:**
```bash
mylogic> read examples/full_adder.v
mylogic> synthesis standard
mylogic> techmap balanced fpga_common  # Technology mapping
mylogic> place force_directed          # Placement
mylogic> route maze                    # Routing
mylogic> timing                        # Timing analysis
```

---

## 🛠️ 6. Utility Commands (4 lệnh)

| Lệnh | Cú Pháp | Mô Tả | Ví Dụ |
|------|---------|-------|-------|
| **history** | `history` | Hiển thị lịch sử 10 lệnh gần nhất | `history` |
| **clear** | `clear` | Xóa màn hình console | `clear` |
| **help** | `help` | Hiển thị help với tất cả commands | `help` |
| **exit** | `exit` | Thoát khỏi shell | `exit` |

---

## 📊 Bảng Tổng Hợp Đầy Đủ

| # | Lệnh | Category | Cú Pháp | Tham Số | Mô Tả Ngắn |
|---|------|----------|---------|---------|------------|
| 1 | `read` | File | `read <file>` | `<file>` - Path to .v file | Load Verilog file |
| 2 | `stats` | File | `stats` | None | Circuit statistics |
| 3 | `vectors` | File | `vectors` | None | Vector width details |
| 4 | `nodes` | File | `nodes` | None | Node details |
| 5 | `wires` | File | `wires` | None | Wire analysis |
| 6 | `modules` | File | `modules` | None | Module instantiations |
| 7 | `export` | File | `export [file]` | `[file]` - Optional output file | Export to JSON |
| 8 | `export_json` | File | `export_json [file]` | `[file]` - Optional output file | Alias for export |
| 9 | `simulate` | Simulation | `simulate` | None | Auto-detect simulation |
| 10 | `vsimulate` | Simulation | `vsimulate` | None | Vector simulation |
| 11 | `strash` | Synthesis | `strash` | None | Structural hashing |
| 12 | `dce` | Synthesis | `dce [level]` | `[level]` - basic/advanced/aggressive | Dead code elimination |
| 13 | `cse` | Synthesis | `cse` | None | Common subexpression elimination |
| 14 | `constprop` | Synthesis | `constprop` | None | Constant propagation |
| 15 | `balance` | Synthesis | `balance` | None | Logic balancing |
| 16 | `synthesis` | Synthesis | `synthesis [level]` | `[level]` - basic/standard/aggressive | Complete synthesis flow |
| 17 | `bdd` | VLSI CAD 1 | `bdd <operation>` | `<operation>` - create/analyze/convert | Binary Decision Diagrams |
| 18 | `bed` | VLSI CAD 1 | `bed <operation>` | `<operation>` - create/up_one/up_all/compare | Boolean Expression Diagrams |
| 19 | `sat` | VLSI CAD 1 | `sat <operation>` | `<operation>` - solve/verify/check | SAT Solver |
| 20 | `verify` | VLSI CAD 1 | `verify <type>` | `<type>` - equivalence/property/functional | Circuit verification |
| 21 | `quine` | VLSI CAD 1 | `quine <minterms> [dont_cares]` | `<minterms>` - comma-separated, `[dont_cares]` - optional | Quine-McCluskey |
| 22 | `minimize` | VLSI CAD 1 | `minimize <minterms> [dont_cares]` | `<minterms>` - comma-separated, `[dont_cares]` - optional | Alias for quine |
| 23 | `aig` | VLSI CAD 1 | `aig <operation>` | `<operation>` - create/strash/convert | And-Inverter Graph |
| 24 | `place` | VLSI CAD 2 | `place <algorithm>` | `<algorithm>` - random/force_directed/simulated_annealing | Cell placement |
| 25 | `route` | VLSI CAD 2 | `route <algorithm>` | `<algorithm>` - maze/lee/ripup_reroute | Wire routing |
| 26 | `timing` | VLSI CAD 2 | `timing` | None | Static timing analysis |
| 27 | `techmap` | VLSI CAD 2 | `techmap <strategy> [library]` | `<strategy>` - area/delay/balanced, `[library]` - optional | Technology mapping |
| 28 | `history` | Utility | `history` | None | Command history |
| 29 | `clear` | Utility | `clear` | None | Clear screen |
| 30 | `help` | Utility | `help` | None | Show help |
| 31 | `exit` | Utility | `exit` | None | Exit shell |

---

## 🎯 Workflow Examples

### Example 1: Basic Synthesis Flow

```bash
mylogic> read examples/full_adder.v
mylogic> stats
mylogic> synthesis standard
mylogic> stats
mylogic> techmap balanced standard
mylogic> stats
```

### Example 2: Complete VLSI CAD Flow

```bash
mylogic> read examples/full_adder.v
mylogic> synthesis aggressive
mylogic> techmap balanced fpga_common
mylogic> place force_directed
mylogic> route maze
mylogic> timing
```

### Example 3: Boolean Analysis

```bash
mylogic> read examples/full_adder.v
mylogic> bdd create
mylogic> bed create
mylogic> sat solve
mylogic> quine 0,1,2,5,6,7
mylogic> aig create
```

### Example 4: Simulation Workflow

```bash
mylogic> read examples/full_adder.v
mylogic> stats
mylogic> simulate
  Value for [7:0] a (integer): 5
  Value for [7:0] b (integer): 3
  Value for cin (0/1): 0
  -> Outputs:
    sum: 8 (int: 8)
    cout: 0
mylogic> export results.json
```

---

## 📝 Notes

### Command Requirements

- **File Operations**: Cần load file trước (`read`)
- **Synthesis Commands**: Cần load file và có netlist
- **VLSI CAD Commands**: Cần load file và có netlist
- **Simulation**: Cần load file và có netlist

### Auto-Export JSON

- `read` command tự động export JSON vào `outputs/` nếu `auto_export_json` được bật
- File name: `{module_name}_netlist.json`
- Manual export: `export <file>` hoặc `export_json <file>`

### Command Aliases

- `export` = `export_json`
- `minimize` = `quine`

### Error Handling

- Nếu command fail, error message sẽ hiển thị
- Type `help` để xem tất cả commands
- Check `history` để xem lệnh đã chạy

---

## 🔗 Related Documentation

- [Technology Mapping Flow](TECHNOLOGY_MAPPING_FLOW.md)
- [Synthesis Guide](SYNTHESIS_GUIDE.md)
- [Quick Start Guide](QUICKSTART.md)

