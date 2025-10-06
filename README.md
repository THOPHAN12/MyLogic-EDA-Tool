# MyLogic EDA Tool

**Unified Electronic Design Automation Tool v1.0.0**

A comprehensive EDA tool for digital circuit design, optimization, and verification with both scalar and vector support, powered by Yosys synthesis engine.

## 🚀 Features

### **Core Features**
- **Multiple Frontend Parsers**: Verilog, Simple Language, Arithmetic Verilog
- **Scalar & Vector Simulation**: 1-bit and n-bit support with auto-detection
- **Arithmetic Operations**: +, -, *, / with full vector support
- **Bitwise Operations**: &, |, ^, ~
- **Interactive CLI**: User-friendly shell interface with comprehensive commands
- **Smart Detection**: Auto-detect scalar vs vector files

### **Yosys Integration**
- **Yosys-Powered Synthesis**: Complete synthesis flow based on Yosys engine
- **Yosys Optimization Passes**: Expression, Clean, MuxTree, Reduce, Merge (from Yosys)
- **ABC Optimization**: Fast, Balanced, Thorough, Area, Delay optimization (Yosys ABC)
- **Technology Mapping**: Liberty-based, LUT-based mapping (Yosys techmap)

### **VLSI CAD Part 1 Features**
- **Dead Code Elimination (DCE)**: Basic, Advanced, Aggressive optimization levels
- **Binary Decision Diagrams (BDD)**: Efficient Boolean function representation
- **SAT Solver**: Boolean satisfiability checking and circuit verification
- **Circuit Verification**: Equivalence checking, property verification

### **VLSI CAD Part 2 Features** 🆕
- **ASIC Placement**: Random, Force-directed, Simulated Annealing algorithms
- **ASIC Routing**: Maze routing (Lee's algorithm), Multi-layer routing, Rip-up & reroute
- **Static Timing Analysis (STA)**: ATs, RATs, Slack calculation, Critical path identification
- **Technology Mapping**: Area-optimal, Delay-optimal, Balanced optimization strategies

## 📦 Installation

```bash
# Clone the repository
git clone <repository-url>
cd Mylogic

# Install dependencies (optional)
pip install numpy matplotlib

# Install Graphviz (optional, for DOT output)
# Windows: Download from https://graphviz.org/download/
# Linux: sudo apt-get install graphviz
# macOS: brew install graphviz

# Install Yosys (for synthesis features)
# Windows: Download from https://github.com/YosysHQ/yosys/releases
# Linux: sudo apt-get install yosys
# macOS: brew install yosys
```

## 🎯 Quick Start

### Basic Usage

```bash
# Start interactive shell (auto-detect mode)
python mylogic.py

# Load file and auto-detect mode
python mylogic.py --file examples/arithmetic_operations.v

# Check dependencies
python mylogic.py --check-deps

# Debug mode
python mylogic.py --debug
```

### Example Workflows

#### 1. Vector Simulation (n-bit)
```bash
python mylogic.py --file examples/arithmetic_operations.v
mylogic> stats
mylogic> simulate
# Enter values: 5, 3, 8, 2
mylogic> exit
```

#### 2. Yosys Synthesis
```bash
python mylogic.py
mylogic> read examples/arithmetic_operations.v
mylogic> yosys_flow examples/arithmetic_operations.v balanced
mylogic> yosys_stat examples/arithmetic_operations.v
mylogic> exit
```

#### 3. Yosys Output Formats
```bash
python mylogic.py
mylogic> read examples/arithmetic_operations.v
mylogic> write_verilog output.v
mylogic> write_json output.json
mylogic> write_blif output.blif
mylogic> # Files saved to outputs/ directory
mylogic> exit
```

#### 4. VLSI CAD Part 2 Features
```bash
python mylogic.py
mylogic> place random           # Random placement
mylogic> place force            # Force-directed placement
mylogic> route maze             # Maze routing
mylogic> timing                 # Static Timing Analysis
mylogic> techmap area           # Area-optimal technology mapping
mylogic> exit
```

#### 5. Auto-detect Mode
```bash
python mylogic.py --file examples/arithmetic_operations.v
# Automatically detects vector file and uses vector shell
```

## 📁 Project Structure

```
Mylogic/
├── mylogic.py              # Main unified launcher
├── cli/                    # Shell interfaces
│   └── vector_shell.py    # Vector shell with Yosys integration
├── core/                   # Core modules
│   ├── arithmetic_simulation.py  # Vector arithmetic simulation + VectorValue
│   ├── bdd.py             # Binary Decision Diagrams (VLSI CAD Part 1)
│   ├── dce.py             # Dead Code Elimination (VLSI CAD Part 1)
│   ├── sat_solver.py      # SAT Solver (VLSI CAD Part 1)
│   ├── placement.py       # ASIC Placement (VLSI CAD Part 2)
│   ├── routing.py         # ASIC Routing (VLSI CAD Part 2)
│   ├── timing_analysis.py # Static Timing Analysis (VLSI CAD Part 2)
│   └── technology_mapping.py # Technology Mapping (VLSI CAD Part 2)
├── frontends/              # Parsers
│   ├── simple_arithmetic_verilog.py  # Arithmetic Verilog parser
│   ├── simplelang.py      # Simple Language parser
│   └── verilog.py         # Basic Verilog parser
├── synthesis/              # Yosys integration
│   ├── yosys_combinational.py  # Combinational synthesis
│   ├── yosys_commands.py      # Yosys commands
│   └── yosys_integration.py   # Integration layer
├── examples/               # Example files
│   ├── arithmetic_operations.v
│   ├── bitwise_operations.v
│   ├── complex_arithmetic.v
│   ├── full_adder.v
│   ├── my_design.v
│   ├── simple_multiplier.v
│   ├── vlsi_cad_demo.py        # VLSI CAD Part 1 demo
│   └── vlsi_cad_part2_demo.py  # VLSI CAD Part 2 demo
├── docs/                   # Documentation
│   └── input_format.md
├── scripts/                # Demo scripts
│   └── flow_demo.sh
├── outputs/                # Output files
│   ├── *.v                # Verilog RTL files
│   ├── *.json             # JSON netlist files
│   └── *.blif             # BLIF format files
├── mylogic_config.json     # Configuration
└── README.md              # This file
```

## 🔧 Commands

### Basic Commands
- `read <file>` - Load Verilog file
- `stats` - Show circuit statistics
- `simulate` - Run simulation (auto-detect vector/scalar)
- `vsimulate` - Run n-bit vector simulation (legacy)
- `history` - Show command history
- `clear` - Clear screen
- `help` - Show all commands
- `exit` - Quit shell

### Yosys Integration Commands
- `yosys_synth <file> [output] [optimization_level]` - Run synthesis
- `yosys_opt <file> <pass> [output]` - Run optimization pass
- `yosys_stat <file>` - Get design statistics
- `yosys_flow <file> [optimization_level]` - Complete synthesis flow
- `yosys_help` - Show Yosys help

### Yosys Output Commands
- `write_verilog <file>` - Write Verilog RTL output (saved to outputs/)
- `write_json <file>` - Write JSON netlist (saved to outputs/)
- `write_blif <file>` - Write BLIF format (saved to outputs/)
- `write_edif <file>` - Write EDIF format (saved to outputs/)
- `write_spice <file>` - Write SPICE netlist (saved to outputs/)
- `write_dot <file>` - Write DOT graph format (saved to outputs/)
- `write_liberty <file>` - Write Liberty library (saved to outputs/)
- `write_systemverilog <file>` - Write SystemVerilog output (saved to outputs/)

### Available Optimization Passes
- `opt_expr` - Expression optimization
- `opt_clean` - Clean up
- `opt_muxtree` - Multiplexer optimization
- `opt_reduce` - Reduction optimization
- `opt_merge` - Merge optimization
- `wreduce` - Wire reduction
- `peepopt` - Peephole optimization
- `opt_dff` - DFF optimization
- `opt_mem` - Memory optimization

## 📝 Example Files

### Arithmetic Operations
```verilog
module arithmetic_operations(a, b, c, d, sum_out, diff_out, prod_out, quot_out);
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

### Bitwise Operations
```verilog
module bitwise_operations(a, b, and_out, or_out, xor_out, not_out);
  input [3:0] a, b;
  output [3:0] and_out, or_out, xor_out, not_out;
  
  assign and_out = a & b;      // Bitwise AND
  assign or_out = a | b;      // Bitwise OR
  assign xor_out = a ^ b;     // Bitwise XOR
  assign not_out = ~a;        // Bitwise NOT
endmodule
```

## 🎯 Supported Operations

### Arithmetic Operations
- **Addition**: `a + b`
- **Subtraction**: `a - b`
- **Multiplication**: `a * b`
- **Division**: `a / b`

### Bitwise Operations
- **AND**: `a & b`
- **OR**: `a | b`
- **XOR**: `a ^ b`
- **NOT**: `~a`

### Vector Support
- **Vector Declarations**: `[3:0] a, b`
- **Multiple Bit Widths**: 2-bit, 3-bit, 4-bit, 5-bit, 6-bit, 8-bit
- **Vector Arithmetic**: Full n-bit operations
- **Vector Simulation**: Integer input/output

### Yosys Synthesis Features (Powered by Yosys)
- **Combinational Logic**: Full combinational circuit synthesis (Yosys proc)
- **Optimization Levels**: Fast, Balanced, Thorough (Yosys ABC scripts)
- **ABC Scripts**: Area, Delay, Mixed optimization (Yosys ABC integration)
- **Technology Mapping**: Liberty-based mapping (Yosys techmap)
- **Statistics**: Design analysis and reporting (Yosys stat)

### Yosys Output Formats (Backends)
- **Verilog**: `write_verilog` - Standard Verilog RTL output (saved to outputs/)
- **JSON**: `write_json` - JSON netlist format (saved to outputs/)
- **BLIF**: `write_blif` - Berkeley Logic Interchange Format (saved to outputs/)
- **EDIF**: `write_edif` - Electronic Design Interchange Format (saved to outputs/)
- **SPICE**: `write_spice` - SPICE netlist format (saved to outputs/)
- **DOT**: `write_dot` - Graphviz DOT format for visualization (saved to outputs/)
- **Liberty**: `write_liberty` - Liberty timing library format (saved to outputs/)
- **SystemVerilog**: `write_systemverilog` - SystemVerilog output (saved to outputs/)

### Output Files Location
- **Directory**: `outputs/` (auto-created)
- **Formats**: .v, .json, .blif, .edif, .spice, .dot, .liberty, .sv
- **Organization**: All output files organized in outputs/ directory

## 🔍 Troubleshooting

### Common Issues

1. **Import Errors**: Ensure all dependencies are installed
2. **File Not Found**: Check file paths and permissions
3. **Simulation Errors**: Verify input values and circuit logic
4. **Vector Errors**: Ensure vector widths match declarations
5. **Yosys Not Available**: Install Yosys for synthesis features
6. **ABC Not Found**: Install ABC for optimization features

### Debug Mode

```bash
python mylogic.py --debug
```

### Check Dependencies

```bash
python mylogic.py --check-deps
```

## 📊 Performance

- **Scalar Simulation**: Optimized for 1-bit operations
- **Vector Simulation**: Efficient n-bit arithmetic
- **Yosys Integration**: Professional synthesis capabilities
- **Memory Usage**: Optimized for large circuits
- **Speed**: Fast simulation and optimization
- **Synthesis**: Complete combinational logic synthesis

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🎉 Acknowledgments

- **Yosys**: Core synthesis engine and optimization algorithms
- **ABC**: Optimization algorithms (integrated via Yosys)
- **Graphviz**: For visualization support
- **NumPy**: For numerical operations
- **Python Community**: For excellent libraries

---

**MyLogic EDA Tool v1.0.0** - *Yosys-Powered Electronic Design Automation*
