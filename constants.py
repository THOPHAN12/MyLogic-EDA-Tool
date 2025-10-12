#!/usr/bin/env python3
"""
MyLogic EDA Tool - Global Constants

Centralized constants for consistent branding and messaging across the entire codebase.
"""

# Project Information
PROJECT_NAME = "MyLogic EDA Tool"
PROJECT_VERSION = "2.0.0"
PROJECT_AUTHOR = "MyLogic EDA Tool Team"
PROJECT_EMAIL = "thophan12@example.com"

# Project Descriptions
PROJECT_DESCRIPTION_SHORT = "Unified Electronic Design Automation Tool"
PROJECT_DESCRIPTION_LONG = "Unified Electronic Design Automation Tool with Advanced VLSI CAD Algorithms"
PROJECT_DESCRIPTION_DETAILED = "A comprehensive EDA tool for digital circuit design, logic synthesis, optimization, and verification with both scalar and vector support, powered by Yosys synthesis engine and advanced VLSI CAD algorithms."

# Branding Messages
WELCOME_MESSAGE = f"{PROJECT_NAME} v{PROJECT_VERSION}"
SUBTITLE_MESSAGE = PROJECT_DESCRIPTION_LONG
FEATURES_MESSAGE = "Enhanced Vector Simulation & Professional Synthesis Support"

# Shell Configuration
DEFAULT_PROMPT = "mylogic> "
DEFAULT_HISTORY_SIZE = 1000
DEFAULT_AUTO_COMPLETE = True
DEFAULT_COLOR_OUTPUT = True

# URLs and Links
GITHUB_URL = "https://github.com/THOPHAN12/MyLogic-EDA-Tool"
DOCS_URL = "https://github.com/THOPHAN12/MyLogic-EDA-Tool/tree/main/docs"
ISSUES_URL = "https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues"
DISCUSSIONS_URL = "https://github.com/THOPHAN12/MyLogic-EDA-Tool/discussions"

# Technical Constants
SUPPORTED_PYTHON_VERSIONS = ["3.8", "3.9", "3.10", "3.11", "3.12"]
MIN_PYTHON_VERSION = "3.8"

# Algorithm Names (for consistency)
ALGORITHMS = {
    "STRASH": "Structural Hashing",
    "DCE": "Dead Code Elimination", 
    "CSE": "Common Subexpression Elimination",
    "CONSTPROP": "Constant Propagation",
    "BALANCE": "Logic Balancing"
}

# VLSI CAD Algorithm Names
VLSI_ALGORITHMS = {
    "BDD": "Binary Decision Diagrams",
    "SAT": "SAT Solver",
    "PLACEMENT": "Placement Algorithms",
    "ROUTING": "Routing Algorithms",
    "STA": "Static Timing Analysis",
    "TECHMAP": "Technology Mapping"
}

# File Extensions
SUPPORTED_INPUT_EXTENSIONS = [".v", ".verilog"]
SUPPORTED_OUTPUT_EXTENSIONS = [".v", ".json", ".blif", ".edif", ".spice", ".dot", ".liberty", ".sv"]

# Default Paths
DEFAULT_EXAMPLES_PATH = "examples/"
DEFAULT_OUTPUTS_PATH = "outputs/"
DEFAULT_TEMP_PATH = "temp/"
DEFAULT_DOCS_PATH = "docs/"

# License Information
LICENSE = "MIT"
LICENSE_URL = "https://opensource.org/licenses/MIT"

# Keywords for PyPI
PYPI_KEYWORDS = ["eda", "vlsi", "synthesis", "optimization", "simulation", "verilog", "yosys"]

# Development Status
DEVELOPMENT_STATUS = "4 - Beta"

# Intended Audiences
INTENDED_AUDIENCES = [
    "Developers",
    "Science/Research", 
    "Education"
]

# Topics
TOPICS = [
    "Scientific/Engineering :: Electronic Design Automation (EDA)",
    "Software Development :: Libraries :: Python Modules",
    "Education"
]
