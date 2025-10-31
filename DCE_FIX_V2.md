# SỬA LỖI DCE - PHIÊN BẢN 2

## 🔍 PHÂN TÍCH VẤN ĐỀ

Từ terminal output, DCE vẫn xóa 5 nodes, chỉ còn 2 nodes. Vấn đề có thể là:

1. **Format mismatch**: Sau strash, nodes có thể là list, nhưng khi normalize sang dict, keys không khớp với output_mapping
2. **Key selection**: Khi normalize từ list, code dùng `id` hoặc index, nhưng output_mapping trỏ đến `output` signals

## ✅ GIẢI PHÁP ĐÃ ÁP DỤNG

### 1. Cải Thiện Normalization (Line 127-147)

**Trước**:
```python
key = str(n.get('id', i))  # Chỉ dùng id hoặc index
```

**Sau**:
```python
# Prefer node id, then output, then index
node_id = n.get('id')
node_output = n.get('output')

if node_id is not None:
    key = str(node_id)
elif node_output is not None:
    key = str(node_output)  # Use output as key - QUAN TRỌNG!
else:
    key = str(i)
```

**Lý do**: `output_mapping` trỏ đến output signals (như "xor_0", "or_7"), nên nếu dùng output làm key, sẽ match được!

### 2. Thêm Debug Logging

- Log tổng số nodes trước DCE
- Log output_mapping và outputs
- Log sample nodes để debug
- Log khi tìm thấy/không tìm thấy nodes
- Log reachable nodes count

### 3. Cải Thiện Matching Logic (Line 162)

**Thêm**: Match cả `key` ngoài `output` và `id`:
```python
if node_output == output_signal or node_id == output_signal or key == output_signal:
```

### 4. Cải Thiện Dead Node Detection (Line 256-258)

**Thêm**: Check cả string và non-string keys:
```python
is_reachable = (node_key_str in reachable_nodes or 
               node_id in reachable_nodes or
               node_key in reachable_nodes)
```

## 🧪 TEST

Chạy lại:
```bash
python mylogic.py
mylogic> read examples/full_adder.v
mylogic> synthesis standard
```

Kiểm tra logs để xem:
- Có tìm thấy nodes từ outputs không?
- Reachable nodes có bao nhiêu?
- Dead nodes có đúng không?

---

**Ngày**: 2025-10-31  
**Status**: Đã sửa normalization và matching logic

