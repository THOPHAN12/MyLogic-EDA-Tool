# 🧮 NỀN TẢNG LÝ THUYẾT CHO LOGIC SYNTHESIS

## 📖 Tổng quan

Tài liệu này cung cấp nền tảng lý thuyết cần thiết để hiểu và implement các thuật toán logic synthesis trong MyLogic EDA Tool.

## 🏗️ Cấu trúc dữ liệu cơ bản

### 📊 Netlist Representation

#### 🎯 Định nghĩa Netlist

**Netlist** là biểu diễn của mạch logic dưới dạng graph, bao gồm:
- **Nodes**: Các logic gates, inputs, outputs
- **Connections**: Các kết nối giữa nodes
- **Attributes**: Thông tin bổ sung (timing, power, etc.)

#### 🔧 Cấu trúc Netlist trong MyLogic

```python
netlist = {
    'name': 'circuit_name',           # Tên mạch
    'inputs': ['a', 'b', 'c'],       # Danh sách input ports
    'outputs': ['out1', 'out2'],     # Danh sách output ports
    'nodes': {                       # Dictionary các nodes
        'n1': {                      # Node ID
            'type': 'AND',           # Loại gate (AND, OR, XOR, etc.)
            'fanins': [              # Danh sách inputs
                ['a', False],        # [signal_name, polarity]
                ['b', False]
            ],
            'output': 'temp1',       # Output signal name
            'delay': 0.1,            # Gate delay (optional)
            'area': 2.0              # Gate area (optional)
        }
    },
    'attrs': {                       # Attributes
        'vector_widths': {           # Vector signal widths
            'a': 4,                  # 4-bit signal
            'b': 4,
            'out1': 4
        }
    }
}
```

#### 📋 Node Types

```python
GATE_TYPES = {
    # Basic gates
    'AND': 'AND gate',
    'OR': 'OR gate', 
    'XOR': 'XOR gate',
    'NAND': 'NAND gate',
    'NOR': 'NOR gate',
    'XNOR': 'XNOR gate',
    'NOT': 'NOT gate (inverter)',
    'BUF': 'Buffer gate',
    
    # Complex gates
    'AOI21': 'AND-OR-Invert (2-1)',
    'OAI21': 'OR-AND-Invert (2-1)',
    'AOI22': 'AND-OR-Invert (2-2)',
    'OAI22': 'OR-AND-Invert (2-2)',
    
    # Sequential elements
    'DFF': 'D Flip-Flop',
    'DFFE': 'D Flip-Flop with Enable',
    'LATCH': 'Latch'
}
```

#### 🔗 Connection Format

```python
# Fanin format: [signal_name, polarity]
fanin = ['signal_name', polarity]

# Polarity:
# False = positive (no inversion)
# True = negative (inverted)

# Examples:
['a', False]    # a (positive)
['a', True]     # !a (negative/inverted)
```

### 🌐 Graph Theory trong Logic Synthesis

#### 📊 Directed Acyclic Graph (DAG)

Logic circuits được biểu diễn dưới dạng **Directed Acyclic Graph (DAG)**:

```python
# DAG Properties:
# 1. Directed: Edges có direction (from input to output)
# 2. Acyclic: Không có cycles (no feedback)
# 3. Graph: Collection of vertices (nodes) và edges (connections)

class LogicDAG:
    def __init__(self):
        self.nodes = {}      # vertices
        self.edges = {}      # connections
        self.inputs = []     # source nodes
        self.outputs = []    # sink nodes
```

#### 🎯 Graph Traversal Algorithms

##### 1. **Topological Ordering**
```python
def topological_sort(nodes: Dict[str, Any]) -> List[str]:
    """
    Sắp xếp nodes theo topological order.
    Input nodes được xử lý trước output nodes.
    """
    visited = set()
    temp_visited = set()
    result = []
    
    def dfs(node_id: str):
        if node_id in temp_visited:
            raise ValueError("Cycle detected!")
        if node_id in visited:
            return
            
        temp_visited.add(node_id)
        
        # Process fanins first
        node = nodes.get(node_id, {})
        fanins = node.get('fanins', [])
        for fanin in fanins:
            if isinstance(fanin, list) and len(fanin) >= 1:
                dfs(fanin[0])
        
        temp_visited.remove(node_id)
        visited.add(node_id)
        result.append(node_id)
    
    # Start from outputs
    for output in nodes:
        if nodes[output].get('type') in ['BUF', 'DFF'] and 'output' in nodes[output]:
            dfs(output)
    
    return result
```

##### 2. **Reachability Analysis**
```python
def find_reachable_nodes(netlist: Dict[str, Any]) -> Set[str]:
    """
    Tìm tất cả nodes có thể tiếp cận từ outputs.
    Sử dụng BFS (Breadth-First Search).
    """
    reachable = set()
    queue = []
    
    # Start từ outputs
    for output_name in netlist.get('outputs', []):
        queue.append(output_name)
        reachable.add(output_name)
    
    # BFS
    while queue:
        current = queue.pop(0)
        node = netlist.get('nodes', {}).get(current, {})
        fanins = node.get('fanins', [])
        
        for fanin in fanins:
            if isinstance(fanin, list) and len(fanin) >= 1:
                input_name = fanin[0]
                if input_name not in reachable:
                    reachable.add(input_name)
                    queue.append(input_name)
    
    return reachable
```

##### 3. **Critical Path Analysis**
```python
def find_critical_path(netlist: Dict[str, Any]) -> List[str]:
    """
    Tìm critical path (longest delay path) trong mạch.
    """
    # Calculate node delays
    node_delays = {}
    max_delay = 0
    critical_end = None
    
    for node_id, node in netlist.get('nodes', {}).items():
        delay = node.get('delay', 1.0)  # Default delay
        
        # Calculate arrival time
        max_fanin_delay = 0
        fanins = node.get('fanins', [])
        for fanin in fanins:
            if isinstance(fanin, list) and len(fanin) >= 1:
                fanin_id = fanin[0]
                max_fanin_delay = max(max_fanin_delay, node_delays.get(fanin_id, 0))
        
        arrival_time = max_fanin_delay + delay
        node_delays[node_id] = arrival_time
        
        if arrival_time > max_delay:
            max_delay = arrival_time
            critical_end = node_id
    
    # Backtrace to find critical path
    critical_path = []
    current = critical_end
    
    while current:
        critical_path.append(current)
        node = netlist.get('nodes', {}).get(current, {})
        fanins = node.get('fanins', [])
        
        # Find fanin with max delay
        max_fanin = None
        max_delay = 0
        
        for fanin in fanins:
            if isinstance(fanin, list) and len(fanin) >= 1:
                fanin_id = fanin[0]
                fanin_delay = node_delays.get(fanin_id, 0)
                if fanin_delay > max_delay:
                    max_delay = fanin_delay
                    max_fanin = fanin_id
        
        current = max_fanin
    
    return critical_path[::-1]  # Reverse to get input-to-output order
```

## 🔢 Boolean Algebra

### 📚 Các phép toán Boolean cơ bản

#### 🎯 Logic Operations

```python
# Basic Boolean operations
def and_op(a: bool, b: bool) -> bool:
    """AND operation: a & b"""
    return a and b

def or_op(a: bool, b: bool) -> bool:
    """OR operation: a | b"""
    return a or b

def xor_op(a: bool, b: bool) -> bool:
    """XOR operation: a ^ b"""
    return a != b

def not_op(a: bool) -> bool:
    """NOT operation: !a"""
    return not a

def nand_op(a: bool, b: bool) -> bool:
    """NAND operation: !(a & b)"""
    return not (a and b)

def nor_op(a: bool, b: bool) -> bool:
    """NOR operation: !(a | b)"""
    return not (a or b)
```

#### 📊 Truth Tables

```python
# Truth table cho 2-input gates
TRUTH_TABLES = {
    'AND': {
        (False, False): False,
        (False, True): False,
        (True, False): False,
        (True, True): True
    },
    'OR': {
        (False, False): False,
        (False, True): True,
        (True, False): True,
        (True, True): True
    },
    'XOR': {
        (False, False): False,
        (False, True): True,
        (True, False): True,
        (True, True): False
    },
    'NAND': {
        (False, False): True,
        (False, True): True,
        (True, False): True,
        (True, True): False
    }
}
```

#### 🧮 Boolean Algebra Laws

```python
# Boolean algebra laws
class BooleanLaws:
    """Implementation of Boolean algebra laws for optimization."""
    
    @staticmethod
    def absorption_law(a: str, b: str) -> str:
        """a & (a | b) = a"""
        return f"{a} & ({a} | {b}) = {a}"
    
    @staticmethod
    def distributive_law(a: str, b: str, c: str) -> str:
        """a & (b | c) = (a & b) | (a & c)"""
        return f"{a} & ({b} | {c}) = ({a} & {b}) | ({a} & {c})"
    
    @staticmethod
    def de_morgan_law(a: str, b: str) -> tuple:
        """!(a & b) = !a | !b and !(a | b) = !a & !b"""
        return (
            f"!({a} & {b}) = !{a} | !{b}",
            f"!({a} | {b}) = !{a} & !{b}"
        )
    
    @staticmethod
    def idempotent_law(a: str) -> str:
        """a & a = a and a | a = a"""
        return f"{a} & {a} = {a} and {a} | {a} = {a}"
```

### 🎯 Karnaugh Maps

#### 📊 K-Map Structure

```python
def create_kmap(variables: List[str]) -> Dict[tuple, bool]:
    """
    Tạo Karnaugh map cho Boolean function.
    
    Args:
        variables: List of variable names ['a', 'b', 'c']
    
    Returns:
        Dictionary mapping input combinations to output values
    """
    n_vars = len(variables)
    kmap = {}
    
    # Generate all possible combinations
    for i in range(2**n_vars):
        combination = []
        for j in range(n_vars):
            combination.append(bool(i & (1 << j)))
        kmap[tuple(combination)] = None  # Output to be determined
    
    return kmap

# Example: 2-variable K-map
def example_2var_kmap():
    """
    K-map cho f(a,b) = a & b
    """
    kmap = {
        (False, False): False,  # a=0, b=0 -> f=0
        (False, True): False,   # a=0, b=1 -> f=0
        (True, False): False,   # a=1, b=0 -> f=0
        (True, True): True      # a=1, b=1 -> f=1
    }
    return kmap
```

#### 🔍 K-Map Minimization

```python
def minimize_kmap(kmap: Dict[tuple, bool]) -> str:
    """
    Minimize Boolean function using K-map.
    
    Args:
        kmap: Karnaugh map with output values
    
    Returns:
        Minimized Boolean expression
    """
    # Find all minterms (where output = True)
    minterms = [combo for combo, output in kmap.items() if output]
    
    # Group adjacent minterms
    groups = group_adjacent_minterms(minterms)
    
    # Generate minimized expression
    expression = generate_expression_from_groups(groups)
    
    return expression

def group_adjacent_minterms(minterms: List[tuple]) -> List[List[tuple]]:
    """
    Group adjacent minterms for minimization.
    """
    groups = []
    used = set()
    
    # Try to group minterms
    for minterm in minterms:
        if minterm in used:
            continue
            
        group = [minterm]
        used.add(minterm)
        
        # Find adjacent minterms
        for other in minterms:
            if other in used:
                continue
            if is_adjacent(minterm, other):
                group.append(other)
                used.add(other)
        
        groups.append(group)
    
    return groups
```

## 🔍 Data Structures cho Optimization

### 📊 Hash Tables

#### 🎯 Structural Hashing

```python
class StructuralHashTable:
    """Hash table for structural hashing algorithm."""
    
    def __init__(self):
        self.hash_table = {}  # hash_key -> node_id
        self.node_table = {}  # node_id -> node_data
    
    def create_hash_key(self, node_data: Dict[str, Any]) -> str:
        """Create hash key for node."""
        gate_type = node_data.get('type', 'UNKNOWN')
        fanins = node_data.get('fanins', [])
        
        # Sort fanins for canonical representation
        sorted_fanins = sorted(fanins, key=lambda x: (x[0], x[1]))
        
        # Create hash key
        fanin_str = ','.join([f"{inp[0]}:{inp[1]}" for inp in sorted_fanins])
        hash_key = f"{gate_type}({fanin_str})"
        
        return hash_key
    
    def add_node(self, node_id: str, node_data: Dict[str, Any]) -> bool:
        """Add node to hash table. Return True if added, False if duplicate."""
        hash_key = self.create_hash_key(node_data)
        
        if hash_key in self.hash_table:
            # Duplicate found
            existing_id = self.hash_table[hash_key]
            return False
        else:
            # Unique node
            self.hash_table[hash_key] = node_id
            self.node_table[node_id] = node_data
            return True
    
    def find_duplicate(self, node_data: Dict[str, Any]) -> Optional[str]:
        """Find duplicate node. Return node_id if found, None otherwise."""
        hash_key = self.create_hash_key(node_data)
        return self.hash_table.get(hash_key)
```

### 🌳 Tree Structures

#### 🎯 Logic Tree Representation

```python
class LogicTreeNode:
    """Node in logic tree."""
    
    def __init__(self, gate_type: str, children: List['LogicTreeNode'] = None):
        self.gate_type = gate_type
        self.children = children or []
        self.value = None  # Computed value
    
    def evaluate(self, inputs: Dict[str, bool]) -> bool:
        """Evaluate tree with given inputs."""
        if self.gate_type in ['AND', 'OR', 'XOR']:
            if len(self.children) != 2:
                raise ValueError(f"{self.gate_type} gate needs exactly 2 inputs")
            
            left = self.children[0].evaluate(inputs)
            right = self.children[1].evaluate(inputs)
            
            if self.gate_type == 'AND':
                return left and right
            elif self.gate_type == 'OR':
                return left or right
            elif self.gate_type == 'XOR':
                return left != right
                
        elif self.gate_type == 'NOT':
            if len(self.children) != 1:
                raise ValueError("NOT gate needs exactly 1 input")
            return not self.children[0].evaluate(inputs)
            
        elif self.gate_type in inputs:
            return inputs[self.gate_type]
        
        else:
            raise ValueError(f"Unknown gate type or input: {self.gate_type}")

class LogicTree:
    """Logic tree for representing Boolean functions."""
    
    def __init__(self, root: LogicTreeNode):
        self.root = root
    
    def evaluate(self, inputs: Dict[str, bool]) -> bool:
        """Evaluate entire tree."""
        return self.root.evaluate(inputs)
    
    def to_netlist(self) -> Dict[str, Any]:
        """Convert tree to netlist format."""
        netlist = {
            'nodes': {},
            'inputs': [],
            'outputs': ['out']
        }
        
        self._convert_node(self.root, netlist, 'out')
        return netlist
    
    def _convert_node(self, node: LogicTreeNode, netlist: Dict[str, Any], output_name: str):
        """Convert tree node to netlist node."""
        if node.gate_type in ['a', 'b', 'c']:  # Input
            netlist['inputs'].append(node.gate_type)
            return
        
        node_id = f"n{len(netlist['nodes'])}"
        fanins = []
        
        for child in node.children:
            if child.gate_type in ['a', 'b', 'c']:
                fanins.append([child.gate_type, False])
            else:
                child_id = f"n{len(netlist['nodes'])}"
                fanins.append([child_id, False])
                self._convert_node(child, netlist, child_id)
        
        netlist['nodes'][node_id] = {
            'type': node.gate_type,
            'fanins': fanins,
            'output': output_name
        }
```

## 🎯 Optimization Principles

### 📊 Cost Functions

#### 🎯 Area Cost

```python
def calculate_area_cost(netlist: Dict[str, Any]) -> float:
    """
    Calculate area cost of netlist.
    """
    total_area = 0.0
    
    for node_id, node in netlist.get('nodes', {}).items():
        gate_type = node.get('type', 'UNKNOWN')
        area = get_gate_area(gate_type)
        total_area += area
    
    return total_area

def get_gate_area(gate_type: str) -> float:
    """Get area cost for different gate types."""
    area_costs = {
        'AND': 2.0,
        'OR': 2.0,
        'XOR': 3.0,
        'NAND': 1.5,
        'NOR': 1.5,
        'NOT': 1.0,
        'BUF': 1.0,
        'AOI21': 2.5,
        'OAI21': 2.5
    }
    return area_costs.get(gate_type, 2.0)  # Default cost
```

#### ⏱️ Timing Cost

```python
def calculate_timing_cost(netlist: Dict[str, Any]) -> float:
    """
    Calculate critical path delay.
    """
    node_delays = {}
    max_delay = 0.0
    
    # Calculate delays for all nodes
    for node_id, node in netlist.get('nodes', {}).items():
        gate_type = node.get('type', 'UNKNOWN')
        gate_delay = get_gate_delay(gate_type)
        
        # Find maximum fanin delay
        max_fanin_delay = 0.0
        fanins = node.get('fanins', [])
        for fanin in fanins:
            if isinstance(fanin, list) and len(fanin) >= 1:
                fanin_id = fanin[0]
                max_fanin_delay = max(max_fanin_delay, node_delays.get(fanin_id, 0.0))
        
        total_delay = max_fanin_delay + gate_delay
        node_delays[node_id] = total_delay
        max_delay = max(max_delay, total_delay)
    
    return max_delay

def get_gate_delay(gate_type: str) -> float:
    """Get delay cost for different gate types."""
    delay_costs = {
        'AND': 0.1,
        'OR': 0.1,
        'XOR': 0.15,
        'NAND': 0.08,
        'NOR': 0.08,
        'NOT': 0.05,
        'BUF': 0.05,
        'AOI21': 0.12,
        'OAI21': 0.12
    }
    return delay_costs.get(gate_type, 0.1)  # Default delay
```

### 🔄 Optimization Strategies

#### 🎯 Multi-objective Optimization

```python
class OptimizationObjective:
    """Multi-objective optimization."""
    
    def __init__(self, area_weight: float = 1.0, delay_weight: float = 1.0):
        self.area_weight = area_weight
        self.delay_weight = delay_weight
    
    def calculate_cost(self, netlist: Dict[str, Any]) -> float:
        """Calculate weighted cost."""
        area_cost = calculate_area_cost(netlist)
        delay_cost = calculate_timing_cost(netlist)
        
        total_cost = (self.area_weight * area_cost + 
                     self.delay_weight * delay_cost)
        
        return total_cost
    
    def is_better(self, cost1: float, cost2: float) -> bool:
        """Check if cost1 is better than cost2."""
        return cost1 < cost2
```

#### 🎯 Pareto Optimization

```python
class ParetoOptimizer:
    """Pareto-optimal solutions."""
    
    def __init__(self):
        self.solutions = []
    
    def add_solution(self, netlist: Dict[str, Any], area: float, delay: float):
        """Add solution to Pareto set."""
        solution = {
            'netlist': netlist,
            'area': area,
            'delay': delay
        }
        
        # Check if this solution dominates any existing solution
        dominated_indices = []
        for i, existing in enumerate(self.solutions):
            if (area <= existing['area'] and delay <= existing['delay'] and
                (area < existing['area'] or delay < existing['delay'])):
                dominated_indices.append(i)
        
        # Remove dominated solutions
        for i in reversed(dominated_indices):
            self.solutions.pop(i)
        
        # Add new solution if not dominated
        is_dominated = any(
            existing['area'] <= area and existing['delay'] <= delay and
            (existing['area'] < area or existing['delay'] < delay)
            for existing in self.solutions
        )
        
        if not is_dominated:
            self.solutions.append(solution)
    
    def get_pareto_front(self) -> List[Dict]:
        """Get Pareto-optimal solutions."""
        return self.solutions
```

## 📚 References

### 📖 Academic References
1. **"Digital Design and Computer Architecture"** - Harris & Harris
2. **"Logic Synthesis and Optimization"** - Giovanni De Micheli
3. **"Introduction to Algorithms"** - Cormen, Leiserson, Rivest, Stein

### 🔗 Technical Resources
1. **ABC Tool**: https://github.com/YosysHQ/abc
2. **Yosys**: https://github.com/YosysHQ/yosys
3. **OpenROAD**: https://github.com/The-OpenROAD-Project/OpenROAD

### 📚 Online Courses
1. **VLSI CAD Part I: Logic** - Coursera
2. **Digital Design and Computer Architecture** - MIT OpenCourseWare
3. **Advanced Digital Design** - Stanford Online

---

**Lưu ý**: Nền tảng lý thuyết này là cơ sở quan trọng để hiểu và implement các thuật toán logic synthesis. Hãy nắm vững các khái niệm này trước khi đi vào chi tiết từng thuật toán.
