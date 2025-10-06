# 🏗️ **MYLOGIC PROJECT STRUCTURE GUIDE**

## 📋 **CẤU TRÚC DỰ ÁN MỚI**

```
Mylogic/
├── 📁 core/                    # Core algorithms (pure logic)
│   ├── synthesis/              # Logic synthesis algorithms
│   │   ├── strash.py          # Structural hashing
│   │   └── synthesis_flow.py  # Main synthesis flow
│   ├── optimization/          # Logic optimization algorithms
│   │   ├── dce.py            # Dead Code Elimination
│   │   ├── cse.py            # Common Subexpression Elimination
│   │   ├── constprop.py      # Constant Propagation
│   │   └── balance.py        # Logic Balancing
│   ├── technology_mapping/   # Technology mapping algorithms
│   │   └── technology_mapping.py
│   └── vlsi_cad/             # VLSI CAD algorithms
│       ├── bdd.py           # Binary Decision Diagrams
│       ├── sat_solver.py    # SAT Solver
│       ├── placement.py     # Placement Algorithm
│       ├── routing.py       # Routing Algorithm
│       └── timing_analysis.py # Static Timing Analysis
├── 📁 integrations/          # External tool integrations
│   ├── yosys/               # Yosys synthesis integration
│   │   ├── mylogic_synthesis.py
│   │   ├── mylogic_engine.py
│   │   ├── mylogic_commands.py
│   │   ├── combinational_synthesis.py
│   │   └── mylogic_synthesis.ys
│   ├── iverilog/            # Icarus Verilog integration
│   └── gtkwave/             # GTKWave integration
├── 📁 backends/              # Output generators
│   ├── verilog_generator.py # Verilog output
│   ├── json_generator.py    # JSON output
│   └── dot_generator.py     # DOT graph output
├── 📁 frontends/             # Input parsers
│   ├── simple_arithmetic_verilog.py
│   └── verilog.py
├── 📁 cli/                   # Command line interface
│   └── vector_shell.py
├── 📁 examples/              # Example files
├── 📁 tests/                 # Test cases
├── 📁 docs/                  # Documentation
├── 📁 scripts/               # Utility scripts
└── 📁 outputs/               # Output files
```

## 🎯 **NGUYÊN TẮC TỔ CHỨC**

### **1. 📁 CORE (Pure Algorithms):**
- **Synthesis**: Logic synthesis algorithms
- **Optimization**: Logic optimization algorithms
- **Technology Mapping**: Technology mapping algorithms
- **VLSI CAD**: VLSI CAD algorithms

### **2. 📁 INTEGRATIONS (External Tools):**
- **Yosys**: Yosys synthesis integration
- **Icarus Verilog**: Simulation integration
- **GTKWave**: Waveform viewer integration

### **3. 📁 BACKENDS (Output Generators):**
- **Verilog**: Verilog output generation
- **JSON**: JSON output generation
- **DOT**: Graph output generation

### **4. 📁 FRONTENDS (Input Parsers):**
- **Verilog**: Verilog input parsing
- **Arithmetic**: Arithmetic expression parsing

## 🚀 **LỢI ÍCH CỦA CẤU TRÚC MỚI**

### **1. 🔧 Dễ Triển Khai:**
- Tách biệt rõ ràng giữa core algorithms và integrations
- Dễ dàng thêm/sửa/xóa modules
- Clear separation of concerns

### **2. 📦 Modular Design:**
- Mỗi module có trách nhiệm riêng biệt
- Dễ test và debug
- Reusable components

### **3. 🔄 Scalable:**
- Dễ dàng thêm integrations mới
- Dễ dàng thêm backends mới
- Dễ dàng thêm frontends mới

### **4. 📚 Maintainable:**
- Clear documentation cho từng module
- Easy to understand structure
- Easy to modify and extend

## 📊 **USAGE EXAMPLES**

### **1. Core Algorithms:**
```python
from core.synthesis.strash import apply_strash
from core.optimization.dce import apply_dce
from core.technology_mapping.technology_mapping import map_to_technology
```

### **2. Integrations:**
```python
from integrations.yosys.mylogic_synthesis import MyLogicSynthesis
from integrations.iverilog.simulator import IcarusSimulator
from integrations.gtkwave.viewer import GTKWaveViewer
```

### **3. Backends:**
```python
from backends.verilog_generator import VerilogGenerator
from backends.json_generator import JSONGenerator
from backends.dot_generator import DOTGenerator
```

### **4. Frontends:**
```python
from frontends.simple_arithmetic_verilog import parse_arithmetic_verilog_simple
from frontends.verilog import parse_verilog
```

## 🎯 **BEST PRACTICES**

### **1. Import Organization:**
- Core algorithms: `from core.module import function`
- Integrations: `from integrations.tool import class`
- Backends: `from backends.generator import class`
- Frontends: `from frontends.parser import function`

### **2. Module Structure:**
- Mỗi module có `__init__.py`
- Clear documentation
- Consistent naming

### **3. Testing:**
- Test cho từng module riêng biệt
- Integration tests
- End-to-end tests

## 📚 **REFERENCES**

- [Python Package Structure](https://docs.python.org/3/tutorial/modules.html)
- [EDA Tool Architecture](https://en.wikipedia.org/wiki/Electronic_design_automation)
- [MyLogic Documentation](./README.md)

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0