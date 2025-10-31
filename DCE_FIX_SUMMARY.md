# TÓM TẮT SỬA LỖI DCE

## ✅ ĐÃ SỬA

### Vấn Đề:
DCE đã xóa tất cả các nodes có chức năng, để lại chỉ 2 CONST0 nodes cho full adder.

### Nguyên Nhân:
1. **Tìm node sai**: Code tìm node bằng `id` field, nhưng `output_mapping` trỏ đến `output` signal (như "xor_0", "or_7")
2. **Matching logic**: Không match được node vì so sánh sai field

### Giải Pháp Đã Áp Dụng:

#### 1. Sửa `_find_reachable_nodes()`:

**Trước**:
```python
if output_name in output_mapping:
    node_id = output_mapping[output_name]  # "xor_0"
    # Tìm node bằng id (SAI)
    if n.get('id') == current_node:
```

**Sau**:
```python
if output_name in output_mapping:
    output_signal = output_mapping[output_name]  # "xor_0"
    # Tìm node bằng output field (ĐÚNG)
    for key, node_data in nodes_dict.items():
        node_output = node_data.get('output')
        node_id = node_data.get('id')
        if node_output == output_signal or node_id == output_signal:
            # Tìm thấy!
```

#### 2. Sửa `_remove_dead_nodes()`:

**Trước**: Dùng list indices, dễ lỗi

**Sau**: Dùng dict keys, match cả `node_key` và `node_id`

#### 3. Cải thiện Fanin Matching:

**Trước**: Chỉ tìm một cách

**Sau**: Tìm bằng cả `output` field và `id` field

---

## 🔍 CHI TIẾT THAY ĐỔI

### File: `core/optimization/dce.py`

1. **Line 120-158**: Sửa logic tìm nodes từ outputs
   - Normalize nodes to dict
   - Tìm node bằng `output` field thay vì chỉ `id`
   - Thêm logging chi tiết

2. **Line 160-207**: Cải thiện BFS traversal
   - Sử dụng dict keys thay vì list
   - Match cả `output` và `id` fields
   - Better error handling

3. **Line 209-249**: Sửa `_remove_dead_nodes()`
   - Làm việc với dict thay vì list
   - Match bằng cả key và id

---

## ✅ KẾT QUẢ MONG ĐỢI

Sau khi sửa, full adder sau synthesis phải:
- **Giữ được ít nhất 5 nodes**: 2 XOR + 2 AND + 1 OR
- **Không còn CONST0 nodes** (trừ khi thực sự là constant)
- **Bảo toàn chức năng**: sum và cout vẫn hoạt động đúng

---

## 🧪 CẦN TEST

Chạy lại synthesis flow:
```bash
mylogic> read examples/full_adder.v
mylogic> synthesis standard
```

Kiểm tra:
- Số lượng nodes sau DCE ≥ 5
- Vẫn có XOR, AND, OR gates
- Output mapping vẫn đúng

---

**Ngày**: 2025-10-31  
**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ

