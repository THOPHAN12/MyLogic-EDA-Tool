# 📚 MYLOGIC EDA TOOL - TÀI LIỆU CHÍNH

## 📋 Tổng quan

Thư mục `docs/` chứa tài liệu chi tiết về các thuật toán và hệ thống MyLogic EDA Tool. Tài liệu được tổ chức theo cấu trúc khoa học để hỗ trợ việc học tập, nghiên cứu và phát triển.

## 📑 Cấu trúc tài liệu mới

### 🎯 1. Tổng quan hệ thống (`00_overview/`)
- **[Giới thiệu tổng quan](00_overview/01_introduction.md)** - Tổng quan về MyLogic EDA Tool
- **[Nền tảng lý thuyết](00_overview/02_theoretical_foundation.md)** - Các khái niệm cơ bản
- **[Hướng dẫn cài đặt](00_overview/installation_guide.md)** - Cài đặt và setup
- **[Cấu trúc dự án](00_overview/project_structure_guide.md)** - Kiến trúc hệ thống
- **[Workflow tổng hợp](00_overview/combinational_workflow.md)** - Quy trình synthesis
- **[Hướng dẫn Yosys](00_overview/yosys_guide.md)** - Tích hợp Yosys
- **[Tham khảo API](00_overview/api_reference.md)** - API và interfaces

### 🧮 2. Thuật toán Logic Synthesis (`algorithms/`)
- **[Structural Hashing (Strash)](algorithms/01_strash.md)** - Loại bỏ duplicate nodes
- **[Dead Code Elimination (DCE)](algorithms/02_dce.md)** - Loại bỏ logic không sử dụng
- **[Common Subexpression Elimination (CSE)](algorithms/03_cse.md)** - Chia sẻ common logic
- **[Constant Propagation](algorithms/04_constprop.md)** - Propagate constants
- **[Logic Balancing](algorithms/05_balance.md)** - Cân bằng logic depth
- **[Complete Synthesis Flow](algorithms/README.md)** - Quy trình tổng hợp hoàn chỉnh

### 🔬 3. VLSI CAD Algorithms (`vlsi_cad/`)
- **[Binary Decision Diagrams (BDD)](vlsi_cad/bdd.md)** - Biểu diễn Boolean functions
- **[SAT Solver](vlsi_cad/sat.md)** - Boolean Satisfiability
- **[Placement Algorithms](vlsi_cad/placement.md)** - Thuật toán placement
- **[Routing Algorithms](vlsi_cad/routing.md)** - Thuật toán routing
- **[Static Timing Analysis](vlsi_cad/sta.md)** - Phân tích timing
- **[Technology Mapping](vlsi_cad/README.md)** - Ánh xạ công nghệ

### 🎮 4. Simulation (`simulation/`)
- **[Simulation Overview](simulation/simulation_overview.md)** - Tổng quan mô phỏng
- **[Vector Simulation](simulation/README.md)** - Mô phỏng vector

### 🧪 5. Testing và Verification (`testing/`)
- **[Test Framework](testing/README.md)** - Cấu trúc testing
- **[Test Cases](testing/README.md)** - Các test cases chi tiết
- **[Performance Metrics](testing/README.md)** - Đánh giá hiệu suất

### 📊 6. Benchmarks và Evaluation (`benchmarks/`)
- **[Benchmark Circuits](benchmarks/README.md)** - Circuits chuẩn
- **[Performance Comparison](benchmarks/README.md)** - So sánh hiệu suất
- **[Results Analysis](benchmarks/README.md)** - Phân tích kết quả

### 📝 7. Báo cáo dự án (`report/`)
- **[Report Outline](report/report_outline.md)** - Sườn báo cáo chi tiết

## 🎯 Cách sử dụng tài liệu

### 📖 Đọc theo trình tự
1. Bắt đầu với [Giới thiệu tổng quan](00_overview/01_introduction.md)
2. Đọc [Nền tảng lý thuyết](00_overview/02_theoretical_foundation.md)
3. Tìm hiểu từng thuật toán theo thứ tự trong `algorithms/`
4. Tham khảo [API Reference](00_overview/api_reference.md) khi cần

### 🔍 Tìm kiếm nhanh
- **Thuật toán cụ thể**: Vào thư mục `algorithms/`
- **VLSI CAD**: Vào thư mục `vlsi_cad/`
- **Simulation**: Vào thư mục `simulation/`
- **Testing**: Vào thư mục `testing/`
- **API**: Xem `00_overview/api_reference.md`

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
- **Headers**: Markdown format với emoji
- **Code blocks**: Syntax highlighting
- **Diagrams**: ASCII art hoặc Mermaid
- **Examples**: Rõ ràng, có thể chạy được

### 🔗 Cross-references
- Liên kết giữa các phần liên quan
- Tham chiếu đến source code
- Link đến external resources

## 🚀 Quick Start

### 📥 Cài đặt nhanh
```bash
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool
pip install -r requirements.txt
```

### 🎮 Sử dụng cơ bản
```bash
python mylogic.py
mylogic> read examples/full_adder.v
mylogic> simulate
mylogic> synthesis standard
```

### 📚 Đọc tài liệu
- Bắt đầu: [Giới thiệu](00_overview/01_introduction.md)
- Thuật toán: [Algorithms](algorithms/README.md)
- API: [API Reference](00_overview/api_reference.md)

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

- **GitHub Issues**: Tạo issue trên GitHub
- **Discussions**: Sử dụng GitHub Discussions
- **Repository**: https://github.com/THOPHAN12/MyLogic-EDA-Tool

---

**📅 Cập nhật**: 2025-01-12  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 2.0 (Restructured)