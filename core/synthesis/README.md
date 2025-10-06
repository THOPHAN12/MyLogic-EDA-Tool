# 🔧 **SYNTHESIS MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các thuật toán logic synthesis cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `strash.py`**
- **Chức năng**: Structural hashing - loại bỏ duplicate logic
- **Thuật toán**: Hash-based structural analysis
- **Ứng dụng**: Optimization trong synthesis flow

### **2. `synthesis_flow.py`**
- **Chức năng**: Main synthesis flow controller
- **Thuật toán**: Orchestrates synthesis steps
- **Ứng dụng**: Core synthesis engine

## 🎯 **SYNTHESIS ALGORITHMS**

### **Structural Hashing (Strash):**
```python
# Loại bỏ duplicate logic structures
def structural_hash(netlist):
    # Hash-based duplicate detection
    # Merge identical structures
    # Optimize gate count
```

### **Synthesis Flow:**
```python
# Orchestrates synthesis steps
def synthesis_flow(verilog_file):
    # 1. Parse Verilog
    # 2. Structural analysis
    # 3. Logic optimization
    # 4. Technology mapping
```

## 🚀 **USAGE**

```python
from core.synthesis.strash import StructuralHasher
from core.synthesis.synthesis_flow import SynthesisFlow

# Structural hashing
hasher = StructuralHasher()
optimized_netlist = hasher.optimize(netlist)

# Synthesis flow
synthesis = SynthesisFlow()
result = synthesis.run_synthesis("input.v")
```

## 📚 **REFERENCES**
- YosysHQ Documentation
- Logic Synthesis textbooks
- EDA tool documentation

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
