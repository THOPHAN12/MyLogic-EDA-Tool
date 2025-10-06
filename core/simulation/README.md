# 🎮 **SIMULATION MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các simulation engines cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `arithmetic_simulation.py`**
- **Chức năng**: Vector arithmetic simulation engine
- **Thuật toán**: Vector operations, arithmetic simulation
- **Ứng dụng**: Multi-bit arithmetic simulation

## 🎯 **SIMULATION ALGORITHMS**

### **Vector Arithmetic Simulation:**
```python
# Vector operations
def vector_add(a: VectorValue, b: VectorValue) -> VectorValue
def vector_multiply(a: VectorValue, b: VectorValue) -> VectorValue
def vector_subtract(a: VectorValue, b: VectorValue) -> VectorValue
def vector_divide(a: VectorValue, b: VectorValue) -> VectorValue

# Bitwise operations
def vector_and(a: VectorValue, b: VectorValue) -> VectorValue
def vector_or(a: VectorValue, b: VectorValue) -> VectorValue
def vector_xor(a: VectorValue, b: VectorValue) -> VectorValue
def vector_not(a: VectorValue) -> VectorValue

# Netlist simulation
def simulate_arithmetic_netlist(netlist, inputs) -> Dict[str, VectorValue]
```

### **VectorValue Class:**
```python
class VectorValue:
    def __init__(self, value: int, width: int)
    def to_int(self) -> int
    def to_binary(self) -> str
    def __repr__(self)
```

## 🚀 **USAGE**

### **1. Vector Operations:**
```python
from core.simulation.arithmetic_simulation import VectorValue, vector_add

# Create vector values
a = VectorValue(5, 4)  # 5 in 4-bit
b = VectorValue(3, 4)  # 3 in 4-bit

# Perform operations
result = vector_add(a, b)
print(f"Result: {result}")  # VectorValue(1000, width=5)
```

### **2. Netlist Simulation:**
```python
from core.simulation.arithmetic_simulation import simulate_arithmetic_netlist

# Define netlist
netlist = {
    'inputs': ['a', 'b'],
    'outputs': ['sum'],
    'nodes': [
        {'id': 'add1', 'type': 'ADD', 'fanins': [('a', False), ('b', False)]}
    ]
}

# Define inputs
inputs = {'a': 5, 'b': 3}

# Simulate
outputs = simulate_arithmetic_netlist(netlist, inputs)
print(f"Sum: {outputs['sum']}")
```

## 📊 **SUPPORTED OPERATIONS**

### **1. Arithmetic Operations:**
- **ADD**: Addition
- **SUB**: Subtraction
- **MULT**: Multiplication
- **DIV**: Division

### **2. Logic Operations:**
- **AND**: Bitwise AND
- **OR**: Bitwise OR
- **XOR**: Bitwise XOR
- **NOT**: Bitwise NOT

### **3. Buffer Operations:**
- **BUF**: Buffer
- **CONST**: Constant

## 🎯 **SIMULATION FEATURES**

### **1. Vector Support:**
- Multi-bit vector operations
- Automatic width calculation
- Overflow/underflow handling

### **2. Netlist Support:**
- Topological simulation
- Fanin/fanout handling
- Inversion support

### **3. Error Handling:**
- Division by zero detection
- Missing input handling
- Invalid operation handling

## 📚 **REFERENCES**
- Digital simulation textbooks
- EDA tool documentation
- Vector arithmetic papers

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
