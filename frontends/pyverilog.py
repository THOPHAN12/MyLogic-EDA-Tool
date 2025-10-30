"""
PyVerilog - Backward Compatibility Wrapper

File này maintain backward compatibility với code cũ.
Import từ module mới nhưng export với tên cũ.

DEPRECATED: File này chỉ để backward compatibility.
Nên sử dụng: from frontends.verilog import parse_verilog

Author: MyLogic Team
Version: 2.0.0
"""

# Import từ module mới
from .verilog.parser import parse_verilog

# Export để code cũ vẫn hoạt động
__all__ = ['parse_verilog']

# Thông báo deprecation (có thể bật nếu muốn)
# import warnings
# warnings.warn(
#     "frontends.pyverilog is deprecated. "
#     "Use 'from frontends.verilog import parse_verilog' instead.",
#     DeprecationWarning,
#     stacklevel=2
# )
