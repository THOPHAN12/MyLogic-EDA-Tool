# Test Scripts và Examples

## 📋 Test Scripts

### `test_complete_features.py`

Script test toàn diện cho tất cả tính năng của MyLogic EDA Tool.

#### Chạy test:

```bash
python test_complete_features.py
```

#### Các test cases:

1. **Verilog Parsing** - Test parsing với tất cả syntax features
2. **Logic Synthesis** - Test complete synthesis flow (5 bước)
3. **Technology Mapping** - Test technology mapping với auto-load library
4. **Simulation** - Test vector simulation
5. **JSON Export** - Test export netlist to JSON
6. **VLSI CAD Algorithms** - Test tất cả VLSI CAD tools:
   - BDD (Binary Decision Diagrams)
   - SAT Solver
   - Placement Algorithms
   - Routing Algorithms
   - Static Timing Analysis (STA)

#### Output:

- Test results với color coding
- Detailed statistics cho mỗi test
- Summary report cuối cùng

## 📝 Example Files

### `examples/advanced_design.v`

File Verilog ví dụ đầy đủ chức năng, bao gồm:

- ✅ **Parameters**: Parameterized module headers
- ✅ **Signed/Unsigned**: Port declarations với signed/unsigned
- ✅ **Always Blocks**: Sequential (`always @(posedge clk)`) và combinational (`always @(*)`)
- ✅ **Generate Blocks**: `generate/endgenerate` với `for` loops và `if` statements
- ✅ **Case Statements**: `case`, `casex`, `casez` với default cases
- ✅ **Bit Manipulation**: Bit slices, replication, concatenation
- ✅ **Memory**: Array declarations và indexing
- ✅ **Functions & Tasks**: Function và task declarations
- ✅ **Module Instantiation**: Named ports (`.port(signal)`) và ordered ports
- ✅ **All Operations**: Arithmetic, bitwise, logical, comparison, shift

### `examples/comprehensive_test.v`

File test tổng hợp khác với các tính năng tương tự.

## 🎯 Usage

### Test một file cụ thể:

```python
from parsers import parse_verilog
from core.synthesis.synthesis_flow import run_complete_synthesis

# Parse
netlist = parse_verilog("examples/advanced_design.v")

# Synthesize
synthesized = run_complete_synthesis(netlist, "standard")

# Export
import json
with open("output.json", "w") as f:
    json.dump(synthesized, f, indent=2)
```

### Test với interactive shell:

```bash
python mylogic.py
mylogic> read examples/advanced_design.v
mylogic> stats
mylogic> synthesis standard
mylogic> techmap balanced auto
mylogic> export_json test_output.json
```

## 📊 Test Results

Khi chạy `test_complete_features.py`, bạn sẽ thấy:

```
======================================================================
               MyLogic EDA Tool - Complete Feature Test
======================================================================

[INFO] Test file: examples/advanced_design.v

======================================================================
                       TEST 1: Verilog Parsing
======================================================================
[OK] Parsing completed in 0.001s
[INFO] Module: advanced_design
[INFO] Inputs: 7
[INFO] Outputs: 4
[INFO] Nodes: XX
[INFO] Wires: XX

======================================================================
              TEST 2: Logic Synthesis (Level: standard)
======================================================================
[OK] Synthesis completed in 0.XXXs
[INFO] Original nodes: XX
[INFO] Final nodes: XX
[INFO] Reduction: XX nodes (XX.X%)

... (các tests khác)

======================================================================
                             TEST SUMMARY
======================================================================
Total tests: 10
Passed: 10
Failed: 0

All tests passed!
```

## 🔧 Customization

Bạn có thể customize test script:

1. **Thay đổi test file**: Sửa `test_file` variable trong `main()`
2. **Thay đổi synthesis level**: Sửa `level` parameter trong `test_synthesis()`
3. **Thay đổi library**: Sửa `library_type` trong `test_technology_mapping()`
4. **Thêm test cases**: Thêm functions mới vào script

## 📝 Notes

- Test script tự động tìm và load libraries từ `techlibs/`
- Output files được lưu trong `outputs/`
- Test results có color coding (nếu terminal hỗ trợ)
- Unicode characters được thay bằng ASCII để tương thích Windows

