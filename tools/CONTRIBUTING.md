# Contributing to MyLogic Tools

Thank you for your interest in contributing to MyLogic Tools! This document provides guidelines for contributing to the tools package.

## 🎯 Areas for Contribution

### 1. **Converters**
- Add new format converters (Verilog, BLIF, etc.)
- Improve existing conversion algorithms
- Add support for more cell types
- Optimize conversion performance

### 2. **Analyzers**
- Add new analysis tools
- Improve circuit understanding algorithms
- Add statistical analysis features
- Enhance reporting capabilities

### 3. **Visualizers**
- Improve SVG generation quality
- Add interactive features
- Support more layout algorithms
- Add animation capabilities

### 4. **Utilities**
- Add new testing utilities
- Improve validation tools
- Add benchmarking tools
- Enhance error reporting

## 📋 Contribution Guidelines

### Code Style
- Follow PEP 8 style guide
- Use type hints for function parameters and return values
- Add docstrings for all functions and classes
- Keep functions focused and single-purpose

### Documentation
- Update README.md when adding new tools
- Add usage examples for new features
- Document all function parameters
- Include error handling information

### Testing
- Add tests for new functionality
- Ensure existing tests pass
- Include edge case testing
- Document test scenarios

### File Organization
```
tools/
├── category/              # converters, analyzers, visualizers, utilities
│   ├── __init__.py       # Module initialization
│   ├── your_tool.py      # Your new tool
│   └── README.md         # Updated with your tool info
```

## 🔧 Development Setup

1. **Clone the repository**:
```bash
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool/tools
```

2. **Install development dependencies**:
```bash
pip install -e ".[dev]"
```

3. **Run tests**:
```bash
pytest tests/
```

4. **Format code**:
```bash
black .
flake8 .
mypy .
```

## 📝 Adding a New Tool

### Step 1: Choose Category
Determine which category your tool belongs to:
- **converters/**: Format conversion
- **analyzers/**: Data analysis
- **visualizers/**: SVG/diagram generation
- **utilities/**: Testing/validation

### Step 2: Create Your Tool
Create a new Python file in the appropriate directory:

```python
#!/usr/bin/env python3
"""
Brief description of your tool

Usage:
    python your_tool.py [arguments]

Author: Your Name
Date: YYYY-MM-DD
"""

import argparse
from pathlib import Path

def your_function(input_data):
    """
    Detailed description of function.
    
    Args:
        input_data: Description of input
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When invalid input
    """
    # Your implementation
    pass

def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Your tool description")
    parser.add_argument('input', help='Input file')
    parser.add_argument('-o', '--output', help='Output file')
    args = parser.parse_args()
    
    # Your main logic
    pass

if __name__ == "__main__":
    main()
```

### Step 3: Update Documentation
- Add tool description to category README.md
- Add usage examples
- Update main tools/README.md

### Step 4: Add Tests
Create tests in the corresponding test file or directory.

### Step 5: Submit Pull Request
- Create a descriptive PR title
- Explain what your tool does
- Include usage examples
- Link to related issues

## 🐛 Bug Reports

When reporting bugs, include:
- Tool name and version
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces
- Input files (if applicable)

## 💡 Feature Requests

When suggesting features:
- Describe the use case
- Explain why it's useful
- Provide examples if possible
- Consider implementation complexity

## 📧 Contact

- **GitHub Issues**: https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues
- **Email**: thophan12@example.com

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the problem, not the person
- Help others learn and grow

## 🙏 Thank You!

Your contributions make MyLogic Tools better for everyone. We appreciate your time and effort!

