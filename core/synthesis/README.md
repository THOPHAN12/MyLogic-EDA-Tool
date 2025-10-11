# 🔧 **SYNTHESIS MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các thuật toán logic synthesis cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `strash.py`**
- **Chức năng**: Structural hashing - loại bỏ duplicate logic
- **Thuật toán**: Hash-based structural analysis (canonical key bởi gate type + inputs đã sort)
- **Ứng dụng**: Giảm số node bằng cách hợp nhất các cấu trúc trùng nhau

### **2. `synthesis_flow.py`**
- **Chức năng**: Orchestrator cho toàn bộ logic synthesis pipeline
- **Thuật toán**: Gọi tuần tự các bước tối ưu hóa: Strash → DCE → CSE → ConstProp → Balance
- **Ứng dụng**: Core synthesis engine cho netlist nội bộ

## 🎯 **SYNTHESIS ALGORITHMS**

### **Structural Hashing (Strash):**
```python
# Remove duplicate logic by hashing canonical node signatures
def apply_strash(netlist):
    # 1) Build a hash from (gate_type, sorted_inputs)
    # 2) If signature exists, reuse existing node (merge)
    # 3) Update wires / fanins accordingly
```

### **Synthesis Flow:**
```python
# Orchestrates logic optimizations on an internal netlist
def run_complete_synthesis(netlist, level="standard"):
    # 1) Strash (remove duplicates)
    # 2) DCE (remove dead logic)
    # 3) CSE (share subexpressions)
    # 4) ConstProp (propagate constants)
    # 5) Balance (rebalance associative gates)
```

## 🚀 **USAGE**

```python
from core.synthesis.strash import apply_strash
from core.synthesis.synthesis_flow import SynthesisFlow, run_complete_synthesis

# Structural hashing (API tiện dụng)
optimized_netlist = apply_strash(netlist)

# Complete synthesis flow (class-based)
flow = SynthesisFlow()
netlist2 = flow.run_complete_synthesis(netlist, optimization_level="standard")

# Hoặc dùng convenience function
netlist3 = run_complete_synthesis(netlist, optimization_level="aggressive")
```

## 📚 **REFERENCES**
- YosysHQ Documentation
- Logic Synthesis textbooks
- EDA tool documentation

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
