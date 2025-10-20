"""
MyLogic EDA Tool - Utilities Module
====================================

This module provides testing and validation utilities.

Available utilities:
    - JSON format testing
    - Netlistsvg compatibility testing
    - SVG comparison and analysis

Version: 2.0.0
"""

__version__ = "2.0.0"
__all__ = [
    'simple_test',
    'test_netlistsvg_compatibility',
    'compare_svg_versions',
    'view_svg_details'
]

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

