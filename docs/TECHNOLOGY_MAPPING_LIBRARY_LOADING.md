# 📚 Technology Mapping - Cách Load Thư Viện

## 🔍 **PHÂN TÍCH HIỆN TẠI**

### **Cách Technology Mapping Load Thư Viện**

Hiện tại, `technology_mapping.py` **KHÔNG load từ file** trong folder `techlibs/`. Thay vào đó, nó sử dụng **hardcoded library** được tạo trong code.

---

## 📋 **CÁCH HOẠT ĐỘNG HIỆN TẠI**

### **1. Hardcoded Library (Hiện tại)**

**File:** `core/technology_mapping/technology_mapping.py`

```python
def create_standard_library() -> TechnologyLibrary:
    """Create a standard technology library with common gates."""
    library = TechnologyLibrary("standard_cells")
    
    # Hardcoded gates
    gates = [
        ("INV", "NOT", 1.0, 0.1, ["A"], ["Y"]),
        ("BUF", "BUF", 1.0, 0.05, ["A"], ["Y"]),
        ("NAND2", "NAND(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        # ... more gates
    ]
    
    for name, function, area, delay, inputs, outputs in gates:
        cell = LibraryCell(name, function, area, delay, inputs, outputs)
        library.add_cell(cell)
    
    return library
```

**Cách sử dụng:**
```python
# Trong CLI (cli/vector_shell.py)
from core.technology_mapping.technology_mapping import create_standard_library

library = create_standard_library()  # Tạo hardcoded library
mapper = TechnologyMapper(library)
```

**Vấn đề:**
- ❌ Không load từ `techlibs/` folder
- ❌ Không đọc file `.lib` (Liberty format)
- ❌ Không đọc file `.json` (JSON format)
- ❌ Library bị giới hạn, không mở rộng được

---

## 📁 **THƯ VIỆN CÓ SẴN TRONG `techlibs/`**

### **1. ASIC Libraries**

**File:** `techlibs/asic/standard_cells.lib`
- **Format:** Liberty (.lib)
- **Nội dung:** Standard cells với timing, power, capacitance
- **Cells:** INV, NAND2, AND2, OR2, XOR2, NAND3, AOI21, DFF

**Ví dụ nội dung:**
```liberty
cell (INV) {
    area : 1.0;
    pin (Y) {
        direction : output;
        function : "!A";
    }
    pin (A) {
        direction : input;
        capacitance : 0.1;
    }
}
```

### **2. FPGA Libraries**

**Files:** `techlibs/fpga/*/cells_map.v`, `techlibs/fpga/*/cells_sim.v`
- **Format:** Verilog (.v)
- **Nội dung:** FPGA primitives, LUTs, FFs, DSPs
- **Vendors:** Xilinx, Intel, Lattice, Gowin, Anlogic

---

## 🔧 **CÁCH LOAD THƯ VIỆN TỪ FILE**

### **Option 1: Load từ Liberty Format (.lib)**

**Tạo function mới:**

```python
# core/technology_mapping/library_loader.py

import re
from typing import Dict, List, Any
from .technology_mapping import TechnologyLibrary, LibraryCell

def load_liberty_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from Liberty format file.
    
    Args:
        file_path: Path to .lib file
        
    Returns:
        TechnologyLibrary object
    """
    library = TechnologyLibrary("loaded_library")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse Liberty format
    # Pattern: cell (NAME) { ... }
    cell_pattern = r'cell\s+\((\w+)\)\s*\{([^}]+)\}'
    
    for match in re.finditer(cell_pattern, content, re.DOTALL):
        cell_name = match.group(1)
        cell_body = match.group(2)
        
        # Extract area
        area_match = re.search(r'area\s*:\s*([\d.]+)', cell_body)
        area = float(area_match.group(1)) if area_match else 1.0
        
        # Extract function
        func_match = re.search(r'function\s*:\s*"([^"]+)"', cell_body)
        function = func_match.group(1) if func_match else cell_name
        
        # Extract pins
        pin_pattern = r'pin\s+\((\w+)\)\s*\{([^}]+)\}'
        input_pins = []
        output_pins = []
        
        for pin_match in re.finditer(pin_pattern, cell_body, re.DOTALL):
            pin_name = pin_match.group(1)
            pin_body = pin_match.group(2)
            
            direction_match = re.search(r'direction\s*:\s*(\w+)', pin_body)
            direction = direction_match.group(1) if direction_match else "input"
            
            if direction == "output":
                output_pins.append(pin_name)
            else:
                input_pins.append(pin_name)
        
        # Extract delay (simplified)
        delay = 0.1  # Default, có thể parse từ timing tables
        
        # Create cell
        cell = LibraryCell(
            name=cell_name,
            function=function,
            area=area,
            delay=delay,
            input_pins=input_pins,
            output_pins=output_pins
        )
        library.add_cell(cell)
    
    return library
```

**Sử dụng:**
```python
from core.technology_mapping.library_loader import load_liberty_library

library = load_liberty_library("techlibs/asic/standard_cells.lib")
mapper = TechnologyMapper(library)
```

---

### **Option 2: Load từ JSON Format**

**Tạo JSON library format:**

```json
{
  "name": "standard_cells",
  "cells": [
    {
      "name": "INV",
      "function": "NOT(A)",
      "area": 1.0,
      "delay": 0.1,
      "input_pins": ["A"],
      "output_pins": ["Y"]
    },
    {
      "name": "NAND2",
      "function": "NAND(A,B)",
      "area": 1.2,
      "delay": 0.15,
      "input_pins": ["A", "B"],
      "output_pins": ["Y"]
    }
  ]
}
```

**Function load:**

```python
import json
from typing import Dict, Any
from .technology_mapping import TechnologyLibrary, LibraryCell

def load_json_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from JSON file.
    
    Args:
        file_path: Path to .json file
        
    Returns:
        TechnologyLibrary object
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    library = TechnologyLibrary(data.get('name', 'loaded_library'))
    
    for cell_data in data.get('cells', []):
        cell = LibraryCell(
            name=cell_data['name'],
            function=cell_data['function'],
            area=cell_data['area'],
            delay=cell_data['delay'],
            input_pins=cell_data['input_pins'],
            output_pins=cell_data['output_pins']
        )
        library.add_cell(cell)
    
    return library
```

---

### **Option 3: Load từ Verilog Format (.v)**

**Parse Verilog cells:**

```python
def load_verilog_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from Verilog file.
    
    Args:
        file_path: Path to .v file
        
    Returns:
        TechnologyLibrary object
    """
    library = TechnologyLibrary("verilog_library")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse module definitions
    # Pattern: module CELL_NAME(...) ... endmodule
    module_pattern = r'module\s+(\w+)\s*\([^)]*\)\s*;([^;]+)endmodule'
    
    for match in re.finditer(module_pattern, content, re.DOTALL):
        cell_name = match.group(1)
        cell_body = match.group(2)
        
        # Extract function from assign statements
        # Simplified parsing
        function = cell_name  # Default
        
        # Create cell with default values
        cell = LibraryCell(
            name=cell_name,
            function=function,
            area=1.0,  # Default
            delay=0.1,  # Default
            input_pins=[],  # Parse from module ports
            output_pins=[]
        )
        library.add_cell(cell)
    
    return library
```

---

## 🎯 **CẢI THIỆN TECHNOLOGY MAPPING**

### **Bước 1: Tạo Library Loader Module**

**File:** `core/technology_mapping/library_loader.py`

```python
"""
Library Loader for Technology Mapping

Hỗ trợ load thư viện từ nhiều format:
- Liberty (.lib)
- JSON (.json)
- Verilog (.v)
"""

import os
import json
import re
from typing import Dict, List, Any, Optional
from .technology_mapping import TechnologyLibrary, LibraryCell

def load_library(file_path: str, library_type: Optional[str] = None) -> TechnologyLibrary:
    """
    Load technology library from file.
    
    Args:
        file_path: Path to library file
        library_type: "liberty", "json", "verilog", or None (auto-detect)
        
    Returns:
        TechnologyLibrary object
    """
    if library_type is None:
        # Auto-detect from extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.lib':
            library_type = 'liberty'
        elif ext == '.json':
            library_type = 'json'
        elif ext == '.v':
            library_type = 'verilog'
        else:
            raise ValueError(f"Unknown library format: {ext}")
    
    if library_type == 'liberty':
        return load_liberty_library(file_path)
    elif library_type == 'json':
        return load_json_library(file_path)
    elif library_type == 'verilog':
        return load_verilog_library(file_path)
    else:
        raise ValueError(f"Unsupported library type: {library_type}")

def load_liberty_library(file_path: str) -> TechnologyLibrary:
    """Load from Liberty format."""
    # Implementation như trên
    pass

def load_json_library(file_path: str) -> TechnologyLibrary:
    """Load from JSON format."""
    # Implementation như trên
    pass

def load_verilog_library(file_path: str) -> TechnologyLibrary:
    """Load from Verilog format."""
    # Implementation như trên
    pass
```

---

### **Bước 2: Update CLI để Load từ File**

**File:** `cli/vector_shell.py`

**Sửa function `_run_technology_mapping`:**

```python
def _run_technology_mapping(self, parts):
    """Chạy technology mapping."""
    if not parts or len(parts) < 2:
        print("Usage: techmap <strategy> [library_file]")
        print("Strategies: area, delay, balanced")
        print("Library: path to .lib or .json file (optional)")
        return
    
    strategy = parts[1].lower()
    library_path = parts[2] if len(parts) > 2 else None
    
    try:
        from core.technology_mapping.technology_mapping import TechnologyMapper, LogicNode
        from core.technology_mapping.library_loader import load_library, create_standard_library
        
        # Load library
        if library_path and os.path.exists(library_path):
            print(f"[INFO] Loading library from: {library_path}")
            library = load_library(library_path)
        else:
            print("[INFO] Using default standard library")
            library = create_standard_library()  # Fallback to hardcoded
        
        mapper = TechnologyMapper(library)
        
        # ... rest of mapping code
```

---

## 📊 **SO SÁNH**

| Cách | Ưu điểm | Nhược điểm |
|------|---------|------------|
| **Hardcoded** | ✅ Đơn giản, nhanh | ❌ Không mở rộng được |
| **Liberty (.lib)** | ✅ Industry standard | ⚠️ Phức tạp, cần parser |
| **JSON** | ✅ Dễ parse, linh hoạt | ⚠️ Không phải standard |
| **Verilog (.v)** | ✅ Dễ hiểu | ⚠️ Thiếu timing info |

---

## ✅ **KHUYẾN NGHỊ**

### **Hiện tại:**
- Technology mapping dùng **hardcoded library**
- **KHÔNG load từ `techlibs/` folder**

### **Cải thiện:**
1. **Tạo library loader module** để load từ file
2. **Hỗ trợ Liberty format** (industry standard)
3. **Hỗ trợ JSON format** (dễ dùng)
4. **Update CLI** để cho phép chọn library file

### **Implementation Priority:**
1. ✅ **JSON loader** - Dễ nhất, nhanh nhất
2. ⚠️ **Liberty loader** - Industry standard, phức tạp hơn
3. ⚠️ **Verilog loader** - Cần parse phức tạp

---

*Tài liệu này giải thích cách technology mapping load thư viện và đề xuất cải thiện*

