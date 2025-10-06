# 📊 MYLOGIC BENCHMARKS

## 🎯 Mục đích

Thư mục này chứa các benchmark circuits để test performance và functionality của MyLogic EDA Tool.

## 📁 Cấu trúc

- `small/` - Small circuits (< 100 gates)
- `medium/` - Medium circuits (100-1000 gates)  
- `large/` - Large circuits (> 1000 gates)
- `performance/` - Performance test results

## 🚀 Sử dụng

```bash
# Chạy benchmark
python scripts/run_benchmarks.py

# Test performance
python scripts/performance_test.py
```

## 📈 Metrics

- **Synthesis Time**: Thời gian synthesis
- **Memory Usage**: Sử dụng bộ nhớ
- **Gate Count**: Số lượng gates
- **Optimization Level**: Mức độ tối ưu hóa
