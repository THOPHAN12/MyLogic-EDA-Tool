# PHÂN TÍCH VẤN ĐỀ FULL ADDER

## ✅ CẤU TRÚC ĐÚNG CỦA FULL ADDER

Full adder **ĐÚNG** phải có:
- **2 cổng XOR**: 
  - XOR1: `A ⊕ B`
  - XOR2: `(A ⊕ B) ⊕ Cin` → **Sum**
- **2 cổng AND**:
  - AND1: `A & B`
  - AND2: `(A ⊕ B) & Cin`
- **1 cổng OR**: 
  - OR1: `(A & B) | ((A ⊕ B) & Cin)` → **Cout**

**Tổng cộng**: 5 cổng logic (2 XOR + 2 AND + 1 OR)

---

## ❌ VẤN ĐỀ HIỆN TẠI

### 1. **Vấn đề DCE (NGHIÊM TRỌNG)**

**Sau synthesis**, full adder chỉ còn:
- **2 nodes CONST0** (sai hoàn toàn!)

**Phân tích**:
- Ban đầu: 9 nodes (2 XOR, 2 AND, 1 OR, 4 BUF)
- Sau Strash: 7 nodes (đã xóa 2 BUF - đúng)
- Sau DCE: **2 nodes CONST0** (SAI - đã xóa tất cả logic!)

**Nguyên nhân**: DCE's `_find_reachable_nodes()` không tìm đúng các nodes từ outputs.

**File output**: `outputs/full_adder_synthesized_standard.json`
```json
{
  "nodes": [
    {"type": "CONST0", "output": "xor_0"},
    {"type": "CONST0", "output": "or_7"}
  ]
}
```

→ **MẤT HOÀN TOÀN chức năng của full adder!**

---

### 2. **Vấn đề Technology Mapping (ĐÃ SỬA)**

**Trước khi sửa**:
- `OR(C,D)` không khớp với `OR(A,B)` trong library
- `XOR(temp1,temp2)` không khớp với `XOR(A,B)` trong library

**Đã sửa**: Thêm `normalize_function()` để chuẩn hóa variable names:
- `OR(C,D)` → `OR(A,B)` ✅
- `XOR(temp1,temp2)` → `XOR(A,B)` ✅

**File đã sửa**: `core/technology_mapping/technology_mapping.py`

---

## 🔧 GIẢI PHÁP

### Ưu Tiên 1: Sửa DCE (CRITICAL)

**Vấn đề trong `core/optimization/dce.py`**:
- `output_mapping` trỏ đến output signal (như `"xor_0"`, `"or_7"`)
- Nhưng `_find_reachable_nodes()` tìm node bằng `id` thay vì `output`

**Cần sửa**:
```python
# Line 128-132: Tìm node bằng output field thay vì id
if output_name in output_mapping:
    output_signal = output_mapping[output_name]  # "xor_0"
    # Tìm node có output == output_signal
    for node_key, node_data in nodes.items():
        if node_data.get('output') == output_signal:
            reachable.add(node_key)
            queue.append(node_key)
```

### Ưu Tiên 2: Technology Mapping (ĐÃ SỬA ✅)

Đã thêm normalize function matching.

---

## 📊 SO SÁNH

| Stage | Số Nodes | Types | Status |
|-------|----------|-------|--------|
| **Ban đầu** | 9 | 2 XOR, 2 AND, 1 OR, 4 BUF | ✅ Đúng |
| **Sau Strash** | 7 | 2 XOR, 2 AND, 1 OR, 2 BUF | ✅ Đúng |
| **Sau DCE** | 2 | 2 CONST0 | ❌ **SAI** |
| **Kỳ vọng** | ≥5 | 2 XOR, 2 AND, 1 OR | ✅ Đúng |

---

## ✅ KẾT LUẬN

1. **Cấu trúc full adder bạn mô tả là ĐÚNG**: 2 XOR + 2 AND + 1 OR
2. **Vấn đề DCE**: Đã xóa sai các nodes có chức năng → cần sửa ngay
3. **Vấn đề Tech Mapping**: Đã sửa xong function matching
4. **Cần test lại**: Sau khi sửa DCE, full adder phải giữ được ít nhất 5 nodes (2 XOR, 2 AND, 1 OR)

---

**Ngày**: 2025-10-31  
**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ

