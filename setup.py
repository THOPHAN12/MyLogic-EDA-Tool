#!/usr/bin/env python3
"""
Setup script for MyLogic EDA Tool.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mylogic-eda",
    version="2.0.0",
    author="MyLogic EDA Tool Team",
    author_email="thophan12@example.com",
    description="Unified Electronic Design Automation Tool with Advanced VLSI CAD Algorithms",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/THOPHAN12/MyLogic-EDA-Tool",
    project_urls={
        "Bug Reports": "https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues",
        "Source": "https://github.com/THOPHAN12/MyLogic-EDA-Tool",
        "Documentation": "https://github.com/THOPHAN12/MyLogic-EDA-Tool/tree/main/docs",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
    ],
    keywords="eda vlsi synthesis optimization simulation verilog yosys",
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
        ],
        "docs": [
            "sphinx>=5.0.0",
            "sphinx-rtd-theme>=1.0.0",
            "myst-parser>=0.18.0",
        ],
        "visualization": [
            "matplotlib>=3.5.0",
            "graphviz>=0.20.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mylogic=mylogic:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.md", "*.txt", "*.lib", "*.v"],
        "techlibs": ["*.lib", "*.json"],
        "docs": ["*.md"],
        "examples": ["*.v"],
    },
    zip_safe=False,
)
