#!/usr/bin/env python3
"""
Static Timing Analysis (STA) for VLSI Physical Design

Dựa trên các khái niệm VLSI CAD Part 2 cho phân tích timing bao gồm ATs, RATs, và SLACKS.
"""

from typing import Dict, List, Set, Any, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class TimingNode:
    """Đại diện cho một node trong timing graph."""
    
    def __init__(self, name: str, node_type: str = "gate"):
        self.name = name
        self.node_type = node_type  # "gate", "input", "output"
        self.arrival_time = 0.0
        self.required_time = float('inf')
        self.slack = float('inf')
        self.fanout = []
        self.fanin = []
        self.delay = 0.0
        self.load_capacitance = 0.0
        
    def add_fanout(self, node: 'TimingNode'):
        """Add fanout node."""
        if node not in self.fanout:
            self.fanout.append(node)
    
    def add_fanin(self, node: 'TimingNode'):
        """Add fanin node."""
        if node not in self.fanin:
            self.fanin.append(node)
    
    def calculate_delay(self) -> float:
        """Calculate gate delay based on load."""
        # Simple delay model: delay = base_delay + load_factor * load_capacitance
        base_delay = 0.1  # Base delay in ns
        load_factor = 0.01  # Load factor
        
        return base_delay + load_factor * self.load_capacitance
    
    def __repr__(self):
        return f"TimingNode({self.name}, AT={self.arrival_time:.2f}, RAT={self.required_time:.2f}, Slack={self.slack:.2f})"

class TimingArc:
    """Represents a timing arc between nodes."""
    
    def __init__(self, from_node: str, to_node: str, delay: float, arc_type: str = "combinational"):
        self.from_node = from_node
        self.to_node = to_node
        self.delay = delay
        self.arc_type = arc_type  # "combinational", "setup", "hold"
    
    def __repr__(self):
        return f"TimingArc({self.from_node} -> {self.to_node}, delay={self.delay:.2f})"

class StaticTimingAnalyzer:
    """
    Static Timing Analysis (STA) engine.
    
    Based on VLSI CAD Part 2 concepts for timing analysis.
    """
    
    def __init__(self):
        self.nodes: Dict[str, TimingNode] = {}
        self.arcs: List[TimingArc] = []
        self.input_nodes: Set[str] = set()
        self.output_nodes: Set[str] = set()
        self.clock_period = 10.0  # Default clock period in ns
        
    def add_node(self, node: TimingNode):
        """Add a timing node."""
        self.nodes[node.name] = node
        
        if node.node_type == "input":
            self.input_nodes.add(node.name)
        elif node.node_type == "output":
            self.output_nodes.add(node.name)
    
    def add_arc(self, arc: TimingArc):
        """Add a timing arc."""
        self.arcs.append(arc)
        
        # Update node connections
        if arc.from_node in self.nodes and arc.to_node in self.nodes:
            self.nodes[arc.from_node].add_fanout(self.nodes[arc.to_node])
            self.nodes[arc.to_node].add_fanin(self.nodes[arc.from_node])
    
    def set_clock_period(self, period: float):
        """Set clock period."""
        self.clock_period = period
    
    def perform_timing_analysis(self) -> Dict[str, Any]:
        """
        Perform complete static timing analysis.
        
        Returns timing analysis results including critical paths.
        """
        logger.info("Starting Static Timing Analysis...")
        
        # Step 1: Calculate Arrival Times (ATs)
        self._calculate_arrival_times()
        
        # Step 2: Calculate Required Arrival Times (RATs)
        self._calculate_required_arrival_times()
        
        # Step 3: Calculate Slacks
        self._calculate_slacks()
        
        # Step 4: Find critical paths
        critical_paths = self._find_critical_paths()
        
        # Step 5: Generate timing report
        timing_report = self._generate_timing_report(critical_paths)
        
        logger.info("Static Timing Analysis completed")
        return timing_report
    
    def _calculate_arrival_times(self):
        """Calculate arrival times using forward propagation."""
        logger.debug("Calculating arrival times...")
        
        # Initialize input nodes
        for node_name in self.input_nodes:
            if node_name in self.nodes:
                self.nodes[node_name].arrival_time = 0.0
        
        # Forward propagation using topological sort
        processed = set(self.input_nodes)
        queue = list(self.input_nodes)
        
        while queue:
            current_node_name = queue.pop(0)
            current_node = self.nodes[current_node_name]
            
            # Update fanout nodes
            for fanout_node in current_node.fanout:
                fanout_name = fanout_node.name
                
                if fanout_name not in processed:
                    # Calculate arrival time at fanout
                    arc_delay = self._get_arc_delay(current_node_name, fanout_name)
                    new_arrival_time = current_node.arrival_time + arc_delay
                    
                    # Update if this is a better path
                    if new_arrival_time > fanout_node.arrival_time:
                        fanout_node.arrival_time = new_arrival_time
                    
                    # Add to queue if all fanins are processed
                    if self._all_fanins_processed(fanout_node, processed):
                        queue.append(fanout_name)
                        processed.add(fanout_name)
    
    def _calculate_required_arrival_times(self):
        """Calculate required arrival times using backward propagation."""
        logger.debug("Calculating required arrival times...")
        
        # Initialize output nodes
        for node_name in self.output_nodes:
            if node_name in self.nodes:
                self.nodes[node_name].required_time = self.clock_period
        
        # Backward propagation
        processed = set(self.output_nodes)
        queue = list(self.output_nodes)
        
        while queue:
            current_node_name = queue.pop(0)
            current_node = self.nodes[current_node_name]
            
            # Update fanin nodes
            for fanin_node in current_node.fanin:
                fanin_name = fanin_node.name
                
                if fanin_name not in processed:
                    # Calculate required time at fanin
                    arc_delay = self._get_arc_delay(fanin_name, current_node_name)
                    new_required_time = current_node.required_time - arc_delay
                    
                    # Update if this is a more restrictive requirement
                    if new_required_time < fanin_node.required_time:
                        fanin_node.required_time = new_required_time
                    
                    # Add to queue if all fanouts are processed
                    if self._all_fanouts_processed(fanin_node, processed):
                        queue.append(fanin_name)
                        processed.add(fanin_name)
    
    def _calculate_slacks(self):
        """Calculate slacks for all nodes."""
        logger.debug("Calculating slacks...")
        
        for node in self.nodes.values():
            if node.required_time != float('inf') and node.arrival_time != float('inf'):
                node.slack = node.required_time - node.arrival_time
            else:
                node.slack = float('inf')
    
    def _find_critical_paths(self) -> List[List[str]]:
        """Find critical paths (paths with zero or negative slack)."""
        logger.debug("Finding critical paths...")
        
        critical_paths = []
        
        # Find nodes with zero or negative slack
        critical_nodes = [node for node in self.nodes.values() 
                         if node.slack <= 0 and node.node_type != "input"]
        
        # Trace back from critical nodes to find complete paths
        for critical_node in critical_nodes:
            path = self._trace_critical_path(critical_node)
            if path:
                critical_paths.append(path)
        
        # Remove duplicate paths
        unique_paths = []
        for path in critical_paths:
            if path not in unique_paths:
                unique_paths.append(path)
        
        return unique_paths
    
    def _trace_critical_path(self, end_node: TimingNode) -> List[str]:
        """Trace critical path backwards from a node."""
        path = [end_node.name]
        current_node = end_node
        
        while current_node.fanin:
            # Find fanin with worst slack
            worst_fanin = None
            worst_slack = float('inf')
            
            for fanin in current_node.fanin:
                if fanin.slack < worst_slack:
                    worst_slack = fanin.slack
                    worst_fanin = fanin
            
            if worst_fanin and worst_fanin.node_type != "input":
                path.insert(0, worst_fanin.name)
                current_node = worst_fanin
            else:
                break
        
        return path if len(path) > 1 else []
    
    def _get_arc_delay(self, from_node: str, to_node: str) -> float:
        """Get delay of arc between two nodes."""
        for arc in self.arcs:
            if arc.from_node == from_node and arc.to_node == to_node:
                return arc.delay
        
        # Default delay if no arc found
        return 0.1
    
    def _all_fanins_processed(self, node: TimingNode, processed: Set[str]) -> bool:
        """Check if all fanin nodes are processed."""
        for fanin in node.fanin:
            if fanin.name not in processed:
                return False
        return True
    
    def _all_fanouts_processed(self, node: TimingNode, processed: Set[str]) -> bool:
        """Check if all fanout nodes are processed."""
        for fanout in node.fanout:
            if fanout.name not in processed:
                return False
        return True
    
    def _generate_timing_report(self, critical_paths: List[List[str]]) -> Dict[str, Any]:
        """Generate comprehensive timing report."""
        
        # Calculate timing statistics
        all_slacks = [node.slack for node in self.nodes.values() 
                     if node.slack != float('inf')]
        
        worst_slack = min(all_slacks) if all_slacks else 0.0
        best_slack = max(all_slacks) if all_slacks else 0.0
        average_slack = sum(all_slacks) / len(all_slacks) if all_slacks else 0.0
        
        # Count timing violations
        violations = sum(1 for slack in all_slacks if slack < 0)
        
        report = {
            'clock_period': self.clock_period,
            'worst_slack': worst_slack,
            'best_slack': best_slack,
            'average_slack': average_slack,
            'timing_violations': violations,
            'critical_paths': critical_paths,
            'total_nodes': len(self.nodes),
            'total_arcs': len(self.arcs),
            'timing_summary': {
                'setup_time': -worst_slack if worst_slack < 0 else 0.0,
                'hold_time': 0.0,  # Simplified
                'maximum_frequency': 1.0 / self.clock_period if self.clock_period > 0 else 0.0
            }
        }
        
        return report
    
    def print_timing_report(self, report: Dict[str, Any]):
        """Print timing analysis report."""
        print("\n" + "="*60)
        print("STATIC TIMING ANALYSIS REPORT")
        print("="*60)
        
        print(f"Clock Period: {report['clock_period']:.2f} ns")
        print(f"Maximum Frequency: {report['timing_summary']['maximum_frequency']:.2f} MHz")
        print(f"Worst Slack: {report['worst_slack']:.2f} ns")
        print(f"Best Slack: {report['best_slack']:.2f} ns")
        print(f"Average Slack: {report['average_slack']:.2f} ns")
        print(f"Timing Violations: {report['timing_violations']}")
        
        print(f"\nCritical Paths ({len(report['critical_paths'])}):")
        for i, path in enumerate(report['critical_paths']):
            print(f"  Path {i+1}: {' -> '.join(path)}")
        
        print(f"\nNode Timing Summary:")
        print(f"{'Node':<15} {'AT':<8} {'RAT':<8} {'Slack':<8}")
        print("-" * 40)
        
        for node_name, node in self.nodes.items():
            if node.slack != float('inf'):
                print(f"{node_name:<15} {node.arrival_time:<8.2f} {node.required_time:<8.2f} {node.slack:<8.2f}")

# Alias for backward compatibility
TimingAnalysis = StaticTimingAnalyzer

# Example usage and testing
if __name__ == "__main__":
    # Create timing analyzer
    sta = StaticTimingAnalyzer()
    
    # Create timing nodes
    nodes_data = [
        ("clk", "input"),
        ("in1", "input"),
        ("in2", "input"),
        ("gate1", "gate"),
        ("gate2", "gate"),
        ("gate3", "gate"),
        ("out1", "output"),
    ]
    
    for name, node_type in nodes_data:
        node = TimingNode(name, node_type)
        sta.add_node(node)
    
    # Create timing arcs
    arcs_data = [
        ("clk", "gate1", 0.1),
        ("in1", "gate1", 0.2),
        ("in2", "gate2", 0.15),
        ("gate1", "gate3", 0.3),
        ("gate2", "gate3", 0.25),
        ("gate3", "out1", 0.2),
    ]
    
    for from_node, to_node, delay in arcs_data:
        arc = TimingArc(from_node, to_node, delay)
        sta.add_arc(arc)
    
    # Set clock period
    sta.set_clock_period(2.0)  # 2 ns clock period
    
    print("Static Timing Analysis Demo:")
    print("=" * 50)
    
    # Perform timing analysis
    timing_report = sta.perform_timing_analysis()
    
    # Print results
    sta.print_timing_report(timing_report)
