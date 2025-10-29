"""Academic alias for parsers.

Re-exports the project's Verilog parser under a concise, consistent namespace.
"""

try:
    # Preferred current parser module
    from frontends.pyverilog import parse_verilog  # type: ignore
except Exception:  # fallback if module path differs
    from frontends.unified_verilog import parse_verilog  # type: ignore

__all__ = ["parse_verilog"]


