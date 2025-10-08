# 📚 MYLOGIC EDA TOOL - TÀI LIỆU THUẬT TOÁN

## 📋 Tổng quan

Thư mục `docs/` chứa tài liệu chi tiết về các thuật toán được sử dụng trong MyLogic EDA Tool. Tài liệu được viết bằng tiếng Việt để hỗ trợ việc học tập và nghiên cứu.

## 📑 Cấu trúc tài liệu

### 🎯 1. Tài liệu cơ bản
- **[Giới thiệu tổng quan](01_introduction.md)** - Tổng quan về MyLogic EDA Tool
- **[Nền tảng lý thuyết](02_theoretical_foundation.md)** - Các khái niệm cơ bản
- **[Cấu trúc dữ liệu](03_data_structures.md)** - Netlist và graph representation

### 🧮 2. Thuật toán Logic Synthesis
- **[Structural Hashing (Strash)](algorithms/01_strash.md)** - Loại bỏ duplicate nodes
- **[Dead Code Elimination (DCE)](algorithms/02_dce.md)** - Loại bỏ logic không sử dụng
- **[Common Subexpression Elimination (CSE)](algorithms/03_cse.md)** - Chia sẻ common logic
- **[Constant Propagation](algorithms/04_constprop.md)** - Propagate constants
- **[Logic Balancing](algorithms/05_balance.md)** - Cân bằng logic depth
- **[Complete Synthesis Flow](algorithms/06_synthesis_flow.md)** - Quy trình tổng hợp hoàn chỉnh

### 🔬 3. VLSI CAD Algorithms
- **[Binary Decision Diagrams (BDD)](vlsi_cad/01_bdd.md)** - Biểu diễn Boolean functions
- **[Static Timing Analysis (STA)](vlsi_cad/02_timing_analysis.md)** - Phân tích timing
- **[Technology Mapping](vlsi_cad/03_technology_mapping.md)** - Ánh xạ công nghệ

### 🧪 4. Testing và Verification
- **[Test Framework](testing/01_test_framework.md)** - Cấu trúc testing
- **[Test Cases](testing/02_test_cases.md)** - Các test cases chi tiết
- **[Performance Metrics](testing/03_performance_metrics.md)** - Đánh giá hiệu suất

### 📊 5. Benchmarks và Evaluation
- **[Benchmark Circuits](benchmarks/01_benchmark_circuits.md)** - Circuits chuẩn
- **[Performance Comparison](benchmarks/02_performance_comparison.md)** - So sánh hiệu suất
- **[Results Analysis](benchmarks/03_results_analysis.md)** - Phân tích kết quả

### 🔧 6. Tài liệu kỹ thuật
- **[API Reference](api_reference.md)** - Tham chiếu API
- **[Installation Guide](installation_guide.md)** - Hướng dẫn cài đặt
- **[Project Structure](project_structure_guide.md)** - Cấu trúc dự án

## 🎯 Cách sử dụng tài liệu

### 📖 Đọc theo trình tự
1. Bắt đầu với [Giới thiệu tổng quan](01_introduction.md)
2. Đọc [Nền tảng lý thuyết](02_theoretical_foundation.md)
3. Tìm hiểu từng thuật toán theo thứ tự
4. Tham khảo [API Reference](api_reference.md) khi cần

### 🔍 Tìm kiếm nhanh
- **Thuật toán cụ thể**: Vào thư mục `algorithms/`
- **VLSI CAD**: Vào thư mục `vlsi_cad/`
- **Testing**: Vào thư mục `testing/`
- **API**: Xem `api_reference.md`

### 💻 Thực hành
- Chạy các ví dụ trong tài liệu
- Sử dụng test suite để verify
- Tham khảo source code trong `core/`

## 📝 Quy ước viết tài liệu

### 🌐 Ngôn ngữ
- **Giải thích**: Tiếng Việt
- **Thuật ngữ kỹ thuật**: English (có giải thích)
- **Code**: Python với comments tiếng Việt

### 📊 Format
- **Headers**: Markdown format
- **Code blocks**: Syntax highlighting
- **Diagrams**: ASCII art hoặc Mermaid
- **Examples**: Rõ ràng, có thể chạy được

### 🔗 Cross-references
- Liên kết giữa các phần liên quan
- Tham chiếu đến source code
- Link đến external resources

## 🤝 Đóng góp

### 📝 Cách đóng góp
1. Fork repository
2. Tạo branch mới cho documentation
3. Viết/chỉnh sửa tài liệu
4. Submit pull request

### ✅ Guidelines
- Tuân thủ format và style
- Kiểm tra spelling và grammar
- Cập nhật cross-references
- Test các code examples

## 📞 Liên hệ

- **Issues**: Tạo issue trên GitHub
- **Discussions**: Sử dụng GitHub Discussions
- **Email**: [Your email]

---

**Lưu ý**: Tài liệu này được cập nhật thường xuyên. Hãy check version mới nhất trước khi sử dụng.
