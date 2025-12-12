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
                'cleaned_source': str,
                'module_body_start_line': int
            }
        """
        # Kiểm tra cân bằng ngoặc cơ bản trước khi parse sâu
        self._validate_brackets(self.original_source)

        # Bước 1: Loại bỏ comments
        self.cleaned_source = self._remove_comments(self.original_source)
        
        # Bước 2: Extract module information
        self._extract_module_info()
        
        return {
            'module_name': self.module_name,
            'param_list': getattr(self, 'param_list', ''),
            'port_list': self.port_list,
            'module_body': self.module_body,
            'cleaned_source': self.cleaned_source,
            'module_body_start_line': getattr(self, 'module_body_start_line', 1)
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
        
        if not module_matches:
            # Không tìm thấy module declaration → báo lỗi rõ ràng
            raise ValueError(f"Syntax error: không tìm thấy 'module ...' trong {self.source_file}")

        # Sử dụng module cuối cùng (thường là top module)
        module_match = module_matches[-1]
        self.module_name = module_match.group(1)
        self.param_list = module_match.group(2) or ""
        self.port_list = module_match.group(3) or ""
        
        # Extract module body (từ sau declaration đến endmodule)
        module_end = module_match.end()
        # Tính dòng bắt đầu của module_body so với file gốc (1-based)
        module_decl = module_match.group(0)
        idx_orig = self.original_source.find(module_decl)
        if idx_orig >= 0:
            self.module_body_start_line = self.original_source[:idx_orig + len(module_decl)].count('\n') + 1
        else:
            # Fallback: dùng cleaned_source
            self.module_body_start_line = self.cleaned_source[:module_end].count('\n') + 1

        endmodule_match = ENDMODULE_PATTERN.search(
            self.cleaned_source[module_end:]
        )
        
        if endmodule_match:
            self.module_body = self.cleaned_source[
                module_end:module_end + endmodule_match.start()
            ]
        else:
            # Thiếu endmodule → báo lỗi thay vì nuốt lỗi
            raise ValueError(f"Syntax error: thiếu 'endmodule' trong {self.source_file}")

    def _validate_brackets(self, source: str) -> None:
        """
        Kiểm tra cân bằng ngoặc tròn/vuông/cặp begin-end đơn giản.
        Báo lỗi sớm nếu mất cân bằng để giúp người dùng dễ sửa.
        """
        pairs = {'(': ')', '[': ']'}
        stack = []
        for ch in source:
            if ch in pairs:
                stack.append(ch)
            elif ch in pairs.values():
                if not stack or pairs[stack.pop()] != ch:
                    raise ValueError(f"Syntax error: ngoặc không cân bằng trong {self.source_file}")
        if stack:
            raise ValueError(f"Syntax error: ngoặc không cân bằng trong {self.source_file}")


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


def _eval_int_simple(expr: str, params: Dict[str, int]) -> int:
    """
    Eval biểu thức số nguyên đơn giản (tránh circular import với parser).
    Hỗ trợ số, parameters, và biểu thức số học cơ bản.
    """
    import re
    expr = expr.strip()
    
    # Nếu là số thuần
    if re.fullmatch(r'[0-9]+', expr):
        return int(expr)
    
    # Nếu chỉ là tên tham số
    if expr.isalpha() or (expr.replace('_', '').isalnum() and not any(c in expr for c in '+-*/%()')):
        if expr not in params:
            raise ValueError(f"Unknown param {expr}")
        return params[expr]
    
    # Thay thế tham số trong biểu thức
    for k, v in params.items():
        expr = re.sub(rf'\b{k}\b', str(v), expr)
    
    # Kiểm tra an toàn
    if not re.match(r'^[0-9+\-*/%\s()]+$', expr):
        raise ValueError(f"Unsafe expression: {expr}")
    
    # Eval an toàn
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return int(result)
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression '{expr}': {e}")


def calculate_vector_width(msb: str, lsb: str, params: Dict[str, int] = None) -> int:
    """
    Tính vector width từ MSB và LSB, hỗ trợ parameterized widths.
    
    Example:
        [3:0] -> width = 4
        [7:0] -> width = 8
        [15:8] -> width = 8
        [N-1:0] -> width = N (nếu N trong params)
        [WIDTH-1:0] -> width = WIDTH (nếu WIDTH trong params)
    
    Args:
        msb: Most Significant Bit (string, có thể là số hoặc biểu thức)
        lsb: Least Significant Bit (string, có thể là số hoặc biểu thức)
        params: Dictionary chứa parameter values (optional)
        
    Returns:
        Vector width (integer)
        
    Raises:
        ValueError: Nếu không thể tính được width (param chưa biết)
    """
    params = params or {}
    
    # Nếu là số thuần, tính trực tiếp
    try:
        msb_val = int(msb)
        lsb_val = int(lsb)
        return msb_val - lsb_val + 1
    except ValueError:
        pass
    
    # Nếu là biểu thức, eval với params
    try:
        msb_val = _eval_int_simple(msb, params)
        lsb_val = _eval_int_simple(lsb, params)
        return msb_val - lsb_val + 1
    except Exception:
        # Nếu không eval được, trả về width mặc định 1 (scalar)
        # Parser sẽ xử lý sau khi có đủ params
        return 1

