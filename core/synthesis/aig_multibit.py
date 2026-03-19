#!/usr/bin/env python3
"""
Multi-bit AIG Support

Extension to AIG to support multi-bit signals and operations.
Each multi-bit signal is represented as a list of single-bit AIG nodes.
"""

from typing import List, Optional, Tuple
from core.synthesis.aig import AIGNode

logger = None
try:
    import logging
    logger = logging.getLogger(__name__)
except:
    pass


class MultiBitAIGNode:
    """
    Multi-bit AIG node - represents a vector of single-bit AIG nodes.
    
    This class wraps multiple single-bit AIG nodes to represent
    multi-bit signals for arithmetic and other multi-bit operations.
    """
    
    def __init__(self, width: int, bits: List[AIGNode]):
        """
        Initialize multi-bit AIG node.
        
        Args:
            width: Bit width of the signal
            bits: List of single-bit AIG nodes [bit0, bit1, ..., bitN-1]
                  where bit0 is LSB (least significant bit)
        """
        if len(bits) != width:
            raise ValueError(f"Width mismatch: expected {width} bits, got {len(bits)}")
        
        self.width = width
        self.bits = bits  # [bit0 (LSB), bit1, ..., bitN-1 (MSB)]
    
    def get_bit(self, index: int) -> AIGNode:
        """
        Get single-bit node at position index.
        
        Args:
            index: Bit position (0 = LSB, width-1 = MSB)
        """
        if index < 0 or index >= self.width:
            raise IndexError(f"Bit index {index} out of range [0, {self.width-1}]")
        return self.bits[index]
    
    def get_lsb(self) -> AIGNode:
        """Get least significant bit (bit 0)."""
        return self.bits[0]
    
    def get_msb(self) -> AIGNode:
        """Get most significant bit (bit width-1)."""
        return self.bits[-1]
    
    def __repr__(self):
        return f"MultiBitAIGNode(width={self.width}, bits=[{self.bits[0].node_id}...{self.bits[-1].node_id}])"
    
    def __len__(self):
        """Return width (number of bits)."""
        return self.width


def create_constant_multibit(aig, value: int, width: int) -> MultiBitAIGNode:
    """
    Create multi-bit constant from integer value.
    
    Args:
        aig: AIG object
        value: Integer value
        width: Bit width
    
    Returns:
        MultiBitAIGNode with constant bits
    """
    bits = []
    for i in range(width):
        bit_value = bool(value & (1 << i))
        bits.append(aig.const1 if bit_value else aig.const0)
    
    return MultiBitAIGNode(width, bits)


def parse_constant_string(const_str: str, default_width: int = 8) -> tuple[int, int]:
    """
    Parse constant string like "8'd10", "8'hFF", "1'b1" into (value, width).
    
    Args:
        const_str: Constant string (e.g., "8'd10", "8'hFF", "1'b1")
        default_width: Default width if not specified
    
    Returns:
        Tuple (value, width)
    """
    # Handle format: [width]'[base][value]
    # Examples: "8'd10", "8'hFF", "1'b1", "8'b0"
    
    if "'" not in const_str:
        # Try to parse as plain integer
        try:
            value = int(const_str)
            return value, default_width
        except:
            return 0, default_width
    
    parts = const_str.split("'")
    if len(parts) != 2:
        return 0, default_width
    
    width_str = parts[0].strip()
    base_value = parts[1].strip()
    
    # Parse width
    try:
        width = int(width_str) if width_str else None
    except:
        width = None
    
    # Parse value
    if not base_value:
        return 0, width
    
    base = base_value[0].lower()
    value_str = base_value[1:] if len(base_value) > 1 else ""
    
    if base == 'd':
        # Decimal
        try:
            value = int(value_str, 10) if value_str else 0
        except:
            value = 0
    elif base == 'h':
        # Hexadecimal
        try:
            value = int(value_str, 16) if value_str else 0
        except:
            value = 0
    elif base == 'b':
        # Binary
        try:
            value = int(value_str, 2) if value_str else 0
        except:
            value = 0
    elif base == 'o':
        # Octal
        try:
            value = int(value_str, 8) if value_str else 0
        except:
            value = 0
    else:
        # Try to parse as decimal
        try:
            value = int(base_value, 10)
        except:
            value = 0
    
    # If unsized like "'b1", choose minimal width from literal (educational scope)
    if width is None:
        if base == 'b':
            width = max(1, len(value_str))
        elif base == 'h':
            width = max(1, len(value_str) * 4)
        elif base == 'o':
            width = max(1, len(value_str) * 3)
        else:
            width = default_width

    return value, width

