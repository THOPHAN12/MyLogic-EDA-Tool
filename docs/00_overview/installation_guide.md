# HƯỚNG DẪN CÀI ĐẶT MYLOGIC EDA TOOL

## 📋 Yêu cầu hệ thống

### **Hệ điều hành hỗ trợ:**
- Windows 10/11
- Linux (Ubuntu 18.04+, CentOS 7+)
- macOS 10.15+

### **Python:**
- Python 3.8 trở lên
- pip package manager

## 🚀 Cài đặt nhanh

### **Bước 1: Clone repository**
```bash
git clone <repository-url>
cd Mylogic
```

### **Bước 2: Cài đặt dependencies**
```bash
# Cài đặt dependencies cơ bản
pip install -r requirements.txt

# Hoặc cài đặt từng package
pip install numpy matplotlib
```

### **Bước 3: Cài đặt dependencies tùy chọn**

#### **Graphviz (cho DOT output):**
```bash
# Windows: Download từ https://graphviz.org/download/
# Linux: 
sudo apt-get install graphviz
# macOS:
brew install graphviz
```

#### **Yosys (cho synthesis features):**
```bash
# Windows: Download từ https://github.com/YosysHQ/yosys/releases
# Linux:
sudo apt-get install yosys
# macOS:
brew install yosys
```

### **Bước 4: Kiểm tra cài đặt**
```bash
python mylogic.py --check-deps
```

## 🔧 Cài đặt từ source

### **Development setup:**
```bash
# Clone repository
git clone <repository-url>
cd Mylogic

# Cài đặt development dependencies
pip install -r requirements.txt
pip install -e .

# Chạy tests
python -m pytest tests/
```

## 🐛 Troubleshooting

### **Lỗi thường gặp:**

1. **ImportError: No module named 'numpy'**
   ```bash
   pip install numpy
   ```

2. **Yosys not found**
   - Cài đặt Yosys theo hướng dẫn trên
   - Kiểm tra PATH environment variable

3. **Graphviz not found**
   - Cài đặt Graphviz
   - Kiểm tra `dot` command có hoạt động

### **Debug mode:**
```bash
python mylogic.py --debug
```

## 📚 Tài liệu tham khảo

- [README.md](../README.md) - Hướng dẫn sử dụng
- [Project Structure Guide](project_structure_guide.md) - Cấu trúc dự án
- [API Documentation](api_reference.md) - Tham khảo API
