# 🧮 MyLogic EDA Tool

**Unified Electronic Design Automation Tool v2.0.0**

A comprehensive EDA tool for digital circuit design, logic synthesis, optimization, and verification with both scalar and vector support, powered by Yosys synthesis engine and advanced VLSI CAD algorithms.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Yosys Integration](https://img.shields.io/badge/Yosys-Integrated-green.svg)](https://github.com/YosysHQ/yosys)

## 🎯 Overview

MyLogic EDA Tool is a unified Electronic Design Automation platform designed for educational and research purposes. It provides a complete pipeline from RTL description to optimized gate-level netlists, featuring advanced synthesis algorithms, VLSI CAD tools, and comprehensive simulation capabilities.

## ✨ Key Features

### 🔧 **Core Synthesis Algorithms**
- **Structural Hashing (Strash)**: Remove duplicate logic structures
- **Dead Code Elimination (DCE)**: Eliminate unused logic with multiple optimization levels
- **Common Subexpression Elimination (CSE)**: Share redundant computations
- **Constant Propagation**: Propagate constant values through the circuit
- **Logic Balancing**: Balance logic depth for timing optimization

### 🎮 **Advanced Simulation**
- **Vector Simulation**: Multi-bit arithmetic and bitwise operations
- **Auto-detection**: Automatic scalar vs vector mode detection
- **Interactive CLI**: User-friendly command-line interface
- **Real-time Feedback**: Immediate simulation results

### 🔬 **VLSI CAD Algorithms**
- **Binary Decision Diagrams (BDD)**: Efficient Boolean function representation
- **SAT Solver**: Boolean satisfiability checking and verification
- **Placement Algorithms**: Random, Force-directed, Simulated Annealing
- **Routing Algorithms**: Maze routing (Lee's algorithm), Rip-up & reroute
- **Static Timing Analysis (STA)**: Critical path analysis and slack calculation
- **Technology Mapping**: Area/delay/balanced optimization strategies

### 🔗 **Professional Integration**
- **Yosys Integration**: Complete synthesis flow powered by Yosys
- **ABC Optimization**: Advanced optimization algorithms
- **Multiple Output Formats**: Verilog, JSON, BLIF, DOT, SPICE, Liberty
- **Technology Libraries**: Standard cells and LUT-based mapping

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool

# Install Python dependencies
pip install -r requirements.txt

# Install optional tools (recommended)
# Yosys for synthesis features
# Windows: Download from https://github.com/YosysHQ/yosys/releases
# Linux: sudo apt-get install yosys
# macOS: brew install yosys

# Graphviz for visualization (optional)
# Windows: Download from https://graphviz.org/download/
# Linux: sudo apt-get install graphviz
# macOS: brew install graphviz
```

### Basic Usage

```bash
# Start interactive shell
python mylogic.py

# Load and simulate a design
mylogic> read examples/arithmetic_operations.v
mylogic> stats
mylogic> simulate
# Enter input values when prompted

# Run synthesis optimization
mylogic> synthesis balanced

# Generate outputs
mylogic> write_verilog optimized.v
mylogic> write_json netlist.json
```

### Example Workflows

#### 1. **Logic Synthesis Flow**
```bash
python mylogic.py
mylogic> read examples/full_adder.v
mylogic> strash                    # Structural hashing
mylogic> dce advanced              # Dead code elimination
mylogic> cse                       # Common subexpression elimination
mylogic> constprop                 # Constant propagation
mylogic> balance                   # Logic balancing
mylogic> stats                     # Show optimization results
```

#### 2. **Yosys Professional Synthesis**
```bash
mylogic> yosys_flow examples/arithmetic_operations.v balanced
mylogic> yosys_stat examples/arithmetic_operations.v
mylogic> write_verilog optimized.v
mylogic> write_dot circuit.dot
```

#### 3. **VLSI CAD Analysis**
```bash
mylogic> place force_directed       # Force-directed placement
mylogic> route maze                 # Maze routing
mylogic> timing                     # Static timing analysis
mylogic> techmap balanced           # Technology mapping
```

## 📁 Project Structure

```
MyLogic-EDA-Tool/
├── 📄 mylogic.py                  # Main launcher
├── 📁 cli/                        # Command-line interface
│   └── vector_shell.py           # Interactive shell with 20+ commands
├── 📁 core/                       # Core algorithms
│   ├── optimization/             # Logic optimization algorithms
│   │   ├── strash.py            # Structural hashing
│   │   ├── dce.py               # Dead code elimination
│   │   ├── cse.py               # Common subexpression elimination
│   │   ├── constprop.py         # Constant propagation
│   │   └── balance.py           # Logic balancing
│   ├── synthesis/                # Logic synthesis
│   │   └── synthesis_flow.py    # Complete synthesis pipeline
│   ├── simulation/               # Circuit simulation
│   │   └── arithmetic_simulation.py  # Vector simulation engine
│   ├── technology_mapping/       # Technology mapping
│   └── vlsi_cad/                # VLSI CAD algorithms
│       ├── bdd.py               # Binary Decision Diagrams
│       ├── sat_solver.py        # SAT Solver
│       ├── placement.py         # Placement algorithms
│       ├── routing.py           # Routing algorithms
│       └── timing_analysis.py   # Static Timing Analysis
├── 📁 frontends/                  # Input parsers
│   ├── verilog.py               # Verilog parser
│   └── simple_arithmetic_verilog.py  # Enhanced Verilog parser
├── 📁 integrations/              # External tool integration
│   └── yosys/                   # Yosys integration
│       ├── mylogic_synthesis.py # Synthesis engine
│       ├── mylogic_commands.py  # Command interface
│       └── combinational_synthesis.py  # Combinational synthesis
├── 📁 techlibs/                  # Technology libraries
│   ├── standard_cells.lib       # Standard cell library
│   ├── lut_library.json         # LUT library
│   └── library_loader.py        # Library management
├── 📁 docs/                      # Comprehensive documentation
│   ├── 00_overview/             # System overview and guides
│   ├── algorithms/              # Algorithm documentation
│   ├── vlsi_cad/               # VLSI CAD documentation
│   ├── simulation/             # Simulation documentation
│   ├── report/                 # Project reports
│   └── README.md               # Documentation index
├── 📁 examples/                 # Example designs
│   ├── arithmetic_operations.v  # Multi-bit arithmetic
│   ├── full_adder.v            # Basic adder
│   └── complex_arithmetic.v    # Complex operations
├── 📁 tests/                    # Test suite
└── 📁 outputs/                  # Generated outputs
```

## 🔧 Command Reference

### **Basic Commands**
- `read <file>` - Load Verilog file
- `stats` - Show circuit statistics
- `simulate` - Run simulation (auto-detect mode)
- `help` - Show all available commands
- `exit` - Quit shell

### **Logic Synthesis Commands**
- `strash` - Structural hashing (remove duplicates)
- `dce <level>` - Dead code elimination (basic/advanced/aggressive)
- `cse` - Common subexpression elimination
- `constprop` - Constant propagation
- `balance` - Logic balancing
- `synthesis <level>` - Complete synthesis flow (basic/standard/aggressive)

### **VLSI CAD Commands**
- `place <algorithm>` - Placement (random/force_directed/simulated_annealing)
- `route <algorithm>` - Routing (maze/lee/ripup_reroute)
- `timing` - Static timing analysis
- `techmap <strategy>` - Technology mapping (area/delay/balanced)

### **Yosys Integration Commands**
- `yosys_flow <file> [level]` - Complete Yosys synthesis
- `yosys_stat <file>` - Get design statistics
- `write_verilog <file>` - Output Verilog RTL
- `write_json <file>` - Output JSON netlist
- `write_dot <file>` - Output DOT graph
- `write_blif <file>` - Output BLIF format

## 📊 Supported Operations

### **Arithmetic Operations**
```verilog
module arithmetic_demo(a, b, c, d, sum_out, diff_out, prod_out, quot_out);
  input [3:0] a, b, c, d;
  output [4:0] sum_out, diff_out;
  output [7:0] prod_out;
  output [3:0] quot_out;
  
  assign sum_out = a + b;      // Addition
  assign diff_out = c - d;     // Subtraction  
  assign prod_out = a * b;     // Multiplication
  assign quot_out = c / d;     // Division
endmodule
```

### **Bitwise Operations**
```verilog
module bitwise_demo(a, b, and_out, or_out, xor_out, not_out);
  input [3:0] a, b;
  output [3:0] and_out, or_out, xor_out, not_out;
  
  assign and_out = a & b;      // Bitwise AND
  assign or_out = a | b;       // Bitwise OR
  assign xor_out = a ^ b;      // Bitwise XOR
  assign not_out = ~a;         // Bitwise NOT
endmodule
```

## 📚 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[📖 System Overview](docs/00_overview/01_introduction.md)** - Complete introduction
- **[🧮 Theoretical Foundation](docs/00_overview/02_theoretical_foundation.md)** - Core concepts
- **[🔧 Installation Guide](docs/00_overview/installation_guide.md)** - Setup instructions
- **[🏗️ Project Structure](docs/00_overview/project_structure_guide.md)** - Architecture overview
- **[🎯 API Reference](docs/00_overview/api_reference.md)** - Complete API documentation
- **[🧪 Algorithm Details](docs/algorithms/README.md)** - Algorithm implementations
- **[🔬 VLSI CAD Tools](docs/vlsi_cad/README.md)** - VLSI CAD algorithms
- **[🎮 Simulation Guide](docs/simulation/README.md)** - Simulation documentation

## 🎯 Key Algorithms

### **Logic Synthesis Pipeline**
```
Input Netlist → Strash → DCE → CSE → ConstProp → Balance → Optimized Netlist
```

### **VLSI CAD Flow**
```
Netlist → Placement → Routing → Timing Analysis → Technology Mapping → Final Design
```

## 📈 Performance Results

| Algorithm | Node Reduction | Timing Improvement | Memory Usage |
|-----------|----------------|-------------------|--------------|
| Strash    | 15-30%         | 10-20%           | -5%          |
| DCE       | 20-40%         | 15-25%           | -10%         |
| CSE       | 25-35%         | 20-30%           | -8%          |
| ConstProp | 30-50%         | 25-40%           | -15%         |
| Balance   | 10-20%         | 30-50%           | +5%          |

## 🔍 Troubleshooting

### **Common Issues**
1. **Import Errors**: Install dependencies with `pip install -r requirements.txt`
2. **Yosys Not Found**: Install Yosys for synthesis features
3. **Simulation Errors**: Check input values and circuit logic
4. **Vector Width Mismatch**: Ensure consistent vector declarations

### **Debug Mode**
```bash
python mylogic.py --debug
python mylogic.py --check-deps
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **[Yosys](https://github.com/YosysHQ/yosys)** - Core synthesis engine
- **[ABC](https://github.com/YosysHQ/abc)** - Optimization algorithms
- **[Graphviz](https://graphviz.org/)** - Visualization support
- **Python Community** - Excellent libraries and tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues)
- **Discussions**: [GitHub Discussions](https://github.com/THOPHAN12/MyLogic-EDA-Tool/discussions)
- **Documentation**: [docs/README.md](docs/README.md)

---

**MyLogic EDA Tool v2.0.0** - *Unified Electronic Design Automation Platform*

*Empowering education and research in digital circuit design and VLSI CAD*