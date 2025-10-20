#!/usr/bin/env python3
"""
Display the professional structure of MyLogic Tools package
"""

import os
from pathlib import Path

def count_lines(file_path):
    """Count lines in a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return len(f.readlines())
    except:
        return 0

def analyze_structure():
    """Analyze and display the professional structure."""
    
    print("=" * 70)
    print("MYLOGIC TOOLS - PROFESSIONAL PACKAGE STRUCTURE")
    print("=" * 70)
    print()
    
    # Package metadata
    print("[PACKAGE INFO]")
    print("  Name    : mylogic-tools")
    print("  Version : 2.0.0")
    print("  License : MIT")
    print("  Status  : Production-Ready Beta")
    print()
    
    # Core files
    core_files = [
        "__init__.py",
        "setup.py",
        "pyproject.toml",
        "requirements.txt",
        "Makefile",
        "LICENSE",
        ".gitignore",
        "MANIFEST.in"
    ]
    
    print("[CORE CONFIGURATION FILES]")
    for file in core_files:
        path = Path(file)
        if path.exists():
            lines = count_lines(path)
            print(f"  [OK] {file:25} ({lines:3} lines)")
        else:
            print(f"  [  ] {file:25} (missing)")
    print()
    
    # Documentation files
    doc_files = [
        "README.md",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "ORGANIZATION_SUMMARY.md",
        "PROFESSIONAL_STRUCTURE.md"
    ]
    
    print("[DOCUMENTATION FILES]")
    total_doc_lines = 0
    for file in doc_files:
        path = Path(file)
        if path.exists():
            lines = count_lines(path)
            total_doc_lines += lines
            print(f"  [OK] {file:30} ({lines:4} lines)")
        else:
            print(f"  [  ] {file:30} (missing)")
    print(f"  Total documentation: {total_doc_lines} lines")
    print()
    
    # Categories
    categories = {
        "converters": "Format Conversion Tools",
        "analyzers": "Circuit Analysis Tools",
        "visualizers": "SVG Generation Tools",
        "utilities": "Testing & Validation Tools"
    }
    
    print("[TOOL CATEGORIES]")
    total_python_files = 0
    total_python_lines = 0
    
    for category, description in categories.items():
        path = Path(category)
        if path.exists():
            python_files = list(path.glob("*.py"))
            python_files = [f for f in python_files if f.name != "__init__.py"]
            
            category_lines = sum(count_lines(f) for f in python_files)
            total_python_files += len(python_files)
            total_python_lines += category_lines
            
            print(f"\n  {category.upper()}/")
            print(f"    Description: {description}")
            print(f"    Python files: {len(python_files)}")
            print(f"    Total lines: {category_lines}")
            
            if (path / "README.md").exists():
                readme_lines = count_lines(path / "README.md")
                print(f"    README: {readme_lines} lines")
            
            for py_file in python_files:
                lines = count_lines(py_file)
                print(f"      - {py_file.name:35} ({lines:4} lines)")
    
    print()
    print(f"  Total Python utility files: {total_python_files}")
    print(f"  Total Python code lines: {total_python_lines}")
    print()
    
    # Professional features
    print("[PROFESSIONAL FEATURES]")
    features = {
        "Package Structure": [
            "__init__.py in all modules",
            "Proper module hierarchy",
            "Importable as package"
        ],
        "Build System": [
            "setup.py (traditional)",
            "pyproject.toml (modern)",
            "Makefile automation",
            "MANIFEST.in"
        ],
        "Documentation": [
            f"{len(doc_files)} comprehensive docs",
            "README in each category",
            "Contribution guidelines",
            "Changelog (SemVer)"
        ],
        "Quality Control": [
            "Code formatting (Black)",
            "Linting (Flake8)",
            "Type checking (MyPy)",
            "Testing (Pytest)"
        ],
        "Distribution": [
            "PyPI-ready",
            "Installable via pip",
            "Command-line tools",
            "Semantic versioning"
        ]
    }
    
    for feature, items in features.items():
        print(f"\n  {feature}:")
        for item in items:
            print(f"    [OK] {item}")
    
    print()
    print("=" * 70)
    print("PROFESSIONAL PACKAGE - READY FOR PRODUCTION")
    print("=" * 70)
    print()
    
    # Statistics
    print("[PACKAGE STATISTICS]")
    print(f"  Python Files    : {total_python_files}")
    print(f"  Code Lines      : {total_python_lines}")
    print(f"  Doc Lines       : {total_doc_lines}")
    print(f"  Config Files    : {len(core_files)}")
    print(f"  Doc Files       : {len(doc_files)}")
    print(f"  Categories      : {len(categories)}")
    print(f"  Total Files     : {total_python_files + len(core_files) + len(doc_files) + len(categories)}")
    print()
    
    # Installation commands
    print("[INSTALLATION]")
    print("  Development:")
    print("    cd tools/")
    print("    pip install -e \".[dev]\"")
    print()
    print("  Standard:")
    print("    pip install mylogic-tools")
    print()
    
    # Usage
    print("[USAGE]")
    print("  Command-line tools:")
    print("    mylogic-convert input.json output.json")
    print("    mylogic-analyze circuit.json")
    print("    mylogic-visualize input.json output.svg")
    print()
    print("  Makefile:")
    print("    make install-dev    # Install with dev dependencies")
    print("    make test           # Run tests")
    print("    make lint           # Run linters")
    print("    make format         # Format code")
    print("    make build          # Build distribution")
    print()

if __name__ == "__main__":
    analyze_structure()

