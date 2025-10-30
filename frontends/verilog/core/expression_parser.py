"""
Expression Parser - Parse biểu thức phức tạp với parentheses

Module này xử lý các expressions phức tạp có:
- Parentheses lồng nhau: ((a & b) | c)
- Multiple operators: (a & b) | (c & d)
- Nested expressions: (a & (b | c))

Thuật toán:
1. Tìm operators chính (ngoài parentheses)
2. Split expression theo precedence
3. Recursively parse sub-expressions
4. Tái sử dụng operation parsers cho simple expressions
5. Build tree of nodes

REFACTORED: Module này BÂY GIỜ TÁI SỬ DỤNG các parsers từ operations/
để giảm code duplication và dễ maintain hơn.
"""

from typing import Dict, List, Tuple, Optional
from .node_builder import NodeBuilder

# Import operation parsers để tái sử dụng
from ..operations.bitwise import parse_bitwise_operation
from ..operations.logical import parse_logical_operation
from ..operations.arithmetic import parse_arithmetic_operation


class ExpressionParser:
    """
    Parser cho biểu thức phức tạp.
    
    Xử lý:
    - Parentheses matching
    - Operator precedence
    - Nested expressions
    """
    
    def __init__(self, node_builder: NodeBuilder):
        """
        Khởi tạo expression parser.
        
        Args:
            node_builder: NodeBuilder để tạo nodes
        """
        self.node_builder = node_builder
        
        # Operator precedence (thấp đến cao)
        # Precedence thấp hơn = parse sau
        self.precedence = {
            '||': 1,   # Logical OR
            '|': 2,    # Bitwise OR
            '^': 3,    # XOR
            '&': 4,    # Bitwise AND
            '&&': 5,   # Logical AND
        }
    
    def parse_complex_expression(
        self,
        expression: str,
        output_signal: str
    ) -> str:
        """
        Parse complex expression và tạo nodes.
        
        Args:
            expression: Expression cần parse
            output_signal: Output signal name
            
        Returns:
            Node ID của kết quả cuối cùng
        """
        # Loại bỏ spaces thừa
        expr = expression.strip()
        
        # Loại bỏ outer parentheses nếu có
        expr = self._remove_outer_parens(expr)
        
        # Tìm main operator (operator ngoài cùng với precedence thấp nhất)
        main_op, pos = self._find_main_operator(expr)
        
        if main_op is None:
            # Không có operator, đây là simple signal
            return self.node_builder.create_simple_assignment(output_signal, expr)
        
        # Split expression bởi main operator
        left_expr = expr[:pos].strip()
        right_expr = expr[pos + len(main_op):].strip()
        
        # Recursively parse left và right
        left_node = self._parse_sub_expression(left_expr)
        right_node = self._parse_sub_expression(right_expr)
        
        # Tạo node cho main operator
        node_type = self._operator_to_type(main_op)
        op_node_id = self.node_builder.create_operation_node(
            node_type=node_type,
            operands=[left_node, right_node]
        )
        
        # Tạo buffer node cho output
        buf_id = self.node_builder.create_buffer_node(op_node_id, output_signal)
        
        return buf_id
    
    def _parse_sub_expression(self, expr: str) -> str:
        """
        Parse sub-expression (không tạo output buffer).
        
        Strategy:
        1. Check xem có phải simple expression không (1 operator, no parens)
        2. Nếu simple → TÁI SỬ DỤNG operation parsers
        3. Nếu complex → Parse recursively
        
        Args:
            expr: Sub-expression
            
        Returns:
            Node ID của sub-expression result
        """
        expr = expr.strip()
        expr = self._remove_outer_parens(expr)
        
        # Tìm main operator trong sub-expression
        main_op, pos = self._find_main_operator(expr)
        
        if main_op is None:
            # Simple signal, return as-is
            return expr
        
        # Check xem có phải simple expression không (no nested parens)
        is_simple = '(' not in expr or expr.count('(') == 0
        
        if is_simple:
            # Simple expression → TÁI SỬ DỤNG operation parser
            return self._parse_simple_sub_expression(expr, main_op)
        
        # Complex expression → Parse recursively
        left_expr = expr[:pos].strip()
        right_expr = expr[pos + len(main_op):].strip()
        
        left_node = self._parse_sub_expression(left_expr)
        right_node = self._parse_sub_expression(right_expr)
        
        # Tạo node cho operator
        node_type = self._operator_to_type(main_op)
        op_node_id = self.node_builder.create_operation_node(
            node_type=node_type,
            operands=[left_node, right_node]
        )
        
        return op_node_id
    
    def _parse_simple_sub_expression(self, expr: str, operator: str) -> str:
        """
        Parse simple sub-expression bằng cách TÁI SỬ DỤNG operation parsers.
        
        Điều này GIẢM CODE DUPLICATION và dễ maintain hơn.
        
        Args:
            expr: Simple expression (e.g., "a & b")
            operator: Operator đã tìm thấy
            
        Returns:
            Node ID của operation node (không có buffer)
        """
        # Tạo temporary output name
        temp_output = f"_temp_{self.node_builder.node_counter}"
        
        # Dispatch đến appropriate parser dựa trên operator
        if operator in ['&', '|', '^', '~&', '~|', '~^', '^~']:
            # Bitwise operation → TÁI SỬ DỤNG bitwise parser
            parse_bitwise_operation(self.node_builder, operator, temp_output, expr)
            # Return operation node (không phải buffer)
            # Operation node là node thứ 2 từ cuối (buffer là cuối cùng)
            nodes = self.node_builder.get_nodes()
            if len(nodes) >= 2:
                return nodes[-2]['id']  # Operation node
            return temp_output
            
        elif operator in ['&&', '||']:
            # Logical operation → TÁI SỬ DỤNG logical parser
            parse_logical_operation(self.node_builder, operator, temp_output, expr)
            nodes = self.node_builder.get_nodes()
            if len(nodes) >= 2:
                return nodes[-2]['id']
            return temp_output
            
        elif operator in ['+', '-', '*', '/', '%']:
            # Arithmetic operation → TÁI SỬ DỤNG arithmetic parser
            parse_arithmetic_operation(self.node_builder, operator, temp_output, expr)
            nodes = self.node_builder.get_nodes()
            if len(nodes) >= 2:
                return nodes[-2]['id']
            return temp_output
        
        else:
            # Fallback: tạo node trực tiếp
            node_type = self._operator_to_type(operator)
            left_expr = expr[:expr.find(operator)].strip()
            right_expr = expr[expr.find(operator) + len(operator):].strip()
            
            return self.node_builder.create_operation_node(
                node_type=node_type,
                operands=[left_expr, right_expr]
            )
    
    def _find_main_operator(self, expr: str) -> Tuple[Optional[str], int]:
        """
        Tìm main operator trong expression.
        
        Main operator là operator có:
        1. Precedence thấp nhất
        2. Nằm ngoài tất cả parentheses
        
        Args:
            expr: Expression cần tìm
            
        Returns:
            (operator, position) hoặc (None, -1) nếu không tìm thấy
        """
        paren_depth = 0
        operators_found = []  # (operator, position, precedence)
        
        i = 0
        while i < len(expr):
            char = expr[i]
            
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif paren_depth == 0:
                # Check for operators (chỉ ở ngoài parentheses)
                # Check multi-char operators first
                for op in ['||', '&&', '~&', '~|', '~^', '^~']:
                    if expr[i:i+len(op)] == op:
                        prec = self.precedence.get(op, 999)
                        operators_found.append((op, i, prec))
                        i += len(op) - 1
                        break
                else:
                    # Check single-char operators
                    if char in ['|', '&', '^']:
                        op = char
                        prec = self.precedence.get(op, 999)
                        operators_found.append((op, i, prec))
            
            i += 1
        
        # Tìm operator với precedence thấp nhất (sẽ parse cuối cùng)
        if not operators_found:
            return (None, -1)
        
        # Sort by precedence (thấp nhất trước)
        operators_found.sort(key=lambda x: x[2])
        
        # Return operator đầu tiên (precedence thấp nhất)
        op, pos, _ = operators_found[0]
        return (op, pos)
    
    def _remove_outer_parens(self, expr: str) -> str:
        """
        Loại bỏ outer parentheses nếu chúng bao toàn bộ expression.
        
        Example:
            "(a & b)" -> "a & b"
            "((a | b))" -> "a | b"
            "(a) & (b)" -> "(a) & (b)" (không loại bỏ)
        
        Args:
            expr: Expression
            
        Returns:
            Expression đã loại bỏ outer parens
        """
        expr = expr.strip()
        
        while expr.startswith('(') and expr.endswith(')'):
            # Check xem có phải outer parens không
            # bằng cách check matching
            paren_depth = 0
            is_outer = True
            
            for i, char in enumerate(expr[1:-1], 1):
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                    if paren_depth < 0:
                        # Closing paren trước opening paren của outer
                        is_outer = False
                        break
            
            if is_outer and paren_depth == 0:
                # Đây là outer parens, loại bỏ
                expr = expr[1:-1].strip()
            else:
                break
        
        return expr
    
    def _operator_to_type(self, operator: str) -> str:
        """
        Map operator string sang node type.
        
        Args:
            operator: Operator string
            
        Returns:
            Node type string
        """
        op_map = {
            '&': 'AND',
            '|': 'OR',
            '^': 'XOR',
            '~&': 'NAND',
            '~|': 'NOR',
            '~^': 'XNOR',
            '^~': 'XNOR',
            '&&': 'LAND',
            '||': 'LOR',
        }
        
        return op_map.get(operator, 'UNKNOWN')


def parse_complex_expression(
    node_builder: NodeBuilder,
    lhs: str,
    rhs: str
) -> None:
    """
    Parse complex expression với parentheses.
    
    Wrapper function để dùng từ parser.py.
    
    Args:
        node_builder: NodeBuilder instance
        lhs: Output signal
        rhs: Complex expression
    """
    parser = ExpressionParser(node_builder)
    parser.parse_complex_expression(rhs, lhs)

