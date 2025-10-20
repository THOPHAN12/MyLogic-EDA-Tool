"""
Setup script for MyLogic Tools package

This allows the tools to be installed as a separate package:
    pip install -e tools/
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding='utf-8') if readme_file.exists() else ""

setup(
    name="mylogic-tools",
    version="2.0.0",
    author="MyLogic EDA Tool Team",
    author_email="thophan12@example.com",
    description="Utility tools for MyLogic EDA Tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/THOPHAN12/MyLogic-EDA-Tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Electronic Design Automation (EDA)",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Core dependencies (same as main project)
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov>=3.0',
            'black>=22.0',
            'flake8>=4.0',
            'mypy>=0.950',
        ],
        'visualization': [
            'matplotlib>=3.5',
            'graphviz>=0.20',
        ],
    },
    entry_points={
        'console_scripts': [
            'mylogic-convert=converters.convert_to_yosys_format:main',
            'mylogic-analyze=analyzers.explain_cell_types:main',
            'mylogic-visualize=visualizers.create_svg_from_json:main',
        ],
    },
    keywords=[
        'eda',
        'electronic-design-automation',
        'vlsi',
        'circuit-analysis',
        'visualization',
        'format-conversion',
    ],
    project_urls={
        'Bug Reports': 'https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues',
        'Source': 'https://github.com/THOPHAN12/MyLogic-EDA-Tool',
        'Documentation': 'https://github.com/THOPHAN12/MyLogic-EDA-Tool/tree/main/docs',
    },
)

