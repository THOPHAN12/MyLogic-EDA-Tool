# Changelog

All notable changes to the MyLogic Tools package will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-20

### Added
- **Project Organization**: Reorganized all tools into logical categories
  - `converters/`: Format conversion tools
  - `analyzers/`: Circuit analysis tools
  - `visualizers/`: SVG generation tools
  - `utilities/`: Testing and validation tools

- **Documentation**:
  - Main `README.md` with comprehensive overview
  - Category-specific README files for each subdirectory
  - `ORGANIZATION_SUMMARY.md` detailing the reorganization
  - `CONTRIBUTING.md` with contribution guidelines
  - This `CHANGELOG.md` file

- **Package Structure**:
  - `__init__.py` files for proper Python package structure
  - `setup.py` for package installation
  - `requirements.txt` for dependency management

- **Converters** (1 tool):
  - `convert_to_yosys_format.py`: Convert MyLogic JSON to Yosys JSON

- **Analyzers** (5 tools):
  - `compare_formats.py`: Compare MyLogic vs Yosys formats
  - `show_yosys_structure.py`: Display Yosys JSON structure
  - `explain_cell_types.py`: Explain circuit cell types
  - `cell_types_summary.py`: Quick cell types summary
  - `demo_mylogic_visualization.py`: Demo visualization capabilities

- **Visualizers** (3 tools):
  - `create_svg_from_json.py`: Generate SVG from JSON
  - `create_all_svgs.py`: Batch SVG generation
  - `create_demo_svg.py`: Create demo circuits

- **Utilities** (4 tools):
  - `simple_test.py`: Basic format validation
  - `test_netlistsvg_compatibility.py`: Test netlistsvg compatibility
  - `compare_svg_versions.py`: Compare SVG versions
  - `view_svg_details.py`: Detailed SVG analysis

### Changed
- Moved all tools from root directory to organized subdirectories
- Updated import paths to reflect new structure
- Improved documentation structure and clarity
- Enhanced code organization and maintainability

### Fixed
- Unicode encoding issues in terminal output
- Path handling for cross-platform compatibility
- Import path issues after reorganization

## [1.0.0] - 2025-10-19

### Added
- Initial release of standalone tools
- Basic format conversion functionality
- Simple circuit analysis tools
- SVG generation capabilities
- Testing utilities

### Notes
- Tools were initially in the root directory
- Limited documentation
- Basic functionality only

---

## Version History Summary

- **v2.0.0**: Major reorganization with professional structure
- **v1.0.0**: Initial standalone tools release

## Future Plans

### v2.1.0 (Planned)
- Add more format converters (BLIF, Verilog)
- Enhance SVG styling and interactivity
- Add timing analysis tools
- Improve error handling and reporting

### v2.2.0 (Planned)
- Add GUI for visualization
- Interactive circuit editing
- Advanced analysis algorithms
- Performance optimization

### v3.0.0 (Future)
- Full-featured standalone package
- Plugin architecture
- Web-based interface
- Cloud integration

---

For more information, see:
- [README.md](README.md) - Main documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - Contribution guidelines
- [GitHub Releases](https://github.com/THOPHAN12/MyLogic-EDA-Tool/releases)

