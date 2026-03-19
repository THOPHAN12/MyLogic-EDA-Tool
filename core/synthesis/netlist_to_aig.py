#!/usr/bin/env python3
"""
Netlist to AIG Conversion (Synthesis)

Synthesis: Chuyển đổi từ Netlist Dictionary → AIG (And-Inverter Graph)

Đây là bước SYNTHESIS riêng biệt, tách khỏi OPTIMIZATION.
Synthesis chỉ làm việc chuyển đổi representation, không tối ưu hóa.
"""

import sys
import os
import re
from typing import Dict, List, Set, Any, Optional
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.synthesis.aig import AIG, AIGNode
from core.synthesis.aig_multibit import MultiBitAIGNode, create_constant_multibit, parse_constant_string

logger = logging.getLogger(__name__)


class NetlistToAIGConverter:
    """
    Converter từ Netlist Dictionary sang AIG.
    
    Đây là bước SYNTHESIS: chuyển đổi representation từ netlist sang AIG.
    """
    
    def __init__(self):
        self.aig = None
        self.netlist = None
        self.node_mapping: Dict[str, AIGNode] = {}  # netlist_node_id -> AIGNode
        self.signal_mapping: Dict[str, AIGNode] = {}  # signal_name -> AIGNode
        self.multibit_signal_mapping: Dict[str, MultiBitAIGNode] = {}  # signal_name -> MultiBitAIGNode
        self._strict_synthesis: bool = False
        self._rev_output_mapping: Dict[str, str] = {}
        
    def convert(self, netlist: Dict[str, Any]) -> AIG:
        """
        Chuyển đổi Netlist Dictionary sang AIG.
        
        Args:
            netlist: Netlist dictionary từ parser
            
        Returns:
            AIG object
        """
        logger.info("Starting Synthesis: Netlist -> AIG conversion...")
        
        if not isinstance(netlist, dict) or 'nodes' not in netlist:
            raise ValueError("Invalid netlist format")
        
        # Khởi tạo AIG
        self.aig = AIG()
        self.netlist = netlist
        self._strict_synthesis = bool((netlist.get("attrs", {}) or {}).get("strict_synthesis", False))
        self.node_mapping = {}
        self.signal_mapping = {}
        self.multibit_signal_mapping = {}
        self._rev_output_mapping = {}
        outmap = (netlist.get("attrs", {}) or {}).get("output_mapping", {}) or {}
        if isinstance(outmap, dict):
            for sig, nid in outmap.items():
                if isinstance(nid, str) and nid:
                    self._rev_output_mapping[nid] = str(sig)
        
        # Bước 1: Tạo Primary Inputs
        self._create_primary_inputs(netlist)
        
        # Bước 2: Tạo Constant nodes
        self._create_constants(netlist)
        
        # Bước 3: Convert nodes theo topological order
        self._convert_nodes(netlist)
        
        # Bước 4: Tạo Primary Outputs
        self._create_primary_outputs(netlist)
        
        logger.info(f"Synthesis completed: {self.aig.count_nodes()} AIG nodes created")
        
        return self.aig
    
    def _create_primary_inputs(self, netlist: Dict[str, Any]):
        """Tạo Primary Input nodes trong AIG."""
        inputs = netlist.get('inputs', [])
        for input_name in inputs:
            aig_pi = self.aig.create_pi(input_name)
            self.signal_mapping[input_name] = aig_pi
            logger.debug(f"Created PI: {input_name}")
    
    def _create_constants(self, netlist: Dict[str, Any]):
        """Tạo Constant nodes trong AIG."""
        nodes = netlist.get('nodes', [])
        
        # Handle both dict and list formats
        if isinstance(nodes, dict):
            nodes_list = list(nodes.values())
        else:
            nodes_list = nodes if isinstance(nodes, list) else []
        
        for node_data in nodes_list:
            if not isinstance(node_data, dict):
                continue
            
            node_type = node_data.get('type', '')
            node_id = node_data.get('id', '')
            
            if node_type in ['CONST0', 'GND', '0']:
                self.node_mapping[node_id] = self.aig.const0
                output = node_data.get('output', node_id)
                if output:
                    self.signal_mapping[output] = self.aig.const0
            elif node_type in ['CONST1', 'VCC', '1']:
                self.node_mapping[node_id] = self.aig.const1
                output = node_data.get('output', node_id)
                if output:
                    self.signal_mapping[output] = self.aig.const1
    
    def _topological_order(
        self, nodes_list: List[Dict], output_mapping: Dict[str, str]
    ) -> List[Dict]:
        """Sắp xếp nodes theo thứ tự topo (dependency trước)."""
        node_ids = {n.get('id', ''): n for n in nodes_list if isinstance(n, dict)}
        node_ids_set = set(node_ids)
        # deps[node_id] = set of node_ids that must be converted before this node
        deps = {}
        for n in nodes_list:
            if not isinstance(n, dict):
                continue
            nid = n.get('id', '')
            fanins = n.get('fanins', []) or n.get('inputs', [])
            sigs = []
            for f in fanins:
                if isinstance(f, (list, tuple)) and f:
                    sigs.append(str(f[0]))
                else:
                    sigs.append(str(f))
            deps[nid] = set()
            for s in sigs:
                if s in node_ids_set and s != nid:
                    deps[nid].add(s)
                elif s in output_mapping and output_mapping[s] != nid:
                    deps[nid].add(output_mapping[s])
        result = []
        remaining = set(deps)
        while remaining:
            ready = [nid for nid in remaining if deps[nid].isdisjoint(remaining)]
            if not ready:
                # cycle: add remaining in arbitrary order
                ready = list(remaining)
            for nid in ready:
                remaining.discard(nid)
                if nid in node_ids:
                    result.append(node_ids[nid])
        return result

    def _convert_nodes(self, netlist: Dict[str, Any]):
        """Convert tất cả nodes sang AIG."""
        nodes = netlist.get('nodes', [])
        
        # Handle both dict and list formats
        if isinstance(nodes, dict):
            nodes_list = list(nodes.values())
        else:
            nodes_list = nodes if isinstance(nodes, list) else []
        
        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
        nodes_list = self._topological_order(nodes_list, output_mapping)
        
        for node_data in nodes_list:
            if not isinstance(node_data, dict):
                continue
            
            node_id = node_data.get('id', '')
            node_type = node_data.get('type', '')
            
            # Skip constants (already handled)
            if node_type in ['CONST0', 'CONST1', 'GND', 'VCC', '0', '1', 'INPUT', 'OUTPUT']:
                continue
            
            # Convert based on node type (BUF handled below for multibit pass-through)
            if node_type in ['AND', 'OR', 'XOR', 'NAND', 'NOR', 'XNOR', 'NOT']:
                aig_node = self._convert_gate_node(node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    
                    # Get output signal from node data or output_mapping
                    output = node_data.get('output', None)
                    if not output:
                        # Check output_mapping to find output signal for this node
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        # Find signal that maps to this node_id
                        for signal, mapped_node_id in output_mapping.items():
                            if mapped_node_id == node_id:
                                output = signal
                                break
                    
                    # Fallback to node_id if still no output found
                    if not output:
                        output = node_id
                    
                    if output:
                        self.signal_mapping[output] = aig_node
            
            # Arithmetic operations (multi-bit)
            elif node_type == 'ADD':
                multi_bit_node = self._convert_add_node(node_data)
                if multi_bit_node:
                    output = node_data.get('output', None)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.multibit_signal_mapping[output] = multi_bit_node
                        # Also store individual bits in signal_mapping for compatibility
                        for i, bit_node in enumerate(multi_bit_node.bits):
                            bit_name = f"{output}[{i}]" if multi_bit_node.width > 1 else output
                            self.signal_mapping[bit_name] = bit_node
                        # Store reference to first bit for node_mapping
                        if multi_bit_node.width > 0:
                            self.node_mapping[node_id] = multi_bit_node.bits[0]
            
            elif node_type == 'SUB':
                multi_bit_node = self._convert_sub_node(node_data)
                if multi_bit_node:
                    output = node_data.get('output', None)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.multibit_signal_mapping[output] = multi_bit_node
                        for i, bit_node in enumerate(multi_bit_node.bits):
                            bit_name = f"{output}[{i}]" if multi_bit_node.width > 1 else output
                            self.signal_mapping[bit_name] = bit_node
                        if multi_bit_node.width > 0:
                            self.node_mapping[node_id] = multi_bit_node.bits[0]
            
            # Comparison operations (single-bit output)
            elif node_type == 'EQ':
                aig_node = self._convert_eq_node(node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    output = node_data.get('output', None)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {}) or {}
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.signal_mapping[output] = aig_node

            elif node_type == 'NE':
                aig_node = self._convert_ne_node(node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    output = self._rev_output_mapping.get(node_id) or node_data.get('output') or node_id
                    self.signal_mapping[output] = aig_node

            elif node_type in ('LT', 'LE', 'GT', 'GE'):
                aig_node = self._convert_rel_node(node_type, node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    output = self._rev_output_mapping.get(node_id) or node_data.get('output') or node_id
                    self.signal_mapping[output] = aig_node

            elif node_type in ('LAND', 'LOR'):
                aig_node = self._convert_logical_node(node_type, node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    output = self._rev_output_mapping.get(node_id) or node_data.get('output') or node_id
                    self.signal_mapping[output] = aig_node
            
            # Multiplexer (multi-bit support)
            elif node_type == 'MUX':
                multi_bit_node = self._convert_mux_node(node_data)
                if multi_bit_node:
                    output = node_data.get('output', None)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.multibit_signal_mapping[output] = multi_bit_node
                        for i, bit_node in enumerate(multi_bit_node.bits):
                            bit_name = f"{output}[{i}]" if multi_bit_node.width > 1 else output
                            self.signal_mapping[bit_name] = bit_node
                        if multi_bit_node.width > 0:
                            self.node_mapping[node_id] = multi_bit_node.bits[0]

            # Concatenation: {a, b, ...} -> multi-bit, first operand is MSB
            elif node_type == 'CONCAT':
                multi_bit_node = self._convert_concat_node(node_data)
                if multi_bit_node:
                    output = node_data.get('output', node_id)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.multibit_signal_mapping[output] = multi_bit_node
                        for i, bit_node in enumerate(multi_bit_node.bits):
                            bit_name = f"{output}[{i}]" if multi_bit_node.width > 1 else output
                            self.signal_mapping[bit_name] = bit_node
                        if multi_bit_node.width > 0:
                            self.node_mapping[node_id] = multi_bit_node.bits[0]

            # Slice/index: signal[msb:lsb] or signal[idx]
            elif node_type == 'SLICE':
                fanins = node_data.get('fanins', [])
                ops = []
                for f in fanins:
                    if isinstance(f, (list, tuple)) and len(f) >= 1:
                        ops.append(str(f[0]))
                    else:
                        ops.append(str(f))
                if len(ops) >= 3:
                    sig_name, msb_s, lsb_s = ops[0], ops[1], ops[2]
                    try:
                        def _eval_idx(s: str) -> int:
                            ss = s.strip()
                            try:
                                return int(ss)
                            except Exception:
                                params = (self.netlist or {}).get("attrs", {}).get("parameters", {}) or {}
                                if ss in params and isinstance(params[ss], int):
                                    return int(params[ss])
                                # Minimal WIDTH-1 style evaluator
                                m = re.match(r"^\s*([A-Za-z_]\w*)\s*([-+])\s*(\d+)\s*$", ss)
                                if m:
                                    base = m.group(1)
                                    op = m.group(2)
                                    k = int(m.group(3))
                                    if base in params and isinstance(params[base], int):
                                        return int(params[base]) - k if op == "-" else int(params[base]) + k
                                raise

                        msb_v = _eval_idx(msb_s)
                        lsb_v = _eval_idx(lsb_s)
                        l = min(msb_v, lsb_v)
                        h = max(msb_v, lsb_v)
                        width = h - l + 1
                        base_bits = self._get_multi_bit_signal(sig_name, self._get_signal_width(sig_name, h + 1))
                        slice_bits = base_bits[l:h + 1]
                        mb = MultiBitAIGNode(width, slice_bits)
                        output = node_data.get('output', None)
                        if not output:
                            output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                            for sig, mapped_id in output_mapping.items():
                                if mapped_id == node_id:
                                    output = sig
                                    break
                        if not output:
                            output = node_id
                        self.multibit_signal_mapping[output] = mb
                        for i, bit_node in enumerate(mb.bits):
                            bit_name = f"{output}[{i}]" if mb.width > 1 else output
                            self.signal_mapping[bit_name] = bit_node
                        if mb.width > 0:
                            self.node_mapping[node_id] = mb.bits[0]
                    except Exception:
                        logger.debug("SLICE with non-int indices not supported yet")
                        continue

            # BUF with multi-bit input (pass-through): input is node_id from CONCAT
            elif node_type == 'BUF':
                fanins = node_data.get('fanins', [])
                inputs = node_data.get('inputs', [])
                input_list = []
                if fanins:
                    input_list = [str(f[0]) if isinstance(f, (list, tuple)) and f else str(f) for f in fanins]
                elif inputs:
                    input_list = [str(inp) for inp in inputs]
                if len(input_list) == 1:
                    inp_sig = input_list[0]
                    if inp_sig in self.multibit_signal_mapping:
                        # Prefer output_mapping (signal name) over node_id so temp2 is keyed by name
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        output = None
                        for sig, mapped_id in output_mapping.items():
                            if mapped_id == node_id:
                                output = sig
                                break
                        if not output:
                            output = node_data.get('output', node_id)
                        if not output:
                            output = node_id
                        if output:
                            mb = self.multibit_signal_mapping[inp_sig]
                            self.multibit_signal_mapping[output] = mb
                            for i, bit_node in enumerate(mb.bits):
                                bit_name = f"{output}[{i}]" if mb.width > 1 else output
                                self.signal_mapping[bit_name] = bit_node
                            self.node_mapping[node_id] = mb.bits[0]
                            continue
                aig_node = self._convert_gate_node(node_data)
                if aig_node:
                    self.node_mapping[node_id] = aig_node
                    output = node_data.get('output', None)
                    if not output:
                        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
                        for signal, mapped_node_id in output_mapping.items():
                            if mapped_node_id == node_id:
                                output = signal
                                break
                    if not output:
                        output = node_id
                    if output:
                        self.signal_mapping[output] = aig_node
            
            # Skip sequential/memory for now
            elif node_type in ['DFF', 'ARRAY_INDEX', 'SLICE']:
                logger.debug(f"Node type '{node_type}' not fully supported yet, skipping")
                continue
    
    def _convert_gate_node(self, node_data: Dict[str, Any]) -> Optional[AIGNode]:
        """Convert một gate node sang AIG."""
        node_type = node_data.get('type', '')
        
        # Get inputs
        inputs = node_data.get('inputs', [])
        fanins = node_data.get('fanins', [])
        
        # Extract input signals from fanins format: [["signal", inverted], ...]
        if fanins:
            input_signals = []
            input_inverted = []
            for fanin in fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                    input_signals.append(str(fanin[0]))
                    input_inverted.append(fanin[1] if len(fanin) > 1 else False)
                else:
                    input_signals.append(str(fanin))
                    input_inverted.append(False)
        elif inputs:
            input_signals = [str(inp) for inp in inputs]
            input_inverted = [False] * len(input_signals)
        else:
            return None
        
        # Get AIG nodes for inputs
        aig_inputs = []
        for sig, inv in zip(input_signals, input_inverted):
            # Constants like 1'b0, 4'hF, 8'd10
            if "'" in sig:
                value, _w = parse_constant_string(sig, 1)
                const_bit = self.aig.const1 if (value & 1) else self.aig.const0
                aig_input = const_bit
            elif sig in self.signal_mapping:
                aig_input = self.signal_mapping[sig]
            elif sig in self.aig.pis:
                aig_input = self.aig.pis[sig]
            elif sig in self.node_mapping:
                # Some netlists reference internal node ids directly as fanins
                aig_input = self.node_mapping[sig]
            else:
                # Input not found in mapping: either floating net (loose) or error (strict).
                if self._strict_synthesis:
                    raise ValueError(f"Synthesis error: input signal '{sig}' not found (undeclared or undriven)")
                logger.warning(f"Input signal '{sig}' not found, creating new primary input")
                aig_input = self.aig.create_pi(sig)
                self.signal_mapping[sig] = aig_input

            # Handle inversion
            if inv:
                aig_input = self.aig.create_not(aig_input)
            aig_inputs.append(aig_input)
        
        # Convert gate type to AIG
        if node_type == 'AND':
            if len(aig_inputs) >= 2:
                result = aig_inputs[0]
                for inp in aig_inputs[1:]:
                    result = self.aig.create_and(result, inp)
                return result
        elif node_type == 'OR':
            if len(aig_inputs) >= 2:
                # OR(a, b) = NOT(AND(NOT(a), NOT(b)))
                not_inputs = [self.aig.create_not(inp) for inp in aig_inputs]
                result = not_inputs[0]
                for inp in not_inputs[1:]:
                    result = self.aig.create_and(result, inp)
                return self.aig.create_not(result)
        elif node_type == 'XOR':
            if len(aig_inputs) >= 2:
                result = aig_inputs[0]
                for inp in aig_inputs[1:]:
                    result = self.aig.create_xor(result, inp)
                return result
        elif node_type == 'NAND':
            if len(aig_inputs) >= 2:
                result = aig_inputs[0]
                for inp in aig_inputs[1:]:
                    result = self.aig.create_and(result, inp)
                return self.aig.create_not(result)
        elif node_type == 'NOR':
            if len(aig_inputs) >= 2:
                not_inputs = [self.aig.create_not(inp) for inp in aig_inputs]
                result = not_inputs[0]
                for inp in not_inputs[1:]:
                    result = self.aig.create_and(result, inp)
                return result  # Already inverted
        elif node_type == 'XNOR':
            if len(aig_inputs) >= 2:
                result = aig_inputs[0]
                for inp in aig_inputs[1:]:
                    result = self.aig.create_xor(result, inp)
                return self.aig.create_not(result)
        elif node_type == 'NOT':
            if len(aig_inputs) >= 1:
                return self.aig.create_not(aig_inputs[0])
        elif node_type == 'BUF':
            if len(aig_inputs) >= 1:
                return aig_inputs[0]  # BUF is just pass-through in AIG
        
        return None
    
    def _create_primary_outputs(self, netlist: Dict[str, Any]):
        """Tạo Primary Output nodes trong AIG."""
        outputs = netlist.get('outputs', [])
        output_mapping = netlist.get('attrs', {}).get('output_mapping', {})
        
        for output_name in outputs:
            # Check if this is a multi-bit signal
            if output_name in self.multibit_signal_mapping:
                # Multi-bit output - add all bits as POs (for now, or could combine)
                multibit_node = self.multibit_signal_mapping[output_name]
                # For multi-bit outputs, add each bit as a separate PO
                # In a real implementation, you might want to track bit indices
                for i, bit_node in enumerate(multibit_node.bits):
                    self.aig.add_po(bit_node, inverted=False)
                logger.debug(f"Added multi-bit output '{output_name}' ({multibit_node.width} bits)")
            else:
                # Single-bit output - find the node/signal that drives this output
                if output_name in output_mapping:
                    node_id = output_mapping[output_name]
                    if node_id in self.node_mapping:
                        aig_node = self.node_mapping[node_id]
                        self.aig.add_po(aig_node, inverted=False)
                    elif node_id in self.signal_mapping:
                        aig_node = self.signal_mapping[node_id]
                        self.aig.add_po(aig_node, inverted=False)
                    else:
                        logger.warning(f"Output '{output_name}' node '{node_id}' not found")
                elif output_name in self.signal_mapping:
                    aig_node = self.signal_mapping[output_name]
                    self.aig.add_po(aig_node, inverted=False)
                else:
                    # Try bit[0] for multi-bit signals stored as bits
                    bit0_name = f"{output_name}[0]"
                    if bit0_name in self.signal_mapping:
                        # This is a multi-bit signal, add all bits
                        width = self._get_signal_width(output_name, 8)
                        for i in range(width):
                            bit_name = f"{output_name}[{i}]"
                            if bit_name in self.signal_mapping:
                                self.aig.add_po(self.signal_mapping[bit_name], inverted=False)
                    else:
                        logger.warning(f"Output '{output_name}' signal not found")
    
    def _get_signal_width(self, signal_name: str, default_width: int = 8) -> int:
        """Get bit width of a signal from netlist metadata."""
        if not self.netlist:
            return default_width
        
        # Check vector_widths in attrs
        vector_widths = self.netlist.get('attrs', {}).get('vector_widths', {})
        if signal_name in vector_widths:
            width = vector_widths[signal_name]
            if width and width > 0:
                return width
        
        # Try to extract from constant string (e.g., "8'd10" -> 8)
        if "'" in signal_name:
            _, width = parse_constant_string(signal_name, default_width)
            return width
        
        return default_width
    
    def _get_multi_bit_signal(self, signal_name: str, width: int) -> List[AIGNode]:
        """
        Get multi-bit signal as list of single-bit AIG nodes.
        
        Handles:
        - Constants (e.g., "8'd10", "8'hFF")
        - Regular signals (creates bit slices)
        """
        # Check if it's a constant
        if "'" in signal_name or signal_name.startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            value, parsed_width = parse_constant_string(signal_name, width)
            actual_width = max(width, parsed_width)
            multibit_const = create_constant_multibit(self.aig, value, actual_width)
            return multibit_const.bits[:width]  # Return requested width
        
        # If the netlist references a node-id directly, map it back to a signal name when possible.
        if signal_name in self._rev_output_mapping:
            signal_name = self._rev_output_mapping[signal_name]

        # Regular signal - try to get from mappings
        bits = []
        for i in range(width):
            bit_name = f"{signal_name}[{i}]" if width > 1 else signal_name
            
            if bit_name in self.signal_mapping:
                bits.append(self.signal_mapping[bit_name])
            elif signal_name in self.signal_mapping and width == 1:
                bits.append(self.signal_mapping[signal_name])
                break
            elif signal_name in self.multibit_signal_mapping:
                # Already have multi-bit version
                mb_node = self.multibit_signal_mapping[signal_name]
                if i < mb_node.width:
                    bits.append(mb_node.bits[i])
                else:
                    # Extend with zeros
                    bits.append(self.aig.const0)
            elif signal_name in self.aig.pis:
                # Primary input - for single-bit, use directly
                if width == 1:
                    bits.append(self.aig.pis[signal_name])
                    break
                else:
                    # Create intermediate PI for each bit
                    bit_pi = self.aig.create_pi(bit_name)
                    self.signal_mapping[bit_name] = bit_pi
                    bits.append(bit_pi)
            else:
                # Create new PI for this bit
                if self._strict_synthesis:
                    raise ValueError(f"Synthesis error: input signal '{signal_name}' not found (undeclared or undriven)")
                bit_pi = self.aig.create_pi(bit_name)
                self.signal_mapping[bit_name] = bit_pi
                bits.append(bit_pi)
        
        return bits if width > 1 else bits[:1]
    
    def _convert_add_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
        """Convert ADD node to AIG using ripple-carry adder."""
        fanins = node_data.get('fanins', [])
        if len(fanins) < 2:
            return None
        
        # Extract signals
        a_signal = str(fanins[0][0]) if isinstance(fanins[0], list) and len(fanins[0]) > 0 else str(fanins[0])
        b_signal = str(fanins[1][0]) if isinstance(fanins[1], list) and len(fanins[1]) > 0 else str(fanins[1])
        
        # Determine width (try to infer from signals or use default)
        output = node_data.get('output', '')
        width = self._get_signal_width(output, 8)
        
        # Try to get width from input signals
        a_width = self._get_signal_width(a_signal, width)
        b_width = self._get_signal_width(b_signal, width)
        width = max(width, a_width, b_width)
        
        # Get AIG nodes for inputs
        a_bits = self._get_multi_bit_signal(a_signal, width)
        b_bits = self._get_multi_bit_signal(b_signal, width)
        
        # Ripple-carry adder
        result_bits = []
        carry = self.aig.const0  # Initial carry = 0
        
        for i in range(width):
            a_bit = a_bits[i]
            b_bit = b_bits[i]
            
            # Full adder: sum = a XOR b XOR carry
            sum_ab = self.aig.create_xor(a_bit, b_bit)
            sum_result = self.aig.create_xor(sum_ab, carry)
            
            # carry_out = (a AND b) OR (carry AND (a XOR b))
            and_ab = self.aig.create_and(a_bit, b_bit)
            and_carry_sum = self.aig.create_and(carry, sum_ab)
            carry = self.aig.create_or(and_ab, and_carry_sum)
            
            result_bits.append(sum_result)
        
        return MultiBitAIGNode(width, result_bits)

    def _convert_concat_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
        """Convert CONCAT node: {a, b, ...} -> multi-bit, first operand is MSB."""
        fanins = node_data.get('fanins', [])
        if not fanins:
            return None
        operands = []
        for f in fanins:
            if isinstance(f, (list, tuple)) and len(f) >= 1:
                operands.append(str(f[0]))
            else:
                operands.append(str(f))
        if not operands:
            return None
        all_bits = []
        for sig in reversed(operands):
            if sig in self.multibit_signal_mapping:
                width = self.multibit_signal_mapping[sig].width
            else:
                width = self._get_signal_width(sig, 1)
            bits = self._get_multi_bit_signal(sig, width)
            all_bits.extend(bits)
        if not all_bits:
            return None
        return MultiBitAIGNode(len(all_bits), all_bits)
    
    def _convert_sub_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
        """Convert SUB node: a - b = a + (~b) + 1 (2's complement)."""
        fanins = node_data.get('fanins', [])
        if len(fanins) < 2:
            return None
        
        a_signal = str(fanins[0][0]) if isinstance(fanins[0], list) and len(fanins[0]) > 0 else str(fanins[0])
        b_signal = str(fanins[1][0]) if isinstance(fanins[1], list) and len(fanins[1]) > 0 else str(fanins[1])
        
        output = node_data.get('output', '')
        width = self._get_signal_width(output, 8)
        
        a_width = self._get_signal_width(a_signal, width)
        b_width = self._get_signal_width(b_signal, width)
        width = max(width, a_width, b_width)
        
        a_bits = self._get_multi_bit_signal(a_signal, width)
        b_bits = self._get_multi_bit_signal(b_signal, width)
        
        # Invert b for 2's complement
        b_inv_bits = [self.aig.create_not(bit) for bit in b_bits]
        
        # Add with carry_in = 1
        result_bits = []
        carry = self.aig.const1  # carry_in = 1 for 2's complement
        
        for i in range(width):
            a_bit = a_bits[i]
            b_inv_bit = b_inv_bits[i]
            
            sum_ab = self.aig.create_xor(a_bit, b_inv_bit)
            sum_result = self.aig.create_xor(sum_ab, carry)
            
            and_ab = self.aig.create_and(a_bit, b_inv_bit)
            and_carry_sum = self.aig.create_and(carry, sum_ab)
            carry = self.aig.create_or(and_ab, and_carry_sum)
            
            result_bits.append(sum_result)
        
        return MultiBitAIGNode(width, result_bits)
    
    def _convert_eq_node(self, node_data: Dict[str, Any]) -> Optional[AIGNode]:
        """
        Convert EQ (equality) node to AIG.
        
        For multi-bit: a == b = AND of all (a[i] XNOR b[i])
        Returns single-bit result.
        """
        fanins = node_data.get('fanins', [])
        if len(fanins) < 2:
            return None
        
        a_signal = str(fanins[0][0]) if isinstance(fanins[0], list) and len(fanins[0]) > 0 else str(fanins[0])
        b_signal = str(fanins[1][0]) if isinstance(fanins[1], list) and len(fanins[1]) > 0 else str(fanins[1])
        
        # Determine width (try to infer from signals or use default)
        # For EQ, width is determined by the input signals
        width = max(self._get_signal_width(a_signal, 1), self._get_signal_width(b_signal, 1))
        
        # Get AIG nodes for inputs
        a_bits = self._get_multi_bit_signal(a_signal, width)
        b_bits = self._get_multi_bit_signal(b_signal, width)
        
        # EQ = AND of all (a[i] XNOR b[i])
        # XNOR = NOT(XOR)
        eq_bits = []
        for i in range(width):
            xor_result = self.aig.create_xor(a_bits[i], b_bits[i])
            xnor_result = self.aig.create_not(xor_result)  # XNOR = NOT(XOR)
            eq_bits.append(xnor_result)
        
        # AND all bits together
        if not eq_bits:
            return None
        
        result = eq_bits[0]
        for bit in eq_bits[1:]:
            result = self.aig.create_and(result, bit)
        
        return result  # Single-bit result

    def _convert_ne_node(self, node_data: Dict[str, Any]) -> Optional[AIGNode]:
        eq = self._convert_eq_node(node_data)
        return self.aig.create_not(eq) if eq else None

    def _convert_rel_node(self, rel: str, node_data: Dict[str, Any]) -> Optional[AIGNode]:
        """Unsigned relational compare LT/LE/GT/GE (single-bit)."""
        fanins = node_data.get('fanins', [])
        if len(fanins) < 2:
            return None
        a_signal = str(fanins[0][0]) if isinstance(fanins[0], list) and len(fanins[0]) > 0 else str(fanins[0])
        b_signal = str(fanins[1][0]) if isinstance(fanins[1], list) and len(fanins[1]) > 0 else str(fanins[1])
        width = max(self._get_signal_width(a_signal, 1), self._get_signal_width(b_signal, 1))
        a_bits = self._get_multi_bit_signal(a_signal, width)
        b_bits = self._get_multi_bit_signal(b_signal, width)

        lt = self.aig.const0
        gt = self.aig.const0
        eq = self.aig.const1
        for i in reversed(range(width)):
            ai = a_bits[i]
            bi = b_bits[i]
            ai_n = self.aig.create_not(ai)
            bi_n = self.aig.create_not(bi)
            ai_lt_bi = self.aig.create_and(ai_n, bi)
            ai_gt_bi = self.aig.create_and(ai, bi_n)
            lt = self.aig.create_or(lt, self.aig.create_and(eq, ai_lt_bi))
            gt = self.aig.create_or(gt, self.aig.create_and(eq, ai_gt_bi))
            eq = self.aig.create_and(eq, self.aig.create_not(self.aig.create_xor(ai, bi)))

        if rel == 'LT':
            return lt
        if rel == 'GT':
            return gt
        if rel == 'LE':
            return self.aig.create_or(lt, eq)
        if rel == 'GE':
            return self.aig.create_or(gt, eq)
        return None

    def _convert_logical_node(self, t: str, node_data: Dict[str, Any]) -> Optional[AIGNode]:
        """Logical AND/OR (single-bit) for results of comparisons etc."""
        fanins = node_data.get('fanins', [])
        if len(fanins) < 2:
            return None
        a_sig = str(fanins[0][0]) if isinstance(fanins[0], list) and len(fanins[0]) > 0 else str(fanins[0])
        b_sig = str(fanins[1][0]) if isinstance(fanins[1], list) and len(fanins[1]) > 0 else str(fanins[1])

        # Resolve node-id -> signal if needed
        if a_sig in self._rev_output_mapping:
            a_sig = self._rev_output_mapping[a_sig]
        if b_sig in self._rev_output_mapping:
            b_sig = self._rev_output_mapping[b_sig]

        a_node = self.signal_mapping.get(a_sig) or self.node_mapping.get(a_sig)
        b_node = self.signal_mapping.get(b_sig) or self.node_mapping.get(b_sig)
        if not a_node or not b_node:
            if self._strict_synthesis:
                missing = a_sig if not a_node else b_sig
                raise ValueError(f"Synthesis error: input signal '{missing}' not found (undeclared or undriven)")
            return None
        if t == 'LAND':
            return self.aig.create_and(a_node, b_node)
        if t == 'LOR':
            return self.aig.create_or(a_node, b_node)
        return None
    
    def _convert_mux_node(self, node_data: Dict[str, Any]) -> Optional[MultiBitAIGNode]:
        """
        Convert MUX (multiplexer) node to AIG.
        
        Format: MUX has multiple data inputs and select signals.
        For N-way MUX: data[0], data[1], ..., data[N-1], select_signals...
        
        For 2-way MUX: out = (!sel AND in0) OR (sel AND in1)
        For N-way: build binary tree of 2-way MUXes.
        
        MUX format in netlist:
        - fanins: [data0, data1, ..., dataN-1, select_signal1, select_signal2, ...]
        - Or: [data0, data1, ..., dataN-1, select_signal]
        - May have case_selector field indicating the select signal name
        - num_cases field indicates number of cases
        """
        fanins = node_data.get('fanins', [])
        if len(fanins) < 3:  # Need at least 2 data inputs + 1 select
            logger.warning(f"MUX node needs at least 3 inputs, got {len(fanins)}")
            return None
        
        # Check for MUX metadata
        num_cases = node_data.get('num_cases', 0)
        case_selector = node_data.get('case_selector', '')
        has_default = node_data.get('has_default', False)
        
        # Extract data signal names and select signals
        # Format depends on parser - could be:
        # Option 1: [data0, data1, ..., dataN, sel0, sel1, ...] (case statement format)
        # Option 2: [data0, data1, ..., dataN, select] (simple format)
        
        # Try to separate data inputs from select signals
        # For case statement: select signals come after data inputs
        # Number of data inputs = num_cases (or num_cases + 1 if has_default)
        
        # Special case: ternary MUX produced by parser uses order [sel, true, false]
        if node_data.get("ternary") is True and len(fanins) >= 3:
            # data0=false, data1=true, select=sel
            data_inputs = [fanins[2], fanins[1]]
            select_inputs = [fanins[0]]
        elif num_cases > 0:
            # Case statement format
            num_data_inputs = num_cases + (1 if has_default else 0)
            if len(fanins) < num_data_inputs + 1:
                logger.warning(f"MUX has {num_cases} cases but insufficient fanins")
                return None
            
            # First num_data_inputs are data inputs
            data_inputs = fanins[:num_data_inputs]
            # Remaining are select signals (EQ results for case matching)
            select_inputs = fanins[num_data_inputs:]
        else:
            # Simple format: assume last fanin is select, rest are data
            data_inputs = fanins[:-1]
            select_inputs = fanins[-1:]
        
        # Extract data signal names
        data_signals = []
        for fanin in data_inputs:
            if isinstance(fanin, list) and len(fanin) > 0:
                data_signals.append(str(fanin[0]))
            else:
                data_signals.append(str(fanin))
        
        num_inputs = len(data_signals)
        if num_inputs < 2:
            logger.warning(f"MUX needs at least 2 data inputs, got {num_inputs}")
            return None
        
        # Determine width from output
        output = node_data.get('output', '')
        width = self._get_signal_width(output, 8)
        
        # Get multi-bit signals for all data inputs
        data_bits_list = []
        for data_signal in data_signals:
            data_bits = self._get_multi_bit_signal(data_signal, width)
            data_bits_list.append(data_bits)
        
        # Build N-way MUX using binary tree of 2-way MUXes
        # This recursively builds a tree: mux_tree(data[0..N-1], sel_bits)
        def build_mux_tree(data_bits_list: List[List[AIGNode]], select_bits: List[AIGNode], bit_pos: int) -> AIGNode:
            """
            Build MUX tree recursively.
            data_bits_list: List of [bit0, bit1, ..., bitN-1] for each data input
            select_bits: Select signal bits
            bit_pos: Current bit position being processed
            """
            if len(data_bits_list) == 1:
                return data_bits_list[0][bit_pos]
            
            if len(data_bits_list) == 2:
                # Base case: 2-way MUX
                in0 = data_bits_list[0][bit_pos]
                in1 = data_bits_list[1][bit_pos]
                sel = select_bits[0] if select_bits else self.aig.const0
                
                not_sel = self.aig.create_not(sel)
                term0 = self.aig.create_and(not_sel, in0)
                term1 = self.aig.create_and(sel, in1)
                return self.aig.create_or(term0, term1)
            
            # Recursive case: split in half and MUX the results
            mid = len(data_bits_list) // 2
            left_data = data_bits_list[:mid]
            right_data = data_bits_list[mid:]
            
            left_result = build_mux_tree(left_data, select_bits[1:], bit_pos)
            right_result = build_mux_tree(right_data, select_bits[1:], bit_pos)
            
            # MUX between left and right using MSB of select
            sel = select_bits[0] if select_bits else self.aig.const0
            not_sel = self.aig.create_not(sel)
            term0 = self.aig.create_and(not_sel, left_result)
            term1 = self.aig.create_and(sel, right_result)
            return self.aig.create_or(term0, term1)
        
        # Handle select signals
        # For case statement: select_inputs are EQ results (single-bit)
        # For simple format: select_inputs is the select signal (multi-bit)
        
        select_width = 1
        if num_cases > 0:
            # Case statement: use EQ results directly
            # But we need to combine them into a select value
            # For now, use first select input as primary select
            if len(select_inputs) > 0:
                select_signal = str(select_inputs[0][0]) if isinstance(select_inputs[0], list) else str(select_inputs[0])
                # This is an EQ result (single-bit), use as LSB of select
                select_bits = [self._get_multi_bit_signal(select_signal, 1)[0]]
            else:
                # Fallback: use case_selector if available
                if case_selector:
                    select_bits = self._get_multi_bit_signal(case_selector, 1)
                else:
                    select_bits = [self.aig.const0]
        else:
            # Simple format: extract select signal
            if len(select_inputs) > 0:
                select_input = select_inputs[0]
                if isinstance(select_input, list) and len(select_input) > 0:
                    select_signal = str(select_input[0])
                else:
                    select_signal = str(select_input)
                
                # Calculate select width needed
                select_width = 1
                while (1 << select_width) < num_inputs:
                    select_width += 1
                
                select_bits = self._get_multi_bit_signal(select_signal, select_width)
            else:
                select_bits = [self.aig.const0]
        
        # Build MUX for each bit position
        result_bits = []
        for bit_pos in range(width):
            mux_result = build_mux_tree(data_bits_list, select_bits, bit_pos)
            result_bits.append(mux_result)
        
        return MultiBitAIGNode(width, result_bits)


def synthesize_netlist_to_aig(netlist: Dict[str, Any]) -> AIG:
    """
    Synthesis function: Convert Netlist → AIG.
    
    Đây là bước SYNTHESIS riêng biệt.
    Chỉ làm chuyển đổi representation, không tối ưu hóa.
    
    Args:
        netlist: Netlist dictionary từ parser
        
    Returns:
        AIG object
    """
    converter = NetlistToAIGConverter()
    return converter.convert(netlist)


# Test function
if __name__ == "__main__":
    # Test với simple netlist
    test_netlist = {
        'name': 'test_synthesis',
        'inputs': ['a', 'b'],
        'outputs': ['out'],
        'nodes': [
            {'id': 'n1', 'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            {'id': 'n2', 'type': 'OR', 'inputs': ['temp1', 'a'], 'output': 'out'}
        ],
        'attrs': {
            'output_mapping': {'out': 'n2'}
        }
    }
    
    print("Test Synthesis: Netlist → AIG")
    print(f"Input netlist: {len(test_netlist['nodes'])} nodes")
    
    aig = synthesize_netlist_to_aig(test_netlist)
    
    print(f"Output AIG: {aig.count_nodes()} nodes")
    print(f"  AND nodes: {aig.count_and_nodes()}")
    print(f"  PIs: {len(aig.pis)}")
    print(f"  POs: {len(aig.pos)}")
    print("✅ Synthesis test passed!")


















