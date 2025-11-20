# 🧪 Test Suite Documentation

## Overview

MyLogic EDA Tool now includes a comprehensive test suite with pytest.

## Running Tests

### Basic Test Execution

```bash
# Run all tests
python -m pytest tests/

# Run with verbose output
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_strash.py

# Run specific test class
python -m pytest tests/test_strash.py::TestStrash

# Run specific test
python -m pytest tests/test_strash.py::TestStrash::test_basic_strash
```

### Using Test Runner

```bash
# Run all tests
python tests/run_tests.py

# Run with coverage
python tests/run_tests.py --coverage

# Run with verbose output
python tests/run_tests.py --verbose
```

### Coverage Reports

```bash
# Generate coverage report
python -m pytest tests/ --cov=core --cov=parsers --cov=cli --cov-report=html

# View HTML report
# Open htmlcov/index.html in browser
```

## Test Structure

```
tests/
├── __init__.py              # Test package initialization
├── conftest.py             # Pytest fixtures and configuration
├── test_strash.py          # Structural Hashing tests
├── test_dce.py             # Dead Code Elimination tests
├── test_cse.py             # Common Subexpression Elimination tests
├── test_constprop.py       # Constant Propagation tests
├── test_balance.py         # Logic Balancing tests
├── test_synthesis_flow.py  # Complete synthesis flow tests
├── test_parser.py          # Verilog parser tests
├── test_integration.py     # Integration tests
├── test_performance.py     # Performance benchmarks
└── run_tests.py            # Test runner script
```

## Test Fixtures

Common fixtures are defined in `conftest.py`:

- `sample_netlist`: Basic test netlist
- `duplicate_netlist`: Netlist with duplicate nodes
- `dead_code_netlist`: Netlist with dead code
- `constant_netlist`: Netlist with constants
- `unbalanced_netlist`: Netlist with unbalanced gates

## Writing New Tests

### Example Test

```python
import pytest
from core.synthesis.strash import apply_strash

def test_my_algorithm(sample_netlist):
    """Test my algorithm."""
    result = apply_strash(sample_netlist)
    
    assert isinstance(result, dict)
    assert 'nodes' in result
    assert len(result['nodes']) <= len(sample_netlist['nodes'])
```

### Test Markers

```python
@pytest.mark.unit
def test_unit_function():
    """Unit test."""
    pass

@pytest.mark.integration
def test_integration():
    """Integration test."""
    pass

@pytest.mark.slow
def test_slow_operation():
    """Slow test."""
    pass
```

## Continuous Integration

Tests run automatically on:
- Push to main/develop branches
- Pull requests
- Multiple Python versions (3.8-3.12)

See `.github/workflows/tests.yml` for CI configuration.

## Test Coverage Goals

- **Current**: ~60% (estimated)
- **Target**: >80%
- **Ideal**: >90%

## Performance Benchmarks

Performance tests ensure algorithms complete within reasonable time:

- Small netlists (< 10 nodes): < 0.1s
- Medium netlists (10-100 nodes): < 1.0s
- Large netlists (100+ nodes): < 5.0s

## Troubleshooting

### Import Errors

If you see import errors, ensure you're running from the project root:

```bash
cd D:\DO_AN_2\Mylogic
python -m pytest tests/
```

### Missing Dependencies

Install test dependencies:

```bash
pip install -r requirements.txt
```

### Skipped Tests

Some tests may be skipped if dependencies are missing (e.g., external tools).
This is expected and tests will be marked as "SKIPPED".

