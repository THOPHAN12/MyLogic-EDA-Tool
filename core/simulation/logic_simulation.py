"""
Logic Gate Simulation Engine

Hỗ trợ simulation cho logic gates:
- Basic gates: AND, OR, NOT, XOR
- Complex gates: NAND, NOR, XNOR
- Sequential elements: DFF, Latch
"""

import os
import sys
from typing import Dict, List, Union, Any, Optional

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .arithmetic_simulation import VectorValue

class LogicSimulator:
    """Logic gate simulation engine."""
    
    def __init__(self):
        """Initialize logic simulator."""
        self.node_values = {}
        self.clock_cycle = 0
        
    def simulate_logic_netlist(self, netlist: Dict[str, Any], 
                             inputs: Dict[str, Union[int, VectorValue]],
                             clock: Optional[bool] = None) -> Dict[str, VectorValue]:
        """
        Simulate logic netlist.
        
        Args:
            netlist: Logic netlist
            inputs: Input values
            clock: Clock signal (for sequential elements)
            
        Returns:
            Output values
        """
        # Initialize node values
        self.node_values = {}
        
        # Set input values
        for input_name, value in inputs.items():
            if isinstance(value, VectorValue):
                self.node_values[input_name] = value
            else:
                self.node_values[input_name] = VectorValue(value, 1)
        
        # Process nodes
        for node in netlist.get('nodes', []):
            self._process_node(node, clock)
        
        # Collect outputs
        outputs = {}
        for output_name in netlist.get('outputs', []):
            if output_name in self.node_values:
                outputs[output_name] = self.node_values[output_name]
        
        return outputs
    
    def _process_node(self, node: Dict[str, Any], clock: Optional[bool] = None):
        """Process a single node."""
        node_id = node['id']
        node_type = node['type']
        fanins = node.get('fanins', [])
        
        if node_type == 'AND':
            result = self._simulate_and(fanins)
        elif node_type == 'OR':
            result = self._simulate_or(fanins)
        elif node_type == 'NOT':
            result = self._simulate_not(fanins)
        elif node_type == 'XOR':
            result = self._simulate_xor(fanins)
        elif node_type == 'NAND':
            result = self._simulate_nand(fanins)
        elif node_type == 'NOR':
            result = self._simulate_nor(fanins)
        elif node_type == 'XNOR':
            result = self._simulate_xnor(fanins)
        elif node_type == 'DFF':
            result = self._simulate_dff(fanins, clock)
        else:
            result = VectorValue(0, 1)
        
        self.node_values[node_id] = result
    
    def _simulate_and(self, fanins: List[tuple]) -> VectorValue:
        """Simulate AND gate."""
        if len(fanins) < 2:
            return VectorValue(0, 1)
        
        result = VectorValue(1, 1)  # Start with 1 for AND
        for fanin_id, inv in fanins:
            if fanin_id in self.node_values:
                val = self.node_values[fanin_id]
                if inv:
                    val = VectorValue(1 - val.to_int(), val.width)
                result = VectorValue(result.to_int() & val.to_int(), 1)
        
        return result
    
    def _simulate_or(self, fanins: List[tuple]) -> VectorValue:
        """Simulate OR gate."""
        if len(fanins) < 2:
            return VectorValue(0, 1)
        
        result = VectorValue(0, 1)  # Start with 0 for OR
        for fanin_id, inv in fanins:
            if fanin_id in self.node_values:
                val = self.node_values[fanin_id]
                if inv:
                    val = VectorValue(1 - val.to_int(), val.width)
                result = VectorValue(result.to_int() | val.to_int(), 1)
        
        return result
    
    def _simulate_not(self, fanins: List[tuple]) -> VectorValue:
        """Simulate NOT gate."""
        if len(fanins) == 1:
            fanin_id, inv = fanins[0]
            if fanin_id in self.node_values:
                val = self.node_values[fanin_id]
                if inv:
                    return val  # Double inversion
                else:
                    return VectorValue(1 - val.to_int(), val.width)
        return VectorValue(0, 1)
    
    def _simulate_xor(self, fanins: List[tuple]) -> VectorValue:
        """Simulate XOR gate."""
        if len(fanins) < 2:
            return VectorValue(0, 1)
        
        result = VectorValue(0, 1)
        for fanin_id, inv in fanins:
            if fanin_id in self.node_values:
                val = self.node_values[fanin_id]
                if inv:
                    val = VectorValue(1 - val.to_int(), val.width)
                result = VectorValue(result.to_int() ^ val.to_int(), 1)
        
        return result
    
    def _simulate_nand(self, fanins: List[tuple]) -> VectorValue:
        """Simulate NAND gate."""
        and_result = self._simulate_and(fanins)
        return VectorValue(1 - and_result.to_int(), 1)
    
    def _simulate_nor(self, fanins: List[tuple]) -> VectorValue:
        """Simulate NOR gate."""
        or_result = self._simulate_or(fanins)
        return VectorValue(1 - or_result.to_int(), 1)
    
    def _simulate_xnor(self, fanins: List[tuple]) -> VectorValue:
        """Simulate XNOR gate."""
        xor_result = self._simulate_xor(fanins)
        return VectorValue(1 - xor_result.to_int(), 1)
    
    def _simulate_dff(self, fanins: List[tuple], clock: Optional[bool]) -> VectorValue:
        """Simulate D flip-flop."""
        if len(fanins) == 1 and clock:
            fanin_id, inv = fanins[0]
            if fanin_id in self.node_values:
                val = self.node_values[fanin_id]
                if inv:
                    val = VectorValue(1 - val.to_int(), val.width)
                return val
        return VectorValue(0, 1)

# Wrapper function for backward compatibility
def simulate_logic_netlist(netlist: Dict[str, Any], 
                          inputs: Dict[str, Union[int, VectorValue]],
                          clock: Optional[bool] = None) -> Dict[str, VectorValue]:
    """
    Wrapper function to simulate logic netlist.
    
    Args:
        netlist: Logic netlist
        inputs: Input values
        clock: Clock signal (for sequential elements)
        
    Returns:
        Output values
    """
    simulator = LogicSimulator()
    return simulator.simulate_logic_netlist(netlist, inputs, clock)

if __name__ == "__main__":
    simulator = LogicSimulator()
    print("Logic Simulator initialized.")
