"""
Performance benchmarking and metrics utilities.
"""

import time
import functools
from typing import Dict, Any, Callable, Optional
import logging

logger = logging.getLogger(__name__)


class PerformanceMetrics:
    """Track performance metrics for algorithms."""
    
    def __init__(self):
        self.metrics: Dict[str, Dict[str, float]] = {}
    
    def record(self, algorithm: str, operation: str, duration: float, **kwargs):
        """Record a performance metric."""
        if algorithm not in self.metrics:
            self.metrics[algorithm] = {}
        
        key = f"{operation}"
        if key not in self.metrics[algorithm]:
            self.metrics[algorithm][key] = {
                'total_time': 0.0,
                'count': 0,
                'min': float('inf'),
                'max': 0.0,
                'avg': 0.0
            }
        
        metric = self.metrics[algorithm][key]
        metric['total_time'] += duration
        metric['count'] += 1
        metric['min'] = min(metric['min'], duration)
        metric['max'] = max(metric['max'], duration)
        metric['avg'] = metric['total_time'] / metric['count']
        
        # Store additional kwargs
        for k, v in kwargs.items():
            metric[k] = v
    
    def get_summary(self) -> Dict[str, Any]:
        """Get summary of all metrics."""
        return self.metrics
    
    def reset(self):
        """Reset all metrics."""
        self.metrics = {}


# Global metrics instance
_global_metrics = PerformanceMetrics()


def benchmark(func: Callable) -> Callable:
    """
    Decorator to benchmark function execution time.
    
    Usage:
        @benchmark
        def my_function():
            ...
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            duration = time.perf_counter() - start_time
            
            # Record metric
            algorithm = func.__module__.split('.')[-1]
            operation = func.__name__
            _global_metrics.record(algorithm, operation, duration)
            
            logger.debug(f"{func.__name__} took {duration:.4f}s")
            return result
        except Exception as e:
            duration = time.perf_counter() - start_time
            logger.error(f"{func.__name__} failed after {duration:.4f}s: {e}")
            raise
    
    return wrapper


def time_function(func: Callable, *args, **kwargs) -> tuple[Any, float]:
    """
    Time a function execution.
    
    Returns:
        (result, duration_in_seconds)
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    duration = time.perf_counter() - start
    return result, duration


def get_metrics() -> PerformanceMetrics:
    """Get global metrics instance."""
    return _global_metrics


def print_performance_summary():
    """Print performance summary."""
    metrics = _global_metrics.get_summary()
    
    if not metrics:
        print("No performance metrics recorded.")
        return
    
    print("\n" + "=" * 70)
    print("PERFORMANCE SUMMARY")
    print("=" * 70)
    
    for algorithm, operations in metrics.items():
        print(f"\n{algorithm.upper()}:")
        for operation, stats in operations.items():
            print(f"  {operation}:")
            print(f"    Count: {stats['count']}")
            print(f"    Total: {stats['total_time']:.4f}s")
            print(f"    Average: {stats['avg']:.4f}s")
            print(f"    Min: {stats['min']:.4f}s")
            print(f"    Max: {stats['max']:.4f}s")
    
    print("=" * 70)

