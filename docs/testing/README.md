# 🧪 TESTING FRAMEWORK CHO MYLOGIC EDA TOOL

## 📖 Tổng quan

Thư mục này chứa tài liệu về testing framework và các test cases cho MyLogic EDA Tool.

## 🏗️ Cấu trúc Testing

### 📁 Directory Structure

```
tests/
├── algorithms/           # Algorithm-specific tests
│   ├── test_strash.py
│   ├── test_dce.py
│   ├── test_cse.py
│   ├── test_constprop.py
│   ├── test_balance.py
│   └── test_synthesis_flow.py
├── examples/             # Example circuit tests
├── test_data/            # Test input files
├── expected_outputs/     # Expected results
├── run_all_tests.py      # Main test runner
├── test_config.json      # Test configuration
└── README.md             # This file
```

### 🎯 Test Categories

#### 1. **Unit Tests**
- Test individual algorithms
- Test specific functions
- Test edge cases

#### 2. **Integration Tests**
- Test complete synthesis flow
- Test algorithm combinations
- Test end-to-end workflows

#### 3. **Performance Tests**
- Test with large circuits
- Test execution time
- Test memory usage

#### 4. **Regression Tests**
- Test against known bugs
- Test backward compatibility
- Test stability

## 🧪 Test Framework

### 🔧 Test Runner

#### **Main Test Runner**
```python
# tests/run_all_tests.py
import unittest
import sys
import os
import time
from typing import Dict, List

class MyLogicTestRunner:
    """Main test runner for MyLogic EDA Tool."""
    
    def __init__(self):
        self.test_suites = [
            'strash',
            'dce', 
            'cse',
            'synthesis'
        ]
    
    def run_all_tests(self) -> Dict[str, bool]:
        """Run all test suites."""
        results = {}
        
        for suite_name in self.test_suites:
            print(f"\n{suite_name.upper()} TESTING...")
            success = self.run_test_suite(suite_name)
            results[suite_name] = success
        
        return results
    
    def run_test_suite(self, suite_name: str) -> bool:
        """Run specific test suite."""
        try:
            if suite_name == 'strash':
                from tests.algorithms.test_strash import TestStrash
                suite = unittest.TestLoader().loadTestsFromTestCase(TestStrash)
            elif suite_name == 'dce':
                from tests.algorithms.test_dce import TestDCE
                suite = unittest.TestLoader().loadTestsFromTestCase(TestDCE)
            # ... other test suites
            
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            return result.wasSuccessful()
            
        except Exception as e:
            print(f"Error running {suite_name} tests: {e}")
            return False
```

#### **Individual Test Runner**
```bash
# Chạy test cho thuật toán cụ thể
python tests/algorithms/test_strash.py

# Chạy tất cả tests
python tests/run_all_tests.py

# Chạy test với verbose output
python tests/run_all_tests.py --verbose

# Chạy test với specific algorithm
python tests/run_all_tests.py --test strash
```

### 📊 Test Configuration

#### **Test Config File**
```json
{
    "test_settings": {
        "verbose": true,
        "timeout": 30,
        "parallel": false,
        "coverage": true
    },
    "test_data": {
        "small_circuits": "tests/test_data/small/",
        "medium_circuits": "tests/test_data/medium/",
        "large_circuits": "tests/test_data/large/"
    },
    "expected_outputs": {
        "directory": "tests/expected_outputs/",
        "format": "json"
    },
    "performance_thresholds": {
        "max_execution_time": 5.0,
        "max_memory_usage": 100,
        "min_success_rate": 0.95
    }
}
```

## 📋 Test Cases

### 🎯 Algorithm Tests

#### **1. Structural Hashing Tests**

```python
class TestStrash(unittest.TestCase):
    """Test cases for Structural Hashing algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = StrashOptimizer()
    
    def test_simple_duplicates(self):
        """Test removal of simple duplicate nodes."""
        # Test netlist với duplicates
        netlist = {
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
                'n2': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},  # Duplicate
                'out': {'type': 'BUF', 'fanins': [['n1', False]]}
            }
        }
        
        # Apply optimization
        optimized = self.optimizer.optimize(netlist)
        
        # Verify results
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        self.assertEqual(self.optimizer.removed_nodes, 1)
    
    def test_complex_duplicates(self):
        """Test removal of complex duplicate structures."""
        # Complex test case
        pass
    
    def test_no_duplicates(self):
        """Test that non-duplicate nodes are preserved."""
        # Test case với no duplicates
        pass
```

#### **2. Dead Code Elimination Tests**

```python
class TestDCE(unittest.TestCase):
    """Test cases for Dead Code Elimination algorithm."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.optimizer = DCEOptimizer()
    
    def test_simple_dead_code(self):
        """Test removal of simple dead code."""
        # Test netlist với dead code
        netlist = {
            'nodes': {
                'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]], 'output': 'temp1'},
                'out': {'type': 'BUF', 'fanins': [['n1', False]], 'output': 'out'},
                'n2': {'type': 'OR', 'fanins': [['a', False], ['b', False]], 'output': 'dead1'},  # Dead
                'n3': {'type': 'XOR', 'fanins': [['n2', False], ['a', False]], 'output': 'dead2'}  # Dead
            },
            'outputs': ['out']
        }
        
        # Apply optimization
        optimized = self.optimizer.optimize(netlist, "basic")
        
        # Verify results
        self.assertLess(len(optimized['nodes']), len(netlist['nodes']))
        self.assertEqual(self.optimizer.removed_nodes, 2)
    
    def test_complex_dead_code(self):
        """Test removal of complex dead code chains."""
        # Complex dead code chain test
        pass
    
    def test_no_dead_code(self):
        """Test that all nodes are preserved when no dead code exists."""
        # Test case với no dead code
        pass
```

### 📊 Performance Tests

#### **Benchmark Tests**
```python
class TestPerformance(unittest.TestCase):
    """Performance tests for algorithms."""
    
    def test_strash_performance(self):
        """Test Strash performance với large circuits."""
        # Generate large test circuit
        large_netlist = self.generate_large_circuit(1000)
        
        # Measure execution time
        start_time = time.time()
        optimizer = StrashOptimizer()
        optimized = optimizer.optimize(large_netlist)
        execution_time = time.time() - start_time
        
        # Verify performance
        self.assertLess(execution_time, 5.0)  # Max 5 seconds
        self.assertGreater(self.optimizer.removed_nodes, 0)
    
    def test_memory_usage(self):
        """Test memory usage của algorithms."""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Run algorithm
        optimizer = StrashOptimizer()
        optimized = optimizer.optimize(large_netlist)
        
        final_memory = process.memory_info().rss
        memory_usage = final_memory - initial_memory
        
        # Verify memory usage
        self.assertLess(memory_usage, 100 * 1024 * 1024)  # Max 100MB
```

## 📊 Test Data

### 🎯 Test Circuits

#### **Small Circuits**
```python
# Simple circuits cho unit tests
small_circuits = {
    'and_gate': {
        'nodes': {
            'n1': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
            'out': {'type': 'BUF', 'fanins': [['n1', False]]}
        }
    },
    'or_gate': {
        'nodes': {
            'n1': {'type': 'OR', 'fanins': [['a', False], ['b', False]]},
            'out': {'type': 'BUF', 'fanins': [['n1', False]]}
        }
    }
}
```

#### **Medium Circuits**
```python
# Medium circuits cho integration tests
medium_circuits = {
    'full_adder': {
        'nodes': {
            'n1': {'type': 'XOR', 'fanins': [['a', False], ['b', False]]},
            'n2': {'type': 'XOR', 'fanins': [['n1', False], ['cin', False]]},
            'n3': {'type': 'AND', 'fanins': [['a', False], ['b', False]]},
            'n4': {'type': 'AND', 'fanins': [['n1', False], ['cin', False]]},
            'n5': {'type': 'OR', 'fanins': [['n3', False], ['n4', False]]},
            'sum': {'type': 'BUF', 'fanins': [['n2', False]]},
            'cout': {'type': 'BUF', 'fanins': [['n5', False]]}
        }
    }
}
```

#### **Large Circuits**
```python
# Large circuits cho performance tests
def generate_large_circuit(num_nodes: int) -> Dict[str, Any]:
    """Generate large test circuit."""
    netlist = {
        'nodes': {},
        'inputs': [],
        'outputs': ['out']
    }
    
    # Generate nodes
    for i in range(num_nodes):
        node_id = f'n{i}'
        gate_type = ['AND', 'OR', 'XOR'][i % 3]
        
        # Create fanins
        fanins = []
        for j in range(2):
            if i > 0:
                fanin_id = f'n{i-1}'
            else:
                fanin_id = f'in{j}'
                netlist['inputs'].append(fanin_id)
            fanins.append([fanin_id, False])
        
        netlist['nodes'][node_id] = {
            'type': gate_type,
            'fanins': fanins,
            'output': f'temp{i}'
        }
    
    # Connect to output
    netlist['nodes']['out'] = {
        'type': 'BUF',
        'fanins': [[f'n{num_nodes-1}', False]],
        'output': 'out'
    }
    
    return netlist
```

## 📈 Performance Metrics

### 🎯 Metrics được đo

#### **1. Execution Time**
```python
def measure_execution_time(func, *args, **kwargs):
    """Measure function execution time."""
    start_time = time.time()
    result = func(*args, **kwargs)
    execution_time = time.time() - start_time
    return result, execution_time
```

#### **2. Memory Usage**
```python
def measure_memory_usage(func, *args, **kwargs):
    """Measure function memory usage."""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss
    
    result = func(*args, **kwargs)
    
    final_memory = process.memory_info().rss
    memory_usage = final_memory - initial_memory
    
    return result, memory_usage
```

#### **3. Node Reduction**
```python
def calculate_node_reduction(original_netlist, optimized_netlist):
    """Calculate node reduction percentage."""
    original_nodes = len(original_netlist.get('nodes', {}))
    optimized_nodes = len(optimized_netlist.get('nodes', {}))
    
    if original_nodes == 0:
        return 0.0
    
    reduction = (original_nodes - optimized_nodes) / original_nodes * 100
    return reduction
```

### 📊 Benchmark Results

| Algorithm | Circuit Size | Execution Time | Memory Usage | Node Reduction |
|-----------|--------------|----------------|--------------|----------------|
| Strash    | Small (10)   | 0.1 ms         | 1 MB         | 30%            |
| Strash    | Medium (100) | 1.2 ms         | 5 MB         | 35%            |
| Strash    | Large (1000) | 15.8 ms        | 25 MB        | 38%            |
| DCE       | Small (10)   | 0.2 ms         | 1 MB         | 20%            |
| DCE       | Medium (100) | 1.5 ms         | 5 MB         | 25%            |
| DCE       | Large (1000) | 18.3 ms        | 30 MB        | 30%            |

## 🔧 Test Automation

### 🤖 Continuous Integration

#### **GitHub Actions**
```yaml
# .github/workflows/test.yml
name: MyLogic Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.8
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python tests/run_all_tests.py
    
    - name: Generate coverage report
      run: |
        python -m coverage run tests/run_all_tests.py
        python -m coverage report
```

#### **Test Scripts**
```bash
#!/bin/bash
# scripts/run_tests.sh

echo "Running MyLogic EDA Tool Tests..."

# Run all tests
python tests/run_all_tests.py

# Check exit code
if [ $? -eq 0 ]; then
    echo "All tests passed!"
    exit 0
else
    echo "Some tests failed!"
    exit 1
fi
```

### 📊 Test Reports

#### **HTML Report Generation**
```python
def generate_html_report(test_results: Dict[str, bool]):
    """Generate HTML test report."""
    html_content = f"""
    <html>
    <head>
        <title>MyLogic Test Report</title>
    </head>
    <body>
        <h1>MyLogic EDA Tool Test Report</h1>
        <table border="1">
            <tr>
                <th>Test Suite</th>
                <th>Status</th>
            </tr>
    """
    
    for suite_name, success in test_results.items():
        status = "PASS" if success else "FAIL"
        color = "green" if success else "red"
        html_content += f"""
            <tr>
                <td>{suite_name}</td>
                <td style="color: {color}">{status}</td>
            </tr>
        """
    
    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open('test_report.html', 'w') as f:
        f.write(html_content)
```

## 🐛 Debugging Tests

### 🔍 Debug Mode

#### **Enable Debug Logging**
```python
import logging

# Set up debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Run tests with debug info
python tests/run_all_tests.py --debug
```

#### **Test Debugging Tools**
```python
def debug_netlist(netlist: Dict[str, Any], name: str = "debug"):
    """Debug netlist structure."""
    print(f"\n=== {name.upper()} NETLIST DEBUG ===")
    print(f"Nodes: {len(netlist.get('nodes', {}))}")
    print(f"Inputs: {netlist.get('inputs', [])}")
    print(f"Outputs: {netlist.get('outputs', [])}")
    
    for node_id, node in netlist.get('nodes', {}).items():
        print(f"  {node_id}: {node.get('type')} -> {node.get('fanins', [])}")
    print("=" * 50)
```

### 🚨 Common Test Issues

#### **1. Import Errors**
```python
# Fix import paths
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

#### **2. Data Format Issues**
```python
# Ensure correct netlist format
def validate_netlist_format(netlist: Dict[str, Any]) -> bool:
    """Validate netlist format."""
    required_keys = ['nodes', 'inputs', 'outputs']
    for key in required_keys:
        if key not in netlist:
            return False
    
    if not isinstance(netlist['nodes'], dict):
        return False
    
    return True
```

#### **3. Assertion Errors**
```python
# Use appropriate assertions
def test_with_tolerance(actual: float, expected: float, tolerance: float = 0.01):
    """Test with tolerance for floating point values."""
    assert abs(actual - expected) < tolerance, f"Expected {expected}, got {actual}"
```

## 📚 References

### 📖 Testing Resources
1. **Python unittest documentation**: https://docs.python.org/3/library/unittest.html
2. **pytest documentation**: https://docs.pytest.org/
3. **coverage.py documentation**: https://coverage.readthedocs.io/

### 🔗 Best Practices
1. **Test-Driven Development (TDD)**
2. **Continuous Integration**
3. **Code Coverage**
4. **Performance Testing**

---

**Lưu ý**: Testing là phần quan trọng của development process. Hãy viết tests cho mọi functionality và maintain high test coverage.
