"""
Verilog Tokenizer - Xử lý làm sạch và tokenize Verilog code

Module này chịu trách nhiệm:
1. Loại bỏ comments
2. Extract module name và ports
3. Parse port declarations (inputs/outputs)
4. Parse wire declarations
5. Extract assign statements

Tất cả regex đã được compiled trong constants.py để tối ưu performance.
"""

import re
from typing import Dict, List, Tuple, Optional
from .constants import (
    SINGLE_LINE_COMMENT,
    MULTI_LINE_COMMENT,
    MODULE_PATTERN,
    ENDMODULE_PATTERN,
)


class VerilogTokenizer:
    """
    Tokenizer cho Verilog code.
    
    Chức năng:
    - Loại bỏ comments (// và /* */)
    - Extract module information
    - Parse declarations
    - Prepare code cho parsing
    """
    
    def __init__(self, source_code: str, source_file: str = ""):
        """
        Khởi tạo tokenizer với source code.
        
        Args:
            source_code: Verilog source code string
            source_file: Path đến file nguồn (optional)
        """
        self.original_source = source_code
        self.source_file = source_file
        self.cleaned_source = ""
        self.module_name = ""
        self.port_list = ""
        self.module_body = ""
        
    def tokenize(self) -> Dict:
        """
        Thực hiện tokenization toàn bộ.
        
        Returns:
            Dict chứa thông tin đã tokenize:
            {
                'module_name': str,
                'port_list': str,
                'module_body': str,
                'cleaned_source': str
            }
        """
        # Bước 1: Loại bỏ comments
        self.cleaned_source = self._remove_comments(self.original_source)
        
        # Bước 2: Extract module information
        self._extract_module_info()
        
        return {
            'module_name': self.module_name,
            'port_list': self.port_list,
            'module_body': self.module_body,
            'cleaned_source': self.cleaned_source,
        }
    
    def _remove_comments(self, source: str) -> str:
        """
        Loại bỏ tất cả comments từ source code.
        
        Hỗ trợ:
        - Single line comments: // comment
        - Multi line comments: /* comment */
        
        Args:
            source: Verilog source code
            
        Returns:
            Source code không có comments
        """
        # Loại bỏ single line comments
        source = SINGLE_LINE_COMMENT.sub('', source)
        
        # Loại bỏ multi line comments
        source = MULTI_LINE_COMMENT.sub('', source)
        
        return source
    
    def _extract_module_info(self):
        """
        Extract module name, port list và module body.
        
        Tìm module declaration cuối cùng (thường là top module).
        Parse ra:
        - module_name: Tên của module
        - port_list: Danh sách ports trong ()
        - module_body: Nội dung bên trong module
        """
        # Tìm tất cả module declarations
        module_matches = list(MODULE_PATTERN.finditer(self.cleaned_source))
        
        if module_matches:
            # Sử dụng module cuối cùng (thường là top module)
            module_match = module_matches[-1]
            self.module_name = module_match.group(1)
            self.port_list = module_match.group(2)
            
            # Extract module body (từ sau declaration đến endmodule)
            module_end = module_match.end()
            endmodule_match = ENDMODULE_PATTERN.search(
                self.cleaned_source[module_end:]
            )
            
            if endmodule_match:
                self.module_body = self.cleaned_source[
                    module_end:module_end + endmodule_match.start()
                ]
            else:
                # Fallback: lấy tất cả từ sau module declaration
                self.module_body = self.cleaned_source[module_end:]
        else:
            # Không tìm thấy module declaration
            # Fallback: toàn bộ source là body
            self.port_list = ""
            self.module_body = self.cleaned_source


def remove_inline_comments(text: str) -> str:
    """
    Loại bỏ inline comments từ một dòng text.
    
    Helper function để clean up individual lines.
    
    Args:
        text: Text có thể chứa comment
        
    Returns:
        Text đã loại bỏ comment
    """
    return re.sub(r'//.*$', '', text).strip()


def split_signal_list(signal_str: str) -> List[str]:
    """
    Split một string chứa nhiều signal names (phân cách bởi dấu phẩy).
    
    Example:
        "a, b, c" -> ["a", "b", "c"]
        "sum_out, carry_out  " -> ["sum_out", "carry_out"]
    
    Args:
        signal_str: String chứa signal names
        
    Returns:
        List các signal names đã clean
    """
    # Loại bỏ trailing comma
    signal_str = signal_str.rstrip(',').strip()
    
    # Split bởi comma
    signals = [s.strip() for s in signal_str.split(',')]
    
    # Filter empty strings và loại bỏ comments
    signals = [
        remove_inline_comments(s) 
        for s in signals 
        if s
    ]
    
    return [s for s in signals if s]


def calculate_vector_width(msb: str, lsb: str) -> int:
    """
    Tính vector width từ MSB và LSB.
    
    Example:
        [3:0] -> width = 4
        [7:0] -> width = 8
        [15:8] -> width = 8
    
    Args:
        msb: Most Significant Bit (string)
        lsb: Least Significant Bit (string)
        
    Returns:
        Vector width (integer)
    """
    return int(msb) - int(lsb) + 1

