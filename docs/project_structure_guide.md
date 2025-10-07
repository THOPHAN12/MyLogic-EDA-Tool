# 🏗️ **MYLOGIC PROJECT STRUCTURE GUIDE**

## 📋 **TỔNG QUAN DỰ ÁN**

**MyLogic EDA Tool** là một công cụ Tự động Hóa Thiết kế Điện tử (Electronic Design Automation) toàn diện, được thiết kế để hỗ trợ:
- Thiết kế mạch số (Digital Circuit Design)
- Tổng hợp luận lý (Logic Synthesis)
- Tối ưu hóa mạch (Circuit Optimization)
- Mô phỏng mạch (Circuit Simulation)
- Ánh cạ công nghệ (Technology Mapping)

---

## 🏗️ **CẤU TRÚC THƯ MỤC CHÍNH**

### **📁 ROOT DIRECTORY** (`/D:/DO_AN_2/Mylogic/`)

#### **🎯 Mục đích:**
- Chứa các file cấu hình chính và entry points
- Quản lý dependencies và logging
- Cung cấp unified launcher

#### **📄 Files chính:**
- `mylogic.py` (8.7KB, 250 lines) - **Main launcher** (unified entry point)
- `setup.py` (2.0KB, 67 lines) - **Package setup** cho pip install
- `requirements.txt` (343B, 18 lines) - **Dependencies** list
- `LICENSE` (1.1KB, 22 lines) - **MIT License**
- `README.md` (12KB, 334 lines) - **Project documentation**
- `mylogic_config.json` (684B, 37 lines) - **Configuration** settings
- `mylogic.log` (1.0B, 1 lines) - **Log file**
- `.gitignore` (1.1KB, 97 lines) - **Git ignore** rules
- `.git/` - **Git repository**

---

## 📁 **CORE FOLDER** (`/core/`)

### 🎯 **Mục đích:**
Chứa **core algorithms** - các thuật toán cốt lõi của hệ thống.

### 📄 **Files chính:**

#### **🔧 Logic Synthesis Algorithms:**
- `strash.py` - **Structural Hashing** (loại bỏ duplicates)
- `cse.py` - **Common Subexpression Elimination** (loại bỏ CSE)
- `constprop.py` - **Constant Propagation** (propagate constants)
- `balance.py` - **Logic Balancing** (cân bằng logic depth)
- `synthesis_flow.py` - **Complete Synthesis Flow** (tích hợp tất cả)

#### **🧠 VLSI CAD Part 1:**
- `dce.py` - **Dead Code Elimination** (loại bỏ dead code)
- `bdd.py` - **Binary Decision Diagrams** (biểu diễn Boolean functions)
- `sat_solver.py` - **SAT Solver** (kiểm tra satisfiability)

#### **🏗️ VLSI CAD Part 2:**
- `placement.py` - **Placement Algorithms** (Random, Force-directed, SA)
- `routing.py` - **Routing Algorithms** (Lee's, Maze, Rip-up)
- `timing_analysis.py` - **Static Timing Analysis** (ATs, RATs, Slack)
- `technology_mapping.py` - **Technology Mapping** (Area/Delay/Balanced)

#### **🎯 Simulation Engine:**
- `arithmetic_simulation.py` - **Vector Simulation Engine** (multi-bit simulation)

### 🔧 **Chức năng chính:**

#### **1. Logic Synthesis Workflow:**
```
Input Netlist
    ↓
1. Structural Hashing (Strash)     ← Loại bỏ duplicates
    ↓
2. Dead Code Elimination (DCE)     ← Loại bỏ dead code
    ↓
3. Common Subexpression Elimination ← Loại bỏ CSE
    ↓
4. Constant Propagation            ← Propagate constants
    ↓
5. Logic Balancing                 ← Cân bằng logic depth
    ↓
Optimized Netlist
```

#### **2. Vector Simulation:**
- **VectorValue Class**: Đại diện multi-bit values
- **Arithmetic Operations**: +, -, *, /
- **Bitwise Operations**: &, |, ^, ~
- **Expression Evaluation**: Complex expressions với operator precedence

#### **3. VLSI CAD Algorithms:**
- **BDD**: Reduced Ordered Binary Decision Diagrams
- **SAT**: DPLL algorithm cho satisfiability
- **Placement**: Force-directed, Simulated Annealing
- **Routing**: Lee's algorithm, Maze routing
- **STA**: Graph-based timing analysis

---

## 📁 **CLI FOLDER** (`/cli/`)

### 🎯 **Mục đích:**
Cung cấp **Command Line Interface** - giao diện dòng lệnh tương tác cho người dùng.

### 📄 **Files:**
- `vector_shell.py` - **Enhanced CLI shell** (867 lines)
- `__pycache__/` - Python cache files

### 🔧 **Chức năng chính:**

#### **1. Interactive Shell Management:**
```python
class VectorShell:
    """Enhanced shell với hỗ trợ vector simulation."""
```
- **Main Loop**: Nhận và xử lý commands từ user
- **Command Parsing**: Phân tích và thực thi 20+ commands
- **Error Handling**: Xử lý lỗi và hiển thị thông báo
- **History Management**: Lưu trữ lịch sử commands

#### **2. Command Categories:**

**🔧 Basic Commands:**
- `read <file>` - Load Verilog file
- `simulate` - Run simulation (auto-detect vector/scalar)
- `stats` - Show circuit statistics
- `help` - Show all commands
- `exit` - Quit shell

**⚡ Logic Synthesis Algorithms:**
- `strash` - Structural Hashing (remove duplicates)
- `cse` - Common Subexpression Elimination
- `constprop` - Constant Propagation
- `balance` - Logic Balancing
- `synthesis <level>` - Complete synthesis flow

**🧠 VLSI CAD Part 1 Features:**
- `dce <level>` - Dead Code Elimination
- `bdd <operation>` - Binary Decision Diagrams
- `sat <operation>` - SAT Solver
- `verify <type>` - Circuit verification

**🏗️ VLSI CAD Part 2 Features:**
- `place <algorithm>` - Placement algorithms
- `route <algorithm>` - Routing algorithms
- `timing` - Static Timing Analysis
- `techmap <strategy>` - Technology mapping

**🔗 Yosys Integration:**
- `yosys_flow` - Complete Yosys synthesis
- `write_verilog` - Output Verilog
- `write_json` - Output JSON
- `write_dot` - Output DOT graph

#### **3. State Management:**
```python
self.netlist = None              # Current loaded netlist
self.current_netlist = None      # Working copy
self.filename = None             # Current file
self.history = []                # Command history
```

#### **4. Unified Simulation:**
- **Auto-detection**: Tự động phát hiện vector vs scalar design
- **Input Handling**: Xử lý user input values
- **Output Display**: Hiển thị kết quả simulation

---

## 📁 **FRONTENDS FOLDER** (`/frontends/`)

### 🎯 **Mục đích:**
Chứa **parser modules** - các module phân tích và chuyển đổi input files.

### 📄 **Files:**
- `verilog.py` - **Verilog Parser** (basic Verilog parsing)
- `simple_arithmetic_verilog.py` - **Enhanced Verilog Parser** (hỗ trợ arithmetic operations)

### 🔧 **Chức năng chính:**

#### **1. Verilog Parsing:**
- **RTL Parsing**: Đọc và parse Verilog RTL code
- **Module Detection**: Nhận diện modules, ports, signals
- **Vector Support**: Hỗ trợ vector declarations `[N:0] signal`
- **Arithmetic Operations**: +, -, *, /, %, **
- **Bitwise Operations**: &, |, ^, ~, <<, >>

#### **2. Netlist Generation:**
- **Internal Representation**: Chuyển đổi Verilog thành internal netlist
- **Node Creation**: Tạo nodes cho gates và operations
- **Connection Mapping**: Mapping connections giữa nodes
- **Vector Width Tracking**: Theo dõi vector widths

---

## 📁 **INTEGRATIONS FOLDER** (`/integrations/`)

### 🎯 **Mục đích:**
Chứa **external tool integrations** - tích hợp với các công cụ bên ngoài.

### 📄 **Files:**
- **Yosys integration** - Professional synthesis tools
- **Icarus Verilog** - Simulation integration
- **GTKWave** - Waveform visualization

### 🔧 **Chức năng chính:**

#### **1. Yosys Integration:**
- **Command Interface**: Giao diện với Yosys commands
- **Synthesis Flow**: Complete synthesis workflow
- **Output Formats**: Multiple output formats (Verilog, JSON, BLIF, etc.)
- **Technology Mapping**: LUT-based và Liberty-based mapping

#### **2. Simulation Integration:**
- **Icarus Verilog**: Verilog simulation
- **GTKWave**: Waveform viewing và analysis

---

## 📁 **BACKENDS FOLDER** (`/backends/`)

### 🎯 **Mục đích:**
Chứa **output generators** - các module tạo output files.

### 📄 **Files:**
- **Verilog Generator** - Verilog RTL output
- **JSON Generator** - JSON netlist output
- **DOT Generator** - Graph visualization output

### 🔧 **Chức năng chính:**

#### **1. Output Generation:**
- **Multiple Formats**: Verilog, JSON, BLIF, DOT, SPICE, Liberty
- **Format Conversion**: Chuyển đổi giữa các formats
- **Graph Visualization**: DOT format cho graph viewing

---

## 📁 **SUPPORTING FOLDERS**

### **📚 DOCS FOLDER** (`/docs/`)
- **Mục đích**: Documentation và guides
- **Files**: `project_structure_guide.md`, `complete_workflow.md`
- **Chức năng**: User manual, technical documentation

### **🎯 EXAMPLES FOLDER** (`/examples/`)
- **Mục đích**: Demo files và test cases
- **Files**: Verilog examples, arithmetic operations, complex circuits
- **Chức năng**: Test cases, demo examples, benchmark circuits

### **⚡ BENCHMARKS FOLDER** (`/benchmarks/`)
- **Mục đích**: Performance benchmarks
- **Files**: Large circuit test cases, optimization results
- **Chức năng**: Performance testing, optimization analysis

### **🔧 SCRIPTS FOLDER** (`/scripts/`)
- **Mục đích**: Utility scripts
- **Files**: Automation tools, setup scripts
- **Chức năng**: Automation, setup, maintenance

### **📤 OUTPUTS FOLDER** (`/outputs/`)
- **Mục đích**: Generated output files
- **Files**: Synthesis results, optimization reports
- **Chức năng**: Output storage, result analysis

---

## 🔄 **WORKFLOW TỔNG QUAN**

### **📋 Complete EDA Workflow:**

```
1. INPUT
   ├── Verilog file (.v)
   └── Parser (frontends/)

2. LOGIC SYNTHESIS
   ├── Structural Hashing (strash)
   ├── Dead Code Elimination (dce)
   ├── Common Subexpression Elimination (cse)
   ├── Constant Propagation (constprop)
   └── Logic Balancing (balance)

3. LOGIC OPTIMIZATION
   ├── BDD Analysis
   ├── SAT Solving
   └── Circuit Verification

4. TECHNOLOGY MAPPING
   ├── Placement Algorithms
   ├── Routing Algorithms
   ├── Static Timing Analysis
   └── Technology Mapping

5. OUTPUT
   ├── Optimized Verilog
   ├── JSON Netlist
   ├── DOT Graph
   └── Multiple formats
```

---

## 🎯 **KIẾN TRÚC TỔNG QUAN**

### **📊 Layered Architecture:**

```
┌─────────────────────────────────────┐
│           CLI Layer                 │  ← User Interface
├─────────────────────────────────────┤
│         Core Algorithms             │  ← Logic Synthesis & VLSI CAD
├─────────────────────────────────────┤
│         Frontend Parsers            │  ← Verilog Parsing
├─────────────────────────────────────┤
│         Integrations                │  ← External Tools
├─────────────────────────────────────┤
│         Backends                    │  ← Output Generation
└─────────────────────────────────────┘
```

### **🔄 Data Flow:**

```
Verilog File → Parser → Netlist → Algorithms → Optimized Netlist → Output
     ↑                                                              ↓
   Input                                                         Multiple Formats
```

---

## 💡 **BEST PRACTICES**

### **📁 Folder Organization:**
- **Separation of Concerns**: Mỗi folder có mục đích riêng biệt
- **Modular Design**: Các module độc lập, dễ maintain
- **Clear Naming**: Tên folder và file rõ ràng, dễ hiểu

### **🔧 Code Organization:**
- **Vietnamese Comments**: Tất cả comments bằng tiếng Việt
- **English Technical Terms**: Thuật ngữ kỹ thuật giữ nguyên tiếng Anh
- **Consistent Style**: Coding style nhất quán
- **Error Handling**: Xử lý lỗi đầy đủ

### **📚 Documentation:**
- **Comprehensive**: Tài liệu đầy đủ cho mọi component
- **User-Friendly**: Dễ đọc, dễ hiểu
- **Technical Depth**: Chi tiết kỹ thuật cho developers

---

## 📊 **USAGE EXAMPLES**

### **1. Core Algorithms:**
```python
from core.strash import apply_strash
from core.dce import apply_dce
from core.synthesis_flow import run_complete_synthesis
```

### **2. CLI Usage:**
```bash
python mylogic.py                    # Start interactive shell
python mylogic.py --file design.v   # Load file and start
```

### **3. Frontend Parsing:**
```python
from frontends.simple_arithmetic_verilog import parse_arithmetic_verilog_simple
netlist = parse_arithmetic_verilog_simple("design.v")
```

### **4. Simulation:**
```python
from core.arithmetic_simulation import simulate_arithmetic_netlist
result = simulate_arithmetic_netlist(netlist, input_values)
```

---

## 🎉 **KẾT LUẬN**

**MyLogic EDA Tool** được thiết kế với kiến trúc modular, rõ ràng:

- **📁 Core**: Thuật toán cốt lõi mạnh mẽ
- **📁 CLI**: Giao diện người dùng thân thiện
- **📁 Frontends**: Parser linh hoạt
- **📁 Integrations**: Tích hợp external tools
- **📁 Backends**: Output generation đa dạng
- **📁 Supporting**: Documentation, examples, tests

**🎯 Mục tiêu**: Cung cấp công cụ EDA hoàn chỉnh cho học tập, nghiên cứu và phát triển VLSI tại Việt Nam.

---

**📅 Ngày tạo**: 2025-10-05  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
