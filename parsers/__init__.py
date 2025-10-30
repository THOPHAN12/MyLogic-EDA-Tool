"""
Parsers Module - Export parse_verilog cho compatibility

File này export parse_verilog để code hiện tại không bị break.

Current imports in codebase:
    from parsers import parse_verilog

Được redirect đến:
    frontends.verilog.parser.parse_verilog
"""

# Import từ frontends
from frontends.verilog import parse_verilog

__all__ = ['parse_verilog']
