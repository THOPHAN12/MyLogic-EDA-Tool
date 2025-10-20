# Converters

Tools for converting between different data formats in MyLogic EDA Tool.

## Files

### `convert_to_yosys_format.py`
**Purpose**: Convert MyLogic JSON format to Yosys JSON format

**Usage**:
```bash
python convert_to_yosys_format.py input.json [output.json]
```

**Features**:
- Converts MyLogic netlist to Yosys format
- Maps cell types (MUX → $_MUX_, BUF → $_BUF_)
- Creates proper port definitions
- Generates numeric bit indices for connections
- Compatible with netlistsvg and other Yosys tools

**Input**: MyLogic JSON file
**Output**: Yosys JSON file

**Example**:
```bash
python convert_to_yosys_format.py examples/priority_encoder_netlist.json examples/priority_encoder_yosys.json
```

## Conversion Process

1. **Parse MyLogic JSON**: Read netlist structure
2. **Map Cell Types**: Convert MyLogic types to Yosys types
3. **Create Ports**: Define input/output ports with bit indices
4. **Generate Cells**: Create Yosys cell definitions
5. **Add Connections**: Map signal connections with numeric indices
6. **Output Yosys JSON**: Write compatible format

## Supported Conversions

| MyLogic Type | Yosys Type | Description |
|--------------|------------|-------------|
| MUX | $_MUX_ | Multiplexer |
| BUF | $_BUF_ | Buffer |
| AND | $_AND_ | Logic AND |
| OR | $_OR_ | Logic OR |
| XOR | $_XOR_ | Logic XOR |
| NOT | $_NOT_ | Logic NOT |
| ADD | $_ADD_ | Addition |
| SUB | $_SUB_ | Subtraction |
| MUL | $_MUL_ | Multiplication |
| DIV | $_DIV_ | Division |
