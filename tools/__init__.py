"""
MyLogic EDA Tool - Tools Package
=================================

This package provides utility tools for working with MyLogic EDA Tool,
including format conversion, circuit analysis, visualization, and testing.

Modules:
    converters: Format conversion utilities
    analyzers: Circuit analysis tools
    visualizers: SVG and diagram generation
    utilities: Testing and validation utilities

Version: 2.0.0
Author: MyLogic EDA Tool Team
License: MIT
"""

__version__ = "2.0.0"
__author__ = "MyLogic EDA Tool Team"
__all__ = [
    'converters',
    'analyzers',
    'visualizers',
    'utilities'
]

# Package metadata
PACKAGE_INFO = {
    "name": "mylogic-tools",
    "version": __version__,
    "description": "Utility tools for MyLogic EDA Tool",
    "author": __author__,
    "license": "MIT"
}

def get_version():
    """Return the version of the tools package."""
    return __version__

def get_package_info():
    """Return package information."""
    return PACKAGE_INFO.copy()

