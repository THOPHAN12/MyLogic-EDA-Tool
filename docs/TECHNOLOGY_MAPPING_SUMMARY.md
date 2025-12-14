# Technology Mapping Flow - Tóm Tắt

## 🔄 Luồng Technology Mapping

Technology Mapping là bước cuối cùng trong synthesis flow, chuyển đổi logic network thành technology cells từ library.

### Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    TECHNOLOGY MAPPING FLOW                  │
└─────────────────────────────────────────────────────────────┘

1. INPUT: Optimized Netlist
   └─> Sau synthesis (Strash, DCE, CSE, ConstProp, Balance)
   └─> Logic network với Boolean functions

2. LOAD LIBRARY
   └─> ASIC: techlibs/asic/standard_cells.lib
   └─> FPGA: techlibs/fpga/common/cells.lib
   └─> Standard: create_standard_library()

3. SELECT STRATEGY
   ├─> area_optimal: Minimize area
   ├─> delay_optimal: Minimize delay
   └─> balanced: Balance area + delay

4. PROCESS NODES
   ├─> Extract function từ node
   ├─> Normalize function (A, B, C, ...)
   ├─> Find matching cells trong library
   └─> Select best cell (dựa trên strategy)

5. MAP NODES
   └─> Gán cell cho mỗi node
   └─> Tính cost (area/delay/weighted)

6. CALCULATE STATISTICS
   ├─> Total area
   ├─> Total delay
   ├─> Cell usage
   └─> Mapping success rate

7. OUTPUT: Mapped Netlist
   └─> Nodes đã được map vào technology cells
   └─> Ready cho placement & routing
```

## 📊 Các Bước Chi Tiết

### Bước 1: Load Optimized Netlist

**Input:** Netlist sau synthesis flow
```python
netlist = {
    'nodes': {
        'n1': {'type': 'AND', 'inputs': ['a', 'b'], ...},
        'n2': {'type': 'OR', 'inputs': ['c', 'd'], ...},
        ...
    }
}
```

### Bước 2: Load Technology Library

**Supported Libraries:**
- **ASIC**: `techlibs/asic/standard_cells.lib` (Liberty format)
- **FPGA Common**: `techlibs/fpga/common/cells.lib` (DFF cells)
- **FPGA Vendors**: ice40, xilinx, lattice, intel, gowin, anlogic
- **Standard**: Built-in library với 23 cells

**Library Structure:**
```python
library = TechnologyLibrary("standard_cells")
library.cells = {
    'AND2': LibraryCell('AND2', 'AND(A,B)', area=1.5, delay=0.2, ...),
    'OR2': LibraryCell('OR2', 'OR(A,B)', area=1.5, delay=0.2, ...),
    ...
}
library.function_map = {
    'AND(A,B)': ['AND2', 'AND2X1', 'AND2X2'],
    'OR(A,B)': ['OR2', 'OR2X1', 'OR2X2'],
    ...
}
```

### Bước 3: Select Mapping Strategy

#### **Area-Optimal**
- **Cost**: `cell.area`
- **Goal**: Minimize total area
- **Use case**: Chip size constrained

#### **Delay-Optimal**
- **Cost**: `cell.delay`
- **Goal**: Minimize total delay
- **Use case**: Timing critical

#### **Balanced**
- **Cost**: `area + delay * 10`
- **Goal**: Balance area và delay
- **Use case**: General purpose

### Bước 4: Process Each Node

#### **4.1. Extract Function**
```python
node = {'type': 'AND', 'inputs': ['a', 'b']}
function = "AND(a,b)"  # Raw function
```

#### **4.2. Normalize Function**
```python
# Input: "AND(a,b)" hoặc "AND(C,D)" hoặc "AND(temp1,temp2)"
# Output: "AND(A,B)"  # Canonical form

normalize_function("AND(a,b)") → "AND(A,B)"
normalize_function("AND(C,D)") → "AND(A,B)"
normalize_function("AND(temp1,temp2)") → "AND(A,B)"
```

#### **4.3. Find Matching Cells**
```python
normalized_func = "AND(A,B)"
matching_cells = library.function_map.get(normalized_func, [])
# Result: ['AND2', 'AND2X1', 'AND2X2']
```

#### **4.4. Select Best Cell**

**Area-Optimal:**
```python
best_cell = min(cells, key=lambda c: c.area)
```

**Delay-Optimal:**
```python
best_cell = min(cells, key=lambda c: c.delay)
```

**Balanced:**
```python
best_cell = min(cells, key=lambda c: c.area + c.delay * 10)
```

### Bước 5: Map Node to Cell

```python
node.mapped_cell = best_cell
node.mapping_cost = best_cell.area  # hoặc delay, hoặc weighted cost
```

### Bước 6: Calculate Statistics

- **Total Area**: Sum of all mapped cell areas
- **Total Delay**: Sum of all mapped cell delays
- **Cell Usage**: Count of each cell type used
- **Mapping Success Rate**: Mapped nodes / Total nodes

### Bước 7: Generate Report

**Report includes:**
- Mapping strategy
- Total nodes vs mapped nodes
- Total area/delay
- Cell usage breakdown
- Node-to-cell mapping details

## 🎯 Example Flow

### Input Verilog
```verilog
module test_techmap(
    input a, b, c, d,
    output out1, out2
);
    wire temp1 = a & b;
    wire temp2 = c | d;
    assign out1 = temp1 ^ temp2;
    assign out2 = (a & b) | (c & d);
endmodule
```

### After Synthesis
- Node `and_0`: `AND(a,b)` → temp1
- Node `or_1`: `OR(c,d)` → temp2
- Node `xor_2`: `XOR(temp1,temp2)` → out1
- Node `or_3`: `OR(and_0, or_1)` → out2

### Technology Mapping Process

1. **Node `and_0`: AND(a,b)**
   - Normalize: `AND(a,b)` → `AND(A,B)`
   - Find: `['AND2', 'AND2X1', 'AND2X2']`
   - Select (area): `AND2X1` (area=1.3)
   - Map: `and_0` → `AND2X1`

2. **Node `or_1`: OR(c,d)**
   - Normalize: `OR(c,d)` → `OR(A,B)`
   - Find: `['OR2', 'OR2X1', 'OR2X2']`
   - Select (area): `OR2X1` (area=1.3)
   - Map: `or_1` → `OR2X1`

3. **Node `xor_2`: XOR(temp1,temp2)**
   - Normalize: `XOR(temp1,temp2)` → `XOR(A,B)`
   - Find: `['XOR2', 'XOR2X1']`
   - Select: `XOR2` (area=2.0, delay=0.25)
   - Map: `xor_2` → `XOR2`

### Result
- **Total Area**: 4.6
- **Total Delay**: 0.75
- **Mapping Success**: 100%

## 📈 Performance

| Strategy | Optimization | Use Case |
|----------|-------------|----------|
| **Area-Optimal** | Minimize area | Chip size constrained |
| **Delay-Optimal** | Minimize delay | Timing critical |
| **Balanced** | Balance area/delay | General purpose |

## 🔧 Usage

### Command Line
```bash
python mylogic.py
mylogic> read examples/test_techmap.v
mylogic> synthesis standard
mylogic> techmap balanced standard
```

### Python API
```python
from core.technology_mapping.technology_mapping import (
    TechnologyMapper, create_standard_library, LogicNode
)

library = create_standard_library()
mapper = TechnologyMapper(library)
# ... add nodes ...
results = mapper.perform_technology_mapping("balanced")
mapper.print_mapping_report(results)
```

## 📝 Notes

- Function normalization là critical để match chính xác
- Library phải có đầy đủ cells cần thiết
- Complex functions (nested expressions) có thể không được map
- Technology mapping chỉ map được nodes có function match với library

