# MyLogic Tools - Makefile
# Professional build and development tasks

.PHONY: help install install-dev test lint format clean build upload docs

# Default target
help:
	@echo "MyLogic Tools - Available Commands:"
	@echo ""
	@echo "  make install       - Install the package"
	@echo "  make install-dev   - Install with development dependencies"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run linters (flake8, mypy)"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Clean build artifacts"
	@echo "  make build         - Build distribution packages"
	@echo "  make upload        - Upload to PyPI (requires credentials)"
	@echo "  make docs          - Generate documentation"
	@echo ""

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev,visualization]"

# Testing
test:
	pytest tests/ -v --cov=. --cov-report=html --cov-report=term

test-quick:
	pytest tests/ -v

# Code quality
lint:
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
	mypy .

format:
	black .

check-format:
	black --check .

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name '*.py[co]' -delete
	find . -type f -name '*.so' -delete

# Building
build: clean
	python -m build

# Upload to PyPI
upload: build
	python -m twine upload dist/*

upload-test: build
	python -m twine upload --repository testpypi dist/*

# Documentation
docs:
	@echo "Generating documentation..."
	@echo "README files are already in place"
	@echo "See tools/README.md for main documentation"

# Development
dev-setup: install-dev
	@echo "Development environment set up successfully"
	@echo "Run 'make test' to verify installation"

# Verification
verify: lint test
	@echo "All checks passed!"

# Quick development cycle
dev: format lint test
	@echo "Development cycle complete!"

