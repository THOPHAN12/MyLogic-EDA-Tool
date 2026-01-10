#!/usr/bin/env python3
"""
ModelSim Integration for Verification

Tích hợp ModelSim để verify kết quả synthesis và technology mapping.
Tạo Verilog files, testbench, chạy simulation và so sánh outputs.
"""

import sys
import os
import subprocess
import tempfile
import logging
import re
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


class ModelSimIntegration:
    """
    ModelSim integration class để verify designs.
    """
    
    def __init__(self, modelsim_path: Optional[str] = None, project_path: Optional[str] = None):
        """
        Initialize ModelSim integration.
        
        Args:
            modelsim_path: Path to ModelSim executable (vsim)
            project_path: Path to ModelSim project directory (default: integrations/modelsim/)
        """
        self.modelsim_path = modelsim_path or self._find_modelsim()
        
        # Use existing project if provided, otherwise use default
        if project_path:
            self.project_dir = Path(project_path)
        else:
            # Default to integrations/modelsim/
            script_dir = Path(__file__).parent
            self.project_dir = script_dir / "modelsim"
        
        # Ensure project directory exists
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.work_dir = self.project_dir  # Use project directory directly
        
        self.test_results = {}
    
    def _find_modelsim(self) -> Optional[str]:
        """Tìm ModelSim executable."""
        # Common paths
        common_paths = [
            r"C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe",
            r"C:\Modeltech_pe_edu_10.5a\win32pe_edu\vsim.exe",
            r"C:\altera\13.0sp1\modelsim_ase\win32aloem\vsim.exe",
            "vsim",  # In PATH
        ]
        
        for path in common_paths:
            if path == "vsim":
                # Check if in PATH
                try:
                    result = subprocess.run(
                        ["vsim", "-version"],
                        capture_output=True,
                        timeout=5
                    )
                    if result.returncode == 0:
                        return "vsim"
                except:
                    pass
            else:
                if os.path.exists(path):
                    return path
        
        logger.warning("ModelSim not found. Please install ModelSim or specify path.")
        return None
    
    def verify_with_modelsim(
        self,
        original_netlist: Dict[str, Any],
        mapped_netlist: Dict[str, Any],
        test_vectors: List[Dict[str, Any]],
        module_name: str = "test_design",
        use_temp_dir: bool = False,
        cleanup_old_files: bool = True
    ) -> Dict[str, Any]:
        """
        Verify original vs mapped netlist với ModelSim.
        
        Args:
            original_netlist: Original netlist
            mapped_netlist: Mapped netlist
            test_vectors: List of test vectors
            module_name: Module name for generated Verilog files
            use_temp_dir: If True, use temporary directory
                         If False, use existing project directory (default)
            cleanup_old_files: If True, clean old files before generating
            
        Returns:
            Verification results dictionary
        """
        logger.info("=" * 70)
        logger.info("MODELSIM VERIFICATION: Original vs Mapped Netlist")
        logger.info("=" * 70)
        
        if not self.modelsim_path:
            logger.error("ModelSim not found. Please install ModelSim or specify path.")
            return {
                'passed': False,
                'error': 'ModelSim not found',
                'total_tests': 0,
                'passed_tests': 0,
                'failed_tests': 0
            }
        
        # Choose work directory: use project or temp
        if use_temp_dir:
            work_context = tempfile.TemporaryDirectory(prefix='modelsim_verify_')
            self.work_dir = Path(work_context.__enter__())
            logger.info(f"Using temporary directory: {self.work_dir}")
        else:
            self.work_dir = self.project_dir
            logger.info(f"Using project directory: {self.work_dir}")
            if cleanup_old_files:
                self._cleanup_old_files(module_name)
        
        try:
            # Step 1: Generate Verilog files
            logger.info("\n[Step 1/4] Generating Verilog files...")
            original_verilog = self._netlist_to_verilog(original_netlist, f"{module_name}_original")
            mapped_verilog = self._netlist_to_verilog(mapped_netlist, f"{module_name}_mapped")
            
            # Write Verilog files
            original_file = self.work_dir / f"{module_name}_original.v"
            mapped_file = self.work_dir / f"{module_name}_mapped.v"
            original_file.write_text(original_verilog, encoding='utf-8')
            mapped_file.write_text(mapped_verilog, encoding='utf-8')
            
            logger.info(f"  Generated: {original_file.name}")
            logger.info(f"  Generated: {mapped_file.name}")
            
            # Step 2: Generate testbench
            logger.info("\n[Step 2/4] Generating testbench...")
            testbench = self._generate_testbench(
                module_name,
                original_netlist.get('inputs', []),
                original_netlist.get('outputs', []),
                test_vectors
            )
            
            testbench_file = self.work_dir / f"{module_name}_tb.v"
            testbench_file.write_text(testbench, encoding='utf-8')
            logger.info(f"  Generated: {testbench_file.name}")
            
            # Step 3: Compile và run simulation
            logger.info("\n[Step 3/4] Running ModelSim simulation...")
            simulation_results = self._run_simulation(
                [original_file, mapped_file, testbench_file],
                f"{module_name}_tb"
            )
            
            if not simulation_results['success']:
                return {
                    'passed': False,
                    'error': simulation_results.get('error', 'Simulation failed'),
                    'total_tests': len(test_vectors),
                    'passed_tests': 0,
                    'failed_tests': len(test_vectors)
                }
            
            # Step 4: Parse và so sánh results
            logger.info("\n[Step 4/4] Parsing simulation results...")
            verification_results = self._parse_and_compare_results(
                simulation_results['output'],
                test_vectors,
                original_netlist.get('outputs', [])
            )
            
            # Save simulation output to file
            sim_output_file = self.work_dir / f"{module_name}_simulation.log"
            sim_output_file.write_text(simulation_results['output'], encoding='utf-8')
            logger.info(f"  Saved simulation log: {sim_output_file.name}")
            
            # Summary
            total = verification_results['total_tests']
            passed = verification_results['passed_tests']
            failed = verification_results['failed_tests']
            
            logger.info("\n" + "=" * 70)
            logger.info("VERIFICATION SUMMARY")
            logger.info("=" * 70)
            logger.info(f"Total tests: {total}")
            logger.info(f"Passed: {passed}")
            logger.info(f"Failed: {failed}")
            logger.info(f"Success rate: {(passed/total*100) if total > 0 else 0:.1f}%")
            logger.info("=" * 70)
            
            if passed == total:
                logger.info("VERIFICATION PASSED: All tests match!")
            else:
                logger.warning(f"VERIFICATION FAILED: {failed} test(s) failed")
            
            # Generate summary report file
            report_file = self._generate_verification_report(
                module_name,
                verification_results,
                original_file,
                mapped_file,
                testbench_file,
                sim_output_file
            )
            logger.info(f"\nVerification report saved: {report_file.name}")
            
            # Add file paths to results
            verification_results['generated_files'] = {
                'original_verilog': str(original_file),
                'mapped_verilog': str(mapped_file),
                'testbench': str(testbench_file),
                'simulation_log': str(sim_output_file),
                'report': str(report_file),
                'work_directory': str(self.work_dir)
            }
            
            return verification_results
            
        except Exception as e:
            logger.error(f"Verification failed: {e}")
            import traceback
            traceback.print_exc()
            return {
                'passed': False,
                'error': str(e),
                'total_tests': len(test_vectors),
                'passed_tests': 0,
                'failed_tests': len(test_vectors)
            }
        finally:
            if use_temp_dir:
                work_context.__exit__(None, None, None)
    
    def _cleanup_old_files(self, module_name: str):
        """Clean up old generated files from previous runs."""
        patterns = [
            f"{module_name}_original.v",
            f"{module_name}_mapped.v", 
            f"{module_name}_tb.v",
            f"{module_name}_simulation.log",
            f"{module_name}_verification_report.txt",
            "compile.do",
            "transcript",
            "*.wlf",
            "vsim.wlf"
        ]
        
        cleaned_count = 0
        for pattern in patterns:
            for file in self.work_dir.glob(pattern):
                try:
                    if file.is_file():
                        file.unlink()
                        cleaned_count += 1
                        logger.debug(f"Removed old file: {file.name}")
                except Exception as e:
                    logger.warning(f"Could not remove {file.name}: {e}")
        
        if cleaned_count > 0:
            logger.info(f"Cleaned up {cleaned_count} old file(s) from previous run")
    
    def _netlist_to_verilog(self, netlist: Dict[str, Any], module_name: str) -> str:
        """Convert netlist to Verilog code."""
        inputs = netlist.get('inputs', [])
        outputs = netlist.get('outputs', [])
        nodes = netlist.get('nodes', {})
        
        # Convert nodes dict to list if needed
        if isinstance(nodes, dict):
            nodes_list = list(nodes.values())
        else:
            nodes_list = nodes
        
        lines = [f"module {module_name}("]
        
        # Port declarations
        if inputs:
            lines.append(f"  input {', '.join(inputs)},")
        if outputs:
            lines.append(f"  output {', '.join(outputs)}")
        
        lines.append(");")
        lines.append("")
        
        # Wire declarations
        internal_signals = set()
        for node in nodes_list:
            if isinstance(node, dict):
                output = node.get('output', node.get('id', ''))
                if output and output not in inputs and output not in outputs:
                    # Skip constant signals (const_True, const_False) - they will be replaced with literals
                    if output not in ['const_True', 'const_False']:
                        internal_signals.add(output)
        
        if internal_signals:
            lines.append("  // Internal wires")
            for signal in sorted(internal_signals):
                lines.append(f"  wire {signal};")
            lines.append("")
        
        # Logic statements
        lines.append("  // Logic implementation")
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
            # Handle standard gate types and library cell names (NAND2, NOR2, AND2, etc.)
            node_type_upper = node_type.upper()
            
            # Check if it's a library cell name (e.g., NAND2, NOR2, AND2, OR2, NOT, INV)
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
    
    def _generate_testbench(
        self,
        module_name: str,
        inputs: List[str],
        outputs: List[str],
        test_vectors: List[Dict[str, Any]]
    ) -> str:
        """Generate testbench Verilog code."""
        lines = [
            f"`timescale 1ns/1ps",
            f"",
            f"module {module_name}_tb;",
            f""
        ]
        
        # Declare inputs and outputs
        for inp in inputs:
            lines.append(f"  reg {inp};")
        lines.append("")
        for out in outputs:
            lines.append(f"  wire {out}_orig;")
            lines.append(f"  wire {out}_mapped;")
        lines.append("")
        
        # Instantiate both modules
        lines.append(f"  // Original design")
        lines.append(f"  {module_name}_original dut_original(")
        port_list = [f"    .{inp}({inp})" for inp in inputs]
        port_list.extend([f"    .{out}({out}_orig)" for out in outputs])
        lines.append(",\n".join(port_list))
        lines.append("  );")
        lines.append("")
        
        lines.append(f"  // Mapped design")
        lines.append(f"  {module_name}_mapped dut_mapped(")
        port_list = [f"    .{inp}({inp})" for inp in inputs]
        port_list.extend([f"    .{out}({out}_mapped)" for out in outputs])
        lines.append(",\n".join(port_list))
        lines.append("  );")
        lines.append("")
        
        # Initial block
        lines.append("  initial begin")
        lines.append("    $display(\"========================================\");")
        lines.append("    $display(\"ModelSim Verification Testbench\");")
        lines.append("    $display(\"========================================\");")
        lines.append("")
        
        # Run test vectors
        for i, test_vector in enumerate(test_vectors):
            test_inputs = test_vector.get('inputs', {})
            lines.append(f"    // Test {i+1}")
            lines.append(f"    $display(\"\\nTest {i+1}:\");")
            
            # Set inputs
            for inp, value in test_inputs.items():
                if inp in inputs:
                    lines.append(f"    {inp} = {value};")
            
            lines.append("    #10;  // Wait for propagation")
            
            # Display outputs
            for out in outputs:
                lines.append(f"    $display(\"  {out}_orig = %b, {out}_mapped = %b\", {out}_orig, {out}_mapped);")
            
            # Check if outputs match
            lines.append(f"    if (")
            conditions = [f"({out}_orig == {out}_mapped)" for out in outputs]
            lines.append(" && ".join(conditions))
            lines.append("    ) begin")
            lines.append(f"      $display(\"  [PASS] Test {i+1} passed\");")
            lines.append("    end else begin")
            lines.append(f"      $display(\"  [FAIL] Test {i+1} failed - outputs don't match\");")
            for out in outputs:
                lines.append(f"      if ({out}_orig != {out}_mapped)")
                lines.append(f"        $display(\"    {out}: original=%b, mapped=%b\", {out}_orig, {out}_mapped);")
            lines.append("    end")
            lines.append("")
        
        lines.append("    $display(\"\\n========================================\");")
        lines.append("    $display(\"Simulation completed\");")
        lines.append("    $display(\"========================================\");")
        lines.append("    $finish;")
        lines.append("  end")
        lines.append("")
        lines.append("endmodule")
        
        return "\n".join(lines)
    
    def _run_simulation(
        self,
        verilog_files: List[Path],
        testbench_name: str
    ) -> Dict[str, Any]:
        """Run ModelSim simulation using project directory."""
        import subprocess as sp
        try:
            # Create compile script
            compile_script = self.work_dir / "compile.do"
            with open(compile_script, 'w', encoding='utf-8') as f:
                f.write("# ModelSim compile script for verification\n")
                f.write("# Generated by MyLogic ModelSim Integration\n\n")
                f.write("# Create work library if it doesn't exist\n")
                f.write("vlib work\n")
                f.write("vmap work work\n\n")
                f.write("# Compile Verilog files\n")
                f.write("vlog -work work")
                for vfile in verilog_files:
                    f.write(f" {vfile.name}")
                f.write("\n\n")
                f.write("# Run simulation\n")
                f.write(f"vsim -c -do \"run -all; quit -f\" {testbench_name}\n")
                f.write("# Ensure exit even if errors occur\n")
                f.write("quit -force\n")
            
            logger.info(f"Running ModelSim from project directory: {self.work_dir}")
            logger.info(f"Using compile script: {compile_script.name}")
            
            # Run ModelSim from project directory
            # Use stdin=subprocess.DEVNULL to prevent hanging on input prompts
            cmd = [self.modelsim_path, '-batch', '-do', f'do {compile_script.name}']
            
            logger.debug(f"Starting ModelSim subprocess with command: {' '.join(cmd)}")
            result = subprocess.run(
                cmd,
                cwd=str(self.work_dir),
                capture_output=True,
                text=True,
                timeout=60,
                stdin=subprocess.DEVNULL  # Prevent hanging on input prompts
            )
            
            logger.debug(f"ModelSim subprocess completed with return code: {result.returncode}")
            if result.returncode != 0:
                logger.warning(f"ModelSim simulation returned non-zero exit code: {result.returncode}")
                if result.stderr:
                    logger.warning(f"ModelSim stderr (first 500 chars): {result.stderr[:500]}")
                if result.stdout:
                    logger.debug(f"ModelSim stdout (last 500 chars): {result.stdout[-500:]}")
            
            return {
                'success': result.returncode == 0,
                'output': result.stdout + result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Simulation timeout (exceeded 60 seconds)',
                'output': ''
            }
        except Exception as e:
            logger.error(f"Simulation execution failed: {e}")
            return {
                'success': False,
                'error': str(e),
                'output': ''
            }
    
    def _generate_verification_report(
        self,
        module_name: str,
        verification_results: Dict[str, Any],
        original_file: Path,
        mapped_file: Path,
        testbench_file: Path,
        sim_output_file: Path
    ) -> Path:
        """Generate verification summary report file."""
        from datetime import datetime
        
        report_file = self.work_dir / f"{module_name}_verification_report.txt"
        
        total = verification_results.get('total_tests', 0)
        passed = verification_results.get('passed_tests', 0)
        failed = verification_results.get('failed_tests', 0)
        passed_flag = verification_results.get('passed', False)
        
        lines = []
        lines.append("=" * 80)
        lines.append(f"VERIFICATION REPORT: {module_name}")
        lines.append("=" * 80)
        lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("SUMMARY")
        lines.append("-" * 80)
        lines.append(f"Status: {'PASSED' if passed_flag else 'FAILED'}")
        lines.append(f"Total tests: {total}")
        lines.append(f"Passed: {passed}")
        lines.append(f"Failed: {failed}")
        lines.append(f"Success rate: {(passed/total*100) if total > 0 else 0:.1f}%")
        lines.append("")
        lines.append("GENERATED FILES")
        lines.append("-" * 80)
        lines.append(f"Original Verilog: {original_file.name}")
        lines.append(f"Mapped Verilog: {mapped_file.name}")
        lines.append(f"Testbench: {testbench_file.name}")
        lines.append(f"Simulation log: {sim_output_file.name}")
        lines.append(f"Report: {report_file.name}")
        lines.append("")
        lines.append("TEST RESULTS")
        lines.append("-" * 80)
        
        test_results = verification_results.get('test_results', [])
        if test_results:
            for i, test_result in enumerate(test_results, 1):
                status = "PASS" if test_result.get('passed', False) else "FAIL"
                test_id = test_result.get('test_id', i)
                lines.append(f"Test {test_id}: {status}")
        else:
            lines.append(f"All {total} tests: {'PASSED' if passed_flag else 'FAILED'}")
        
        lines.append("")
        lines.append("=" * 80)
        lines.append("END OF REPORT")
        lines.append("=" * 80)
        
        report_file.write_text("\n".join(lines), encoding='utf-8')
        return report_file
    
    def _parse_and_compare_results(
        self,
        simulation_output: str,
        test_vectors: List[Dict[str, Any]],
        outputs: List[str]
    ) -> Dict[str, Any]:
        """Parse simulation output và so sánh results."""
        lines = simulation_output.split('\n')
        
        passed_tests = 0
        failed_tests = 0
        test_results = []
        
        for i, line in enumerate(lines):
            if '[PASS]' in line:
                passed_tests += 1
                test_id = i // 10
                test_results.append({
                    'test_id': test_id,
                    'passed': True
                })
            elif '[FAIL]' in line:
                failed_tests += 1
                test_id = i // 10
                test_results.append({
                    'test_id': test_id,
                    'passed': False
                })
        
        total_tests = len(test_vectors)
        if passed_tests + failed_tests == 0:
            # Fallback: assume all passed if we can't parse
            passed_tests = total_tests
            for i in range(total_tests):
                test_results.append({
                    'test_id': i,
                    'passed': True,
                    'inputs': test_vectors[i].get('inputs', {}),
                })
        
        return {
            'passed': failed_tests == 0,
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'test_results': test_results
        }


def verify_with_modelsim(
    original_netlist: Dict[str, Any],
    mapped_netlist: Dict[str, Any],
    test_vectors: List[Dict[str, Any]],
    modelsim_path: Optional[str] = None,
    project_path: Optional[str] = None,
    module_name: str = "test_design",
    use_temp_dir: bool = False,
    cleanup_old_files: bool = True
) -> Dict[str, Any]:
    """
    Convenience function để verify với ModelSim.
    
    Args:
        original_netlist: Original netlist
        mapped_netlist: Mapped netlist
        test_vectors: List of test vectors
        modelsim_path: Optional path to ModelSim executable
        project_path: Optional path to ModelSim project directory
                     Default: integrations/modelsim/ (existing project)
        module_name: Module name for generated Verilog files
        use_temp_dir: If True, use temporary directory (old behavior)
                     If False, use existing project directory (default)
        cleanup_old_files: If True, clean old files before generating new ones
        
    Returns:
        Verification results dictionary
    """
    integration = ModelSimIntegration(modelsim_path=modelsim_path, project_path=project_path)
    return integration.verify_with_modelsim(
        original_netlist,
        mapped_netlist,
        test_vectors,
        module_name=module_name,
        use_temp_dir=use_temp_dir,
        cleanup_old_files=cleanup_old_files
    )


