#!/usr/bin/env python3
"""
Technology Library Loader - MyLogic EDA Tool

Tải và quản lý các thư viện công nghệ từ nhiều format khác nhau.
Hỗ trợ: Verilog, Liberty (.lib), JSON, và custom formats.
"""

import json
import os
import re
import sys
from typing import Dict, List, Any, Optional
import logging

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from core.technology_mapping.technology_mapping import LibraryCell, TechnologyLibrary

logger = logging.getLogger(__name__)

class LibraryLoader:
    """
    Technology Library Loader cho MyLogic EDA Tool.
    
    Hỗ trợ load thư viện từ:
    - Verilog files (.v)
    - Liberty files (.lib)
    - JSON files (.json)
    - Custom Python libraries
    """
    
    def __init__(self, techlibs_dir: str = "techlibs"):
        self.techlibs_dir = techlibs_dir
        self.loaded_libraries: Dict[str, TechnologyLibrary] = {}
        
    def load_verilog_library(self, filename: str) -> TechnologyLibrary:
        """
        Load thư viện từ Verilog file.
        
        Args:
            filename: Tên file Verilog (.v)
            
        Returns:
            TechnologyLibrary object
        """
        filepath = os.path.join(self.techlibs_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Verilog library file not found: {filepath}")
        
        library = TechnologyLibrary(filename.replace('.v', ''))
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse Verilog modules
        module_pattern = r'module\s+(\w+)\s*\(([^)]+)\);'
        modules = re.findall(module_pattern, content)
        
        for module_name, ports in modules:
            # Parse input/output ports
            inputs = []
            outputs = []
            
            port_pattern = r'(input|output)\s+([^,;]+)'
            port_matches = re.findall(port_pattern, ports)
            
            for direction, port_names in port_matches:
                # Parse individual ports
                ports_list = [p.strip() for p in port_names.split(',')]
                
                for port in ports_list:
                    # Remove array declarations [N:0]
                    port = re.sub(r'\[[^\]]+\]', '', port).strip()
                    if direction == 'input':
                        inputs.append(port)
                    else:
                        outputs.append(port)
            
            # Estimate area và delay dựa trên số inputs
            area = 1.0 + len(inputs) * 0.2
            delay = 0.1 + len(inputs) * 0.02
            
            # Create LibraryCell
            cell = LibraryCell(
                name=module_name,
                function=f"module_{module_name}",  # Placeholder
                area=area,
                delay=delay,
                input_pins=inputs,
                output_pins=outputs
            )
            
            library.add_cell(cell)
            logger.debug(f"Loaded Verilog cell: {module_name}")
        
        self.loaded_libraries[library.name] = library
        logger.info(f"Loaded Verilog library: {filename} with {len(library.cells)} cells")
        return library
    
    def load_liberty_library(self, filename: str) -> TechnologyLibrary:
        """
        Load thư viện từ Liberty file (.lib).
        
        Args:
            filename: Tên file Liberty (.lib)
            
        Returns:
            TechnologyLibrary object
        """
        filepath = os.path.join(self.techlibs_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Liberty library file not found: {filepath}")
        
        library = TechnologyLibrary(filename.replace('.lib', ''))
        
        with open(filepath, 'r') as f:
            content = f.read()
        
        # Parse Liberty format (simplified)
        cell_pattern = r'cell\s*\(\s*(\w+)\s*\)\s*\{([^}]+)\}'
        cells = re.findall(cell_pattern, content, re.DOTALL)
        
        for cell_name, cell_content in cells:
            # Extract area
            area_match = re.search(r'area\s*:\s*([\d.]+)', cell_content)
            area = float(area_match.group(1)) if area_match else 1.0
            
            # Extract pins
            pin_pattern = r'pin\s*\(\s*(\w+)\s*\)\s*\{([^}]+)\}'
            pins = re.findall(pin_pattern, cell_content)
            
            inputs = []
            outputs = []
            
            for pin_name, pin_content in pins:
                direction_match = re.search(r'direction\s*:\s*(\w+)', pin_content)
                if direction_match:
                    direction = direction_match.group(1)
                    if direction == 'input':
                        inputs.append(pin_name)
                    elif direction == 'output':
                        outputs.append(pin_name)
            
            # Estimate delay (simplified)
            delay = 0.1 + len(inputs) * 0.02
            
            # Create LibraryCell
            cell = LibraryCell(
                name=cell_name,
                function=f"liberty_{cell_name}",  # Placeholder
                area=area,
                delay=delay,
                input_pins=inputs,
                output_pins=outputs
            )
            
            library.add_cell(cell)
            logger.debug(f"Loaded Liberty cell: {cell_name}")
        
        self.loaded_libraries[library.name] = library
        logger.info(f"Loaded Liberty library: {filename} with {len(library.cells)} cells")
        return library
    
    def load_json_library(self, filename: str) -> TechnologyLibrary:
        """
        Load thư viện từ JSON file.
        
        Args:
            filename: Tên file JSON (.json)
            
        Returns:
            TechnologyLibrary object
        """
        filepath = os.path.join(self.techlibs_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"JSON library file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        library = TechnologyLibrary(data.get('library_name', filename.replace('.json', '')))
        
        # Load LUT cells
        lut4_cells = data.get('lut4_cells', {})
        lut6_cells = data.get('lut6_cells', {})
        
        for cell_name, cell_data in lut4_cells.items():
            cell = LibraryCell(
                name=cell_name,
                function=cell_data['function'],
                area=cell_data['area'],
                delay=cell_data['delay'],
                input_pins=['A', 'B', 'C', 'D'],  # Standard LUT4 inputs
                output_pins=['Y']
            )
            library.add_cell(cell)
            logger.debug(f"Loaded JSON LUT4 cell: {cell_name}")
        
        for cell_name, cell_data in lut6_cells.items():
            cell = LibraryCell(
                name=cell_name,
                function=cell_data['function'],
                area=cell_data['area'],
                delay=cell_data['delay'],
                input_pins=['A', 'B', 'C', 'D', 'E', 'F'],  # Standard LUT6 inputs
                output_pins=['Y']
            )
            library.add_cell(cell)
            logger.debug(f"Loaded JSON LUT6 cell: {cell_name}")
        
        # Load memory elements
        memory_elements = data.get('memory_elements', {})
        for cell_name, cell_data in memory_elements.items():
            inputs = ['D', 'CLK']
            if 'reset' in cell_data.get('type', '').lower():
                inputs.append('RST')
            if 'enable' in cell_data.get('type', '').lower():
                inputs.append('EN')
            
            cell = LibraryCell(
                name=cell_name,
                function=f"memory_{cell_name}",
                area=cell_data['area'],
                delay=cell_data['delay'],
                input_pins=inputs,
                output_pins=['Q']
            )
            library.add_cell(cell)
            logger.debug(f"Loaded JSON memory cell: {cell_name}")
        
        self.loaded_libraries[library.name] = library
        logger.info(f"Loaded JSON library: {filename} with {len(library.cells)} cells")
        return library
    
    def load_all_libraries(self) -> Dict[str, TechnologyLibrary]:
        """
        Load tất cả thư viện trong techlibs directory.
        
        Returns:
            Dictionary of loaded libraries
        """
        if not os.path.exists(self.techlibs_dir):
            logger.warning(f"Techlibs directory not found: {self.techlibs_dir}")
            return {}
        
        libraries = {}
        
        # Load Verilog libraries
        for filename in os.listdir(self.techlibs_dir):
            if filename.endswith('.v'):
                try:
                    lib = self.load_verilog_library(filename)
                    libraries[lib.name] = lib
                except Exception as e:
                    logger.error(f"Failed to load Verilog library {filename}: {e}")
        
        # Load Liberty libraries
        for filename in os.listdir(self.techlibs_dir):
            if filename.endswith('.lib'):
                try:
                    lib = self.load_liberty_library(filename)
                    libraries[lib.name] = lib
                except Exception as e:
                    logger.error(f"Failed to load Liberty library {filename}: {e}")
        
        # Load JSON libraries
        for filename in os.listdir(self.techlibs_dir):
            if filename.endswith('.json'):
                try:
                    lib = self.load_json_library(filename)
                    libraries[lib.name] = lib
                except Exception as e:
                    logger.error(f"Failed to load JSON library {filename}: {e}")
        
        logger.info(f"Loaded {len(libraries)} technology libraries")
        return libraries
    
    def get_library(self, name: str) -> Optional[TechnologyLibrary]:
        """
        Lấy thư viện theo tên.
        
        Args:
            name: Tên thư viện
            
        Returns:
            TechnologyLibrary object hoặc None
        """
        return self.loaded_libraries.get(name)
    
    def list_available_libraries(self) -> List[str]:
        """
        Liệt kê tất cả thư viện có sẵn.
        
        Returns:
            List of library names
        """
        return list(self.loaded_libraries.keys())
    
    def get_library_info(self, name: str) -> Dict[str, Any]:
        """
        Lấy thông tin chi tiết về thư viện.
        
        Args:
            name: Tên thư viện
            
        Returns:
            Dictionary with library information
        """
        library = self.get_library(name)
        if not library:
            return {}
        
        return {
            'name': library.name,
            'total_cells': len(library.cells),
            'cell_names': list(library.cells.keys()),
            'functions': list(library.function_map.keys()),
            'average_area': sum(cell.area for cell in library.cells.values()) / len(library.cells),
            'average_delay': sum(cell.delay for cell in library.cells.values()) / len(library.cells)
        }

def test_library_loader():
    """Test library loader functionality."""
    print("Testing Technology Library Loader...")
    
    loader = LibraryLoader()
    
    try:
        # Load all libraries
        libraries = loader.load_all_libraries()
        
        print(f"\nLoaded {len(libraries)} libraries:")
        for name, library in libraries.items():
            print(f"  - {name}: {len(library.cells)} cells")
        
        # Test specific library loading
        if 'standard_cells' in libraries:
            lib_info = loader.get_library_info('standard_cells')
            print(f"\nStandard Cells Library Info:")
            print(f"  Total cells: {lib_info['total_cells']}")
            print(f"  Average area: {lib_info['average_area']:.2f}")
            print(f"  Average delay: {lib_info['average_delay']:.3f}")
            print(f"  Cell names: {lib_info['cell_names'][:5]}...")  # Show first 5
        
        print("Library loader test completed!")
        
    except Exception as e:
        print(f"Library loader test failed: {e}")

if __name__ == "__main__":
    test_library_loader()
