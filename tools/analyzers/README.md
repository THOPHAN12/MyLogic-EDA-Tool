# Analyzers

Tools for analyzing and understanding circuit data in MyLogic EDA Tool.

## Files

### `compare_formats.py`
**Purpose**: Compare MyLogic vs Yosys JSON formats

**Usage**:
```bash
python compare_formats.py mylogic.json yosys.json
```

**Features**:
- Compares metadata, modules, ports, cells
- Shows node types and counts
- Analyzes vector widths and connections
- Provides detailed format comparison

### `show_yosys_structure.py`
**Purpose**: Display Yosys JSON structure

**Usage**:
```bash
python show_yosys_structure.py file.json
```

**Features**:
- Shows module information
- Lists ports with directions and bits
- Displays cells with connections
- Shows netnames and attributes

### `explain_cell_types.py`
**Purpose**: Explain different cell types in circuits

**Usage**:
```bash
python explain_cell_types.py [file.json]
```

**Features**:
- Explains all supported cell types
- Shows Yosys mapping
- Analyzes specific circuit files
- Provides educational information

### `cell_types_summary.py`
**Purpose**: Summary of cell types

**Usage**:
```bash
python cell_types_summary.py
```

**Features**:
- Quick overview of cell types
- Source information
- Usage examples
- Educational content

### `demo_mylogic_visualization.py`
**Purpose**: Demo MyLogic visualization capabilities

**Usage**:
```bash
python demo_mylogic_visualization.py
```

**Features**:
- Shows current MyLogic features
- Compares with Yosys
- Explains visualization workflow
- Lists enhancement opportunities

## Analysis Categories

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **compare_formats.py** | Format comparison | 2 JSON files | Comparison report |
| **show_yosys_structure.py** | Structure analysis | Yosys JSON | Structure details |
| **explain_cell_types.py** | Cell type education | Optional JSON | Educational content |
| **cell_types_summary.py** | Quick summary | None | Summary report |
| **demo_mylogic_visualization.py** | Capability demo | None | Feature overview |

## Key Features

- **Format Analysis**: Compare different JSON formats
- **Structure Display**: Show detailed circuit structure
- **Educational Content**: Explain circuit concepts
- **Capability Demo**: Show tool features
- **Comprehensive Reports**: Detailed analysis output
