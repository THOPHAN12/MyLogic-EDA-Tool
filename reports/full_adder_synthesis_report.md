# BÁO CÁO KẾT QUẢ SYNTHESIS VÀ TECHNOLOGY MAPPING

## THÔNG TIN ĐỒ ÁN

**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ  
**Circuit Test**: Full Adder  
**Ngày thực hiện**: 2025-10-31  
**Tool Version**: MyLogic EDA Tool v2.0.0  
**Test File**: `examples/full_adder.v`

---

## I. THÔNG TIN CIRCUIT BAN ĐẦU

### 1.1. Mô Tả Circuit

**Module**: `full_adder`  
**File**: `examples/full_adder.v`

**Mã Verilog**:
```verilog
module full_adder(a, b, cin, sum, cout);
  input a, b;
  input cin;
  output sum, cout;
  
  assign sum = a ^ b ^ cin;
  assign cout = (a & b) | (cin & (a ^ b));
endmodule
```

**Chức năng**:
- **sum**: Phép XOR của 3 ngõ vào (a, b, cin) → `sum = a ⊕ b ⊕ cin`
- **cout**: Ngõ ra nhớ → `cout = (a & b) | (cin & (a ^ b))`

### 1.2. Thống Kê Circuit (Trước Synthesis)

| Chỉ Số | Giá Trị | Phần Trăm |
|--------|---------|----------|
| **Tổng Nodes** | 9 | 100% |
| **Ngõ Vào Chính** | 3 | - |
| **Ngõ Ra Chính** | 2 | - |
| **Tổng Dây Nối** | 15 | - |

**Phân Bố Loại Node**:
- **Cổng AND**: 2 nodes (22.2%)
- **BUF (Buffer)**: 4 nodes (44.4%)
- **Cổng OR**: 1 node (11.1%)
- **Cổng XOR**: 2 nodes (22.2%)

**Phân Tích Vector**:
- Tất cả tín hiệu có độ rộng 1 bit
- Các tín hiệu: `a`, `b`, `cin`, `sum`, `cout`

---

## II. KẾT QUẢ LOGIC SYNTHESIS

### 2.1. Cấu Hình Synthesis Flow

**Mức Synthesis**: `standard`  
**Các Bước Flow**:
1. Structural Hashing (Strash) - Băm cấu trúc
2. Dead Code Elimination (DCE) - Loại bỏ mã chết
3. Common Subexpression Elimination (CSE) - Loại bỏ biểu thức con chung
4. Constant Propagation (ConstProp) - Lan truyền hằng số
5. Logic Balancing (Balance) - Cân bằng logic

### 2.2. Kết Quả Từng Bước

#### **Bước 1: Structural Hashing (Strash)**

**Mục đích**: Loại bỏ các nodes và buffers trùng lặp

**Kết quả**:
- **Nodes ban đầu**: 9
- **Nodes sau tối ưu**: 7
- **Nodes đã loại bỏ**: 2
- **Tỷ lệ giảm**: 22.2%

**Nodes Đã Loại Bỏ**:
1. `buf_1` (BUF) - inputs: `[xor_0]` → được thay thế bằng kết nối trực tiếp tới `xor_0`
2. `buf_8` (BUF) - inputs: `[or_7]` → được thay thế bằng kết nối trực tiếp tới `or_7`

**Phân tích**: ✅ **THÀNH CÔNG** - Đã xác định và loại bỏ đúng các buffer thừa.

---

#### **Bước 2: Dead Code Elimination (DCE)**

**Mục đích**: Loại bỏ các nodes không thể truy cập từ bất kỳ ngõ ra chính nào

**Kết quả**:
- **Nodes đầu vào**: 7
- **Nodes đầu ra**: 2
- **Nodes đã loại bỏ**: 5
- **Dây nối đã loại bỏ**: 15
- **Tỷ lệ giảm**: 71.4%

**Phân tích**: ⚠️ **CÓ VẤN ĐỀ TIỀM ẨN** - DCE đã loại bỏ 5 trong 7 nodes, chỉ còn lại 2 nodes. Điều này quá mạnh và có thể cho thấy vấn đề trong phân tích khả năng truy cập hoặc ánh xạ ngõ ra.

---

#### **Bước 3: Common Subexpression Elimination (CSE)**

**Mục đích**: Xác định và chia sẻ các biểu thức con chung

**Kết quả**:
- **Nodes đầu vào**: 2
- **Nodes đầu ra**: 2
- **Biểu thức con chung tìm thấy**: 0
- **Nodes đã loại bỏ**: 0
- **Tỷ lệ giảm**: 0%

**Phân tích**: ✅ **DỰ ĐOÁN ĐƯỢC** - Không tìm thấy biểu thức con chung trong 2 nodes còn lại.

---

#### **Bước 4: Constant Propagation (ConstProp)**

**Mục đích**: Lan truyền các giá trị hằng số qua mạch

**Kết quả**:
- **Nodes đầu vào**: 2
- **Nodes đầu ra**: 2
- **Hằng số đã lan truyền**: 20
- **Cổng đã đơn giản hóa**: 2
- **Nodes đã loại bỏ**: 0
- **Số lần lặp**: 10

**Phân tích**: ⚠️ **ĐÁNG LO NGẠI** - Lan truyền 20 hằng số trong 10 lần lặp cho chỉ 2 nodes cho thấy có thể có vấn đề với logic lan truyền hằng số hoặc cấu trúc mạch sau DCE.

---

#### **Bước 5: Logic Balancing (Balance)**

**Mục đích**: Cân bằng độ sâu logic để tối ưu timing

**Kết quả**:
- **Nodes đầu vào**: 2
- **Nodes đầu ra**: 2
- **Mức logic tối đa**: 0
- **Nodes đã cân bằng**: 0
- **Nodes đã thêm**: 0

**Phân tích**: ✅ **DỰ ĐOÁN ĐƯỢC** - Không cần cân bằng khi chỉ còn 2 nodes.

---

### 2.3. Tổng Kết Synthesis

| Chỉ Số | Giá Trị |
|--------|---------|
| **Nodes Ban Đầu** | 9 |
| **Nodes Cuối Cùng** | 2 |
| **Tổng Giảm** | 7 nodes (77.8%) |
| **File Netlist** | `outputs/full_adder_synthesized_standard.json` |

**Phân Tích Tối Ưu Hóa**:
```
STRASH:    9 → 7 nodes (removed 2, -22.2%)
DCE:       7 → 2 nodes (removed 5, -71.4%)
CSE:       2 → 2 nodes (removed 0, 0%)
CONSTPROP: 2 → 2 nodes (removed 0, 0%)
BALANCE:   2 → 2 nodes (added 0, 0%)
-------------------------------------------
TOTAL:     9 → 2 nodes (-77.8%)
```

**Final Netlist Structure**:
```json
{
  "nodes": [
    {
      "type": "CONST0",
      "output": "xor_0",
      "value": 0,
      "id": "0"
    },
    {
      "type": "CONST0",
      "output": "or_7",
      "value": 0,
      "id": "1"
    }
  ],
  "output_mapping": {
    "sum": "xor_0",
    "cout": "or_7"
  }
}
```

---

## III. KẾT QUẢ TECHNOLOGY MAPPING

### 3.1. Cấu Hình Technology Mapping

**Chiến Lược**: `area_optimal` (tối ưu diện tích)  
**Thư Viện**: Standard Cell Library  
**Mục Tiêu Mapping**: Tối thiểu hóa tổng chi phí diện tích

### 3.2. Kết Quả Mapping

| Chỉ Số | Giá Trị |
|--------|---------|
| **Tổng Nodes** | 3 |
| **Nodes Đã Map** | 1 |
| **Nodes Chưa Map** | 2 |
| **Tỷ Lệ Thành Công** | 33.3% |
| **Tổng Diện Tích** | 1.50 |

**Sử Dụng Cell**:
- **AND2**: 1 instance

**Chi Tiết Mapping Node**:

| Node | Hàm | Cell Đã Map | Chi Phí | Trạng Thái |
|------|-----|-------------|---------|-----------|
| `n1` | AND(A,B) | AND2 | 1.50 | ✅ Đã Map |
| `n2` | OR(C,D) | Không có | N/A | ❌ Không Tìm Thấy |
| `n3` | XOR(temp1,temp2) | Không có | N/A | ❌ Không Tìm Thấy |

**Cảnh Báo**:
- ⚠️ Không tìm thấy cell phù hợp cho `n2` với hàm `OR(C,D)`
- ⚠️ Không tìm thấy cell phù hợp cho `n3` với hàm `XOR(temp1,temp2)`

### 3.3. Phân Tích Chi Tiết

#### **Nguyên Nhân Gốc: Lỗi Function Matching**

**Vấn Đề Chính**: Thuật toán matching hiện tại chỉ khớp **exact match** (khớp chính xác) theo tên biến, không normalize tên biến.

**Phân Tích**:
- **Node `n2`**: Function = `"OR(C,D)"`
- **Library Cell OR2**: Function = `"OR(A,B)"`
- **Kết Quả**: Không khớp vì `C,D` ≠ `A,B` (tên biến khác nhau)

- **Node `n3`**: Function = `"XOR(temp1,temp2)"`  
- **Library Cell XOR2**: Function = `"XOR(A,B)"`
- **Kết Quả**: Không khớp vì `temp1,temp2` ≠ `A,B`

**Kỳ Vọng**: Cả hai đều nên khớp vì chúng có cùng **logic function** (OR 2-input, XOR 2-input), chỉ khác tên biến.

**Vấn Đề Đã Xác Định**:
1. **Tỷ Lệ Thành Công Mapping Thấp (33.3%)**: Chỉ có 1 trong 3 nodes được map thành công
2. **Lỗi Function Matching**: Thuật toán matching không normalize tên biến, dẫn đến `OR(C,D)` không khớp `OR(A,B)` và `XOR(temp1,temp2)` không khớp `XOR(A,B)`
3. **Thư Viện Có Đầy Đủ**: Thư viện **có chứa** OR2 và XOR2, nhưng matching algorithm không tìm thấy do vấn đề trên
4. **Không Khớp Với Output Synthesis**: Technology mapping hiển thị 3 nodes trong khi output synthesis chỉ có 2 nodes CONST0 - cho thấy sự không nhất quán về dữ liệu

---

## IV. PHÂN TÍCH VÀ ĐÁNH GIÁ

### 4.1. Vấn Đề Synthesis Flow

#### ⚠️ **VẤN ĐỀ NGHIÊM TRỌNG: Circuit Không Đúng Sau Synthesis**

**Vấn đề**: Sau synthesis, mạch full adder đã bị giảm xuống chỉ còn 2 nodes CONST0, điều này **sai về mặt chức năng**.

**Hành Vi Mong Đợi**:
- Full adder phải duy trì logic XOR cho `sum = a ⊕ b ⊕ cin`
- Full adder phải duy trì logic phức tạp cho `cout = (a & b) | (cin & (a ^ b))`
- Mạch KHÔNG NÊN bị giảm xuống thành hằng số

**Phân Tích Nguyên Nhân Gốc**:
1. **DCE quá mạnh**: Đã loại bỏ 5 trong 7 nodes (giảm 71.4%)
2. **Vấn đề ánh xạ ngõ ra**: `output_mapping` trong netlist có thể không xác định đúng nodes nào điều khiển các ngõ ra chính
3. **Lỗi phân tích khả năng truy cập**: Thuật toán BFS của DCE có thể không truy vết đúng từ ngõ ra về ngõ vào

**Bằng Chứng**:
- Mạch ban đầu: 9 nodes (cổng XOR, AND, OR, BUF)
- Sau synthesis: 2 nodes CONST0
- Ánh xạ ngõ ra cho thấy `sum → xor_0` và `cout → or_7`, nhưng cả hai đều là CONST0

---

### 4.2. Vấn Đề Technology Mapping

#### ⚠️ **VẤN ĐỀ: Tỷ Lệ Thành Công Mapping Thấp**

**Vấn đề**: Chỉ có 33.3% nodes được map thành công vào các cell của thư viện công nghệ.

**Nguyên Nhân Có Thể**:
1. **Thư Viện Công Nghệ Không Đầy Đủ**: Thư viện có thể không chứa cổng OR và XOR
2. **Lỗi Function Matching**: Thuật toán matching có thể không xác định đúng các hàm Boolean tương đương
3. **Không Khớp Tên Node**: ID nodes trong output synthesis (`xor_0`, `or_7`) không khớp với ID nodes trong input techmap (`n1`, `n2`, `n3`)

---

### 4.3. Không Nhất Quán Dữ Liệu

#### ⚠️ **VẤN ĐỀ: Không Khớp Giữa Output Synthesis và Input Techmap**

**Output Synthesis**:
- 2 nodes: các nodes `CONST0` với outputs `xor_0` và `or_7`

**Input Techmap**:
- 3 nodes: `n1` (AND), `n2` (OR), `n3` (XOR)

**Phân Tích**: Điều này cho thấy rằng:
1. Technology mapping đang sử dụng một netlist khác/đã cache
2. Output synthesis không được truyền đúng đến technology mapping
3. Technology mapping đang đọc từ netlist gốc (trước synthesis)

---

## V. ĐỀ XUẤT KHẮC PHỤC

### 5.1. Sửa Chữa Synthesis Flow

#### **Ưu Tiên 1: Sửa Phân Tích Khả Năng Truy Cập DCE**

**Đề Xuất**: Xem xét và sửa phương thức `_find_reachable_nodes()` trong `core/optimization/dce.py`

**Các Vấn Đề Cần Giải Quyết**:
1. **Sử Dụng Output Mapping**: Đảm bảo DCE sử dụng đúng `output_mapping` từ `netlist['attrs']` để tìm các nodes điều khiển ngõ ra chính
2. **Duyệt BFS**: Xác minh rằng BFS duyệt đúng từ ngõ ra về ngõ vào
3. **Khớp Node ID**: Đảm bảo logic khớp Node ID xác định đúng các nodes bằng trường `output` của chúng

**Đề Xuất Sửa**:
```python
# In _find_reachable_nodes(), improve output mapping resolution:
output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
for output_name in outputs:
    if output_name in output_mapping:
        node_id = output_mapping[output_name]
        # Find node by matching output field, not just ID
        for node_key, node_data in nodes.items():
            if node_data.get('output') == node_id:
                reachable.add(node_key)
```

#### **Ưu Tiên 2: Xác Minh Logic Constant Propagation**

**Đề Xuất**: Xem xét constant propagation để đảm bảo nó không lan truyền sai các hằng số

**Các Vấn Đề Cần Giải Quyết**:
- Tại sao có 20 hằng số được lan truyền cho chỉ 2 nodes?
- Xác minh rằng khởi tạo hằng số không đánh dấu tất cả nodes thành hằng số

#### **Ưu Tiên 3: Thêm Các Kiểm Tra Validation**

**Đề Xuất**: Thêm validation sau synthesis để đảm bảo:
- Tất cả ngõ ra chính vẫn được kết nối
- Chức năng mạch được bảo toàn
- Sự giảm số lượng nodes là hợp lý

---

### 5.2. Sửa Chữa Technology Mapping

#### **Ưu Tiên 1: Kiểm Tra Thư Viện Công Nghệ**

**Lưu Ý**: Sau khi kiểm tra code, thư viện **đã có đầy đủ** các cell cần thiết:
- ✅ OR2, OR3 (đã có trong `create_standard_library()`)
- ✅ XOR2, XNOR2 (đã có)
- ✅ AND2, AND3 (đã có)
- ✅ NAND2, NOR2 (đã có)

**Kết Luận**: Vấn đề **KHÔNG PHẢI** thiếu cell, mà là **lỗi function matching**. Xem Ưu Tiên 2 để giải quyết.

**Đề Xuất Bổ Sung** (nếu cần mở rộng):
- Thêm các cell phức tạp hơn (AOI, OAI với nhiều variants)
- Thêm các cell tối ưu cho specific use cases

#### **Ưu Tiên 2: Cải Thiện Function Matching (CRITICAL)**

**Vấn Đề**: Function matching hiện tại chỉ khớp exact match, không normalize variable names.

**Đề Xuất**: Cải thiện thuật toán khớp hàm Boolean với các bước:

1. **Normalize Variable Names** (Ưu tiên cao nhất):
   ```python
   def normalize_function(function: str) -> str:
       # OR(C,D) -> OR(A,B)
       # XOR(temp1,temp2) -> XOR(A,B)
       # Extract function name and arity
       # Replace all variables with canonical names (A, B, C, ...)
   ```

2. **Pattern Matching**: So sánh theo pattern thay vì exact string:
   - `OR(C,D)` → Pattern: `OR(2-input)` → Match với `OR2` (function: `OR(A,B)`)
   - `XOR(temp1,temp2)` → Pattern: `XOR(2-input)` → Match với `XOR2` (function: `XOR(A,B)`)

3. **Function Canonicalization**: 
   - Trích xuất tên function và số lượng inputs
   - Bỏ qua tên biến cụ thể
   - So sánh: `function_name + arity`

4. **Hỗ Trợ Nâng Cao**:
   - Hỗ trợ các phép biến đổi định luật De Morgan
   - Xử lý các ngõ vào/ra đảo
   - Hỗ trợ multi-input gates (3-input, 4-input)

**Ví Dụ Cải Thiện**:
```python
# Hiện tại (sai):
"OR(C,D)" != "OR(A,B)" → Không khớp ❌

# Sau khi normalize (đúng):
normalize("OR(C,D)") = "OR(A,B)"
normalize("OR(A,B)") = "OR(A,B)"
→ Khớp ✅
```

#### **Ưu Tiên 3: Sửa Luồng Dữ Liệu**

**Đề Xuất**: Đảm bảo technology mapping nhận đúng netlist (sau synthesis):
- Xác minh việc truyền netlist giữa synthesis và techmap
- Thêm validation để kiểm tra tính nhất quán của nodes
- Xóa bất kỳ netlist đã cache nào

---

## VI. KẾT LUẬN

### 6.1. Tóm Tắt

1. **Synthesis Flow**: 
   - ✅ Strash đã loại bỏ đúng các buffer thừa
   - ❌ DCE quá mạnh và loại bỏ sai các nodes có chức năng
   - ✅ CSE, ConstProp, Balance hoạt động đúng nhưng không có hiệu quả do vấn đề DCE

2. **Technology Mapping**:
   - ❌ Tỷ lệ thành công thấp (33.3%) do **lỗi function matching** (không normalize variable names)
   - ⚠️ Thư viện có đầy đủ OR2 và XOR2, nhưng matching không tìm thấy do khớp exact string
   - ⚠️ Không nhất quán dữ liệu giữa output synthesis và input techmap

3. **Trạng Thái Tổng Thể**: 
   - ⚠️ **CHƯA SẴN SÀNG CHO PRODUCTION** - Lỗi nghiêm trọng trong DCE ngăn cản kết quả synthesis đúng

### 6.2. Các Bước Tiếp Theo

1. **Ngay Lập Tức**: 
   - Sửa phân tích khả năng truy cập DCE để bảo toàn các nodes có chức năng
   - **Sửa function matching**: Thêm normalize variable names để `OR(C,D)` khớp với `OR(A,B)`

2. **Ngắn Hạn**: 
   - Kiểm tra và xác minh function matching hoạt động đúng với normalize
   - Thêm unit tests cho function matching với các trường hợp khác nhau

3. **Trung Hạn**: 
   - Thêm validation sau synthesis và xác minh chức năng
   - Cải thiện pattern matching cho các hàm phức tạp hơn

4. **Dài Hạn**: 
   - Triển khai kiểm tra tương đương chính thức giữa mạch trước và sau synthesis
   - Hỗ trợ De Morgan's law transformations trong matching

---

## VII. APPENDIX

### A. Vị Trí Các File

- **Mạch Nguồn**: `examples/full_adder.v`
- **Netlist Đã Synthesis**: `outputs/full_adder_synthesized_standard.json`
- **Module Synthesis**: `core/synthesis/synthesis_flow.py`
- **Module DCE**: `core/optimization/dce.py`
- **Technology Mapping**: `core/technology_mapping/technology_mapping.py`

### B. Chuỗi Lệnh Đã Sử Dụng

```bash
mylogic> read examples/full_adder.v
mylogic> stats
mylogic> synthesis standard
mylogic> techmap area
```

### C. File Log

- Log synthesis: `mylogic.log`
- Cảnh báo technology mapping được ghi lại trong terminal output

---

**Báo cáo được tạo tự động bởi MyLogic EDA Tool v2.0.0**  
**Ngày**: 2025-10-31  
**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ

