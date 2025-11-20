#!/usr/bin/env python3
"""
Script để chạy tất cả tests và tạo transcript file.

Chạy tất cả tests và ghi lại kết quả vào file transcript.
"""

import os
import sys
import subprocess
import re
from pathlib import Path
from datetime import datetime

# Project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Output directory
output_dir = project_root / "outputs"
output_dir.mkdir(exist_ok=True)

# Transcript file
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
transcript_file = output_dir / f"test_transcript_{timestamp}.txt"


def strip_ansi_codes(text):
    """Remove ANSI escape sequences from text."""
    # ANSI escape code pattern: ESC [ ... m (for colors/formatting)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class TranscriptWriter:
    """Helper class để ghi transcript."""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = open(file_path, 'w', encoding='utf-8')
        
    def write(self, text):
        """Write text to file and stdout."""
        print(text, end='')
        self.file.write(text)
        self.file.flush()
        
    def writeline(self, text=""):
        """Write line to file and stdout."""
        print(text)
        self.file.write(text + "\n")
        self.file.flush()
        
    def section(self, title):
        """Write section header."""
        separator = "=" * 70
        self.writeline()
        self.writeline(separator)
        self.writeline(title)
        self.writeline(separator)
        
    def close(self):
        """Close file."""
        self.file.close()


def run_command(command, transcript, description=""):
    """Run command and capture output to transcript."""
    if description:
        transcript.section(f"Running: {description}")
        transcript.writeline(f"Command: {command}")
        transcript.writeline()
    
    try:
        # Run command and capture output
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        # Write output (strip ANSI codes)
        if result.stdout:
            cleaned_stdout = strip_ansi_codes(result.stdout)
            transcript.writeline(cleaned_stdout)
        if result.stderr:
            cleaned_stderr = strip_ansi_codes(result.stderr)
            transcript.writeline("STDERR:")
            transcript.writeline(cleaned_stderr)
        
        # Write return code
        transcript.writeline()
        transcript.writeline(f"Return code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        transcript.writeline(f"ERROR: {str(e)}")
        return False


def main():
    """Main function to run all tests."""
    # Create transcript writer
    transcript = TranscriptWriter(transcript_file)
    
    # Header
    transcript.section("MYLOGIC EDA TOOL - COMPLETE TEST TRANSCRIPT")
    transcript.writeline(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    transcript.writeline(f"Project: {project_root}")
    transcript.writeline(f"Output file: {transcript_file}")
    
    # Change to project root
    os.chdir(project_root)
    
    summary = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'skipped': 0
    }
    
    # 1. Run all pytest tests
    transcript.section("1. RUNNING ALL PYTEST TESTS")
    result = run_command(
        "python -m pytest tests/ -v --tb=short",
        transcript,
        "All pytest tests"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 2. Run examples tests
    transcript.section("2. RUNNING EXAMPLES TESTS")
    result = run_command(
        "python tests/test_examples.py --level basic",
        transcript,
        "Examples tests (basic level)"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 3. Run examples tests with standard level
    transcript.section("3. RUNNING EXAMPLES TESTS (STANDARD LEVEL)")
    result = run_command(
        "python tests/test_examples.py --level standard",
        transcript,
        "Examples tests (standard level)"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 4. Run technology mapping tests
    transcript.section("4. RUNNING TECHNOLOGY MAPPING TESTS")
    result = run_command(
        "python -m pytest tests/test_technology_mapping.py -v",
        transcript,
        "Technology mapping unit tests"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 5. Run technology mapping with examples
    transcript.section("5. RUNNING TECHNOLOGY MAPPING WITH EXAMPLES")
    result = run_command(
        "python tests/test_techmap_examples.py --strategy area_optimal",
        transcript,
        "Technology mapping with examples (area optimal)"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 6. Run technology mapping with delay optimal
    transcript.section("6. RUNNING TECHNOLOGY MAPPING (DELAY OPTIMAL)")
    result = run_command(
        "python tests/test_techmap_examples.py --strategy delay_optimal",
        transcript,
        "Technology mapping with examples (delay optimal)"
    )
    summary['total'] += 1
    if result:
        summary['passed'] += 1
    else:
        summary['failed'] += 1
    
    # 7. Test individual examples
    transcript.section("7. TESTING INDIVIDUAL EXAMPLES")
    examples_dir = project_root / "examples"
    if examples_dir.exists():
        verilog_files = list(examples_dir.glob("*.v"))
        for verilog_file in sorted(verilog_files):
            transcript.writeline()
            transcript.writeline(f"Testing: {verilog_file.name}")
            result = run_command(
                f'python tests/test_examples.py --file "{verilog_file}" --level basic',
                transcript,
                f"Example: {verilog_file.name}"
            )
    
    # 8. Test technology mapping with individual examples
    transcript.section("8. TECHNOLOGY MAPPING WITH INDIVIDUAL EXAMPLES")
    if examples_dir.exists():
        verilog_files = list(examples_dir.glob("*.v"))
        for verilog_file in sorted(verilog_files):
            transcript.writeline()
            transcript.writeline(f"Testing: {verilog_file.name}")
            result = run_command(
                f'python tests/test_techmap_examples.py --file "{verilog_file}" --strategy area_optimal',
                transcript,
                f"Techmap: {verilog_file.name}"
            )
    
    # 9. Library loading test
    transcript.section("9. TESTING LIBRARY LOADING")
    result = run_command(
        'python -c "from core.technology_mapping.library_loader import load_library; lib = load_library(\'techlibs/asic/standard_cells.json\'); print(f\'Library: {lib.name}\'); print(f\'Total cells: {len(lib.cells)}\'); print(\'Cells:\', \', \'.join(sorted(lib.cells.keys())))"',
        transcript,
        "Load library from techlibs"
    )
    
    # 10. Synthesis flow test
    transcript.section("10. TESTING SYNTHESIS FLOW")
    result = run_command(
        'python -c "from parsers import parse_verilog; from core.synthesis.synthesis_flow import run_complete_synthesis; netlist = parse_verilog(\'examples/full_adder.v\'); print(f\'Original: {len(netlist[\\\"nodes\\\"])} nodes\'); synthesized = run_complete_synthesis(netlist, \'basic\'); print(f\'Final: {len(synthesized[\\\"nodes\\\"])} nodes\'); print(\'SUCCESS\')"',
        transcript,
        "Complete synthesis flow"
    )
    
    # Summary
    transcript.section("TEST SUMMARY")
    transcript.writeline(f"Total test suites: {summary['total']}")
    transcript.writeline(f"  Passed: {summary['passed']}")
    transcript.writeline(f"  Failed: {summary['failed']}")
    transcript.writeline(f"  Skipped: {summary['skipped']}")
    transcript.writeline()
    transcript.writeline(f"Transcript saved to: {transcript_file}")
    transcript.writeline()
    transcript.writeline("=" * 70)
    transcript.writeline("TRANSCRIPT COMPLETE")
    transcript.writeline("=" * 70)
    
    transcript.close()
    
    print()
    print("=" * 70)
    print(f"Transcript saved to: {transcript_file}")
    print("=" * 70)
    
    return transcript_file


if __name__ == "__main__":
    transcript_file = main()
    sys.exit(0)

