# 🏗️ **VLSI CAD MODULE**

## 📋 **MÔ TẢ**
Thư mục chứa các thuật toán VLSI CAD cho MyLogic EDA Tool.

## 📁 **FILES**

### **1. `bdd.py` - Binary Decision Diagrams**
- **Chức năng**: Efficient Boolean function representation (ROBDD-inspired)
- **Thuật toán**: Unique table, cached operations, recursive apply
- **Ứng dụng**: Verification, support set, Verilog export (đơn giản)

### **2. `sat_solver.py` - SAT Solver**
- **Chức năng**: Boolean satisfiability checking (DPLL core)
- **Thuật toán**: Unit propagation, decisions, backtracking (CDCL-stub)
- **Ứng dụng**: Formal verification, equivalence/property checking

### **3. `placement.py` - Placement Algorithms**
- **Chức năng**: Đặt vị trí cells (random, force-directed, simulated annealing)
- **Thuật toán**: HPWL metric, lực hút theo tâm mạng, SA với nhiệt độ giảm dần
- **Ứng dụng**: Physical design, minimize wirelength / improve utilization

### **4. `routing.py` - Routing Algorithms**
- **Chức năng**: Kết nối nets trên lưới nhiều lớp (maze/Lee, rip-up & reroute)
- **Thuật toán**: Wave propagation (Lee - simplified), lộ trình tham lam, via layers
- **Ứng dụng**: Physical design, báo cáo wirelength và congestion

### **5. `timing_analysis.py` - Static Timing Analysis**
- **Chức năng**: Phân tích timing tĩnh (AT, RAT, Slack, đường critical)
- **Thuật toán**: Lan truyền tiến/lùi trên đồ thị timing, tổng hợp báo cáo
- **Ứng dụng**: Timing closure, phát hiện vi phạm setup/hold (simple)

## 🎯 **VLSI CAD ALGORITHMS**

### **Binary Decision Diagrams (API gist):**
```python
class BDD:
    def create_variable(name) -> BDDNode
    def create_constant(value: bool) -> BDDNode
    def apply_operation(op: str, left: BDDNode, right: BDDNode) -> BDDNode  # AND/OR/XOR/...
    def evaluate(node: BDDNode, assignment: Dict[str, bool]) -> bool
    def get_support(node: BDDNode) -> Set[str]
    def count_nodes(node: BDDNode) -> int
    def to_verilog(node: BDDNode, output_name: str = "out") -> str
```

### **SAT Solving (API gist):**
```python
class SATSolver:
    def add_clause(lits: List[int]) -> None  # literals: +v / -v
    def add_clauses_from_formula(formula: List[List[int]]) -> None
    def solve() -> Tuple[bool, Optional[Dict[int, bool]]]
    def get_statistics() -> Dict[str, int]

class SATBasedVerifier:
    def verify_equivalence(c1: Dict, c2: Dict]) -> Tuple[bool, Optional[Dict]]
    def verify_property(circ: Dict, prop_expr: str) -> Tuple[bool, Optional[Dict]]
```

### **Placement (API gist):**
```python
class PlacementEngine:
    def add_cell(cell: Cell) -> None
    def add_net(net: Net) -> None
    def random_placement() -> Dict[str, Cell]
    def force_directed_placement(iterations: int = 100) -> Dict[str, Cell]
    def simulated_annealing_placement(T0=1000.0, cooling_rate=0.95, max_iter=10000) -> Dict[str, Cell]
    def get_placement_statistics() -> Dict[str, Any]
```

### **Routing (API gist):**
```python
class RoutingGrid:
    def is_free(p: Point, layer: int = 0) -> bool
    def occupy(p: Point, layer: int = 0) -> None
    def get_neighbors(p: Point, layer: int = 0) -> List[Tuple[Point,int]]

class MazeRouter:
    def add_net(net: Net) -> None
    def route_all_nets(strategy: str = "maze") -> Dict[str, bool]
    def get_routing_statistics() -> Dict[str, Any]
    def visualize_routing() -> None
```

### **Timing Analysis (API gist):**
```python
class StaticTimingAnalyzer:
    def add_node(node: TimingNode) -> None
    def add_arc(arc: TimingArc) -> None
    def set_clock_period(period: float) -> None
    def perform_timing_analysis() -> Dict[str, Any]
    def print_timing_report(report: Dict[str, Any]) -> None
```

## 🚀 **USAGE**

```python
from core.vlsi_cad.bdd import BDD
from core.vlsi_cad.sat_solver import SATSolver
from core.vlsi_cad.placement import Placement
from core.vlsi_cad.routing import Routing
from core.vlsi_cad.timing_analysis import TimingAnalysis

# BDD analysis
bdd = BDD()
result = bdd.analyze(boolean_function)

# SAT solving
solver = SATSolver()
satisfiable = solver.solve(formula)

# Placement
placer = Placement()
placement = placer.place(netlist)

# Routing
router = Routing()
routing = router.route(placement, netlist)

# Timing analysis
timing = TimingAnalysis()
analysis = timing.analyze(netlist, constraints)
```

## 📊 **VLSI CAD METRICS**

- **Area**: Chip area utilization
- **Delay**: Critical path delays
- **Power**: Dynamic and static power
- **Timing**: Setup/hold violations
- **Congestion**: Routing congestion

## 🎯 **DESIGN FLOW**

### **1. Logic Design:**
- RTL description
- Logic synthesis
- Technology mapping

### **2. Physical Design:**
- Floorplanning
- Placement
- Routing

### **3. Verification:**
- Timing analysis
- Power analysis
- Design rule checking

## 📚 **REFERENCES**
- VLSI design textbooks
- EDA tool documentation
- Academic papers on VLSI CAD

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
