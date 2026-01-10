#!/usr/bin/env python3
"""
Helper script to run ModelSim simulation

Usage:
    python run_simulation.py <module_name> [mode]
    
    module_name: Name of module (e.g., 'simple_and', 'full_adder')
    mode: 'batch' (default) or 'gui' or 'waveform'
    
Examples:
    python run_simulation.py simple_and batch
    python run_simulation.py simple_and gui
    python run_simulation.py simple_and waveform
"""

import subprocess
import sys
import os
from pathlib import Path

def find_modelsim():
    """Find ModelSim executable."""
    common_paths = [
        r"C:\intelFPGA\18.1\modelsim_ase\win32aloem\vsim.exe",
        r"C:\Modeltech_pe_edu_10.5a\win32pe_edu\vsim.exe",
        r"C:\altera\13.0sp1\modelsim_ase\win32aloem\vsim.exe",
        "vsim",  # In PATH
    ]
    
    for path in common_paths:
        if path == "vsim":
            # Check if vsim is in PATH
            try:
                result = subprocess.run(
                    ["vsim", "-version"],
                    capture_output=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return "vsim"
            except:
                continue
        else:
            if os.path.exists(path):
                return path
    
    return None

def run_simulation(module_name, mode='batch'):
    """
    Run ModelSim simulation.
    
    Args:
        module_name: Name of module (e.g., 'simple_and')
        mode: 'batch' (command line), 'gui' (interactive), or 'waveform' (VCD output)
    """
    # Get script directory
    script_dir = Path(__file__).parent
    modelsim_path = find_modelsim()
    
    if modelsim_path is None:
        print("ERROR: ModelSim not found!")
        print("Please install ModelSim or set it in PATH")
        return 1
    
    print("=" * 70)
    print(f"ModelSim Simulation: {module_name}")
    print("=" * 70)
    print(f"Mode: {mode}")
    print(f"ModelSim: {modelsim_path}")
    print()
    
    # Check if Verilog files exist
    original_file = script_dir / f"{module_name}_original.v"
    mapped_file = script_dir / f"{module_name}_mapped.v"
    testbench_file = script_dir / f"{module_name}_tb.v"
    
    if not original_file.exists():
        print(f"ERROR: {original_file.name} not found!")
        return 1
    if not mapped_file.exists():
        print(f"ERROR: {mapped_file.name} not found!")
        return 1
    if not testbench_file.exists():
        print(f"ERROR: {testbench_file.name} not found!")
        return 1
    
    # Run simulation based on mode
    if mode == 'batch':
        # Batch mode: use compile.do
        cmd = [modelsim_path, '-batch', '-do', f'do compile.do {module_name}']
        print("Running in batch mode (no GUI)...")
        
    elif mode == 'gui':
        # GUI mode: use interactive script
        cmd = [modelsim_path, '-do', f'do scripts/run_interactive.do {module_name}']
        print("Running in GUI mode (interactive)...")
        
    elif mode == 'waveform':
        # Waveform mode: generate VCD file
        # Create simulation directory for module
        sim_dir = script_dir / "simulations" / module_name
        sim_dir.mkdir(parents=True, exist_ok=True)
        
        cmd = [modelsim_path, '-batch', '-do', f'do scripts/run_with_waveform.do {module_name}']
        print("Running with VCD waveform output...")
        print(f"Waveform will be saved to: simulations/{module_name}/{module_name}_waveform.vcd")
    else:
        print(f"ERROR: Unknown mode '{mode}'")
        print("Valid modes: batch, gui, waveform")
        return 1
    
    print()
    
    try:
        # Run ModelSim
        result = subprocess.run(
            cmd,
            cwd=str(script_dir),
            timeout=120
        )
        
        if result.returncode == 0:
            print()
            print("=" * 70)
            print("Simulation completed successfully!")
            print("=" * 70)
            return 0
        else:
            print()
            print("=" * 70)
            print(f"Simulation failed with exit code {result.returncode}")
            print("=" * 70)
            return 1
            
    except subprocess.TimeoutExpired:
        print()
        print("ERROR: Simulation timeout (exceeded 120 seconds)")
        return 1
    except Exception as e:
        print()
        print(f"ERROR: {e}")
        return 1

def main():
    """Main function."""
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        print(__doc__)
        print()
        if len(sys.argv) >= 2 and sys.argv[1] in ['-h', '--help', 'help']:
            print("Quick Examples:")
            print("  python run_simulation.py simple_and batch      # Batch mode")
            print("  python run_simulation.py simple_and gui        # GUI mode")
            print("  python run_simulation.py simple_and waveform   # With VCD output")
            return 0
        else:
            print("ERROR: Module name required")
            print()
            print("Example:")
            print("  python run_simulation.py simple_and batch")
            return 1
    
    module_name = sys.argv[1]
    mode = sys.argv[2] if len(sys.argv) > 2 else 'batch'
    
    return run_simulation(module_name, mode)

if __name__ == "__main__":
    exit(main())

