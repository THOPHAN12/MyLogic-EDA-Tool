# 📚 **MYLOGIC TECHNOLOGY LIBRARIES**

## 🎯 **TỔNG QUAN**

Thư viện công nghệ (Technology Libraries) cho MyLogic EDA Tool, tích hợp từ **YosysHQ/yosys**.

**Source**: https://github.com/YosysHQ/yosys/tree/main/techlibs

---

## 📁 **CẤU TRÚC THƯ MỤC**

### **NEW ORGANIZED STRUCTURE** ✨

```
techlibs/
├── asic/              ← ASIC Technology Libraries
│   ├── README.md
│   └── standard_cells.lib
│
└── fpga/              ← FPGA Technology Libraries  
    ├── README.md
    ├── common/        (Technology-independent)
    ├── xilinx/        (Xilinx FPGAs)
    ├── intel/         (Intel/Altera FPGAs)
    ├── ice40/         (Lattice iCE40)
    ├── lattice/       (Lattice ECP5/MachXO)
    ├── gowin/         (Gowin FPGAs)
    └── anlogic/       (Anlogic FPGAs)
```

---

## 🔲 **ASIC LIBRARIES**

### **`asic/standard_cells.lib` - MyLogic Custom Library**
- **Mô tả**: Standard cell library in Liberty format
- **Cells**: INV, NAND2, AND2, OR2, XOR2, NAND3, AOI21, DFF (8 cells)
- **Features**: Timing characterization, power analysis, capacitance modeling
- **Ứng dụng**: ASIC synthesis, static timing analysis, academic purposes
- **Documentation**: `asic/README.md`

---

## 🔷 **FPGA LIBRARIES**

### **1. `fpga/common/` - Common Cells (25 files)**
- **Mô tả**: Thư viện simulation cells cơ bản
- **Files quan trọng**:
  - `simcells.v` - Basic simulation primitives
  - `simlib.v` - Simulation library
  - `techmap.v` - Technology mapping rules
- **Ứng dụng**: Technology-independent synthesis, simulation

### **2. `fpga/xilinx/` - Xilinx FPGA (46 files)**
- **Mô tả**: Thư viện cho Xilinx FPGAs (7-series, UltraScale, UltraScale+)
- **Chips hỗ trợ**:
  - Artix-7, Kintex-7, Virtex-7
  - Zynq-7000
  - UltraScale, UltraScale+
- **Files quan trọng**:
  - `cells_sim.v` - Xilinx primitives simulation
  - `cells_xtra.v` - Additional cells
  - `arith_map.v` - Arithmetic mapping
  - `dsp_map.v` - DSP48 mapping
- **Ứng dụng**: Xilinx FPGA synthesis, mapping LUTs/FFs/DSPs

### **3. `fpga/intel/` - Intel/Altera FPGA (20 files)**
- **Mô tả**: Thư viện cho Intel (Altera) FPGAs
- **Chips hỗ trợ**:
  - Cyclone IV, V, 10
  - Stratix IV, V, 10
  - Arria II, V, 10
  - MAX 10
- **Files quan trọng**:
  - `common/` - Common Intel primitives
  - `cyclone10/` - Cyclone 10 specific
  - `max10/` - MAX 10 specific
- **Ứng dụng**: Intel FPGA synthesis

### **4. `fpga/ice40/` - Lattice iCE40 (30 files)**
- **Mô tả**: Thư viện cho Lattice iCE40 FPGAs (open-source friendly)
- **Chips hỗ trợ**:
  - iCE40 LP, HX, UP5K
  - iCE40 UltraPlus
- **Files quan trọng**:
  - `cells_sim.v` - iCE40 simulation primitives
  - `cells_map.v` - Technology mapping
  - `brams.txt` - Block RAM configuration
  - `lutrams.txt` - LUT RAM configuration
- **Ứng dụng**: Open-source FPGA development, ice storm toolchain

### **5. `fpga/lattice/` - Lattice ECP5 & MachXO (43 files)**
- **Mô tả**: Thư viện cho Lattice ECP5 và MachXO FPGAs
- **Chips hỗ trợ**:
  - ECP5, ECP5-5G
  - MachXO2, MachXO3
- **Files quan trọng**:
  - `ecp5/` - ECP5 primitives
  - `machxo2/` - MachXO2 primitives
- **Ứng dụng**: Lattice FPGA synthesis

### **6. `fpga/gowin/` - Gowin FPGA (15 files)**
- **Mô tả**: Thư viện cho Gowin FPGAs (Chinese vendor)
- **Chips hỗ trợ**:
  - GW1N, GW2A series
  - GW1NR, GW1NS
- **Files quan trọng**:
  - `cells_sim.v` - Gowin primitives
  - `cells_map.v` - Technology mapping
- **Ứng dụng**: Gowin FPGA synthesis

### **7. `fpga/anlogic/` - Anlogic FPGA (12 files)**
- **Mô tả**: Thư viện cho Anlogic FPGAs (Chinese vendor)
- **Chips hỗ trợ**:
  - EG4, Eagle series
- **Files quan trọng**:
  - `cells_sim.v` - Anlogic primitives
  - `arith_map.v` - Arithmetic mapping
- **Ứng dụng**: Anlogic FPGA synthesis


---

## 🚀 **USAGE EXAMPLES**

### **Example 1: Technology Mapping với Xilinx**

```python
from core.technology_mapping.technology_mapping import TechnologyMapper, TechnologyLibrary

# Load Xilinx techlib
library = TechnologyLibrary("xilinx_7series")
# Parse cells_sim.v để tạo library
# ...

# Perform technology mapping
mapper = TechnologyMapper(library)
results = mapper.perform_technology_mapping("area_optimal")
```

### **Example 2: Simulation với Common Cells**

```python
# Use simcells.v for technology-independent simulation
# MyLogic simulation engine có thể reference common cells
```

### **Example 3: FPGA Synthesis Flow**

```bash
# Yosys script example:
read_verilog design.v
synth_xilinx -top top_module
abc -lut 6
write_blif output.blif
```

---

## 📊 **STATISTICS**

| Vendor | Files | Description |
|--------|-------|-------------|
| **common** | 25 | Technology-independent cells |
| **xilinx** | 58 | Xilinx FPGA primitives |
| **intel** | 20 | Intel/Altera FPGA primitives |
| **ice40** | 30 | Lattice iCE40 primitives |
| **lattice** | 43 | Lattice ECP5/MachXO primitives |
| **gowin** | 15 | Gowin FPGA primitives |
| **anlogic** | 12 | Anlogic FPGA primitives |
| **TOTAL** | **203** | **7 vendors** |

---

## 🔧 **INTEGRATION STATUS**

### ✅ **Integrated (Có sẵn)**
- [x] Common cells (simcells.v, simlib.v)
- [x] Xilinx 7-series, UltraScale
- [x] Intel Cyclone/Stratix/Arria
- [x] Lattice iCE40 (open-source)
- [x] Lattice ECP5/MachXO
- [x] Gowin FPGA
- [x] Anlogic FPGA

### 🔄 **To Be Integrated (Có thể thêm)**
- [ ] Achronix FPGAs
- [ ] Efinix FPGAs
- [ ] GateMate FPGAs
- [ ] QuickLogic FPGAs
- [ ] Microchip FPGAs
- [ ] NanoXplore FPGAs

---

## 📚 **FILE FORMATS**

### **1. Verilog (.v)**
- Simulation primitives
- Technology mapping rules
- Primitive instantiation templates

### **2. Liberty (.lib)**
- Timing characterization
- Power analysis
- Cell descriptions

### **3. Text Files (.txt)**
- Configuration tables (BRAM, LUTRAM)
- Routing resources
- Device parameters

### **4. Makefiles**
- Build scripts
- Library compilation

---

## 🎓 **LEARNING RESOURCES**

### **Yosys Documentation**
- https://yosyshq.net/yosys/documentation.html
- https://github.com/YosysHQ/yosys

### **FPGA Vendor Documentation**
- **Xilinx**: https://www.xilinx.com/support/documentation.html
- **Intel**: https://www.intel.com/content/www/us/en/products/programmable.html
- **Lattice**: https://www.latticesemi.com/en/Support/Documentation

### **Open-Source FPGA Tools**
- **Project IceStorm**: http://www.clifford.at/icestorm/
- **nextpnr**: https://github.com/YosysHQ/nextpnr
- **Symbiflow**: https://symbiflow.github.io/

---

## 🔗 **REFERENCES**

1. **YosysHQ/yosys** - https://github.com/YosysHQ/yosys
2. **ABC Tool** - https://github.com/berkeley-abc/abc
3. **VLSI CAD Textbooks** - Logic synthesis and technology mapping
4. **Industry Standards** - Liberty, Verilog, EDIF

---

## 📝 **VERSION HISTORY**

- **v1.0** (2025-10-30)
  - Tích hợp 7 vendors từ Yosys
  - 203 files techlibs
  - Custom standard_cells.lib

---

## 👨‍💻 **AUTHORS & CONTRIBUTORS**

- **MyLogic Team** - Integration and customization
- **YosysHQ** - Original techlibs source
- **Open-source FPGA community** - Cell libraries

---

**📅 Last Updated**: 2025-10-30  
**📦 Source**: YosysHQ/yosys (main branch)  
**📄 License**: ISC License (from Yosys)

