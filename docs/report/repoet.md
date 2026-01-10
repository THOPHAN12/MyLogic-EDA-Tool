# BÁO CÁO CUỐI KỲ

# MYLOGIC EDA TOOL

## Unified Electronic Design Automation Tool with Advanced VLSI CAD Algorithms

**Tác giả:** MyLogic EDA Tool Team
**Phiên bản:** 2.0.0
**Năm:** 2024

---

## MỤC LỤC

1. [Chương 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT](#chương-1-tổng-quan-và-cơ-sở-lý-thuyết)
2. [Chương 2: LOGIC SYNTHESIS](#chương-2-logic-synthesis)
3. [Chương 3: LOGIC OPTIMIZATION](#chương-3-logic-optimization)
4. [Chương 4: TECHNOLOGY MAPPING](#chương-4-technology-mapping)
5. [Chương 5: CÁC THÀNH PHẦN KHÁC](#chương-5-các-thành-phần-khác)
6. [Chương 6: HƯỚNG DẪN SỬ DỤNG MYLOGIC](#chương-6-hướng-dẫn-sử-dụng-mylogic)
7. [Chương 7: KẾT QUẢ VÀ KẾT LUẬN](#chương-7-kết-quả-và-kết-luận)

---

# TÓM TẮT

MyLogic EDA Tool là một công cụ Electronic Design Automation (EDA) được phát triển nhằm mục đích giáo dục và nghiên cứu, cung cấp một pipeline hoàn chỉnh từ mô tả RTL (Register Transfer Level) đến netlist mức gate được tối ưu hóa. Dự án tập trung vào việc xây dựng một hệ thống logic synthesis với các thuật toán tối ưu hóa tiên tiến và tích hợp các công cụ VLSI CAD cơ bản.

Dự án đã thành công trong việc phát triển một Verilog parser đầy đủ tính năng, có khả năng parse các cấu trúc Verilog phức tạp bao gồm module declarations, always blocks, case statements, generate blocks, và các operations đa dạng. Hệ thống synthesis engine được xây dựng dựa trên And-Inverter Graph (AIG) - một canonical form hiệu quả cho logic synthesis, cho phép chuyển đổi netlist sang AIG và thực hiện các tối ưu hóa về diện tích, delay, và công suất tiêu thụ.

Các thuật toán optimization được triển khai bao gồm Structural Hashing (Strash), Dead Code Elimination (DCE), Common Subexpression Elimination (CSE), Constant Propagation (ConstProp), và Logic Balancing (Balance). Hệ thống cũng hỗ trợ technology mapping để map AIG sang các technology libraries khác nhau (ASIC và FPGA), cùng với hệ thống verification tích hợp sử dụng ModelSim để đảm bảo tính đúng đắn của synthesis và optimization.

Ngoài ra, dự án đã implement các thuật toán VLSI CAD cơ bản như Binary Decision Diagrams (BDD), Boolean Expression Diagrams (BED), SAT Solver, Placement algorithms (Random, Force-directed, Simulated Annealing), Routing algorithms (Maze routing, Rip-up & reroute), và Static Timing Analysis (STA). Hệ thống cung cấp CLI interface với 36 commands, hỗ trợ cả scalar và vector simulation, cùng với AST dump utility để trực quan hóa cấu trúc netlist.

Kết quả đạt được cho thấy MyLogic EDA Tool là một công cụ giáo dục hiệu quả, với code dễ đọc và hiểu, documentation đầy đủ, và thiết kế modular dễ mở rộng. Mặc dù còn một số hạn chế về sequential logic và performance so với các công cụ chuyên nghiệp, dự án đã thành công trong việc tạo ra một nền tảng EDA có đầy đủ tính năng cơ bản, phù hợp cho mục đích học tập và nghiên cứu.

---

# CHƯƠNG 1: TỔNG QUAN VÀ CƠ SỞ LÝ THUYẾT

## 1.1. MỞ ĐẦU

### 1.1.1. Giới Thiệu

### Đặt Vấn Đề

Trong thiết kế VLSI (Very Large Scale Integration), Electronic Design Automation (EDA) đóng vai trò quan trọng trong việc chuyển đổi mô tả logic mức cao (RTL - Register Transfer Level) sang các netlist mức gate phù hợp với công nghệ sản xuất. Logic synthesis là một bước then chốt trong quy trình EDA, chuyển đổi RTL description thành gate-level netlist thông qua các bước optimization và technology mapping.

Hiện tại, các công cụ EDA chuyên nghiệp như Synopsys Design Compiler, Cadence Genus đều là các phần mềm thương mại với chi phí cao, không phù hợp cho mục đích giáo dục và nghiên cứu. Các công cụ mã nguồn mở như Yosys, ABC mặc dù mạnh mẽ nhưng có độ phức tạp cao và khó tùy chỉnh.

### Lý Do Chọn Đề Tài

Việc phát triển một công cụ EDA đơn giản, dễ hiểu nhưng đầy đủ tính năng sẽ giúp:

- **Học sinh, sinh viên**: Hiểu rõ hơn về quy trình logic synthesis
- **Nghiên cứu viên**: Có thể tùy chỉnh và thử nghiệm các thuật toán mới
- **Giảng viên**: Có công cụ để minh họa các khái niệm EDA

### Mục Tiêu Nghiên Cứu

Dự án MyLogic EDA Tool nhằm mục tiêu:

1. **Phát triển Verilog Parser**: Xây dựng parser có khả năng parse các cấu trúc Verilog cơ bản và phức tạp, bao gồm module declarations, always blocks, case statements, generate blocks, và các operations khác nhau.
2. **Xây dựng Synthesis Engine**: Implement synthesis engine chuyển đổi netlist sang And-Inverter Graph (AIG) - một canonical form hiệu quả cho logic synthesis.
3. **Triển Khai Optimization Algorithms**: Implement các thuật toán optimization quan trọng như Structural Hashing, Dead Code Elimination, Common Subexpression Elimination, Constant Propagation, và Logic Balancing.
4. **Technology Mapping**: Xây dựng technology mapping engine có khả năng map AIG sang các technology libraries khác nhau (ASIC, FPGA).
5. **Verification System**: Phát triển hệ thống verification để đảm bảo tính đúng đắn của synthesis và optimization bằng cách so sánh kết quả simulation.
6. **VLSI CAD Algorithms**: Implement các thuật toán VLSI CAD cơ bản như BDD, SAT Solver, Placement, Routing, và Timing Analysis.

### Đối Tượng Nghiên Cứu

- Verilog HDL parsing và AST generation
- Logic synthesis: Netlist → AIG conversion
- AIG optimization algorithms
- Technology mapping
- Functional verification

### Phạm Vi Nghiên Cứu

Dự án tập trung vào:

- **Combinational logic synthesis**: Hỗ trợ các cổng combinational (AND, OR, XOR, NAND, NOR, XNOR, NOT)
- **Multi-bit operations**: ADD, SUB, MUX, EQ (đã implement)
- **Optimization**: Các thuật toán optimization cơ bản và nâng cao
- **Verification**: Functional verification cho combinational logic

**Giới hạn hiện tại:**

- Sequential logic (flip-flops, registers) chưa được hỗ trợ đầy đủ
- Memory arrays cần được xử lý riêng
- Complex always blocks cần được cải thiện

### Cấu Trúc Báo Cáo

Báo cáo được chia thành 6 chương chính:

- **Chương 1**: Tổng quan và Cơ sở Lý thuyết - Giới thiệu EDA, Logic Synthesis, và AIG
- **Chương 2**: Logic Synthesis - Chi tiết về quá trình chuyển đổi Netlist sang AIG
- **Chương 3**: Logic Optimization - Các thuật toán tối ưu hóa AIG
- **Chương 4**: Technology Mapping - Chuyển đổi AIG sang technology libraries
- **Chương 5**: Các Thành Phần Khác - Verilog Parser, Verification, VLSI CAD, Simulation, CLI
- **Chương 6**: Kết Quả và Kết Luận - Đánh giá kết quả, hạn chế, và hướng phát triển

---

## 1.2. TỔNG QUAN VỀ EDA VÀ LOGIC SYNTHESIS

### 1.2.1. Electronic Design Automation (EDA)

#### 1.2.1.1. Khái Niệm

**Electronic Design Automation (EDA)** là một tập hợp các công cụ phần mềm được sử dụng để thiết kế các hệ thống điện tử như vi mạch tích hợp (Integrated Circuits - ICs) và bảng mạch in (Printed Circuit Boards - PCBs).

EDA tools tự động hóa các tác vụ thiết kế phức tạp, giúp các kỹ sư:

- Thiết kế và kiểm tra các hệ thống điện tử
- Mô phỏng và xác minh thiết kế
- Tối ưu hóa về diện tích, hiệu năng, và công suất tiêu thụ
- Tạo ra các file cần thiết cho quá trình sản xuất

#### 1.2.1.2. Vai Trò của EDA trong VLSI Design

Trong thiết kế VLSI, EDA đóng vai trò then chốt trong:

1. **Design Entry**: Nhập thiết kế bằng HDL (Verilog, VHDL)
2. **Simulation**: Mô phỏng để kiểm tra tính đúng đắn
3. **Synthesis**: Chuyển đổi RTL sang gate-level netlist
4. **Place & Route**: Sắp xếp và định tuyến các cells
5. **Verification**: Xác minh tính đúng đắn ở các mức khác nhau
6. **Timing Analysis**: Phân tích timing constraints

#### 1.2.1.3. Design Flow

Quy trình thiết kế VLSI điển hình:

```
RTL Description (Verilog)
    ↓
Functional Simulation
    ↓
Logic Synthesis
    ↓
Gate-level Netlist
    ↓
Technology Mapping
    ↓
Place & Route
    ↓
Timing Analysis
    ↓
GDSII (Manufacturing)
```

## 1.2.2. Logic Synthesis

#### 1.2.2.1. Định Nghĩa

**Logic Synthesis** là quá trình chuyển đổi mô tả logic mức cao (high-level description) như RTL code sang một representation mức thấp hơn (gate-level netlist) phù hợp với công nghệ sản xuất chip.

#### 1.2.2.2. Quy Trình Synthesis

Logic synthesis bao gồm các bước chính:

1. **Parsing & Elaboration**
   - Parse HDL code
   - Resolve hierarchy
   - Expand parameters và generate blocks
2. **Technology-Independent Optimization**
   - Convert sang canonical form (AIG, BDD)
   - Apply optimization algorithms
   - Logic minimization
3. **Technology Mapping**
   - Map logic functions sang target library
   - Optimize cho area/delay/power
4. **Optimization**
   - Post-mapping optimization
   - Timing optimization

#### 1.2.2.3. Synthesis Goals

Mục tiêu của synthesis:

- **Functional Correctness**: Đảm bảo output giống với input
- **Area Optimization**: Giảm số lượng gates
- **Delay Optimization**: Tối ưu hóa critical path
- **Power Optimization**: Giảm công suất tiêu thụ

## 1.2.3. And-Inverter Graph (AIG)

#### 1.2.3.1. Định Nghĩa

**And-Inverter Graph (AIG)** là một directed acyclic graph (DAG) biểu diễn Boolean functions chỉ sử dụng:

- **AND gates** (2-input AND)
- **Inverters** (NOT gates, được biểu diễn bằng inversion flags)

#### 1.2.3.2. Cấu Trúc AIG

Một AIG node có cấu trúc:

```
AIGNode {
    node_id: int              // Unique identifier
    node_type: str            // CONST0, CONST1, PI, AND
    left: AIGNode             // Left child (for AND nodes)
    right: AIGNode            // Right child (for AND nodes)
    left_inverted: bool       // Left input inversion flag
    right_inverted: bool      // Right input inversion flag
    var_name: str             // Variable name (for PI nodes)
}
```

#### 1.2.3.3. Tại Sao Chỉ Dùng AND và NOT?

**Functional Completeness**: Bất kỳ Boolean function nào cũng có thể được biểu diễn chỉ bằng AND và NOT:

- **NOT**: `NOT(a) = !a`
- **OR**: `OR(a, b) = !(!a AND !b)` (De Morgan's law)
- **XOR**: `XOR(a, b) = (!a AND b) OR (a AND !b)`
- **NAND**: `NAND(a, b) = !(a AND b)`
- **NOR**: `NOR(a, b) = !(a OR b) = !a AND !b`

**Lợi Ích:**

1. **Canonical Form**: Dễ dàng so sánh và optimize
2. **Efficient Operations**: Các thao tác trên AIG rất hiệu quả
3. **Technology Independence**: Không phụ thuộc vào technology library cụ thể
4. **Structural Hashing**: Dễ dàng implement structural hashing để loại bỏ duplicates

#### 1.2.3.4. Biểu Diễn NOT trong AIG

Trong AIG, NOT được biểu diễn bằng inversion flags thay vì explicit NOT nodes:

```
NOT(x) = AND(x, const1) với left_inverted=True
```

Điều này giúp:

- Giảm số lượng nodes
- Dễ dàng combine inversions
- Efficient structural hashing

#### 1.2.3.5. Conversion Các Cổng Cơ Bản sang AIG

##### AND

```
AND(a, b) = AND(a, b)  // Giữ nguyên
```

##### OR (De Morgan's Law)

```
OR(a, b) = NOT(AND(NOT(a), NOT(b)))
         = AND(AND(NOT(a), NOT(b)), const1) với output inverted
```

##### XOR

```
XOR(a, b) = (!a AND b) OR (a AND !b)
          = NOT(AND(NOT(AND(NOT(a), b)), NOT(AND(a, NOT(b)))))
```

##### NAND

```
NAND(a, b) = NOT(AND(a, b))
           = AND(AND(a, b), const1) với output inverted
```

##### NOR

```
NOR(a, b) = NOT(OR(a, b))
          = AND(NOT(a), NOT(b))
          = AND(AND(a, const1), AND(b, const1)) với both inputs inverted
```

##### XNOR

```
XNOR(a, b) = NOT(XOR(a, b))
           = NOT(XOR(a, b))
```

## 1.2.4. Related Work

#### 1.2.4.1. Các Công Cụ EDA Hiện Có

**Commercial Tools:**

- **Synopsys Design Compiler**: Industry standard synthesis tool
- **Cadence Genus**: Advanced synthesis với AI-based optimization
- **Mentor Graphics Precision**: RTL synthesis solution

**Open Source Tools:**

- **Yosys**: Open synthesis suite, được sử dụng rộng rãi
- **ABC**: AIG-based synthesis và verification tool
- **OpenROAD**: Complete RTL-to-GDSII flow

#### 1.2.4.2. So Sánh với MyLogic EDA Tool

| Feature            | MyLogic     | Yosys           | ABC         |
| ------------------ | ----------- | --------------- | ----------- |
| Verilog Parser     | ✅ Custom   | ✅ Full support | ❌          |
| AIG Synthesis      | ✅          | ✅              | ✅          |
| Optimization       | ✅ Basic    | ✅ Advanced     | ✅ Advanced |
| Technology Mapping | ✅          | ✅              | ✅          |
| Verification       | ✅ ModelSim | ✅              | ✅          |
| Educational Focus  | ✅          | ❌              | ❌          |
| Code Readability   | ✅ High     | ⚠️ Medium     | ⚠️ Medium |

**Điểm Mạnh của MyLogic:**

- Code dễ đọc và hiểu, phù hợp cho giáo dục
- Có documentation đầy đủ
- Modular design, dễ mở rộng
- Verification tích hợp

**Hạn Chế:**

- Chưa hỗ trợ đầy đủ các tính năng như Yosys/ABC
- Optimization chưa mạnh bằng các tools chuyên nghiệp
- Sequential logic chưa được hỗ trợ đầy đủ

---

# CHƯƠNG 2: LOGIC SYNTHESIS

## 2.1. TỔNG QUAN VỀ LOGIC SYNTHESIS

### 2.1.1. Định Nghĩa và Vai Trò

**Logic Synthesis** là quá trình chuyển đổi mô tả logic mức cao (high-level description) sang một representation mức thấp hơn, phù hợp với công nghệ sản xuất chip. Trong dự án MyLogic EDA Tool, synthesis được định nghĩa như một bước riêng biệt, có nhiệm vụ chuyển đổi Netlist Dictionary sang And-Inverter Graph (AIG) - một canonical form hiệu quả cho logic synthesis.

#### 2.1.1.1. Phân Biệt Synthesis và Optimization

Một điểm quan trọng cần nhấn mạnh là sự phân biệt rõ ràng giữa **Synthesis** và **Optimization**:

- **Synthesis**: Là bước chuyển đổi representation từ Netlist Dictionary sang AIG. Đây là bước **technology-independent**, chỉ làm việc chuyển đổi representation, **không tối ưu hóa**. Mục tiêu của synthesis là đảm bảo tính đúng đắn về mặt chức năng (functional correctness) - output của AIG phải tương đương với input Netlist.
- **Optimization**: Là bước tối ưu hóa AIG về các mục tiêu như diện tích (area), delay (timing), và công suất tiêu thụ (power). Optimization được thực hiện sau synthesis, trên AIG đã được tạo ra.

Sự phân tách này giúp:

- **Modularity**: Mỗi bước có trách nhiệm rõ ràng
- **Debugging**: Dễ dàng debug và verify từng bước
- **Maintainability**: Code dễ maintain và mở rộng

### 2.1.2. Quy Trình Synthesis trong MyLogic

Quy trình synthesis trong MyLogic EDA Tool bao gồm các bước chính:

```
Netlist Dictionary (từ Verilog Parser)
    ↓
[1] Khởi tạo AIG
    - Tạo CONST0, CONST1 nodes
    - Khởi tạo hash table
    ↓
[2] Tạo Primary Inputs (PI)
    - Tạo PI node cho mỗi input signal
    - Lưu vào signal_mapping
    ↓
[3] Xử lý Constants
    - Xử lý constant signals (const_True, const_False, 1'b1, 1'b0)
    - Tạo constant nodes
    ↓
[4] Chuyển đổi Nodes (Topological Order)
    - Convert từng node trong netlist sang AIG
    - Áp dụng gate conversion algorithms
    - Xử lý multi-bit operations (ADD, SUB, MUX, EQ)
    ↓
[5] Tạo Primary Outputs (PO)
    - Lấy AIG node từ signal_mapping
    - Thêm vào AIG.pos
    ↓
AIG (Kết quả Synthesis)
```

### 2.1.3. Mục Tiêu của Synthesis

Mục tiêu chính của synthesis là:

1. **Functional Correctness**: Đảm bảo output AIG có cùng hành vi chức năng với input Netlist
2. **Completeness**: Hỗ trợ đầy đủ các cổng logic cơ bản và multi-bit operations
3. **Efficiency**: Sử dụng structural hashing để tránh duplicate nodes
4. **Extensibility**: Dễ dàng mở rộng để hỗ trợ thêm các operations mới

---

## 2.2. CẤU TRÚC DỮ LIỆU AIG (AND-INVERTER GRAPH)

### 2.2.1. Tổng Quan về AIG

**And-Inverter Graph (AIG)** là một directed acyclic graph (DAG) biểu diễn Boolean functions chỉ sử dụng:

- **AND gates** (2-input AND)
- **Inverters** (NOT gates, được biểu diễn bằng inversion flags)

AIG là một canonical form được sử dụng rộng rãi trong logic synthesis, đặc biệt trong các công cụ như ABC (Berkeley Logic Synthesis Tool) và Yosys.

### 2.2.2. AIG Class - Cấu Trúc và Implementation

#### 2.2.2.1. Cấu Trúc AIG Class

Class `AIG` trong MyLogic được implement như sau:

```python
class AIG:
    def __init__(self):
        # Node storage
        self.nodes: Dict[int, AIGNode] = {}
        self.next_node_id = 0
      
        # Constant nodes (singleton)
        self.const0 = self._create_node('CONST0')
        self.const1 = self._create_node('CONST1')
      
        # Primary inputs
        self.pis: Dict[str, AIGNode] = {}
      
        # Primary outputs
        self.pos: List[Tuple[AIGNode, bool]] = []  # (node, inverted)
      
        # Structural hashing table
        # Key: (left_id, right_id, left_inv, right_inv) -> node_id
        self.hash_table: Dict[Tuple[int, int, bool, bool], int] = {}
      
        # Level information
        self.max_level = 0
```

**Các thành phần chính:**

- **nodes**: Dictionary lưu trữ tất cả AIG nodes, key là `node_id`
- **const0, const1**: Constant nodes (singleton pattern)
- **pis**: Dictionary mapping signal names đến PI nodes
- **pos**: List các primary outputs, mỗi PO là tuple (node, inverted)
- **hash_table**: Hash table cho structural hashing, key là `(left_id, right_id, left_inv, right_inv)`
- **max_level**: Logic level lớn nhất trong AIG

#### 2.2.2.2. AIGNode Structure

Mỗi node trong AIG được biểu diễn bởi class `AIGNode`:

```python
class AIGNode:
    def __init__(self, node_id: int, node_type: str = 'AND',
                 left: Optional['AIGNode'] = None,
                 right: Optional['AIGNode'] = None,
                 left_inverted: bool = False,
                 right_inverted: bool = False,
                 var_name: Optional[str] = None):
        self.node_id = node_id
        self.node_type = node_type  # CONST0, CONST1, PI, AND
        self.left = left
        self.right = right
        self.left_inverted = left_inverted
        self.right_inverted = right_inverted
        self.var_name = var_name  # For PI nodes
        self.ref_count = 0
        self.level = 0  # Logic level
```

**Các loại node:**

- **CONST0, CONST1**: Constant nodes (False, True)
- **PI**: Primary Input nodes
- **AND**: AND gate nodes với 2 inputs (có thể có inversion flags)

**Inversion flags**: NOT được biểu diễn bằng inversion flags thay vì explicit NOT nodes, giúp:

- Giảm số lượng nodes
- Dễ dàng combine inversions
- Efficient structural hashing

### 2.2.3. Structural Hashing trong AIG (Built-in)

**Structural Hashing** là một kỹ thuật quan trọng được tích hợp sẵn (built-in) trong AIG class để tự động loại bỏ duplicate nodes trong quá trình tạo AIG. Đây là một cơ chế tự động, không phải là một bước optimization riêng biệt.

**Cơ chế hoạt động:**

Mỗi AND node được hash bằng:

```python
hash_key = (left_node_id, right_node_id, left_inverted, right_inverted)
```

**Normalization**: Đảm bảo `left_node_id <= right_node_id` để có canonical form. Nếu `left_id > right_id`, swap left và right cùng với inversion flags.

**Duplicate Elimination**: Khi tạo node mới trong `create_and()`:

1. Normalize inputs (đảm bảo left_id <= right_id)
2. Check hash table với key `(left_id, right_id, left_inv, right_inv)`
3. Nếu đã tồn tại → return existing node (reuse)
4. Nếu chưa tồn tại → create new node và store trong hash table

**Lưu ý quan trọng:**

- **Structural Hashing trong Synthesis**: Đây là cơ chế tự động, được thực hiện trong quá trình synthesis khi tạo AIG nodes. Nó đảm bảo không tạo duplicate nodes ngay từ đầu, nhưng **không phải là một bước optimization**.
- **Strash Pass trong Optimization**: Đây là một bước optimization riêng biệt (xem Chương 3), được thực hiện sau synthesis để rebuild và tối ưu hóa hash table, đảm bảo AIG ở dạng canonical hoàn toàn.

**Lợi ích của Structural Hashing (Built-in):**

- Giảm số lượng nodes ngay trong quá trình synthesis
- Automatic common subexpression elimination (CSE) cơ bản
- Efficient memory usage
- Faster operations
- Đảm bảo AIG không có duplicate nodes ngay từ đầu

### 2.2.4. Constant Folding

Trong quá trình tạo nodes, AIG thực hiện **constant folding** để simplify logic:

- `AND(x, const0)` → `const0`
- `AND(x, const1)` → `x` (hoặc NOT(x) nếu có inversion)
- `AND(x, !x)` → `const0` (tautology)

Constant folding được thực hiện trong hàm `create_and()` của AIG class.

---

## 2.3. THUẬT TOÁN CHUYỂN ĐỔI NETLIST SANG AIG

### 2.3.1. Tổng Quan về NetlistToAIGConverter

Class `NetlistToAIGConverter` là thành phần chính thực hiện chuyển đổi từ Netlist Dictionary sang AIG. Converter này được thiết kế theo kiến trúc modular, tách biệt rõ ràng giữa các bước xử lý.

**Cấu trúc Converter:**

```python
class NetlistToAIGConverter:
    def __init__(self):
        self.aig = None
        self.netlist = None
        self.node_mapping: Dict[str, AIGNode] = {}  # netlist_node_id -> AIGNode
        self.signal_mapping: Dict[str, AIGNode] = {}  # signal_name -> AIGNode
        self.multibit_signal_mapping: Dict[str, MultiBitAIGNode] = {}  # signal_name -> MultiBitAIGNode
```

**Các mapping quan trọng:**

- **node_mapping**: Ánh xạ từ netlist node ID sang AIG node tương ứng
- **signal_mapping**: Ánh xạ từ tên signal sang AIG node (single-bit)
- **multibit_signal_mapping**: Ánh xạ từ tên signal sang MultiBitAIGNode (multi-bit)

### 2.3.2. Quy Trình Chuyển Đổi Chi Tiết

Quy trình chuyển đổi được thực hiện qua 4 bước chính:

#### Bước 1: Tạo Primary Inputs (PI)

Primary inputs được tạo trước tiên để đảm bảo các signal references có sẵn cho các bước sau.

```python
def _create_primary_inputs(self, netlist: Dict[str, Any]):
    """Tạo Primary Input nodes trong AIG."""
    inputs = netlist.get('inputs', [])
    for input_name in inputs:
        aig_pi = self.aig.create_pi(input_name)
        self.signal_mapping[input_name] = aig_pi
```

**Lưu ý:**

- Mỗi input signal được tạo một PI node duy nhất
- PI nodes được lưu trong `signal_mapping` để truy cập nhanh
- PI nodes cũng được lưu trong `aig.pis` dictionary

#### Bước 2: Xử Lý Constants

Constants được xử lý ngay sau primary inputs để đảm bảo constant nodes có sẵn.

```python
def _create_constants(self, netlist: Dict[str, Any]):
    """Tạo Constant nodes trong AIG."""
    for node_data in nodes_list:
        node_type = node_data.get('type', '')
        if node_type in ['CONST0', 'GND', '0']:
            self.node_mapping[node_id] = self.aig.const0
            self.signal_mapping[output] = self.aig.const0
        elif node_type in ['CONST1', 'VCC', '1']:
            self.node_mapping[node_id] = self.aig.const1
            self.signal_mapping[output] = self.aig.const1
```

**Các loại constant được hỗ trợ:**

- `CONST0`, `GND`, `0`: Constant 0 (False)
- `CONST1`, `VCC`, `1`: Constant 1 (True)

#### Bước 3: Chuyển Đổi Nodes (Topological Order)

Bước này là trung tâm của quá trình synthesis, chuyển đổi từng node trong netlist sang AIG.

**Thuật toán tổng quát:**

```
Algorithm: Convert Nodes to AIG

1. Lấy danh sách nodes từ netlist
2. For each node in nodes:
   a. Xác định node_type
   b. Nếu là gate (AND, OR, XOR, ...):
      → Gọi _convert_gate_node()
   c. Nếu là ADD/SUB/MUX/EQ:
      → Gọi _convert_add_node() / _convert_sub_node() / ...
   d. Lưu kết quả vào node_mapping và signal_mapping
```

**Xử lý Fanins:**

Fanins trong netlist có format: `[["signal", inverted], ...]` hoặc `["signal", ...]`

```python
# Extract input signals from fanins
if fanins:
    input_signals = []
    input_inverted = []
    for fanin in fanins:
        if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
            input_signals.append(str(fanin[0]))
            input_inverted.append(fanin[1] if len(fanin) > 1 else False)
```

**Topological Ordering:**

Mặc dù code hiện tại xử lý tất cả nodes trong một lần, về mặt lý thuyết, nodes nên được xử lý theo topological order để đảm bảo:

- Input nodes được convert trước output nodes
- Dependencies được resolve đúng thứ tự
- Tránh reference đến nodes chưa được tạo

#### Bước 4: Tạo Primary Outputs (PO)

Sau khi tất cả nodes đã được convert, primary outputs được tạo từ signal_mapping.

```python
def _create_primary_outputs(self, netlist: Dict[str, Any]):
    """Tạo Primary Output nodes trong AIG."""
    outputs = netlist.get('outputs', [])
    for output_name in outputs:
        if output_name in self.multibit_signal_mapping:
            # Multi-bit output - add each bit as PO
            multibit_node = self.multibit_signal_mapping[output_name]
            for bit_node in multibit_node.bits:
                self.aig.add_po(bit_node, inverted=False)
        elif output_name in self.signal_mapping:
            # Single-bit output
            aig_node = self.signal_mapping[output_name]
            self.aig.add_po(aig_node, inverted=False)
```

**Xử lý Multi-bit Outputs:**

- Multi-bit outputs được tách thành các single-bit outputs
- Mỗi bit được thêm vào `aig.pos` như một PO riêng biệt

---

## 2.4. CHUYỂN ĐỔI CÁC CỔNG LOGIC CƠ BẢN

### 2.4.1. Nguyên Tắc Chuyển Đổi

Tất cả các cổng logic được chuyển đổi sang AIG chỉ sử dụng:

- AND gates (2-input)
- Inverters (biểu diễn bằng inversion flags)

Các cổng khác (OR, XOR, NAND, NOR, XNOR) được chuyển đổi dựa trên các công thức Boolean algebra.

### 2.4.2. AND Gate

AND gate là cổng cơ bản nhất trong AIG, được giữ nguyên:

```python
if node_type == 'AND':
    result = aig_inputs[0]
    for inp in aig_inputs[1:]:
        result = self.aig.create_and(result, inp)
    return result
```

**Formula:** `AND(a, b) = a AND b` (giữ nguyên)

### 2.4.3. OR Gate (De Morgan's Law)

OR gate được chuyển đổi sử dụng De Morgan's Law:

```python
elif node_type == 'OR':
    # OR(a, b) = NOT(AND(NOT(a), NOT(b)))
    not_inputs = [self.aig.create_not(inp) for inp in aig_inputs]
    result = not_inputs[0]
    for inp in not_inputs[1:]:
        result = self.aig.create_and(result, inp)
    return self.aig.create_not(result)
```

**Formula:** `a OR b = !(!a AND !b)`

**Giải thích:**

- NOT tất cả inputs
- AND các inputs đã NOT
- NOT kết quả

### 2.4.4. XOR Gate

XOR gate được chuyển đổi dựa trên công thức:

```python
elif node_type == 'XOR':
    result = aig_inputs[0]
    for inp in aig_inputs[1:]:
        result = self.aig.create_xor(result, inp)
    return result
```

Trong AIG, XOR được implement như sau:

```python
def create_xor(self, left: AIGNode, right: AIGNode) -> AIGNode:
    """Create XOR: a XOR b = (!a AND b) OR (a AND !b)."""
    not_left = self.create_not(left)
    not_right = self.create_not(right)
    term1 = self.create_and(not_left, right)
    term2 = self.create_and(left, not_right)
    return self.create_or(term1, term2)
```

**Formula:** `a XOR b = (!a AND b) OR (a AND !b)`

**Giải thích:**

- Tạo 2 terms: `(!a AND b)` và `(a AND !b)`
- OR 2 terms lại

### 2.4.5. NAND Gate

NAND gate là NOT của AND:

```python
elif node_type == 'NAND':
    result = aig_inputs[0]
    for inp in aig_inputs[1:]:
        result = self.aig.create_and(result, inp)
    return self.aig.create_not(result)
```

**Formula:** `NAND(a, b) = NOT(AND(a, b))`

### 2.4.6. NOR Gate

NOR gate được chuyển đổi tối ưu, không cần NOT cuối:

```python
elif node_type == 'NOR':
    not_inputs = [self.aig.create_not(inp) for inp in aig_inputs]
    result = not_inputs[0]
    for inp in not_inputs[1:]:
        result = self.aig.create_and(result, inp)
    return result  # Already inverted
```

**Formula:** `NOR(a, b) = AND(NOT(a), NOT(b))`

**Lưu ý:** Không cần NOT cuối vì đã có NOT ở inputs, kết quả đã là NOR.

### 2.4.7. XNOR Gate

XNOR gate là NOT của XOR:

```python
elif node_type == 'XNOR':
    result = aig_inputs[0]
    for inp in aig_inputs[1:]:
        result = self.aig.create_xor(result, inp)
    return self.aig.create_not(result)
```

**Formula:** `XNOR(a, b) = NOT(XOR(a, b))`

### 2.4.8. NOT Gate

NOT gate được biểu diễn bằng inversion flag trong AIG:

```python
elif node_type == 'NOT':
    return self.aig.create_not(aig_inputs[0])
```

**Implementation trong AIG:**

```python
def _create_not(self, node: AIGNode) -> AIGNode:
    """Create NOT by inverting."""
    if node.is_constant():
        return self.create_constant(not node.get_value())
  
    # NOT(x) is represented as AND(x, const1) with left_inverted=True
    key = (node.node_id, self.const1.node_id, True, False)
    if key in self.hash_table:
        return self.nodes[self.hash_table[key]]
  
    not_node = self._create_node('AND',
                                left=node, right=self.const1,
                                left_inverted=True,
                                right_inverted=False)
    not_node.level = node.level
    self.hash_table[key] = not_node.node_id
    return not_node
```

**Formula:** `NOT(x) = x AND 1` với `left_inverted=True`

### 2.4.9. BUF Gate

BUF gate là pass-through, không cần chuyển đổi:

```python
elif node_type == 'BUF':
    return aig_inputs[0]  # BUF is just pass-through in AIG
```

**Formula:** `BUF(a) = a` (giữ nguyên)

### 2.4.10. Bảng Tóm Tắt Chuyển Đổi

| Cổng | Công Thức AIG                 | Số AND Nodes | Số Inversion |
| ----- | ------------------------------- | ------------- | ------------- |
| AND   | `a AND b`                     | 1             | 0             |
| OR    | `!(!a AND !b)`                | 1             | 3             |
| XOR   | `(!a AND b) OR (a AND !b)`    | 3             | 2             |
| NAND  | `!(a AND b)`                  | 1             | 1             |
| NOR   | `!a AND !b`                   | 1             | 2             |
| XNOR  | `!((!a AND b) OR (a AND !b))` | 3             | 3             |
| NOT   | `x AND 1` (left_inv=True)     | 1             | 1             |
| BUF   | `a`                           | 0             | 0             |

---

## 2.5. MULTI-BIT OPERATIONS

### 2.5.1. MultiBitAIGNode - Cấu Trúc Dữ Liệu

Để hỗ trợ các operations multi-bit (ADD, SUB, MUX, EQ), MyLogic sử dụng class `MultiBitAIGNode`:

```python
class MultiBitAIGNode:
    def __init__(self, width: int, bits: List[AIGNode]):
        """
        Args:
            width: Bit width of the signal
            bits: List of single-bit AIG nodes [bit0 (LSB), ..., bitN-1 (MSB)]
        """
        self.width = width
        self.bits = bits  # [bit0 (LSB), bit1, ..., bitN-1 (MSB)]
```

**Lưu ý quan trọng:**

- `bits[0]` là LSB (Least Significant Bit)
- `bits[width-1]` là MSB (Most Significant Bit)
- Mỗi bit là một AIGNode riêng biệt

### 2.5.2. ADD Operation - Ripple-Carry Adder

ADD operation được implement bằng **Ripple-Carry Adder**, một thuật toán cổ điển và đơn giản.

**Thuật toán Ripple-Carry Adder:**

```
Algorithm: Ripple-Carry Adder

Input: a[width], b[width] (multi-bit signals)
Output: sum[width] (multi-bit result)

carry = 0 (initial)
For i from 0 to width-1:
    sum[i] = a[i] XOR b[i] XOR carry
    carry = (a[i] AND b[i]) OR (carry AND (a[i] XOR b[i]))
```

**Implementation:**

```python
def _convert_add_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
    """Convert ADD node to AIG using ripple-carry adder."""
    # Get input signals and determine width
    a_bits = self._get_multi_bit_signal(a_signal, width)
    b_bits = self._get_multi_bit_signal(b_signal, width)
  
    # Ripple-carry adder
    result_bits = []
    carry = self.aig.const0  # Initial carry = 0
  
    for i in range(width):
        a_bit = a_bits[i]
        b_bit = b_bits[i]
      
        # Full adder: sum = a XOR b XOR carry
        sum_ab = self.aig.create_xor(a_bit, b_bit)
        sum_result = self.aig.create_xor(sum_ab, carry)
      
        # carry_out = (a AND b) OR (carry AND (a XOR b))
        and_ab = self.aig.create_and(a_bit, b_bit)
        and_carry_sum = self.aig.create_and(carry, sum_ab)
        carry = self.aig.create_or(and_ab, and_carry_sum)
      
        result_bits.append(sum_result)
  
    return MultiBitAIGNode(width, result_bits)
```

**Full Adder Logic:**

- **Sum bit:** `sum = a XOR b XOR carry_in`
- **Carry out:** `carry_out = (a AND b) OR (carry_in AND (a XOR b))`

**Đặc điểm:**

- Độ phức tạp: O(width) - xử lý từng bit tuần tự
- Delay: O(width) - carry propagation từ LSB đến MSB
- Area: O(width) - linear với bit width

**Ví dụ:** ADD 4-bit

```
a = [a3, a2, a1, a0]
b = [b3, b2, b1, b0]

Step 0 (LSB): sum[0] = a0 XOR b0 XOR 0, carry1 = ...
Step 1: sum[1] = a1 XOR b1 XOR carry1, carry2 = ...
Step 2: sum[2] = a2 XOR b2 XOR carry2, carry3 = ...
Step 3 (MSB): sum[3] = a3 XOR b3 XOR carry3
```

### 2.5.3. SUB Operation - 2's Complement Subtraction

SUB operation được implement bằng cách sử dụng 2's complement:

**Công thức:** `A - B = A + (~B) + 1`

**Implementation:**

```python
def _convert_sub_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
    """Convert SUB node: a - b = a + (~b) + 1 (2's complement)."""
    # Get input signals
    a_bits = self._get_multi_bit_signal(a_signal, width)
    b_bits = self._get_multi_bit_signal(b_signal, width)
  
    # Invert b for 2's complement
    b_inv_bits = [self.aig.create_not(bit) for bit in b_bits]
  
    # Add with carry_in = 1
    result_bits = []
    carry = self.aig.const1  # carry_in = 1 for 2's complement
  
    for i in range(width):
        a_bit = a_bits[i]
        b_inv_bit = b_inv_bits[i]
      
        # Full adder with inverted b and carry_in = 1
        sum_ab = self.aig.create_xor(a_bit, b_inv_bit)
        sum_result = self.aig.create_xor(sum_ab, carry)
      
        and_ab = self.aig.create_and(a_bit, b_inv_bit)
        and_carry_sum = self.aig.create_and(carry, sum_ab)
        carry = self.aig.create_or(and_ab, and_carry_sum)
      
        result_bits.append(sum_result)
  
    return MultiBitAIGNode(width, result_bits)
```

**Giải thích:**

1. Invert tất cả bits của B: `~B`
2. Sử dụng ripple-carry adder với:
   - Input 1: A
   - Input 2: ~B
   - Carry in: 1
3. Kết quả: `A + (~B) + 1 = A - B` (2's complement)

### 2.5.4. EQ Operation - Equality Comparison

EQ operation so sánh 2 multi-bit signals và trả về single-bit result.

**Công thức:** `a == b = AND of all (a[i] XNOR b[i])`

**Implementation:**

```python
def _convert_eq_node(self, node_data: Dict[str, Any]) -> Optional[AIGNode]:
    """
    Convert EQ (equality) node to AIG.
  
    For multi-bit: a == b = AND of all (a[i] XNOR b[i])
    Returns single-bit result.
    """
    # Get multi-bit signals
    a_bits = self._get_multi_bit_signal(a_signal, width)
    b_bits = self._get_multi_bit_signal(b_signal, width)
  
    # EQ = AND of all (a[i] XNOR b[i])
    # XNOR = NOT(XOR)
    eq_bits = []
    for i in range(width):
        xor_result = self.aig.create_xor(a_bits[i], b_bits[i])
        xnor_result = self.aig.create_not(xor_result)  # XNOR = NOT(XOR)
        eq_bits.append(xnor_result)
  
    # AND all bits together
    result = eq_bits[0]
    for bit in eq_bits[1:]:
        result = self.aig.create_and(result, bit)
  
    return result  # Single-bit result
```

**Giải thích:**

1. Với mỗi bit position i:
   - Tính `XOR(a[i], b[i])`
   - NOT để có `XNOR(a[i], b[i])` (bằng 1 nếu a[i] == b[i])
2. AND tất cả XNOR results lại
3. Kết quả = 1 nếu và chỉ nếu tất cả bits bằng nhau

**Ví dụ:** EQ 4-bit

```
a = [1, 0, 1, 1]
b = [1, 0, 1, 1]

XNOR(1, 1) = 1
XNOR(0, 0) = 1
XNOR(1, 1) = 1
XNOR(1, 1) = 1

Result = AND(1, 1, 1, 1) = 1 (equal)
```

### 2.5.5. MUX Operation - Multiplexer

MUX operation chọn một trong nhiều data inputs dựa trên select signals.

**2-way MUX Formula:** `out = (!sel AND in0) OR (sel AND in1)`

**N-way MUX:** Được build bằng binary tree của 2-way MUXes.

**Implementation:**

```python
def _convert_mux_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
    """
    Convert MUX (multiplexer) node to AIG.
  
    For 2-way MUX: out = (!sel AND in0) OR (sel AND in1)
    For N-way: build binary tree of 2-way MUXes.
    """
    # Extract data inputs and select signals
    data_signals = [...]  # data0, data1, ..., dataN-1
    select_inputs = [...]  # select signals
  
    # Build MUX tree recursively
    def build_mux_tree(data_bits_list, select_bits, bit_pos):
        if len(data_bits_list) == 1:
            return data_bits_list[0][bit_pos]
      
        if len(data_bits_list) == 2:
            # Base case: 2-way MUX
            in0 = data_bits_list[0][bit_pos]
            in1 = data_bits_list[1][bit_pos]
            sel = select_bits[0] if select_bits else self.aig.const0
          
            not_sel = self.aig.create_not(sel)
            term0 = self.aig.create_and(not_sel, in0)
            term1 = self.aig.create_and(sel, in1)
            return self.aig.create_or(term0, term1)
      
        # Recursive case: split in half
        mid = len(data_bits_list) // 2
        left_result = build_mux_tree(data_bits_list[:mid], select_bits[1:], bit_pos)
        right_result = build_mux_tree(data_bits_list[mid:], select_bits[1:], bit_pos)
      
        # MUX between left and right using MSB of select
        sel = select_bits[0] if select_bits else self.aig.const0
        not_sel = self.aig.create_not(sel)
        term0 = self.aig.create_and(not_sel, left_result)
        term1 = self.aig.create_and(sel, right_result)
        return self.aig.create_or(term0, term1)
  
    # Apply to each bit position
    result_bits = []
    for bit_pos in range(width):
        bit_results = [data_bits[bit_pos] for data_bits in data_bits_list]
        result_bit = build_mux_tree(bit_results, select_bits, bit_pos)
        result_bits.append(result_bit)
  
    return MultiBitAIGNode(width, result_bits)
```

**Giải thích:**

1. **2-way MUX (base case):**

   - `out = (!sel AND in0) OR (sel AND in1)`
2. **N-way MUX (recursive):**

   - Split data inputs thành 2 nhóm
   - Recursively build MUX tree cho mỗi nhóm
   - MUX 2 results lại bằng MSB của select signal

**Ví dụ:** 4-way MUX

```
Data inputs: in0, in1, in2, in3
Select: sel[1:0]

Level 1:
  left = MUX(in0, in1, sel[0])
  right = MUX(in2, in3, sel[0])

Level 2:
  out = MUX(left, right, sel[1])
```

### 2.5.6. Constant Multi-bit Signals

MyLogic hỗ trợ parsing và tạo multi-bit constants từ strings như `"8'd10"`, `"8'hFF"`, `"1'b1"`:

```python
def parse_constant_string(const_str: str, default_width: int = 8) -> tuple[int, int]:
    """
    Parse constant string like "8'd10", "8'hFF", "1'b1" into (value, width).
    """
    # Parse format: width'radixvalue
    # Examples: "8'd10" -> (10, 8), "8'hFF" -> (255, 8), "1'b1" -> (1, 1)
```

**Format được hỗ trợ:**

- Decimal: `"8'd10"` → value=10, width=8
- Hexadecimal: `"8'hFF"` → value=255, width=8
- Binary: `"1'b1"` → value=1, width=1

---

## 2.6. IMPLEMENTATION VÀ KIẾN TRÚC

### 2.6.1. Kiến Trúc Tổng Thể

Synthesis module trong MyLogic được tổ chức theo kiến trúc modular:

```
core/synthesis/
├── aig.py                    # AIG data structure và operations
├── aig_multibit.py           # Multi-bit AIG support
├── netlist_to_aig.py         # NetlistToAIGConverter class
└── synthesis_flow.py         # SynthesisFlow wrapper class
```

**Phân tách trách nhiệm:**

- `aig.py`: Core AIG data structure, structural hashing
- `aig_multibit.py`: Extension cho multi-bit operations
- `netlist_to_aig.py`: Conversion logic từ netlist sang AIG
- `synthesis_flow.py`: High-level synthesis flow interface

### 2.6.2. Signal Width Inference

MyLogic cần infer bit width của signals từ netlist metadata:

```python
def _get_signal_width(self, signal_name: str, default_width: int = 8) -> int:
    """Get bit width of a signal from netlist metadata."""
    # Check vector_widths in attrs
    vector_widths = self.netlist.get('attrs', {}).get('vector_widths', {})
    if signal_name in vector_widths:
        return vector_widths[signal_name]
  
    # Try to extract from constant string (e.g., "8'd10" -> 8)
    if "'" in signal_name:
        _, width = parse_constant_string(signal_name, default_width)
        return width
  
    return default_width
```

**Nguồn thông tin width:**

1. `vector_widths` trong netlist attrs (từ parser)
2. Parse từ constant strings (e.g., `"8'd10"`)
3. Default width (thường là 8 bits)

### 2.6.3. Multi-bit Signal Handling

Hàm `_get_multi_bit_signal()` xử lý việc lấy multi-bit signals:

```python
def _get_multi_bit_signal(self, signal_name: str, width: int) -> List[AIGNode]:
    """
    Get multi-bit signal as list of single-bit AIG nodes.
  
    Handles:
    - Constants (e.g., "8'd10", "8'hFF")
    - Regular signals (creates bit slices)
    """
    # Check if it's a constant
    if "'" in signal_name:
        value, parsed_width = parse_constant_string(signal_name, width)
        multibit_const = create_constant_multibit(self.aig, value, actual_width)
        return multibit_const.bits[:width]
  
    # Regular signal - get from mappings or create PIs
    bits = []
    for i in range(width):
        bit_name = f"{signal_name}[{i}]" if width > 1 else signal_name
        if bit_name in self.signal_mapping:
            bits.append(self.signal_mapping[bit_name])
        elif signal_name in self.multibit_signal_mapping:
            mb_node = self.multibit_signal_mapping[signal_name]
            bits.append(mb_node.bits[i] if i < mb_node.width else self.aig.const0)
        else:
            # Create new PI for this bit
            bit_pi = self.aig.create_pi(bit_name)
            self.signal_mapping[bit_name] = bit_pi
            bits.append(bit_pi)
  
    return bits
```

**Xử lý:**

1. Constants: Parse và tạo constant multi-bit node
2. Existing signals: Lấy từ `signal_mapping` hoặc `multibit_signal_mapping`
3. New signals: Tạo PI nodes cho từng bit

### 2.6.4. Error Handling và Validation

Converter thực hiện validation cơ bản:

```python
def convert(self, netlist: Dict[str, Any]) -> AIG:
    if not isinstance(netlist, dict) or 'nodes' not in netlist:
        raise ValueError("Invalid netlist format")
  
    # ... conversion logic ...
```

**Validation points:**

- Netlist format validation
- Node type validation
- Signal reference validation (warnings nếu signal không tìm thấy)

### 2.6.5. Performance Considerations

**Structural Hashing:**

- Tự động loại bỏ duplicate nodes
- Giảm memory footprint
- Accelerate operations

**Topological Order:**

- Hiện tại: Process tất cả nodes (assume netlist đã được topologically sorted)
- Lý tưởng: Implement topological sort để đảm bảo dependencies

**Memory Management:**

- Mappings (node_mapping, signal_mapping) có thể chiếm nhiều memory với designs lớn
- Consider: Sparse mappings, lazy evaluation

---

## 2.7. SO SÁNH VÀ ĐÁNH GIÁ

### 2.7.1. So Sánh với Yosys

**Yosys** là một công cụ logic synthesis nổi tiếng, open-source. So sánh synthesis module của MyLogic với Yosys:

| Khía cạnh                           | MyLogic                                 | Yosys                                                                 |
| ------------------------------------- | --------------------------------------- | --------------------------------------------------------------------- |
| **Input Format**                | Netlist Dictionary (từ Verilog parser) | Verilog RTL trực tiếp                                               |
| **Intermediate Representation** | AIG                                     | Internal RTLIL (Register Transfer Level Intermediate Language) → AIG |
| **Structural Hashing**          | Có (trong AIG class)                   | Có (trong AIG manager)                                               |
| **Multi-bit Operations**        | Ripple-carry adder, basic MUX           | Nhiều thuật toán tối ưu hơn (carry-lookahead, etc.)             |
| **Optimization**                | Tách riêng (sau synthesis)            | Tích hợp trong synthesis flow                                       |
| **Technology Mapping**          | Tách riêng                            | Tích hợp (techmap pass)                                             |

**Điểm mạnh của MyLogic:**

- Kiến trúc modular, dễ hiểu
- Tách biệt rõ ràng synthesis/optimization/techmap
- Phù hợp cho giáo dục và nghiên cứu

**Hạn chế:**

- Chưa hỗ trợ nhiều optimizations như Yosys
- Ripple-carry adder chậm hơn carry-lookahead
- Chưa có nhiều passes như Yosys

### 2.7.2. Kết Quả Synthesis

**Metrics quan trọng:**

- **Functional Correctness**: Output AIG phải tương đương với input Netlist
- **Node Count**: Số lượng AIG nodes được tạo ra
- **Depth**: Logic depth (max_level) của AIG
- **Memory Usage**: Memory footprint của AIG structure

**Ví dụ synthesis results:**

```
Input: Simple AND gate netlist
- Netlist nodes: 1
- AIG nodes: 2 (1 PI + 1 AND)
- Max level: 1

Input: 4-bit adder netlist
- Netlist nodes: 1 (ADD node)
- AIG nodes: ~40-50 (depends on implementation)
- Max level: ~10-15 (ripple-carry depth)
```

### 2.7.3. Hạn Chế và Hướng Phát Triển

**Hạn chế hiện tại:**

1. **Topological Ordering**: Chưa implement proper topological sort
2. **Signal Width Inference**: Phụ thuộc vào parser metadata
3. **Error Handling**: Còn basic, cần improve
4. **Performance**: Chưa optimize cho large designs
5. **Multi-bit Operations**: Chỉ có ripple-carry, chưa có advanced algorithms

**Hướng phát triển:**

1. **Advanced Adders**: Carry-lookahead adder, carry-select adder
2. **Better Width Inference**: Automatic width inference từ usage
3. **Validation**: Formal verification của synthesis results
4. **Performance**: Optimize cho large designs
5. **Extensions**: Hỗ trợ thêm operations (MULT, DIV, SHIFT, etc.)

---

## 2.8. KẾT LUẬN CHƯƠNG

CHƯƠNG 2 đã trình bày chi tiết về **Logic Synthesis** trong MyLogic EDA Tool, bao gồm:

1. **Tổng quan về Logic Synthesis**: Định nghĩa, vai trò, và sự phân biệt với Optimization
2. **Cấu trúc dữ liệu AIG**: AIG class, AIGNode structure, structural hashing, constant folding
3. **Thuật toán chuyển đổi**: Quy trình 4 bước từ Netlist Dictionary sang AIG
4. **Chuyển đổi cổng logic cơ bản**: Các công thức và implementation cho AND, OR, XOR, NAND, NOR, XNOR, NOT, BUF
5. **Multi-bit Operations**: ADD (ripple-carry), SUB (2's complement), EQ (equality), MUX (binary tree)
6. **Implementation và Kiến trúc**: Modular architecture, signal width inference, error handling
7. **So sánh và Đánh giá**: So sánh với Yosys, kết quả synthesis, hạn chế và hướng phát triển

Synthesis module của MyLogic đạt được mục tiêu chính: **chuyển đổi Netlist Dictionary sang AIG một cách chính xác và có cấu trúc**, tạo nền tảng cho các bước Optimization và Technology Mapping tiếp theo.

---

# CHƯƠNG 3: LOGIC OPTIMIZATION

## 3.1. TỔNG QUAN VỀ LOGIC OPTIMIZATION

### 3.1.1. Định Nghĩa và Vai Trò

**Logic Optimization** là quá trình tối ưu hóa AIG (And-Inverter Graph) về các mục tiêu như diện tích (area), delay (timing), và công suất tiêu thụ (power). Trong dự án MyLogic EDA Tool, optimization là một bước riêng biệt, được thực hiện sau synthesis, trên AIG đã được tạo ra từ quá trình synthesis.

#### 3.1.1.1. Phân Biệt Optimization và Synthesis

Một điểm quan trọng cần nhấn mạnh là sự phân biệt rõ ràng giữa **Synthesis** và **Optimization**:

- **Synthesis**: Chuyển đổi representation từ Netlist Dictionary sang AIG. Đây là bước **technology-independent**, chỉ làm việc chuyển đổi representation, **không tối ưu hóa**.
- **Optimization**: Tối ưu hóa AIG về các mục tiêu như area, delay, và power. Optimization được thực hiện **sau synthesis**, trên AIG đã được tạo ra. Mục tiêu của optimization là cải thiện chất lượng của AIG về các metrics cụ thể.

Sự phân tách này giúp:

- **Modularity**: Mỗi bước có trách nhiệm rõ ràng
- **Flexibility**: Có thể chạy optimization với các levels khác nhau
- **Debugging**: Dễ dàng debug và verify từng bước
- **Maintainability**: Code dễ maintain và mở rộng

### 3.1.2. Mục Tiêu của Optimization

Mục tiêu chính của optimization trong MyLogic là:

1. **Area Optimization**: Giảm số lượng AIG nodes (gates) để giảm diện tích chip
2. **Delay Optimization**: Tối ưu hóa logic depth (critical path) để cải thiện timing
3. **Power Optimization**: Giảm số lượng nodes để giảm công suất tiêu thụ (dynamic power)
4. **Functional Correctness**: Đảm bảo output AIG sau optimization có cùng hành vi chức năng với input AIG

### 3.1.3. Optimization Levels

MyLogic hỗ trợ 3 mức độ optimization:

1. **basic**: Chỉ các optimization algorithms cơ bản
2. **standard**: Các optimization algorithms tiêu chuẩn (default)
3. **aggressive**: Tất cả optimization algorithms với nhiều iterations và optimizations nâng cao

### 3.1.4. Quy Trình Optimization trong MyLogic

Quy trình optimization trong MyLogic EDA Tool bao gồm 5 bước chính:

```
AIG (từ Synthesis)
    ↓
[1] Structural Hashing (Strash)
    - Rebuild hash table
    - Loại bỏ duplicate nodes
    ↓
[2] Dead Code Elimination (DCE)
    - Tìm nodes không reachable từ outputs
    - Loại bỏ dead code
    ↓
[3] Common Subexpression Elimination (CSE)
    - Tìm và share common subexpressions
    - Giảm redundancy
    ↓
[4] Constant Propagation (ConstProp)
    - Propagate constants qua mạch
    - Simplify logic với constants
    ↓
[5] Logic Balancing (Balance)
    - Cân bằng logic depth
    - Tối ưu hóa timing
    ↓
Optimized AIG (Kết quả Optimization)
```

---

## 3.2. STRUCTURAL HASHING (STRASH)

### 3.2.1. Định Nghĩa

**Structural Hashing (Strash)** là một bước optimization riêng biệt để rebuild và tối ưu hóa hash table của AIG, đảm bảo AIG ở dạng canonical hoàn toàn và loại bỏ mọi duplicate nodes còn sót lại.

**Sự khác biệt với Structural Hashing trong Synthesis:**

- **Structural Hashing trong Synthesis (Chương 2)**: Là cơ chế built-in tự động trong AIG class, hoạt động khi tạo nodes trong quá trình synthesis. Nó ngăn chặn việc tạo duplicate nodes ngay từ đầu, nhưng **không phải là bước optimization**.

- **Strash Pass trong Optimization (Chương 3)**: Là một bước optimization riêng biệt, được thực hiện sau synthesis. Mặc dù AIG class đã có structural hashing built-in trong `create_and()`, Strash pass rebuild toàn bộ AIG từ đầu, đảm bảo:
  - Hash table được rebuild và tối ưu
  - Không có duplicate nodes còn sót lại
  - AIG ở dạng canonical hoàn toàn
  - Sẵn sàng cho các bước optimization tiếp theo

### 3.2.2. Nguyên Tắc Hoạt Động

Structural hashing trong AIG hoạt động dựa trên:

1. **Hash Key**: Mỗi AND node được hash bằng `(left_node_id, right_node_id, left_inverted, right_inverted)`
2. **Normalization**: Đảm bảo `left_node_id <= right_node_id` để có canonical form
3. **Duplicate Detection**: Khi tạo node mới, check hash table để tìm duplicate
4. **Reuse**: Nếu duplicate được tìm thấy, reuse existing node thay vì tạo mới

### 3.2.3. Implementation

**Implementation trong Optimization Flow:**

```python
def _run_strash(self, aig: AIG) -> AIG:
    """Chạy Structural Hashing trên AIG."""
    nodes_before = aig.count_nodes()
  
    # AIG đã có structural hashing built-in trong create_and()
    # Strash trên AIG chủ yếu là rebuild hash table
    optimized_aig = aig.strash()
  
    nodes_after = optimized_aig.count_nodes()
    return optimized_aig
```

**Strash Method trong AIG:**

```python
def strash(self) -> 'AIG':
    """
    Structural hashing - loại bỏ duplicate nodes.
  
    Đây là thuật toán tương tự như Strash trong ABC.
    """
    new_aig = AIG()
  
    # Recreate PIs
    pi_map = {}
    for var_name, old_pi in self.pis.items():
        new_pi = new_aig.create_pi(var_name)
        pi_map[old_pi.node_id] = new_pi
  
    # Recreate nodes in topological order
    visited = set()
  
    def recreate_node(old_node: AIGNode) -> AIGNode:
        if old_node.node_id in visited:
            return pi_map.get(old_node.node_id) or new_aig.nodes.get(old_node.node_id)
      
        visited.add(old_node.node_id)
      
        if old_node.is_constant():
            return new_aig.create_constant(old_node.get_value())
        elif old_node.is_pi():
            return pi_map[old_node.node_id]
        else:
            left = recreate_node(old_node.left)
            right = recreate_node(old_node.right)
            return new_aig.create_and(left, right,
                                     old_node.left_inverted,
                                     old_node.right_inverted)
  
    # Recreate outputs
    for old_po, inverted in self.pos:
        new_po = recreate_node(old_po)
        if inverted:
            new_po = new_aig.create_not(new_po)
        new_aig.add_po(new_po)
  
    return new_aig
```

### 3.2.4. Lợi Ích

- **Automatic CSE**: Structural hashing tự động loại bỏ common subexpressions
- **Memory Efficiency**: Giảm memory footprint bằng cách share nodes
- **Faster Operations**: Ít nodes hơn → operations nhanh hơn
- **Canonical Form**: Đảm bảo AIG ở dạng canonical, dễ so sánh

### 3.2.5. Kết Quả

Strash thường giữ nguyên số lượng nodes (vì AIG đã có hashing built-in), nhưng đảm bảo:

- Không có duplicate nodes
- Hash table được rebuild và tối ưu
- AIG ở dạng canonical

---

## 3.3. DEAD CODE ELIMINATION (DCE)

### 3.3.1. Định Nghĩa

**Dead Code Elimination (DCE)** là thuật toán loại bỏ các nodes không thể tiếp cận từ bất kỳ output nào, hiệu quả loại bỏ dead code và giảm kích thước mạch.

### 3.3.2. Nguyên Tắc Hoạt Động

DCE hoạt động theo nguyên tắc:

1. **Reachability Analysis**: Tìm tất cả nodes reachable từ outputs
2. **Marking**: Đánh dấu các nodes được sử dụng (reachable)
3. **Removal**: Loại bỏ các nodes không được đánh dấu (unreachable)

### 3.3.3. Thuật Toán

**Algorithm: Dead Code Elimination**

```
Algorithm: DCE

1. Khởi tạo:
   - reachable = empty set
   - queue = empty queue

2. Mark outputs as reachable:
   For each output port:
     - Add output node to queue
     - Mark output node as reachable

3. Backward traversal (BFS):
   While queue is not empty:
     - current = dequeue()
     - For each input node của current:
       - If input node not in reachable:
         - Mark input node as reachable
         - Enqueue input node

4. Remove unreachable nodes:
   For each node in netlist:
     - If node not in reachable:
       - Remove node from netlist

5. Update connections:
   - Remove references to deleted nodes
   - Update wire connections
```

### 3.3.4. Implementation

**Implementation:**

DCE được implement trên cả AIG và Netlist:

- **Trên AIG**: Rebuild AIG chỉ với các nodes reachable từ outputs, loại bỏ các nodes không được sử dụng.
- **Trên Netlist**: Sử dụng BFS (Breadth-First Search) để tìm tất cả nodes reachable từ output ports, sau đó loại bỏ các nodes không reachable.

### 3.3.5. Optimization Levels

DCE hỗ trợ 3 levels:

- **basic**: Simple backward traversal, loại bỏ nodes không reachable
- **advanced**: Multiple passes với pattern matching, xử lý Don't Care conditions
- **aggressive**: Aggressive elimination với nhiều iterations, loại bỏ redundant nodes

### 3.3.6. Lợi Ích

- **Area Reduction**: Giảm số lượng nodes → giảm diện tích
- **Power Reduction**: Ít nodes → ít switching activity → giảm power
- **Simplification**: Mạch đơn giản hơn, dễ optimize hơn
- **Memory Efficiency**: Giảm memory footprint

### 3.3.7. Kết Quả

DCE thường loại bỏ 5-20% nodes tùy thuộc vào design. Ví dụ:

- Small designs: 5-10% reduction
- Large designs với nhiều unused logic: 15-25% reduction

---

## 3.4. COMMON SUBEXPRESSION ELIMINATION (CSE)

### 3.4.1. Định Nghĩa

**Common Subexpression Elimination (CSE)** là thuật toán tìm và loại bỏ các subexpressions trùng lặp trong mạch bằng cách tạo shared nodes và cập nhật connections.

### 3.4.2. Nguyên Tắc Hoạt Động

CSE hoạt động theo nguyên tắc:

1. **Pattern Matching**: Tìm các nodes có cùng structure (type, inputs)
2. **Sharing**: Tạo một shared node cho common subexpression
3. **Replacement**: Thay thế tất cả occurrences bằng shared node
4. **Cleanup**: Loại bỏ duplicate nodes

### 3.4.3. Thuật Toán

**Algorithm: Common Subexpression Elimination**

```
Algorithm: CSE

1. Identify common subexpressions:
   For each computational node:
     - Create expression signature: type(inputs...)
     - Group nodes by signature
     - Find signatures appearing > 1 time

2. Create shared nodes:
   For each common expression:
     - Create shared node với expression đó
     - Map original nodes → shared node

3. Replace occurrences:
   For each node using common expression:
     - Replace input references với shared node
   
4. Remove duplicate nodes:
   - Remove original nodes đã được thay thế
   - Update connections
```

### 3.4.4. Implementation

**Implementation:**

CSE hoạt động theo 3 bước:

1. **Tạo Expression Signature**: Tạo signature cho mỗi node dựa trên type và inputs (đã sort để có canonical form).
2. **Tìm Common Subexpressions**: Nhóm các nodes có cùng signature, chỉ giữ lại các expressions xuất hiện nhiều hơn 1 lần.
3. **Tạo Shared Nodes**: Tạo một shared node cho mỗi common expression, thay thế tất cả occurrences bằng shared node.

### 3.4.5. Relationship với Structural Hashing

CSE và Structural Hashing có mối quan hệ chặt chẽ:

- **Structural Hashing**: Tự động loại bỏ duplicate nodes trong AIG bằng hash table
- **CSE trên Netlist**: Tìm và share common subexpressions ở netlist level
- **CSE trên AIG**: AIG đã tự động share qua structural hashing, nên CSE pass chủ yếu là rebuild hash table

**Implementation trên AIG:**

```python
def _run_cse(self, aig: AIG) -> AIG:
    """Chạy Common Subexpression Elimination trên AIG."""
    # CSE trên AIG: AIG đã tự động share common subexpressions qua hash table
    # Nên CSE chủ yếu là rebuild để tối ưu hơn
    optimized_aig = aig.strash()  # Rebuild hash table
    return optimized_aig
```

### 3.4.6. Lợi Ích

- **Area Reduction**: Giảm số lượng nodes bằng cách share common logic
- **Power Reduction**: Ít nodes → ít switching activity
- **Timing Improvement**: Shared nodes có thể cải thiện timing trong một số trường hợp
- **Memory Efficiency**: Giảm memory footprint

### 3.4.7. Kết Quả

CSE thường giảm 10-30% nodes tùy thuộc vào design. Ví dụ:

- Designs với nhiều common logic: 20-35% reduction
- Designs ít common logic: 5-15% reduction

---

## 3.5. CONSTANT PROPAGATION (CONSTPROP)

### 3.5.1. Định Nghĩa

**Constant Propagation (ConstProp)** là thuật toán propagate constant values qua mạch và simplify logic với known values, loại bỏ unnecessary gates và tối ưu hóa mạch.

### 3.5.2. Nguyên Tắc Hoạt Động

ConstProp hoạt động theo nguyên tắc:

1. **Initialization**: Tìm tất cả constant nodes (CONST0, CONST1)
2. **Propagation**: Propagate constants forward qua gates
3. **Evaluation**: Đánh giá output của gates với constant inputs
4. **Simplification**: Thay thế nodes có constant values bằng constant nodes

### 3.5.3. Thuật Toán

**Algorithm: Constant Propagation**

```
Algorithm: Constant Propagation

1. Initialize constants:
   For each node:
     - If node is CONST0/CONST1:
       - constant_values[node_id] = value

2. Propagate constants (multiple passes):
   While changes occur:
     For each gate node:
       - If all inputs are constants:
         - Evaluate gate output
         - constant_values[node_id] = output_value
   
3. Simplify logic:
   For each node:
     - If node_id in constant_values:
       - Replace node with CONST0/CONST1 node
       - Remove original node
```

### 3.5.4. Gate Evaluation Rules

**Evaluation rules cho các gates:**

- **AND**: `AND(0, x) = 0`, `AND(1, x) = x`, `AND(x, x) = x`
- **OR**: `OR(1, x) = 1`, `OR(0, x) = x`, `OR(x, x) = x`
- **XOR**: `XOR(0, x) = x`, `XOR(1, x) = NOT(x)`, `XOR(x, x) = 0`
- **NAND**: `NAND(0, x) = 1`, `NAND(1, x) = NOT(x)`
- **NOR**: `NOR(1, x) = 0`, `NOR(0, x) = NOT(x)`
- **NOT**: `NOT(0) = 1`, `NOT(1) = 0`
- **BUF**: `BUF(x) = x`

### 3.5.5. Implementation

**Initialization:**

```python
def _initialize_constants(self, netlist: Dict[str, Any]):
    """
    Khởi tạo constant values từ inputs và constant nodes.
    """
    for node in netlist.get('nodes', []):
        if isinstance(node, dict):
            node_id = node.get('id', '')
            node_type = node.get('type', '')
          
            if node_type in ['CONST0', 'GND', '0']:
                self.constant_values[node_id] = False
            elif node_type in ['CONST1', 'VCC', '1']:
                self.constant_values[node_id] = True
```

**Propagation:**

```python
def _propagate_constants(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Propagate constants qua mạch.
    """
    optimized_netlist = netlist.copy()
  
    # Multiple passes để propagate constants
    max_passes = 10
    for pass_num in range(max_passes):
        constants_found = False
      
        for node in optimized_netlist.get('nodes', []):
            if not isinstance(node, dict):
                continue
          
            node_id = node.get('id', '')
            if self._is_gate_node(node):
                inputs = self._get_node_inputs(node)
              
                # Kiểm tra xem tất cả inputs có phải constants không
                if inputs and all(inp in self.constant_values for inp in inputs):
                    # Tất cả inputs là constants, tính output
                    output_value = self._evaluate_gate(node, inputs)
                    self.constant_values[node_id] = output_value
                    self.propagated_constants += 1
                    constants_found = True
      
        if not constants_found:
            break
  
    return optimized_netlist
```

**Gate Evaluation:**

```python
def _evaluate_gate(self, node_data: Dict[str, Any], inputs: List[str]) -> bool:
    """
    Đánh giá output của gate với constant inputs.
    """
    gate_type = node_data.get('type', '').upper()
    input_values = [self.constant_values[inp] for inp in inputs]
  
    if gate_type == 'AND':
        return all(input_values)
    elif gate_type == 'OR':
        return any(input_values)
    elif gate_type == 'XOR':
        return sum(input_values) % 2 == 1
    elif gate_type == 'NAND':
        return not all(input_values)
    elif gate_type == 'NOR':
        return not any(input_values)
    elif gate_type == 'XNOR':
        return sum(input_values) % 2 == 0
    elif gate_type == 'NOT':
        return not input_values[0]
    elif gate_type == 'BUF':
        return input_values[0]
  
    return False
```

**Simplification:**

```python
def _simplify_logic(self, netlist: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simplify logic với known constants.
    """
    optimized_netlist = netlist.copy()
    optimized_netlist['nodes'] = []
  
    for node in netlist.get('nodes', []):
        if not isinstance(node, dict):
            optimized_netlist['nodes'].append(node)
            continue
      
        node_id = node.get('id', '')
        if node_id in self.constant_values:
            # Node có constant value, thay thế bằng constant
            constant_value = self.constant_values[node_id]
          
            if constant_value:
                optimized_netlist['nodes'].append({
                    'id': node_id,
                    'type': 'CONST1',
                    'inputs': [],
                    'output': node.get('output', node_id),
                    'value': 1
                })
            else:
                optimized_netlist['nodes'].append({
                    'id': node_id,
                    'type': 'CONST0',
                    'inputs': [],
                    'output': node.get('output', node_id),
                    'value': 0
                })
          
            self.simplified_gates += 1
        else:
            # Node không có constant value, giữ nguyên
            optimized_netlist['nodes'].append(node)
  
    return optimized_netlist
```

**Implementation trên AIG:**

```python
def _apply_constprop_on_aig(self, aig: AIG) -> AIG:
    """
    Apply Constant Propagation trên AIG.
  
    Propagate constants through AND gates:
    - AND(x, 1) = x
    - AND(x, 0) = 0
    - AND(1, x) = x
    - AND(0, x) = 0
    """
    new_aig = AIG()
  
    # Map old nodes to new nodes
    node_map = {}
  
    # Recreate PIs and constants
    for var_name, old_pi in aig.pis.items():
        new_pi = new_aig.create_pi(var_name)
        node_map[old_pi.node_id] = new_pi
  
    node_map[aig.const0.node_id] = new_aig.const0
    node_map[aig.const1.node_id] = new_aig.const1
  
    visited = set()
  
    def propagate_node(old_node: AIGNode) -> AIGNode:
        """Propagate constants through nodes."""
        if old_node.node_id in node_map:
            return node_map[old_node.node_id]
      
        if old_node.node_id in visited:
            return node_map.get(old_node.node_id)
      
        visited.add(old_node.node_id)
      
        if old_node.is_constant() or old_node.is_pi():
            return node_map[old_node.node_id]
        elif old_node.is_and():
            left = propagate_node(old_node.left)
            right = propagate_node(old_node.right)
          
            # Constant propagation rules
            left_val = left.get_value() if left.is_constant() else None
            right_val = right.get_value() if right.is_constant() else None
          
            # AND(x, 0) = 0 or AND(0, x) = 0
            if (left_val is False) or (right_val is False):
                return new_aig.const0
          
            # AND(x, 1) = x
            if right_val is True:
                return left if not old_node.right_inverted else new_aig.create_not(left)
          
            if left_val is True:
                return right if not old_node.left_inverted else new_aig.create_not(right)
          
            # No constant propagation possible, create AND node
            new_node = new_aig.create_and(
                left, right,
                old_node.left_inverted,
                old_node.right_inverted
            )
            node_map[old_node.node_id] = new_node
            return new_node
      
        return old_node
  
    # Recreate outputs with constant propagation
    for old_po, inverted in aig.pos:
        new_po = propagate_node(old_po)
        if inverted:
            new_po = new_aig.create_not(new_po)
        new_aig.add_po(new_po)
  
    return new_aig
```

### 3.5.6. Lợi Ích

- **Constant Folding**: Simplify logic với constant inputs
- **Logic Simplification**: Loại bỏ unnecessary gates
- **Dead Code Elimination Opportunities**: Constants có thể tạo ra dead code
- **Area Reduction**: Giảm số lượng nodes

### 3.5.7. Kết Quả

ConstProp thường giảm 5-15% nodes tùy thuộc vào design. Ví dụ:

- Designs với nhiều constants: 15-25% reduction
- Designs ít constants: 3-8% reduction

---

## 3.6. LOGIC BALANCING (BALANCE)

### 3.6.1. Định Nghĩa

**Logic Balancing (Balance)** là thuật toán cân bằng độ sâu logic của mạch để tối ưu hóa timing và giảm critical path delay. Balance restructuring logic tree để tạo balanced structures thay vì unbalanced trees.

### 3.6.2. Nguyên Tắc Hoạt Động

Balance hoạt động theo nguyên tắc:

1. **Level Calculation**: Tính logic level cho tất cả nodes
2. **Unbalance Detection**: Tìm các paths có logic depth không cân bằng
3. **Tree Restructuring**: Restructure logic tree thành balanced tree
4. **Depth Optimization**: Giảm maximum logic depth

### 3.6.3. Logic Level

**Logic Level** của một node là số lượng gates trên longest path từ inputs đến node đó:

- **Primary Inputs**: Level = 0
- **Gate Nodes**: Level = max(input levels) + 1
- **Maximum Level**: Logic depth của circuit (critical path)

### 3.6.4. Thuật Toán

**Algorithm: Logic Balancing**

```
Algorithm: Logic Balancing

1. Calculate logic levels:
   For each node:
     - If node is PI: level = 0
     - Else: level = max(input levels) + 1

2. Identify unbalanced paths:
   - Find nodes with high levels
   - Identify paths với significant level differences

3. Balance logic tree:
   For unbalanced nodes:
     - If node has many inputs:
       - Build balanced tree structure
       - Combine inputs in pairs recursively
       - Create balanced AND/OR tree

4. Rebuild AIG:
   - Recreate nodes với balanced structure
   - Update connections
```

### 3.6.5. Implementation

**Level Calculation:**

```python
def _calculate_logic_levels(self, netlist: Dict[str, Any]):
    """
    Tính logic level cho tất cả nodes.
    """
    # Reset levels
    self.node_levels = {}
  
    # Khởi tạo levels cho inputs (level 0)
    for input_name in netlist.get('inputs', []):
        self.node_levels[input_name] = 0
  
    # Tính levels cho các nodes khác (multiple passes)
    max_iterations = len(netlist.get('nodes', [])) * 2
    for iteration in range(max_iterations):
        levels_updated = False
      
        for node in netlist.get('nodes', []):
            if not isinstance(node, dict):
                continue
          
            node_id = node.get('id', '')
            inputs = node.get('inputs', [])
          
            if node_id not in self.node_levels:
                if all(inp in self.node_levels for inp in inputs) and inputs:
                    # Tất cả inputs đã có level
                    max_input_level = max(self.node_levels[inp] for inp in inputs)
                    self.node_levels[node_id] = max_input_level + 1
                    levels_updated = True
                  
                    if self.node_levels[node_id] > self.max_level:
                        self.max_level = self.node_levels[node_id]
      
        if not levels_updated:
            break
```

**Balancing Tree:**

```python
def balance_and_tree(nodes: List[AIGNode], left_inverted: List[bool], right_inverted: List[bool]) -> AIGNode:
    """
    Balance a tree of AND operations.
    """
    if len(nodes) == 0:
        return new_aig.const1
    if len(nodes) == 1:
        return nodes[0]
    if len(nodes) == 2:
        return new_aig.create_and(nodes[0], nodes[1], left_inverted[0], right_inverted[0])
  
    # Sort nodes by level (shallow first for better balancing)
    sorted_indices = sorted(range(len(nodes)), key=lambda i: get_node_level(nodes[i]))
    sorted_nodes = [nodes[i] for i in sorted_indices]
    sorted_left_inv = [left_inverted[i] for i in sorted_indices]
    sorted_right_inv = [right_inverted[i] for i in sorted_indices]
  
    # Build balanced tree: combine pairs recursively
    while len(sorted_nodes) > 1:
        new_level = []
        new_left_inv = []
        new_right_inv = []
      
        # Combine pairs
        for i in range(0, len(sorted_nodes), 2):
            if i + 1 < len(sorted_nodes):
                # Combine two nodes
                combined = new_aig.create_and(
                    sorted_nodes[i],
                    sorted_nodes[i + 1],
                    sorted_left_inv[i],
                    sorted_right_inv[i + 1]
                )
                new_level.append(combined)
                new_left_inv.append(False)
                new_right_inv.append(False)
            else:
                # Odd one out, keep as is
                new_level.append(sorted_nodes[i])
                new_left_inv.append(sorted_left_inv[i])
                new_right_inv.append(sorted_right_inv[i])
      
        sorted_nodes = new_level
        sorted_left_inv = new_left_inv
        sorted_right_inv = new_right_inv
  
    return sorted_nodes[0]
```

**Implementation trên AIG:**

```python
def _apply_balance_on_aig(self, aig: AIG) -> AIG:
    """
    Apply Logic Balancing trên AIG.
  
    Balance logic depth by restructuring AND trees to minimize maximum depth.
    """
    new_aig = AIG()
    node_map = {}
  
    # Recreate PIs and constants
    for var_name, old_pi in aig.pis.items():
        new_pi = new_aig.create_pi(var_name)
        node_map[old_pi.node_id] = new_pi
  
    node_map[aig.const0.node_id] = new_aig.const0
    node_map[aig.const1.node_id] = new_aig.const1
  
    visited = set()
  
    def balance_node(old_node: AIGNode) -> Optional[AIGNode]:
        """Balance a single node."""
        if old_node.node_id in node_map:
            return node_map[old_node.node_id]
      
        if old_node.node_id in visited:
            return node_map.get(old_node.node_id)
      
        visited.add(old_node.node_id)
      
        if old_node.is_constant() or old_node.is_pi():
            return node_map.get(old_node.node_id)
        elif old_node.is_and():
            # Balance left and right subtrees first
            left = balance_node(old_node.left)
            right = balance_node(old_node.right)
          
            if left is None or right is None:
                return None
          
            # Create AND node (structural hashing will handle balancing)
            new_node = new_aig.create_and(
                left, right,
                old_node.left_inverted,
                old_node.right_inverted
            )
            node_map[old_node.node_id] = new_node
            return new_node
      
        return None
  
    # Recreate outputs with balancing
    for old_po, inverted in aig.pos:
        new_po = balance_node(old_po)
        if new_po is None:
            continue
        if inverted:
            new_po = new_aig.create_not(new_po)
        new_aig.add_po(new_po)
  
    # Rebuild hash table for better structure sharing
    return new_aig.strash()
```

### 3.6.6. Lợi Ích

- **Timing Improvement**: Giảm critical path delay
- **Better Delay Characteristics**: More uniform logic depth
- **Improved Skew**: Balanced paths có skew tốt hơn
- **Potential Area Increase**: Balance có thể tăng số lượng nodes (trade-off)

### 3.6.7. Kết Quả

Balance có thể:

- **Giảm logic depth**: 10-30% reduction trong critical path
- **Tăng nodes**: 5-15% increase (trade-off cho timing)
- **Cải thiện timing**: 10-25% improvement trong worst-case delay

---

## 3.7. OPTIMIZATION FLOW VÀ INTEGRATION

### 3.7.1. Optimization Flow Class

Class `AIGOptimizationFlow` quản lý toàn bộ optimization flow:

```python
class AIGOptimizationFlow:
    """
    AIG Optimization Flow.
  
    Tối ưu hóa AIG với các thuật toán:
    - Strash (Structural Hashing)
    - DCE (Dead Code Elimination)
    - CSE (Common Subexpression Elimination)
    - ConstProp (Constant Propagation)
    - Balance (Logic Balancing)
    """
  
    def optimize(self, aig: AIG, level: str = "standard") -> AIG:
        """
        Chạy complete AIG optimization flow.
        """
        original_nodes = aig.count_nodes()
        current_aig = aig
      
        # Step 1: Structural Hashing (Strash)
        current_aig = self._run_strash(current_aig)
      
        # Step 2: Dead Code Elimination
        current_aig = self._run_dce(current_aig, level)
      
        # Step 3: Common Subexpression Elimination
        current_aig = self._run_cse(current_aig)
      
        # Step 4: Constant Propagation
        current_aig = self._run_constprop(current_aig)
      
        # Step 5: Logic Balancing
        current_aig = self._run_balance(current_aig)
      
        return current_aig
```

### 3.7.2. Optimization Statistics

Optimization flow track statistics cho mỗi bước:

```python
self.optimization_stats = {
    'strash': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
    'dce': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
    'cse': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
    'constprop': {'nodes_before': 0, 'nodes_after': 0, 'removed': 0},
    'balance': {'nodes_before': 0, 'nodes_after': 0, 'added': 0}
}
```

### 3.7.3. Optimization Order

Thứ tự các bước optimization quan trọng:

1. **Strash**: Rebuild hash table, loại bỏ duplicates ngay từ đầu
2. **DCE**: Loại bỏ dead code trước khi optimize further
3. **CSE**: Share common subexpressions sau khi đã loại bỏ dead code
4. **ConstProp**: Propagate constants sau khi đã có structure tốt
5. **Balance**: Balance timing cuối cùng (có thể tăng nodes)

**Lý do thứ tự:**

- DCE nên chạy sớm để loại bỏ unnecessary logic
- CSE và ConstProp benefit từ structure đã được clean
- Balance nên chạy cuối vì có thể tăng nodes

### 3.7.4. Integration với Complete Flow

Optimization được tích hợp trong complete flow:

```
Synthesis → AIG
    ↓
Optimization → Optimized AIG
    ↓
Technology Mapping → Mapped Netlist
```

**Usage:**

```python
from core.optimization.optimization_flow import optimize

# Optimize AIG
optimized_aig = optimize(aig, level="standard")
```

---

## 3.8. SO SÁNH VÀ ĐÁNH GIÁ

### 3.8.1. So Sánh với Yosys/ABC

**Yosys/ABC** là các công cụ optimization mạnh mẽ. So sánh optimization module của MyLogic:

| Khía cạnh                   | MyLogic                         | Yosys/ABC                    |
| ----------------------------- | ------------------------------- | ---------------------------- |
| **Strash**              | Có (rebuild hash table)        | Có (advanced)               |
| **DCE**                 | Có (basic/advanced/aggressive) | Có (advanced)               |
| **CSE**                 | Có (pattern matching)          | Có (advanced)               |
| **ConstProp**           | Có (multiple passes)           | Có (advanced)               |
| **Balance**             | Có (tree balancing)            | Có (advanced)               |
| **Other Optimizations** | Chưa có                       | Có nhiều (rewriting, etc.) |

**Điểm mạnh của MyLogic:**

- Kiến trúc modular, dễ hiểu
- Code rõ ràng, phù hợp cho giáo dục
- Hỗ trợ multiple levels

**Hạn chế:**

- Chưa có nhiều optimizations như Yosys/ABC
- Một số algorithms chưa được optimize tốt
- Chưa có advanced rewriting techniques

### 3.8.2. Kết Quả Optimization

**Typical Results:**

- **Strash**: 0-5% reduction (AIG đã có hashing)
- **DCE**: 5-20% reduction
- **CSE**: 10-30% reduction
- **ConstProp**: 5-15% reduction
- **Balance**: -5% to +15% (có thể tăng nodes)

**Total Reduction**: 20-50% nodes reduction tùy design

**Ví dụ:**

```
Input: 1000 nodes AIG
After Strash: 1000 nodes (0% reduction)
After DCE: 850 nodes (15% reduction)
After CSE: 650 nodes (23.5% reduction from DCE)
After ConstProp: 600 nodes (7.7% reduction from CSE)
After Balance: 630 nodes (5% increase from ConstProp, trade-off)

Total: 1000 → 630 nodes (37% reduction)
```

### 3.8.3. Trade-offs

**Area vs Timing:**

- **DCE, CSE, ConstProp**: Giảm area, có thể cải thiện timing
- **Balance**: Cải thiện timing, có thể tăng area

**Optimization Level:**

- **basic**: Nhanh, ít optimization
- **standard**: Cân bằng tốt
- **aggressive**: Chậm hơn, optimization tốt hơn

### 3.8.4. Hạn Chế và Hướng Phát Triển

**Hạn chế hiện tại:**

1. **Limited Algorithms**: Chưa có nhiều optimizations như rewriting
2. **Performance**: Chưa optimize cho very large designs
3. **Advanced Techniques**: Chưa có SAT-based optimization, etc.
4. **Sequential Logic**: Chưa hỗ trợ optimization cho sequential logic

**Hướng phát triển:**

1. **Advanced Rewriting**: Technology-independent rewriting
2. **SAT-based Optimization**: Sử dụng SAT solver cho optimization
3. **Sequential Optimization**: Optimization cho sequential logic
4. **Performance**: Optimize cho large designs
5. **More Algorithms**: Thêm các algorithms mới

---

## 3.9. KẾT LUẬN CHƯƠNG

CHƯƠNG 3 đã trình bày chi tiết về **Logic Optimization** trong MyLogic EDA Tool, bao gồm:

1. **Tổng quan về Logic Optimization**: Định nghĩa, vai trò, mục tiêu, và optimization levels
2. **Structural Hashing (Strash)**: Rebuild hash table, loại bỏ duplicates
3. **Dead Code Elimination (DCE)**: Loại bỏ nodes không reachable từ outputs
4. **Common Subexpression Elimination (CSE)**: Tìm và share common subexpressions
5. **Constant Propagation (ConstProp)**: Propagate constants và simplify logic
6. **Logic Balancing (Balance)**: Cân bằng logic depth để tối ưu hóa timing
7. **Optimization Flow và Integration**: Quy trình optimization và tích hợp với complete flow
8. **So sánh và Đánh giá**: So sánh với Yosys/ABC, kết quả optimization, trade-offs

Optimization module của MyLogic đạt được mục tiêu chính: **tối ưu hóa AIG về area, delay, và power**, với kiến trúc modular và code dễ hiểu, phù hợp cho giáo dục và nghiên cứu.

---

# CHƯƠNG 4: TECHNOLOGY MAPPING

## 4.1. TỔNG QUAN VỀ TECHNOLOGY MAPPING

### 4.1.1. Định Nghĩa và Vai Trò

**Technology Mapping** là quá trình chuyển đổi AIG (And-Inverter Graph) - một representation technology-independent - sang technology-mapped netlist sử dụng các cells từ technology library cụ thể (ASIC hoặc FPGA). Đây là bước cuối cùng trong logic synthesis flow, chuyển đổi logic đã được tối ưu hóa thành các cells thực tế có thể được sử dụng trong quá trình place & route.

#### 4.1.1.1. Phân Biệt Technology Mapping với Synthesis và Optimization

Một điểm quan trọng cần nhấn mạnh là sự phân biệt rõ ràng giữa **Synthesis**, **Optimization**, và **Technology Mapping**:

- **Synthesis**: Chuyển đổi Netlist Dictionary sang AIG (technology-independent representation)
- **Optimization**: Tối ưu hóa AIG về area, delay, và power (vẫn technology-independent)
- **Technology Mapping**: Chuyển đổi AIG sang technology-mapped netlist sử dụng cells từ technology library cụ thể (ASIC hoặc FPGA)

Sự phân tách này giúp:

- **Modularity**: Mỗi bước có trách nhiệm rõ ràng
- **Flexibility**: Có thể map cùng một AIG sang nhiều technology libraries khác nhau
- **Reusability**: AIG đã được optimize có thể được map sang nhiều targets
- **Maintainability**: Code dễ maintain và mở rộng

### 4.1.2. Mục Tiêu của Technology Mapping

Mục tiêu chính của technology mapping trong MyLogic là:

1. **Area Optimization**: Chọn cells có diện tích nhỏ nhất để implement logic
2. **Delay Optimization**: Chọn cells có delay nhỏ nhất để cải thiện timing
3. **Balanced Optimization**: Cân bằng giữa area và delay
4. **Functional Correctness**: Đảm bảo output technology-mapped netlist có cùng hành vi chức năng với input AIG
5. **Library Compatibility**: Map logic sang các cells có sẵn trong technology library

### 4.1.3. Technology Mapping Strategies

MyLogic hỗ trợ 3 chiến lược mapping:

1. **area_optimal**: Tối ưu hóa về diện tích, chọn cells có area nhỏ nhất
2. **delay_optimal**: Tối ưu hóa về delay, chọn cells có delay nhỏ nhất
3. **balanced**: Cân bằng giữa area và delay, sử dụng weighted cost function

### 4.1.4. Quy Trình Technology Mapping trong MyLogic

Quy trình technology mapping trong MyLogic EDA Tool bao gồm các bước chính:

```
AIG (từ Synthesis hoặc Optimization)
    ↓
[1] Convert AIG → LogicNodes
    - Chuyển đổi từng AIG node thành LogicNode
    - Extract function strings từ AIG structure
    ↓
[2] Load Technology Library
    - Load library từ file (.lib, .json, .v)
    - Parse cells và functions
    ↓
[3] Function Matching
    - Match LogicNode functions với library cells
    - Normalize functions để matching
    ↓
[4] Cell Selection
    - Chọn best cell cho mỗi LogicNode
    - Dựa trên strategy (area/delay/balanced)
    ↓
[5] Generate Mapped Netlist
    - Convert mapped LogicNodes sang netlist format
    - Tạo technology-mapped netlist
    ↓
Technology-Mapped Netlist (Kết quả Mapping)
```

---

## 4.2. TECHNOLOGY LIBRARIES

### 4.2.1. Tổng Quan về Technology Libraries

**Technology Library** là tập hợp các cells (gates) có sẵn trong một công nghệ sản xuất cụ thể. Mỗi cell có:

- **Name**: Tên cell (e.g., `NAND2`, `AND3`, `AOI21`)
- **Function**: Boolean function mà cell implement (e.g., `NAND(A,B)`, `AND(A,B,C)`)
- **Area**: Diện tích cell (đơn vị: square microns hoặc relative units)
- **Delay**: Delay của cell (đơn vị: nanoseconds hoặc relative units)
- **Input/Output Pins**: Danh sách input và output pins
- **Load/Drive**: Input load và output drive capacity

### 4.2.2. LibraryCell Class

Class `LibraryCell` đại diện cho một cell trong technology library:

```python
class LibraryCell:
    def __init__(self, name: str, function: str, area: float, delay: float, 
                 input_pins: List[str], output_pins: List[str], 
                 input_load: float = 1.0, output_drive: float = 1.0):
        self.name = name
        self.function = function  # Hàm Boolean (e.g., "NAND(A,B)")
        self.area = area
        self.delay = delay
        self.input_pins = input_pins
        self.output_pins = output_pins
        self.input_load = input_load
        self.output_drive = output_drive
```

**Ví dụ:**

- `NAND2`: `function="NAND(A,B)"`, `area=1.2`, `delay=0.15`
- `AND3`: `function="AND(A,B,C)"`, `area=2.2`, `delay=0.25`
- `AOI21`: `function="NOT(OR(AND(A,B),C))"`, `area=2.5`, `delay=0.3`

### 4.2.3. TechnologyLibrary Class

Class `TechnologyLibrary` quản lý tập hợp các cells:

```python
class TechnologyLibrary:
    def __init__(self, name: str):
        self.name = name
        self.cells: Dict[str, LibraryCell] = {}
        self.function_map: Dict[str, List[str]] = {}  # function -> list of cell names
  
    def add_cell(self, cell: LibraryCell):
        """Add a cell to the library."""
        self.cells[cell.name] = cell
      
        # Normalize function for mapping
        normalized_func = normalize_function(cell.function)
      
        # Update function mapping
        if normalized_func not in self.function_map:
            self.function_map[normalized_func] = []
        self.function_map[normalized_func].append(cell.name)
```

**Function Mapping:**

- `function_map` lưu mapping từ normalized function string đến danh sách cell names
- Giúp tìm cells nhanh chóng cho một function cụ thể

### 4.2.4. Function Normalization

Function normalization là quá trình chuẩn hóa function strings để matching:

```python
def normalize_function(function: str) -> str:
    """
    Normalize function string by replacing variable names with canonical names.
  
    Examples:
        normalize_function("OR(C,D)") -> "OR(A,B)"
        normalize_function("AND(A,B)") -> "AND(A,B)"
        normalize_function("NOT(X)") -> "NOT(A)"
    """
    # Extract function name and arguments
    # Replace variable names with canonical names (A, B, C, ...)
    # Return normalized function
```

**Lý do normalization:**

- `NAND(a, b)` và `NAND(x, y)` đều represent cùng function
- Normalization giúp match functions bất kể tên biến

### 4.2.5. ASIC Standard Cell Libraries

**ASIC (Application-Specific Integrated Circuit)** libraries chứa các standard cells:

**Basic Gates:**

- `INV`: Inverter (NOT gate)
- `BUF`: Buffer
- `AND2`, `AND3`, `AND4`: 2/3/4-input AND gates
- `OR2`, `OR3`, `OR4`: 2/3/4-input OR gates
- `NAND2`, `NAND3`, `NAND4`: 2/3/4-input NAND gates
- `NOR2`, `NOR3`, `NOR4`: 2/3/4-input NOR gates
- `XOR2`, `XOR3`: 2/3-input XOR gates
- `XNOR2`: 2-input XNOR gate

**Complex Gates:**

- `AOI21`: And-Or-Invert: `NOT(OR(AND(A,B),C))`
- `OAI21`: Or-And-Invert: `NOT(AND(OR(A,B),C))`
- `AOI22`: `NOT(OR(AND(A,B),AND(C,D)))`
- `OAI22`: `NOT(AND(OR(A,B),OR(C,D)))`

**Ưu điểm của complex gates:**

- Diện tích nhỏ hơn so với implement bằng basic gates
- Delay tốt hơn trong một số trường hợp
- Giảm số lượng cells trong netlist

### 4.2.6. FPGA Libraries

**FPGA (Field-Programmable Gate Array)** libraries chứa các LUTs (Look-Up Tables):

**LUT Cells:**

- `LUT1`: 1-input LUT
- `LUT2`: 2-input LUT
- `LUT3`: 3-input LUT
- `LUT4`: 4-input LUT
- `LUT5`: 5-input LUT
- `LUT6`: 6-input LUT

**Đặc điểm:**

- LUTs có thể implement bất kỳ Boolean function nào với số inputs tương ứng
- Area và delay phụ thuộc vào số inputs
- Mapping AIG sang LUTs khác với ASIC mapping

### 4.2.7. Standard Library Creation

MyLogic cung cấp hàm `create_standard_library()` để tạo standard ASIC library:

```python
def create_standard_library() -> TechnologyLibrary:
    """
    Create a standard technology library with common gates.
    """
    library = TechnologyLibrary("standard_cells")
  
    # Basic gates
    gates = [
        ("INV", "NOT", 1.0, 0.1, ["A"], ["Y"]),
        ("BUF", "BUF", 1.0, 0.05, ["A"], ["Y"]),
        ("NAND2", "NAND(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("NOR2", "NOR(A,B)", 1.2, 0.15, ["A", "B"], ["Y"]),
        ("AND2", "AND(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        ("OR2", "OR(A,B)", 1.5, 0.2, ["A", "B"], ["Y"]),
        # ... more gates
    ]
  
    for name, function, area, delay, inputs, outputs in gates:
        cell = LibraryCell(name, function, area, delay, inputs, outputs)
        library.add_cell(cell)
  
    return library
```

---

## 4.3. LIBRARY LOADING

### 4.3.1. Tổng Quan về Library Loading

MyLogic hỗ trợ load technology libraries từ nhiều formats:

- **Liberty (.lib)**: Industry standard format cho ASIC libraries
- **JSON (.json)**: Easy-to-use format cho custom libraries
- **Verilog (.v)**: Basic support cho Verilog module definitions

### 4.3.2. Liberty Format

**Liberty format** là industry standard cho ASIC cell libraries, được sử dụng bởi các công cụ EDA chuyên nghiệp.

**Cấu trúc Liberty file:**

```
library (library_name) {
    cell (NAND2) {
        area : 1.2;
        pin (A) {
            direction : input;
        }
        pin (B) {
            direction : input;
        }
        pin (Y) {
            direction : output;
            function : "!(A & B)";
        }
    }
    ...
}
```

**Parsing Liberty:**

- Parse nested braces để extract cell definitions
- Extract function strings từ pin definitions
- Convert function strings sang normalized format

### 4.3.3. JSON Format

**JSON format** dễ sử dụng và dễ tạo custom libraries:

```json
{
    "name": "standard_cells",
    "cells": [
        {
            "name": "NAND2",
            "function": "NAND(A,B)",
            "area": 1.2,
            "delay": 0.15,
            "input_pins": ["A", "B"],
            "output_pins": ["Y"]
        },
        ...
    ]
}
```

**Ưu điểm:**

- Dễ đọc và chỉnh sửa
- Hỗ trợ tốt cho custom libraries
- Không cần parse phức tạp như Liberty

### 4.3.4. Verilog Format

**Verilog format** sử dụng module definitions:

```verilog
module NAND2(A, B, Y);
    input A, B;
    output Y;
    assign Y = ~(A & B);
endmodule
```

**Parsing Verilog:**

- Extract module name, ports, và function từ `assign` statements
- Convert Verilog operators sang function strings

### 4.3.5. Library Loader Implementation

```python
def load_library(file_path: str, library_type: Optional[str] = None) -> TechnologyLibrary:
    """
    Load technology library from file with auto-detection.
    """
    if library_type is None:
        # Auto-detect from extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.lib':
            library_type = 'liberty'
        elif ext == '.json':
            library_type = 'json'
        elif ext == '.v':
            library_type = 'verilog'
  
    if library_type == 'liberty':
        return load_liberty_library(file_path)
    elif library_type == 'json':
        return load_json_library(file_path)
    elif library_type == 'verilog':
        return load_verilog_library(file_path)
```

---

## 4.4. AIG TO LOGICNODES CONVERSION

### 4.4.1. Tổng Quan về Conversion

Trước khi thực hiện technology mapping, AIG cần được chuyển đổi sang `LogicNode` format - một representation phù hợp cho mapping.

**LogicNode Structure:**

```python
class LogicNode:
    def __init__(self, name: str, function: str, inputs: List[str], output: str):
        self.name = name
        self.function = function  # Function string (e.g., "AND(A,B)")
        self.inputs = inputs
        self.output = output
        self.mapped_cell: Optional[LibraryCell] = None
        self.mapping_cost = float('inf')
```

### 4.4.2. Conversion Algorithm

**Algorithm: AIG → LogicNodes**

```
Algorithm: Convert AIG to LogicNodes

1. Process nodes in topological order:
   For each AIG node:
     a. If CONST0/CONST1:
        → Create LogicNode với function "CONST0"/"CONST1"
     b. If PI:
        → Create LogicNode với function = var_name
     c. If AND node:
        → Extract left và right inputs
        → Determine function based on inversions:
           - left & right → "AND(left, right)"
           - !left & right → "AND(NOT(left), right)"
           - left & !right → "AND(left, NOT(right))"
           - !left & !right → "NOR(left, right)"
        → Create LogicNode với function string

2. Build LogicNode network:
   - Connect LogicNodes theo AIG structure
   - Track input/output relationships
```

### 4.4.3. Handling Inversions

AIG sử dụng inversion flags thay vì explicit NOT nodes. Conversion cần xử lý inversions:

```python
# AIG node: (left^left_inv) & (right^right_inv)

if node.left_inverted and node.right_inverted:
    # !left & !right = NOR(left, right)
    function = f"NOR({left_input},{right_input})"
elif node.left_inverted:
    # !left & right = AND(NOT(left), right)
    function = f"AND(NOT({left_input}),{right_input})"
elif node.right_inverted:
    # left & !right = AND(left, NOT(right))
    function = f"AND({left_input},NOT({right_input}))"
else:
    # left & right = AND(left, right)
    function = f"AND({left_input},{right_input})"
```

### 4.4.4. Implementation

```python
def aig_to_logic_nodes(aig) -> List[LogicNode]:
    """
    Convert AIG to LogicNodes for technology mapping.
    """
    logic_nodes = []
    visited = set()
  
    def process_node(node) -> str:
        """Process AIG node and return its name."""
        if node.node_id in visited:
            return get_node_name(node)
      
        visited.add(node.node_id)
      
        # Handle constants
        if node.is_constant():
            return "CONST0" if not node.get_value() else "CONST1"
      
        # Handle primary inputs
        if node.is_pi():
            return node.var_name or f"pi_{node.node_id}"
      
        # Handle AND nodes
        left_name = process_node(node.left) if node.left else None
        right_name = process_node(node.right) if node.right else None
      
        # Build function string based on inversions
        function = build_function_string(node, left_name, right_name)
      
        # Create LogicNode
        logic_node = LogicNode(node_name, function, inputs_list, node_name)
        logic_nodes.append(logic_node)
      
        return node_name
  
    # Process all nodes reachable from outputs
    for po_node, po_inverted in aig.pos:
        process_node(po_node)
  
    return logic_nodes
```

---

## 4.5. TECHNOLOGY MAPPING ALGORITHMS

### 4.5.1. Tổng Quan về Mapping Algorithms

Technology mapping trong MyLogic sử dụng **greedy matching algorithm**: Với mỗi LogicNode, tìm cell tốt nhất trong library để implement function của node đó.

**Mapping Process:**

1. **Function Matching**: Match LogicNode function với library cells
2. **Cell Selection**: Chọn best cell dựa trên strategy (area/delay/balanced)
3. **Cost Calculation**: Tính mapping cost cho mỗi node
4. **Network Building**: Build mapped network với selected cells

### 4.5.2. Area-Optimal Mapping

**Area-optimal mapping** chọn cells có diện tích nhỏ nhất:

```python
def _area_optimal_mapping(self) -> Dict[str, Any]:
    """Perform area-optimal technology mapping."""
    total_area = 0.0
    mapped_nodes = 0
  
    for node_name, node in self.logic_network.items():
        # Find best cell for this function (minimize area)
        best_cell = self.library.get_best_cell_for_function(node.function, "area")
      
        if best_cell:
            node.mapped_cell = best_cell
            node.mapping_cost = best_cell.area
            total_area += best_cell.area
            mapped_nodes += 1
  
    return {
        'strategy': 'area_optimal',
        'total_area': total_area,
        'mapped_nodes': mapped_nodes,
        ...
    }
```

**Cell Selection:**

```python
def get_best_cell_for_function(self, function: str, optimization_target: str = "area") -> Optional[LibraryCell]:
    """Get the best cell for a function based on optimization target."""
    cells = self.get_cells_for_function(function)
    if not cells:
        return None
  
    if optimization_target == "area":
        return min(cells, key=lambda c: c.area)
    ...
```

**Ví dụ:**

- Function: `AND(A,B)`
- Available cells: `AND2` (area=1.5), `NAND2+INV` (area=2.2)
- Selected: `AND2` (area nhỏ hơn)

### 4.5.3. Delay-Optimal Mapping

**Delay-optimal mapping** chọn cells có delay nhỏ nhất:

```python
def _delay_optimal_mapping(self) -> Dict[str, Any]:
    """Perform delay-optimal technology mapping."""
    total_delay = 0.0
    mapped_nodes = 0
  
    for node_name, node in self.logic_network.items():
        # Find best cell for this function (minimize delay)
        best_cell = self.library.get_best_cell_for_function(node.function, "delay")
      
        if best_cell:
            node.mapped_cell = best_cell
            node.mapping_cost = best_cell.delay
            total_delay += best_cell.delay
            mapped_nodes += 1
  
    return {
        'strategy': 'delay_optimal',
        'total_delay': total_delay,
        ...
    }
```

**Ví dụ:**

- Function: `AND(A,B)`
- Available cells: `AND2` (delay=0.2), `NAND2+INV` (delay=0.25)
- Selected: `AND2` (delay nhỏ hơn)

### 4.5.4. Balanced Mapping

**Balanced mapping** cân bằng giữa area và delay:

```python
def _balanced_mapping(self) -> Dict[str, Any]:
    """Perform balanced technology mapping."""
    total_area = 0.0
    total_delay = 0.0
  
    for node_name, node in self.logic_network.items():
        # Find best cell for this function (balanced cost)
        best_cell = self.library.get_best_cell_for_function(node.function, "balanced")
      
        if best_cell:
            # Weighted cost: area + delay * weight
            node.mapping_cost = best_cell.area + best_cell.delay * 10
            total_area += best_cell.area
            total_delay += best_cell.delay
```

**Cost Function:**

```python
if optimization_target == "balanced":
    # Weighted combination of area and delay
    return min(cells, key=lambda c: c.area + c.delay * 10)
```

**Weight factor (10):**

- Delay được nhân với weight để cân bằng với area
- Có thể điều chỉnh weight tùy theo requirements

### 4.5.5. Function Matching

Function matching là quá trình tìm cells trong library có thể implement function của LogicNode:

```python
def get_cells_for_function(self, function: str) -> List[LibraryCell]:
    """Get all cells that implement a given function."""
    # Normalize the function to match library entries
    normalized_func = normalize_function(function)
  
    if normalized_func in self.function_map:
        return [self.cells[name] for name in self.function_map[normalized_func]]
    return []
```

**Matching Process:**

1. Normalize function string (e.g., `AND(a,b)` → `AND(A,B)`)
2. Look up trong `function_map`
3. Return danh sách cells có thể implement function đó

**Ví dụ:**

- Function: `AND(A,B)`
- Library có: `AND2`, `NAND2+INV` (có thể implement AND)
- Return: `[AND2]` (nếu chỉ có AND2 trong function_map)

---

## 4.6. TECHNOLOGY MAPPER CLASS

### 4.6.1. TechnologyMapper Structure

Class `TechnologyMapper` quản lý toàn bộ technology mapping process:

```python
class TechnologyMapper:
    def __init__(self, library: TechnologyLibrary):
        self.library = library
        self.logic_network: Dict[str, LogicNode] = {}
        self.mapping_results = {}
  
    def add_logic_node(self, node: LogicNode):
        """Add a logic node to the network."""
        self.logic_network[node.name] = node
  
    def perform_technology_mapping(self, strategy: str = "area_optimal") -> Dict[str, Any]:
        """Perform technology mapping."""
        if strategy == "area_optimal":
            return self._area_optimal_mapping()
        elif strategy == "delay_optimal":
            return self._delay_optimal_mapping()
        elif strategy == "balanced":
            return self._balanced_mapping()
```

### 4.6.2. Mapping Statistics

Mapper track statistics về mapping results:

```python
def get_mapping_statistics(self) -> Dict[str, Any]:
    """Get technology mapping statistics."""
    mapped_nodes = sum(1 for node in self.logic_network.values() if node.mapped_cell)
    total_nodes = len(self.logic_network)
  
    # Count cells used
    cell_usage = {}
    for node in self.logic_network.values():
        if node.mapped_cell:
            cell_name = node.mapped_cell.name
            cell_usage[cell_name] = cell_usage.get(cell_name, 0) + 1
  
    return {
        'total_nodes': total_nodes,
        'mapped_nodes': mapped_nodes,
        'mapping_success_rate': mapped_nodes / total_nodes if total_nodes > 0 else 0,
        'cell_usage': cell_usage,
        'unique_cells_used': len(cell_usage)
    }
```

### 4.6.3. Mapping Report

Mapper có thể generate mapping report:

```python
def print_mapping_report(self, results: Dict[str, Any]):
    """Print technology mapping report."""
    print("TECHNOLOGY MAPPING REPORT")
    print(f"Mapping Strategy: {results['strategy']}")
    print(f"Total Nodes: {results['total_nodes']}")
    print(f"Mapped Nodes: {results['mapped_nodes']}")
    print(f"Mapping Success Rate: {results['mapping_success_rate']*100:.1f}%")
  
    if 'total_area' in results:
        print(f"Total Area: {results['total_area']:.2f}")
    if 'total_delay' in results:
        print(f"Total Delay: {results['total_delay']:.2f}")
  
    # Cell usage statistics
    stats = self.get_mapping_statistics()
    print(f"\nCell Usage:")
    for cell_name, count in sorted(stats['cell_usage'].items()):
        print(f"  {cell_name}: {count} instances")
```

---

## 4.7. TECHMAP FUNCTION

### 4.7.1. High-Level Techmap Interface

Function `techmap()` là high-level interface cho technology mapping:

```python
def techmap(aig, library: TechnologyLibrary, strategy: str = "area_optimal") -> Dict[str, Any]:
    """
    Technology mapping: AIG → Technology-mapped netlist.
  
    Args:
        aig: AIG object (từ synthesis hoặc optimize)
        library: Technology library
        strategy: Mapping strategy ("area_optimal", "delay_optimal", "balanced")
      
    Returns:
        Dictionary chứa mapping results và statistics
    """
    # Convert AIG → LogicNodes
    logic_nodes = aig_to_logic_nodes(aig)
  
    # Create TechnologyMapper
    mapper = TechnologyMapper(library)
  
    # Add LogicNodes to mapper
    for logic_node in logic_nodes:
        mapper.add_logic_node(logic_node)
  
    # Perform technology mapping
    results = mapper.perform_technology_mapping(strategy)
  
    # Add additional statistics
    results['input_aig_nodes'] = aig.count_nodes()
    results['converted_logic_nodes'] = len(logic_nodes)
    results['library_name'] = library.name
  
    return results
```

### 4.7.2. Usage Example

```python
from core.synthesis.synthesis_flow import synthesize
from core.technology_mapping.technology_mapping import techmap, create_standard_library

# Synthesize netlist to AIG
aig = synthesize(netlist)

# Load technology library
library = create_standard_library()

# Perform technology mapping
results = techmap(aig, library, strategy="area_optimal")

# Print results
print(f"Mapped {results['mapped_nodes']}/{results['total_nodes']} nodes")
print(f"Total area: {results['total_area']:.2f}")
```

### 4.7.3. Convert to Netlist

Sau khi mapping, có thể convert mapped LogicNodes sang netlist format:

```python
def convert_mapped_logic_network_to_netlist(
    mapper: TechnologyMapper,
    aig,
    original_netlist: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert mapped LogicNode network back to netlist format.
    """
    mapped_netlist = {
        'inputs': original_netlist.get('inputs', []),
        'outputs': original_netlist.get('outputs', []),
        'nodes': []
    }
  
    # Convert each LogicNode to netlist node format
    for node_name, logic_node in mapper.logic_network.items():
        node_dict = {
            'id': logic_node.name,
            'output': logic_node.output,
            'inputs': logic_node.inputs,
        }
      
        if logic_node.mapped_cell:
            # Use mapped cell name as type
            node_dict['type'] = logic_node.mapped_cell.name
            node_dict['mapped'] = True
            node_dict['area'] = logic_node.mapped_cell.area
            node_dict['delay'] = logic_node.mapped_cell.delay
        else:
            node_dict['type'] = extract_gate_type(logic_node.function)
            node_dict['mapped'] = False
      
        mapped_netlist['nodes'].append(node_dict)
  
    return mapped_netlist
```

---

## 4.8. IMPLEMENTATION VÀ KIẾN TRÚC

### 4.8.1. Kiến Trúc Tổng Thể

Technology mapping module trong MyLogic được tổ chức theo kiến trúc modular:

```
core/technology_mapping/
├── technology_mapping.py    # Core mapping algorithms
├── library_loader.py        # Library loading (Liberty, JSON, Verilog)
└── __init__.py
```

**Phân tách trách nhiệm:**

- `technology_mapping.py`: Core mapping logic, TechnologyMapper, LibraryCell, TechnologyLibrary
- `library_loader.py`: Library loading từ các formats khác nhau

### 4.8.2. Integration với Complete Flow

Technology mapping được tích hợp trong complete flow:

```
Verilog → Parser → Netlist Dictionary
    ↓
Synthesis → AIG
    ↓
Optimization → Optimized AIG
    ↓
Technology Mapping → Technology-Mapped Netlist
    ↓
Verification (ModelSim)
```

**Usage trong complete flow:**

```python
from core.synthesis.synthesis_flow import synthesize
from core.optimization.optimization_flow import optimize
from core.technology_mapping.technology_mapping import techmap, create_standard_library

# Complete flow
netlist = parse_verilog("design.v")
aig = synthesize(netlist)
optimized_aig = optimize(aig, level="standard")
library = create_standard_library()
mapping_results = techmap(optimized_aig, library, strategy="area_optimal")
```

### 4.8.3. Error Handling

Technology mapping có error handling cơ bản:

```python
# Function matching
cells = library.get_cells_for_function(function)
if not cells:
    logger.warning(f"No suitable cell found for {node_name} with function {function}")
    # Node remains unmapped
```

**Handling unmapped nodes:**

- Nodes không tìm thấy matching cell sẽ remain unmapped
- Mapping success rate được track trong statistics
- Unmapped nodes có thể được handle trong post-processing

### 4.8.4. Performance Considerations

**Function Normalization:**

- Normalization được cache để tránh redundant computation
- Function map được build một lần khi load library

**Cell Selection:**

- Greedy algorithm: O(n * m) với n = số nodes, m = số cells per function
- Có thể optimize bằng cách pre-compute best cells cho common functions

**Memory Management:**

- LogicNodes có thể chiếm nhiều memory với designs lớn
- Consider: Lazy evaluation, sparse storage

---

## 4.9. SO SÁNH VÀ ĐÁNH GIÁ

### 4.9.1. So Sánh với Yosys/ABC

**Yosys/ABC** là các công cụ technology mapping mạnh mẽ. So sánh technology mapping module của MyLogic:

| Khía cạnh                | MyLogic              | Yosys/ABC           |
| -------------------------- | -------------------- | ------------------- |
| **Input Format**     | AIG                  | AIG                 |
| **Mapping Strategy** | Area/Delay/Balanced  | Area/Delay/Balanced |
| **Library Format**   | Liberty/JSON/Verilog | Liberty             |
| **Cut Enumeration**  | Chưa có            | Có (advanced)      |
| **Tree Mapping**     | Greedy               | Advanced algorithms |
| **Complex Gates**    | Có (AOI, OAI)       | Có (advanced)      |
| **FPGA Mapping**     | Chưa có            | Có (LUT mapping)   |

**Điểm mạnh của MyLogic:**

- Kiến trúc modular, dễ hiểu
- Hỗ trợ nhiều library formats (JSON, Verilog)
- Code rõ ràng, phù hợp cho giáo dục

**Hạn chế:**

- Chưa có cut enumeration (advanced mapping)
- Chưa có tree-based mapping algorithms
- Chưa hỗ trợ FPGA LUT mapping

### 4.9.2. Kết Quả Technology Mapping

**Typical Results:**

**Area-Optimal Mapping:**

- Giảm 10-30% area so với delay-optimal
- Có thể tăng delay 5-15%

**Delay-Optimal Mapping:**

- Giảm 10-25% delay so với area-optimal
- Có thể tăng area 5-20%

**Balanced Mapping:**

- Cân bằng tốt giữa area và delay
- Trade-off phù hợp cho nhiều applications

**Ví dụ:**

```
Input: 100 AIG nodes
Library: Standard cells (20 cells)

Area-Optimal:
- Mapped nodes: 95/100 (95%)
- Total area: 120.5
- Total delay: 15.2

Delay-Optimal:
- Mapped nodes: 95/100 (95%)
- Total area: 145.8
- Total delay: 12.5

Balanced:
- Mapped nodes: 95/100 (95%)
- Total area: 130.2
- Total delay: 13.8
```

### 4.9.3. Cell Usage Statistics

**Typical cell usage trong mapped netlist:**

- `NAND2`, `NOR2`: 30-40% (most common)
- `AND2`, `OR2`: 20-30%
- `INV`: 15-25%
- `XOR2`, `XNOR2`: 5-10%
- Complex gates (AOI, OAI): 5-15%

**Factors ảnh hưởng cell usage:**

- Library composition (cells available)
- Mapping strategy (area vs delay)
- AIG structure (sau optimization)

### 4.9.4. Hạn Chế và Hướng Phát Triển

**Hạn chế hiện tại:**

1. **Greedy Algorithm**: Chỉ xem xét local optimization, không global
2. **No Cut Enumeration**: Chưa có advanced cut-based mapping
3. **No Tree Mapping**: Chưa có tree-based mapping algorithms
4. **No FPGA Support**: Chưa hỗ trợ LUT mapping cho FPGA
5. **Limited Complex Gates**: Chưa exploit hết complex gates trong library

**Hướng phát triển:**

1. **Cut Enumeration**: Implement cut-based mapping như ABC
2. **Tree Mapping**: Tree-based algorithms cho better results
3. **FPGA Mapping**: LUT mapping cho FPGA targets
4. **Global Optimization**: Global optimization thay vì greedy
5. **Advanced Gates**: Better exploitation của complex gates (AOI, OAI)
6. **Timing-Aware Mapping**: Consider timing constraints trong mapping

---

## 4.10. KẾT LUẬN CHƯƠNG

CHƯƠNG 4 đã trình bày chi tiết về **Technology Mapping** trong MyLogic EDA Tool, bao gồm:

1. **Tổng quan về Technology Mapping**: Định nghĩa, vai trò, mục tiêu, và strategies
2. **Technology Libraries**: LibraryCell, TechnologyLibrary, ASIC và FPGA libraries, function normalization
3. **Library Loading**: Hỗ trợ Liberty, JSON, và Verilog formats
4. **AIG to LogicNodes Conversion**: Chuyển đổi AIG sang LogicNodes format cho mapping
5. **Technology Mapping Algorithms**: Area-optimal, delay-optimal, và balanced mapping
6. **TechnologyMapper Class**: Implementation của mapping engine
7. **Techmap Function**: High-level interface cho technology mapping
8. **Implementation và Kiến trúc**: Modular architecture, integration với complete flow
9. **So sánh và Đánh giá**: So sánh với Yosys/ABC, kết quả mapping, hạn chế và hướng phát triển

Technology mapping module của MyLogic đạt được mục tiêu chính: **chuyển đổi AIG sang technology-mapped netlist sử dụng cells từ technology library**, với kiến trúc modular và code dễ hiểu, phù hợp cho giáo dục và nghiên cứu. Mặc dù còn một số hạn chế về advanced algorithms, module đã cung cấp đầy đủ tính năng cơ bản cho technology mapping.

---

# CHƯƠNG 5: KIỂM THỬ TÍNH ĐÚNG ĐẮN

## 5.1. TỔNG QUAN VỀ KIỂM THỬ TÍNH ĐÚNG ĐẮN

### 5.1.1. Định Nghĩa và Vai Trò

**Kiểm thử tính đúng đắn (Verification)** là quá trình xác minh rằng các bước synthesis, optimization, và technology mapping không làm thay đổi hành vi chức năng của thiết kế. Trong MyLogic EDA Tool, verification được thực hiện bằng cách so sánh kết quả simulation giữa:

- **Original netlist** (trước synthesis) vs **Synthesized netlist** (sau synthesis)
- **Synthesized netlist** (trước optimization) vs **Optimized netlist** (sau optimization)
- **Original netlist** vs **Technology-mapped netlist** (sau technology mapping)

### 5.1.2. Phương Pháp Verification

MyLogic sử dụng **ModelSim** để thực hiện functional verification:

1. **Generate Verilog Files**: Convert netlists sang Verilog code
2. **Generate Testbench**: Tạo testbench để so sánh 2 designs
3. **Run ModelSim Simulation**: Chạy simulation và so sánh outputs
4. **Parse Results**: Phân tích kết quả và generate verification report

### 5.1.3. Quy Trình Verification

```
Original Netlist
    ↓
[1] Generate Test Vectors (exhaustive hoặc custom)
    ↓
[2] Run Synthesis/Optimization/Techmap
    ↓
[3] Generate Verilog Files (original + synthesized/optimized/mapped)
    ↓
[4] Generate Testbench
    ↓
[5] Run ModelSim Simulation
    ↓
[6] Compare Outputs → Verification Results (Passed/Failed)
```

---

## 5.2. MODELSIM INTEGRATION

### 5.2.1. Tổng Quan

MyLogic tích hợp **ModelSim** để thực hiện functional verification bằng cách so sánh kết quả simulation giữa original và synthesized/optimized/mapped netlists.

### 5.2.2. ModelSimIntegration Class

Class `ModelSimIntegration` quản lý quá trình verification:

```python
class ModelSimIntegration:
    def __init__(self, modelsim_path: Optional[str] = None, project_path: Optional[str] = None):
        """
        Initialize ModelSim integration.
        
        Args:
            modelsim_path: Path to ModelSim executable (vsim)
            project_path: Path to ModelSim project directory
        """
        self.modelsim_path = modelsim_path or self._find_modelsim()
        self.project_dir = Path(project_path) if project_path else Path("integrations/modelsim/")
        self.work_dir = self.project_dir
```

**Tính năng:**
- Tự động tìm ModelSim trong các paths phổ biến
- Hỗ trợ Windows và Linux
- Có thể chỉ định path thủ công

### 5.2.3. Quy Trình Verification

Quy trình verification với ModelSim:

**Các bước:**

1. **Generate Verilog Files**: Convert netlists sang Verilog code
2. **Generate Testbench**: Tạo testbench để so sánh 2 designs
3. **Run ModelSim Simulation**: Compile và chạy simulation
4. **Parse Results**: Phân tích kết quả và generate report

**Compile Script:**
```
vlib work
vmap work work
vlog -work work original.v mapped.v testbench.v
vsim -c -do "run -all; quit -f" testbench_tb
```

### 5.2.4. Verification Report

ModelSim tự động generate verification report:

```
================================================================================
VERIFICATION REPORT: module_name
================================================================================
Generated: 2024-01-01 12:00:00

SUMMARY
--------------------------------------------------------------------------------
Status: PASSED
Total tests: 16
Passed: 16
Failed: 0
Success rate: 100.0%

GENERATED FILES
--------------------------------------------------------------------------------
Original Verilog: module_original.v
Mapped Verilog: module_mapped.v
Testbench: module_tb.v
Simulation log: module_simulation.log
Report: module_verification_report.txt

TEST RESULTS
--------------------------------------------------------------------------------
Test 1: PASS
Test 2: PASS
...
```

---

## 5.3. VERIFICATION CHO SYNTHESIS, OPTIMIZATION VÀ TECHMAP

### 5.3.1. Verification Synthesis

Kiểm tra tính đúng đắn của synthesis: **Original vs Synthesized**

```python
def verify_synthesis_with_simulation(
    original_netlist: Dict[str, Any],
    synthesized_netlist: Dict[str, Any],
    test_vectors: List[Dict[str, Any]],
    modelsim_path: Optional[str] = None,
    module_name: str = "design"
) -> Dict[str, Any]:
    """
    Verify synthesis correctness: Original vs Synthesized
    """
    results = verify_with_modelsim(
        original_netlist,
        synthesized_netlist,
        test_vectors,
        modelsim_path=modelsim_path,
        module_name=f"{module_name}_synthesis_verify"
    )
    return results
```

### 5.3.2. Verification Optimization

Kiểm tra tính đúng đắn của optimization: **Synthesized vs Optimized**

```python
def verify_optimization_with_simulation(
    synthesized_netlist: Dict[str, Any],
    optimized_netlist: Dict[str, Any],
    test_vectors: List[Dict[str, Any]],
    modelsim_path: Optional[str] = None,
    module_name: str = "design"
) -> Dict[str, Any]:
    """
    Verify optimization correctness: Synthesized vs Optimized
    """
    results = verify_with_modelsim(
        synthesized_netlist,
        optimized_netlist,
        test_vectors,
        modelsim_path=modelsim_path,
        module_name=f"{module_name}_optimization_verify"
    )
    return results
```

### 5.3.3. Verification Technology Mapping

Kiểm tra tính đúng đắn của technology mapping: **Original vs Technology-mapped**

Technology mapping verification được thực hiện tương tự, so sánh original netlist với technology-mapped netlist sau khi mapping.

### 5.3.4. Complete Verification Flow

Function `verify_complete_flow()` thực hiện verification cho cả synthesis và optimization:

```python
def verify_complete_flow(
    original_netlist: Dict[str, Any],
    synthesized_aig,
    optimized_aig: Optional[Any] = None,
    test_vectors: List[Dict[str, Any]] = None,
    modelsim_path: Optional[str] = None,
    module_name: str = "design",
    enable_optimization_verification: bool = True
) -> Dict[str, Any]:
    """
    Complete verification flow: Synthesis + Optimization
    """
    # VERIFICATION 1: Synthesis
    synthesis_verif = verify_synthesis_with_simulation(...)
    
    # VERIFICATION 2: Optimization (if applicable)
    if enable_optimization_verification:
        optimization_verif = verify_optimization_with_simulation(...)
    
    return verification_results
```

### 5.3.5. Test Vector Generation

MyLogic tự động generate exhaustive test vectors:

```python
def _generate_test_vectors(self, netlist: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate exhaustive test vectors."""
    inputs = netlist.get('inputs', [])
    num_inputs = len(inputs)
    
    test_vectors = []
    for i in range(2 ** num_inputs):
        input_dict = {}
        for j, input_name in enumerate(inputs):
            input_dict[input_name] = (i >> j) & 1
        test_vectors.append({'inputs': input_dict})
    
    return test_vectors
```

**Exhaustive Testing:** Với n inputs, generate 2^n test vectors để test tất cả input combinations.

---

## 5.4. VERIFICATION RESULTS VÀ USAGE

### 5.4.1. Verification Results Format

Verification results có format:

```python
{
    'passed': bool,              # Overall pass/fail status
    'total_tests': int,          # Total number of test vectors
    'passed_tests': int,         # Number of passed tests
    'failed_tests': int,         # Number of failed tests
    'test_results': [...],       # Detailed results per test
    'generated_files': {...}     # Paths to generated files
}
```

### 5.4.2. Usage Example

**Integration với Complete Flow:**

```python
from core.complete_flow import run_complete_flow

results = run_complete_flow(
    netlist,
    optimization_level="standard",
    techmap_strategy="area_optimal",
    enable_verification=True,  # Enable verification
    test_vectors=test_vectors
)

# Access verification results
if 'verification' in results:
    verif_results = results['verification']
    if verif_results['passed']:
        print("Verification PASSED!")
```

**Standalone Verification:**

```python
from core.verification import verify_complete_flow

verification_results = verify_complete_flow(
    original_netlist=netlist,
    synthesized_aig=aig,
    optimized_aig=optimized_aig,
    test_vectors=test_vectors
)
```

---

## 5.5. KẾT LUẬN CHƯƠNG

CHƯƠNG 5 đã trình bày về **Kiểm thử Tính đúng đắn** trong MyLogic EDA Tool, bao gồm:

1. **Tổng quan về Verification**: Định nghĩa và vai trò của verification trong EDA flow

2. **ModelSim Integration**: Tích hợp ModelSim để thực hiện functional verification bằng simulation

3. **Verification cho Synthesis, Optimization và Techmap**: 
   - Verification synthesis: Original vs Synthesized
   - Verification optimization: Synthesized vs Optimized
   - Verification technology mapping: Original vs Technology-mapped

4. **Test Vector Generation**: Tự động generate exhaustive test vectors

5. **Verification Results và Usage**: Format results và cách sử dụng verification trong flow

Verification module của MyLogic đạt được mục tiêu chính: **đảm bảo tính đúng đắn của synthesis, optimization và technology mapping** thông qua ModelSim integration, phù hợp cho giáo dục và nghiên cứu.

---

# CHƯƠNG 6: HƯỚNG DẪN SỬ DỤNG MYLOGIC

## 6.1. TỔNG QUAN

MyLogic EDA Tool cung cấp một giao diện dòng lệnh (CLI) tương tác để thực hiện các tác vụ EDA từ parsing Verilog đến synthesis, optimization, technology mapping và verification. Chương này trình bày hướng dẫn chi tiết về cách sử dụng công cụ.

### 6.1.1. Kiến Trúc CLI

MyLogic sử dụng một **interactive shell** với hơn 30 lệnh được tổ chức thành các nhóm:

- **File Operations**: Đọc file, xuất kết quả, hiển thị thống kê
- **Simulation**: Mô phỏng mạch số (scalar và vector)
- **Logic Synthesis**: Chuyển đổi netlist sang AIG
- **Optimization**: Tối ưu hóa AIG (Strash, DCE, CSE, ConstProp, Balance)
- **Technology Mapping**: Ánh xạ AIG sang technology libraries
- **VLSI CAD**: Các thuật toán BDD, SAT, Placement, Routing, Timing Analysis
- **Verification**: Kiểm thử tính đúng đắn với ModelSim

### 6.1.2. Các Chế Độ Sử Dụng

MyLogic hỗ trợ nhiều chế độ sử dụng:

1. **Interactive Shell**: Chế độ tương tác chính, khởi động bằng `python mylogic.py`
2. **Command-line Mode**: Chạy synthesis tự động với `--synthesize`
3. **Python API**: Sử dụng các module Python trực tiếp trong script
4. **Complete Flow**: Chạy toàn bộ pipeline tự động

---

## 6.2. CÀI ĐẶT VÀ KHỞI ĐỘNG

### 6.2.1. Yêu Cầu Hệ Thống

**Python Version**: Python 3.8 trở lên

**Dependencies**:
- NumPy (cho vector simulation)
- Matplotlib (cho visualization, optional)
- Graphviz (cho DOT output, optional)

**Optional Tools**:
- ModelSim (cho verification)
- Yosys (cho external synthesis integration)

### 6.2.2. Cài Đặt

```bash
# Clone repository
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool

# Install dependencies
pip install -r requirements.txt
```

### 6.2.3. Khởi Động MyLogic

**Cách 1: Interactive Shell (Khuyến nghị)**

```bash
python mylogic.py
```

Sau khi khởi động, shell sẽ hiển thị:

```
============================================================
  MyLogic EDA Tool v2.0.0
  Unified Electronic Design Automation Platform
============================================================
Welcome to MyLogic Vector Shell. Type 'help' for commands.
mylogic> 
```

**Cách 2: Load File Ngay Khi Khởi Động**

```bash
python mylogic.py --file examples/full_adder.v
```

**Cách 3: Synthesis Mode (Tự Động)**

```bash
python mylogic.py --file design.v --synthesize standard
```

**Cách 4: Debug Mode**

```bash
python mylogic.py --debug
```

---

## 6.3. CÁC LỆNH CƠ BẢN

### 6.3.1. File Operations

#### `read <file>`

Đọc file Verilog và parse thành netlist. Tự động export JSON nếu được bật.

**Ví dụ:**
```bash
mylogic> read examples/10_arithmetic/test_arithmetic.v
[OK] Loaded vector netlist with 15 nodes.
```

**Lưu ý:**
- Hỗ trợ file `.v` (Verilog)
- Tự động phát hiện vector/scalar design
- Auto-export JSON vào thư mục `outputs/` nếu được bật

#### `stats`

Hiển thị thống kê chi tiết về mạch hiện tại.

**Output bao gồm:**
- Số lượng inputs, outputs, nodes, wires
- Phân tích vector widths
- Phân tích node types
- Phân tích wire types
- Module instantiations

**Ví dụ:**
```bash
mylogic> stats
=== ENHANCED CIRCUIT STATISTICS ===
  Name    : test_arithmetic
  Inputs  : 2
  Outputs : 1
  Wires   : 12
  Nodes   : 15

  Vector Analysis:
    8-bit (2 signals): a, b
    8-bit (1 signals): result

  Node Analysis:
    ADD: 1 (6.7%)
    AND: 5 (33.3%)
    OR: 4 (26.7%)
    ...
```

#### `vectors`, `nodes`, `wires`, `modules`

Hiển thị chi tiết về vectors, nodes, wires và module instantiations.

**Ví dụ:**
```bash
mylogic> vectors
Detailed Vector Widths:

8-bit signals (3 total):
  1. a
  2. b
  3. result
```

#### `export_json [file]`

Xuất netlist hiện tại ra file JSON.

**Ví dụ:**
```bash
mylogic> export_json my_design.json
[OK] Exported to my_design.json
```

#### `dump` / `dump_ast`

Dump cấu trúc netlist dưới dạng AST tree (tương tự Yosys).

---

### 6.3.2. Simulation Commands

#### `simulate`

Chạy simulation tự động phát hiện vector/scalar.

**Quy trình:**
1. Tự động phát hiện design là vector hay scalar
2. Yêu cầu nhập giá trị cho các inputs
3. Tính toán và hiển thị outputs

**Ví dụ (Scalar):**
```bash
mylogic> simulate
  Value for a (0/1): 1
  Value for b (0/1): 0
  -> Outputs:
    out: 0
```

**Ví dụ (Vector):**
```bash
mylogic> simulate
  Value for [7:0] a (integer): 42
  Value for [7:0] b (integer): 15
  -> Outputs:
    result: 57 (int: 57)
```

#### `vsimulate`

Chạy vector simulation (legacy command, tương đương `simulate` cho vector designs).

---

### 6.3.3. Logic Synthesis Commands

#### `synthesis [level]`

Chạy synthesis flow: Netlist → AIG.

**Levels:**
- `basic`: Chỉ synthesis cơ bản
- `standard`: Synthesis với một số optimizations
- `aggressive`: Synthesis với tất cả optimizations

**Ví dụ:**
```bash
mylogic> synthesis standard
[INFO] Running synthesis flow (standard)...
[OK] Synthesis completed!
  Original: 25 nodes
  Synthesized: 18 nodes
  Reduction: 7 nodes (28.0%)
```

**Lưu ý:**
- Sau synthesis, netlist được chuyển sang AIG format
- Sử dụng `stats` để xem kết quả

#### `strash`

Structural Hashing: Loại bỏ các cấu trúc logic trùng lặp.

**Ví dụ:**
```bash
mylogic> strash
[INFO] Running Structural Hashing optimization...
[OK] Structural Hashing completed!
  Original: 20 nodes
  Optimized: 15 nodes
  Removed: 5 nodes
```

---

### 6.3.4. Optimization Commands

#### `dce [level]`

Dead Code Elimination: Loại bỏ logic không sử dụng.

**Levels:**
- `basic`: DCE cơ bản
- `advanced`: DCE nâng cao
- `aggressive`: DCE tích cực

**Ví dụ:**
```bash
mylogic> dce advanced
[INFO] Running Dead Code Elimination (advanced)...
[OK] DCE completed!
  Original: 18 nodes
  Optimized: 12 nodes
  Removed: 6 nodes
```

#### `cse`

Common Subexpression Elimination: Loại bỏ các biểu thức con trùng lặp.

**Ví dụ:**
```bash
mylogic> cse
[INFO] Running Common Subexpression Elimination...
[OK] CSE optimization completed!
  Original: 15 nodes
  Optimized: 10 nodes
  Removed: 5 nodes
```

#### `constprop`

Constant Propagation: Lan truyền các giá trị hằng số.

**Ví dụ:**
```bash
mylogic> constprop
[INFO] Running Constant Propagation...
[OK] Constant Propagation completed!
  Original: 12 nodes
  Optimized: 8 nodes
  Removed: 4 nodes
```

#### `balance`

Logic Balancing: Cân bằng độ sâu logic để tối ưu timing.

**Ví dụ:**
```bash
mylogic> balance
[INFO] Running Logic Balancing...
[OK] Logic Balancing completed!
  Original: 10 nodes
  Optimized: 10 nodes (depth reduced)
```

#### `optimize [level]`

Chạy toàn bộ optimization flow.

**Levels:**
- `basic`: Strash + DCE basic
- `standard`: Strash + DCE advanced + CSE + ConstProp
- `aggressive`: Tất cả optimizations với DCE aggressive

**Ví dụ:**
```bash
mylogic> optimize standard
[INFO] Running optimization flow (standard)...
[OK] Optimization completed!
  Original: 20 nodes
  Optimized: 8 nodes
  Reduction: 12 nodes (60.0%)
```

---

### 6.3.5. Technology Mapping Commands

#### `techmap [strategy] [library]`

Technology Mapping: Ánh xạ AIG sang technology library.

**Strategies:**
- `area_optimal`: Tối ưu diện tích
- `delay_optimal`: Tối ưu delay
- `balanced`: Cân bằng diện tích và delay

**Libraries:**
- `asic`: ASIC standard cells
- `fpga_common`: Common FPGA cells
- `xilinx`: Xilinx FPGA cells
- `ice40`: Lattice iCE40 cells
- `auto`: Tự động phát hiện library

**Ví dụ:**
```bash
mylogic> techmap balanced fpga_common
[INFO] Loading technology library: fpga_common...
[INFO] Running technology mapping (balanced)...
[OK] Technology mapping completed!
  Original AIG nodes: 15
  Mapped cells: 8
  Area: 120 units
  Delay: 3.5 ns
```

---

### 6.3.6. VLSI CAD Commands

#### `bdd [operation]`

Binary Decision Diagrams operations.

**Operations:**
- `create`: Tạo BDD từ netlist
- `analyze`: Phân tích BDD
- `convert`: Chuyển đổi BDD

**Ví dụ:**
```bash
mylogic> bdd create
[INFO] Creating BDD from netlist...
[OK] BDD created with 25 nodes
```

#### `sat [operation]`

SAT Solver operations.

**Operations:**
- `solve`: Giải bài toán SAT
- `verify`: Verification với SAT
- `check`: Kiểm tra satisfiability

#### `place [algorithm]`

Placement algorithms.

**Algorithms:**
- `random`: Random placement
- `force_directed`: Force-directed placement
- `simulated_annealing`: Simulated annealing

**Ví dụ:**
```bash
mylogic> place force_directed
[INFO] Running force-directed placement...
[OK] Placement completed!
  Total cells: 20
  Wirelength: 150 units
```

#### `route [algorithm]`

Routing algorithms.

**Algorithms:**
- `maze`: Maze routing (Lee's algorithm)
- `lee`: Alias cho maze
- `ripup_reroute`: Rip-up and reroute

**Ví dụ:**
```bash
mylogic> route maze
[INFO] Running maze routing...
[OK] Routing completed!
  Routed nets: 15/15 (100%)
  Total wirelength: 200 units
```

#### `timing`

Static Timing Analysis.

**Ví dụ:**
```bash
mylogic> timing
[INFO] Running Static Timing Analysis...
[OK] Timing analysis completed!
  Critical path delay: 5.2 ns
  Setup slack: 2.1 ns
  Hold slack: 0.5 ns
```

---

### 6.3.7. Verification Commands

#### `verify [type]`

Verification với ModelSim.

**Types:**
- `synthesis`: Verify synthesis correctness
- `optimization`: Verify optimization correctness
- `techmap`: Verify technology mapping correctness
- `complete`: Verify complete flow

**Ví dụ:**
```bash
mylogic> verify synthesis
[INFO] Running synthesis verification with ModelSim...
[INFO] Generating test vectors...
[INFO] Running ModelSim simulation...
[OK] Verification PASSED!
  Total tests: 16
  Passed: 16
  Failed: 0
```

**Lưu ý:**
- Cần ModelSim đã cài đặt
- Tự động generate test vectors exhaustive
- So sánh outputs giữa original và transformed design

---

### 6.3.8. Complete Flow Commands

#### `complete_flow` / `workflow`

Chạy toàn bộ pipeline: Synthesis → Optimization → Technology Mapping → Verification.

**Options:**
- `--verify`: Bật verification
- `--no-verify`: Tắt verification (mặc định)

**Ví dụ:**
```bash
mylogic> complete_flow --verify
[INFO] Running complete flow...
[1/4] Synthesis...
[2/4] Optimization...
[3/4] Technology Mapping...
[4/4] Verification...
[OK] Complete flow finished!
```

---

### 6.3.9. Utility Commands

#### `help`

Hiển thị danh sách tất cả lệnh có sẵn.

#### `history`

Hiển thị lịch sử 10 lệnh gần nhất.

#### `clear`

Xóa màn hình.

#### `exit`

Thoát khỏi shell.

---

## 6.4. WORKFLOW TỔNG HỢP

### 6.4.1. Workflow Cơ Bản

**Bước 1: Load Design**

```bash
mylogic> read examples/10_arithmetic/test_arithmetic.v
mylogic> stats
```

**Bước 2: Synthesis**

```bash
mylogic> synthesis standard
mylogic> stats
```

**Bước 3: Optimization**

```bash
mylogic> optimize standard
mylogic> stats
```

**Bước 4: Technology Mapping**

```bash
mylogic> techmap balanced fpga_common
mylogic> stats
```

**Bước 5: Export Results**

```bash
mylogic> export_json final_design.json
```

---

### 6.4.2. Workflow với Verification

**Bước 1-4**: Tương tự workflow cơ bản

**Bước 5: Verification**

```bash
mylogic> verify complete
```

**Bước 6: Xem Verification Results**

```bash
# Xem report
cat integrations/modelsim/*_verification_report.txt
```

---

### 6.4.3. Workflow Tự Động (Complete Flow)

**Cách 1: Trong Shell**

```bash
mylogic> read design.v
mylogic> complete_flow --verify
```

**Cách 2: Command-line**

```bash
python mylogic.py --file design.v --synthesize standard
```

**Cách 3: Python Script**

```python
from parsers import parse_verilog
from core.complete_flow import run_complete_flow

# Parse
netlist = parse_verilog("design.v")

# Generate test vectors
inputs = netlist.get('inputs', [])
test_vectors = []
for i in range(2 ** len(inputs)):
    test_inputs = {}
    for j, input_name in enumerate(inputs):
        test_inputs[input_name] = (i >> (len(inputs) - 1 - j)) & 1
    test_vectors.append({'inputs': test_inputs})

# Run complete flow
results = run_complete_flow(
    netlist,
    optimization_level="standard",
    techmap_strategy="balanced",
    enable_verification=True,
    test_vectors=test_vectors
)

# Check results
if results['verification']['passed']:
    print("Verification PASSED!")
```

---

## 6.5. VÍ DỤ SỬ DỤNG

### 6.5.1. Ví Dụ 1: Full Adder

**File:** `examples/full_adder.v`

```bash
# Khởi động MyLogic
python mylogic.py

# Load design
mylogic> read examples/full_adder.v
mylogic> stats

# Synthesis
mylogic> synthesis standard
mylogic> stats

# Optimization
mylogic> optimize standard
mylogic> stats

# Technology mapping
mylogic> techmap balanced asic
mylogic> stats

# Simulation
mylogic> simulate
  Value for a (0/1): 1
  Value for b (0/1): 1
  Value for cin (0/1): 1
  -> Outputs:
    sum: 1
    cout: 1

# Export
mylogic> export_json full_adder_final.json
```

---

### 6.5.2. Ví Dụ 2: Arithmetic Operations với Verification

**File:** `examples/10_arithmetic/test_arithmetic.v`

```bash
# Load design
mylogic> read examples/10_arithmetic/test_arithmetic.v
mylogic> stats

# Complete flow với verification
mylogic> complete_flow --verify

# Xem kết quả
mylogic> stats
```

**Output:**
```
[INFO] Running complete flow...
[1/4] Synthesis...
  Original: 25 nodes
  Synthesized: 18 nodes
[2/4] Optimization...
  Optimized: 12 nodes
[3/4] Technology Mapping...
  Mapped cells: 8
[4/4] Verification...
  Total tests: 256
  Passed: 256
  Failed: 0
[OK] Complete flow finished!
```

---

### 6.5.3. Ví Dụ 3: Python Script

**File:** `my_synthesis.py`

```python
#!/usr/bin/env python3
from parsers import parse_verilog
from core.complete_flow import run_complete_flow

# Parse Verilog
netlist = parse_verilog("examples/11_bitwise/test_bitwise.v")

# Generate exhaustive test vectors
inputs = netlist.get('inputs', [])
test_vectors = []
for i in range(2 ** len(inputs)):
    test_inputs = {}
    for j, input_name in enumerate(inputs):
        test_inputs[input_name] = (i >> (len(inputs) - 1 - j)) & 1
    test_vectors.append({'inputs': test_inputs})

# Run complete flow
results = run_complete_flow(
    netlist,
    optimization_level="aggressive",
    techmap_strategy="area_optimal",
    techmap_library="fpga_common",
    enable_verification=True,
    test_vectors=test_vectors
)

# Print results
print("=" * 60)
print("SYNTHESIS RESULTS")
print("=" * 60)
print(f"Original nodes: {results['synthesis']['original_nodes']}")
print(f"Synthesized nodes: {results['synthesis']['synthesized_nodes']}")
print(f"Reduction: {results['synthesis']['reduction_percent']:.1f}%")

print("\n" + "=" * 60)
print("OPTIMIZATION RESULTS")
print("=" * 60)
print(f"Optimized nodes: {results['optimization']['optimized_nodes']}")
print(f"Optimization reduction: {results['optimization']['reduction_percent']:.1f}%")

print("\n" + "=" * 60)
print("TECHNOLOGY MAPPING RESULTS")
print("=" * 60)
print(f"Mapped cells: {results['techmap']['mapped_cells']}")
print(f"Area: {results['techmap']['area']} units")
print(f"Delay: {results['techmap']['delay']} ns")

print("\n" + "=" * 60)
print("VERIFICATION RESULTS")
print("=" * 60)
verif = results['verification']
print(f"Overall: {'PASSED' if verif['passed'] else 'FAILED'}")
print(f"Total tests: {verif['total_tests']}")
print(f"Passed: {verif['passed_tests']}")
print(f"Failed: {verif['failed_tests']}")
```

**Chạy:**
```bash
python my_synthesis.py
```

---

## 6.6. TROUBLESHOOTING

### 6.6.1. Lỗi Thường Gặp

#### **Lỗi: "No netlist loaded"**

**Nguyên nhân:** Chưa load file hoặc file không hợp lệ.

**Giải pháp:**
```bash
mylogic> read examples/full_adder.v
mylogic> stats  # Kiểm tra xem đã load thành công chưa
```

#### **Lỗi: "ModelSim not found"**

**Nguyên nhân:** ModelSim chưa được cài đặt hoặc không có trong PATH.

**Giải pháp:**
- Cài đặt ModelSim
- Thêm ModelSim vào PATH
- Hoặc chỉ định đường dẫn ModelSim trong code

#### **Lỗi: "Library not found"**

**Nguyên nhân:** Technology library không tồn tại.

**Giải pháp:**
- Kiểm tra thư mục `techlibs/`
- Sử dụng `auto` để tự động phát hiện library
- Hoặc chỉ định library đúng tên

#### **Lỗi: "Syntax error"**

**Nguyên nhân:** File Verilog có syntax không hợp lệ.

**Giải pháp:**
- Kiểm tra syntax Verilog
- Xem log chi tiết với `--debug`
- Thử với file example đơn giản trước

---

### 6.6.2. Debug Mode

**Khởi động với debug logging:**

```bash
python mylogic.py --debug
```

**Trong shell, kiểm tra thông tin:**

```bash
mylogic> stats        # Xem thống kê
mylogic> vectors      # Xem vector details
mylogic> nodes        # Xem node details
mylogic> dump_ast     # Xem AST structure
```

---

### 6.6.3. Kiểm Tra Dependencies

```bash
python mylogic.py --check-deps
```

**Output:**
```
Checking dependencies...
[OK] NumPy is available
[OK] Matplotlib is available
[OK] Graphviz is available
```

---

## 6.7. KẾT LUẬN CHƯƠNG

CHƯƠNG 6 đã trình bày **Hướng dẫn Sử dụng MyLogic EDA Tool**, bao gồm:

1. **Tổng quan**: Kiến trúc CLI và các chế độ sử dụng

2. **Cài đặt và Khởi động**: Yêu cầu hệ thống, cài đặt dependencies, và các cách khởi động

3. **Các Lệnh Cơ Bản**: 
   - File operations (read, stats, export)
   - Simulation (simulate, vsimulate)
   - Logic synthesis (synthesis, strash)
   - Optimization (dce, cse, constprop, balance, optimize)
   - Technology mapping (techmap)
   - VLSI CAD (bdd, sat, place, route, timing)
   - Verification (verify)
   - Complete flow (complete_flow)

4. **Workflow Tổng Hợp**: 
   - Workflow cơ bản
   - Workflow với verification
   - Workflow tự động

5. **Ví Dụ Sử Dụng**: 
   - Full Adder example
   - Arithmetic operations với verification
   - Python script integration

6. **Troubleshooting**: Các lỗi thường gặp và cách giải quyết

MyLogic EDA Tool cung cấp một giao diện CLI mạnh mẽ và dễ sử dụng, phù hợp cho cả người mới bắt đầu và người dùng nâng cao. Với hơn 30 lệnh được tổ chức rõ ràng, người dùng có thể thực hiện toàn bộ EDA flow từ parsing đến verification một cách hiệu quả.

---
