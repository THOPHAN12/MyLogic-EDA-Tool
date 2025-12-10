# Verilog Parser - Modular Architecture

## 📚 Tổng Quan

Parser Verilog đã được refactor từ 1 file lớn (1228 dòng) thành cấu trúc modular, dễ đọc và maintain.

## 🏗️ Cấu Trúc Module

```
verilog/
├── __init__.py              # Export parse_verilog
├── README.md                # Documentation này
├── constants.py             # Regex patterns, hằng số (200 dòng)
├── tokenizer.py             # Tokenization logic (150 dòng)
├── node_builder.py          # Builder pattern cho nodes (250 dòng)
├── parser.py                # Main parser logic (400 dòng)
└── operations/              # Operation parsers
    ├── __init__.py         # Export operations
    ├── arithmetic.py       # +, -, *, /, % (120 dòng)
    ├── bitwise.py          # &, |, ^, ~, NAND, NOR, XNOR (150 dòng)
    ├── logical.py          # &&, ||, ! (120 dòng)
    ├── comparison.py       # ==, !=, <, >, <=, >= (100 dòng)
    ├── shift.py            # <<, >>, <<<, >>> (120 dòng)
    └── special.py          # ternary, concat, slice (180 dòng)
```

## 📖 Chi Tiết Modules

### 1. `constants.py` - Hằng Số và Patterns

**Chức năng:**
- Định nghĩa tất cả regex patterns (compiled để tăng performance)
- Operator precedence
- Node type mapping
- Configuration constants

**Lợi ích:**
- Tất cả regex ở 1 chỗ, dễ maintain
- Compiled regex -> faster parsing
- Dễ thêm operators mới

**Example:**
```python
from .constants import OPERATOR_TO_NODE_TYPE, ARITHMETIC_OPS

op_type = OPERATOR_TO_NODE_TYPE['+']  # 'ADD'
is_arithmetic = '+' in ARITHMETIC_OPS  # True
```

### 2. `tokenizer.py` - Tokenization

**Chức năng:**
- Loại bỏ comments (// và /* */)
- Extract module name và ports
- Clean và prepare code cho parsing

**Classes:**
- `VerilogTokenizer`: Main tokenizer class

**Example:**
```python
from .tokenizer import VerilogTokenizer

tokenizer = VerilogTokenizer(source_code, file_path)
tokens = tokenizer.tokenize()
# Returns: {'module_name', 'port_list', 'module_body', ...}
```

### 3. `node_builder.py` - Node Creation

**Chức năng:**
- Builder pattern để tạo nodes
- Tự động generate unique IDs
- Centralize node creation logic
- Track output mappings

**Classes:**
- `NodeBuilder`: Tạo operation nodes, buffer nodes
- `WireGenerator`: Generate wire connections

**Example:**
```python
from .node_builder import NodeBuilder

builder = NodeBuilder()
builder.create_operation_with_buffer(
    node_type='ADD',
    operands=['a', 'b'],
    output_signal='sum'
)
nodes = builder.get_nodes()
```

### 4. `operations/*` - Operation Parsers

Mỗi file chứa parsers cho một nhóm operations cụ thể:

#### `arithmetic.py` - Phép Toán Số Học
- `parse_addition()`: a + b
- `parse_subtraction()`: a - b
- `parse_multiplication()`: a * b
- `parse_division()`: a / b
- `parse_modulo()`: a % b

#### `bitwise.py` - Phép Toán Bitwise
- `parse_and_operation()`: a & b
- `parse_or_operation()`: a | b
- `parse_xor_operation()`: a ^ b (hỗ trợ chain)
- `parse_not_operation()`: ~a
- `parse_nand_operation()`: a ~& b
- `parse_nor_operation()`: a ~| b
- `parse_xnor_operation()`: a ~^ b hoặc a ^~ b

#### `logical.py` - Phép Toán Logic
- `parse_logical_and()`: a && b
- `parse_logical_or()`: a || b
- `parse_logical_not()`: !a

#### `comparison.py` - Phép So Sánh
- `parse_equality()`: a == b
- `parse_not_equal()`: a != b
- `parse_less_than()`: a < b
- `parse_less_or_equal()`: a <= b
- `parse_greater_than()`: a > b
- `parse_greater_or_equal()`: a >= b

#### `shift.py` - Phép Dịch Bit
- `parse_shift_left()`: a << n
- `parse_shift_right()`: a >> n
- `parse_arithmetic_shift_left()`: a <<< n
- `parse_arithmetic_shift_right()`: a >>> n

#### `special.py` - Operations Đặc Biệt
- `parse_ternary_operation()`: cond ? a : b
- `parse_concatenation()`: {a, b, c}
- `parse_slice()`: signal[msb:lsb]
- `parse_replication()`: {4{a}}

### 5. `parser.py` - Main Parser

**Chức năng:**
- Entry point chính: `parse_verilog(path)`
- Tổng hợp tất cả modules
- Implement parsing flow
- Generate statistics

**Flow:**
```
1. Read file
2. Tokenize → extract module info
3. Parse ports & wires
4. Parse assign statements → dispatch to operation parsers
5. Parse gate/module instantiations
6. Generate wire connections
7. Compute statistics
8. Return netlist
```

## 🎯 Lợi Ích của Refactoring

### 1. **Dễ Đọc (Readability)**
- Mỗi file < 300 dòng
- Chức năng rõ ràng, tách biệt
- Comment tiếng Việt đầy đủ

### 2. **Dễ Maintain (Maintainability)**
- Tìm bug dễ dàng (biết file nào chứa logic nào)
- Thêm operators mới: chỉ sửa 1 file
- Test từng module độc lập

### 3. **Performance**
- Compiled regex patterns (faster)
- Builder pattern (less code duplication)
- Centralized logic

### 4. **Extensibility**
- Dễ thêm parsers mới
- Dễ thêm optimizations
- Dễ customize cho project cụ thể

## 🔧 Usage

### Basic Usage

```python
from frontends.verilog import parse_verilog

# Parse file
netlist = parse_verilog("design.v")

# Access parsed data
print(f"Module: {netlist['name']}")
print(f"Inputs: {netlist['inputs']}")
print(f"Outputs: {netlist['outputs']}")
print(f"Nodes: {len(netlist['nodes'])}")
```

### Advanced Usage

```python
from frontends.verilog import parse_verilog
from frontends.verilog.node_builder import NodeBuilder
from frontends.verilog.operations.arithmetic import parse_addition

# Custom parsing
builder = NodeBuilder()
parse_addition(builder, 'sum', 'a + b')
nodes = builder.get_nodes()
```

## 📝 Adding New Operations

Để thêm operation mới (ví dụ: exponential `**`):

### Bước 1: Update `constants.py`

```python
# Thêm vào ARITHMETIC_OPS
ARITHMETIC_OPS = {'+', '-', '*', '/', '%', '**'}

# Thêm vào OPERATOR_TO_NODE_TYPE
OPERATOR_TO_NODE_TYPE = {
    # ...
    '**': 'POW',
}
```

### Bước 2: Thêm parser vào `operations/arithmetic.py`

```python
def parse_power(node_builder: NodeBuilder, lhs: str, rhs: str) -> None:
    """Parse phép lũy thừa (a ** b)."""
    parse_arithmetic_operation(node_builder, '**', lhs, rhs)
```

### Bước 3: Update `parser.py`

```python
# Trong _dispatch_assign_parser, thêm check:
if '**' in rhs:
    from .operations.arithmetic import parse_power
    parse_power(node_builder, lhs, rhs)
    return
```

Xong! Operation mới đã được integrate.

## 🧪 Testing

Mỗi module có thể test độc lập:

```python
# Test tokenizer
from frontends.verilog.tokenizer import VerilogTokenizer

code = "module test(input a, output b); assign b = a; endmodule"
tokenizer = VerilogTokenizer(code)
tokens = tokenizer.tokenize()
assert tokens['module_name'] == 'test'

# Test node builder
from frontends.verilog.node_builder import NodeBuilder

builder = NodeBuilder()
builder.create_operation_with_buffer('ADD', ['a', 'b'], 'sum')
assert len(builder.get_nodes()) == 2  # ADD + BUF

# Test operations
from frontends.verilog.operations.arithmetic import detect_arithmetic_operator

assert detect_arithmetic_operator('a + b') == '+'
assert detect_arithmetic_operator('a * b') == '*'
```

## 📊 So Sánh: Trước và Sau

### Trước Refactor:
```
pyverilog.py (1228 lines)
├── All regex patterns mixed in code
├── All parsing logic in one place
├── Code duplication in parse functions
└── Hard to find specific logic
```

**Vấn đề:**
- Khó đọc (quá dài)
- Khó maintain (logic rải rác)
- Code duplication (mỗi parse_* function giống nhau)
- Regex không được optimize

### Sau Refactor:
```
verilog/ (modular, ~1500 lines total nhưng organized)
├── constants.py (200 lines) - Tất cả patterns
├── tokenizer.py (150 lines) - Tokenization
├── node_builder.py (250 lines) - Node creation
├── parser.py (400 lines) - Main logic
└── operations/ (540 lines) - Operation parsers
    ├── arithmetic.py (120 lines)
    ├── bitwise.py (150 lines)
    ├── logical.py (120 lines)
    ├── comparison.py (100 lines)
    ├── shift.py (120 lines)
    └── special.py (180 lines)
```

**Lợi ích:**
- ✅ Dễ đọc (mỗi file < 300 dòng)
- ✅ Dễ maintain (biết logic ở đâu)
- ✅ No duplication (Builder pattern)
- ✅ Optimized (compiled regex)
- ✅ Extensible (dễ thêm features)
- ✅ Testable (test từng module)

## 🔗 Backward Compatibility

Code cũ vẫn hoạt động:

```python
# Old imports still work
from parsers import parse_verilog  # ✅
from frontends.pyverilog import parse_verilog  # ✅

# New recommended import
from frontends.verilog import parse_verilog  # ✅
```

## 👥 Contributors

- MyLogic Team
- Refactored: 2024

## 📄 License

MIT License

