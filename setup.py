#!/usr/bin/env python3
"""
Setup script for MyLogic EDA Tool.
"""

from setuptools import setup, find_packages
import os

# Import constants
from constants import (
    PROJECT_NAME, PROJECT_VERSION, PROJECT_AUTHOR, PROJECT_EMAIL,
    PROJECT_DESCRIPTION_LONG, GITHUB_URL, DOCS_URL, ISSUES_URL,
    SUPPORTED_PYTHON_VERSIONS, MIN_PYTHON_VERSION, LICENSE, PYPI_KEYWORDS,
    DEVELOPMENT_STATUS, INTENDED_AUDIENCES, TOPICS
)

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
    version=PROJECT_VERSION,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_EMAIL,
    description=PROJECT_DESCRIPTION_LONG,
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url=GITHUB_URL,
    project_urls={
        "Bug Reports": ISSUES_URL,
        "Source": GITHUB_URL,
        "Documentation": DOCS_URL,
    },
    packages=find_packages(),
    classifiers=[
        f"Development Status :: {DEVELOPMENT_STATUS}",
        *[f"Intended Audience :: {audience}" for audience in INTENDED_AUDIENCES],
        f"License :: OSI Approved :: {LICENSE} License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        *[f"Programming Language :: Python :: {version}" for version in SUPPORTED_PYTHON_VERSIONS],
        *TOPICS,
    ],
    keywords=" ".join(PYPI_KEYWORDS),
    python_requires=f">={MIN_PYTHON_VERSION}",
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
