"""
Node Builder - Tạo nodes và wire connections

Module này chịu trách nhiệm:
1. Tạo operation nodes (ADD, AND, OR, etc.)
2. Tạo buffer nodes cho outputs
3. Generate wire connections giữa các nodes
4. Maintain node counter
5. Update output mapping

Thiết kế:
- Sử dụng Builder pattern để tạo nodes
- Tự động track node IDs
- Centralize logic tạo nodes để giảm code duplication
"""

from typing import Dict, List, Optional, Tuple, Any


class NodeBuilder:
    """
    Builder class để tạo nodes cho netlist.
    
    Chức năng:
    - Tự động generate unique node IDs
    - Tạo operation nodes
    - Tạo buffer nodes
    - Update output mappings
    - Track statistics
    """
    
    def __init__(self):
        """Khởi tạo NodeBuilder với counter = 0."""
        self.node_counter = 0
        self.nodes: List[Dict] = []
        self.output_mapping: Dict[str, str] = {}
        
    def create_operation_node(
        self,
        node_type: str,
        operands: List[str],
        output_signal: Optional[str] = None,
        extra_attrs: Optional[Dict] = None
    ) -> str:
        """
        Tạo một operation node (ADD, AND, OR, XOR, etc.).
        
        Args:
            node_type: Loại node (ADD, AND, OR, etc.)
            operands: List các operands (inputs)
            output_signal: Tên signal output (nếu có)
            extra_attrs: Attributes bổ sung cho node
            
        Returns:
            Node ID của operation node đã tạo
        """
        # Generate node ID
        node_id = f"{node_type.lower()}_{self.node_counter}"
        self.node_counter += 1
        
        # Tạo node dictionary
        node = {
            "id": node_id,
            "type": node_type,
            "fanins": [[op, False] for op in operands]
        }
        
        # Thêm extra attributes nếu có
        if extra_attrs:
            node.update(extra_attrs)
        
        # Thêm vào danh sách nodes
        self.nodes.append(node)
        
        return node_id
    
    def create_buffer_node(
        self,
        input_signal: str,
        output_signal: str
    ) -> str:
        """
        Tạo một buffer node (BUF).
        
        Buffer nodes được dùng để:
        - Connect operation node với output
        - Isolate signals
        - Maintain signal integrity
        
        Args:
            input_signal: Input signal (thường là output của operation node)
            output_signal: Output signal name
            
        Returns:
            Node ID của buffer node đã tạo
        """
        # Generate buffer ID
        buf_id = f"buf_{self.node_counter}"
        self.node_counter += 1
        
        # Tạo buffer node
        buf_node = {
            "id": buf_id,
            "type": "BUF",
            "fanins": [[input_signal, False]]
        }
        
        # Thêm vào danh sách nodes
        self.nodes.append(buf_node)
        
        # Update output mapping
        self.output_mapping[output_signal] = buf_id
        
        return buf_id
    
    def create_operation_with_buffer(
        self,
        node_type: str,
        operands: List[str],
        output_signal: str,
        extra_attrs: Optional[Dict] = None
    ) -> Tuple[str, str]:
        """
        Tạo operation node + buffer node (pattern phổ biến).
        
        DEPRECATED: Sử dụng create_operation_direct() thay vì function này.
        Giữ lại để backward compatibility.
        
        Args:
            node_type: Loại operation (ADD, AND, OR, etc.)
            operands: List operands
            output_signal: Tên output signal
            extra_attrs: Extra attributes cho operation node
            
        Returns:
            Tuple (operation_node_id, buffer_node_id)
        """
        # Tạo operation node trực tiếp (không qua BUF)
        op_node_id = self.create_operation_direct(
            node_type, operands, output_signal, extra_attrs
        )
        
        # Không tạo BUF node nữa - trả về operation node ID cho cả hai
        # (để backward compatible với code cũ đang expect 2 return values)
        return (op_node_id, op_node_id)
    
    def create_operation_direct(
        self,
        node_type: str,
        operands: List[str],
        output_signal: str,
        extra_attrs: Optional[Dict] = None
    ) -> str:
        """
        Tạo operation node trực tiếp, KHÔNG tạo BUF node.
        
        Đây là cách đúng đắn hơn - không tạo BUF nodes không cần thiết.
        Strash sẽ tự động optimize nếu cần.
        
        Args:
            node_type: Loại operation (ADD, AND, OR, etc.)
            operands: List operands
            output_signal: Tên output signal
            extra_attrs: Extra attributes cho operation node
            
        Returns:
            Operation node ID
        """
        # Tạo operation node
        op_node_id = self.create_operation_node(
            node_type, operands, output_signal, extra_attrs
        )
        
        # Update output mapping trực tiếp đến operation node (không qua BUF)
        if output_signal:
            self.output_mapping[output_signal] = op_node_id
        
        return op_node_id
    
    def create_simple_assignment(self, lhs: str, rhs: str) -> str:
        """
        Tạo simple assignment (wire = signal).
        
        Chỉ cần 1 buffer node.
        
        Args:
            lhs: Left-hand side (output signal)
            rhs: Right-hand side (input signal)
            
        Returns:
            Buffer node ID
        """
        return self.create_buffer_node(rhs.strip(), lhs)
    
    def create_gate_node(
        self,
        gate_type: str,
        inst_name: str,
        inputs: List[str],
        output: str
    ) -> str:
        """
        Tạo gate instantiation node.
        
        Example Verilog:
            and u1 (out, a, b);
            
        Args:
            gate_type: Loại gate (and, or, xor, etc.)
            inst_name: Instance name (u1, u2, etc.)
            inputs: List input signals
            output: Output signal
            
        Returns:
            Gate node ID
        """
        # Sử dụng inst_name nếu có, không thì generate
        gate_id = inst_name if inst_name else f"{gate_type}_{self.node_counter}"
        self.node_counter += 1
        
        # Tạo gate node
        gate_node = {
            "id": gate_id,
            "type": gate_type.upper(),
            "fanins": [[inp, False] for inp in inputs]
        }
        
        # Thêm vào nodes
        self.nodes.append(gate_node)
        
        # Update output mapping
        self.output_mapping[output] = gate_id
        
        return gate_id
    
    def create_module_instance_node(
        self,
        module_type: str,
        inst_name: str,
        connections: List[str]
    ) -> str:
        """
        Tạo module instantiation node.
        
        Example Verilog:
            full_adder fa1 (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));
            
        Args:
            module_type: Loại module (full_adder, etc.)
            inst_name: Instance name (fa1, etc.)
            connections: List connections
            
        Returns:
            Module instance node ID
        """
        # Sử dụng inst_name
        module_id = inst_name if inst_name else f"{module_type}_{self.node_counter}"
        self.node_counter += 1
        
        # Tạo module node
        module_node = {
            "id": module_id,
            "type": "MODULE",
            "module_type": module_type,
            "connections": connections,
            "fanins": []  # Will be populated based on connections
        }
        
        # Thêm vào nodes
        self.nodes.append(module_node)
        
        return module_id
    
    def get_nodes(self) -> List[Dict]:
        """Lấy tất cả nodes đã tạo."""
        return self.nodes
    
    def get_output_mapping(self) -> Dict[str, str]:
        """Lấy output mapping."""
        return self.output_mapping
    
    def get_node_count(self) -> int:
        """Lấy số lượng nodes đã tạo."""
        return len(self.nodes)
    
    def reset(self):
        """Reset builder về trạng thái ban đầu."""
        self.node_counter = 0
        self.nodes = []
        self.output_mapping = {}


class WireGenerator:
    """
    Generator để tạo wire connections giữa các nodes.
    
    Wire connections được tạo dựa trên fanins của nodes.
    """
    
    @staticmethod
    def generate_wires(nodes: List[Dict]) -> List[Dict]:
        """
        Generate wire connections từ node fanins.
        
        Mỗi fanin connection tạo ra một wire:
        - source: fanin signal
        - destination: node ID
        
        Args:
            nodes: List các nodes
            
        Returns:
            List các wire dictionaries
        """
        wires = []
        wire_counter = 0
        
        for node in nodes:
            node_id = node.get('id', '')
            fanins = node.get('fanins', [])
            
            for fanin in fanins:
                if len(fanin) >= 1:
                    source = fanin[0]
                    destination = node_id
                    
                    # Tạo wire connection
                    wire = {
                        "id": f"wire_{wire_counter}",
                        "source": source,
                        "destination": destination,
                        "type": "connection"
                    }
                    
                    wires.append(wire)
                    wire_counter += 1
        
        return wires
    
    @staticmethod
    def add_wire_statistics(netlist: Dict, wires: List[Dict]) -> Dict:
        """
        Thêm wire statistics vào netlist.
        
        Args:
            netlist: Netlist dictionary
            wires: List wires
            
        Returns:
            Netlist với statistics đã update
        """
        if 'parsing_stats' not in netlist.get('attrs', {}):
            netlist.setdefault('attrs', {})['parsing_stats'] = {}
        
        netlist['attrs']['parsing_stats']['total_wires'] = len(wires)
        netlist['attrs']['parsing_stats']['wire_generation'] = 'automatic'
        
        return netlist

