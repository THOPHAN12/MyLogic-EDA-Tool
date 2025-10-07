# 📚 Technology Libraries - MyLogic EDA Tool

## Tổng quan

Thư mục `techlibs/` chứa các thư viện công nghệ (technology libraries) cho MyLogic EDA Tool. Các thư viện này định nghĩa các cell có sẵn cho technology mapping và synthesis.

## 📁 Cấu trúc thư mục

```
techlibs/
├── README.md                    # Tài liệu này
├── library_loader.py           # Library loader utility
├── standard_cells.v            # Standard cell library (Verilog)
├── standard_cells.lib          # Standard cell library (Liberty)
├── lut_library.json            # FPGA LUT library (JSON)
└── custom_libraries/           # Thư viện tùy chỉnh (nếu có)
```

## 📋 Các loại thư viện

### 1. **Standard Cell Libraries**

#### **Verilog Format (.v)**
- **File**: `standard_cells.v`
- **Mô tả**: Thư viện cell chuẩn định nghĩa bằng Verilog
- **Cells**: INV, NAND2, NOR2, AND2, OR2, XOR2, XNOR2, NAND3, NOR3, AND3, OR3, AOI21, OAI21, AOI22, OAI22, NAND4, NOR4, AND4, OR4, MUX2, MUX4, DFF, DFFE

#### **Liberty Format (.lib)**
- **File**: `standard_cells.lib`
- **Mô tả**: Thư viện cell chuẩn định nghĩa bằng Liberty format
- **Đặc điểm**: Industry standard format với timing information
- **Cells**: INV, NAND2, AND2, OR2, XOR2, NAND3, AOI21, DFF

### 2. **FPGA LUT Libraries**

#### **JSON Format (.json)**
- **File**: `lut_library.json`
- **Mô tả**: Thư viện LUT cho FPGA technology mapping
- **LUT Sizes**: 4-input LUTs, 6-input LUTs
- **Cells**: LUT4_AND, LUT4_OR, LUT4_XOR, LUT6_AND, LUT6_OR, LUT6_XOR, LUT6_MUX4, etc.
- **Memory Elements**: DFF, DFFE, LATCH

### 3. **Library Loader**

#### **Python Module**
- **File**: `library_loader.py`
- **Mô tả**: Utility để load và quản lý các thư viện
- **Hỗ trợ**: Verilog, Liberty, JSON formats
- **Features**: Auto-discovery, parsing, validation

## 🔧 Sử dụng Library Loader

### **Load tất cả thư viện:**
```python
from techlibs.library_loader import LibraryLoader

loader = LibraryLoader()
libraries = loader.load_all_libraries()

# Lấy thư viện cụ thể
standard_lib = loader.get_library('standard_cells')
lut_lib = loader.get_library('lut_library')
```

### **Load thư viện cụ thể:**
```python
# Load Verilog library
verilog_lib = loader.load_verilog_library('standard_cells.v')

# Load Liberty library
liberty_lib = loader.load_liberty_library('standard_cells.lib')

# Load JSON library
json_lib = loader.load_json_library('lut_library.json')
```

### **Lấy thông tin thư viện:**
```python
# List tất cả thư viện
available_libs = loader.list_available_libraries()

# Lấy thông tin chi tiết
lib_info = loader.get_library_info('standard_cells')
print(f"Total cells: {lib_info['total_cells']}")
print(f"Average area: {lib_info['average_area']}")
print(f"Average delay: {lib_info['average_delay']}")
```

## 📊 Cell Information

### **LibraryCell Properties:**
- **name**: Tên cell (ví dụ: NAND2, LUT4_AND)
- **function**: Hàm Boolean (ví dụ: ~(A & B), A & B & C & D)
- **area**: Diện tích cell (đơn vị: μm² hoặc normalized)
- **delay**: Độ trễ cell (đơn vị: ns hoặc normalized)
- **input_pins**: Danh sách input pins
- **output_pins**: Danh sách output pins
- **input_load**: Load capacitance của inputs
- **output_drive**: Drive strength của outputs

### **TechnologyLibrary Properties:**
- **name**: Tên thư viện
- **cells**: Dictionary của cells (name -> LibraryCell)
- **function_map**: Mapping từ function đến list of cell names

## 🎯 Technology Mapping

### **Area-Optimal Mapping:**
```python
from core.technology_mapping.technology_mapping import TechnologyMapper

# Load library
loader = LibraryLoader()
library = loader.get_library('standard_cells')

# Create mapper
mapper = TechnologyMapper(library)

# Map với area optimization
mapped_netlist = mapper.map_netlist(netlist, optimization_target="area")
```

### **Delay-Optimal Mapping:**
```python
# Map với delay optimization
mapped_netlist = mapper.map_netlist(netlist, optimization_target="delay")
```

### **Balanced Mapping:**
```python
# Map với balanced optimization
mapped_netlist = mapper.map_netlist(netlist, optimization_target="balanced")
```

## 📈 Performance Metrics

### **Standard Cells Library:**
- **Total Cells**: 20+ cells
- **Gate Types**: Basic gates, complex gates, memory elements
- **Area Range**: 1.0 - 5.0 (normalized)
- **Delay Range**: 0.1 - 0.7 ns (normalized)

### **LUT Library:**
- **LUT4 Cells**: 8 cells
- **LUT6 Cells**: 6 cells
- **Memory Elements**: 3 types
- **Area Range**: 1.0 - 2.2 (normalized)
- **Delay Range**: 0.1 - 0.3 ns (normalized)

## 🔄 Integration với MyLogic

### **CLI Commands:**
```bash
# Load library và show info
mylogic> load_library standard_cells
mylogic> library_info standard_cells

# Technology mapping
mylogic> techmap area
mylogic> techmap delay
mylogic> techmap balanced
```

### **Python API:**
```python
# Load library
from techlibs.library_loader import LibraryLoader
loader = LibraryLoader()
library = loader.get_library('standard_cells')

# Use trong synthesis flow
from core.synthesis.synthesis_flow import run_complete_synthesis
optimized_netlist = run_complete_synthesis(netlist, "standard")
```

## 🚀 Tạo thư viện tùy chỉnh

### **1. Verilog Library:**
```verilog
// custom_library.v
module CUSTOM_GATE (input A, B, output Y);
    assign Y = ~(A & B);
endmodule
```

### **2. JSON Library:**
```json
{
  "library_name": "custom_library",
  "lut4_cells": {
    "CUSTOM_LUT": {
      "function": "A & B & C & D",
      "area": 1.2,
      "delay": 0.15,
      "power": 0.08
    }
  }
}
```

### **3. Liberty Library:**
```liberty
library(custom_library) {
    cell(CUSTOM_CELL) {
        area : 1.5;
        pin(A) { direction : input; }
        pin(Y) { direction : output; }
    }
}
```

## 📚 Tham khảo

### **Industry Standards:**
- **Liberty Format**: IEEE 1364-2005
- **Verilog**: IEEE 1364-2005
- **JSON**: RFC 7159

### **ABC Integration:**
- **ABC Library Binding**: `src/map/mapper.c`
- **Cut Enumeration**: ABC technology mapping algorithms
- **Area/Delay Optimization**: ABC optimization techniques

### **MyLogic Integration:**
- **Technology Mapping**: `core/technology_mapping/technology_mapping.py`
- **Library Loading**: `techlibs/library_loader.py`
- **Synthesis Flow**: `core/synthesis/synthesis_flow.py`

---

**📅 Cập nhật cuối**: 2025-10-07  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
