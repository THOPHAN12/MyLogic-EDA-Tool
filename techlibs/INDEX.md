# 📚 **TECHLIBS INDEX - QUICK REFERENCE**

## 🔍 **NAVIGATION GUIDE**

### **Main Documentation**
- 📖 **[README.md](README.md)** - Complete techlibs overview and usage guide

---

## 📁 **LIBRARY STRUCTURE**

### **NEW ORGANIZED LAYOUT** ✨

```
techlibs/
├── 📖 README.md          ← Main documentation
├── 📑 INDEX.md           ← This quick reference
│
├── 🔲 asic/              ← ASIC Technology Libraries
│   ├── README.md         ← ASIC library documentation
│   └── standard_cells.lib (7.1 KB)
│
└── 🔷 fpga/              ← FPGA Technology Libraries
    ├── README.md         ← FPGA library documentation
    ├── common/           (25 files)
    ├── xilinx/           (46 files)
    ├── intel/            (20 files)
    ├── ice40/            (30 files)
    ├── lattice/          (43 files)
    ├── gowin/            (15 files)
    └── anlogic/          (12 files)
```

---

## 🔲 **ASIC LIBRARIES**

### **asic/standard_cells.lib - MyLogic Custom**

**Path**: `techlibs/asic/standard_cells.lib`  
**Format**: Liberty (.lib)  
**Target**: ASIC synthesis

**Contents**:
- 8 Standard cells (INV, NAND2, AND2, OR2, XOR2, NAND3, AOI21, DFF)
- Timing characterization (cell_rise, cell_fall)
- Power analysis (leakage power)
- Capacitance modeling

**Documentation**: See `asic/README.md`

---

## 🔷 **FPGA LIBRARIES**

### **1. fpga/common/ (Technology-Independent)**
**Path**: `techlibs/fpga/common/`  
**Files**: 25  
**Key Files**:
- `simcells.v` (90KB) - Basic simulation primitives (AND, OR, XOR, FF, ...)
- `simlib.v` (78KB) - Extended simulation library
- `techmap.v` (17KB) - Technology mapping rules
- `cells.lib` - Liberty format cell library

**Usage**:
```verilog
// Include in Verilog simulation
`include "simcells.v"
```

---

### **2. fpga/xilinx/ (FPGA - Most Popular)**
**Path**: `techlibs/fpga/xilinx/`  
**Files**: 46  
**Supported Devices**:
- 7-Series: Artix-7, Kintex-7, Virtex-7
- UltraScale, UltraScale+
- Zynq-7000, Zynq UltraScale+ MPSoC

**Key Files**:
- `cells_sim.v` - Xilinx primitive simulation models
- `cells_xtra.v` - Additional Xilinx cells
- `xc7_dsp_map.v` - 7-Series DSP48E1 mapping
- `xcu_dsp_map.v` - UltraScale DSP48E2 mapping
- `brams_xcu_map.v` - UltraRAM mapping
- `lut_map.v` - LUT mapping (LUT1-LUT6)

**Resources**:
- BRAM variants: xc2v, xc3sda, xc4v, xc5v, xc6v, xcu, xcv
- LUTRAM support for xc5v, xcu, xcv
- DSP48: 3sda, 3s, 4v, 5v, 6s, 7, ultras cale

---

### **3. fpga/intel/ (FPGA - Second Most Popular)**
**Path**: `techlibs/fpga/intel/`  
**Files**: 20  
**Supported Devices**:
- Cyclone IV, V, 10 LP/GX
- Stratix IV, V, 10
- Arria II, V, 10
- MAX 10

**Key Files**:
- Common Intel primitives and mapping rules
- Device-specific optimizations

---

### **4. fpga/ice40/ (Lattice - Open-Source Friendly)**
**Path**: `techlibs/fpga/ice40/`  
**Files**: 30  
**Supported Devices**:
- iCE40 LP (Low Power)
- iCE40 HX (High Performance)
- iCE40 UP5K (UltraPlus 5K)
- iCE40 UltraPlus

**Key Files**:
- `cells_sim.v` - iCE40 primitive models
- `cells_map.v` - Technology mapping
- `brams.txt` - 4Kbit Block RAM configuration
- `lutrams.txt` - LUT RAM configuration
- `dsp_map.v` - DSP (MAC16) mapping

**Special Features**:
- 4-input LUTs (LUT4)
- Carry logic (SB_CARRY)
- Block RAM (SB_RAM40_4K, SB_RAM256x16)
- Hard multipliers (SB_MAC16)
- RGB LED driver, I2C, SPI primitives

**Open-Source Toolchain**:
- Project IceStorm
- nextpnr-ice40
- icestorm tools

---

### **5. fpga/lattice/ (ECP5 & MachXO)**
**Path**: `techlibs/fpga/lattice/`  
**Files**: 43  
**Supported Devices**:
- ECP5, ECP5-5G
- MachXO2, MachXO3

**Sub-libraries**:
- `ecp5/` - ECP5 primitives
- `machxo2/` - MachXO2 primitives

---

### **6. fpga/gowin/ (Chinese FPGA Vendor)**
**Path**: `techlibs/fpga/gowin/`  
**Files**: 15  
**Supported Devices**:
- GW1N, GW1NR, GW1NS series
- GW2A series

**Key Files**:
- `cells_sim.v` - Gowin LUT, FF, BRAM, DSP primitives
- `cells_map.v` - Technology mapping
- `arith_map.v` - Arithmetic logic mapping
- `brams_map.v` - Block RAM mapping

---

### **7. fpga/anlogic/ (Chinese FPGA Vendor)**
**Path**: `techlibs/fpga/anlogic/`  
**Files**: 12  
**Supported Devices**:
- EG4 series (Eagle)

**Key Files**:
- `cells_sim.v` - Anlogic primitives
- `arith_map.v` - Arithmetic mapping
- `lutrams_map.v` - LUTRAM mapping

---

## 🎯 **QUICK START EXAMPLES**

### **Example 1: Xilinx 7-Series Synthesis**

```tcl
# Yosys script for Xilinx 7-Series
read_verilog design.v
synth_xilinx -top top_module -family xc7
write_edif output.edif
```

### **Example 2: iCE40 Open-Source Flow**

```bash
# Complete open-source FPGA flow
yosys -p "synth_ice40 -top top -json design.json" design.v
nextpnr-ice40 --up5k --json design.json --asc design.asc
icepack design.asc design.bin
```

### **Example 3: Technology-Independent Simulation**

```verilog
// Use common simcells for verification
`timescale 1ns/1ps
`include "simcells.v"

module testbench;
  // Your testbench code
endmodule
```

---

## 📊 **LIBRARY COMPARISON**

| Vendor | LUT Size | Block RAM | DSP | Open-Source Tools |
|--------|----------|-----------|-----|-------------------|
| **Xilinx 7-Series** | LUT6 | 36Kb | DSP48E1 | ❌ (Vivado only) |
| **Intel Cyclone V** | ALM (8-input) | M10K | DSP | ❌ (Quartus only) |
| **iCE40 UP5K** | LUT4 | 4Kb (30 blocks) | MAC16 | ✅ **IceStorm** |
| **ECP5** | LUT4 | 18Kb | DSP | ✅ **nextpnr** |
| **Gowin GW1N** | LUT4 | 9Kb (BSRAM) | DSP | 🟡 Partial |
| **Anlogic EG4** | LUT4 | 9Kb | - | 🟡 Partial |

---

## 🔧 **FILE TYPE GUIDE**

### **Verilog Files (.v)**
- `cells_sim.v` - Simulation models for primitives
- `cells_map.v` - Technology mapping rules
- `xxx_map.v` - Specific resource mapping (BRAM, DSP, LUTRAM, ...)

### **Text Files (.txt)**
- `brams*.txt` - Block RAM configurations (width, depth, init)
- `lutrams*.txt` - LUT RAM configurations
- `urams.txt` - UltraRAM configurations (Xilinx)

### **Liberty Files (.lib)**
- Cell timing and power characterization
- Used for static timing analysis (STA)

### **Python Scripts (.py)**
- `cells_xtra.py` - Generate additional cell variants
- `gen_fine_ffs.py` - Generate fine-grained flip-flop variants

### **C++ Files (.cc)**
- Yosys plugin implementations
- Optimization passes

### **PMG Files (.pmg)**
- Pattern matching for optimization
- Used by Yosys pattern matcher

---

## 📖 **DOCUMENTATION HIERARCHY**

```
techlibs/
├── 📖 INDEX.md (THIS FILE) ← Quick reference guide
├── 📖 README.md ← Complete overview and usage
│
├── 🔲 asic/ ← ASIC Technology Libraries
│   ├── README.md ← ASIC documentation
│   └── standard_cells.lib ← MyLogic custom library
│
└── 🔷 fpga/ ← FPGA Technology Libraries
    ├── README.md ← FPGA documentation
    ├── common/ ← Technology-independent
    │   ├── simcells.v ← Basic primitives
    │   └── simlib.v ← Extended library
    ├── xilinx/ ← Xilinx FPGAs
    │   ├── cells_sim.v ← Xilinx primitives
    │   ├── xc7_dsp_map.v ← DSP48 mapping
    │   └── ...
    ├── intel/ ← Intel/Altera FPGAs
    ├── ice40/ ← Lattice iCE40
    │   ├── cells_sim.v ← iCE40 primitives
    │   └── brams.txt ← BRAM config
    ├── lattice/ ← Lattice ECP5/MachXO
    ├── gowin/ ← Gowin FPGAs
    └── anlogic/ ← Anlogic FPGAs
```

---

## 🔗 **USEFUL LINKS**

### **Yosys Resources**
- 📚 [Yosys Manual](https://yosyshq.readthedocs.io/)
- 🐙 [Yosys GitHub](https://github.com/YosysHQ/yosys)
- 💬 [Yosys Discussions](https://github.com/YosysHQ/yosys/discussions)

### **FPGA Vendor Documentation**
- 🔷 [Xilinx 7-Series Libraries Guide](https://www.xilinx.com/support/documentation/sw_manuals/xilinx2021_1/ug953-vivado-7series-libraries.pdf)
- 🔶 [Intel Quartus Primitives](https://www.intel.com/content/www/us/en/docs/programmable/683328/current/primitives.html)
- 🧊 [iCE40 Datasheet](https://www.latticesemi.com/Products/FPGAandCPLD/iCE40)

### **Open-Source FPGA Tools**
- ❄️ [Project IceStorm](http://www.clifford.at/icestorm/)
- 🔀 [nextpnr](https://github.com/YosysHQ/nextpnr)
- 🦋 [SymbiFlow](https://symbiflow.github.io/)

---

## 📝 **NOTES**

1. **File Encoding**: UTF-8
2. **Line Endings**: Unix (LF) preferred
3. **Verilog Standard**: Verilog-2005 / SystemVerilog subset
4. **Case Sensitivity**: Module names are case-sensitive

---

## ✨ **HIGHLIGHTS**

### **Most Complete**: Xilinx (58 files)
- Comprehensive support from Spartan to UltraScale+
- All resources: LUTs, FFs, BRAM, URAM, DSP48

### **Best Open-Source**: iCE40 (30 files)
- Full open-source toolchain available
- Well-documented primitives
- Active community support

### **Most Universal**: common/ (25 files)
- simcells.v: 90KB of technology-independent cells
- Works with any synthesis tool
- Perfect for academic use

---

**📅 Last Updated**: 2025-10-30  
**📦 Source**: YosysHQ/yosys (main branch)  
**👨‍💻 MyLogic EDA Tool Team**

