"""
Verilog Parser Module - MyLogic EDA Tool

Module parser Verilog được tổ chức theo cấu trúc modular để dễ đọc và maintain.

Cấu trúc:
- constants.py: Các hằng số và regex patterns
- tokenizer.py: Xử lý tokenization và làm sạch code
- node_builder.py: Tạo nodes và wire connections
- operations/: Các parser cho từng loại operation
- parser.py: Main parser logic

Author: MyLogic Team
Version: 2.0.0
"""

from .parser import parse_verilog

__all__ = ['parse_verilog']

