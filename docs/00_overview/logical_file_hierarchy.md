# 📊 HIERARCHY LOGIC - MYLOGIC EDA TOOL

## 🎯 Cấu trúc thứ bậc logic

```
┌─────────────────────────────────────────────────────────────────┐
│                    MYLOGIC EDA TOOL v2.0.0                     │
│              Unified Electronic Design Automation              │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1️⃣ ENTRY POINTS & CONFIGURATION                                │
├─────────────────────────────────────────────────────────────────┤
│ constants.py ──────► mylogic.py ──────► mylogic_config.json   │
│      │                     │                      │             │
│      ▼                     ▼                      ▼             │
│ setup.py ────────────► requirements.txt                         │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2️⃣ DOCUMENTATION LAYER                                         │
├─────────────────────────────────────────────────────────────────┤
│ README.md ──────► LICENSE ──────► docs/README.md               │
│      │                                 │                        │
│      ▼                                 ▼                        │
│ docs/00_overview/ ────► docs/algorithms/ ────► docs/vlsi_cad/  │
│      │                                 │                        │
│      ▼                                 ▼                        │
│ docs/simulation/ ─────► docs/report/                            │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3️⃣ CORE MODULES (Algorithms & Engines)                        │
├─────────────────────────────────────────────────────────────────┤
│ core/__init__.py                                                │
│    │                                                            │
│    ├─── simulation/                                             │
│    │    ├── arithmetic_simulation.py                           │
│    │    ├── logic_simulation.py                               │
│    │    └── timing_simulation.py                              │
│    │                                                            │
│    ├─── synthesis/                                              │
│    │    ├── strash.py                                         │
│    │    └── synthesis_flow.py                                 │
│    │                                                            │
│    ├─── optimization/                                           │
│    │    ├── dce.py                                            │
│    │    ├── cse.py                                            │
│    │    ├── constprop.py                                      │
│    │    └── balance.py                                        │
│    │                                                            │
│    ├─── technology_mapping/                                     │
│    │    └── technology_mapping.py                             │
│    │                                                            │
│    └─── vlsi_cad/                                              │
│         ├── bdd.py                                            │
│         ├── sat_solver.py                                     │
│         ├── placement.py                                      │
│         ├── routing.py                                        │
│         └── timing_analysis.py                               │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4️⃣ INPUT PROCESSING LAYER                                      │
├─────────────────────────────────────────────────────────────────┤
│ frontends/                                                      │
│    ├── verilog.py ────────► simple_arithmetic_verilog.py      │
│    └── (parsers convert input files to netlist)                │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5️⃣ USER INTERFACE LAYER                                        │
├─────────────────────────────────────────────────────────────────┤
│ cli/                                                            │
│    └── vector_shell.py                                         │
│         ├── Command processing                                  │
│         ├── User interaction                                   │
│         └── Integration with all modules                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6️⃣ EXTERNAL INTEGRATION LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│ integrations/                                                   │
│    ├── __init__.py                                             │
│    └── yosys/                                                  │
│         ├── __init__.py                                        │
│         ├── mylogic_synthesis.py                               │
│         ├── mylogic_commands.py                                │
│         └── combinational_synthesis.py                         │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7️⃣ TECHNOLOGY LIBRARIES LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│ techlibs/                                                       │
│    ├── library_loader.py                                       │
│    ├── standard_cells.lib                                      │
│    ├── lut_library.json                                        │
│    ├── custom_library.lib                                      │
│    └── custom_lut_library.json                                 │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8️⃣ TESTING & VALIDATION LAYER                                  │
├─────────────────────────────────────────────────────────────────┤
│ tests/                                                          │
│    ├── test_config.json                                        │
│    ├── test_data/                                              │
│    │   ├── simple_and.v                                        │
│    │   ├── complex_expression.v                                │
│    │   └── ... (test input files)                              │
│    ├── algorithms/                                              │
│    │   ├── test_strash.py                                      │
│    │   ├── test_dce.py                                         │
│    │   ├── test_cse.py                                         │
│    │   └── test_synthesis_flow.py                              │
│    └── run_all_tests.py                                        │
└─────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9️⃣ EXAMPLES & OUTPUTS LAYER                                    │
├─────────────────────────────────────────────────────────────────┤
│ examples/                    outputs/                          │
│    ├── full_adder.v              ├── *.v (generated)          │
│    ├── arithmetic_operations.v   ├── *.json (generated)       │
│    ├── bitwise_operations.v      ├── *.blif (generated)       │
│    └── ... (example designs)     └── ... (runtime outputs)    │
│                                                               │
│ scripts/                                                       │
│    ├── demo_flow.sh                                           │
│    └── run_tests.sh                                           │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow Logic

```
Input Files ──┐
              │
              ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │Frontends│───▶│  Core   │───▶│Integrations│
         │(Parsers)│    │Algorithms│    │(Yosys)  │
         └─────────┘    └─────────┘    └─────────┘
              │              │              │
              ▼              ▼              ▼
         ┌─────────┐    ┌─────────┐    ┌─────────┐
         │   CLI   │    │ TechLibs│    │ Outputs │
         │(Shell)  │    │(Libraries)│    │(Results)│
         └─────────┘    └─────────┘    └─────────┘
```

## 📊 Layer Dependencies

```
Layer 1: Constants & Configuration (Independent)
    │
    ▼
Layer 2: Documentation (Depends on Layer 1)
    │
    ▼
Layer 3: Core Modules (Depends on Layer 1)
    │
    ▼
Layer 4: Frontends (Depends on Layer 1, 3)
    │
    ▼
Layer 5: CLI Interface (Depends on Layers 1, 3, 4)
    │
    ▼
Layer 6: Integrations (Depends on Layers 1, 3, 5)
    │
    ▼
Layer 7: Tech Libraries (Depends on Layer 1)
    │
    ▼
Layer 8: Testing (Depends on All Layers)
    │
    ▼
Layer 9: Examples & Outputs (Runtime)
```

## 🎯 Key Design Principles

### **1. Separation of Concerns**
- Mỗi layer có trách nhiệm riêng biệt
- Clear boundaries giữa các layers

### **2. Dependency Inversion**
- Higher layers depend on lower layers
- No circular dependencies

### **3. Single Source of Truth**
- Constants centralized in Layer 1
- No duplicate configurations

### **4. Progressive Complexity**
- Từ simple (constants) đến complex (algorithms)
- Easy to understand và maintain

### **5. User-Centric Design**
- CLI layer provides unified interface
- Examples layer provides learning materials

---

**Kết luận**: Cấu trúc được thiết kế theo **hierarchy logic rõ ràng** với 9 layers, từ configuration đến outputs, đảm bảo tính modular, maintainable và scalable.
