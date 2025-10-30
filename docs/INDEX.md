# MyLogic EDA Tool - Documentation Index

## 📚 Hệ Thống Tài Liệu Hoàn Chỉnh

Tài liệu được tổ chức theo logic từ tổng quan đến chi tiết cụ thể.

---

## 🎯 1. BẮT ĐẦU (Getting Started)

### 1.1. Tài Liệu Chính
- **[QUICKSTART.md](QUICKSTART.md)** ⭐
  - Hướng dẫn nhanh cho người mới
  - Cài đặt và chạy dự án
  - Ví dụ thực tế
  - Checklist bắt đầu

### 1.2. Hướng Dẫn Synthesis
- **[SYNTHESIS_GUIDE.md](SYNTHESIS_GUIDE.md)**
  - Chi tiết về synthesis flow (5 bước)
  - Optimization levels (basic/standard/aggressive)
  - Cách chạy synthesis
  - Troubleshooting

### 1.3. Tài Liệu Đầy Đủ
- **[COMPLETE_DOCUMENTATION.md](COMPLETE_DOCUMENTATION.md)**
  - Tổng quan toàn bộ project
  - Cấu trúc thư mục chi tiết
  - Logic flow đầy đủ
  - Professional standards

---

## 📖 2. LÝ THUYẾT CƠ BẢN (Theoretical Foundation)

### 2.1. Giới Thiệu Tổng Quan
- **[00_overview/01_introduction.md](00_overview/01_introduction.md)**
  - Giới thiệu về EDA Tools
  - Mục đích của MyLogic
  - Kiến trúc hệ thống
  - Use cases

### 2.2. Nền Tảng Lý Thuyết
- **[00_overview/02_theoretical_foundation.md](00_overview/02_theoretical_foundation.md)**
  - Boolean Algebra & Logic Design
  - Synthesis Algorithms (Strash, DCE, CSE)
  - Optimization Techniques
  - VLSI CAD Concepts

### 2.3. Cấu Trúc Dự Án
- **[00_overview/project_structure_guide.md](00_overview/project_structure_guide.md)**
  - Tổ chức thư mục
  - Module relationships
  - Design patterns
  - Best practices

---

## 🔧 3. CÁC THUẬT TOÁN (Algorithms)

### 3.1. Tổng Quan
- **[algorithms/README.md](algorithms/README.md)**
  - Overview tất cả algorithms
  - Phân loại theo chức năng
  - Complexity analysis

### 3.2. Lý Thuyết Chuyên Sâu
- **[00_overview/03_mathematical_foundations.md](00_overview/03_mathematical_foundations.md)** ⭐
  - Boolean Algebra & Graph Theory
  - BDD Theory & SAT Algorithms
  - Optimization Theory & Complexity Classes
  - Data Structures for EDA
  - Numerical Methods

- **[algorithms/SYNTHESIS_THEORY.md](algorithms/SYNTHESIS_THEORY.md)** ⭐
  - Structural Hashing Theory
  - AIG (And-Inverter Graph)
  - Multi-Level Logic Optimization
  - Technology-Independent Optimization
  - Equivalence Checking
  - Formal Verification

- **[algorithms/VLSI_CAD_THEORY.md](algorithms/VLSI_CAD_THEORY.md)** ⭐
  - BDD Algorithms Chi Tiết
  - SAT Solving (DPLL, CDCL)
  - Placement Algorithms (Force-Directed, SA)
  - Routing Algorithms (Lee, A*, PathFinder)
  - Static Timing Analysis
  - Power Analysis

### 3.3. Optimization Algorithms
- **[../core/optimization/README.md](../core/optimization/README.md)** ⭐
  - Dead Code Elimination (DCE) - Lý thuyết đầy đủ
  - Common Subexpression Elimination (CSE) - Formal definition
  - Constant Propagation (ConstProp) - Data flow analysis
  - Logic Balancing (Balance) - Level optimization
  - Complexity Analysis & Correctness Proofs

### 3.4. Synthesis Algorithms
- **[../core/synthesis/README.md](../core/synthesis/README.md)**
  - Structural Hashing (Strash)
  - Complete Synthesis Flow
  - ABC Integration

### 3.5. Implementation Details
- **Core Optimization:** `../core/optimization/` - DCE, CSE, ConstProp, Balance
- **Core Synthesis:** `../core/synthesis/` - Strash, Synthesis Flow
- **VLSI CAD:** `../core/vlsi_cad/` - BDD, SAT, Placement, Routing, Timing

### 3.6. VLSI CAD Algorithms
- **[vlsi_cad/README.md](vlsi_cad/README.md)**
  - Binary Decision Diagrams (BDD)
  - SAT Solver
  - Placement & Routing
  - Timing Analysis

### 3.7. Mathematical Foundations
- **[00_overview/03_mathematical_foundations.md](00_overview/03_mathematical_foundations.md)** ⭐⭐⭐
  - **Boolean Algebra:** Functions, Normal Forms, Laws
  - **Graph Theory:** DAG, Hypergraph, Algorithms
  - **BDD Theory:** Shannon Expansion, ROBDD Properties
  - **SAT:** DPLL, CDCL, Complexity
  - **Graph Algorithms:** MST, Dijkstra, Max Flow
  - **Optimization:** Simulated Annealing, Force-Directed
  - **Timing:** Static Timing Analysis, Critical Path
  - **Technology Mapping:** Covering Problem, LUT Mapping
  - **Complexity Theory:** P, NP, NP-Complete, Approximations
  - **Data Structures:** Union-Find, Hash Tables, Spatial Structures

---

## 🧪 4. MÔ PHỎNG (Simulation)

### 4.1. Tổng Quan Simulation
- **[simulation/simulation_overview.md](simulation/simulation_overview.md)**
  - Scalar vs Vector simulation
  - Arithmetic simulation
  - Logic simulation
  - Timing simulation

### 4.2. Implementation Details
- **[../core/simulation/README.md](../core/simulation/README.md)**
  - Architecture
  - APIs
  - Examples

---

## 🔌 5. PARSERS & FRONTENDS

### 5.1. Verilog Parser
- **[../frontends/README.md](../frontends/README.md)**
  - Parser overview
  - Modular structure
  - Refactoring history

### 5.2. Parser Architecture
- **[../frontends/verilog/docs/INDEX.md](../frontends/verilog/docs/INDEX.md)**
  - Core components
  - Operations modules
  - Expression parsing

### 5.3. Design & Reuse
- **[../frontends/verilog/docs/ARCHITECTURE.md](../frontends/verilog/docs/ARCHITECTURE.md)**
  - Design patterns
  - Code reuse strategy
  - Extensibility

---

## 🔬 6. TECHNOLOGY MAPPING & TECHLIBS

### 6.1. Technology Mapping
- **[../core/technology_mapping/README.md](../core/technology_mapping/README.md)**
  - LUT-based mapping
  - Cell library mapping
  - Area optimization

### 6.2. Technology Libraries
- **[../techlibs/INDEX.md](../techlibs/INDEX.md)**
  - ASIC libraries
  - FPGA vendor libraries (Yosys integration)
  - Library organization

---

## 🧪 7. TESTING & VALIDATION

### 7.1. Testing Strategy
- **[testing/README.md](testing/README.md)**
  - Unit tests
  - Integration tests
  - Test coverage
  - CI/CD

### 7.2. Examples & Benchmarks
- **[../examples/](../examples/)**
  - full_adder.v
  - comprehensive_combinational.v
  - priority_encoder.v
  - arithmetic_operations.v

---

## 🛠️ 8. TOOLS & UTILITIES

### 8.1. Visualization Tools
- **[../tools/visualizers/README.md](../tools/visualizers/README.md)**
  - SVG generation
  - Netlist visualization
  - Demo tools

### 8.2. Analysis Tools
- **[../tools/analyzers/README.md](../tools/analyzers/README.md)**
  - Cell type analysis
  - Format comparison
  - Structure analysis

### 8.3. Converters
- **[../tools/converters/README.md](../tools/converters/README.md)**
  - Format conversion
  - Yosys compatibility

---

## 📊 9. REPORTS & BENCHMARKS

### 9.1. Benchmark Results
- **[report/](report/)** (if exists)
  - Performance metrics
  - Comparison with other tools
  - Optimization statistics

---

## 🤝 10. CONTRIBUTING & DEVELOPMENT

### 10.1. How to Contribute
- **[../tools/CONTRIBUTING.md](../tools/CONTRIBUTING.md)**
  - Code style
  - Pull request process
  - Development workflow

### 10.2. Changelog
- **[../tools/CHANGELOG.md](../tools/CHANGELOG.md)**
  - Version history
  - Feature additions
  - Bug fixes

---

## 📋 CẤU TRÚC LOGIC CỦA TÀI LIỆU

```
QUICKSTART → Bắt đầu nhanh
    ↓
SYNTHESIS_GUIDE → Hiểu về synthesis
    ↓
COMPLETE_DOCUMENTATION → Toàn bộ chi tiết
    ↓
Lý thuyết (00_overview/) → Nền tảng
    ↓
Algorithms → Hiểu thuật toán
    ↓
Implementation (core/) → Code thực tế
    ↓
Testing → Kiểm tra
```

---

## 🎯 LỘ TRÌNH HỌC TẬP KHUYẾN NGHỊ

### Người Mới Bắt Đầu (Beginner)
1. ✅ QUICKSTART.md - Chạy thử ngay
2. ✅ 00_overview/01_introduction.md - Hiểu tổng quan
3. ✅ SYNTHESIS_GUIDE.md - Học synthesis
4. ✅ Examples - Thử các ví dụ

### Trung Cấp (Intermediate)
1. ✅ 00_overview/02_theoretical_foundation.md
2. ✅ 00_overview/03_mathematical_foundations.md ⭐
3. ✅ algorithms/README.md
4. ✅ core/optimization/README.md
5. ✅ frontends/README.md

### Nâng Cao (Advanced)
1. ✅ COMPLETE_DOCUMENTATION.md
2. ✅ algorithms/SYNTHESIS_THEORY.md ⭐⭐
3. ✅ algorithms/VLSI_CAD_THEORY.md ⭐⭐
4. ✅ vlsi_cad/README.md
5. ✅ core/simulation/README.md
6. ✅ Source code trong core/

### Nghiên Cứu (Research)
1. ✅ 00_overview/03_mathematical_foundations.md ⭐⭐⭐ - Toán học nền tảng
2. ✅ algorithms/SYNTHESIS_THEORY.md ⭐⭐⭐ - Synthesis algorithms formal
3. ✅ algorithms/VLSI_CAD_THEORY.md ⭐⭐⭐ - VLSI CAD algorithms formal
4. ✅ core/optimization/README.md - Optimization theory với proofs
5. ✅ benchmarks/ - Kết quả benchmark
6. ✅ Source code - Phân tích implementation
7. ✅ tools/ - Extend & customize

---

## 🔍 TÌM KIẾM NHANH

### Tôi muốn...

**...chạy dự án ngay:**
→ [QUICKSTART.md](QUICKSTART.md)

**...hiểu synthesis flow:**
→ [SYNTHESIS_GUIDE.md](SYNTHESIS_GUIDE.md)

**...hiểu lý thuyết EDA:**
→ [00_overview/02_theoretical_foundation.md](00_overview/02_theoretical_foundation.md)

**...nền tảng toán học:**
→ [00_overview/03_mathematical_foundations.md](00_overview/03_mathematical_foundations.md) ⭐

**...lý thuyết synthesis chi tiết:**
→ [algorithms/SYNTHESIS_THEORY.md](algorithms/SYNTHESIS_THEORY.md) ⭐

**...lý thuyết VLSI CAD chi tiết:**
→ [algorithms/VLSI_CAD_THEORY.md](algorithms/VLSI_CAD_THEORY.md) ⭐

**...xem code optimization:**
→ [../core/optimization/](../core/optimization/)

**...xem parser implementation:**
→ [../frontends/verilog/](../frontends/verilog/)

**...tích hợp Yosys:**
→ [../integrations/yosys/](../integrations/yosys/)

**...customize tools:**
→ [../tools/](../tools/)

**...contribute code:**
→ [../tools/CONTRIBUTING.md](../tools/CONTRIBUTING.md)

---

## 📞 HỖ TRỢ

Nếu gặp vấn đề:
1. Kiểm tra [QUICKSTART.md](QUICKSTART.md) - Troubleshooting section
2. Xem [SYNTHESIS_GUIDE.md](SYNTHESIS_GUIDE.md) - Common issues
3. Đọc source code READMEs
4. Tạo issue trên GitHub

---

**Cập nhật**: 2025-10-30  
**Version**: 2.0.0  
**Tác giả**: MyLogic Development Team

