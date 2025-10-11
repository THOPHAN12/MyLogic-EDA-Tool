# 🎮 **SIMULATION MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các simulation engines cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `arithmetic_simulation.py`**
- **Chức năng**: Vector arithmetic simulation engine
- **Thuật toán**: Vector operations, arithmetic simulation
- **Ứng dụng**: Multi-bit arithmetic simulation

---

## 🧩 Kiến trúc & Dữ liệu

- **VectorValue**: đại diện một giá trị n-bit có mask an toàn theo `width`.
  - `value: int` luôn được mask với `(1 << width) - 1` để không tràn ngoài độ rộng.
  - `width: int` là số bit của giá trị.
  - Phương thức tiện ích:
    - `to_int()` trả về số nguyên đã mask
    - `to_binary()` trả về chuỗi nhị phân đủ `width`
    - `__repr__()` hiển thị dạng gọn cho debug

- Quy tắc tính độ rộng kết quả:
  - Cộng/Trừ: `max(a.width, b.width) + 1` (thêm 1 bit cho carry/borrow)
  - Nhân: `a.width + b.width`
  - Chia: giữ `a.width` (số bị chia)
  - Bitwise (AND/OR/XOR/NOT): dùng `max(a.width, b.width)`; riêng `NOT` giữ `a.width`

---

## 🔧 API chi tiết (arithmetic_simulation.py)

- Arithmetic operations:
  - `vector_add(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_subtract(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_multiply(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_divide(a: VectorValue, b: VectorValue) -> VectorValue`
    - Chia nguyên; width = `a.width`; lỗi nếu chia cho 0

- Bitwise operations:
  - `vector_and(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_or(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_xor(a: VectorValue, b: VectorValue) -> VectorValue`
  - `vector_not(a: VectorValue) -> VectorValue`
    - Đảo bit an toàn theo mask `(1 << a.width) - 1`

- Netlist simulation:
  - `simulate_arithmetic_netlist(netlist, inputs) -> Dict[str, VectorValue]`
    - Chuẩn hóa input (int, chuỗi nhị phân, danh sách bool, hoặc `VectorValue`)
    - Thực thi các node theo thứ tự hợp lệ, trả về map `tên_output -> VectorValue`

---

## 🧠 Luồng mô phỏng (tóm tắt)

1) Chuẩn hóa input sang `VectorValue` theo độ rộng yêu cầu  
2) Duyệt các node theo thứ tự hợp lệ (topological hoặc thứ tự định nghĩa hợp lệ)  
3) Với từng node, gọi hàm toán học/bitwise tương ứng  
4) Ghi nhận giá trị trung gian và ánh xạ ra các output cuối cùng  

---

## ⚠️ Edge cases & Lỗi thường gặp

- Division by zero: `vector_divide` sẽ raise `ValueError("Division by zero")`
- Overflow/underflow: mọi kết quả đều được mask theo `width` đã tính để tránh tràn
- Độ rộng không đồng nhất: các phép toán tự chọn `width` phù hợp (xem quy tắc ở trên)
- Định dạng input: nếu là chuỗi nhị phân, cần đúng độ dài hoặc sẽ được chuẩn hóa/mask

---

## 🧪 Ví dụ nâng cao

```python
from core.simulation.arithmetic_simulation import (
    VectorValue,
    vector_add, vector_subtract, vector_multiply, vector_divide,
    vector_and, vector_or, vector_xor
)

# Create operands (4-bit)
a = VectorValue(0b1011, 4)  # 11
b = VectorValue(0b0011, 4)  # 3

# Arithmetic
sum_ab   = vector_add(a, b)      # width 5
diff_ab  = vector_subtract(a, b) # width 5
prod_ab  = vector_multiply(a, b) # width 8
quot_ab  = vector_divide(a, b)   # width 4

# Bitwise (width 4)
and_ab = vector_and(a, b)
or_ab  = vector_or(a, b)
xor_ab = vector_xor(a, b)

print(sum_ab.to_binary(), prod_ab.to_binary(), and_ab.to_binary())
```

---

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
