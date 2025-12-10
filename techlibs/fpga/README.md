# 🔷 **FPGA TECHNOLOGY LIBRARIES**

## 📋 **OVERVIEW**

Technology libraries cho **FPGA (Field-Programmable Gate Array)** synthesis, tích hợp từ **YosysHQ/yosys**.

**Source**: https://github.com/YosysHQ/yosys/tree/main/techlibs

---

## 📁 **VENDOR LIBRARIES**

### **Summary**

| Vendor | Files | Target Devices | Open-Source |
|--------|-------|----------------|-------------|
| **common** | 25 | Technology-independent | ✅ |
| **xilinx** | 46 | 7-Series, UltraScale(+) | ❌ |
| **intel** | 20 | Cyclone, Stratix, Arria | ❌ |
| **ice40** | 30 | Lattice iCE40 | ✅ |
| **lattice** | 43 | ECP5, MachXO | 🟡 |
| **gowin** | 15 | GW1N, GW2A | 🟡 |
| **anlogic** | 12 | EG4, Eagle | 🟡 |
| **TOTAL** | **203+** | | |

---

## 📚 **VENDOR DETAILS**

### **1. common/ - Technology-Independent (25 files)**

**Purpose**: Generic simulation and synthesis  
**Use Case**: Technology-independent development, simulation, verification

**Key Files**:
- `simcells.v` (90 KB) - Basic primitives (AND, OR, XOR, FF, ...)
- `simlib.v` (78 KB) - Extended library
- `techmap.v` (17 KB) - Generic mapping rules
- `cells.lib` (2.4 KB) - Liberty format

**Supported Primitives**:
- Logic gates: AND, OR, XOR, NOT, NAND, NOR, XNOR
- Multiplexers: MUX2, MUX4, MUX8, MUX16
- Flip-flops: DFF, DFFE, DFFSR
- Latches: Transparent latches
- Arithmetic: ADD, SUB, MUL

---

### **2. xilinx/ - Xilinx FPGAs (46 files)** ⭐

**Supported Families**:
- **7-Series**: Artix-7, Kintex-7, Virtex-7, Zynq-7000
- **UltraScale**: Kintex UltraScale, Virtex UltraScale
- **UltraScale+**: Kintex UltraScale+, Virtex UltraScale+, Zynq UltraScale+ MPSoC

**Key Resources**:
- **LUTs**: LUT1, LUT2, LUT3, LUT4, LUT5, LUT6
- **Carry Logic**: CARRY4 (7-Series), CARRY8 (UltraScale+)
- **Block RAM**: RAMB36E1, RAMB18E1 (36Kb, 18Kb)
- **UltraRAM**: URAM288 (288Kb, UltraScale+ only)
- **DSP**: DSP48E1 (7-Series), DSP48E2 (UltraScale)
- **Multiplexers**: MUXF7, MUXF8, MUXF9
- **Flip-Flops**: FDRE, FDSE, FDCE, FDPE

**Key Files**:
- `cells_sim.v` - Xilinx primitive models
- `xc7_dsp_map.v` - DSP48E1 mapping (7-Series)
- `xcu_dsp_map.v` - DSP48E2 mapping (UltraScale)
- `brams_xcu_map.v` - BRAM/URAM mapping
- `lut_map.v` - LUT1-LUT6 mapping

---

### **3. intel/ - Intel/Altera FPGAs (20 files)**

**Supported Families**:
- **Cyclone**: IV, V, 10 LP/GX
- **Stratix**: IV, V, 10
- **Arria**: II, V, 10
- **MAX**: 10

**Key Resources**:
- **ALM**: Adaptive Logic Module (8-input fracturable)
- **M10K**: 10Kb memory blocks
- **DSP**: Variable-precision DSP blocks
- **PLLs**: Phase-locked loops

**Key Files**:
- `common/` - Intel common primitives
- `cyclone10lp/` - Cyclone 10 LP specific
- `max10/` - MAX 10 specific

---

### **4. ice40/ - Lattice iCE40 (30 files)** ⭐ OPEN-SOURCE

**Supported Devices**:
- **iCE40 LP**: Low Power (384-7680 LUTs)
- **iCE40 HX**: High Performance (384-7680 LUTs)
- **iCE40 UP5K**: UltraPlus 5K (5280 LUTs)
- **iCE40 UltraPlus**: Advanced features

**Key Resources**:
- **LUTs**: SB_LUT4 (4-input LUT)
- **Carry**: SB_CARRY
- **Block RAM**: SB_RAM40_4K (4Kb, 30 blocks)
- **SPRAM**: 4x 32Kb single-port RAM (UP5K only)
- **DSP**: SB_MAC16 (16x16 multiplier-accumulator, 8 blocks)
- **IO**: SB_IO (5V-tolerant)
- **Special**: SB_RGBA_DRV (RGB LED), SB_I2C, SB_SPI

**Key Files**:
- `cells_sim.v` - iCE40 primitive models
- `cells_map.v` - Technology mapping
- `brams.txt` - 4Kb BRAM configuration
- `dsp_map.v` - MAC16 DSP mapping

**Open-Source Toolchain**:
```bash
# Complete open-source flow
yosys -p "synth_ice40 -top top -json design.json" design.v
nextpnr-ice40 --up5k --json design.json --asc design.asc
icepack design.asc design.bin
iceprog design.bin
```

---

### **5. lattice/ - Lattice ECP5 & MachXO (43 files)**

**Supported Families**:
- **ECP5**: LFE5U series (12K-85K LUTs)
- **ECP5-5G**: With 5G SERDES
- **MachXO2**: Low-cost CPLD/FPGA
- **MachXO3**: Enhanced version
- **Nexus**: Next-generation

**Key Resources**:
- **LUTs**: LUT4 (ECP5), enhanced LUTs (Nexus)
- **Block RAM**: 18Kb dual-port
- **DSP**: 18x18 multipliers
- **SERDES**: Multi-Gb/s transceivers (ECP5-5G)

**Key Files**:
- `cells_sim_ecp5.v` - ECP5 primitives
- `cells_sim_nexus.v` - Nexus primitives
- `dsp_map_18x18.v` - 18x18 DSP mapping

---

### **6. gowin/ - Gowin FPGAs (15 files)**

**Supported Families**:
- **GW1N** series (1K-9K LUTs)
- **GW1NR** series (with embedded SDRAM)
- **GW1NS** series (small package)
- **GW2A** series (18K-55K LUTs)

**Key Resources**:
- **LUTs**: LUT4
- **BSRAM**: 9Kb block RAM
- **DSP**: 18x18 multipliers
- **PLLs**: Phase-locked loops

**Key Files**:
- `cells_sim.v` - Gowin primitive models
- `cells_map.v` - Technology mapping
- `brams_map.v` - BRAM mapping

---

### **7. anlogic/ - Anlogic FPGAs (12 files)**

**Supported Families**:
- **EG4** series (Eagle)
- **AL3** series

**Key Resources**:
- **LUTs**: LUT4
- **Block RAM**: 9Kb
- **Arithmetic**: Dedicated carry logic

**Key Files**:
- `cells_sim.v` - Anlogic primitives
- `arith_map.v` - Arithmetic mapping

---

## 🚀 **USAGE EXAMPLES**

### **Example 1: Xilinx 7-Series Synthesis**

```tcl
# Yosys synthesis script
read_verilog design.v

# Xilinx synthesis
synth_xilinx -top top_module -family xc7

# Write output
write_edif output.edif
write_blif output.blif
```

### **Example 2: Open-Source iCE40 Flow**

```bash
# Complete open-source toolchain
yosys -p "synth_ice40 -top top -json design.json" design.v
nextpnr-ice40 --up5k --package sg48 --json design.json --asc design.asc
icepack design.asc design.bin
iceprog design.bin
```

### **Example 3: Technology-Independent Simulation**

```verilog
`timescale 1ns/1ps
`include "common/simcells.v"

module testbench;
  // Your testbench using generic cells
endmodule
```

---

## 📊 **RESOURCE COMPARISON**

| Vendor | LUT Size | Block RAM | DSP | Open-Source |
|--------|----------|-----------|-----|-------------|
| **Xilinx 7-Series** | LUT6 | 36Kb | DSP48E1 (25x18) | ❌ Vivado |
| **Intel Cyclone V** | ALM (8-in) | M10K (10Kb) | Variable | ❌ Quartus |
| **iCE40 UP5K** | LUT4 | 4Kb (30 blocks) | MAC16 (16x16) | ✅ IceStorm |
| **Lattice ECP5** | LUT4 | 18Kb | 18x18 | ✅ nextpnr |
| **Gowin GW1N** | LUT4 | 9Kb (BSRAM) | 18x18 | 🟡 Partial |
| **Anlogic EG4** | LUT4 | 9Kb | - | 🟡 Partial |

---

## 🔧 **FILE TYPES**

### **Verilog Files (.v)**
- `cells_sim.v` - Simulation models for primitives
- `cells_map.v` - Technology mapping rules
- `*_map.v` - Resource-specific mapping (BRAM, DSP, LUTRAM)

### **Text Files (.txt)**
- `brams*.txt` - Block RAM configurations
- `lutrams*.txt` - LUT RAM configurations
- `urams.txt` - UltraRAM (Xilinx only)

### **C++ Files (.cc)**
- Yosys plugin implementations
- Optimization passes

### **PMG Files (.pmg)**
- Pattern matching for optimization

---

## 🎓 **LEARNING RESOURCES**

### **Yosys**
- https://yosyshq.net/yosys/documentation.html
- https://github.com/YosysHQ/yosys

### **Open-Source FPGA**
- **IceStorm**: http://www.clifford.at/icestorm/
- **nextpnr**: https://github.com/YosysHQ/nextpnr
- **SymbiFlow**: https://symbiflow.github.io/

### **Vendor Documentation**
- **Xilinx**: https://www.xilinx.com/support/documentation.html
- **Intel**: https://www.intel.com/content/www/us/en/products/programmable.html
- **Lattice**: https://www.latticesemi.com/Support/Documentation

---

## 📝 **NOTES**

1. All files from **Yosys main branch** (latest as of 2025-10-30)
2. Files maintain **original structure** from Yosys
3. **No modifications** made (pristine copies)
4. **License**: ISC License (inherited from Yosys)

---

**📅 Last Updated**: 2025-10-30  
**📦 Source**: YosysHQ/yosys  
**👨‍💻 MyLogic EDA Tool Team**  
**📄 License**: ISC License

