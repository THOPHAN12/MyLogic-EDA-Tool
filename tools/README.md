# MyLogic EDA Tool - Tools Directory

This directory contains all the utility tools and scripts for the MyLogic EDA Tool project.

## 📁 Directory Structure

### 🔄 `converters/`
**Purpose**: Convert between different data formats
- `convert_to_yosys_format.py` - Convert MyLogic JSON to Yosys JSON format

### 🔍 `analyzers/`
**Purpose**: Analyze and understand circuit data
- `compare_formats.py` - Compare MyLogic vs Yosys JSON formats
- `show_yosys_structure.py` - Display Yosys JSON structure
- `explain_cell_types.py` - Explain different cell types in circuits
- `cell_types_summary.py` - Summary of cell types
- `demo_mylogic_visualization.py` - Demo MyLogic visualization capabilities

### 🎨 `visualizers/`
**Purpose**: Create visual representations of circuits
- `create_svg_from_json.py` - Generate SVG from Yosys JSON
- `create_all_svgs.py` - Batch process all JSON files to SVG
- `create_demo_svg.py` - Create demo SVG files

### 🛠️ `utilities/`
**Purpose**: General utility functions and testing
- `simple_test.py` - Basic testing utilities
- `test_netlistsvg_compatibility.py` - Test netlistsvg compatibility
- `compare_svg_versions.py` - Compare different SVG versions
- `view_svg_details.py` - View detailed SVG information

## 🚀 Usage

### Converters
```bash
# Convert MyLogic JSON to Yosys format
python tools/converters/convert_to_yosys_format.py input.json output.json
```

### Analyzers
```bash
# Compare two JSON formats
python tools/analyzers/compare_formats.py file1.json file2.json

# Show Yosys structure
python tools/analyzers/show_yosys_structure.py file.json

# Explain cell types
python tools/analyzers/explain_cell_types.py file.json
```

### Visualizers
```bash
# Create SVG from JSON
python tools/visualizers/create_svg_from_json.py input.json output.svg

# Create all SVGs
python tools/visualizers/create_all_svgs.py

# Create demo SVG
python tools/visualizers/create_demo_svg.py
```

### Utilities
```bash
# Test JSON format
python tools/utilities/simple_test.py file.json

# Test netlistsvg compatibility
python tools/utilities/test_netlistsvg_compatibility.py file.json

# View SVG details
python tools/utilities/view_svg_details.py
```

## 📋 Tool Categories

| Category | Purpose | Files |
|----------|---------|-------|
| **Converters** | Format conversion | 1 file |
| **Analyzers** | Data analysis | 5 files |
| **Visualizers** | SVG generation | 3 files |
| **Utilities** | Testing & utilities | 4 files |

## 🎯 Key Features

- **Format Conversion**: MyLogic ↔ Yosys JSON
- **Circuit Analysis**: Cell types, connections, structure
- **Visualization**: SVG generation with connections
- **Testing**: Compatibility and validation tools
- **Documentation**: Comprehensive analysis tools

## 📚 Related Documentation

- [Main README](../README.md) - Project overview
- [Core Documentation](../docs/) - Detailed documentation
- [Examples](../examples/) - Example files and outputs
