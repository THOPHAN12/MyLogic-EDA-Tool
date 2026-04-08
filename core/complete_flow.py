#!/usr/bin/env python3
"""
Complete Flow: Synthesis → Optimization → Technology Mapping

Luồng tự động chạy 3 bước:
1. SYNTHESIS: Netlist → AIG
2. OPTIMIZE: AIG → Optimized AIG
3. TECHMAP: AIG → Technology-mapped netlist

Luồng phù hợp phạm vi đề tài: tổng hợp luận lý, tối ưu, ánh xạ công nghệ.
"""

import sys
import os
from typing import Dict, List, Set, Any, Optional
from pathlib import Path
import logging
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logger = logging.getLogger(__name__)


def _safe_log_msg(msg: str) -> str:
    """Replace Unicode characters with ASCII equivalents for Windows console compatibility."""
    replacements = {
        '→': '->',
        '✅': '[OK]',
        '📄': '[FILE]',
        '⚠️': '[WARN]',
        '⏭️': '[SKIP]',
    }
    result = msg
    for unicode_char, ascii_replacement in replacements.items():
        result = result.replace(unicode_char, ascii_replacement)
    return result


def netlist_to_verilog(netlist: Dict[str, Any], module_name: str) -> str:
    """
    Convert netlist dictionary to Verilog code.
    
    Standalone utility function to enable Verilog output generation
    after synthesis/optimization/techmap steps (like Yosys).
    
    Args:
        netlist: Netlist dictionary with 'inputs', 'outputs', 'nodes'
        module_name: Name for the Verilog module
        
    Returns:
        Verilog code as string
    """
    inputs = netlist.get('inputs', [])
    outputs = netlist.get('outputs', [])
    nodes = netlist.get('nodes', {})
    attrs = netlist.get('attrs', {})
    output_mapping = attrs.get('output_mapping', {})
    
    # Convert nodes dict to list if needed
    if isinstance(nodes, dict):
        nodes_list = list(nodes.values())
        nodes_dict = nodes
    else:
        nodes_list = nodes
        nodes_dict = {node.get('id', f'node_{i}'): node for i, node in enumerate(nodes) if isinstance(node, dict)}
    
    lines = [f"module {module_name}("]
    
    # Port declarations
    if inputs:
        lines.append(f"  input {', '.join(inputs)},")
    if outputs:
        lines.append(f"  output {', '.join(outputs)}")
    
    lines.append(");")
    lines.append("")
    
    # Wire declarations
    # First pass: collect all signals referenced in nodes
    internal_signals = set()
    referenced_signals = set()  # Signals referenced in assign statements
    
    # Pattern to match Verilog constants (e.g., 1'b0, 2'b00, 8'hFF)
    const_pattern = re.compile(r"^\d+'[bdh]\w+$")
    
    # Collect signals that are outputs of nodes
    for node in nodes_list:
        if isinstance(node, dict):
            output = node.get('output', node.get('id', ''))
            if output and output not in inputs and output not in outputs:
                # Skip constant signals (const_True, const_False, and Verilog constants like 1'b0, 2'b00)
                if output not in ['const_True', 'const_False'] and not const_pattern.match(str(output)):
                    internal_signals.add(output)
    
    # Second pass: collect all signals referenced in input_signals
    # This includes temporary signals like _temp_3, _temp_5 that may not have nodes
    for node in nodes_list:
        if not isinstance(node, dict):
            continue
        node_inputs = node.get('inputs', [])
        node_fanins = node.get('fanins', [])
        
        # Collect from fanins
        if node_fanins:
            for fanin in node_fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                    signal = str(fanin[0])
                    if signal not in ['const_True', 'const_False'] and signal not in inputs and signal not in outputs and not const_pattern.match(signal):
                        referenced_signals.add(signal)
                else:
                    signal = str(fanin)
                    if signal not in ['const_True', 'const_False'] and signal not in inputs and signal not in outputs and not const_pattern.match(signal):
                        referenced_signals.add(signal)
        # Collect from inputs
        elif node_inputs:
            for inp in node_inputs:
                signal = str(inp)
                if signal not in ['const_True', 'const_False'] and signal not in inputs and signal not in outputs and not const_pattern.match(signal):
                    referenced_signals.add(signal)
    
    # Also collect signals from output_mapping (temp signals)
    # These are signals that map to nodes but don't have nodes with output field
    output_mapping_signals = set()
    if output_mapping:
        for signal, node_id in output_mapping.items():
            if signal not in inputs and signal not in outputs:
                if signal not in ['const_True', 'const_False'] and not const_pattern.match(str(signal)):
                    output_mapping_signals.add(signal)
                    # Also add to referenced_signals so we create wire declarations
                    referenced_signals.add(signal)
    
    # Combine internal_signals and referenced_signals
    all_internal_signals = internal_signals.union(referenced_signals)
    
    if all_internal_signals:
        lines.append("  // Internal wires")
        for signal in sorted(all_internal_signals):
            lines.append(f"  wire {signal};")
        lines.append("")
    
    # Logic statements
    lines.append("  // Logic implementation")
    
    # First, create assign statements for signals in output_mapping
    # These are temp signals that map to nodes
    if output_mapping and nodes_dict:
        for signal, node_id in output_mapping.items():
            if signal not in inputs and signal not in outputs:
                # Find the node for this signal
                if node_id in nodes_dict:
                    node = nodes_dict[node_id]
                    if isinstance(node, dict):
                        node_type = node.get('type', '')
                        node_inputs = node.get('inputs', [])
                        node_fanins = node.get('fanins', [])
                        
                        # Get input signals
                        input_signals = []
                        if node_fanins:
                            for fanin in node_fanins:
                                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                                    sig = str(fanin[0])
                                    if sig == 'const_True':
                                        sig = "1'b1"
                                    elif sig == 'const_False':
                                        sig = "1'b0"
                                    if len(fanin) > 1 and fanin[1]:
                                        sig = f"~{sig}"
                                    input_signals.append(sig)
                                else:
                                    sig = str(fanin)
                                    if sig == 'const_True':
                                        sig = "1'b1"
                                    elif sig == 'const_False':
                                        sig = "1'b0"
                                    input_signals.append(sig)
                        elif node_inputs:
                            for inp in node_inputs:
                                sig = str(inp)
                                if sig == 'const_True':
                                    sig = "1'b1"
                                elif sig == 'const_False':
                                    sig = "1'b0"
                                input_signals.append(sig)
                        
                        # Generate assign statement
                        if node_type.upper() == 'AND' and len(input_signals) >= 2:
                            expr = " & ".join(input_signals)
                            lines.append(f"  assign {signal} = {expr};")
                        elif node_type.upper() == 'OR' and len(input_signals) >= 2:
                            expr = " | ".join(input_signals)
                            lines.append(f"  assign {signal} = {expr};")
                        elif node_type.upper() in ['NOT', 'INV'] and len(input_signals) >= 1:
                            lines.append(f"  assign {signal} = ~{input_signals[0]};")
                        elif node_type.upper() == 'XOR' and len(input_signals) >= 2:
                            expr = " ^ ".join(input_signals)
                            lines.append(f"  assign {signal} = {expr};")
                        elif node_type.upper() == 'NAND' and len(input_signals) >= 2:
                            expr = " & ".join(input_signals)
                            lines.append(f"  assign {signal} = ~({expr});")
                        elif node_type.upper() == 'NOR' and len(input_signals) >= 2:
                            expr = " | ".join(input_signals)
                            lines.append(f"  assign {signal} = ~({expr});")
                        # Fallback to AND
                        elif len(input_signals) >= 2:
                            expr = " & ".join(input_signals)
                            lines.append(f"  assign {signal} = {expr};")
    
    # Then, create gate instances or assign statements for nodes
    instance_counter = {}  # Track instance numbers for each cell type
    
    for node in nodes_list:
        if not isinstance(node, dict):
            continue
        
        node_type = node.get('type', '')
        node_inputs = node.get('inputs', [])
        node_fanins = node.get('fanins', [])
        output = node.get('output', node.get('id', ''))
        cell_name = node.get('cell_name', '')
        mapped = node.get('mapped', False)
        
        if not output:
            continue
        
        # Get input signals
        if node_fanins:
            input_signals = []
            for fanin in node_fanins:
                if isinstance(fanin, (list, tuple)) and len(fanin) >= 1:
                    signal = str(fanin[0])
                    # Replace const_True/const_False with Verilog literals
                    if signal == 'const_True':
                        signal = "1'b1"
                    elif signal == 'const_False':
                        signal = "1'b0"
                    if len(fanin) > 1 and fanin[1]:  # Inverted
                        signal = f"~{signal}"
                    input_signals.append(signal)
                else:
                    signal = str(fanin)
                    # Replace const_True/const_False with Verilog literals
                    if signal == 'const_True':
                        signal = "1'b1"
                    elif signal == 'const_False':
                        signal = "1'b0"
                    input_signals.append(signal)
        elif node_inputs:
            input_signals = []
            for inp in node_inputs:
                signal = str(inp)
                # Replace const_True/const_False with Verilog literals
                if signal == 'const_True':
                    signal = "1'b1"
                elif signal == 'const_False':
                    signal = "1'b0"
                input_signals.append(signal)
        else:
            continue
        
        # If node is mapped to a library cell, create gate instance
        if mapped and cell_name:
            # Create gate instance: cell_name instance_name (.pin1(sig1), .pin2(sig2), .out(sig_out));
            # Get cell pin names from node (if available) or use default A, B, Y
            cell_pins = node.get('cell_pins', {})
            
            # Default pin names for common gates
            if not cell_pins:
                if len(input_signals) == 1:
                    cell_pins = {'A': input_signals[0], 'Y': output}
                elif len(input_signals) == 2:
                    cell_pins = {'A': input_signals[0], 'B': input_signals[1], 'Y': output}
                elif len(input_signals) == 3:
                    cell_pins = {'A': input_signals[0], 'B': input_signals[1], 'C': input_signals[2], 'Y': output}
                else:
                    # Use positional mapping
                    pin_names = ['A', 'B', 'C', 'D', 'E', 'F'][:len(input_signals)]
                    cell_pins = {pin: sig for pin, sig in zip(pin_names, input_signals)}
                    cell_pins['Y'] = output
            
            # Generate instance name
            if cell_name not in instance_counter:
                instance_counter[cell_name] = 0
            instance_counter[cell_name] += 1
            instance_name = f"{cell_name}_inst{instance_counter[cell_name]}"
            
            # Create instance statement
            pin_connections = []
            for pin, signal in cell_pins.items():
                pin_connections.append(f".{pin}({signal})")
            
            instance_line = f"  {cell_name} {instance_name} ({', '.join(pin_connections)});"
            lines.append(instance_line)
            continue
        
        # Generate Verilog statement (for unmapped nodes)
        node_type_upper = node_type.upper()
        
        # Check if it's a library cell name
        is_library_cell = False
        gate_function = None
        
        if node_type_upper.startswith('AND') and len(input_signals) >= 2:
            gate_function = 'AND'
            is_library_cell = True
        elif node_type_upper.startswith('NAND') and len(input_signals) >= 2:
            gate_function = 'NAND'
            is_library_cell = True
        elif node_type_upper.startswith('OR') and len(input_signals) >= 2 and not node_type_upper.startswith('NOR'):
            gate_function = 'OR'
            is_library_cell = True
        elif node_type_upper.startswith('NOR') and len(input_signals) >= 2:
            gate_function = 'NOR'
            is_library_cell = True
        elif node_type_upper.startswith('XOR') and len(input_signals) >= 2:
            gate_function = 'XOR'
            is_library_cell = True
        elif node_type_upper in ['NOT', 'INV'] and len(input_signals) >= 1:
            gate_function = 'NOT'
            is_library_cell = True
        
        # Generate Verilog based on gate function
        if gate_function == 'AND' or (node_type in ['AND', 'and'] and not is_library_cell):
            if len(input_signals) >= 2:
                expr = " & ".join(input_signals)
                lines.append(f"  assign {output} = {expr};")
        elif gate_function == 'OR' or (node_type in ['OR', 'or'] and not is_library_cell):
            if len(input_signals) >= 2:
                expr = " | ".join(input_signals)
                lines.append(f"  assign {output} = {expr};")
        elif gate_function == 'NOT' or node_type in ['NOT', 'not']:
            if len(input_signals) >= 1:
                lines.append(f"  assign {output} = ~{input_signals[0]};")
        elif gate_function == 'XOR' or node_type in ['XOR', 'xor']:
            if len(input_signals) >= 2:
                expr = " ^ ".join(input_signals)
                lines.append(f"  assign {output} = {expr};")
        elif gate_function == 'NAND' or node_type in ['NAND', 'nand']:
            if len(input_signals) >= 2:
                expr = " & ".join(input_signals)
                lines.append(f"  assign {output} = ~({expr});")
        elif gate_function == 'NOR' or node_type in ['NOR', 'nor']:
            if len(input_signals) >= 2:
                expr = " | ".join(input_signals)
                lines.append(f"  assign {output} = ~({expr});")
        else:
            # Try to extract function from node if available
            function_str = node.get('function', '')
            if function_str:
                # Parse function string like "AND(A,B)" or "NAND(A,B)"
                func_match = re.match(r'^(\w+)\s*\(', function_str)
                if func_match:
                    func_name = func_match.group(1).upper()
                    if func_name in ['AND'] and len(input_signals) >= 2:
                        expr = " & ".join(input_signals)
                        lines.append(f"  assign {output} = {expr};")
                    elif func_name in ['OR'] and len(input_signals) >= 2:
                        expr = " | ".join(input_signals)
                        lines.append(f"  assign {output} = {expr};")
                    elif func_name in ['NAND'] and len(input_signals) >= 2:
                        expr = " & ".join(input_signals)
                        lines.append(f"  assign {output} = ~({expr});")
                    elif func_name in ['NOR'] and len(input_signals) >= 2:
                        expr = " | ".join(input_signals)
                        lines.append(f"  assign {output} = ~({expr});")
                    elif func_name in ['XOR'] and len(input_signals) >= 2:
                        expr = " ^ ".join(input_signals)
                        lines.append(f"  assign {output} = {expr};")
                    elif func_name in ['NOT', 'INV'] and len(input_signals) >= 1:
                        lines.append(f"  assign {output} = ~{input_signals[0]};")
                    else:
                        # Generic gate - use basic AND as fallback
                        if len(input_signals) >= 2:
                            expr = " & ".join(input_signals)
                            lines.append(f"  assign {output} = {expr};")
                else:
                    # Generic gate - use basic AND as fallback
                    if len(input_signals) >= 2:
                        expr = " & ".join(input_signals)
                        lines.append(f"  assign {output} = {expr};")
            else:
                # Generic gate - use basic AND as fallback
                if len(input_signals) >= 2:
                    expr = " & ".join(input_signals)
                    lines.append(f"  assign {output} = {expr};")
    
    lines.append("")
    lines.append("endmodule")
    
    return "\n".join(lines)


def run_complete_flow(
    netlist: Dict[str, Any],
    techmap_library = None,
    enable_optimization: bool = True,
    enable_techmap: bool = True,
    output_dir: Optional[str] = None,
    write_verilog: bool = True,
    techmap_merge_standard_library: bool = True,
) -> Dict[str, Any]:
    """
    Chạy complete flow: Synthesis → Optimization → Technology Mapping (một chuẩn duy nhất).
    
    Flow:
    1. SYNTHESIS: Netlist → AIG
    2. OPTIMIZATION: AIG → Optimized AIG
    3. TECHMAP (optional): AIG → Technology-mapped netlist (luôn area_optimal).

    Args:
        netlist: Circuit netlist dictionary từ parser
        techmap_library: Technology library object (None = auto-load standard library)
        enable_optimization: Có chạy optimization không (default: True)
        enable_techmap: Có chạy technology mapping không (default: True)
        output_dir: Directory để lưu output Verilog files (None = current directory)
        write_verilog: Có xuất file .v sau mỗi bước không (default: True, giống Yosys)
        techmap_merge_standard_library: Gộp thư viện generic vào techmap (default: True).
            Đặt False để chỉ dùng thư viện đã truyền (ví dụ thuần Sky130).
        
    Returns:
        Dictionary chứa kết quả của tất cả các bước:
        {
            'synthesis': {
                'aig': AIG object,
                'netlist': Synthesized netlist (converted back from AIG),
                'stats': synthesis statistics
            },
            'optimization': {
                'aig': Optimized AIG object,
                'netlist': Optimized netlist (converted back from AIG),
                'stats': optimization statistics,
                'enabled': bool
            },
            'techmap': {
                'results': techmap results,
                'enabled': bool
            },
            'output_files': {
                'syn': path to *_syn.v (if write_verilog=True),
                'opt': path to *_opt.v (if optimization enabled),
                'mapped': path to mapped.v (if techmap enabled)
            }
        }
        
    Examples:
        >>> from parsers import parse_verilog
        >>> from core.complete_flow import run_complete_flow
        >>> 
        >>> netlist = parse_verilog("design.v")
        >>> results = run_complete_flow(netlist)
        >>> 
        >>> # Access results
        >>> synthesized_aig = results['synthesis']['aig']
        >>> optimized_aig = results['optimization']['aig']
        >>> techmap_results = results['techmap']['results']
    """
    logger.info("=" * 70)
    logger.info(_safe_log_msg("COMPLETE FLOW: Synthesis -> Optimization -> Technology Mapping"))
    logger.info("=" * 70)
    
    # Get module name from netlist
    module_name = netlist.get('name', 'design')
    
    # Setup output directory
    if output_dir is None:
        output_dir = Path.cwd()
    else:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
    
    results = {
        'synthesis': {},
        'optimization': {'enabled': enable_optimization},
        'techmap': {'enabled': enable_techmap},
        'output_files': {}  # Track generated Verilog files
    }
    
    # ============================================================
    # STEP 1: SYNTHESIS (Netlist → AIG)
    # ============================================================
    logger.info("\n[STEP 1] SYNTHESIS: Netlist -> AIG")
    logger.info("-" * 70)
    
    try:
        from core.synthesis.synthesis_flow import synthesize
        
        original_nodes = len(netlist.get('nodes', {})) if isinstance(netlist.get('nodes'), dict) else len(netlist.get('nodes', []))
        logger.info(f"Input netlist: {original_nodes} nodes")
        
        # Run synthesis
        aig = synthesize(netlist)
        
        synthesis_stats = {
            'netlist_nodes': original_nodes,
            'aig_nodes': aig.count_nodes(),
            'aig_and_nodes': aig.count_and_nodes(),
            'primary_inputs': len(aig.pis),
            'primary_outputs': len(aig.pos)
        }
        
        results['synthesis'] = {
            'aig': aig,
            'stats': synthesis_stats
        }
        
        logger.info(_safe_log_msg(f"[OK] Synthesis completed: {synthesis_stats['netlist_nodes']} nodes -> {synthesis_stats['aig_nodes']} AIG nodes"))
        
        # Convert AIG to netlist for verification
        from core.synthesis.aig import aig_to_netlist
        synthesized_netlist = aig_to_netlist(aig, netlist)
        results['synthesis']['netlist'] = synthesized_netlist
        
        # Write Verilog file after synthesis (like Yosys)
        if write_verilog:
            try:
                # IMPORTANT:
                # Use netlist-based Verilog export so vector widths (e.g. sel[1:0]) are preserved.
                # AIG-only export may lose bus information and emit invalid port lists.
                from core.export import netlist_to_verilog as export_netlist_to_verilog
                synthesized_verilog = export_netlist_to_verilog(
                    synthesized_netlist, module_name=f"{module_name}_syn"
                )
                output_file = output_dir / f"{module_name}_syn.v"
                output_file.write_text(synthesized_verilog, encoding='utf-8')
                results['output_files']['syn'] = str(output_file)
                logger.info(_safe_log_msg(f"[FILE] Written: {output_file.name}"))
            except Exception as e:
                logger.warning(f"Could not write synthesized Verilog: {e}")
        
    except Exception as e:
        logger.error(f"[ERROR] Synthesis failed: {e}")
        raise
    
    # NOTE: Simulation/verification removed. This flow only produces artifacts.
    
    # ============================================================
    # STEP 2: OPTIMIZATION (AIG → Optimized AIG)
    # ============================================================
    if enable_optimization:
        logger.info("\n[STEP 2] OPTIMIZATION: AIG -> Optimized AIG")
        logger.info("-" * 70)
        
        try:
            from core.optimization.optimization_flow import optimize
            
            original_aig_nodes = aig.count_nodes()
            logger.info(f"Input AIG: {original_aig_nodes} nodes")
            # Run optimization (một chuẩn duy nhất)
            optimized_aig = optimize(aig)
            
            optimization_stats = {
                'nodes_before': original_aig_nodes,
                'nodes_after': optimized_aig.count_nodes(),
                'reduction': original_aig_nodes - optimized_aig.count_nodes(),
                'reduction_percent': ((original_aig_nodes - optimized_aig.count_nodes()) / original_aig_nodes * 100) if original_aig_nodes > 0 else 0
            }
            
            results['optimization'] = {
                'aig': optimized_aig,
                'stats': optimization_stats,
                'enabled': True
            }
            
            logger.info(_safe_log_msg(f"[OK] Optimization completed: {optimization_stats['nodes_before']} -> {optimization_stats['nodes_after']} nodes"))
            logger.info(f"   Reduction: {optimization_stats['reduction']} nodes ({optimization_stats['reduction_percent']:.1f}%)")
            
            # Convert optimized AIG to netlist for verification
            from core.synthesis.aig import aig_to_netlist
            optimized_netlist = aig_to_netlist(optimized_aig, netlist)
            results['optimization']['netlist'] = optimized_netlist
            
            # Write Verilog file after optimization (like Yosys)
            if write_verilog:
                try:
                    from core.export import netlist_to_verilog as export_netlist_to_verilog
                    optimized_verilog = export_netlist_to_verilog(
                        optimized_netlist, module_name=f"{module_name}_opt"
                    )
                    output_file = output_dir / f"{module_name}_opt.v"
                    output_file.write_text(optimized_verilog, encoding='utf-8')
                    results['output_files']['opt'] = str(output_file)
                    logger.info(_safe_log_msg(f"[FILE] Written: {output_file.name}"))
                except Exception as e:
                    logger.warning(f"Could not write optimized Verilog: {e}")
            
            # Use optimized AIG for next step
            aig = optimized_aig
            
            # NOTE: Simulation/verification removed from project scope
            
        except Exception as e:
            logger.error(f"❌ Optimization failed: {e}")
            logger.warning("Continuing with non-optimized AIG...")
            results['optimization']['enabled'] = False
            results['optimization']['error'] = str(e)
    else:
        logger.info("\n[STEP 2] OPTIMIZATION: SKIPPED")
        results['optimization']['aig'] = aig  # Use original AIG
        results['optimization']['stats'] = {'skipped': True}
    
    # ============================================================
    # STEP 3: TECHNOLOGY MAPPING (AIG → Technology-mapped)
    # ============================================================
    if enable_techmap:
        logger.info("\n[STEP 3] TECHNOLOGY MAPPING: AIG -> Technology-mapped netlist")
        logger.info("-" * 70)
        
        try:
            from core.technology_mapping.technology_mapping import techmap, create_standard_library
            
            input_aig_nodes = aig.count_nodes()
            logger.info(f"Input AIG: {input_aig_nodes} nodes, {aig.count_and_nodes()} AND nodes")
            logger.info("Techmap strategy: area_optimal (fixed for thesis / simple flow)")
            
            # Load library if not provided
            if techmap_library is None:
                logger.info("Loading standard technology library...")
                library = create_standard_library()
                logger.info(f"Loaded library '{library.name}' with {len(library.cells)} cells")
            else:
                library = techmap_library
            
            # Run technology mapping
            techmap_results = techmap(
                aig,
                library,
                "area_optimal",
                merge_standard_library=techmap_merge_standard_library,
            )
            
            results['techmap'] = {
                'results': techmap_results,
                'library_name': library.name,
                'enabled': True
            }
            
            # Store mapper and AIG for gate level netlist generation
            if '_mapper' in techmap_results:
                results['techmap']['_mapper'] = techmap_results['_mapper']
            if '_aig' in techmap_results:
                results['techmap']['_aig'] = techmap_results['_aig']
            
            logger.info(_safe_log_msg(f"[OK] Technology mapping completed:"))
            logger.info(f"   Mapped nodes: {techmap_results['mapped_nodes']}/{techmap_results['total_nodes']}")
            logger.info(f"   Success rate: {techmap_results['mapping_success_rate']*100:.1f}%")
            if 'total_area' in techmap_results:
                logger.info(f"   Total area: {techmap_results['total_area']:.2f}")
            if 'total_delay' in techmap_results:
                logger.info(f"   Total delay: {techmap_results['total_delay']:.2f}")
            
            # Write Verilog file after techmap (like Yosys)
            if write_verilog:
                try:
                    from core.technology_mapping.technology_mapping import convert_mapped_logic_network_to_netlist
                    
                    if '_mapper' in techmap_results and '_aig' in techmap_results:
                        mapper = techmap_results['_mapper']
                        aig_for_mapping = techmap_results['_aig']
                        mapped_netlist = convert_mapped_logic_network_to_netlist(
                            mapper, aig_for_mapping, netlist
                        )
                        mapped_verilog = netlist_to_verilog(mapped_netlist, f"{module_name}_mapped")
                        output_file = output_dir / f"{module_name}_mapped.v"
                        output_file.write_text(mapped_verilog, encoding='utf-8')
                        results['output_files']['mapped'] = str(output_file)
                        logger.info(_safe_log_msg(f"[FILE] Written: {output_file.name}"))
                except Exception as e:
                    logger.warning(f"Could not write mapped Verilog: {e}")
                    import traceback
                    logger.debug(traceback.format_exc())
            
        except Exception as e:
            logger.error(f"❌ Technology mapping failed: {e}")
            logger.warning("Complete flow finished without technology mapping")
            results['techmap']['enabled'] = False
            results['techmap']['error'] = str(e)
    else:
        logger.info("\n[STEP 3] TECHNOLOGY MAPPING: SKIPPED")
        results['techmap']['results'] = {'skipped': True}
    
    # ============================================================
    # NOTE: Simulation/verification removed from project scope
    # ============================================================
    
    # ============================================================
    # SUMMARY
    # ============================================================
    logger.info("\n" + "=" * 70)
    logger.info("COMPLETE FLOW SUMMARY")
    logger.info("=" * 70)
    logger.info(_safe_log_msg(f"Synthesis: [OK] {results['synthesis']['stats']['netlist_nodes']} nodes -> {results['synthesis']['stats']['aig_nodes']} AIG nodes"))
    
    if enable_optimization and results['optimization'].get('stats'):
        opt_stats = results['optimization']['stats']
        logger.info(_safe_log_msg(f"Optimization: [OK] {opt_stats['nodes_before']} -> {opt_stats['nodes_after']} nodes ({opt_stats['reduction_percent']:.1f}% reduction)"))
    else:
        logger.info(_safe_log_msg(f"Optimization: [SKIP] SKIPPED"))
    
    if enable_techmap and results['techmap'].get('results'):
        tm_results = results['techmap']['results']
        logger.info(_safe_log_msg(f"Technology Mapping: [OK] {tm_results['mapped_nodes']}/{tm_results['total_nodes']} nodes mapped ({tm_results['mapping_success_rate']*100:.1f}%)"))
    else:
        logger.info(_safe_log_msg(f"Technology Mapping: [SKIP] SKIPPED"))
    
    # NOTE: Simulation/verification removed from project scope
    
    logger.info("=" * 70)
    logger.info(_safe_log_msg("[OK] Complete flow finished successfully!"))
    logger.info("=" * 70)
    
    # Show output files summary (like Yosys)
    if write_verilog and results.get('output_files'):
        logger.info(_safe_log_msg("\n[FILE] Generated Verilog files:"))
        for file_type, file_path in results['output_files'].items():
            logger.info(f"   - {Path(file_path).name} ({file_type})")
        logger.info(f"   Output directory: {output_dir}")
        logger.info("=" * 70)
    
    return results


# Convenience functions for common use cases
def run_synthesis_only(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """Chạy chỉ synthesis (Netlist → AIG)."""
    return run_complete_flow(
        netlist,
        enable_optimization=False,
        enable_techmap=False
    )


def run_synthesis_optimization(netlist: Dict[str, Any]) -> Dict[str, Any]:
    """Chạy synthesis + optimization (Netlist → AIG → Optimized AIG)."""
    return run_complete_flow(netlist, enable_techmap=False)


# Test function
if __name__ == "__main__":
    # Create test netlist
    test_netlist = {
        'name': 'test_complete_flow',
        'inputs': ['a', 'b', 'c'],
        'outputs': ['out'],
        'nodes': {
            'n1': {'type': 'AND', 'inputs': ['a', 'b'], 'output': 'temp1'},
            'n2': {'type': 'OR', 'inputs': ['temp1', 'c'], 'output': 'out'},
        },
        'wires': {}
    }
    
    print("Testing Complete Flow...")
    print("=" * 70)
    
    # Test complete flow
    results = run_complete_flow(
        test_netlist,
        enable_optimization=True,
        enable_techmap=True
    )
    
    print("\n✅ Complete flow test passed!")


