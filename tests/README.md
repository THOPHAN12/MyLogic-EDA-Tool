# MyLogic EDA Tool - Test Suite

Hệ thống test hoàn chỉnh để kiểm tra các thuật toán trong MyLogic EDA Tool.

## 📁 Cấu trúc thư mục

```
tests/
├── algorithms/           # Test files cho các thuật toán
│   ├── test_strash.py
│   ├── test_dce.py
│   ├── test_cse.py
│   └── test_synthesis_flow.py
├── examples/            # Ví dụ sử dụng
│   └── test_example.py
├── test_data/           # Dữ liệu test
│   ├── simple_and.v
│   ├── complex_expression.v
│   ├── duplicate_nodes.v
│   ├── dead_code.v
│   ├── common_subexpressions.v
│   └── constants.v
├── expected_outputs/    # Kết quả mong đợi
│   ├── strash_expected.txt
│   └── dce_expected.txt
├── run_all_tests.py     # Test runner chính
├── test_config.json     # Cấu hình test
└── README.md           # Tài liệu này
```

## 🚀 Cách chạy test

### Chạy tất cả test:
```bash
python tests/run_all_tests.py
```

### Chạy test cụ thể:
```bash
python tests/run_all_tests.py --test strash
python tests/run_all_tests.py --test dce
python tests/run_all_tests.py --test cse
python tests/run_all_tests.py --test synthesis
```

### Chạy ví dụ:
```bash
python tests/examples/test_example.py
```

## 🧪 Các test có sẵn

### 1. Structural Hashing (Strash)
- **File**: `tests/algorithms/test_strash.py`
- **Mục đích**: Kiểm tra thuật toán loại bỏ node trùng lặp
- **Test cases**:
  - Simple duplicates
  - Complex duplicates
  - No duplicates

### 2. Dead Code Elimination (DCE)
- **File**: `tests/algorithms/test_dce.py`
- **Mục đích**: Kiểm tra thuật toán loại bỏ logic không cần thiết
- **Test cases**:
  - Simple dead code
  - Complex dead code chains
  - No dead code

### 3. Common Subexpression Elimination (CSE)
- **File**: `tests/algorithms/test_cse.py`
- **Mục đích**: Kiểm tra thuật toán loại bỏ biểu thức con trùng lặp
- **Test cases**:
  - Simple common subexpressions
  - Complex common subexpressions
  - No common subexpressions

### 4. Complete Synthesis Flow
- **File**: `tests/algorithms/test_synthesis_flow.py`
- **Mục đích**: Kiểm tra quy trình tổng hợp hoàn chỉnh
- **Test cases**:
  - Basic synthesis
  - Standard synthesis
  - Aggressive synthesis

## 📊 Test Data

### Verilog Test Files:
- `simple_and.v`: AND gate đơn giản
- `complex_expression.v`: Biểu thức phức tạp
- `duplicate_nodes.v`: Node trùng lặp (cho Strash)
- `dead_code.v`: Dead code (cho DCE)
- `common_subexpressions.v`: Biểu thức con trùng lặp (cho CSE)
- `constants.v`: Hằng số (cho ConstProp)

## ✅ Success Criteria

### Strash Test:
- Duplicate nodes được loại bỏ
- Non-duplicate nodes được bảo toàn
- Node count giảm khi có duplicates

### DCE Test:
- Dead code nodes được loại bỏ
- Used logic nodes được bảo toàn
- Node count giảm khi có dead code

### CSE Test:
- Common subexpressions được loại bỏ
- Unique subexpressions được bảo toàn
- Node count giảm khi có common subexpressions

### Synthesis Flow Test:
- Tất cả optimizations hoạt động cùng nhau
- Significant node reduction
- Dead code removal
- Duplicate elimination

## 🔧 Troubleshooting

### Import Errors:
```bash
# Đảm bảo đang ở thư mục gốc project
cd /path/to/MyLogic
python tests/run_all_tests.py
```

### Module Not Found:
```bash
# Kiểm tra Python path
export PYTHONPATH=$PYTHONPATH:/path/to/MyLogic
```

### Test Failures:
1. Kiểm tra import paths
2. Kiểm tra test data files
3. Kiểm tra algorithm implementations
4. Xem detailed error messages

## 📈 Test Results

Test suite sẽ hiển thị:
- Số lượng test cases
- Pass/Fail status
- Success rate
- Detailed error messages
- Optimization statistics

## 🎯 Mục tiêu

Test suite đảm bảo:
- Tất cả algorithms hoạt động đúng
- Optimization hiệu quả
- Code quality cao
- Regression testing
- Performance validation
