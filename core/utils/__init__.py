"""
Utility modules for MyLogic EDA Tool.
"""

from .error_handling import (
    MyLogicError,
    ValidationError,
    OptimizationError,
    ParserError,
    validate_netlist,
    safe_optimize,
    safe_parse,
    validate_file_path
)

from .performance import (
    PerformanceMetrics,
    benchmark,
    time_function,
    get_metrics,
    print_performance_summary
)

__all__ = [
    'MyLogicError',
    'ValidationError',
    'OptimizationError',
    'ParserError',
    'validate_netlist',
    'safe_optimize',
    'safe_parse',
    'validate_file_path',
    'PerformanceMetrics',
    'benchmark',
    'time_function',
    'get_metrics',
    'print_performance_summary'
]

