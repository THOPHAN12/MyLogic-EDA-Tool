"""
MyLogic EDA Tool - Visualizers Module
======================================

This module provides SVG generation and circuit visualization tools.

Available visualizers:
    - SVG generation from JSON
    - Batch SVG processing
    - Demo circuit creation

Version: 2.0.0
"""

__version__ = "2.0.0"
__all__ = [
    'create_svg_from_json',
    'create_all_svgs',
    'create_demo_svg'
]

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

