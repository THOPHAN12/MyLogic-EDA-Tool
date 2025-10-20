# Visualizers

Tools for creating visual representations of circuits in MyLogic EDA Tool.

## Files

### `create_svg_from_json.py`
**Purpose**: Generate SVG from Yosys JSON format

**Usage**:
```bash
python create_svg_from_json.py input.json [output.svg]
```

**Features**:
- Creates professional SVG circuit diagrams
- Adds connection lines with arrows
- Positions ports and cells logically
- Includes color coding and styling
- Fallback to manual creation if netlistsvg unavailable

### `create_all_svgs.py`
**Purpose**: Batch process all JSON files to SVG

**Usage**:
```bash
python create_all_svgs.py
```

**Features**:
- Automatically finds all JSON files
- Creates SVG for each JSON file
- Provides batch processing report
- Handles errors gracefully

### `create_demo_svg.py`
**Purpose**: Create demo SVG files

**Usage**:
```bash
python create_demo_svg.py
```

**Features**:
- Creates simple demo circuit
- Shows basic SVG features
- Educational example
- Professional styling

## Visualization Features

### SVG Elements
- **Ports**: Input (green) and output (red) ports
- **Cells**: Logic gates and arithmetic units
- **Connections**: Lines with arrows showing signal flow
- **Labels**: Signal names and connection descriptions
- **Styling**: Professional colors and layout

### Layout Algorithm
1. **Input Ports**: Positioned on the left
2. **Logic Cells**: Positioned in the center
3. **Output Ports**: Positioned on the right
4. **Connections**: Lines connecting related elements
5. **Labels**: Text describing connections

### Color Scheme
- **Green**: Input ports
- **Red**: Output ports
- **Orange**: Logic gates
- **Blue**: Module titles
- **Black**: Connection lines
- **Gray**: Labels and annotations

## Output Formats

| Tool | Input | Output | Features |
|------|-------|--------|----------|
| **create_svg_from_json.py** | Yosys JSON | SVG | Full circuit diagram |
| **create_all_svgs.py** | Multiple JSON | Multiple SVG | Batch processing |
| **create_demo_svg.py** | None | Demo SVG | Educational example |

## SVG Features

- **Scalable**: Vector graphics for any size
- **Interactive**: Hover and click support
- **Professional**: Industry-standard styling
- **Educational**: Clear signal flow visualization
- **Compatible**: Works in all modern browsers
