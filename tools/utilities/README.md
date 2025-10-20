# Utilities

General utility functions and testing tools for MyLogic EDA Tool.

## Files

### `simple_test.py`
**Purpose**: Basic testing utilities

**Usage**:
```bash
python simple_test.py file.json
```

**Features**:
- Tests JSON format validity
- Validates cell connections
- Checks numeric bit indices
- Provides simple pass/fail results

### `test_netlistsvg_compatibility.py`
**Purpose**: Test netlistsvg compatibility

**Usage**:
```bash
python test_netlistsvg_compatibility.py file.json
```

**Features**:
- Tests JSON structure compatibility
- Validates required fields
- Checks cell connections format
- Tests netlistsvg command execution

### `compare_svg_versions.py`
**Purpose**: Compare different SVG versions

**Usage**:
```bash
python compare_svg_versions.py
```

**Features**:
- Compares SVG file sizes
- Counts elements (lines, rectangles, text)
- Checks for connections and arrows
- Analyzes enhancement opportunities

### `view_svg_details.py`
**Purpose**: View detailed SVG information

**Usage**:
```bash
python view_svg_details.py
```

**Features**:
- Shows file sizes and dimensions
- Counts SVG elements
- Extracts ports and cells
- Analyzes connections and colors
- Checks interactive features

## Testing Categories

| Tool | Purpose | Input | Output |
|------|---------|-------|--------|
| **simple_test.py** | Basic validation | JSON file | Pass/fail report |
| **test_netlistsvg_compatibility.py** | Compatibility test | JSON file | Compatibility report |
| **compare_svg_versions.py** | SVG comparison | None | Comparison report |
| **view_svg_details.py** | SVG analysis | None | Detailed analysis |

## Key Features

- **Validation**: Test data format correctness
- **Compatibility**: Check tool compatibility
- **Comparison**: Compare different versions
- **Analysis**: Detailed file information
- **Reporting**: Comprehensive test results

## Testing Workflow

1. **Basic Validation**: Use `simple_test.py` for quick checks
2. **Compatibility Testing**: Use `test_netlistsvg_compatibility.py` for tool compatibility
3. **Version Comparison**: Use `compare_svg_versions.py` for SVG analysis
4. **Detailed Analysis**: Use `view_svg_details.py` for comprehensive information

## Error Handling

- **Graceful Failures**: Tools handle errors without crashing
- **Detailed Messages**: Clear error descriptions
- **Fallback Options**: Alternative approaches when tools fail
- **Progress Reporting**: Status updates during processing
