"""
MyLogic EDA Tool - Converters Module
=====================================

This module provides format conversion utilities for MyLogic EDA Tool.

Available converters:
    - MyLogic JSON to Yosys JSON format
    - Future: Verilog to JSON, JSON to Verilog, etc.

Version: 2.0.0
"""

__version__ = "2.0.0"
__all__ = ['convert_to_yosys_format']

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

