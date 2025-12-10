#!/usr/bin/env python3
"""
Library Loader for Technology Mapping

Hỗ trợ load thư viện từ nhiều format:
- Liberty (.lib) - Industry standard
- JSON (.json) - Easy to use
- Verilog (.v) - Basic support

Author: MyLogic EDA Tool Team
"""

import os
import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple

from .technology_mapping import TechnologyLibrary, LibraryCell

logger = logging.getLogger(__name__)


def load_library(file_path: str, library_type: Optional[str] = None) -> TechnologyLibrary:
    """
    Load technology library from file with auto-detection.
    
    Args:
        file_path: Path to library file
        library_type: "liberty", "json", "verilog", or None (auto-detect)
        
    Returns:
        TechnologyLibrary object
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If format is unsupported
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Library file not found: {file_path}")
    
    if library_type is None:
        # Auto-detect from extension
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.lib':
            library_type = 'liberty'
        elif ext == '.json':
            library_type = 'json'
        elif ext == '.v':
            library_type = 'verilog'
        else:
            raise ValueError(f"Unknown library format: {ext}. Supported: .lib, .json, .v")
    
    logger.info(f"Loading library from {file_path} (format: {library_type})")
    
    if library_type == 'liberty':
        return load_liberty_library(file_path)
    elif library_type == 'json':
        return load_json_library(file_path)
    elif library_type == 'verilog':
        return load_verilog_library(file_path)
    else:
        raise ValueError(f"Unsupported library type: {library_type}")


def load_liberty_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from Liberty format file.
    
    Liberty format là industry standard cho ASIC cell libraries.
    
    Args:
        file_path: Path to .lib file
        
    Returns:
        TechnologyLibrary object
    """
    logger.info(f"Parsing Liberty library: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract library name
    lib_name_match = re.search(r'library\s*\(([^)]+)\)', content)
    library_name = lib_name_match.group(1) if lib_name_match else "loaded_library"
    
    library = TechnologyLibrary(library_name)
    
    # Parse cells: cell (NAME) { ... }
    # Liberty format có nested braces, cần parse cẩn thận bằng cách đếm braces
    cells_parsed = 0
    
    # Find all cell declarations
    cell_start_pattern = r'cell\s*\((\w+)\)\s*\{'
    cell_starts = list(re.finditer(cell_start_pattern, content))
    
    for i, cell_start_match in enumerate(cell_starts):
        cell_name = cell_start_match.group(1)
        start_pos = cell_start_match.end()  # Position after opening brace
        
        # Find matching closing brace by counting braces
        brace_count = 1
        pos = start_pos
        end_pos = len(content)
        
        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_pos = pos
                    break
            pos += 1
        
        # Extract cell body (without the closing brace)
        cell_body = content[start_pos:end_pos]
        
        try:
            # Extract area
            area_match = re.search(r'area\s*:\s*([\d.]+)', cell_body)
            area = float(area_match.group(1)) if area_match else 1.0
            
            logger.debug(f"Parsing cell: {cell_name}, area: {area}")
            
            # Extract function from output pin
            # Look for pin(Y) { function : "..." }
            function = None
            func_match = re.search(r'pin\s*\((\w+)\)\s*\{[^}]*function\s*:\s*"([^"]+)"', cell_body, re.DOTALL)
            if func_match:
                output_pin = func_match.group(1)
                function = func_match.group(2)
                # Convert Liberty function to standard format
                # "!A" -> "NOT(A)", "A&B" -> "AND(A,B)", etc.
                function = _convert_liberty_function(function)
            else:
                # Try to infer from cell name
                function = _infer_function_from_name(cell_name)
            
            # Extract pins
            input_pins = []
            output_pins = []
            
            pin_pattern = r'pin\s*\((\w+)\)\s*\{([^}]+)\}'
            for pin_match in re.finditer(pin_pattern, cell_body, re.DOTALL):
                pin_name = pin_match.group(1)
                pin_body = pin_match.group(2)
                
                direction_match = re.search(r'direction\s*:\s*(\w+)', pin_body)
                direction = direction_match.group(1).lower() if direction_match else "input"
                
                if direction == "output":
                    output_pins.append(pin_name)
                else:
                    input_pins.append(pin_name)
            
            # Extract delay (simplified - use average of timing values if available)
            delay = _extract_delay_from_liberty(cell_body)
            
            # Create cell
            if function:
                cell = LibraryCell(
                    name=cell_name,
                    function=function,
                    area=area,
                    delay=delay,
                    input_pins=input_pins,
                    output_pins=output_pins
                )
                library.add_cell(cell)
                cells_parsed += 1
                logger.debug(f"Parsed cell: {cell_name} - {function}")
        
        except Exception as e:
            logger.warning(f"Failed to parse cell {cell_name}: {e}")
            continue
    
    logger.info(f"Loaded {cells_parsed} cells from Liberty library")
    return library


def _convert_liberty_function(func_str: str) -> str:
    """
    Convert Liberty function format to standard format.
    
    Examples:
        "!A" -> "NOT(A)"
        "A&B" -> "AND(A,B)"
        "A|B" -> "OR(A,B)"
        "A^B" -> "XOR(A,B)"
        "!(A&B)" -> "NAND(A,B)"
        "!(A|B)" -> "NOR(A,B)"
    """
    func_str = func_str.strip()
    
    # Handle NOT
    if func_str.startswith('!'):
        inner = func_str[1:].strip()
        if '(' in inner:
            # Complex NOT like "!(A&B)"
            inner_func = inner[1:-1] if inner.startswith('(') and inner.endswith(')') else inner
            if '&' in inner_func:
                return f"NAND({inner_func.replace('&', ',').replace(' ', '')})"
            elif '|' in inner_func:
                return f"NOR({inner_func.replace('|', ',').replace(' ', '')})"
            else:
                return f"NOT({inner_func})"
        else:
            return f"NOT({inner})"
    
    # Handle AND
    if '&' in func_str:
        parts = [p.strip() for p in func_str.split('&')]
        return f"AND({','.join(parts)})"
    
    # Handle OR
    if '|' in func_str:
        parts = [p.strip() for p in func_str.split('|')]
        return f"OR({','.join(parts)})"
    
    # Handle XOR
    if '^' in func_str:
        parts = [p.strip() for p in func_str.split('^')]
        return f"XOR({','.join(parts)})"
    
    # Default: return as is
    return func_str


def _infer_function_from_name(cell_name: str) -> str:
    """Infer function from cell name if function not found."""
    name_upper = cell_name.upper()
    
    if name_upper.startswith('INV'):
        return "NOT(A)"
    elif name_upper.startswith('BUF'):
        return "BUF(A)"
    elif name_upper.startswith('NAND'):
        num_inputs = _extract_number_from_name(name_upper, 'NAND')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"NAND({inputs})"
    elif name_upper.startswith('NOR'):
        num_inputs = _extract_number_from_name(name_upper, 'NOR')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"NOR({inputs})"
    elif name_upper.startswith('AND'):
        num_inputs = _extract_number_from_name(name_upper, 'AND')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"AND({inputs})"
    elif name_upper.startswith('OR'):
        num_inputs = _extract_number_from_name(name_upper, 'OR')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"OR({inputs})"
    elif name_upper.startswith('XOR'):
        num_inputs = _extract_number_from_name(name_upper, 'XOR')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"XOR({inputs})"
    elif name_upper.startswith('XNOR'):
        num_inputs = _extract_number_from_name(name_upper, 'XNOR')
        inputs = ','.join([chr(65 + i) for i in range(num_inputs)])
        return f"XNOR({inputs})"
    
    return cell_name


def _extract_number_from_name(name: str, prefix: str) -> int:
    """Extract number from cell name like NAND2 -> 2."""
    if prefix in name:
        remaining = name[len(prefix):]
        # Extract first number
        num_match = re.search(r'\d+', remaining)
        if num_match:
            return int(num_match.group(0))
    return 2  # Default to 2 inputs


def _extract_delay_from_liberty(cell_body: str) -> float:
    """Extract average delay from Liberty timing tables."""
    # Look for timing tables
    timing_pattern = r'timing\s*\(\)\s*\{[^}]*cell_rise[^}]*values\s*\([^)]+\)[^}]*cell_fall[^}]*values\s*\([^)]+\)'
    
    delays = []
    
    # Try to find cell_rise and cell_fall values
    rise_match = re.search(r'cell_rise[^{]*values\s*\([^)]+\)', cell_body, re.DOTALL)
    fall_match = re.search(r'cell_fall[^{]*values\s*\([^)]+\)', cell_body, re.DOTALL)
    
    for match in [rise_match, fall_match]:
        if match:
            values_str = match.group(0)
            # Extract numbers from values("0.1, 0.15, 0.2")
            num_matches = re.findall(r'[\d.]+', values_str)
            for num_str in num_matches:
                try:
                    delays.append(float(num_str))
                except ValueError:
                    pass
    
    if delays:
        return sum(delays) / len(delays)
    
    # Default delay based on cell type
    return 0.1


def load_json_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from JSON file.
    
    JSON format dễ parse và linh hoạt hơn Liberty.
    
    Expected JSON format:
    {
        "name": "library_name",
        "cells": [
            {
                "name": "INV",
                "function": "NOT(A)",
                "area": 1.0,
                "delay": 0.1,
                "input_pins": ["A"],
                "output_pins": ["Y"]
            },
            ...
        ]
    }
    
    Args:
        file_path: Path to .json file
        
    Returns:
        TechnologyLibrary object
    """
    logger.info(f"Parsing JSON library: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    library_name = data.get('name', 'loaded_library')
    library = TechnologyLibrary(library_name)
    
    cells_parsed = 0
    
    for cell_data in data.get('cells', []):
        try:
            cell = LibraryCell(
                name=cell_data['name'],
                function=cell_data.get('function', cell_data['name']),
                area=float(cell_data.get('area', 1.0)),
                delay=float(cell_data.get('delay', 0.1)),
                input_pins=cell_data.get('input_pins', []),
                output_pins=cell_data.get('output_pins', []),
                input_load=float(cell_data.get('input_load', 1.0)),
                output_drive=float(cell_data.get('output_drive', 1.0))
            )
            library.add_cell(cell)
            cells_parsed += 1
            logger.debug(f"Parsed cell: {cell.name} - {cell.function}")
        
        except KeyError as e:
            logger.warning(f"Missing required field in cell data: {e}")
            continue
        except Exception as e:
            logger.warning(f"Failed to parse cell: {e}")
            continue
    
    logger.info(f"Loaded {cells_parsed} cells from JSON library")
    return library


def load_verilog_library(file_path: str) -> TechnologyLibrary:
    """
    Load technology library from Verilog file.
    
    Parse Verilog module definitions as cells.
    Simplified implementation - chỉ extract basic info.
    
    Args:
        file_path: Path to .v file
        
    Returns:
        TechnologyLibrary object
    """
    logger.info(f"Parsing Verilog library: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    library = TechnologyLibrary("verilog_library")
    
    # Parse module definitions
    # Pattern: module CELL_NAME(...) ... endmodule
    module_pattern = r'module\s+(\w+)\s*\([^)]*\)\s*;([^;]+?)endmodule'
    
    cells_parsed = 0
    
    for match in re.finditer(module_pattern, content, re.DOTALL):
        cell_name = match.group(1)
        cell_body = match.group(2)
        
        try:
            # Extract ports
            ports_match = re.search(r'\(([^)]+)\)', match.group(0))
            ports = []
            if ports_match:
                ports = [p.strip() for p in ports_match.group(1).split(',')]
            
            # Try to extract function from assign statements
            assign_match = re.search(r'assign\s+(\w+)\s*=\s*([^;]+);', cell_body)
            function = cell_name  # Default
            
            if assign_match:
                output = assign_match.group(1)
                expr = assign_match.group(2).strip()
                # Convert Verilog expression to function format
                function = _convert_verilog_expression(expr)
            
            # Separate input and output ports (simplified)
            input_pins = ports[:len(ports)//2] if ports else []
            output_pins = ports[len(ports)//2:] if ports else []
            
            # Create cell with default values
            cell = LibraryCell(
                name=cell_name,
                function=function,
                area=1.0,  # Default
                delay=0.1,  # Default
                input_pins=input_pins,
                output_pins=output_pins
            )
            library.add_cell(cell)
            cells_parsed += 1
            logger.debug(f"Parsed cell: {cell_name}")
        
        except Exception as e:
            logger.warning(f"Failed to parse module {cell_name}: {e}")
            continue
    
    logger.info(f"Loaded {cells_parsed} cells from Verilog library")
    return library


def _convert_verilog_expression(expr: str) -> str:
    """Convert Verilog expression to function format."""
    expr = expr.strip()
    
    # Handle bitwise operators
    if '&' in expr:
        parts = [p.strip() for p in expr.split('&')]
        return f"AND({','.join(parts)})"
    elif '|' in expr:
        parts = [p.strip() for p in expr.split('|')]
        return f"OR({','.join(parts)})"
    elif '^' in expr:
        parts = [p.strip() for p in expr.split('^')]
        return f"XOR({','.join(parts)})"
    elif expr.startswith('~'):
        return f"NOT({expr[1:].strip()})"
    
    return expr


def create_json_library_from_liberty(liberty_file: str, json_file: str) -> None:
    """
    Convert Liberty library to JSON format for easier loading.
    
    Args:
        liberty_file: Path to input .lib file
        json_file: Path to output .json file
    """
    library = load_liberty_library(liberty_file)
    
    json_data = {
        "name": library.name,
        "cells": []
    }
    
    for cell_name, cell in library.cells.items():
        json_data["cells"].append({
            "name": cell.name,
            "function": cell.function,
            "area": cell.area,
            "delay": cell.delay,
            "input_pins": cell.input_pins,
            "output_pins": cell.output_pins,
            "input_load": cell.input_load,
            "output_drive": cell.output_drive
        })
    
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2)
    
    logger.info(f"Converted Liberty library to JSON: {json_file}")


# Example usage
if __name__ == "__main__":
    # Test loading Liberty library
    try:
        lib_path = "techlibs/asic/standard_cells.lib"
        if os.path.exists(lib_path):
            library = load_liberty_library(lib_path)
            print(f"Loaded library: {library.name}")
            print(f"Total cells: {len(library.cells)}")
            print("\nCells:")
            for name, cell in library.cells.items():
                print(f"  {name}: {cell.function} (area={cell.area}, delay={cell.delay})")
        else:
            print(f"Library file not found: {lib_path}")
    except Exception as e:
        print(f"Error: {e}")

