#!/usr/bin/env python3
"""
Verification Functions for Synthesis and Optimization

Industry standard verification methodology:
1. Functional simulation comparison (Pre-synthesis vs Post-synthesis)
2. Functional simulation comparison (Post-synthesis vs Post-optimization)

This module provides functions to verify that synthesis and optimization
steps maintain functional correctness.
"""

import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def verify_synthesis_with_simulation(
    original_netlist: Dict[str, Any],
    synthesized_netlist: Dict[str, Any],
    test_vectors: List[Dict[str, Any]],
    modelsim_path: Optional[str] = None,
    module_name: str = "design"
) -> Dict[str, Any]:
    """
    Verify synthesis correctness: Original vs Synthesized
    
    Industry practice: Pre-synthesis vs Post-synthesis simulation
    
    Args:
        original_netlist: Original netlist (before synthesis)
        synthesized_netlist: Synthesized netlist (AIG converted back)
        test_vectors: List of test vectors to verify
        modelsim_path: Path to ModelSim executable (None = auto-detect)
        module_name: Module name for generated Verilog files
        
    Returns:
        Verification results dictionary with passed/failed status
    """
    from integrations.modelsim_integration import verify_with_modelsim
    
    logger.info("=" * 70)
    logger.info("VERIFICATION: SYNTHESIS (Original vs Synthesized)")
    logger.info("Industry practice: Pre-synthesis vs Post-synthesis simulation")
    logger.info("=" * 70)
    
    results = verify_with_modelsim(
        original_netlist,
        synthesized_netlist,
        test_vectors,
        modelsim_path=modelsim_path,
        module_name=f"{module_name}_synthesis_verify",
        use_temp_dir=False,
        cleanup_old_files=True
    )
    
    return results


def verify_optimization_with_simulation(
    synthesized_netlist: Dict[str, Any],
    optimized_netlist: Dict[str, Any],
    test_vectors: List[Dict[str, Any]],
    modelsim_path: Optional[str] = None,
    module_name: str = "design"
) -> Dict[str, Any]:
    """
    Verify optimization correctness: Synthesized vs Optimized
    
    Industry practice: Post-synthesis vs Post-optimization simulation
    
    Args:
        synthesized_netlist: Synthesized netlist (before optimization)
        optimized_netlist: Optimized netlist (after optimization)
        test_vectors: List of test vectors to verify
        modelsim_path: Path to ModelSim executable (None = auto-detect)
        module_name: Module name for generated Verilog files
        
    Returns:
        Verification results dictionary with passed/failed status
    """
    from integrations.modelsim_integration import verify_with_modelsim
    
    logger.info("=" * 70)
    logger.info("VERIFICATION: OPTIMIZATION (Synthesized vs Optimized)")
    logger.info("Industry practice: Post-synthesis vs Post-optimization simulation")
    logger.info("=" * 70)
    
    results = verify_with_modelsim(
        synthesized_netlist,
        optimized_netlist,
        test_vectors,
        modelsim_path=modelsim_path,
        module_name=f"{module_name}_optimization_verify",
        use_temp_dir=False,
        cleanup_old_files=True
    )
    
    return results


def verify_complete_flow(
    original_netlist: Dict[str, Any],
    synthesized_aig,
    optimized_aig: Optional[Any] = None,
    test_vectors: List[Dict[str, Any]] = None,
    modelsim_path: Optional[str] = None,
    module_name: str = "design",
    enable_optimization_verification: bool = True
) -> Dict[str, Any]:
    """
    Complete verification flow: Synthesis + Optimization
    
    This function verifies both synthesis and optimization steps
    using functional simulation (industry standard approach).
    
    Args:
        original_netlist: Original netlist (before synthesis)
        synthesized_aig: AIG object after synthesis
        optimized_aig: AIG object after optimization (None if not optimized)
        test_vectors: List of test vectors for verification
        modelsim_path: Path to ModelSim executable
        module_name: Module name for generated files
        enable_optimization_verification: Whether to verify optimization
        
    Returns:
        Dictionary with verification results:
        {
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
            } (if applicable)
        }
    """
    from core.synthesis.aig import aig_to_netlist
    
    if test_vectors is None:
        logger.warning("No test vectors provided, skipping verification")
        return {
            'synthesis_verification': None,
            'optimization_verification': None
        }
    
    verification_results = {}
    
    # Convert AIGs to netlists for verification
    synthesized_netlist = aig_to_netlist(synthesized_aig, original_netlist)
    
    # VERIFICATION 1: Synthesis
    logger.info("\n[VERIFICATION 1/2] SYNTHESIS VERIFICATION")
    synthesis_verif = verify_synthesis_with_simulation(
        original_netlist,
        synthesized_netlist,
        test_vectors,
        modelsim_path=modelsim_path,
        module_name=module_name
    )
    
    verification_results['synthesis_verification'] = {
        'passed': synthesis_verif['passed'],
        'total_tests': synthesis_verif['total_tests'],
        'passed_tests': synthesis_verif['passed_tests'],
        'failed_tests': synthesis_verif['failed_tests'],
        'results': synthesis_verif
    }
    
    if synthesis_verif['passed']:
        logger.info(f"✅ Synthesis verification PASSED: {synthesis_verif['passed_tests']}/{synthesis_verif['total_tests']} tests")
    else:
        logger.warning(f"⚠️ Synthesis verification FAILED: {synthesis_verif['failed_tests']}/{synthesis_verif['total_tests']} tests failed")
    
    # VERIFICATION 2: Optimization (if applicable)
    if enable_optimization_verification and optimized_aig is not None:
        logger.info("\n[VERIFICATION 2/2] OPTIMIZATION VERIFICATION")
        optimized_netlist = aig_to_netlist(optimized_aig, original_netlist)
        
        optimization_verif = verify_optimization_with_simulation(
            synthesized_netlist,
            optimized_netlist,
            test_vectors,
            modelsim_path=modelsim_path,
            module_name=module_name
        )
        
        verification_results['optimization_verification'] = {
            'passed': optimization_verif['passed'],
            'total_tests': optimization_verif['total_tests'],
            'passed_tests': optimization_verif['passed_tests'],
            'failed_tests': optimization_verif['failed_tests'],
            'results': optimization_verif
        }
        
        if optimization_verif['passed']:
            logger.info(f"✅ Optimization verification PASSED: {optimization_verif['passed_tests']}/{optimization_verif['total_tests']} tests")
        else:
            logger.warning(f"⚠️ Optimization verification FAILED: {optimization_verif['failed_tests']}/{optimization_verif['total_tests']} tests failed")
    
    return verification_results

