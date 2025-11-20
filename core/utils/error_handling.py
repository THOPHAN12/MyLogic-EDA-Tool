"""
Error handling and validation utilities for MyLogic EDA Tool.
"""

from typing import Dict, Any, List, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class MyLogicError(Exception):
    """Base exception for MyLogic EDA Tool."""
    pass


class ValidationError(MyLogicError):
    """Raised when netlist validation fails."""
    pass


class OptimizationError(MyLogicError):
    """Raised when optimization fails."""
    pass


class ParserError(MyLogicError):
    """Raised when parsing fails."""
    pass


def validate_netlist(netlist: Dict[str, Any], strict: bool = True) -> List[str]:
    """
    Validate netlist structure and return list of errors.
    
    Args:
        netlist: Netlist dictionary to validate
        strict: If True, raise ValidationError on errors
        
    Returns:
        List of error messages (empty if valid)
        
    Raises:
        ValidationError: If strict=True and errors found
    """
    errors = []
    
    # Check required fields
    required_fields = ['name', 'inputs', 'outputs', 'nodes', 'wires']
    for field in required_fields:
        if field not in netlist:
            errors.append(f"Missing required field: '{field}'")
    
    if errors and strict:
        raise ValidationError(f"Netlist validation failed: {', '.join(errors)}")
    
    # Validate types
    if 'inputs' in netlist and not isinstance(netlist['inputs'], list):
        errors.append("'inputs' must be a list")
    
    if 'outputs' in netlist and not isinstance(netlist['outputs'], list):
        errors.append("'outputs' must be a list")
    
    if 'nodes' in netlist:
        if not isinstance(netlist['nodes'], (dict, list)):
            errors.append("'nodes' must be a dict or list")
        else:
            # Validate node structure
            nodes = netlist['nodes']
            if isinstance(nodes, dict):
                nodes_iter = nodes.items()
            else:
                nodes_iter = enumerate(nodes)
            
            for node_id, node in nodes_iter:
                if not isinstance(node, dict):
                    errors.append(f"Node {node_id} must be a dict")
                    continue
                
                if 'type' not in node:
                    errors.append(f"Node {node_id} missing 'type' field")
                # Accept 'id', 'output', or 'name' field for node identification
                if 'output' not in node and 'name' not in node and 'id' not in node:
                    errors.append(f"Node {node_id} missing 'output', 'name', or 'id' field")
    
    if 'wires' in netlist:
        if not isinstance(netlist['wires'], (dict, list)):
            errors.append("'wires' must be a dict or list")
    
    # Validate outputs exist in nodes
    if 'outputs' in netlist and 'nodes' in netlist:
        outputs = netlist['outputs']
        nodes = netlist['nodes']
        
        # Get node IDs
        if isinstance(nodes, dict):
            node_ids = {node.get('output') or node.get('name') or node.get('id') for node in nodes.values()}
        else:
            node_ids = {node.get('output') or node.get('name') or node.get('id') for node in nodes}
        
        # Check output_mapping in attrs (if present)
        attrs = netlist.get('attrs', {})
        output_mapping = attrs.get('output_mapping', {})
        
        for output in outputs:
            # Check if output is directly a node ID or input
            if output in node_ids or output in netlist.get('inputs', []):
                continue
            # Check if output is mapped in output_mapping
            if output in output_mapping:
                mapped_node = output_mapping[output]
                if mapped_node in node_ids or mapped_node in netlist.get('inputs', []):
                    continue
            # Output not found
            errors.append(f"Output '{output}' not found in nodes or inputs")
    
    if errors and strict:
        raise ValidationError(f"Netlist validation failed: {', '.join(errors)}")
    
    return errors


def safe_optimize(
    optimizer_func: Callable[[Dict[str, Any]], Dict[str, Any]],
    netlist: Dict[str, Any],
    error_message: str = "Optimization failed"
) -> Dict[str, Any]:
    """
    Safely run optimization with error handling.
    
    Args:
        optimizer_func: Optimization function to call
        netlist: Netlist to optimize
        error_message: Error message prefix
        
    Returns:
        Optimized netlist
        
    Raises:
        OptimizationError: If optimization fails
    """
    try:
        # Validate input
        validate_netlist(netlist, strict=False)
        
        # Run optimization
        result = optimizer_func(netlist)
        
        # Validate output
        validate_netlist(result, strict=False)
        
        return result
        
    except ValidationError as e:
        logger.error(f"{error_message}: Validation error: {e}")
        raise OptimizationError(f"{error_message}: {e}") from e
    except Exception as e:
        logger.error(f"{error_message}: {type(e).__name__}: {e}")
        raise OptimizationError(f"{error_message}: {e}") from e


def validate_file_path(file_path: str, must_exist: bool = True) -> str:
    """
    Validate file path.
    
    Args:
        file_path: Path to validate
        must_exist: If True, file must exist
        
    Returns:
        Normalized file path
        
    Raises:
        FileNotFoundError: If must_exist=True and file doesn't exist
        ValueError: If path is invalid
    """
    import os
    
    if not file_path or not isinstance(file_path, str):
        raise ValueError("File path must be a non-empty string")
    
    normalized = os.path.normpath(file_path)
    
    if must_exist and not os.path.exists(normalized):
        raise FileNotFoundError(f"File not found: {normalized}")
    
    return normalized


def safe_parse(
    parser_func: Callable[[str], Dict[str, Any]],
    file_path: str
) -> Dict[str, Any]:
    """
    Safely parse file with error handling.
    
    Args:
        parser_func: Parser function to call
        file_path: Path to file to parse
        
    Returns:
        Parsed netlist
        
    Raises:
        ParserError: If parsing fails
    """
    try:
        validated_path = validate_file_path(file_path, must_exist=True)
        result = parser_func(validated_path)
        
        # Validate parsed result
        validate_netlist(result, strict=False)
        
        return result
        
    except FileNotFoundError as e:
        logger.error(f"Parser error: File not found: {e}")
        raise ParserError(f"File not found: {e}") from e
    except ValidationError as e:
        logger.error(f"Parser error: Invalid netlist: {e}")
        raise ParserError(f"Invalid netlist: {e}") from e
    except Exception as e:
        logger.error(f"Parser error: {type(e).__name__}: {e}")
        raise ParserError(f"Parsing failed: {e}") from e

