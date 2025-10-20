"""
MyLogic EDA Tool - Analyzers Module
====================================

This module provides circuit analysis and understanding tools.

Available analyzers:
    - Format comparison (MyLogic vs Yosys)
    - Structure analysis
    - Cell type explanation
    - Visualization capability demo

Version: 2.0.0
"""

__version__ = "2.0.0"
__all__ = [
    'compare_formats',
    'show_yosys_structure',
    'explain_cell_types',
    'cell_types_summary',
    'demo_mylogic_visualization'
]

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

