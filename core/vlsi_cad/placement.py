#!/usr/bin/env python3
"""
Placement Algorithms for VLSI Physical Design

Dựa trên các khái niệm VLSI CAD Part 2 cho ASIC placement và tối ưu hóa.
"""

from typing import Dict, List, Set, Any, Tuple, Optional
import math
import random
import logging

logger = logging.getLogger(__name__)

class Cell:
    """Đại diện cho một logic cell trong thiết kế."""
    
    def __init__(self, name: str, width: float, height: float, cell_type: str = "standard"):
        self.name = name
        self.width = width
        self.height = height
        self.cell_type = cell_type
        self.x = 0.0
        self.y = 0.0
        self.fixed = False  # Liệu vị trí cell có cố định không
        self.area = width * height
        
    def set_position(self, x: float, y: float):
        """Đặt vị trí cell."""
        if not self.fixed:
            self.x = x
            self.y = y
    
    def get_center(self) -> Tuple[float, float]:
        """Lấy tọa độ trung tâm cell."""
        return (self.x + self.width/2, self.y + self.height/2)
    
    def __repr__(self):
        return f"Cell({self.name}, {self.width}x{self.height} @ ({self.x:.2f}, {self.y:.2f}))"

class Net:
    """Represents a net connecting multiple cells."""
    
    def __init__(self, name: str, pins: List[str]):
        self.name = name
        self.pins = pins  # List of cell names connected to this net
        self.weight = 1.0  # Net weight for optimization
        
    def get_half_perimeter_wire_length(self, cells: Dict[str, Cell]) -> float:
        """Calculate half-perimeter wire length (HPWL) for this net."""
        if len(self.pins) < 2:
            return 0.0
        
        # Get bounding box
        x_coords = []
        y_coords = []
        
        for pin in self.pins:
            if pin in cells:
                cell = cells[pin]
                x_coords.extend([cell.x, cell.x + cell.width])
                y_coords.extend([cell.y, cell.y + cell.height])
        
        if not x_coords:
            return 0.0
        
        # Calculate bounding box dimensions
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        
        # Half-perimeter wire length
        hpwl = (x_max - x_min) + (y_max - y_min)
        return hpwl * self.weight

class PlacementEngine:
    """
    Placement engine implementing various placement algorithms.
    
    Based on VLSI CAD Part 2 concepts for ASIC placement.
    """
    
    def __init__(self, chip_width: float, chip_height: float):
        self.chip_width = chip_width
        self.chip_height = chip_height
        self.cells: Dict[str, Cell] = {}
        self.nets: Dict[str, Net] = {}
        self.total_wirelength = 0.0
        self.total_area = 0.0
        
    def add_cell(self, cell: Cell):
        """Add a cell to the placement."""
        self.cells[cell.name] = cell
        self.total_area += cell.area
        
    def add_net(self, net: Net):
        """Add a net to the placement."""
        self.nets[net.name] = net
        
    def random_placement(self) -> Dict[str, Cell]:
        """Perform random placement of cells."""
        logger.info("Performing random placement...")
        
        # Calculate placement area (leave some margin)
        margin = 0.1
        placement_width = self.chip_width * (1 - 2 * margin)
        placement_height = self.chip_height * (1 - 2 * margin)
        
        # Place cells randomly
        placed_cells = []
        for cell in self.cells.values():
            if not cell.fixed:
                # Random position within placement area
                max_x = placement_width - cell.width
                max_y = placement_height - cell.height
                
                x = random.uniform(margin * self.chip_width, max_x)
                y = random.uniform(margin * self.chip_height, max_y)
                
                cell.set_position(x, y)
                placed_cells.append(cell)
        
        self._update_wirelength()
        logger.info(f"Random placement completed. Wirelength: {self.total_wirelength:.2f}")
        
        return self.cells.copy()
    
    def force_directed_placement(self, iterations: int = 100) -> Dict[str, Cell]:
        """
        Perform force-directed placement.
        
        Based on spring-mass model where cells are connected by springs.
        """
        logger.info(f"Performing force-directed placement ({iterations} iterations)...")
        
        # Initialize with random placement
        self.random_placement()
        
        for iteration in range(iterations):
            forces = self._calculate_forces()
            self._apply_forces(forces, 0.1)  # Damping factor
            self._update_wirelength()
            
            if iteration % 20 == 0:
                logger.debug(f"Iteration {iteration}: Wirelength = {self.total_wirelength:.2f}")
        
        logger.info(f"Force-directed placement completed. Wirelength: {self.total_wirelength:.2f}")
        return self.cells.copy()
    
    def simulated_annealing_placement(self, initial_temp: float = 1000.0, 
                                    cooling_rate: float = 0.95, 
                                    max_iterations: int = 10000) -> Dict[str, Cell]:
        """
        Perform simulated annealing placement.
        
        Uses simulated annealing to find good placement solution.
        """
        logger.info("Performing simulated annealing placement...")
        
        # Initialize with random placement
        current_placement = self.random_placement()
        current_wirelength = self.total_wirelength
        
        best_placement = current_placement.copy()
        best_wirelength = current_wirelength
        
        temperature = initial_temp
        iteration = 0
        
        while temperature > 1.0 and iteration < max_iterations:
            # Generate neighboring solution
            neighbor_placement = self._generate_neighbor()
            neighbor_wirelength = self._calculate_total_wirelength(neighbor_placement)
            
            # Accept or reject based on temperature and improvement
            delta = neighbor_wirelength - current_wirelength
            
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                # Accept move
                current_placement = neighbor_placement
                current_wirelength = neighbor_wirelength
                
                if current_wirelength < best_wirelength:
                    best_placement = current_placement.copy()
                    best_wirelength = current_wirelength
            
            # Cool down
            temperature *= cooling_rate
            iteration += 1
            
            if iteration % 1000 == 0:
                logger.debug(f"SA iteration {iteration}: T={temperature:.2f}, "
                           f"WL={current_wirelength:.2f}, Best={best_wirelength:.2f}")
        
        # Restore best placement
        self.cells = best_placement
        self.total_wirelength = best_wirelength
        
        logger.info(f"Simulated annealing completed. Best wirelength: {best_wirelength:.2f}")
        return self.cells.copy()
    
    def _calculate_forces(self) -> Dict[str, Tuple[float, float]]:
        """Calculate forces acting on each cell."""
        forces = {}
        
        for cell_name in self.cells:
            forces[cell_name] = (0.0, 0.0)
        
        # Calculate forces from nets (attraction between connected cells)
        for net in self.nets.values():
            if len(net.pins) < 2:
                continue
            
            # Calculate net center of mass
            total_x, total_y = 0.0, 0.0
            pin_count = 0
            
            for pin in net.pins:
                if pin in self.cells:
                    cell = self.cells[pin]
                    center_x, center_y = cell.get_center()
                    total_x += center_x
                    total_y += center_y
                    pin_count += 1
            
            if pin_count == 0:
                continue
            
            net_center_x = total_x / pin_count
            net_center_y = total_y / pin_count
            
            # Apply attraction force to each pin
            for pin in net.pins:
                if pin in self.cells:
                    cell = self.cells[pin]
                    center_x, center_y = cell.get_center()
                    
                    # Force proportional to distance from net center
                    fx = (net_center_x - center_x) * 0.1
                    fy = (net_center_y - center_y) * 0.1
                    
                    forces[pin] = (forces[pin][0] + fx, forces[pin][1] + fy)
        
        return forces
    
    def _apply_forces(self, forces: Dict[str, Tuple[float, float]], damping: float):
        """Apply forces to cells with damping."""
        for cell_name, (fx, fy) in forces.items():
            if cell_name in self.cells:
                cell = self.cells[cell_name]
                if not cell.fixed:
                    # Apply force with damping
                    new_x = cell.x + fx * damping
                    new_y = cell.y + fy * damping
                    
                    # Keep within bounds
                    new_x = max(0, min(new_x, self.chip_width - cell.width))
                    new_y = max(0, min(new_y, self.chip_height - cell.height))
                    
                    cell.set_position(new_x, new_y)
    
    def _generate_neighbor(self) -> Dict[str, Cell]:
        """Generate a neighboring placement by moving a random cell."""
        neighbor = {}
        for name, cell in self.cells.items():
            neighbor[name] = Cell(cell.name, cell.width, cell.height, cell.cell_type)
            neighbor[name].x = cell.x
            neighbor[name].y = cell.y
            neighbor[name].fixed = cell.fixed
        
        # Move a random non-fixed cell
        movable_cells = [name for name, cell in neighbor.items() if not cell.fixed]
        if not movable_cells:
            return neighbor
        
        cell_to_move = random.choice(movable_cells)
        cell = neighbor[cell_to_move]
        
        # Random displacement
        max_displacement = min(self.chip_width, self.chip_height) * 0.1
        dx = random.uniform(-max_displacement, max_displacement)
        dy = random.uniform(-max_displacement, max_displacement)
        
        new_x = max(0, min(cell.x + dx, self.chip_width - cell.width))
        new_y = max(0, min(cell.y + dy, self.chip_height - cell.height))
        
        cell.set_position(new_x, new_y)
        
        return neighbor
    
    def _update_wirelength(self):
        """Update total wirelength."""
        self.total_wirelength = self._calculate_total_wirelength(self.cells)
    
    def _calculate_total_wirelength(self, cells: Dict[str, Cell]) -> float:
        """Calculate total wirelength for given cell positions."""
        total_wl = 0.0
        for net in self.nets.values():
            total_wl += net.get_half_perimeter_wire_length(cells)
        return total_wl
    
    def get_placement_statistics(self) -> Dict[str, Any]:
        """Get placement statistics."""
        return {
            'total_cells': len(self.cells),
            'total_nets': len(self.nets),
            'total_wirelength': self.total_wirelength,
            'total_area': self.total_area,
            'area_utilization': self.total_area / (self.chip_width * self.chip_height),
            'average_net_degree': sum(len(net.pins) for net in self.nets.values()) / len(self.nets) if self.nets else 0
        }
    
    def visualize_placement(self, filename: str = "placement.svg"):
        """Visualize placement (simplified text output)."""
        print(f"\nPlacement Visualization:")
        print(f"Chip dimensions: {self.chip_width} x {self.chip_height}")
        print(f"Total cells: {len(self.cells)}")
        print(f"Total wirelength: {self.total_wirelength:.2f}")
        print(f"Area utilization: {self.total_area/(self.chip_width*self.chip_height)*100:.1f}%")
        
        print(f"\nCell positions:")
        for name, cell in self.cells.items():
            print(f"  {name}: ({cell.x:.2f}, {cell.y:.2f}) - {cell.width}x{cell.height}")

# Alias for backward compatibility
Placement = PlacementEngine

# Example usage and testing
if __name__ == "__main__":
    # Create placement engine
    engine = PlacementEngine(1000.0, 1000.0)
    
    # Add cells
    cells_data = [
        ("cell1", 50, 50),
        ("cell2", 60, 40),
        ("cell3", 45, 55),
        ("cell4", 55, 45),
        ("cell5", 40, 60),
    ]
    
    for name, width, height in cells_data:
        cell = Cell(name, width, height)
        engine.add_cell(cell)
    
    # Add nets
    nets_data = [
        ("net1", ["cell1", "cell2", "cell3"]),
        ("net2", ["cell2", "cell4"]),
        ("net3", ["cell1", "cell4", "cell5"]),
        ("net4", ["cell3", "cell5"]),
    ]
    
    for name, pins in nets_data:
        net = Net(name, pins)
        engine.add_net(net)
    
    print("Placement Algorithms Demo:")
    print("=" * 50)
    
    # Test different placement algorithms
    print("\n1. Random Placement:")
    random_placement = engine.random_placement()
    stats = engine.get_placement_statistics()
    print(f"   Wirelength: {stats['total_wirelength']:.2f}")
    
    print("\n2. Force-Directed Placement:")
    force_placement = engine.force_directed_placement(50)
    stats = engine.get_placement_statistics()
    print(f"   Wirelength: {stats['total_wirelength']:.2f}")
    
    print("\n3. Simulated Annealing Placement:")
    sa_placement = engine.simulated_annealing_placement(1000, 0.95, 1000)
    stats = engine.get_placement_statistics()
    print(f"   Wirelength: {stats['total_wirelength']:.2f}")
    
    print("\nFinal Statistics:")
    engine.visualize_placement()
