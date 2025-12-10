"""
Verilog Parser Module - MyLogic EDA Tool

Module parser Verilog được tổ chức theo cấu trúc modular để dễ đọc và maintain.

Cấu trúc:
- docs/: Documentation folder (README.md, ARCHITECTURE.md, INDEX.md)
- core/: Core implementation (organized)
  - constants.py: Regex patterns, operator definitions
  - tokenizer.py: Tokenization và code cleaning
  - node_builder.py: Node creation và wire generation
  - parser.py: Main parsing logic
  - expression_parser.py: Complex expression handling
- operations/: Operation parsers (modular)
  - arithmetic.py, bitwise.py, logical.py, comparison.py, shift.py, special.py

Documentation:
- See docs/README.md for comprehensive guide
- See docs/ARCHITECTURE.md for design details
- See docs/INDEX.md for navigation

Author: MyLogic Team
Version: 2.0.0
"""

from .core import parse_verilog

__all__ = ['parse_verilog']

