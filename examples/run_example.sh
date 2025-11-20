#!/bin/bash
# MyLogic EDA Tool - Example Runnable Script
# This script demonstrates the complete workflow: generate Verilog → read → simulate → write_json

set -e  # Exit on error

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}MyLogic EDA Tool - Example Workflow${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"
OUTPUT_DIR="$PROJECT_ROOT/outputs"
EXAMPLE_DIR="$SCRIPT_DIR"

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Step 1: Generate a simple Verilog file
echo -e "${GREEN}[1/4] Generating example Verilog file...${NC}"
EXAMPLE_VERILOG="$EXAMPLE_DIR/example_adder.v"
cat > "$EXAMPLE_VERILOG" << 'EOF'
module example_adder(a, b, cin, sum, cout);
    input [3:0] a;
    input [3:0] b;
    input cin;
    output [3:0] sum;
    output cout;
    
    assign {cout, sum} = a + b + cin;
endmodule
EOF

echo "  ✓ Created: $EXAMPLE_VERILOG"
echo ""

# Step 2: Parse Verilog using Python
echo -e "${GREEN}[2/4] Parsing Verilog file...${NC}"
cd "$PROJECT_ROOT"
python3 << PYTHON_SCRIPT
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from parsers import parse_verilog

# Parse the example file
example_file = Path(__file__).parent / "examples" / "example_adder.v"
netlist = parse_verilog(str(example_file))

print(f"  ✓ Parsed successfully")
print(f"    Module: {netlist['name']}")
print(f"    Inputs: {len(netlist['inputs'])}")
print(f"    Outputs: {len(netlist['outputs'])}")
print(f"    Nodes: {len(netlist['nodes'])}")
PYTHON_SCRIPT

echo ""

# Step 3: Simulate the design
echo -e "${GREEN}[3/4] Simulating design...${NC}"
python3 << PYTHON_SCRIPT
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from parsers import parse_verilog
from core.simulation.arithmetic_simulation import simulate_arithmetic_netlist, VectorValue

# Parse the example file
example_file = Path(__file__).parent / "examples" / "example_adder.v"
netlist = parse_verilog(str(example_file))

# Simulate with test inputs
test_inputs = {
    "a": VectorValue(5, 4),   # 5 in 4 bits
    "b": VectorValue(3, 4),   # 3 in 4 bits
    "cin": VectorValue(1, 1)  # 1 in 1 bit
}

print("  Test inputs:")
for name, value in test_inputs.items():
    print(f"    {name} = {value} (int: {value.to_int()})")

results = simulate_arithmetic_netlist(netlist, test_inputs)

print("  Simulation results:")
for name, value in results.items():
    if isinstance(value, VectorValue):
        print(f"    {name} = {value} (int: {value.to_int()})")
    else:
        print(f"    {name} = {value}")

# Verify: 5 + 3 + 1 = 9
expected_sum = 9
actual_sum = results.get("sum")
if actual_sum and isinstance(actual_sum, VectorValue):
    if actual_sum.to_int() == expected_sum:
        print(f"  ✓ Verification passed: {actual_sum.to_int()} == {expected_sum}")
    else:
        print(f"  ✗ Verification failed: {actual_sum.to_int()} != {expected_sum}")
        sys.exit(1)
PYTHON_SCRIPT

echo ""

# Step 4: Export to JSON
echo -e "${GREEN}[4/4] Exporting to JSON...${NC}"
python3 << PYTHON_SCRIPT
import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from parsers import parse_verilog

# Parse the example file
example_file = Path(__file__).parent / "examples" / "example_adder.v"
netlist = parse_verilog(str(example_file))

# Prepare export data
output_file = Path(__file__).parent / "outputs" / "example_output.json"
export_data = {
    "metadata": {
        "tool": "MyLogic EDA Tool v2.0.0",
        "export_time": datetime.now().isoformat(),
        "source_file": "example_adder.v",
        "version": "2.0.0"
    },
    "netlist": netlist
}

# Write JSON file
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(export_data, f, indent=2, ensure_ascii=False)

print(f"  ✓ Exported to: {output_file}")
print(f"    Nodes: {len(netlist['nodes'])}")
print(f"    Inputs: {len(netlist['inputs'])}")
print(f"    Outputs: {len(netlist['outputs'])}")
PYTHON_SCRIPT

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Example workflow completed successfully!${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "Generated files:"
echo "  - $EXAMPLE_VERILOG"
echo "  - $OUTPUT_DIR/example_output.json"
echo ""
echo "To view the JSON output:"
echo "  cat $OUTPUT_DIR/example_output.json | python -m json.tool"
echo ""

