# BÁO CÁO SYNTHESIS VÀ TECHNOLOGY MAPPING

Thư mục này chứa các báo cáo kết quả synthesis và technology mapping của MyLogic EDA Tool.

---

## Files trong thư mục

### 1. `full_adder_synthesis_report.md`
**Báo cáo chi tiết** dạng Markdown về kết quả synthesis và technology mapping của full adder.

**Nội dung**:
- Thông tin circuit ban đầu
- Kết quả từng bước synthesis (Strash, DCE, CSE, ConstProp, Balance)
- Kết quả technology mapping
- Phân tích và đánh giá
- Đề xuất khắc phục
- Kết luận

**Định dạng**: Markdown (.md)

---

### 2. `full_adder_summary.json`
**Báo cáo tóm tắt** dạng JSON với dữ liệu có cấu trúc.

**Nội dung**:
- Metadata của báo cáo
- Thông tin circuit
- Dữ liệu từng bước synthesis
- Tóm tắt kết quả
- Danh sách issues và recommendations

**Định dạng**: JSON (.json) - dễ dàng parse và phân tích bằng script

---

## Cách sử dụng

### Xem báo cáo chi tiết:
```bash
cat reports/full_adder_synthesis_report.md
# hoặc mở bằng editor
```

### Parse JSON summary:
```python
import json
with open('reports/full_adder_summary.json') as f:
    report = json.load(f)
    print(f"Synthesis status: {report['test_results']['synthesis_flow']}")
```

---

## Cấu trúc báo cáo

### Synthesis Report Structure:
1. **Thông tin đồ án**: Metadata về đề tài, tool version
2. **Thông tin circuit ban đầu**: Statistics, node distribution
3. **Kết quả synthesis**: Từng bước với metrics chi tiết
4. **Kết quả technology mapping**: Mapping success rate, cell usage
5. **Phân tích và đánh giá**: Issues, root cause analysis
6. **Đề xuất khắc phục**: Recommendations theo priority
7. **Kết luận**: Summary và next steps

---

## Test Cases

| Circuit | Report | Status |
|---------|--------|--------|
| full_adder | ✅ | Có issues (DCE too aggressive) |

---

**Lưu ý**: Các báo cáo được tạo tự động từ terminal output và analysis của synthesis flow.

**Tool**: MyLogic EDA Tool v2.0.0  
**Đề tài**: Phát triển công cụ tổng hợp, tối ưu luận lý, và ánh xạ công nghệ

