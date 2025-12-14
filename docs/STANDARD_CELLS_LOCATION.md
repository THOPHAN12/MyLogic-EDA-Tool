# Standard Cells Location - MyLogic EDA Tool

## 📍 Vị Trí Standard Cells

Standard cells trong MyLogic EDA Tool được định nghĩa ở **2 nơi chính**:

### 1. **Code Python (Hardcoded Library)**

**File:** `core/technology_mapping/technology_mapping.py`

**Function:** `create_standard_library()` (dòng 355-403)

**Mô tả:** Đây là standard library được hardcode trong Python code, chứa 23 cells cơ bản.

**Cells bao gồm:**
- **Basic gates:** INV (NOT), BUF
- **2-input gates:** NAND2, NOR2, AND2, OR2, XOR2, XNOR2
- **3-input gates:** NAND3, NOR3, AND3, OR3, XOR3
- **4-input gates:** AND4, OR4, NAND4, NOR4
- **Complex gates:** AOI21, OAI21, AOI22, OAI22, AOI211, OAI211

**Code:**
```python
def create_standard_library() -> TechnologyLibrary:
    library = TechnologyLibrary("standard_cells")
    
    gates = [
        ("INV", "NOT", 1.0, 0.1, ["A"], ["Y"]),
        ("BUF", "BUF", 1.0, 0.05, ["A"], ["Y"]),
        ("NAND2", "NAND(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        ("OR2", "OR(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        ("XOR2", "XOR(A,B)", 2.0, 0.25, ["A", "B"], ["Y"]),
        # ... và nhiều cells khác
    ]
    
    for name, function, area, delay, inputs, outputs in gates:
        cell = LibraryCell(name, function, area, delay, inputs, outputs)
        library.add_cell(cell)
    
    return library
```

**Khi nào sử dụng:**
- Fallback khi không load được library từ file
- Testing và demo
- Default library khi không chỉ định library cụ thể

### 2. **Library Files (techlibs/)**

#### **2.1. ASIC Standard Cells**

**Location:** `techlibs/asic/`

**Files:**
- `standard_cells.lib` - Liberty format (industry standard)
- `standard_cells.json` - JSON format (custom format)

**Mô tả:** Standard cells cho ASIC design, có thể chứa nhiều cells hơn và có timing information chi tiết hơn.

**Usage:**
```python
from core.technology_mapping.technology_mapping import load_library_from_file

library = load_library_from_file("techlibs/asic/standard_cells.lib")
```

#### **2.2. FPGA Common Cells**

**Location:** `techlibs/fpga/common/`

**File:** `cells.lib` (Liberty format)

**Mô tả:** Chứa **DFF cells** (flip-flops) cho FPGA, không phải standard logic gates.

**Cells trong cells.lib:**
- DFF_N, DFF_P (basic flip-flops)
- DFF_NN0, DFF_NN1, DFF_NP0, DFF_NP1 (with reset/preset)
- DFF_PN0, DFF_PN1, DFF_PP0, DFF_PP1 (various configurations)

**Lưu ý:** File này chỉ có DFF cells, không có logic gates (AND, OR, XOR, etc.)

#### **2.3. FPGA Vendor Libraries**

**Locations:**
- `techlibs/fpga/anlogic/` - Anlogic FPGA
- `techlibs/fpga/gowin/` - Gowin FPGA
- `techlibs/fpga/ice40/` - Lattice iCE40
- `techlibs/fpga/intel/` - Intel/Altera FPGA
- `techlibs/fpga/lattice/` - Lattice FPGA
- `techlibs/fpga/xilinx/` - Xilinx FPGA

**Mô tả:** Các vendor-specific libraries cho FPGA synthesis.

## 🔍 Cách Tìm Standard Cells

### Method 1: Check Code

```python
from core.technology_mapping.technology_mapping import create_standard_library

library = create_standard_library()
print(f"Library: {library.name}")
print(f"Total cells: {len(library.cells)}")
print("Cells:", list(library.cells.keys()))
```

### Method 2: Check Files

```bash
# ASIC standard cells
ls techlibs/asic/

# FPGA common cells (DFF only)
ls techlibs/fpga/common/

# FPGA vendor libraries
ls techlibs/fpga/
```

### Method 3: Load and Inspect

```python
from core.technology_mapping.technology_mapping import load_library_from_file

# Load ASIC library
library = load_library_from_file("techlibs/asic/standard_cells.lib")
print(f"Cells: {list(library.cells.keys())[:10]}")
```

## 📊 So Sánh

| Source | Location | Format | Cells | Use Case |
|--------|----------|--------|-------|----------|
| **Code** | `core/technology_mapping/technology_mapping.py` | Python | 23 gates | Fallback, testing |
| **ASIC** | `techlibs/asic/standard_cells.lib` | Liberty | Full library | ASIC synthesis |
| **FPGA Common** | `techlibs/fpga/common/cells.lib` | Liberty | DFF only | FPGA flip-flops |
| **FPGA Vendors** | `techlibs/fpga/{vendor}/` | Various | Vendor-specific | FPGA synthesis |

## 🎯 Khi Nào Dùng Cái Nào?

### **Standard Library (Code)**
- ✅ Quick testing
- ✅ Demo và examples
- ✅ Fallback khi không có library file
- ✅ Development

### **ASIC Library (File)**
- ✅ ASIC design flow
- ✅ Industry-standard cells
- ✅ Detailed timing information
- ✅ Production use

### **FPGA Libraries (Files)**
- ✅ FPGA synthesis
- ✅ Vendor-specific optimization
- ✅ DFF mapping
- ✅ FPGA placement & routing

## 📝 Notes

1. **Standard library trong code** là hardcoded, dễ modify nhưng không flexible
2. **Library files** có thể chứa nhiều cells hơn và có timing info chi tiết
3. **FPGA common/cells.lib** chỉ có DFF, không có logic gates
4. **Vendor libraries** có thể có format khác nhau (Verilog, Liberty, JSON)

## 🔧 Modify Standard Cells

### Thêm cells vào standard library:

Edit `core/technology_mapping/technology_mapping.py`:

```python
def create_standard_library() -> TechnologyLibrary:
    library = TechnologyLibrary("standard_cells")
    
    gates = [
        # ... existing cells ...
        ("NEW_CELL", "NEW_FUNC(A,B)", 2.0, 0.2, ["A", "B"], ["Y"]),  # Add here
    ]
    
    # ... rest of code ...
```

### Thêm cells vào library file:

Edit `techlibs/asic/standard_cells.lib` hoặc `standard_cells.json` theo format tương ứng.

