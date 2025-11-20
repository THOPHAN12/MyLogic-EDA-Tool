# MyLogic EDA Tool - Example Runnable Script (PowerShell)
# This script demonstrates the complete workflow: generate Verilog → read → simulate → write_json

$ErrorActionPreference = "Stop"

Write-Host "========================================" -ForegroundColor Blue
Write-Host "MyLogic EDA Tool - Example Workflow" -ForegroundColor Blue
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""

# Get script directory
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
$PROJECT_ROOT = Split-Path -Parent $SCRIPT_DIR
$OUTPUT_DIR = Join-Path $PROJECT_ROOT "outputs"
$EXAMPLE_DIR = $SCRIPT_DIR

# Create output directory
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

# Step 1: Generate a simple Verilog file
Write-Host "[1/4] Generating example Verilog file..." -ForegroundColor Green
$EXAMPLE_VERILOG = Join-Path $EXAMPLE_DIR "example_adder.v"
@"
module example_adder(a, b, cin, sum, cout);
    input [3:0] a;
    input [3:0] b;
    input cin;
    output [3:0] sum;
    output cout;
    
    assign {cout, sum} = a + b + cin;
endmodule
"@ | Set-Content -Path $EXAMPLE_VERILOG -Encoding UTF8

Write-Host "  ✓ Created: $EXAMPLE_VERILOG"
Write-Host ""

# Step 2: Parse Verilog using Python
Write-Host "[2/4] Parsing Verilog file..." -ForegroundColor Green
Push-Location $PROJECT_ROOT
try {
    python -c @"
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path('$PROJECT_ROOT').resolve()))

from parsers import parse_verilog

example_file = Path('$EXAMPLE_VERILOG').resolve()
netlist = parse_verilog(str(example_file))

print(f'  ✓ Parsed successfully')
print(f'    Module: {netlist[\"name\"]}')
print(f'    Inputs: {len(netlist[\"inputs\"])}')
print(f'    Outputs: {len(netlist[\"outputs\"])}')
print(f'    Nodes: {len(netlist[\"nodes\"])}')
"@
} finally {
    Pop-Location
}
Write-Host ""

# Step 3: Simulate the design
Write-Host "[3/4] Simulating design..." -ForegroundColor Green
Push-Location $PROJECT_ROOT
try {
    python -c @"
import sys
from pathlib import Path

sys.path.insert(0, str(Path('$PROJECT_ROOT').resolve()))

from parsers import parse_verilog
from core.simulation.arithmetic_simulation import simulate_arithmetic_netlist, VectorValue

example_file = Path('$EXAMPLE_VERILOG').resolve()
netlist = parse_verilog(str(example_file))

test_inputs = {
    'a': VectorValue(5, 4),
    'b': VectorValue(3, 4),
    'cin': VectorValue(1, 1)
}

print('  Test inputs:')
for name, value in test_inputs.items():
    print(f'    {name} = {value} (int: {value.to_int()})')

results = simulate_arithmetic_netlist(netlist, test_inputs)

print('  Simulation results:')
for name, value in results.items():
    if isinstance(value, VectorValue):
        print(f'    {name} = {value} (int: {value.to_int()})')
    else:
        print(f'    {name} = {value}')

expected_sum = 9
actual_sum = results.get('sum')
if actual_sum and isinstance(actual_sum, VectorValue):
    if actual_sum.to_int() == expected_sum:
        print(f'  ✓ Verification passed: {actual_sum.to_int()} == {expected_sum}')
    else:
        print(f'  ✗ Verification failed: {actual_sum.to_int()} != {expected_sum}')
        sys.exit(1)
"@
} finally {
    Pop-Location
}
Write-Host ""

# Step 4: Export to JSON
Write-Host "[4/4] Exporting to JSON..." -ForegroundColor Green
$OUTPUT_FILE = Join-Path $OUTPUT_DIR "example_output.json"
Push-Location $PROJECT_ROOT
try {
    python -c @"
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path('$PROJECT_ROOT').resolve()))

from parsers import parse_verilog

example_file = Path('$EXAMPLE_VERILOG').resolve()
netlist = parse_verilog(str(example_file))

output_file = Path('$OUTPUT_FILE').resolve()

export_data = {
    'metadata': {
        'tool': 'MyLogic EDA Tool v2.0.0',
        'export_time': datetime.now().isoformat(),
        'source_file': 'example_adder.v',
        'version': '2.0.0'
    },
    'netlist': netlist
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print(f'  ✓ Exported to: {output_file}')
print(f'    Nodes: {len(netlist[\"nodes\"])}')
print(f'    Inputs: {len(netlist[\"inputs\"])}')
print(f'    Outputs: {len(netlist[\"outputs\"])}')
"@
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Blue
Write-Host "✓ Example workflow completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Blue
Write-Host ""
Write-Host "Generated files:"
Write-Host "  - $EXAMPLE_VERILOG"
Write-Host "  - $OUTPUT_FILE"
Write-Host ""
Write-Host "To view the JSON output:"
Write-Host "  Get-Content $OUTPUT_FILE | ConvertFrom-Json | ConvertTo-Json -Depth 10"
Write-Host ""

