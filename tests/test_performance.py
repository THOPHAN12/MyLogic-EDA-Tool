"""
Performance benchmarks for MyLogic EDA Tool.
"""

import pytest
import time
from core.utils.performance import benchmark, time_function, get_metrics, print_performance_summary
from core.synthesis.strash import apply_strash
from core.optimization.cse import apply_cse
from core.optimization.dce import apply_dce


class TestPerformance:
    """Performance benchmark tests."""
    
    def test_strash_performance(self, duplicate_netlist):
        """Benchmark Strash performance."""
        result, duration = time_function(apply_strash, duplicate_netlist)
        
        assert duration < 1.0  # Should complete in < 1 second
        assert isinstance(result, dict)
    
    def test_cse_performance(self, duplicate_netlist):
        """Benchmark CSE performance."""
        result, duration = time_function(apply_cse, duplicate_netlist)
        
        assert duration < 1.0  # Should complete in < 1 second
        assert isinstance(result, dict)
    
    def test_dce_performance(self, dead_code_netlist):
        """Benchmark DCE performance."""
        result, duration = time_function(apply_dce, dead_code_netlist, 'basic')
        
        assert duration < 1.0  # Should complete in < 1 second
        assert isinstance(result, dict)
    
    def test_large_netlist_performance(self):
        """Test performance with larger netlist."""
        # Create a larger netlist
        large_netlist = {
            'name': 'large_circuit',
            'inputs': [f'in{i}' for i in range(10)],
            'outputs': [f'out{i}' for i in range(5)],
            'nodes': {
                f'n{i}': {
                    'type': 'AND',
                    'inputs': [f'in{i % 10}', f'in{(i+1) % 10}'],
                    'output': f'temp{i}',
                    'name': f'n{i}'
                }
                for i in range(100)
            },
            'wires': {}
        }
        
        result, duration = time_function(apply_strash, large_netlist)
        
        assert duration < 5.0  # Should complete in < 5 seconds
        assert isinstance(result, dict)

