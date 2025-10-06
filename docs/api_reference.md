# API REFERENCE - MYLOGIC EDA TOOL

## 📚 Tổng quan

Tài liệu API reference cho MyLogic EDA Tool, bao gồm tất cả các modules, classes và functions chính.

## 🏗️ Core Modules

### **Arithmetic Simulation (`core.arithmetic_simulation`)**

#### **VectorValue Class**
```python
class VectorValue:
    def __init__(self, value: int, width: int)
    def to_int(self) -> int
    def to_binary(self) -> str
```

#### **Vector Operations**
```python
def vector_add(a: VectorValue, b: VectorValue) -> VectorValue
def vector_multiply(a: VectorValue, b: VectorValue) -> VectorValue
def vector_and(a: VectorValue, b: VectorValue) -> VectorValue
def vector_or(a: VectorValue, b: VectorValue) -> VectorValue
def vector_xor(a: VectorValue, b: VectorValue) -> VectorValue
def vector_not(a: VectorValue) -> VectorValue
```

### **Logic Synthesis (`core.synthesis_flow`)**

#### **SynthesisFlow Class**
```python
class SynthesisFlow:
    def __init__(self, netlist: Dict[str, Any])
    def run_strash(self) -> Dict[str, Any]
    def run_dce(self, level: str = "basic") -> Dict[str, Any]
    def run_cse(self) -> Dict[str, Any]
    def run_constprop(self) -> Dict[str, Any]
    def run_balance(self) -> Dict[str, Any]
    def run_complete_flow(self) -> Dict[str, Any]
```

### **VLSI CAD Part 1**

#### **BDD (`core.bdd`)**
```python
class BDDNode:
    def __init__(self, var_id: int, low: 'BDDNode', high: 'BDDNode', value: bool = None)
    def is_terminal(self) -> bool

class BDD:
    def __init__(self)
    def create_constant(self, value: bool) -> BDDNode
    def create_variable(self, var_name: str) -> BDDNode
    def apply_operation(self, left: BDDNode, right: BDDNode, op_func: callable) -> BDDNode
```

#### **SAT Solver (`core.sat_solver`)**
```python
class SATSolver:
    def __init__(self)
    def add_clause(self, clause: List[int])
    def solve(self) -> Tuple[bool, Dict[int, bool]]
    def is_satisfiable(self) -> bool
```

### **VLSI CAD Part 2**

#### **Placement (`core.placement`)**
```python
class PlacementEngine:
    def __init__(self, cells: Dict, nets: Dict)
    def random_placement(self) -> Dict[str, Tuple[float, float]]
    def force_directed_placement(self) -> Dict[str, Tuple[float, float]]
    def simulated_annealing_placement(self) -> Dict[str, Tuple[float, float]]
```

#### **Routing (`core.routing`)**
```python
class RoutingEngine:
    def __init__(self, nets: Dict, grid_size: Tuple[int, int])
    def maze_routing(self) -> Dict[str, List[Tuple[int, int]]]
    def lee_algorithm(self) -> Dict[str, List[Tuple[int, int]]]
    def ripup_reroute(self) -> Dict[str, List[Tuple[int, int]]]
```

## 🔧 Frontend Modules

### **Verilog Parser (`frontends.simple_arithmetic_verilog`)**

```python
def parse_arithmetic_verilog_simple(path: str) -> Dict[str, Any]
```

**Returns:**
- `netlist`: Dictionary containing parsed circuit information
- `nodes`: Dictionary of circuit nodes
- `connections`: List of connections between nodes

## 🎮 CLI Interface

### **Vector Shell (`cli.vector_shell`)**

#### **VectorShell Class**
```python
class VectorShell:
    def __init__(self, config: Optional[Dict[str, Any]] = None)
    def run(self) -> None
    def _read_file(self, args: List[str]) -> None
    def _simulate(self, args: List[str]) -> None
    def _show_stats(self, args: List[str]) -> None
```

#### **Available Commands**
- `read <file>` - Load Verilog file
- `simulate` - Run simulation
- `stats` - Show circuit statistics
- `strash` - Structural hashing
- `dce <level>` - Dead code elimination
- `cse` - Common subexpression elimination
- `constprop` - Constant propagation
- `balance` - Logic balancing
- `place <algorithm>` - Placement algorithms
- `route <algorithm>` - Routing algorithms
- `timing` - Static timing analysis
- `techmap <strategy>` - Technology mapping
- `yosys_flow` - Yosys synthesis flow
- `write_verilog <file>` - Write Verilog output
- `write_json <file>` - Write JSON output
- `write_dot <file>` - Write DOT graph output

## 🔗 Yosys Integration

### **Yosys Commands (`synthesis.yosys_commands`)**

```python
def run_yosys_synthesis(input_file: str, output_file: str, optimization_level: str) -> bool
def run_yosys_optimization(input_file: str, pass_name: str, output_file: str) -> bool
def get_yosys_statistics(input_file: str) -> Dict[str, Any]
```

### **Yosys Integration (`synthesis.yosys_integration`)**

```python
def integrate_yosys_commands() -> Dict[str, callable]
```

## 📊 Data Structures

### **Netlist Format**
```python
netlist = {
    'nodes': {
        'node_id': {
            'type': 'gate_type',
            'inputs': ['input1', 'input2'],
            'outputs': ['output1'],
            'width': 4
        }
    },
    'connections': [
        {'from': 'node1', 'to': 'node2', 'signal': 'wire_name'}
    ],
    'inputs': ['input1', 'input2'],
    'outputs': ['output1', 'output2']
}
```

## 🎯 Usage Examples

### **Basic Usage**
```python
from frontends.simple_arithmetic_verilog import parse_arithmetic_verilog_simple
from core.arithmetic_simulation import simulate_arithmetic_netlist

# Parse Verilog file
netlist = parse_arithmetic_verilog_simple("examples/arithmetic_operations.v")

# Run simulation
result = simulate_arithmetic_netlist(netlist, inputs={'a': 5, 'b': 3})
```

### **Logic Synthesis**
```python
from core.synthesis_flow import SynthesisFlow

# Create synthesis flow
synthesis = SynthesisFlow(netlist)

# Run complete synthesis
optimized_netlist = synthesis.run_complete_flow()
```

### **VLSI CAD Features**
```python
from core.placement import PlacementEngine
from core.routing import RoutingEngine

# Placement
placement = PlacementEngine(cells, nets)
positions = placement.force_directed_placement()

# Routing
routing = RoutingEngine(nets, grid_size)
routes = routing.maze_routing()
```
