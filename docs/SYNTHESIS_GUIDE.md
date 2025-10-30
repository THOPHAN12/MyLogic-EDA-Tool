# MyLogic - Hướng Dẫn Sử Dụng Complete Synthesis Flow

## Tổng Quan

MyLogic cung cấp 2 cách để chạy toàn bộ quy trình tối ưu hóa (Complete Synthesis Flow):

1. **Chế độ tự động** (`--synthesize`): Chạy và export kết quả, sau đó thoát
2. **Chế độ tương tác** (shell): Load file, sau đó chạy lệnh `synthesis`

## Quy Trình Tối Ưu Hóa

Synthesis Flow bao gồm 5 bước tối ưu hóa tuần tự:

```
1. Strash (Structural Hashing)
   └─> Loại bỏ các node trùng lặp và buffer không cần thiết
   
2. DCE (Dead Code Elimination)
   └─> Loại bỏ các node không thể tiếp cận từ outputs
   
3. CSE (Common Subexpression Elimination)
   └─> Tạo shared nodes cho các subexpression trùng lặp
   
4. ConstProp (Constant Propagation)
   └─> Propagate constants qua mạch và simplify logic
   
5. Balance (Logic Balancing)
   └─> Cân bằng độ sâu logic để tối ưu timing
```

## Cách 1: Chế Độ Tự Động

### Cú pháp

```bash
python mylogic.py --file <verilog_file> --synthesize <level>
```

### Optimization Levels

- `basic`: Chỉ optimizations cơ bản
- `standard`: Optimizations tiêu chuẩn (khuyến nghị)
- `aggressive`: Optimizations tích cực nhất

### Ví Dụ

```bash
# Full adder với optimization standard
python mylogic.py --file examples/full_adder.v --synthesize standard

# Comprehensive combinational với optimization aggressive
python mylogic.py --file examples/comprehensive_combinational.v --synthesize aggressive

# Với debug logging
python mylogic.py --file examples/full_adder.v --synthesize standard --debug
```

### Output

Kết quả được export tự động vào thư mục `outputs/`:

```
outputs/
  └─ <filename>_synthesized_<level>.json
```

## Cách 2: Chế Độ Tương Tác (Shell)

### Bước 1: Khởi động shell

```bash
python mylogic.py --file examples/full_adder.v
```

hoặc

```bash
python mylogic.py
```

### Bước 2: Load file (nếu chưa load)

```
mylogic> read examples/full_adder.v
```

### Bước 3: Chạy synthesis

```
mylogic> synthesis standard
```

hoặc

```
mylogic> synthesis basic
mylogic> synthesis aggressive
```

### Bước 4: Xem kết quả

```
mylogic> stats
```

### Bước 5: Export (optional)

```
mylogic> export_json synthesized_output.json
```

## Xem Output Chi Tiết

Để xem log chi tiết trong quá trình synthesis, sử dụng flag `--debug`:

```bash
python mylogic.py --file examples/full_adder.v --synthesize standard --debug
```

Output sẽ bao gồm:
- Log chi tiết từng bước optimization
- Debug information
- Thống kê đầy đủ

## Chạy Từng Bước Optimization Riêng Lẻ

Ngoài synthesis flow hoàn chỉnh, bạn có thể chạy từng optimization riêng:

### Trong Shell

```
mylogic> read examples/full_adder.v
mylogic> strash       # Structural Hashing
mylogic> stats
mylogic> dce          # Dead Code Elimination
mylogic> stats
mylogic> cse          # Common Subexpression Elimination
mylogic> stats
mylogic> constprop    # Constant Propagation
mylogic> stats
mylogic> balance      # Logic Balancing
mylogic> stats
```

### Test Modules Riêng Lẻ

```bash
# Test từng module optimization
python core/optimization/dce.py
python core/optimization/cse.py
python core/optimization/constprop.py
python core/optimization/balance.py

# Test strash
python core/synthesis/strash.py

# Test complete synthesis flow
python core/synthesis/synthesis_flow.py
```

## So Sánh 2 Phương Pháp

| Tính năng | `--synthesize` | Shell Interactive |
|-----------|----------------|-------------------|
| Tự động chạy toàn bộ | ✓ | ✗ |
| Output chi tiết | ✓ (với --debug) | ✓ |
| Tương tác | ✗ | ✓ |
| Auto export | ✓ | ✗ (dùng export_json) |
| Chạy từng bước riêng | ✗ | ✓ |
| Debug mode | ✓ | ✓ |
| Phù hợp cho | Automation, Scripts | Development, Testing |

## Tips & Best Practices

### 1. Chọn Optimization Level

- **basic**: Cho circuits nhỏ, cần tốc độ compile nhanh
- **standard**: Cho hầu hết các trường hợp (khuyến nghị)
- **aggressive**: Cho circuits lớn, cần tối ưu tối đa

### 2. Xem Thống Kê Chi Tiết

Sử dụng shell mode để xem thống kê sau mỗi bước:

```bash
python mylogic.py --file examples/full_adder.v
```

Trong shell:
```
mylogic> strash
mylogic> stats    # Xem kết quả sau strash
mylogic> dce
mylogic> stats    # Xem kết quả sau DCE
```

### 3. Debug Mode

Khi gặp lỗi, sử dụng `--debug`:

```bash
python mylogic.py --file examples/full_adder.v --synthesize standard --debug
```

### 4. Kiểm Tra Output File

Kết quả synthesis được lưu dạng JSON, dễ dàng kiểm tra:

```bash
# Windows
type outputs\full_adder_synthesized_standard.json

# Linux/Mac
cat outputs/full_adder_synthesized_standard.json
```

## Ví Dụ Thực Tế

### Ví dụ 1: Quick Synthesis

```bash
python mylogic.py -f examples/full_adder.v -s standard
```

### Ví dụ 2: Development với Shell

```bash
python mylogic.py --file examples/comprehensive_combinational.v

# Trong shell:
mylogic> synthesis standard
mylogic> stats
mylogic> export_json my_optimized_circuit.json
```

### Ví dụ 3: Batch Processing

```bash
# Windows PowerShell
Get-ChildItem examples\*.v | ForEach-Object {
    python mylogic.py -f $_.FullName -s standard
}

# Linux/Mac
for file in examples/*.v; do
    python mylogic.py -f "$file" -s standard
done
```

### Ví dụ 4: Debug Mode cho Presentation

```bash
# Output chi tiết cho demo/presentation
python mylogic.py -f examples/full_adder.v -s standard --debug
python mylogic.py -f examples/comprehensive_combinational.v -s aggressive --debug
```

## Troubleshooting

### Lỗi: "No netlist loaded"

**Nguyên nhân**: Chưa load file trong shell mode

**Giải pháp**:
```
mylogic> read examples/full_adder.v
mylogic> synthesis standard
```

### Lỗi: "Invalid optimization level"

**Nguyên nhân**: Level không hợp lệ

**Giải pháp**: Chỉ dùng `basic`, `standard`, hoặc `aggressive`

### Kết quả không như mong đợi

**Nguyên nhân**: Có thể do format netlist hoặc optimization quá aggressive

**Giải pháp**:
1. Thử level thấp hơn (`basic` thay vì `aggressive`)
2. Sử dụng `--debug` để xem log chi tiết
3. Chạy từng optimization riêng lẻ trong shell mode

## Tài Liệu Tham Khảo

- `docs/` - Tài liệu chi tiết về project
- `core/optimization/README.md` - Chi tiết về optimization algorithms
- `core/synthesis/README.md` - Chi tiết về synthesis algorithms
- `examples/` - Các file Verilog mẫu để test

## Liên Hệ & Báo Lỗi

Nếu gặp vấn đề hoặc có câu hỏi, vui lòng tạo issue trên GitHub repository.

---

**Tác giả**: MyLogic Development Team  
**Phiên bản**: 2.0  
**Cập nhật**: 2025

