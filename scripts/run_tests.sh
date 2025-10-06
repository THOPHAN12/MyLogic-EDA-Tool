#!/bin/bash
# MyLogic EDA Tool Test Runner
# Chạy tất cả tests

echo "=== MyLogic EDA Tool Test Suite ==="
echo "Chạy unit tests..."

# Chạy tests
python -m pytest tests/ -v

echo "Tests hoàn thành!"
