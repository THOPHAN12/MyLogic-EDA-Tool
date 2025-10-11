# 🗺️ **TECHNOLOGY MAPPING MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các thuật toán technology mapping cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `technology_mapping.py`**
- **Chức năng**: Map generic logic network sang thư viện công nghệ cụ thể (standard cells/LUTs)
- **Thuật toán**: Library-based mapping, chọn cell tốt nhất theo tiêu chí (area/delay/balanced)
- **Ứng dụng**: Tối ưu theo công nghệ mục tiêu, chuẩn bị cho backend (placement, routing)

## 🎯 **TECHNOLOGY MAPPING ALGORITHMS**

### **Library Mapping (API overview):**
```python
class TechnologyLibrary:
    def add_cell(cell: LibraryCell) -> None
    def get_cells_for_function(function: str) -> List[LibraryCell]
    def get_best_cell_for_function(function: str, optimization_target: str)

class TechnologyMapper:
    def __init__(self, library: TechnologyLibrary)
    def add_logic_node(node: LogicNode) -> None
    def perform_technology_mapping(strategy: str) -> Dict[str, Any]  # "area_optimal" | "delay_optimal" | "balanced"
    def get_mapping_statistics() -> Dict[str, Any]
    def print_mapping_report(results: Dict[str, Any]) -> None
```

### **Gate Mapping (core idea):**
```python
def map_function(function: str, library: TechnologyLibrary, target: str):
    # 1) Tra cứu các cell hỗ trợ function (function_map)
    # 2) Chọn cell tối ưu theo target: area | delay | balanced
    # 3) Gán cell cho LogicNode và lưu chi phí (area/delay/weighted)
```

## 🏭 **SUPPORTED TECHNOLOGIES**

### **1. Standard Cell Libraries:**
- **NAND/NOR gates**: Universal logic
- **AND/OR gates**: Basic logic
- **XOR gates**: Arithmetic logic
- **Multiplexers**: Selection logic

### **2. FPGA Technologies:**
- **LUT mapping**: Look-up table optimization
- **CLB mapping**: Configurable logic blocks
- **DSP mapping**: Digital signal processing

### **3. ASIC Technologies:**
- **CMOS gates**: Complementary logic
- **Custom cells**: Application-specific
- **Memory cells**: Storage elements

## 🚀 **USAGE**

```python
from core.technology_mapping.technology_mapping import (
    TechnologyLibrary, LibraryCell,
    TechnologyMapper, LogicNode, create_standard_library
)

# 1) Tạo/cấp thư viện công nghệ
library = create_standard_library()  # hoặc tự add_cell(...) vào TechnologyLibrary

# 2) Tạo mapper và network logic
mapper = TechnologyMapper(library)
mapper.add_logic_node(LogicNode("n1", "AND(A,B)", ["a","b"], "temp1"))
mapper.add_logic_node(LogicNode("n2", "OR(C,D)",  ["c","d"], "temp2"))
mapper.add_logic_node(LogicNode("n3", "XOR(temp1,temp2)", ["temp1","temp2"], "out"))

# 3) Chọn chiến lược và thực hiện mapping
results = mapper.perform_technology_mapping("balanced")
mapper.print_mapping_report(results)
```

## 📊 **MAPPING METRICS**

- **Area**: Cell count and size
- **Delay**: Gate delays and paths
- **Power**: Switching activity
- **Timing**: Setup/hold constraints

## 🎯 **MAPPING STRATEGIES**

### **1. Area-Optimized:**
- Minimize cell count
- Use smallest cells
- Optimize for area

### **2. Delay-Optimized:**
- Minimize critical path
- Use fastest cells
- Optimize for speed

### **3. Balanced:**
- Trade-off area vs delay
- Use balanced cells
- Optimize for both

Ghi chú: Chi phí balanced mặc định là `area + delay * 10` (có thể điều chỉnh trong code nếu cần).

## 📚 **REFERENCES**
- Technology mapping textbooks
- Library documentation
- EDA tool manuals

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
