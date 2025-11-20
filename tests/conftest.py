"""
Pytest configuration and fixtures for MyLogic EDA Tool tests.
"""

import pytest
import sys
import os
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def sample_netlist() -> Dict[str, Any]:
    """Sample netlist for testing."""
    return {
        'name': 'test_circuit',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1', 'name': 'n1'},
            'n2': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out1', 'name': 'n2'},
            'n3': {'type': 'XOR', 'inputs': ['a', 'b'], 'output': 'out2', 'name': 'n3'}
        },
        'wires': {
            'w1': {'source': 'a', 'sink': 'n1'},
            'w2': {'source': 'b', 'sink': 'n1'},
            'w3': {'source': 'n1', 'sink': 'n2'},
            'w4': {'source': 'c', 'sink': 'n2'},
            'w5': {'source': 'a', 'sink': 'n3'},
            'w6': {'source': 'b', 'sink': 'n3'}
        }
    }

@pytest.fixture
def duplicate_netlist() -> Dict[str, Any]:
    """Netlist with duplicate nodes for Strash testing."""
    return {
        'name': 'duplicate_circuit',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out1', 'out2'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1', 'name': 'n1'},
            'n2': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp2', 'name': 'n2'},  # Duplicate
            'n3': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out1', 'name': 'n3'},
            'n4': {'type': 'OR', 'inputs': ['temp2', 'c'], 'output': 'out2', 'name': 'n4'}
        },
        'wires': {
            'w1': {'source': 'a', 'sink': 'n1'},
            'w2': {'source': 'b', 'sink': 'n1'},
            'w3': {'source': 'a', 'sink': 'n2'},
            'w4': {'source': 'b', 'sink': 'n2'},
            'w5': {'source': 'n1', 'sink': 'n3'},
            'w6': {'source': 'n2', 'sink': 'n4'},
            'w7': {'source': 'c', 'sink': 'n3'},
            'w8': {'source': 'c', 'sink': 'n4'}
        }
    }

@pytest.fixture
def dead_code_netlist() -> Dict[str, Any]:
    """Netlist with dead code for DCE testing."""
    return {
        'name': 'dead_code_circuit',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1', 'name': 'n1'},
            'n2': {'type': 'OR', 'inputs': ['a', 'b'], 'output': 'temp2', 'name': 'n2'},
            'n3': {'type': 'XOR', 'inputs': ['temp1', 'temp2'], 'output': 'out', 'name': 'n3'},
            'n4': {'type': 'AND', 'inputs': ['temp1', 'temp2'], 'output': 'dead_out', 'name': 'n4'}  # Dead
        },
        'wires': {
            'w1': {'source': 'a', 'sink': 'n1'},
            'w2': {'source': 'b', 'sink': 'n1'},
            'w3': {'source': 'a', 'sink': 'n2'},
            'w4': {'source': 'b', 'sink': 'n2'},
            'w5': {'source': 'n1', 'sink': 'n3'},
            'w6': {'source': 'n2', 'sink': 'n3'},
            'w7': {'source': 'n1', 'sink': 'n4'},
            'w8': {'source': 'n2', 'sink': 'n4'}
        }
    }

@pytest.fixture
def constant_netlist() -> Dict[str, Any]:
    """Netlist with constants for ConstProp testing."""
    return {
        'name': 'constant_circuit',
        'inputs': ['a'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'CONST', 'value': 1, 'output': 'const1', 'name': 'n1'},
            'n2': {'type': 'AND', 'inputs': ['a', 'const1'], 'output': 'out', 'name': 'n2'}
        },
        'wires': {
            'w1': {'source': 'n1', 'sink': 'n2'},
            'w2': {'source': 'a', 'sink': 'n2'}
        }
    }

@pytest.fixture
def unbalanced_netlist() -> Dict[str, Any]:
    """Netlist with unbalanced gates for Balance testing."""
    return {
        'name': 'unbalanced_circuit',
        'inputs': ['a', 'b', 'c', 'd', 'e'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b', 'c', 'd', 'e'], 'output': 'out', 'name': 'n1'}
        },
        'wires': {
            'w1': {'source': 'a', 'sink': 'n1'},
            'w2': {'source': 'b', 'sink': 'n1'},
            'w3': {'source': 'c', 'sink': 'n1'},
            'w4': {'source': 'd', 'sink': 'n1'},
            'w5': {'source': 'e', 'sink': 'n1'}
        }
    }

