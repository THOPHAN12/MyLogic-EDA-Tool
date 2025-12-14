# Examples Directory - Test Cases by Feature

Thư mục này chứa các ví dụ test được tổ chức theo từng tính năng riêng biệt.

## 📁 Cấu Trúc Thư Mục

```
examples/
├── 01_parameters/          # Parameters và Localparams
├── 02_always_blocks/       # Always blocks (sequential & combinational)
├── 03_generate_blocks/     # Generate blocks (for/if)
├── 04_case_statements/    # Case statements (case/casex/casez)
├── 05_bit_manipulation/   # Bit slices, replication, concatenation
├── 06_memory_arrays/      # Memory và arrays
├── 07_functions_tasks/    # Functions và tasks
├── 08_module_instantiation/# Module instantiation (named/ordered ports)
├── 09_optimization/        # Mạch tối ưu vs chưa tối ưu
├── 10_arithmetic/         # Arithmetic operations
├── 11_bitwise/            # Bitwise operations
├── 12_logical/            # Logical operations
├── 13_comparison/         # Comparison operations
├── 14_shift_operations/   # Shift operations
└── 15_comprehensive/       # Test tổng hợp tất cả tính năng
```

## 🧪 Test Cases

### 01_parameters/
- `test_parameters.v` - Module parameters, localparams, parameterized widths

### 02_always_blocks/
- `test_always_sequential.v` - Sequential always blocks với clock edges
- `test_always_combinational.v` - Combinational always blocks

### 03_generate_blocks/
- `test_generate_for.v` - Generate for loops với unrolling
- `test_generate_if.v` - Generate if statements

### 04_case_statements/
- `test_case.v` - Case, casex, casez statements

### 05_bit_manipulation/
- `test_bit_slices.v` - Bit slices và single bit access
- `test_replication.v` - Replication và concatenation

### 06_memory_arrays/
- `test_memory.v` - Memory declarations và array indexing

### 07_functions_tasks/
- `test_functions.v` - Function declarations và calls
- `test_tasks.v` - Task declarations và calls

### 08_module_instantiation/
- `test_named_ports.v` - Module instantiation với named ports
- `test_ordered_ports.v` - Module instantiation với ordered ports

### 09_optimization/
- `unoptimized.v` - Mạch chưa tối ưu (có redundant logic)
- `optimized.v` - Mạch đã tối ưu (CSE, DCE, constant propagation)

### 10_arithmetic/
- `test_arithmetic.v` - +, -, *, /, % operations

### 11_bitwise/
- `test_bitwise.v` - &, |, ^, ~^, ~ operations

### 12_logical/
- `test_logical.v` - &&, ||, ! operations

### 13_comparison/
- `test_comparison.v` - >, <, ==, !=, >=, <= operations

### 14_shift_operations/
- `test_shift.v` - <<, >>, >>> operations

### 15_comprehensive/
- `full_feature_test.v` - Test tổng hợp tất cả tính năng

## 🚀 Cách Sử Dụng

### Test một tính năng cụ thể:

```bash
python mylogic.py
mylogic> read examples/01_parameters/test_parameters.v
mylogic> stats
mylogic> synthesis standard
```

### Test tất cả tính năng:

```bash
python mylogic.py
mylogic> read examples/15_comprehensive/full_feature_test.v
mylogic> stats
mylogic> synthesis aggressive
```

### So sánh optimization:

```bash
# Test mạch chưa tối ưu
mylogic> read examples/09_optimization/unoptimized.v
mylogic> synthesis standard
mylogic> stats

# Test mạch đã tối ưu
mylogic> read examples/09_optimization/optimized.v
mylogic> synthesis standard
mylogic> stats
```

## 📊 Test Results

Mỗi test case sẽ cho kết quả:
- **Parsing:** Số nodes, wires, inputs, outputs
- **Synthesis:** Reduction percentage
- **Optimization:** Các optimizations được áp dụng

## 🔍 Features Tested

### ✅ Fully Supported
- Parameters và localparams
- Always blocks (sequential & combinational)
- Generate blocks (for/if)
- Case statements (case/casex/casez)
- Bit slices và replication
- Memory và arrays
- Functions và tasks
- Module instantiation
- Arithmetic operations
- Bitwise operations
- Logical operations
- Comparison operations
- Shift operations

### ⚠️ Limitations
- Parser chỉ parse module cuối cùng trong file
- Một số advanced features có thể cần thêm testing

## 📝 Notes

- Tất cả test cases đều là single module (để tránh vấn đề parser)
- Mỗi test case tập trung vào một tính năng cụ thể
- Comprehensive test chứa tất cả tính năng trong một module

