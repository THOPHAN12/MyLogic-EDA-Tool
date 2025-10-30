# TÀI LIỆU THAM KHẢO / REFERENCES

## 📚 DANH MỤC TÀI LIỆU THAM KHẢO

---

## I. SÁCH GIÁO KHOA / TEXTBOOKS

### Logic Synthesis và Verification

[1] G. D. Hachtel and F. Somenzi, *Logic Synthesis and Verification Algorithms*, Springer, 1996.
   - **Nội dung**: Thuật toán tối ưu hóa logic, BDD, formal verification
   - **Trích dẫn**: Section 4.2 (BDD), Section 6.1 (Logic Optimization)

[2] G. De Micheli, *Synthesis and Optimization of Digital Circuits*, McGraw-Hill, 1994.
   - **Nội dung**: Multi-level logic synthesis, technology mapping
   - **Trích dẫn**: Chapter 7 (Technology Mapping), Chapter 8 (Logic Optimization)

[3] R. K. Brayton and C. McMullen, *Logic Minimization Algorithms for VLSI Synthesis*, Springer, 1984.
   - **Nội dung**: Two-level và multi-level logic minimization
   - **Trích dẫn**: Chapter 3 (Espresso Algorithm), Chapter 5 (Don't Cares)

### VLSI Physical Design

[4] A. B. Kahng, J. Lienig, I. L. Markov, and J. Hu, *VLSI Physical Design: From Graph Partitioning to Timing Closure*, Springer, 2011.
   - **Nội dung**: Placement, routing, timing analysis, optimization
   - **Trích dẫn**: Chapter 4 (Placement), Chapter 5 (Routing), Chapter 6 (Timing)

[5] S. H. Gerez, *Algorithms for VLSI Design Automation*, John Wiley & Sons, 1999.
   - **Nội dung**: Graph algorithms, optimization theory
   - **Trích dẫn**: Chapter 2 (Graph Theory), Chapter 7 (Placement Algorithms)

### Algorithms và Data Structures

[6] T. H. Cormen, C. E. Leiserson, R. L. Rivest, and C. Stein, *Introduction to Algorithms*, 3rd ed., MIT Press, 2009.
   - **Nội dung**: Graph algorithms, data structures, complexity theory
   - **Trích dẫn**: Chapter 22 (Graph Algorithms), Chapter 34 (NP-Completeness)

[7] J. Kleinberg and É. Tardos, *Algorithm Design*, Addison-Wesley, 2005.
   - **Nội dung**: Algorithm design techniques, dynamic programming, greedy algorithms
   - **Trích dẫn**: Chapter 6 (Dynamic Programming), Chapter 13 (Approximation Algorithms)

---

## II. PAPERS VÀ CÔNG TRÌNH NGHIÊN CỨU / RESEARCH PAPERS

### Boolean Functions và BDD

[8] R. E. Bryant, "Graph-Based Algorithms for Boolean Function Manipulation," *IEEE Transactions on Computers*, vol. C-35, no. 8, pp. 677-691, August 1986.
   - **DOI**: 10.1109/TC.1986.1676819
   - **Nội dung**: Binary Decision Diagrams (BDD), ROBDD canonical form
   - **Trích dẫn**: Section 3 (BDD Operations), Section 4 (Reduction Rules)

[9] K. S. Brace, R. L. Rudell, and R. E. Bryant, "Efficient Implementation of a BDD Package," in *Proc. 27th ACM/IEEE Design Automation Conference*, 1990, pp. 40-45.
   - **DOI**: 10.1109/DAC.1990.114826
   - **Nội dung**: BDD package implementation, memory management
   - **Trích dẫn**: Section 2 (BDD Operations Efficiency)

### SAT Solving

[10] M. Davis, G. Logemann, and D. Loveland, "A Machine Program for Theorem-Proving," *Communications of the ACM*, vol. 5, no. 7, pp. 394-397, July 1962.
   - **DOI**: 10.1145/368273.368557
   - **Nội dung**: DPLL algorithm for SAT solving
   - **Trích dẫn**: Original DPLL algorithm

[11] J. P. Marques-Silva and K. A. Sakallah, "GRASP: A Search Algorithm for Propositional Satisfiability," *IEEE Transactions on Computers*, vol. 48, no. 5, pp. 506-521, May 1999.
   - **DOI**: 10.1109/12.769433
   - **Nội dung**: Conflict-Driven Clause Learning (CDCL)
   - **Trích dẫn**: Section 3 (Conflict Analysis), Section 4 (Non-chronological Backtracking)

### Logic Optimization

[12] A. Mishchenko, S. Chatterjee, and R. Brayton, "DAG-Aware AIG Rewriting: A Fresh Look at Combinational Logic Synthesis," in *Proc. 43rd Design Automation Conference*, 2006, pp. 532-535.
   - **DOI**: 10.1145/1146909.1147048
   - **Nội dung**: And-Inverter Graph (AIG) rewriting
   - **Trích dẫn**: Section 2 (AIG Structure), Section 3 (Rewriting Algorithm)

[13] S. Chatterjee, A. Mishchenko, R. K. Brayton, and A. Ng, "Fast Boolean Optimization Using Redundancy Addition and Removal," in *Proc. IEEE/ACM International Conference on Computer-Aided Design*, 2009, pp. 181-186.
   - **DOI**: 10.1109/ICCAD.2009.5361288
   - **Nội dung**: Redundancy addition and removal for optimization
   - **Trích dẫn**: Section 3 (Don't Care Computation)

[14] R. K. Brayton, G. D. Hachtel, C. T. McMullen, and A. L. Sangiovanni-Vincentelli, "Logic Minimization Algorithms for VLSI Synthesis," *Proceedings of the IEEE*, vol. 72, no. 10, pp. 1340-1362, October 1984.
   - **DOI**: 10.1109/PROC.1984.13027
   - **Nội dung**: Espresso algorithm, two-level minimization
   - **Trích dẫn**: Section 4 (Espresso Algorithm)

### Structural Hashing

[15] R. K. Brayton and A. Mishchenko, "ABC: An Academic Industrial-Strength Verification Tool," in *Proc. 22nd International Conference on Computer Aided Verification*, 2010, pp. 24-40.
   - **DOI**: 10.1007/978-3-642-14295-6_5
   - **Nội dung**: ABC tool, structural hashing, AIG manipulation
   - **Trích dẫn**: Section 2 (Structural Hashing), Section 3 (AIG Package)

### Technology Mapping

[16] K. Keutzer, "DAGON: Technology Binding and Local Optimization by DAG Matching," in *Proc. 24th ACM/IEEE Design Automation Conference*, 1987, pp. 341-347.
   - **DOI**: 10.1145/37888.37940
   - **Nội dung**: DAG-based technology mapping
   - **Trích dẫn**: Section 3 (Covering Problem)

[17] J. Cong and Y. Ding, "FlowMap: An Optimal Technology Mapping Algorithm for Delay Optimization in Lookup-Table Based FPGA Designs," *IEEE Transactions on Computer-Aided Design*, vol. 13, no. 1, pp. 1-12, January 1994.
   - **DOI**: 10.1109/43.273754
   - **Nội dung**: FlowMap algorithm for LUT mapping
   - **Trích dẫn**: Section 3 (Optimal Depth Mapping)

### Placement và Routing

[18] C. J. Alpert, T. Chan, D. J.-H. Huang, and I. Markov, "Quadratic Placement Revisited," in *Proc. 34th Design Automation Conference*, 1997, pp. 752-757.
   - **DOI**: 10.1145/266021.266277
   - **Nội dung**: Quadratic placement, force-directed methods
   - **Trích dẫn**: Section 2 (Force-Directed Placement)

[19] C. Y. Lee, "An Algorithm for Path Connections and Its Applications," *IRE Transactions on Electronic Computers*, vol. EC-10, no. 3, pp. 346-365, September 1961.
   - **DOI**: 10.1109/TEC.1961.5219222
   - **Nội dung**: Lee's maze routing algorithm
   - **Trích dẫn**: Original Lee algorithm

[20] L. McMurchie and C. Ebeling, "PathFinder: A Negotiation-Based Performance-Driven Router for FPGAs," in *Proc. 3rd ACM International Symposium on Field-Programmable Gate Arrays*, 1995, pp. 111-117.
   - **DOI**: 10.1145/201310.201328
   - **Nội dung**: PathFinder negotiation-based routing
   - **Trích dẫn**: Section 3 (Negotiation-Based Routing)

### Static Timing Analysis

[21] R. B. Hitchcock, G. L. Smith, and D. D. Cheng, "Timing Analysis of Computer Hardware," *IBM Journal of Research and Development*, vol. 26, no. 1, pp. 100-105, January 1982.
   - **DOI**: 10.1147/rd.261.0100
   - **Nội dung**: Static timing analysis fundamentals
   - **Trích dẫn**: Section 2 (Arrival Time Computation)

---

## III. CÔNG CỤ VÀ OPEN-SOURCE PROJECTS / TOOLS AND OPEN-SOURCE

### ABC (Berkeley Logic Synthesis)

[22] Berkeley Logic Synthesis and Verification Group, "ABC: A System for Sequential Synthesis and Verification," 
   - **URL**: https://people.eecs.berkeley.edu/~alanmi/abc/
   - **Trích dẫn**: ABC tool reference, AIG manipulation

### Yosys

[23] C. Wolf, "Yosys Open SYnthesis Suite," 
   - **URL**: http://www.clifford.at/yosys/
   - **GitHub**: https://github.com/YosysHQ/yosys
   - **Trích dẫn**: Yosys synthesis framework

[24] C. Wolf, J. Glaser, and J. Kepler, "Yosys - A Free Verilog Synthesis Suite," in *Proc. 21st Austrian Workshop on Microelectronics (Austrochip)*, 2013.
   - **Trích dẫn**: Yosys architecture and design

### SIS (UC Berkeley Synthesis System)

[25] E. M. Sentovich et al., "SIS: A System for Sequential Circuit Synthesis," University of California, Berkeley, Tech. Rep. UCB/ERL M92/41, May 1992.
   - **Trích dẫn**: SIS command reference, multi-level optimization

---

## IV. TIÊU CHUẨN VÀ SPECIFICATION / STANDARDS AND SPECIFICATIONS

### Verilog HDL

[26] IEEE Standard for Verilog Hardware Description Language, IEEE Std 1364-2005, 2006.
   - **DOI**: 10.1109/IEEESTD.2006.99495
   - **Trích dẫn**: Verilog language reference

### Liberty Format

[27] Synopsys, Inc., "Liberty User Guide and Reference Manual Suite Version 2013.03," March 2013.
   - **Trích dẫn**: Liberty (.lib) file format specification

---

## V. KHÓA LUẬN VÀ ĐỒ ÁN / THESES AND PROJECTS

[28] MyLogic EDA Tool Development Team, "MyLogic: A Comprehensive Open-Source EDA Tool for Logic Synthesis and Optimization," Đồ Án 2, 2025.
   - **Trích dẫn**: Đồ án này

---

## VI. WEBSITE VÀ TÀI NGUYÊN ONLINE / WEBSITES AND ONLINE RESOURCES

### Educational Resources

[29] Berkeley EECS Courses, "CS 294-2: Synthesis and Verification of Digital Systems,"
   - **URL**: https://people.eecs.berkeley.edu/~alanmi/courses/
   - **Trích dẫn**: Course materials on logic synthesis

[30] MIT OpenCourseWare, "6.374: Analysis and Design of Digital Integrated Circuits,"
   - **URL**: https://ocw.mit.edu/
   - **Trích dẫn**: Digital circuit design fundamentals

---

## VII. PHÂN LOẠI THEO CHỦ ĐỀ / CLASSIFICATION BY TOPIC

### Boolean Algebra và Logic Design
- [1], [2], [3], [8], [9], [14]

### Binary Decision Diagrams (BDD)
- [1], [8], [9]

### SAT Solving
- [10], [11]

### Logic Optimization
- [1], [2], [3], [12], [13], [14], [15]

### Technology Mapping
- [2], [16], [17]

### VLSI Physical Design
- [4], [5], [18], [19], [20]

### Timing Analysis
- [4], [21]

### Graph Theory và Algorithms
- [5], [6], [7]

### Tools và Software
- [22], [23], [24], [25]

---

## VIII. GLOSARY / THUẬT NGỮ

- **AIG**: And-Inverter Graph
- **BDD**: Binary Decision Diagram
- **CDCL**: Conflict-Driven Clause Learning
- **CNF**: Conjunctive Normal Form
- **CSE**: Common Subexpression Elimination
- **DAG**: Directed Acyclic Graph
- **DCE**: Dead Code Elimination
- **DPLL**: Davis-Putnam-Logemann-Loveland
- **EDA**: Electronic Design Automation
- **FPGA**: Field-Programmable Gate Array
- **LUT**: Look-Up Table
- **ODC**: Observability Don't Care
- **ROBDD**: Reduced Ordered Binary Decision Diagram
- **SAT**: Boolean Satisfiability
- **SDC**: Satisfiability Don't Care
- **STA**: Static Timing Analysis

---

## IX. PHỤ LỤC / APPENDIX

### A. Công thức trích dẫn / Citation Format

**IEEE Style (sử dụng trong đồ án này):**
```
[Số] Tác giả, "Tiêu đề," Tên tạp chí/hội nghị, vol. X, no. Y, pp. Z-W, Tháng Năm.
```

**Ví dụ:**
```
[1] G. D. Hachtel and F. Somenzi, Logic Synthesis and Verification Algorithms, Springer, 1996.
```

### B. Cách trích dẫn trong văn bản / In-text Citation

**Format:**
- Trích dẫn đơn: "...như đã trình bày trong [1]..."
- Trích dẫn nhiều: "...các nghiên cứu [1], [5], [12] đã chỉ ra..."
- Trích dẫn liên tiếp: "...theo [1]-[3]..."

---

**Cập nhật**: 2025-10-30  
**Phiên bản**: 1.0  
**Người biên soạn**: MyLogic Development Team

**Lưu ý**: Tài liệu tham khảo được cập nhật liên tục khi có thêm nguồn mới.

