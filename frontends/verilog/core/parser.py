"""
Verilog Parser - Main Parser Logic

File này tổng hợp tất cả các modules lại:
- tokenizer: Làm sạch và tokenize code
- node_builder: Tạo nodes và connections
- operations/*: Parse từng loại operation

Flow:
1. Tokenize source code
2. Extract ports và wires
3. Parse assign statements
4. Parse gate/module instantiations
5. Generate wire connections
6. Compute statistics

Author: MyLogic Team
Version: 2.0.0 (Refactored)
"""

from typing import Dict, Any, List
import re

from .tokenizer import (
    VerilogTokenizer,
    split_signal_list,
    calculate_vector_width,
    remove_inline_comments
)
from .node_builder import NodeBuilder, WireGenerator
from .constants import *
from ..operations import *
from .expression_parser import parse_complex_expression


def parse_verilog(path: str) -> Dict[str, Any]:
    """
    Parse file Verilog thành netlist dictionary.
    
    Đây là entry point chính của parser. Function này:
    1. Đọc file Verilog
    2. Tokenize và làm sạch code
    3. Extract module info, ports, wires
    4. Parse tất cả statements
    5. Generate connections
    6. Tính statistics
    
    Args:
        path: Đường dẫn đến file Verilog
        
    Returns:
        Dictionary chứa netlist với cấu trúc:
        {
            "name": str,              # Tên module
            "inputs": List[str],      # Danh sách inputs
            "outputs": List[str],     # Danh sách outputs
            "wires": List[Dict],      # Danh sách wire connections
            "nodes": List[Dict],      # Danh sách nodes (operations)
            "attrs": {                # Attributes bổ sung
                "source_file": str,
                "vector_widths": Dict,
                "output_mapping": Dict,
                "parsing_stats": Dict
            }
        }
        
    Raises:
        ValueError: Nếu path invalid
        FileNotFoundError: Nếu file không tồn tại
    """
    # Validate input
    if not path or not isinstance(path, str):
        raise ValueError("Path phải là string không rỗng")
    
    # Đọc file - nâng cấp error handling giống YosysHQ
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            source_code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Không tìm thấy file: {path}")
    except UnicodeDecodeError as e:
        # Thử với encoding khác nếu UTF-8 fail
        try:
            with open(path, 'r', encoding='latin-1') as f:
                source_code = f.read()
        except Exception:
            raise ValueError(f"Không thể đọc file {path}: encoding error - {e}")
    except Exception as e:
        raise ValueError(f"Lỗi khi đọc file {path}: {e}")
    
    # Khởi tạo netlist structure
    netlist = _initialize_netlist(path)
    
    # Bước 1: Tokenize
    tokenizer = VerilogTokenizer(source_code, path)
    tokens = tokenizer.tokenize()

    # Kiểm tra lỗi cú pháp cơ bản để trả về thông báo rõ ràng
    if not tokens.get('module_name'):
        raise ValueError(f"Syntax error: không tìm thấy module declaration trong {path}")
    if not tokens.get('module_body', '').strip():
        raise ValueError(f"Syntax error: thiếu 'endmodule' hoặc module body rỗng trong {path}")
    _basic_statement_validation(
        tokens.get('module_body', ''),
        path,
        tokens.get('module_body_start_line', 1)
    )
    _validate_generate_blocks(tokens.get('module_body', ''), path)
    
    # Bước 2: Extract module info
    netlist['name'] = tokens['module_name']
    
    # Bước 3: Parse parameters và localparams trước (cần cho width calculation)
    _parse_parameters(netlist, tokens['module_body'])
    
    # Thu thập parameter (từ header và body) để hỗ trợ width calculation và unroll for/if
    params = _collect_parameters(tokens.get('param_list', ''), tokens['module_body'])
    
    # Bước 3.5: Parse ports và wires (với params để tính parameterized widths)
    _parse_port_declarations(netlist, tokens, params)
    _parse_wire_declarations(netlist, tokens['module_body'], params)

    node_builder = NodeBuilder()

    # Bước 3.75: Parse generate blocks (for/if) và lấy phần còn lại cho assign
    assign_body = _parse_generate_blocks(tokens['module_body'], node_builder, params)
    
    # Bước 4: Parse functions và tasks trước (cần để parse calls)
    _parse_functions(netlist, tokens['module_body'], params)
    _parse_tasks(netlist, tokens['module_body'])
    
    # Bước 4.5: Parse assign statements, always blocks, case statements, và gates
    _parse_always_blocks(netlist, tokens['module_body'], node_builder)
    _parse_case_statements(netlist, tokens['module_body'], node_builder)
    _parse_assign_statements(netlist, assign_body, node_builder)
    _parse_gate_instantiations(netlist, tokens['module_body'], node_builder)
    _parse_module_instantiations(netlist, tokens['module_body'], node_builder)
    
    # Bước 5: Lấy nodes từ builder
    netlist['nodes'] = node_builder.get_nodes()
    netlist['attrs']['output_mapping'].update(node_builder.get_output_mapping())
    
    # Bước 6: Generate wire connections
    if AUTO_GENERATE_WIRES:
        wires = WireGenerator.generate_wires(netlist['nodes'])
        netlist['wires'] = wires
        WireGenerator.add_wire_statistics(netlist, wires)
    
    # Bước 7: Compute statistics
    if COMPUTE_STATISTICS:
        _compute_statistics(netlist)
    
    # Bước 8: Ensure output mapping
    _ensure_output_mapping(netlist)
    
    return netlist


def _basic_statement_validation(module_body: str, path: str, base_line: int) -> None:
    """
    Kiểm tra nhanh một số lỗi cú pháp phổ biến:
    - Dòng có dấu '=' nhưng không có 'assign' ở đầu và thiếu ';'
    - Dòng có '=' nhưng thiếu ';'
    """
    suspicious_prefixes = (
        "assign", "wire", "reg", "input", "output",
        "parameter", "localparam", "always", "if",
        "for", "case", "while", "generate", "end", "module"
    )

    # Bỏ qua các dòng nằm bên trong always block, generate block, function, và task để không false-positive
    from .constants import ALWAYS_PATTERN, GENERATE_PATTERN, FUNCTION_PATTERN, TASK_PATTERN
    skip_lines = set()

    def _mark_skip(pattern):
        for m in pattern.finditer(module_body):
            start_idx, end_idx = m.span()
            prefix = module_body[:start_idx]
            start_line = prefix.count('\n') + base_line + 1
            block_lines = module_body[start_idx:end_idx].count('\n') + 1
            for lno in range(start_line, start_line + block_lines):
                skip_lines.add(lno)

    _mark_skip(ALWAYS_PATTERN)
    _mark_skip(GENERATE_PATTERN)
    _mark_skip(FUNCTION_PATTERN)
    _mark_skip(TASK_PATTERN)

    for lineno, raw in enumerate(module_body.splitlines(), start=base_line + 1):
        if lineno in skip_lines:
            continue
        line = raw.strip()
        if not line or line.startswith("//"):
            continue
        has_eq = "=" in line
        has_semicolon = ";" in line
        starts_with_kw = line.startswith(suspicious_prefixes)
        has_nonblocking = "<=" in line

        # Bỏ qua nonblocking (<=) vì thuộc procedural
        if has_nonblocking:
            continue

        # Nếu có dấu '=' mà không bắt đầu bằng keyword hợp lệ → thiếu assign / statement không hợp lệ
        if has_eq and not starts_with_kw:
            raise ValueError(
                f"Syntax error: thiếu 'assign' hoặc statement không hợp lệ tại dòng {lineno} của {path}"
            )

        # Thiếu assign hoặc thiếu ; trên dòng gán đơn giản
        if has_eq and not starts_with_kw and not has_semicolon:
            raise ValueError(
                f"Syntax error: thiếu 'assign' hoặc ';' tại dòng {lineno} của {path}"
            )


def _validate_generate_blocks(module_body: str, path: str) -> None:
    """
    Kiểm tra generate/endgenerate: nếu có từ khóa generate nhưng không khớp endgenerate -> báo lỗi.
    """
    from .constants import GENERATE_PATTERN
    found = False
    for _ in GENERATE_PATTERN.finditer(module_body):
        found = True
    if "generate" in module_body and not found:
        raise ValueError(f"Syntax error: thiếu 'endgenerate' trong {path}")


def _parse_generate_blocks(module_body: str, node_builder: NodeBuilder, params: Dict[str, int]) -> str:
    """
    Parse generate blocks (for/if) ở mức đơn giản:
    - Nếu có generate/endgenerate hợp lệ, parse assign bên trong
    - Trả về module_body đã loại bỏ các generate block để tránh parse trùng
    """
    from .constants import GENERATE_PATTERN, FOR_PATTERN, IF_PATTERN, IF_ELSE_PATTERN

    cleaned = module_body
    for m in GENERATE_PATTERN.finditer(module_body):
        block_full = m.group(0)
        block_content = m.group(1) or ""

        # Unroll for-loops bên trong generate
        block_content = _unroll_generate_for(block_content, params, node_builder)
        # Unroll if/else đơn giản bên trong generate
        block_content = _unroll_generate_if(block_content, params, node_builder)
        # Parse assign statements (bên ngoài for/if đã unroll)
        _parse_assign_statements({}, block_content, node_builder)

        # Loại bỏ block khỏi module_body để tránh parse trùng ở bước assign chung
        cleaned = cleaned.replace(block_full, "")

    return cleaned


def _collect_parameters(param_list: str, module_body: str) -> Dict[str, int]:
    """
    Thu thập parameter/localparam, hỗ trợ biểu thức số học đơn giản.
    
    Hỗ trợ:
    - parameter N = 8;
    - parameter WIDTH = 16, DEPTH = 32;
    - parameter SIZE = N * 2;
    - localparam MAX = WIDTH - 1;
    """
    params: Dict[str, int] = {}
    import re
    from .constants import PARAMETER_PATTERN, LOCALPARAM_PATTERN
    
    # Helper để eval parameter value
    def eval_param_value(value_str: str, current_params: Dict[str, int]) -> int:
        """Eval giá trị parameter, có thể là số hoặc biểu thức."""
        value_str = value_str.strip()
        # Nếu là số thuần
        if re.fullmatch(r'[0-9]+', value_str):
            return int(value_str)
        # Thay thế parameters đã biết trong biểu thức
        expr = value_str
        for k, v in current_params.items():
            expr = re.sub(rf'\b{k}\b', str(v), expr)
        # Eval an toàn (chỉ cho phép +, -, *, /, %, và số)
        try:
            # Chỉ cho phép các ký tự an toàn
            if not re.match(r'^[0-9+\-*/%\s()]+$', expr):
                raise ValueError(f"Unsafe expression: {expr}")
            return int(eval(expr, {"__builtins__": None}, {}))
        except Exception:
            raise ValueError(f"Cannot evaluate parameter expression: {value_str}")
    
    # Thu thập theo thứ tự: header params trước, sau đó body params/localparams
    # Header params
    for m in PARAMETER_PATTERN.finditer(param_list or ''):
        name = m.group(1)
        value_str = m.group(2)
        try:
            params[name] = eval_param_value(value_str, params)
        except Exception:
            # Nếu không eval được, bỏ qua (có thể phụ thuộc vào param khác chưa định nghĩa)
            pass
    
    # Body params/localparams (có thể phụ thuộc vào header params)
    all_param_patterns = [
        (PARAMETER_PATTERN, "parameter"),
        (LOCALPARAM_PATTERN, "localparam")
    ]
    
    # Lặp nhiều lần để xử lý dependencies (tối đa 10 lần để tránh vòng lặp vô hạn)
    max_iterations = 10
    for iteration in range(max_iterations):
        found_new = False
        for pattern, param_type in all_param_patterns:
            for m in pattern.finditer(module_body):
                name = m.group(1)
                if name in params:
                    continue  # Đã có rồi
                value_str = m.group(2)
                try:
                    params[name] = eval_param_value(value_str, params)
                    found_new = True
                except Exception:
                    # Có thể chưa đủ dependencies, thử lại ở lần lặp sau
                    pass
        if not found_new:
            break
    
    return params


def _eval_int(expr: str, params: Dict[str, int]) -> int:
    """
    Eval biểu thức số nguyên, hỗ trợ:
    - Số nguyên: 8, 16, 32
    - Parameters: N, WIDTH
    - Biểu thức số học: N-1, WIDTH*2, SIZE+1, (N+1)/2
    - Nested expressions với parentheses
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
    
    # Thay thế tham số trong biểu thức (giữ nguyên các toán tử và số)
    # Sử dụng word boundary để tránh thay thế nhầm
    for k, v in params.items():
        expr = re.sub(rf'\b{k}\b', str(v), expr)
    
    # Kiểm tra an toàn: chỉ cho phép số, toán tử, và dấu ngoặc
    if not re.match(r'^[0-9+\-*/%\s()]+$', expr):
        raise ValueError(f"Unsafe expression: {expr}")
    
    # Eval an toàn biểu thức số
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return int(result)
    except Exception as e:
        raise ValueError(f"Cannot evaluate expression '{expr}': {e}")


def _unroll_generate_for(block_content: str, params: Dict[str, int], node_builder: NodeBuilder) -> str:
    """Unroll for-loop đơn giản trong generate, thay biến loop bằng hằng."""
    from .constants import FOR_PATTERN
    content = block_content
    for m in FOR_PATTERN.finditer(block_content):
        init, cond, step, begin_body, single_stmt = m.groups()
        body = (begin_body or single_stmt or "").strip()
        try:
            # Parse init: i = 0
            var_name, init_rhs = [x.strip() for x in init.split('=')]
            i = _eval_int(init_rhs, params)

            # Parse cond: i < N or i <= N
            import re
            cond = cond.strip()
            cond_match = re.match(rf'{re.escape(var_name)}\s*(<=|<)\s*(.+)', cond)
            if not cond_match:
                continue
            op = cond_match.group(1)
            cond_rhs = cond_match.group(2).strip()

            # Parse step: i = i + 1
            step_rhs = step.replace(var_name, '').replace('=', '').strip()
            step_val = 1
            if '+' in step_rhs:
                step_val = _eval_int(step_rhs.split('+')[-1], params)
            elif '-' in step_rhs:
                step_val = -_eval_int(step_rhs.split('-')[-1], params)

            # Unroll loop
            unrolled = ""
            iter_count = 0
            while True:
                rhs_val = _eval_int(cond_rhs, params)
                ok = i <= rhs_val if op == '<=' else i < rhs_val
                if not ok:
                    break
                iter_body = body.replace(var_name, str(i))
                _parse_assign_statements({}, iter_body, node_builder)
                unrolled += f"// unrolled {var_name}={i}\n{iter_body}\n"
                i += step_val
                iter_count += 1
                if iter_count > 1024:  # safety
                    break

            # Remove the for-block from content
            content = content.replace(m.group(0), unrolled)
        except Exception:
            # Nếu không unroll được (param chưa biết), giữ nguyên block
            continue

    return content


def _unroll_generate_if(block_content: str, params: Dict[str, int], node_builder: NodeBuilder) -> str:
    """Unroll if/else đơn giản trong generate: chỉ giữ nhánh nếu eval được cond."""
    from .constants import IF_PATTERN, IF_ELSE_PATTERN
    content = block_content

    # Handle if-else
    for m in IF_ELSE_PATTERN.finditer(block_content):
        cond, then_begin, then_stmt, else_begin, else_stmt = m.groups()
        cond = cond.strip()
        try:
            cond_val = _eval_int(cond, params)
        except Exception:
            continue
        body = (then_begin or then_stmt or "") if cond_val else (else_begin or else_stmt or "")
        body = body.strip()
        _parse_assign_statements({}, body, node_builder)
        content = content.replace(m.group(0), body)

    # Handle if without else
    for m in IF_PATTERN.finditer(block_content):
        cond, then_begin, then_stmt = m.groups()
        cond = cond.strip()
        try:
            cond_val = _eval_int(cond, params)
        except Exception:
            continue
        if not cond_val:
            # remove block
            content = content.replace(m.group(0), "")
        else:
            body = (then_begin or then_stmt or "").strip()
            _parse_assign_statements({}, body, node_builder)
            content = content.replace(m.group(0), body)

    return content


# ============================================================================
# INITIALIZATION
# ============================================================================

def _initialize_netlist(source_file: str) -> Dict[str, Any]:
    """
    Khởi tạo netlist structure rỗng.
    
    Args:
        source_file: Path đến file nguồn
        
    Returns:
        Netlist dictionary với structure cơ bản
    """
    return {
        "name": "",
        "inputs": [],
        "outputs": [],
        "wires": [],
        "nodes": [],
        "attrs": {
            "source_file": source_file,
            "vector_widths": {},
            "output_mapping": {},
            "parsing_stats": {}
        }
    }


# ============================================================================
# PORT DECLARATIONS PARSING
# ============================================================================

def _parse_port_declarations(netlist: Dict, tokens: Dict, params: Dict[str, int] = None):
    """
    Parse input/output declarations từ port list và module body.
    
    Hỗ trợ:
    - Vector ports: input [3:0] a, b;
    - Scalar ports: input clk, reset;
    - Signed/unsigned: input signed [7:0] data;
    - Parameterized widths: input [N-1:0] addr;
    - Port list style: module test(input a, output b);
    - Module body style: input a; output b;
    
    Args:
        netlist: Netlist dictionary để update
        tokens: Tokens từ tokenizer
        params: Dictionary chứa parameter values (cho parameterized widths)
    """
    port_list = tokens['port_list']
    module_body = tokens['module_body']
    params = params or {}
    
    # Parse inputs
    _parse_input_ports(netlist, port_list, module_body, params)
    
    # Parse outputs
    _parse_output_ports(netlist, port_list, module_body, params)


def _parse_input_ports(netlist: Dict, port_list: str, module_body: str, params: Dict[str, int] = None):
    """
    Parse input ports (cả vector và scalar), hỗ trợ signed/unsigned và parameterized widths.
    """
    from .constants import SIGNED_KEYWORD, UNSIGNED_KEYWORD
    params = params or {}
    signed_signals = netlist['attrs'].setdefault('signed_signals', [])
    
    # Helper để parse một declaration line
    def parse_declaration(match, is_vector: bool, is_signed: bool = False):
        if is_vector:
            msb, lsb, signals_str = match.groups()
            width = calculate_vector_width(msb, lsb, params)
        else:
            signals_str = match.group(1)
            width = 1
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if not signal:
                continue
            if signal not in netlist['inputs']:
                netlist['inputs'].append(signal)
            netlist['attrs']['vector_widths'][signal] = width
            if is_signed:
                if signal not in signed_signals:
                    signed_signals.append(signal)
    
    # 1. Vector inputs từ port list
    for match in PORT_INPUT_VECTOR_PATTERN.finditer(port_list):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=True, is_signed=is_signed)
    
    # 2. Scalar inputs từ port list
    for match in PORT_INPUT_SCALAR_PATTERN.finditer(port_list):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=False, is_signed=is_signed)
    
    # 3. Vector inputs từ module body
    for match in INPUT_VECTOR_PATTERN.finditer(module_body):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=True, is_signed=is_signed)
    
    # 4. Scalar inputs từ module body
    for match in INPUT_SCALAR_PATTERN.finditer(module_body):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=False, is_signed=is_signed)


def _parse_output_ports(netlist: Dict, port_list: str, module_body: str, params: Dict[str, int] = None):
    """
    Parse output ports (cả vector và scalar), hỗ trợ signed/unsigned và parameterized widths.
    """
    from .constants import SIGNED_KEYWORD, UNSIGNED_KEYWORD
    params = params or {}
    signed_signals = netlist['attrs'].setdefault('signed_signals', [])
    
    # Helper để parse một declaration line
    def parse_declaration(match, is_vector: bool, is_signed: bool = False):
        if is_vector:
            msb, lsb, signals_str = match.groups()
            width = calculate_vector_width(msb, lsb, params)
        else:
            signals_str = match.group(1)
            width = 1
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if not signal:
                continue
            if signal not in netlist['outputs']:
                netlist['outputs'].append(signal)
            netlist['attrs']['vector_widths'][signal] = width
            if is_signed:
                if signal not in signed_signals:
                    signed_signals.append(signal)
    
    # 1. Vector outputs từ port list
    for match in PORT_OUTPUT_VECTOR_PATTERN.finditer(port_list):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=True, is_signed=is_signed)
    
    # 2. Scalar outputs từ port list
    for match in PORT_OUTPUT_SCALAR_PATTERN.finditer(port_list):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=False, is_signed=is_signed)
    
    # 3. Vector outputs từ module body
    for match in OUTPUT_VECTOR_PATTERN.finditer(module_body):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=True, is_signed=is_signed)
    
    # 4. Scalar outputs từ module body
    for match in OUTPUT_SCALAR_PATTERN.finditer(module_body):
        decl_text = match.group(0)
        is_signed = bool(SIGNED_KEYWORD.search(decl_text))
        parse_declaration(match, is_vector=False, is_signed=is_signed)


# ============================================================================
# PARAMETER & LOCALPARAM PARSING
# ============================================================================

def _parse_parameters(netlist: Dict, module_body: str):
    """
    Parse parameter và localparam declarations.
    
    Hỗ trợ:
    - parameter WIDTH = 8;
    - parameter DEPTH = 16, ADDR_WIDTH = 4;
    - localparam MAX = 255;
    - parameter [7:0] DATA = 8'hFF;
    
    Args:
        netlist: Netlist dictionary để update
        module_body: Module body content
    """
    from .constants import PARAMETER_PATTERN, LOCALPARAM_PATTERN
    
    parameters = netlist['attrs'].setdefault('parameters', {})
    
    # Parse parameters
    for match in PARAMETER_PATTERN.finditer(module_body):
        param_name = match.group(1).strip()
        param_value = match.group(2).strip()
        parameters[param_name] = param_value
    
    # Parse localparams
    for match in LOCALPARAM_PATTERN.finditer(module_body):
        param_name = match.group(1).strip()
        param_value = match.group(2).strip()
        parameters[param_name] = param_value
        parameters[f'localparam_{param_name}'] = param_value  # Mark as localparam


# ============================================================================
# WIRE DECLARATIONS PARSING
# ============================================================================

def _parse_wire_declarations(netlist: Dict, module_body: str, params: Dict[str, int] = None):
    """
    Parse wire declarations - nâng cấp giống YosysHQ.
    
    Hỗ trợ:
    - wire [3:0] temp;
    - wire [3:0] temp = a + b;
    - wire signed [7:0] data;
    - wire [N-1:0] addr; (parameterized width)
    - wire clk;
    - wire ready = enable & valid;
    - Multiple declarations: wire a, b, c;
    - Mixed vector và scalar: wire [7:0] data; wire clk;
    """
    from .constants import (
        WIRE_VECTOR_ASSIGN_PATTERN, WIRE_SCALAR_ASSIGN_PATTERN,
        WIRE_VECTOR_PATTERN, WIRE_SCALAR_PATTERN, REG_PATTERN,
        SIGNED_KEYWORD, UNSIGNED_KEYWORD
    )
    params = params or {}
    signed_signals = netlist['attrs'].setdefault('signed_signals', [])
    
    # Helper để xử lý signed
    def check_signed(decl_text: str) -> bool:
        return bool(SIGNED_KEYWORD.search(decl_text))
    
    # Pattern 1: wire [3:0] temp = assignment;
    for match in WIRE_VECTOR_ASSIGN_PATTERN.finditer(module_body):
        msb, lsb, signals_str, assignment = match.groups()
        decl_text = match.group(0)
        width = calculate_vector_width(msb, lsb, params)
        is_signed = check_signed(decl_text)
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                wire_entry = f"{signal} = {assignment.strip()}"
                if wire_entry not in netlist['wires']:
                    netlist['wires'].append(wire_entry)
                    netlist['attrs']['vector_widths'][wire_entry] = width
                    netlist['attrs']['vector_widths'][signal] = width
                    if is_signed and signal not in signed_signals:
                        signed_signals.append(signal)
    
    # Pattern 2: wire temp = assignment; (scalar)
    for match in WIRE_SCALAR_ASSIGN_PATTERN.finditer(module_body):
        signals_str, assignment = match.groups()
        decl_text = match.group(0)
        is_signed = check_signed(decl_text)
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                wire_entry = f"{signal} = {assignment.strip()}"
                if wire_entry not in netlist['wires']:
                    netlist['wires'].append(wire_entry)
                    netlist['attrs']['vector_widths'][wire_entry] = 1
                    netlist['attrs']['vector_widths'][signal] = 1
                    if is_signed and signal not in signed_signals:
                        signed_signals.append(signal)
    
    # Pattern 3: wire [3:0] temp; (declaration only)
    for match in WIRE_VECTOR_PATTERN.finditer(module_body):
        msb, lsb, signals_str = match.groups()
        decl_text = match.group(0)
        width = calculate_vector_width(msb, lsb, params)
        is_signed = check_signed(decl_text)
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal and signal not in netlist['wires']:
                netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
                if is_signed and signal not in signed_signals:
                    signed_signals.append(signal)
    
    # Pattern 4: wire temp; (scalar declaration)
    for match in WIRE_SCALAR_PATTERN.finditer(module_body):
        signals_str = match.group(1)
        decl_text = match.group(0)
        is_signed = check_signed(decl_text)
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal and signal not in netlist['wires']:
                netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = 1
                if is_signed and signal not in signed_signals:
                    signed_signals.append(signal)
    
    # Pattern 5: Memory declarations (reg [width-1:0] mem [depth-1:0];)
    from .constants import MEMORY_PATTERN
    for match in MEMORY_PATTERN.finditer(module_body):
        width_msb, width_lsb, mem_name, depth_msb, depth_lsb = match.groups()
        decl_text = match.group(0)
        is_signed = check_signed(decl_text)
        
        # Tính width và depth
        width = calculate_vector_width(width_msb, width_lsb, params)
        depth = calculate_vector_width(depth_msb, depth_lsb, params)
        
        # Lưu memory information
        if 'memories' not in netlist['attrs']:
            netlist['attrs']['memories'] = {}
        
        netlist['attrs']['memories'][mem_name] = {
            'width': width,
            'width_msb': width_msb,
            'width_lsb': width_lsb,
            'depth': depth,
            'depth_msb': depth_msb,
            'depth_lsb': depth_lsb,
            'signed': is_signed
        }
        
        # Memory cũng là một signal (có thể index)
        if mem_name not in netlist['wires']:
            netlist['wires'].append(mem_name)
        netlist['attrs']['vector_widths'][mem_name] = width
        netlist['attrs'].setdefault('memory_signals', []).append(mem_name)
        if is_signed and mem_name not in signed_signals:
            signed_signals.append(mem_name)
    
    # Pattern 6: reg declarations (giống wire, hỗ trợ signed/unsigned và parameterized widths)
    # Skip nếu đã match memory pattern
    for match in REG_PATTERN.finditer(module_body):
        # Check xem có phải memory không (đã parse ở trên)
        mem_match = MEMORY_PATTERN.search(match.group(0))
        if mem_match:
            continue  # Đã parse như memory
        
        groups = match.groups()
        decl_text = match.group(0)
        is_signed = check_signed(decl_text)
        
        if len(groups) >= 3 and groups[0] and groups[1]:
            msb, lsb, signals_str = groups[0], groups[1], groups[2]
            width = calculate_vector_width(msb, lsb, params)
        else:
            signals_str = groups[-1] if groups else ""
            width = 1
        
        for signal in split_signal_list(signals_str):
            signal = signal.strip()
            if signal:
                # Regs có thể không là wires, nhưng vẫn cần track
                if signal not in netlist['wires']:
                    netlist['wires'].append(signal)
                netlist['attrs']['vector_widths'][signal] = width
                netlist['attrs'].setdefault('reg_signals', []).append(signal)
                if is_signed and signal not in signed_signals:
                    signed_signals.append(signal)


# ============================================================================
# ALWAYS BLOCKS PARSING (SEQUENTIAL CIRCUITS)
# ============================================================================

def _parse_always_blocks(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse always blocks cho sequential circuits.
    
    Hỗ trợ:
    - always @(posedge clk) { ... }
    - always @(negedge clk) { ... }
    - Non-blocking assignments (<=)
    - Blocking assignments (=) trong always blocks
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        node_builder: NodeBuilder instance
    """
    from .constants import (
        ALWAYS_PATTERN, EDGE_PATTERN, POSEDGE_PATTERN, NEGEDGE_PATTERN,
        NON_BLOCKING_ASSIGN_PATTERN, BLOCKING_ASSIGN_PATTERN, BEGIN_END_PATTERN
    )
    
    # Tìm tất cả always blocks
    for match in ALWAYS_PATTERN.finditer(module_body):
        sensitivity_list = match.group(1).strip()
        # Group 2 là begin...end content, group 3 là {...} content
        block_content = (match.group(2) or match.group(3) or '').strip()
        
        # Parse edge sensitivity (posedge/negedge)
        clock_signal = None
        edge_type = None
        
        posedge_match = POSEDGE_PATTERN.search(sensitivity_list)
        negedge_match = NEGEDGE_PATTERN.search(sensitivity_list)
        
        if posedge_match:
            clock_signal = posedge_match.group(1)
            edge_type = 'posedge'
        elif negedge_match:
            clock_signal = negedge_match.group(1)
            edge_type = 'negedge'
        else:
            # Combinational always block (@(*) hoặc không có edge)
            # Parse như combinational logic (blocking assignments)
            _parse_always_combinational(block_content, node_builder)
            continue
        
        # Sequential always block với clock edge
        # Extract begin-end content nếu có
        begin_match = BEGIN_END_PATTERN.search(block_content)
        if begin_match:
            block_content = begin_match.group(1).strip()
        
        # Parse non-blocking assignments (<=) - Sequential logic
        _parse_always_sequential(block_content, clock_signal, edge_type, node_builder)


def _parse_always_sequential(
    block_content: str,
    clock_signal: str,
    edge_type: str,
    node_builder: NodeBuilder
):
    """
    Parse sequential always block với clock edge.
    
    Args:
        block_content: Nội dung của always block
        clock_signal: Clock signal name
        edge_type: 'posedge' hoặc 'negedge'
        node_builder: NodeBuilder instance
    """
    from .constants import NON_BLOCKING_ASSIGN_PATTERN
    from .expression_parser import parse_complex_expression
    
    # Tìm tất cả non-blocking assignments (<=)
    for match in NON_BLOCKING_ASSIGN_PATTERN.finditer(block_content):
        output_signal = match.group(1).strip()
        input_expression = match.group(2).strip()
        
        # Tạo DFF node cho sequential assignment
        dff_node_id = node_builder.create_sequential_node(
            node_type='DFF',
            data_input=input_expression,
            clock_signal=clock_signal,
            edge_type=edge_type,
            output_signal=output_signal
        )


def _parse_always_combinational(block_content: str, node_builder: NodeBuilder):
    """
    Parse combinational always block (@(*) hoặc không có edge).
    
    Hỗ trợ:
    - Blocking assignments (=)
    - Case statements
    - If-else statements
    
    Args:
        block_content: Nội dung của always block
        node_builder: NodeBuilder instance
    """
    from .constants import (
        BLOCKING_ASSIGN_PATTERN, BEGIN_END_PATTERN, CASE_PATTERN
    )
    from .expression_parser import parse_complex_expression
    
    # Extract begin-end content nếu có
    begin_match = BEGIN_END_PATTERN.search(block_content)
    if begin_match:
        block_content = begin_match.group(1).strip()
    
    # Parse case statements trước (có thể chứa assignments)
    _parse_case_statements_in_block(block_content, node_builder)
    
    # Loại bỏ case statements đã parse để tránh parse trùng
    cleaned_content = block_content
    for match in CASE_PATTERN.finditer(block_content):
        cleaned_content = cleaned_content.replace(match.group(0), '')
    
    # Tìm tất cả blocking assignments (=)
    for match in BLOCKING_ASSIGN_PATTERN.finditer(cleaned_content):
        output_signal = match.group(1).strip()
        input_expression = match.group(2).strip()
        
        # Parse expression như combinational logic
        parse_complex_expression(node_builder, output_signal, input_expression)


# ============================================================================
# CASE STATEMENTS PARSING
# ============================================================================

def _parse_case_statements(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse case statements (case, casex, casez) ở top-level module body.
    
    Case statements thường nằm trong always blocks, nhưng cũng có thể
    ở top-level (ít gặp hơn).
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        node_builder: NodeBuilder instance
    """
    from .constants import CASE_PATTERN
    
    # Tìm case statements không nằm trong always blocks
    # (case trong always đã được parse bởi _parse_always_combinational)
    for match in CASE_PATTERN.finditer(module_body):
        case_type = match.group(1) or ''  # 'x', 'z', hoặc '' (case)
        selector = match.group(2).strip()
        case_body = match.group(3).strip()
        
        # Parse case items
        _parse_case_body(selector, case_body, case_type, node_builder)


def _parse_case_statements_in_block(block_content: str, node_builder: NodeBuilder):
    """
    Parse case statements trong always block hoặc block khác.
    
    Args:
        block_content: Block content (always block, begin-end, etc.)
        node_builder: NodeBuilder instance
    """
    from .constants import CASE_PATTERN
    
    # Tìm tất cả case statements trong block
    for match in CASE_PATTERN.finditer(block_content):
        case_type = match.group(1) or ''
        selector = match.group(2).strip()
        case_body = match.group(3).strip()
        
        # Parse case items
        _parse_case_body(selector, case_body, case_type, node_builder)


def _parse_case_body(
    selector: str,
    case_body: str,
    case_type: str,
    node_builder: NodeBuilder
):
    """
    Parse case body và tạo logic nodes.
    
    Args:
        selector: Selector expression (ví dụ: sel[1:0])
        case_body: Nội dung case statement
        case_type: 'x', 'z', hoặc '' (case)
        node_builder: NodeBuilder instance
    """
    from .constants import CASE_ITEM_PATTERN, CASE_ITEM_BLOCK_PATTERN
    from ..operations.special import parse_ternary_operation
    
    case_items = []
    default_item = None
    
    # Parse case items với begin-end blocks trước
    for match in CASE_ITEM_BLOCK_PATTERN.finditer(case_body):
        value_str = match.group(1).strip()
        block_content = match.group(2).strip()
        
        if value_str.lower() == 'default':
            default_item = block_content
        else:
            case_items.append((value_str, block_content))
    
    # Parse case items đơn giản (không có begin-end)
    # Loại bỏ các items đã parse bởi CASE_ITEM_BLOCK_PATTERN
    remaining_body = case_body
    for match in CASE_ITEM_BLOCK_PATTERN.finditer(case_body):
        remaining_body = remaining_body.replace(match.group(0), '')
    
    for match in CASE_ITEM_PATTERN.finditer(remaining_body):
        value_str = match.group(1).strip()
        statement = match.group(2).strip()
        
        if value_str.lower() == 'default':
            default_item = statement
        else:
            case_items.append((value_str, statement))
    
    # Chuyển case thành MUX tree hoặc if-else chain
    # Đơn giản hóa: tạo MUX nodes cho mỗi case item
    # Trong thực tế, có thể tối ưu thành tree structure
    
    if not case_items and not default_item:
        return  # Empty case statement
    
    # Tạo intermediate signals cho mỗi case item
    # Format: case_sel_eq_value -> output_value
    mux_inputs = []
    mux_selects = []
    
    for idx, (value_str, statement) in enumerate(case_items):
        # Tạo comparison node: selector == value
        eq_signal = f"_case_eq_{idx}"
        
        # Parse value (có thể là số, binary, hex, range)
        value_expr = _parse_case_value(value_str, selector)
        
        # Tạo EQ node: selector == value_expr
        eq_node_id = node_builder.create_operation_node(
            node_type='EQ',
            operands=[selector, value_expr],
            extra_attrs={'case_item': value_str}
        )
        node_builder.create_buffer_node(eq_node_id, eq_signal)
        
        # Parse statement để lấy output value
        output_value = _extract_case_output(statement)
        mux_inputs.append(output_value)
        mux_selects.append(eq_signal)
    
    # Thêm default nếu có
    if default_item:
        default_output = _extract_case_output(default_item)
        mux_inputs.append(default_output)
        # Default được chọn khi không có case nào match
        # Tạo OR của tất cả các select signals, sau đó NOT
        if mux_selects:
            # Tạo OR node cho tất cả selects
            or_signal = f"_case_or_all"
            or_node_id = node_builder.create_operation_node(
                node_type='OR',
                operands=mux_selects,
                extra_attrs={'case_or': True}
            )
            node_builder.create_buffer_node(or_node_id, or_signal)
            
            # NOT để có default select
            default_select = f"_case_default_sel"
            not_node_id = node_builder.create_operation_node(
                node_type='NOT',
                operands=[or_signal],
                extra_attrs={'case_default': True}
            )
            node_builder.create_buffer_node(not_node_id, default_select)
            mux_selects.append(default_select)
        else:
            # Nếu không có case items, default luôn được chọn
            mux_selects.append("1'b1")  # Constant true
    
    # Tạo MUX tree (đơn giản: tạo MUX node cho mỗi level)
    # Hoặc có thể tạo một MUX lớn với nhiều inputs
    # Ở đây, tạo MUX node đơn giản
    if len(mux_inputs) > 0:
        # Tìm output signal từ case items (thường là signal đầu tiên được assign)
        output_signal = None
        for _, statement in case_items:
            output_signal = _extract_case_output_signal(statement)
            if output_signal:
                break
        if not output_signal and default_item:
            output_signal = _extract_case_output_signal(default_item)
        
        if output_signal:
            # Tạo MUX node với tất cả inputs và selects
            mux_node_id = node_builder.create_operation_node(
                node_type='MUX',
                operands=mux_inputs + mux_selects,
                extra_attrs={
                    'case_selector': selector,
                    'case_type': case_type,
                    'num_cases': len(case_items),
                    'has_default': default_item is not None
                }
            )
            # Kết nối với output signal
            node_builder.create_buffer_node(mux_node_id, output_signal)
        else:
            # Nếu không tìm thấy output signal, tạo signal tạm
            temp_output = f"_case_output_{node_builder.get_next_node_id()}"
            mux_node_id = node_builder.create_operation_node(
                node_type='MUX',
                operands=mux_inputs + mux_selects,
                extra_attrs={
                    'case_selector': selector,
                    'case_type': case_type,
                    'num_cases': len(case_items),
                    'has_default': default_item is not None
                }
            )
            node_builder.create_buffer_node(mux_node_id, temp_output)


def _parse_case_value(value_str: str, selector: str) -> str:
    """
    Parse case value string thành expression.
    
    Hỗ trợ:
    - Single value: 4'b1010, 8, 'hFF
    - Range: 4:7
    - Simple identifier: STATE_IDLE
    
    Args:
        value_str: Case value string
        selector: Selector signal (để tính width nếu cần)
        
    Returns:
        Expression string có thể dùng trong comparison
    """
    import re
    
    value_str = value_str.strip()
    
    # Default
    if value_str.lower() == 'default':
        return "1'b1"  # Always true
    
    # Range: 4:7
    range_match = re.match(r'(\d+)\s*:\s*(\d+)', value_str)
    if range_match:
        # Range được chuyển thành comparison: selector >= min && selector <= max
        min_val = range_match.group(1)
        max_val = range_match.group(2)
        # Trả về expression để so sánh sau
        return f"RANGE_{min_val}_{max_val}"  # Placeholder, sẽ xử lý trong comparison
    
    # Binary: 4'b1010
    if re.match(r'\d+\'[bB]', value_str):
        return value_str
    
    # Hex: 8'hFF
    if re.match(r'\d+\'[hH]', value_str):
        return value_str
    
    # Decimal: 8
    if re.match(r'^\d+$', value_str):
        return value_str
    
    # Identifier: STATE_IDLE
    return value_str


def _extract_case_output(statement: str) -> str:
    """
    Extract output expression từ case statement.
    
    Hỗ trợ:
    - assign out = value;
    - out = value;
    - Multiple statements (lấy statement đầu tiên)
    
    Args:
        statement: Case item statement
        
    Returns:
        Output expression (RHS của assignment)
    """
    import re
    
    statement = statement.strip()
    
    # Pattern: signal = expression
    assign_match = re.search(r'(\w+)\s*=\s*([^;]+)', statement)
    if assign_match:
        return assign_match.group(2).strip()
    
    # Pattern: assign signal = expression;
    assign_full_match = re.search(r'assign\s+(\w+)\s*=\s*([^;]+)', statement)
    if assign_full_match:
        return assign_full_match.group(2).strip()
    
    # Nếu không match, trả về statement như là expression
    return statement


def _extract_case_output_signal(statement: str) -> str:
    """
    Extract output signal name từ case statement.
    
    Args:
        statement: Case item statement
        
    Returns:
        Output signal name (LHS của assignment) hoặc None
    """
    import re
    
    statement = statement.strip()
    
    # Pattern: signal = expression
    assign_match = re.search(r'(\w+)\s*=\s*', statement)
    if assign_match:
        return assign_match.group(1).strip()
    
    # Pattern: assign signal = expression;
    assign_full_match = re.search(r'assign\s+(\w+)\s*=\s*', statement)
    if assign_full_match:
        return assign_full_match.group(1).strip()
    
    return None


# ============================================================================
# ASSIGN STATEMENTS PARSING
# ============================================================================

def _parse_assign_statements(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse tất cả assign statements.
    
    Assign statements có format:
        assign output = expression;
        
    Expression có thể là:
    - Arithmetic: a + b, a - b, a * b, a / b, a % b
    - Bitwise: a & b, a | b, a ^ b, ~a
    - Logical: a && b, a || b, !a
    - Comparison: a == b, a != b, a < b, a > b
    - Shift: a << 2, a >> 1
    - Special: cond ? a : b, {a, b}, a[3:0]
    - Simple: wire = signal
    """
    
    for match in ASSIGN_PATTERN.finditer(module_body):
        lhs, rhs = match.groups()
        lhs = lhs.strip()
        rhs = rhs.strip()
        
        # Dispatch đến parser thích hợp dựa trên operators
        # Lấy params từ netlist nếu có
        params = netlist.get('attrs', {}).get('parameters', {})
        # Convert string params to int nếu có thể
        int_params = {}
        for k, v in params.items():
            if isinstance(v, int):
                int_params[k] = v
            elif isinstance(v, str):
                try:
                    int_params[k] = _eval_int(v, {})
                except:
                    pass
        _dispatch_assign_parser(lhs, rhs, node_builder, int_params)


def _dispatch_assign_parser(lhs: str, rhs: str, node_builder: NodeBuilder, params: Dict[str, int] = None):
    """
    Dispatch assignment đến parser thích hợp.
    
    Kiểm tra operators theo thứ tự ưu tiên.
    """
    from ..operations.arithmetic import detect_arithmetic_operator
    from ..operations.bitwise import detect_bitwise_operator
    from ..operations.logical import detect_logical_operator
    from ..operations.comparison import detect_comparison_operator
    from ..operations.shift import detect_shift_operator
    
    # 1. Special operations (check trước vì phức tạp nhất)
    # Check replication trước concatenation (vì replication cũng dùng {})
    from ..operations.special import is_replication, parse_replication
    
    if is_replication(rhs):
        parse_replication(node_builder, lhs, rhs, params)
        return
    
    if is_ternary(rhs):
        parse_ternary_operation(node_builder, lhs, rhs)
        return
    
    if is_concatenation(rhs):
        parse_concatenation(node_builder, lhs, rhs, params)
        return
    
    if is_slice(rhs):
        parse_slice(node_builder, lhs, rhs, params)
        return
    
    # 2. Complex expressions với parentheses
    # Check trước các simple operators
    if '(' in rhs and ')' in rhs:
        # Có parentheses - có thể là complex expression
        # Check xem có nhiều operators không
        has_multiple_ops = sum([
            rhs.count('&'), rhs.count('|'), rhs.count('^'),
            rhs.count('+'), rhs.count('-')
        ]) > 1
        
        if has_multiple_ops:
            # Complex expression, dùng expression parser
            parse_complex_expression(node_builder, lhs, rhs)
            return
    
    # 3. Shift operations (check trước comparison vì >> có thể nhầm với >)
    shift_op = detect_shift_operator(rhs)
    if shift_op:
        from ..operations.shift import parse_shift_operation
        parse_shift_operation(node_builder, shift_op, lhs, rhs)
        return
    
    # 4. Comparison operations
    comp_op = detect_comparison_operator(rhs)
    if comp_op:
        from ..operations.comparison import parse_comparison_operation
        parse_comparison_operation(node_builder, comp_op, lhs, rhs)
        return
    
    # 5. Logical operations  
    logical_op = detect_logical_operator(rhs)
    if logical_op:
        from ..operations.logical import parse_logical_operation
        parse_logical_operation(node_builder, logical_op, lhs, rhs)
        return
    
    # 6. Bitwise operations
    bitwise_op = detect_bitwise_operator(rhs)
    if bitwise_op:
        from ..operations.bitwise import parse_bitwise_operation
        parse_bitwise_operation(node_builder, bitwise_op, lhs, rhs)
        return
    
    # 7. Arithmetic operations
    arith_op = detect_arithmetic_operator(rhs)
    if arith_op:
        from ..operations.arithmetic import parse_arithmetic_operation
        parse_arithmetic_operation(node_builder, arith_op, lhs, rhs)
        return
    
    # 8. Simple assignment (fallback)
    node_builder.create_simple_assignment(lhs, rhs)


# ============================================================================
# GATE & MODULE INSTANTIATIONS
# ============================================================================

def _parse_gate_instantiations(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """Parse gate instantiations (and, or, xor, etc.)."""
    
    for match in GATE_PATTERN.finditer(module_body):
        gate_type, inst_name, connections = match.groups()
        
        # Parse connections
        conns = [c.strip() for c in connections.split(',')]
        if len(conns) >= 2:
            output = conns[0]
            inputs = conns[1:]
            
            # Tạo gate node
            node_builder.create_gate_node(gate_type, inst_name, inputs, output)


def _parse_module_instantiations(netlist: Dict, module_body: str, node_builder: NodeBuilder):
    """
    Parse module instantiations với hỗ trợ đầy đủ như YosysHQ.
    
    Hỗ trợ:
    - Ordered ports: module_inst inst1 (a, b, c);
    - Named ports: module_inst inst1 (.port1(a), .port2(b));
    - Mixed: module_inst inst1 (a, .port2(b), c);
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        node_builder: NodeBuilder instance
    """
    from .constants import (
        MODULE_INST_PATTERN, NAMED_PORT_PATTERN, STANDARD_GATES
    )
    
    for match in MODULE_INST_PATTERN.finditer(module_body):
        module_type = match.group(1).strip()
        inst_name = match.group(2).strip() if match.group(2) else None
        port_list = match.group(3).strip() if match.group(3) else ""
        
        # Skip nếu là gate (đã được parse bởi _parse_gate_instantiations)
        if module_type.lower() in STANDARD_GATES:
            continue
        
        # Parse port connections
        connections = {}
        ordered_ports = []
        
        # Parse port connections - hỗ trợ named và ordered ports
        connections, ordered_ports, has_named_ports = _parse_port_connections(port_list)
        
        # Generate instance name nếu không có
        if not inst_name:
            instance_counter = len([k for k in netlist.get('attrs', {}).get('module_instantiations', {})])
            inst_name = f"{module_type}_inst_{instance_counter}"
        
        # Create module instance node
        module_id = node_builder.create_module_instance_node(
            module_type=module_type,
            inst_name=inst_name,
            connections=connections
        )
        
        # Store trong netlist attributes
        if 'module_instantiations' not in netlist['attrs']:
            netlist['attrs']['module_instantiations'] = {}
        
        netlist['attrs']['module_instantiations'][module_id] = {
            "module_type": module_type,
            "instance_name": inst_name,
            "connections": connections,
            "ordered_ports": ordered_ports if not has_named_ports else None,
            "has_named_ports": has_named_ports is not None
        }


# ============================================================================
# FUNCTIONS & TASKS PARSING
# ============================================================================

def _parse_functions(netlist: Dict, module_body: str, params: Dict[str, int] = None):
    """
    Parse function declarations.
    
    Hỗ trợ:
    - function [width-1:0] func_name; ... endfunction
    - function signed [7:0] func_name; ... endfunction
    - function automatic func_name; ... endfunction
    - Parameterized widths: function [WIDTH-1:0] func_name; ... endfunction
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
        params: Dictionary chứa parameter values
    """
    from .constants import FUNCTION_PATTERN, SIGNED_KEYWORD
    from .tokenizer import calculate_vector_width
    
    params = params or {}
    
    if 'functions' not in netlist['attrs']:
        netlist['attrs']['functions'] = {}
    
    for match in FUNCTION_PATTERN.finditer(module_body):
        width_msb = match.group(1)
        width_lsb = match.group(2)
        func_name = match.group(3).strip()
        func_body = match.group(0)
        
        # Parse function body (giữa function ... ; và endfunction)
        func_decl_end = func_body.find(';')
        func_body_start = func_decl_end + 1 if func_decl_end >= 0 else 0
        func_body_end = func_body.rfind('endfunction')
        func_content = func_body[func_body_start:func_body_end].strip() if func_body_end > func_body_start else ""
        
        # Tính width nếu có
        width = 1  # Default cho scalar
        is_signed = bool(SIGNED_KEYWORD.search(func_body))
        
        if width_msb and width_lsb:
            width = calculate_vector_width(width_msb, width_lsb, params)
        
        # Lưu function information
        netlist['attrs']['functions'][func_name] = {
            'width': width,
            'width_msb': width_msb,
            'width_lsb': width_lsb,
            'signed': is_signed,
            'body': func_content,
            'full_declaration': func_body
        }


def _parse_tasks(netlist: Dict, module_body: str):
    """
    Parse task declarations.
    
    Hỗ trợ:
    - task task_name; ... endtask
    - task automatic task_name; ... endtask
    
    Args:
        netlist: Netlist dictionary
        module_body: Module body content
    """
    from .constants import TASK_PATTERN
    
    if 'tasks' not in netlist['attrs']:
        netlist['attrs']['tasks'] = {}
    
    for match in TASK_PATTERN.finditer(module_body):
        task_name = match.group(1).strip()
        task_body = match.group(0)
        
        # Parse task body (giữa task ... ; và endtask)
        task_decl_end = task_body.find(';')
        task_body_start = task_decl_end + 1 if task_decl_end >= 0 else 0
        task_body_end = task_body.rfind('endtask')
        task_content = task_body[task_body_start:task_body_end].strip() if task_body_end > task_body_start else ""
        
        # Lưu task information
        netlist['attrs']['tasks'][task_name] = {
            'body': task_content,
            'full_declaration': task_body
        }


# ============================================================================
# PORT CONNECTION PARSING (HELPER)
# ============================================================================

def _parse_port_connections(port_list: str) -> tuple:
    """
    Parse port connections từ port list string.
    
    Hỗ trợ:
    - Named ports: .port_name(signal), .port_name({a, b}), .port_name(a + b)
    - Ordered ports: signal1, signal2, {a, b}
    - Mixed: signal1, .port_name(signal2), signal3
    
    Args:
        port_list: Port list string (ví dụ: "a, b, c" hoặc ".clk(clk), .rst(rst)")
        
    Returns:
        Tuple (connections_dict, ordered_ports_list, has_named_ports_bool)
    """
    from .constants import NAMED_PORT_PATTERN
    import re
    
    connections = {}
    ordered_ports = []
    has_named_ports = False
    
    if not port_list or not port_list.strip():
        return connections, ordered_ports, has_named_ports
    
    # Parse named ports trước (vì dễ nhận diện với .port_name(...))
    named_port_matches = list(NAMED_PORT_PATTERN.finditer(port_list))
    has_named_ports = len(named_port_matches) > 0
    
    if has_named_ports:
        # Parse named ports
        for port_match in named_port_matches:
            port_name = port_match.group(1).strip()
            # Port connection có thể là expression phức tạp
            port_connection = port_match.group(2).strip()
            connections[port_name] = port_connection
        
        # Parse ordered ports (nếu có - mixed mode)
        # Loại bỏ named ports từ port_list
        remaining = port_list
        for port_match in reversed(named_port_matches):  # Reverse để giữ indices
            remaining = remaining[:port_match.start()] + remaining[port_match.end():]
        
        # Parse ordered ports từ remaining
        # Cần xử lý cẩn thận để không split bên trong parentheses/braces
        ordered_ports = _parse_ordered_ports(remaining)
    else:
        # Chỉ có ordered ports
        ordered_ports = _parse_ordered_ports(port_list)
        # Create connections với index-based keys
        for i, signal in enumerate(ordered_ports):
            connections[f'port_{i}'] = signal
    
    return connections, ordered_ports, has_named_ports


def _parse_ordered_ports(port_list: str) -> list:
    """
    Parse ordered ports từ port list string.
    
    Hỗ trợ expressions phức tạp: signal, {a, b}, signal[7:0], a + b
    
    Args:
        port_list: Port list string (ví dụ: "a, b, {c, d}")
        
    Returns:
        List of port connection strings
    """
    import re
    
    if not port_list or not port_list.strip():
        return []
    
    ports = []
    i = 0
    current_port = ""
    paren_depth = 0
    brace_depth = 0
    bracket_depth = 0
    
    while i < len(port_list):
        char = port_list[i]
        
        if char == '(':
            paren_depth += 1
            current_port += char
        elif char == ')':
            paren_depth -= 1
            current_port += char
        elif char == '{':
            brace_depth += 1
            current_port += char
        elif char == '}':
            brace_depth -= 1
            current_port += char
        elif char == '[':
            bracket_depth += 1
            current_port += char
        elif char == ']':
            bracket_depth -= 1
            current_port += char
        elif char == ',':
            # Chỉ split nếu không nằm trong parentheses/braces/brackets
            if paren_depth == 0 and brace_depth == 0 and bracket_depth == 0:
                port = current_port.strip()
                if port:
                    ports.append(port)
                current_port = ""
            else:
                current_port += char
        else:
            current_port += char
        
        i += 1
    
    # Thêm port cuối cùng
    if current_port.strip():
        ports.append(current_port.strip())
    
    return ports


# ============================================================================
# STATISTICS & FINALIZATION
# ============================================================================

def _compute_statistics(netlist: Dict):
    """Tính toán statistics cho netlist."""
    nodes = netlist.get('nodes', [])
    
    # Count node types
    type_counts = {}
    for node in nodes:
        node_type = node.get('type', 'UNKNOWN')
        type_counts[node_type] = type_counts.get(node_type, 0) + 1
    
    # Group by categories
    category_counts = {cat: 0 for cat in NODE_CATEGORIES}
    for node_type, count in type_counts.items():
        for category, members in NODE_CATEGORIES.items():
            if node_type in members:
                category_counts[category] += count
    
    # Store statistics
    netlist['attrs']['operator_summary'] = {
        'type_counts': type_counts,
        'category_counts': category_counts,
        'total_nodes': len(nodes)
    }
    
    # Mirror to parsing_stats
    stats = netlist['attrs'].setdefault('parsing_stats', {})
    stats.update({
        'total_nodes': len(nodes),
        'logic_nodes': category_counts['logic'],
        'arith_nodes': category_counts['arith'],
        'shift_nodes': category_counts['shift'],
        'compare_nodes': category_counts['compare'],
        'logical_nodes': category_counts['logical'],
        'struct_nodes': category_counts['struct']
    })


def _ensure_output_mapping(netlist: Dict):
    """Ensure mọi output đều có mapping."""
    out_map = netlist['attrs'].setdefault('output_mapping', {})
    
    for node in netlist.get('nodes', []):
        node_id = node.get('id')
        if not node_id:
            continue
        
        # Bind output name to node if matching
        for out_name in netlist.get('outputs', []):
            if out_name not in out_map and out_name == node_id:
                out_map[out_name] = node_id

