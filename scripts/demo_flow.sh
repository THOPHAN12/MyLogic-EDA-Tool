#!/bin/bash
# MyLogic EDA Tool Demo Script
# Hướng dẫn sử dụng cơ bản

echo "=== MyLogic EDA Tool Demo ==="
echo "1. Khởi động MyLogic..."
python mylogic.py --file examples/arithmetic_operations.v

echo "2. Chạy synthesis..."
python mylogic.py
# Trong shell: read examples/arithmetic_operations.v
# Trong shell: mylogic_flow examples/arithmetic_operations.v balanced
# Trong shell: write_verilog output.v
# Trong shell: exit

echo "3. Demo hoàn thành!"
