"""
Verilog Parser Core Module

Module này chứa core implementation của Verilog parser:
- constants: Regex patterns, operator definitions
- tokenizer: Code cleaning và tokenization
- node_builder: Node creation và wire generation
- parser: Main parsing logic
- expression_parser: Complex expression handling

Usage:
    from frontends.verilog.core import parse_verilog
    
    netlist = parse_verilog('design.v')

Author: MyLogic Team
Version: 2.0.0
"""

from .parser import parse_verilog

__all__ = ['parse_verilog']

