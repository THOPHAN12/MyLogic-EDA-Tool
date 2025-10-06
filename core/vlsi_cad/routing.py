#!/usr/bin/env python3
"""
Routing Algorithms for VLSI Physical Design

Dựa trên các khái niệm VLSI CAD Part 2 cho ASIC routing, bao gồm Maze Routing.
"""

from typing import Dict, List, Set, Any, Tuple, Optional
import heapq
import logging

logger = logging.getLogger(__name__)

class Point:
    """Đại diện cho một điểm 2D."""
    
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __repr__(self):
        return f"({self.x}, {self.y})"
    
    def distance_to(self, other: 'Point') -> float:
        """Tính toán Manhattan distance đến một điểm khác."""
        return abs(self.x - other.x) + abs(self.y - other.y)

class RoutingGrid:
    """Đại diện cho routing grid cho maze routing."""
    
    def __init__(self, width: int, height: int, layers: int = 3):
        self.width = width
        self.height = height
        self.layers = layers
        
        # Grid: [layer][y][x] = trạng thái chiếm dụng
        # 0 = free, 1 = occupied, 2 = blocked
        self.grid = [[[0 for _ in range(width)] for _ in range(height)] for _ in range(layers)]
        
        # Theo dõi lịch sử routing cho visualization
        self.routing_history = []
        
    def is_free(self, point: Point, layer: int = 0) -> bool:
        """Check if a point is free for routing."""
        if (0 <= point.x < self.width and 
            0 <= point.y < self.height and 
            0 <= layer < self.layers):
            return self.grid[layer][point.y][point.x] == 0
        return False
    
    def is_occupied(self, point: Point, layer: int = 0) -> bool:
        """Check if a point is occupied."""
        if (0 <= point.x < self.width and 
            0 <= point.y < self.height and 
            0 <= layer < self.layers):
            return self.grid[layer][point.y][point.x] == 1
        return True
    
    def occupy(self, point: Point, layer: int = 0):
        """Occupy a point."""
        if (0 <= point.x < self.width and 
            0 <= point.y < self.height and 
            0 <= layer < self.layers):
            self.grid[layer][point.y][point.x] = 1
    
    def block(self, point: Point, layer: int = 0):
        """Block a point (permanent obstacle)."""
        if (0 <= point.x < self.width and 
            0 <= point.y < self.height and 
            0 <= layer < self.layers):
            self.grid[layer][point.y][point.x] = 2
    
    def get_neighbors(self, point: Point, layer: int = 0) -> List[Tuple[Point, int]]:
        """Get valid neighboring points."""
        neighbors = []
        
        # 4-directional movement
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        for dx, dy in directions:
            new_point = Point(point.x + dx, point.y + dy)
            if self.is_free(new_point, layer):
                neighbors.append((new_point, layer))
        
        # Via to other layers
        for other_layer in range(self.layers):
            if other_layer != layer and self.is_free(point, other_layer):
                neighbors.append((point, other_layer))
        
        return neighbors

class Net:
    """Represents a net to be routed."""
    
    def __init__(self, name: str, sources: List[Point], targets: List[Point], 
                 layer: int = 0, priority: int = 1):
        self.name = name
        self.sources = sources  # Source pins
        self.targets = targets  # Target pins
        self.layer = layer
        self.priority = priority
        self.routes = []  # List of route segments
        self.routed = False
        self.wirelength = 0
        
    def add_route_segment(self, start: Point, end: Point, layer: int):
        """Add a route segment."""
        self.routes.append((start, end, layer))
        self.wirelength += start.distance_to(end)
    
    def get_all_pins(self) -> List[Point]:
        """Get all pins (sources + targets)."""
        return self.sources + self.targets

class MazeRouter:
    """
    Maze Router implementation for VLSI routing.
    
    Based on VLSI CAD Part 2 concepts for ASIC routing.
    """
    
    def __init__(self, grid: RoutingGrid):
        self.grid = grid
        self.nets: Dict[str, Net] = {}
        self.routed_nets = 0
        self.total_wirelength = 0
        self.routing_congestion = {}
        
    def add_net(self, net: Net):
        """Add a net to be routed."""
        self.nets[net.name] = net
    
    def route_all_nets(self, strategy: str = "maze") -> Dict[str, bool]:
        """
        Route all nets using specified strategy.
        
        Args:
            strategy: "maze", "lee", or "rip_up_reroute"
        """
        logger.info(f"Routing {len(self.nets)} nets using {strategy} strategy...")
        
        # Sort nets by priority and wirelength estimate
        sorted_nets = self._sort_nets_for_routing()
        
        routing_results = {}
        
        for net_name in sorted_nets:
            net = self.nets[net_name]
            logger.debug(f"Routing net: {net_name}")
            
            if strategy == "maze":
                success = self._route_net_maze(net)
            elif strategy == "lee":
                success = self._route_net_lee(net)
            elif strategy == "rip_up_reroute":
                success = self._route_net_rip_up_reroute(net)
            else:
                success = self._route_net_maze(net)
            
            routing_results[net_name] = success
            
            if success:
                self.routed_nets += 1
                self.total_wirelength += net.wirelength
                logger.debug(f"Successfully routed {net_name}, wirelength: {net.wirelength}")
            else:
                logger.warning(f"Failed to route {net_name}")
        
        logger.info(f"Routing completed: {self.routed_nets}/{len(self.nets)} nets routed")
        return routing_results
    
    def _sort_nets_for_routing(self) -> List[str]:
        """Sort nets by priority and estimated wirelength."""
        def net_priority(net_name):
            net = self.nets[net_name]
            # Higher priority for nets with more pins and higher priority
            pin_count = len(net.get_all_pins())
            estimated_wirelength = self._estimate_net_wirelength(net)
            return (net.priority, -pin_count, -estimated_wirelength)
        
        return sorted(self.nets.keys(), key=net_priority, reverse=True)
    
    def _estimate_net_wirelength(self, net: Net) -> float:
        """Estimate wirelength using minimum spanning tree."""
        pins = net.get_all_pins()
        if len(pins) < 2:
            return 0.0
        
        # Simple estimation using bounding box
        x_coords = [p.x for p in pins]
        y_coords = [p.y for p in pins]
        
        width = max(x_coords) - min(x_coords)
        height = max(y_coords) - min(y_coords)
        
        return width + height
    
    def _route_net_maze(self, net: Net) -> bool:
        """
        Route a single net using maze routing algorithm.
        
        This is a simplified implementation of the Lee algorithm.
        """
        pins = net.get_all_pins()
        if len(pins) < 2:
            return True
        
        # Start with first pin and route to all other pins
        start_pin = pins[0]
        remaining_pins = pins[1:]
        
        # Route to each remaining pin
        for target_pin in remaining_pins:
            if not self._route_point_to_point(start_pin, target_pin, net):
                return False
        
        net.routed = True
        return True
    
    def _route_net_lee(self, net: Net) -> bool:
        """
        Route using Lee's algorithm (wave propagation).
        
        This is the classic maze routing algorithm.
        """
        pins = net.get_all_pins()
        if len(pins) < 2:
            return True
        
        # Use Lee's algorithm for point-to-point routing
        start_pin = pins[0]
        for target_pin in pins[1:]:
            if not self._route_point_to_point_lee(start_pin, target_pin, net):
                return False
        
        net.routed = True
        return True
    
    def _route_net_rip_up_reroute(self, net: Net) -> bool:
        """
        Route using rip-up and reroute strategy.
        
        If routing fails due to congestion, rip up some existing routes
        and try again.
        """
        max_attempts = 3
        
        for attempt in range(max_attempts):
            if self._route_net_maze(net):
                net.routed = True
                return True
            
            if attempt < max_attempts - 1:
                # Rip up some existing routes and try again
                self._rip_up_congested_routes()
                logger.debug(f"Rip-up and reroute attempt {attempt + 1} for {net.name}")
        
        return False
    
    def _route_point_to_point(self, start: Point, end: Point, net: Net) -> bool:
        """Route from start point to end point using simple pathfinding."""
        # Simple greedy routing for demonstration
        current = start
        
        while current != end:
            # Find direction towards target
            dx = 1 if end.x > current.x else -1 if end.x < current.x else 0
            dy = 1 if end.y > current.y else -1 if end.y < current.y else 0
            
            # Try to move in preferred direction
            next_point = Point(current.x + dx, current.y + dy)
            
            if self.grid.is_free(next_point, net.layer):
                # Add route segment
                net.add_route_segment(current, next_point, net.layer)
                self.grid.occupy(next_point, net.layer)
                current = next_point
            else:
                # Try alternative directions
                alternatives = [
                    Point(current.x + dx, current.y),
                    Point(current.x, current.y + dy),
                    Point(current.x - dx, current.y),
                    Point(current.x, current.y - dy)
                ]
                
                routed = False
                for alt_point in alternatives:
                    if self.grid.is_free(alt_point, net.layer):
                        net.add_route_segment(current, alt_point, net.layer)
                        self.grid.occupy(alt_point, net.layer)
                        current = alt_point
                        routed = True
                        break
                
                if not routed:
                    return False
        
        return True
    
    def _route_point_to_point_lee(self, start: Point, end: Point, net: Net) -> bool:
        """Route using Lee's algorithm (wave propagation)."""
        # This is a simplified implementation
        # In practice, you'd implement the full wave propagation algorithm
        
        # For now, use the simple routing
        return self._route_point_to_point(start, end, net)
    
    def _rip_up_congested_routes(self):
        """Rip up some congested routes to free space for new routing."""
        # Simple strategy: rip up routes with high congestion
        # In practice, you'd analyze congestion and rip up strategically
        
        congested_nets = []
        for net_name, net in self.nets.items():
            if net.routed and net.wirelength > 100:  # Simple threshold
                congested_nets.append(net_name)
        
        # Rip up some congested nets
        for net_name in congested_nets[:2]:  # Rip up max 2 nets
            self._rip_up_net(net_name)
    
    def _rip_up_net(self, net_name: str):
        """Rip up a specific net."""
        if net_name in self.nets:
            net = self.nets[net_name]
            # Free up grid cells occupied by this net
            for start, end, layer in net.routes:
                # Free intermediate points (simplified)
                self.grid.grid[layer][end.y][end.x] = 0
            
            # Reset net
            net.routes = []
            net.routed = False
            net.wirelength = 0
    
    def get_routing_statistics(self) -> Dict[str, Any]:
        """Get routing statistics."""
        total_nets = len(self.nets)
        routed_nets = sum(1 for net in self.nets.values() if net.routed)
        
        return {
            'total_nets': total_nets,
            'routed_nets': routed_nets,
            'routing_success_rate': routed_nets / total_nets if total_nets > 0 else 0,
            'total_wirelength': self.total_wirelength,
            'average_wirelength': self.total_wirelength / routed_nets if routed_nets > 0 else 0,
            'grid_utilization': self._calculate_grid_utilization()
        }
    
    def _calculate_grid_utilization(self) -> float:
        """Calculate grid utilization percentage."""
        total_cells = self.grid.width * self.grid.height * self.grid.layers
        occupied_cells = 0
        
        for layer in range(self.grid.layers):
            for y in range(self.grid.height):
                for x in range(self.grid.width):
                    if self.grid.grid[layer][y][x] == 1:
                        occupied_cells += 1
        
        return (occupied_cells / total_cells) * 100
    
    def visualize_routing(self):
        """Visualize routing results (text output)."""
        print(f"\nRouting Visualization:")
        print(f"Grid size: {self.grid.width} x {self.grid.height} x {self.grid.layers}")
        
        stats = self.get_routing_statistics()
        print(f"Routing success rate: {stats['routing_success_rate']*100:.1f}%")
        print(f"Total wirelength: {stats['total_wirelength']:.2f}")
        print(f"Grid utilization: {stats['grid_utilization']:.1f}%")
        
        print(f"\nNet routing results:")
        for net_name, net in self.nets.items():
            status = "✓" if net.routed else "✗"
            print(f"  {status} {net_name}: {net.wirelength:.2f} wirelength")

# Example usage and testing
if __name__ == "__main__":
    # Create routing grid
    grid = RoutingGrid(50, 50, 3)
    
    # Create router
    router = MazeRouter(grid)
    
    # Add some nets
    nets_data = [
        ("net1", [Point(5, 5)], [Point(45, 45)], 0, 1),
        ("net2", [Point(10, 10)], [Point(40, 40)], 0, 1),
        ("net3", [Point(15, 15)], [Point(35, 35)], 0, 1),
        ("net4", [Point(20, 20)], [Point(30, 30)], 0, 1),
    ]
    
    for name, sources, targets, layer, priority in nets_data:
        net = Net(name, sources, targets, layer, priority)
        router.add_net(net)
    
    print("Routing Algorithms Demo:")
    print("=" * 50)
    
    # Test different routing strategies
    print("\n1. Maze Routing:")
    results1 = router.route_all_nets("maze")
    stats1 = router.get_routing_statistics()
    print(f"   Success rate: {stats1['routing_success_rate']*100:.1f}%")
    print(f"   Wirelength: {stats1['total_wirelength']:.2f}")
    
    # Reset for next test
    for net in router.nets.values():
        net.routes = []
        net.routed = False
        net.wirelength = 0
    
    print("\n2. Lee's Algorithm:")
    results2 = router.route_all_nets("lee")
    stats2 = router.get_routing_statistics()
    print(f"   Success rate: {stats2['routing_success_rate']*100:.1f}%")
    print(f"   Wirelength: {stats2['total_wirelength']:.2f}")
    
    router.visualize_routing()
