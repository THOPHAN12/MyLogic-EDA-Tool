# Tính Năng Mới - MyLogic EDA Tool

## Tổng Quan

Các tính năng mới đã được thêm vào MyLogic EDA Tool để hỗ trợ đầy đủ mục lục đồ án:

1. **BED (Boolean Expression Diagrams)** - CHƯƠNG 2
2. **Quine-McCluskey Algorithm** - CHƯƠNG 3.1.1
3. **AIG (And-Inverter Graph)** - CHƯƠNG 3.1.3
4. **4-bit Examples** - CHƯƠNG 5

---

## 1. Boolean Expression Diagrams (BED)

### Mô Tả
BED là một cấu trúc dữ liệu để biểu diễn các biểu thức Boolean, tương tự BDD nhưng linh hoạt hơn.

### Vị Trí Code
- **File**: `core/vlsi_cad/bed.py`
- **Class**: `BED`, `BEDNode`

### Các Thuật Toán

#### MK() - Make Node
Tạo node mới hoặc trả về node đã tồn tại (structural hashing).

```python
from core.vlsi_cad.bed import BED

bed = BED()
a = bed.create_variable("a")
b = bed.create_variable("b")
f = bed.create_and(a, b)
```

#### UP_ONE() - Upward Traversal Một Bước
Thay thế một biến bằng giá trị cụ thể và đơn giản hóa.

```python
f_up = bed.UP_ONE(f, "a", True)  # Thay a = True
```

#### UP_ALL() - Upward Traversal Toàn Bộ
Thay thế tất cả các biến và đơn giản hóa hoàn toàn.

```python
assignment = {"a": True, "b": False}
f_simplified = bed.UP_ALL(f, assignment)
```

### Sử Dụng Trong CLI

```bash
mylogic> bed create          # Tạo BED example
mylogic> bed up_one         # Demo UP_ONE
mylogic> bed up_all         # Demo UP_ALL
mylogic> bed compare        # So sánh với BDD
```

### So Sánh BED vs BDD

| Đặc điểm | BED | BDD |
|----------|-----|-----|
| Canonical form | Không bắt buộc | Bắt buộc |
| Linh hoạt | Cao | Trung bình |
| Hiệu quả | Tốt cho biểu thức phức tạp | Tốt cho hàm Boolean đơn giản |
| Ứng dụng | Verification, Synthesis | Logic optimization |

---

## 2. Quine-McCluskey Algorithm

### Mô Tả
Thuật toán Quine-McCluskey là một phương pháp Boolean minimization, tương tự Espresso nhưng đảm bảo tìm được minimal form.

### Vị Trí Code
- **File**: `core/optimization/quine_mccluskey.py`
- **Class**: `QuineMcCluskey`, `Minterm`, `Implicant`

### Các Bước Thuật Toán

1. **Tìm Prime Implicants**: Nhóm và kết hợp minterms
2. **Tìm Essential Prime Implicants**: Xác định các PI bắt buộc
3. **Cover Remaining Minterms**: Chọn minimal cover
4. **Generate Expression**: Tạo biểu thức Boolean tối giản

### Ví Dụ Sử Dụng

```python
from core.optimization.quine_mccluskey import QuineMcCluskey

qm = QuineMcCluskey()
# f(a,b) = Σ(0, 1, 3)
result = qm.minimize([0, 1, 3], num_vars=2, variable_names=['a', 'b'])
print(result['expression'])  # Output: minimized SOP form
```

### Sử Dụng Trong CLI

```bash
mylogic> quine 0,1,3                    # Minimize với minterms
mylogic> quine 0,1,2,5,6 3,7           # Với don't cares
mylogic> minimize 0,1,3                # Alias cho quine
```

### Kết Quả Trả Về

```python
{
    'expression': 'x0 | x1',           # Minimized expression
    'prime_implicants': 2,              # Số PI
    'essential_implicants': 1,         # Số essential PI
    'minimal_implicants': 1,           # Số PI trong minimal cover
    'minterms': 3,                     # Số minterms input
    'num_vars': 2,                     # Số biến
    'coverage': 100.0                  # % coverage
}
```

---

## 3. And-Inverter Graph (AIG)

### Mô Tả
AIG là một cấu trúc dữ liệu quan trọng trong logic synthesis, đặc biệt được sử dụng trong ABC. AIG chỉ sử dụng AND gates và inverters.

### Vị Trí Code
- **File**: `core/synthesis/aig.py`
- **Class**: `AIG`, `AIGNode`

### Đặc Điểm

- **Canonical Form**: Chỉ sử dụng AND và NOT
- **Structural Hashing**: Tự động loại bỏ duplicate nodes
- **Level Information**: Theo dõi logic depth
- **Verilog Export**: Chuyển đổi sang Verilog

### Ví Dụ Sử Dụng

```python
from core.synthesis.aig import AIG

aig = AIG()
a = aig.create_pi("a")
b = aig.create_pi("b")
c = aig.create_pi("c")

# Create logic: f = (a AND b) OR c
ab = aig.create_and(a, b)
f = aig.create_or(ab, c)  # OR được implement bằng De Morgan
aig.add_po(f)

# Get statistics
stats = aig.get_statistics()
print(stats)
```

### Sử Dụng Trong CLI

```bash
mylogic> aig create        # Tạo AIG example
mylogic> aig strash       # Demo structural hashing
mylogic> aig convert      # Chuyển sang Verilog
mylogic> aig stats        # Hiển thị statistics
```

### Structural Hashing

AIG tự động sử dụng structural hashing trong `create_and()`:

```python
ab1 = aig.create_and(a, b)
ab2 = aig.create_and(a, b)  # Reuse ab1, không tạo node mới
assert ab1 == ab2
```

### Verilog Export

```python
verilog_code = aig.to_verilog("module_name")
# Tạo Verilog module từ AIG
```

---

## 4. 4-bit Examples

### Mô Tả
Các ví dụ 4-bit được tạo để test synthesis và optimization algorithms.

### Files

#### `examples/4bit_adder.v`
- **Mô tả**: 4-bit ripple-carry adder
- **Sử dụng**: Test synthesis flow với arithmetic operations
- **Cấu trúc**: 4 full adder modules kết nối nối tiếp

#### `examples/4bit_multiplier.v`
- **Mô tả**: 4-bit unsigned multiplier
- **Sử dụng**: Test synthesis với partial products
- **Cấu trúc**: Partial product generation + addition

### Sử Dụng

```bash
# Load và synthesize
mylogic> read examples/4bit_adder.v
mylogic> synthesis aggressive
mylogic> stats

# Test với multiplier
mylogic> read examples/4bit_multiplier.v
mylogic> strash
mylogic> cse
mylogic> balance
```

---

## Tích Hợp Vào Synthesis Flow

### Các Tính Năng Mới Trong Pipeline

```
Input Verilog
    ↓
Parser
    ↓
[OPTIONAL] Quine-McCluskey Minimization  ← NEW
    ↓
Strash (hoặc AIG Strash)                  ← AIG support
    ↓
DCE
    ↓
CSE
    ↓
ConstProp
    ↓
Balance
    ↓
[OPTIONAL] BED Analysis                   ← NEW
    ↓
Technology Mapping
    ↓
Output
```

### Ví Dụ Workflow

```bash
# 1. Load design
mylogic> read examples/4bit_adder.v

# 2. Boolean minimization (optional)
mylogic> quine 0,1,2,3,4,5,6,7  # Nếu có truth table

# 3. Convert to AIG (optional)
mylogic> aig create

# 4. Standard synthesis
mylogic> synthesis aggressive

# 5. BED analysis (optional)
mylogic> bed compare

# 6. Export
mylogic> export optimized.json
```

---

## Testing

### Test BED

```bash
python -c "from core.vlsi_cad.bed import BED; bed = BED(); a = bed.create_variable('a'); b = bed.create_variable('b'); f = bed.create_and(a, b); print(bed.to_string(f))"
```

### Test Quine-McCluskey

```bash
python -c "from core.optimization.quine_mccluskey import QuineMcCluskey; qm = QuineMcCluskey(); result = qm.minimize([0,1,3], 2, ['a','b']); print(result['expression'])"
```

### Test AIG

```bash
python -c "from core.synthesis.aig import AIG; aig = AIG(); a = aig.create_pi('a'); b = aig.create_pi('b'); f = aig.create_and(a, b); print(aig.count_nodes())"
```

---

## Tài Liệu Tham Khảo

1. **BED**: Boolean Expression Diagrams - Research papers on BED
2. **Quine-McCluskey**: Classic two-level minimization algorithm
3. **AIG**: ABC (Berkeley Logic Synthesis Tool) - AIG structure
4. **4-bit Examples**: Standard test cases for synthesis tools

---

## Kết Luận

Các tính năng mới đã được tích hợp đầy đủ vào MyLogic EDA Tool, hỗ trợ:
- ✅ CHƯƠNG 2: BED implementation
- ✅ CHƯƠNG 3.1.1: Quine-McCluskey (Boolean minimization)
- ✅ CHƯƠNG 3.1.3: AIG structure
- ✅ CHƯƠNG 5: 4-bit examples

Tất cả các tính năng đều có thể sử dụng qua CLI và có thể tích hợp vào synthesis flow.

