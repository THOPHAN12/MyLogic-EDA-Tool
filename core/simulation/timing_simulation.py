"""
Timing Simulation Engine

Hỗ trợ timing analysis và simulation:
- Gate delays
- Path delays
- Setup/hold time analysis
- Clock domain analysis
"""

import os
import sys
from typing import Dict, List, Union, Any, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .arithmetic_simulation import VectorValue

class TimingSimulator:
    """Timing simulation engine."""
    
    def __init__(self):
        """Initialize timing simulator."""
        self.gate_delays = {
            'AND': 1.0,
            'OR': 1.0,
            'NOT': 0.5,
            'XOR': 1.5,
            'NAND': 1.0,
            'NOR': 1.0,
            'XNOR': 1.5,
            'DFF': 2.0
        }
        self.path_delays = {}
        self.arrival_times = {}
        self.required_times = {}
        
    def analyze_timing(self, netlist: Dict[str, Any], 
                      clock_period: float = 10.0) -> Dict[str, Any]:
        """
        Analyze timing of netlist.
        
        Args:
            netlist: Logic netlist
            clock_period: Clock period in time units
            
        Returns:
            Timing analysis results
        """
        # Calculate arrival times
        self._calculate_arrival_times(netlist)
        
        # Calculate required times
        self._calculate_required_times(netlist, clock_period)
        
        # Find critical paths
        critical_paths = self._find_critical_paths(netlist)
        
        # Calculate slack
        slack = self._calculate_slack()
        
        return {
            'arrival_times': self.arrival_times,
            'required_times': self.required_times,
            'critical_paths': critical_paths,
            'slack': slack,
            'clock_period': clock_period
        }
    
    def _calculate_arrival_times(self, netlist: Dict[str, Any]):
        """Calculate arrival times for all nodes."""
        # Initialize input arrival times
        for input_name in netlist.get('inputs', []):
            self.arrival_times[input_name] = 0.0
        
        # Process nodes in topological order
        for node in netlist.get('nodes', []):
            node_id = node['id']
            node_type = node['type']
            fanins = node.get('fanins', [])
            
            # Calculate arrival time
            max_fanin_time = 0.0
            for fanin_id, _ in fanins:
                if fanin_id in self.arrival_times:
                    max_fanin_time = max(max_fanin_time, self.arrival_times[fanin_id])
            
            gate_delay = self.gate_delays.get(node_type, 1.0)
            self.arrival_times[node_id] = max_fanin_time + gate_delay
    
    def _calculate_required_times(self, netlist: Dict[str, Any], clock_period: float):
        """Calculate required times for all nodes."""
        # Initialize output required times
        for output_name in netlist.get('outputs', []):
            self.required_times[output_name] = clock_period
        
        # Process nodes in reverse topological order
        for node in reversed(netlist.get('nodes', [])):
            node_id = node['id']
            node_type = node['type']
            fanouts = self._get_fanouts(netlist, node_id)
            
            # Calculate required time
            min_fanout_time = clock_period
            for fanout_id in fanouts:
                if fanout_id in self.required_times:
                    gate_delay = self.gate_delays.get(node_type, 1.0)
                    min_fanout_time = min(min_fanout_time, 
                                        self.required_times[fanout_id] - gate_delay)
            
            self.required_times[node_id] = min_fanout_time
    
    def _get_fanouts(self, netlist: Dict[str, Any], node_id: str) -> List[str]:
        """Get fanout nodes for a given node."""
        fanouts = []
        for node in netlist.get('nodes', []):
            for fanin_id, _ in node.get('fanins', []):
                if fanin_id == node_id:
                    fanouts.append(node['id'])
        return fanouts
    
    def _find_critical_paths(self, netlist: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Find critical paths in the netlist."""
        critical_paths = []
        
        for output_name in netlist.get('outputs', []):
            if output_name in self.arrival_times and output_name in self.required_times:
                arrival = self.arrival_times[output_name]
                required = self.required_times[output_name]
                slack = required - arrival
                
                if slack <= 0:  # Critical path
                    path = self._trace_critical_path(netlist, output_name)
                    critical_paths.append({
                        'output': output_name,
                        'path': path,
                        'arrival_time': arrival,
                        'required_time': required,
                        'slack': slack
                    })
        
        return critical_paths
    
    def _trace_critical_path(self, netlist: Dict[str, Any], output_name: str) -> List[str]:
        """Trace critical path from output to input."""
        path = [output_name]
        current = output_name
        
        while current in netlist.get('inputs', []):
            # Find the node that drives current
            for node in netlist.get('nodes', []):
                if node['id'] == current:
                    # Find the fanin with latest arrival time
                    latest_fanin = None
                    latest_time = -1
                    
                    for fanin_id, _ in node.get('fanins', []):
                        if fanin_id in self.arrival_times:
                            if self.arrival_times[fanin_id] > latest_time:
                                latest_time = self.arrival_times[fanin_id]
                                latest_fanin = fanin_id
                    
                    if latest_fanin:
                        path.append(latest_fanin)
                        current = latest_fanin
                    else:
                        break
                    break
        
        return path
    
    def _calculate_slack(self) -> Dict[str, float]:
        """Calculate slack for all nodes."""
        slack = {}
        for node_id in self.arrival_times:
            if node_id in self.required_times:
                slack[node_id] = self.required_times[node_id] - self.arrival_times[node_id]
        return slack

if __name__ == "__main__":
    simulator = TimingSimulator()
    print("Timing Simulator initialized.")
