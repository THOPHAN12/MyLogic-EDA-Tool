# MyLogic EDA Tool - Quick Command Reference

## 📊 Bảng Thống Kê Tất Cả Lệnh

### Tổng Quan

| Category | Số Lệnh | Commands |
|----------|---------|----------|
| **File Operations** | 8 | read, stats, vectors, nodes, wires, modules, export, export_json |
| **Simulation** | 2 | simulate, vsimulate |
| **Logic Synthesis** | 6 | strash, dce, cse, constprop, balance, synthesis |
| **VLSI CAD Part 1** | 7 | bdd, bed, sat, verify, quine, minimize, aig |
| **VLSI CAD Part 2** | 4 | place, route, timing, techmap |
| **Utility** | 4 | history, clear, help, exit |
| **TOTAL** | **31** | |

---

## 📁 File Operations

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `read` | `read <file>` | Load Verilog file (auto-export JSON) | `read examples/full_adder.v` |
| `stats` | `stats` | Circuit statistics | `stats` |
| `vectors` | `vectors` | Vector width details | `vectors` |
| `nodes` | `nodes` | Node details | `nodes` |
| `wires` | `wires` | Wire analysis | `wires` |
| `modules` | `modules` | Module instantiations | `modules` |
| `export` | `export [file]` | Export to JSON | `export netlist.json` |
| `export_json` | `export_json [file]` | Alias for export | `export_json output.json` |

---

## 🎮 Simulation

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `simulate` | `simulate` | Auto-detect simulation | `simulate` |
| `vsimulate` | `vsimulate` | Vector simulation | `vsimulate` |

---

## ⚙️ Logic Synthesis

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `strash` | `strash` | Structural hashing | `strash` |
| `dce` | `dce [level]` | Dead code elimination | `dce advanced` |
| `cse` | `cse` | Common subexpression elimination | `cse` |
| `constprop` | `constprop` | Constant propagation | `constprop` |
| `balance` | `balance` | Logic balancing | `balance` |
| `synthesis` | `synthesis [level]` | Complete synthesis flow | `synthesis standard` |

**Levels:**
- `dce`: `basic`, `advanced`, `aggressive`
- `synthesis`: `basic`, `standard`, `aggressive`

---

## 🔬 VLSI CAD Part 1

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `bdd` | `bdd <operation>` | Binary Decision Diagrams | `bdd create` |
| `bed` | `bed <operation>` | Boolean Expression Diagrams | `bed create` |
| `sat` | `sat <operation>` | SAT Solver | `sat solve` |
| `verify` | `verify <type>` | Circuit verification | `verify equivalence` |
| `quine` | `quine <minterms> [dont_cares]` | Quine-McCluskey | `quine 0,1,2,5,6,7` |
| `minimize` | `minimize <minterms> [dont_cares]` | Alias for quine | `minimize 0,1,2,5` |
| `aig` | `aig <operation>` | And-Inverter Graph | `aig create` |

**Operations:**
- `bdd`: `create`, `analyze`, `convert`
- `bed`: `create`, `up_one`, `up_all`, `compare`
- `sat`: `solve`, `verify`, `check`
- `verify`: `equivalence`, `property`, `functional`
- `aig`: `create`, `strash`, `convert`

---

## 🏗️ VLSI CAD Part 2

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `place` | `place <algorithm>` | Cell placement | `place force_directed` |
| `route` | `route <algorithm>` | Wire routing | `route maze` |
| `timing` | `timing` | Static timing analysis | `timing` |
| `techmap` | `techmap <strategy> [library]` | Technology mapping | `techmap balanced fpga_common` |

**Algorithms:**
- `place`: `random`, `force_directed`, `simulated_annealing`
- `route`: `maze`, `lee`, `ripup_reroute`

**Strategies:**
- `techmap`: `area`, `delay`, `balanced`

**Libraries:**
- `asic`, `fpga_common`, `ice40`, `xilinx`, `lattice`, `intel`, `gowin`, `anlogic`, `auto`

---

## 🛠️ Utility

| Lệnh | Syntax | Mô Tả | Example |
|------|--------|-------|---------|
| `history` | `history` | Command history | `history` |
| `clear` | `clear` | Clear screen | `clear` |
| `help` | `help` | Show help | `help` |
| `exit` | `exit` | Exit shell | `exit` |

---

## 🎯 Quick Workflows

### Basic Flow
```bash
read <file> → stats → synthesis standard → techmap balanced → stats
```

### Complete Flow
```bash
read <file> → synthesis aggressive → techmap balanced fpga_common → place force_directed → route maze → timing
```

### Boolean Analysis
```bash
read <file> → bdd create → bed create → sat solve → quine 0,1,2,5,6,7 → aig create
```

---

## 📝 Notes

- Tất cả commands cần load file trước (`read`)
- `read` tự động export JSON nếu `auto_export_json` được bật
- `export` và `export_json` là aliases
- `minimize` là alias cho `quine`
- Type `help` để xem tất cả commands

