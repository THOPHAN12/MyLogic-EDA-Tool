#!/usr/bin/env python3
"""
Complete Flow: Synthesis → Optimization → Technology Mapping → Verification

Luồng tự động chạy cả 4 bước:
1. SYNTHESIS: Netlist → AIG
2. OPTIMIZE: AIG → Optimized AIG
3. TECHMAP: AIG → Technology-mapped netlist
4. VERIFICATION: ModelSim simulation để so sánh output

Đây là workflow hoàn chỉnh cho VLSI CAD flow.
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
    
    This is a standalone utility function extracted from ModelSimIntegration
    to enable Verilog output generation after synthesis steps (like Yosys).
    
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
    
    # Then, create assign statements for nodes
    for node in nodes_list:
        if not isinstance(node, dict):
            continue
        
        node_type = node.get('type', '')
        node_inputs = node.get('inputs', [])
        node_fanins = node.get('fanins', [])
        output = node.get('output', node.get('id', ''))
        
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
        
        # Generate Verilog statement
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
    optimization_level: str = "standard",
    techmap_strategy: str = "area_optimal",
    techmap_library = None,
    enable_optimization: bool = True,
    enable_techmap: bool = True,
    enable_verification: bool = False,
    test_vectors: Optional[List[Dict[str, Any]]] = None,
    modelsim_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    write_verilog: bool = True
) -> Dict[str, Any]:
    """
    Chạy complete flow: Synthesis → Verification → Optimization → Verification → Technology Mapping.
    
    Flow:
    1. SYNTHESIS: Netlist → AIG
       → VERIFICATION 1: Original vs Synthesized (functional simulation)
    2. OPTIMIZATION: AIG → Optimized AIG
       → VERIFICATION 2: Synthesized vs Optimized (functional simulation)
    3. TECHMAP (optional): AIG → Technology-mapped netlist
       → No verification needed (implementation mapping only)
    
    Similar to Yosys flow: read → synth → verify → optimize → verify → techmap → write_verilog
    
    Args:
        netlist: Circuit netlist dictionary từ parser
        optimization_level: Optimization level ("basic", "standard", "aggressive")
        techmap_strategy: Technology mapping strategy ("area_optimal", "delay_optimal", "balanced")
        techmap_library: Technology library object (None = auto-load standard library)
        enable_optimization: Có chạy optimization không (default: True)
        enable_techmap: Có chạy technology mapping không (default: True)
        enable_verification: Có chạy verification không (default: False)
                           Verification sẽ chạy sau synthesis và optimization
        test_vectors: Test vectors cho verification (required nếu enable_verification=True)
        modelsim_path: Path to ModelSim executable (for verification, None = auto-detect)
        output_dir: Directory để lưu output Verilog files (None = current directory)
        write_verilog: Có xuất file .v sau mỗi bước không (default: True, giống Yosys)
        
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
            'verification': {
                'synthesis_verification': {
                    'passed': bool,
                    'total_tests': int,
                    'passed_tests': int,
                    'failed_tests': int,
                    'results': {...}
                },
                'optimization_verification': {
                    'passed': bool,
                    'total_tests': int,
                    'passed_tests': int,
                    'failed_tests': int,
                    'results': {...}
                } (if optimization enabled)
            },
            'output_files': {
                'synthesized': path to synthesized.v (if write_verilog=True),
                'optimized': path to optimized.v (if optimization enabled),
                'mapped': path to mapped.v (if techmap enabled)
            }
        }
        
    Examples:
        >>> from parsers import parse_verilog
        >>> from core.complete_flow import run_complete_flow
        >>> 
        >>> netlist = parse_verilog("design.v")
        >>> results = run_complete_flow(netlist, "standard", "area_optimal")
        >>> 
        >>> # Access results
        >>> synthesized_aig = results['synthesis']['aig']
        >>> optimized_aig = results['optimization']['aig']
        >>> techmap_results = results['techmap']['results']
    """
    logger.info("=" * 70)
    logger.info(_safe_log_msg("COMPLETE FLOW: Synthesis -> Verification -> Optimization -> Verification -> Technology Mapping"))
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
                synthesized_verilog = aig.to_verilog(f"{module_name}_synthesized")
                output_file = output_dir / f"{module_name}_synthesized.v"
                output_file.write_text(synthesized_verilog, encoding='utf-8')
                results['output_files']['synthesized'] = str(output_file)
                logger.info(_safe_log_msg(f"[FILE] Written: {output_file.name}"))
            except Exception as e:
                logger.warning(f"Could not write synthesized Verilog: {e}")
        
    except Exception as e:
        logger.error(f"[ERROR] Synthesis failed: {e}")
        raise
    
    # ============================================================
    # VERIFICATION 1: SYNTHESIS VERIFICATION (Original vs Synthesized)
    # ============================================================
    if enable_verification and test_vectors:
        logger.info("\n[VERIFICATION 1] SYNTHESIS: Original vs Synthesized")
        logger.info("-" * 70)
        
        # Check if synthesis produced outputs
        if len(aig.pos) == 0:
            logger.warning(_safe_log_msg("[SKIP] Synthesis verification SKIPPED: No primary outputs generated by synthesis"))
            logger.warning("")
            logger.warning("   REASON: Synthesis engine currently only supports combinational logic gates.")
            logger.warning("   UNSUPPORTED FEATURES:")
            logger.warning("     - Sequential logic (flip-flops, registers, always @(posedge clk))")
            logger.warning("     - Memory arrays")
            logger.warning("     - Functions and tasks")
            logger.warning("     - Complex expressions in always blocks")
            logger.warning("")
            logger.warning("   SOLUTION:")
            logger.warning("     - Use combinational logic only for verification")
            logger.warning("     - Or use simpler test cases (e.g., simple gates)")
            logger.warning("     - Sequential logic verification requires future synthesis improvements")
            logger.warning("")
            if 'verification' not in results:
                results['verification'] = {}
            results['verification']['synthesis_verification'] = {
                'passed': False,
                'total_tests': len(test_vectors),
                'passed_tests': 0,
                'failed_tests': len(test_vectors),
                'error': 'No primary outputs generated - synthesis does not support sequential logic/memories',
                'skipped': True,
                'reason': 'Synthesis only supports combinational gates (AND, OR, XOR, NOT, etc.)',
                'unsupported_features': ['Sequential logic', 'Memory arrays', 'Functions', 'Complex always blocks']
            }
        else:
            try:
                from core.verification import verify_synthesis_with_simulation
                
                logger.info(f"Running synthesis verification with {len(test_vectors)} test vector(s)...")
                
                synthesis_verif = verify_synthesis_with_simulation(
                    netlist,  # Original netlist
                    synthesized_netlist,  # Synthesized netlist
                    test_vectors,
                    modelsim_path=modelsim_path,
                    module_name=module_name
                )
            
                if 'verification' not in results:
                    results['verification'] = {}
                
                results['verification']['synthesis_verification'] = {
                    'passed': synthesis_verif['passed'],
                    'total_tests': synthesis_verif['total_tests'],
                    'passed_tests': synthesis_verif['passed_tests'],
                    'failed_tests': synthesis_verif['failed_tests'],
                    'results': synthesis_verif
                }
                
                if synthesis_verif['passed']:
                    logger.info(_safe_log_msg(f"[OK] Synthesis verification PASSED: {synthesis_verif['passed_tests']}/{synthesis_verif['total_tests']} tests"))
                else:
                    logger.warning(_safe_log_msg(f"[WARN] Synthesis verification FAILED: {synthesis_verif['failed_tests']}/{synthesis_verif['total_tests']} tests failed"))
                
            except ImportError:
                logger.warning("Verification module not available. Skipping synthesis verification...")
                if 'verification' not in results:
                    results['verification'] = {}
                results['verification']['synthesis_verification'] = {
                    'passed': False,
                    'error': 'Verification module not available',
                    'skipped': True
                }
            except Exception as e:
                logger.error(f"[ERROR] Synthesis verification failed: {e}")
                if 'verification' not in results:
                    results['verification'] = {}
                results['verification']['synthesis_verification'] = {
                    'passed': False,
                    'error': str(e),
                    'skipped': False
                }
    
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
            logger.info(f"Optimization level: {optimization_level}")
            
            # Run optimization
            optimized_aig = optimize(aig, optimization_level)
            
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
                    optimized_verilog = optimized_aig.to_verilog(f"{module_name}_optimized")
                    output_file = output_dir / f"{module_name}_optimized.v"
                    output_file.write_text(optimized_verilog, encoding='utf-8')
                    results['output_files']['optimized'] = str(output_file)
                    logger.info(_safe_log_msg(f"[FILE] Written: {output_file.name}"))
                except Exception as e:
                    logger.warning(f"Could not write optimized Verilog: {e}")
            
            # Use optimized AIG for next step
            aig = optimized_aig
            
            # ============================================================
            # VERIFICATION 2: OPTIMIZATION VERIFICATION (Synthesized vs Optimized)
            # ============================================================
            if enable_verification and test_vectors:
                logger.info("\n[VERIFICATION 2] OPTIMIZATION: Synthesized vs Optimized")
                logger.info("-" * 70)
                
                # Check if optimization produced outputs
                if len(optimized_aig.pos) == 0:
                    logger.warning(_safe_log_msg("[SKIP] Optimization verification SKIPPED: No primary outputs generated"))
                    logger.warning("   (Same reason as synthesis verification above)")
                    if 'verification' not in results:
                        results['verification'] = {}
                    results['verification']['optimization_verification'] = {
                        'passed': False,
                        'total_tests': len(test_vectors),
                        'passed_tests': 0,
                        'failed_tests': len(test_vectors),
                        'error': 'No primary outputs generated - synthesis does not support sequential logic/memories',
                        'skipped': True
                    }
                else:
                    try:
                        from core.verification import verify_optimization_with_simulation
                        
                        # Get synthesized netlist (before optimization)
                        synthesized_netlist = results['synthesis'].get('netlist')
                        if synthesized_netlist is None:
                            synthesized_netlist = aig_to_netlist(results['synthesis']['aig'], netlist)
                        
                        logger.info(f"Running optimization verification with {len(test_vectors)} test vector(s)...")
                        
                        optimization_verif = verify_optimization_with_simulation(
                            synthesized_netlist,  # Before optimization
                            optimized_netlist,    # After optimization
                            test_vectors,
                            modelsim_path=modelsim_path,
                            module_name=module_name
                        )
                        
                        if 'verification' not in results:
                            results['verification'] = {}
                        
                        results['verification']['optimization_verification'] = {
                            'passed': optimization_verif['passed'],
                            'total_tests': optimization_verif['total_tests'],
                            'passed_tests': optimization_verif['passed_tests'],
                            'failed_tests': optimization_verif['failed_tests'],
                            'results': optimization_verif
                        }
                        
                        if optimization_verif['passed']:
                            logger.info(_safe_log_msg(f"[OK] Optimization verification PASSED: {optimization_verif['passed_tests']}/{optimization_verif['total_tests']} tests"))
                        else:
                            logger.warning(_safe_log_msg(f"[WARN] Optimization verification FAILED: {optimization_verif['failed_tests']}/{optimization_verif['total_tests']} tests failed"))
                        
                    except ImportError:
                        logger.warning("Verification module not available. Skipping optimization verification...")
                        if 'verification' not in results:
                            results['verification'] = {}
                        results['verification']['optimization_verification'] = {
                            'passed': False,
                            'error': 'Verification module not available',
                            'skipped': True
                        }
                    except Exception as e:
                        logger.error(f"[ERROR] Optimization verification failed: {e}")
                        if 'verification' not in results:
                            results['verification'] = {}
                        results['verification']['optimization_verification'] = {
                            'passed': False,
                            'error': str(e),
                            'skipped': False
                        }
            
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
            logger.info(f"Techmap strategy: {techmap_strategy}")
            
            # Load library if not provided
            if techmap_library is None:
                logger.info("Loading standard technology library...")
                library = create_standard_library()
                logger.info(f"Loaded library '{library.name}' with {len(library.cells)} cells")
            else:
                library = techmap_library
            
            # Run technology mapping
            techmap_results = techmap(aig, library, techmap_strategy)
            
            results['techmap'] = {
                'results': techmap_results,
                'library_name': library.name,
                'enabled': True
            }
            
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
    # NOTE: Verification is done after Synthesis and Optimization steps
    # Technology mapping does not require verification (it's just implementation mapping)
    # ============================================================
    if enable_verification and not test_vectors:
        logger.warning("\n[NOTE] No test vectors provided. Verification skipped.")
        if 'verification' not in results:
            results['verification'] = {}
        results['verification']['note'] = 'No test vectors provided'
    
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
    
    # Verification summary
    if enable_verification and results.get('verification'):
        verif = results['verification']
        
        # Synthesis verification
        if 'synthesis_verification' in verif and verif['synthesis_verification']:
            synth_verif = verif['synthesis_verification']
            if not synth_verif.get('skipped'):
                total_tests = synth_verif.get('total_tests', 0)
                if synth_verif.get('passed'):
                    logger.info(_safe_log_msg(f"Synthesis Verification: [OK] {synth_verif.get('passed_tests', 0)}/{total_tests} tests passed"))
                else:
                    logger.warning(_safe_log_msg(f"Synthesis Verification: [WARN] {synth_verif.get('failed_tests', 0)}/{total_tests} tests failed"))
            else:
                logger.info(_safe_log_msg(f"Synthesis Verification: [SKIP] SKIPPED ({synth_verif.get('error', 'N/A')})"))
        else:
            logger.info(_safe_log_msg(f"Synthesis Verification: [SKIP] SKIPPED"))
        
        # Optimization verification
        if 'optimization_verification' in verif and verif['optimization_verification']:
            opt_verif = verif['optimization_verification']
            if not opt_verif.get('skipped'):
                total_tests = opt_verif.get('total_tests', 0)
                if opt_verif.get('passed'):
                    logger.info(_safe_log_msg(f"Optimization Verification: [OK] {opt_verif.get('passed_tests', 0)}/{total_tests} tests passed"))
                else:
                    logger.warning(_safe_log_msg(f"Optimization Verification: [WARN] {opt_verif.get('failed_tests', 0)}/{total_tests} tests failed"))
            else:
                logger.info(_safe_log_msg(f"Optimization Verification: [SKIP] SKIPPED ({opt_verif.get('error', 'N/A')})"))
        else:
            logger.info(_safe_log_msg(f"Optimization Verification: [SKIP] SKIPPED"))
    else:
        logger.info(_safe_log_msg(f"Verification: [SKIP] SKIPPED"))
    
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


def run_synthesis_optimization(netlist: Dict[str, Any], optimization_level: str = "standard") -> Dict[str, Any]:
    """Chạy synthesis + optimization (Netlist → AIG → Optimized AIG)."""
    return run_complete_flow(
        netlist,
        optimization_level=optimization_level,
        enable_techmap=False
    )


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
        optimization_level="standard",
        techmap_strategy="area_optimal",
        enable_optimization=True,
        enable_techmap=True
    )
    
    print("\n✅ Complete flow test passed!")


