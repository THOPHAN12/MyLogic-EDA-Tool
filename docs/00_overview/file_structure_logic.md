# 📁 CẤU TRÚC FILE LOGIC - MYLOGIC EDA TOOL

## 🎯 Tổng quan thứ tự logic

Dự án MyLogic EDA Tool được tổ chức theo **thứ tự logic từ cơ bản đến nâng cao**, từ entry point đến các modules chuyên sâu.

## 📋 Thứ tự logic các file

### 🚀 **1. ENTRY POINTS & CONFIGURATION (Điểm vào & Cấu hình)**

```
1. constants.py              # 📊 Constants tập trung - ĐỌC ĐẦU TIÊN
2. mylogic.py               # 🎮 Main launcher - Entry point chính
3. mylogic_config.json      # ⚙️ Configuration settings
4. setup.py                 # 📦 Package setup & distribution
5. requirements.txt         # 📋 Dependencies list
```

**Lý do thứ tự:**
- `constants.py` chứa tất cả metadata cần thiết cho các file khác
- `mylogic.py` là entry point chính, import từ constants
- `mylogic_config.json` cung cấp cấu hình runtime
- `setup.py` và `requirements.txt` cho packaging

---

### 📚 **2. DOCUMENTATION (Tài liệu)**

```
6. README.md                # 📖 Main documentation
7. LICENSE                  # 📄 License information
8. docs/README.md           # 📚 Documentation index
9. docs/00_overview/        # 🎯 System overview
10. docs/algorithms/        # 🧮 Algorithm documentation
11. docs/vlsi_cad/         # 🔬 VLSI CAD documentation
12. docs/simulation/       # 🎮 Simulation documentation
13. docs/report/           # 📝 Project reports
```

**Lý do thứ tự:**
- README.md là tài liệu đầu tiên người dùng đọc
- docs/ được tổ chức theo độ phức tạp tăng dần
- Từ overview → algorithms → vlsi_cad → simulation → reports

---

### 🏗️ **3. CORE MODULES (Modules cốt lõi)**

#### **3.1 Core Base**
```
14. core/__init__.py        # 🔧 Core module initialization
15. core/simulation/__init__.py  # 🎮 Simulation module init
```

#### **3.2 Simulation Engine**
```
16. core/simulation/arithmetic_simulation.py  # 🧮 Vector simulation engine
17. core/simulation/logic_simulation.py      # ⚡ Logic gate simulation
18. core/simulation/timing_simulation.py     # ⏱️ Timing simulation
```

#### **3.3 Logic Synthesis**
```
19. core/synthesis/strash.py           # 🔍 Structural Hashing
20. core/synthesis/synthesis_flow.py   # 🔄 Complete synthesis pipeline
```

#### **3.4 Optimization Algorithms**
```
21. core/optimization/dce.py           # 🗑️ Dead Code Elimination
22. core/optimization/cse.py           # 🔄 Common Subexpression Elimination
23. core/optimization/constprop.py     # 📊 Constant Propagation
24. core/optimization/balance.py       # ⚖️ Logic Balancing
```

#### **3.5 Technology Mapping**
```
25. core/technology_mapping/technology_mapping.py  # 🎯 Technology mapping
```

#### **3.6 VLSI CAD Algorithms**
```
26. core/vlsi_cad/bdd.py              # 🌳 Binary Decision Diagrams
27. core/vlsi_cad/sat_solver.py       # ✅ SAT Solver
28. core/vlsi_cad/placement.py        # 📍 Placement algorithms
29. core/vlsi_cad/routing.py          # 🛣️ Routing algorithms
30. core/vlsi_cad/timing_analysis.py  # ⏱️ Static Timing Analysis
```

**Lý do thứ tự:**
- Core modules theo thứ tự phức tạp tăng dần
- Từ simulation → synthesis → optimization → technology mapping → vlsi_cad
- Mỗi module có __init__.py riêng để import

---

### 🔧 **4. FRONTENDS (Input Parsers)**

```
31. frontends/verilog.py                    # 📝 Basic Verilog parser
32. frontends/simple_arithmetic_verilog.py  # 🧮 Enhanced Verilog parser
```

**Lý do thứ tự:**
- Basic parser trước, enhanced parser sau
- Parsers đọc input files và chuyển đổi thành netlist

---

### 🎮 **5. CLI INTERFACE (Giao diện dòng lệnh)**

```
33. cli/vector_shell.py  # 🖥️ Interactive command-line interface
```

**Lý do thứ tự:**
- CLI sử dụng tất cả core modules và frontends
- Cung cấp interface cho người dùng

---

### 🔗 **6. INTEGRATIONS (Tích hợp external tools)**

```
34. integrations/__init__.py                    # 🔧 Integration module init
35. integrations/yosys/__init__.py              # 🎯 Yosys integration init
36. integrations/yosys/mylogic_synthesis.py     # 🔄 Yosys synthesis engine
37. integrations/yosys/mylogic_commands.py      # 📋 Yosys commands
38. integrations/yosys/combinational_synthesis.py  # 🧮 Combinational synthesis
```

**Lý do thứ tự:**
- Integration modules sử dụng core modules
- Yosys integration là external tool chính

---

### 📚 **7. TECHNOLOGY LIBRARIES (Thư viện công nghệ)**

```
39. techlibs/library_loader.py     # 📚 Library management
40. techlibs/standard_cells.lib    # 🏭 Standard cell library
41. techlibs/lut_library.json      # 🔢 LUT library
42. techlibs/custom_library.lib    # ⚙️ Custom library
43. techlibs/custom_lut_library.json  # 🔢 Custom LUT library
```

**Lý do thứ tự:**
- Library loader quản lý tất cả libraries
- Standard libraries trước, custom libraries sau

---

### 🧪 **8. TESTING (Kiểm thử)**

#### **8.1 Test Configuration**
```
44. tests/test_config.json    # ⚙️ Test configuration
45. tests/README.md           # 📖 Test documentation
```

#### **8.2 Test Data**
```
46. tests/test_data/          # 📊 Test input files
   ├── simple_and.v
   ├── complex_expression.v
   ├── duplicate_nodes.v
   ├── dead_code.v
   ├── common_subexpressions.v
   └── constants.v
```

#### **8.3 Test Implementations**
```
47. tests/algorithms/test_strash.py           # 🔍 Strash tests
48. tests/algorithms/test_dce.py              # 🗑️ DCE tests
49. tests/algorithms/test_cse.py              # 🔄 CSE tests
50. tests/algorithms/test_synthesis_flow.py   # 🔄 Synthesis flow tests
51. tests/examples/test_example.py            # 📝 Example tests
52. tests/test_arithmetic_simulation.py       # 🧮 Simulation tests
53. tests/test_verilog_parser.py              # 📝 Parser tests
```

#### **8.4 Test Runner**
```
54. tests/run_all_tests.py    # 🏃 Main test runner
```

**Lý do thứ tự:**
- Configuration trước
- Test data (input files) trước
- Test implementations theo thứ tự algorithms
- Test runner cuối cùng

---

### 📁 **9. EXAMPLES & OUTPUTS (Ví dụ & Kết quả)**

#### **9.1 Example Files**
```
55. examples/                 # 📝 Example designs
   ├── full_adder.v
   ├── arithmetic_operations.v
   ├── bitwise_operations.v
   ├── complex_arithmetic.v
   ├── simple_multiplier.v
   └── sequential_counter.v
```

#### **9.2 Output Directory**
```
56. outputs/                  # 📤 Generated outputs (empty, created at runtime)
```

#### **9.3 Scripts**
```
57. scripts/                  # 🔧 Utility scripts
   ├── demo_flow.sh
   └── run_tests.sh
```

**Lý do thứ tự:**
- Examples cung cấp input cho testing và demonstration
- Outputs chứa kết quả runtime
- Scripts cho automation

---

## 🔄 **Workflow Logic**

### **Development Workflow:**
```
1. constants.py → 2. mylogic.py → 3. core/ → 4. frontends/ → 5. cli/ → 6. integrations/
```

### **User Workflow:**
```
1. README.md → 2. examples/ → 3. mylogic.py → 4. cli/ → 5. outputs/
```

### **Testing Workflow:**
```
1. tests/test_config.json → 2. tests/test_data/ → 3. tests/algorithms/ → 4. tests/run_all_tests.py
```

---

## 📊 **File Categories Summary**

| Category | Count | Purpose |
|----------|-------|---------|
| **Entry Points** | 5 | Configuration & main entry |
| **Documentation** | 8+ | User guides & API docs |
| **Core Modules** | 16+ | Core algorithms & engines |
| **Frontends** | 2 | Input parsers |
| **CLI Interface** | 1 | User interface |
| **Integrations** | 5+ | External tool integration |
| **Tech Libraries** | 5+ | Technology libraries |
| **Testing** | 10+ | Test suite |
| **Examples** | 6+ | Example designs |
| **Scripts** | 2+ | Utility scripts |

---

## 🎯 **Key Principles**

### **1. Dependency Order**
- Files được sắp xếp theo thứ tự dependency
- Constants → Core → Frontends → CLI → Integrations

### **2. Complexity Order**
- Từ đơn giản đến phức tạp
- Basic → Enhanced → Advanced

### **3. User Journey**
- Entry points trước
- Documentation dễ tiếp cận
- Examples để học tập

### **4. Development Order**
- Core algorithms trước
- Integration sau
- Testing cuối cùng

---

**Kết luận**: Cấu trúc file được tổ chức theo **thứ tự logic rõ ràng**, từ entry points đến core modules, từ basic đến advanced, đảm bảo dễ hiểu, dễ maintain và dễ mở rộng.
