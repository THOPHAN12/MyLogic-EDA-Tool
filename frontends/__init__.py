"""
Frontends Module - Verilog và các frontend parsers khác

Module này chứa các parsers cho different input formats:
- verilog: Verilog parser (refactored, modular)
- pyverilog: Backward compatibility wrapper

Recommended import:
    from frontends.verilog import parse_verilog

Legacy import (deprecated):
    from frontends.pyverilog import parse_verilog
"""

# Import chính từ verilog module
from .verilog import parse_verilog

__all__ = ['parse_verilog']

