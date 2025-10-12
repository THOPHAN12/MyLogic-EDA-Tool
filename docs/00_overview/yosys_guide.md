# 🎯 **HƯỚNG DẪN YOSYS CHO MYLOGIC EDA TOOL**

## 📋 **TỔNG QUAN YOSYS**

**Yosys** là công cụ synthesis mạnh mẽ cho Verilog, được tích hợp vào MyLogic EDA Tool để cung cấp khả năng synthesis chuyên nghiệp.

> **Tài liệu tham khảo**: [YosysHQ Documentation](https://yosyshq.readthedocs.io/en/latest/) - Hướng dẫn chính thức từ YosysHQ

## 🔧 **CÀI ĐẶT YOSYS**

### **Windows:**
```bash
# Download từ GitHub
https://github.com/YosysHQ/yosys/releases

# Hoặc sử dụng package manager
winget install yosys
```

### **Linux:**
```bash
sudo apt-get install yosys
# hoặc
sudo yum install yosys
```

### **macOS:**
```bash
brew install yosys
```

## 🚀 **QUY TRÌNH SYNTHESIS YOSYS**

### **1. Parsing & Elaboration**
```bash
read_verilog design.v          # Đọc Verilog file
hierarchy -check -top module   # Kiểm tra hierarchy
```

### **2. Logic Synthesis**
```bash
proc                    # Chuyển behavioral → structural
opt_expr               # Tối ưu expressions
opt_clean              # Dọn dẹp unused signals
opt_muxtree            # Tối ưu multiplexers
opt_reduce             # Tối ưu reductions
```

### **3. Technology Mapping**
```bash
techmap                # Map to target technology
abc -script +strash    # ABC optimization
clean                  # Final cleanup
```

### **4. Output Generation**
```bash
write_verilog output.v    # Verilog RTL
write_json output.json    # JSON netlist
write_blif output.blif    # BLIF format
write_dot output.dot      # DOT graph
```

## 📝 **YOSYS SCRIPT CHO MYLOGIC**

### **Basic Script:**
```bash
# MyLogic Basic Synthesis
read_verilog examples/arithmetic_operations.v
hierarchy -check -top arithmetic_operations
proc
opt
stat
write_verilog outputs/arithmetic_synth.v
write_json outputs/arithmetic_synth.json
```

### **Advanced Script:**
```bash
# MyLogic Advanced Synthesis
read_verilog examples/arithmetic_operations.v
hierarchy -check -top arithmetic_operations
proc
opt_expr
opt_clean
opt_muxtree
opt_reduce
memory
opt
techmap
abc -script +strash
clean
stat
write_verilog outputs/arithmetic_advanced.v
write_json outputs/arithmetic_advanced.json
write_blif outputs/arithmetic_advanced.blif
write_dot outputs/arithmetic_advanced.dot
```

## 🎯 **OPTIMIZATION LEVELS**

### **Fast (Prototype):**
```bash
proc
opt
abc -script +fast
```

### **Balanced (Production):**
```bash
proc
opt_expr
opt_clean
opt_muxtree
opt_reduce
opt
abc -script +balanced
```

### **Thorough (Maximum):**
```bash
proc
opt_expr
opt_clean
opt_muxtree
opt_reduce
memory
opt
techmap
abc -script +strash
abc -script +dch
abc -script +map
```

## 🔍 **COMMON YOSYS COMMANDS**

| Command | Mô tả | Ví dụ |
|---------|-------|-------|
| `read_verilog` | Đọc Verilog file | `read_verilog design.v` |
| `hierarchy` | Xử lý hierarchy | `hierarchy -check -top module` |
| `proc` | Chuyển behavioral → structural | `proc` |
| `opt` | Tối ưu hóa chung | `opt` |
| `opt_expr` | Tối ưu expressions | `opt_expr` |
| `opt_clean` | Dọn dẹp unused signals | `opt_clean` |
| `opt_muxtree` | Tối ưu multiplexers | `opt_muxtree` |
| `opt_reduce` | Tối ưu reductions | `opt_reduce` |
| `memory` | Xử lý memories | `memory` |
| `techmap` | Technology mapping | `techmap` |
| `abc` | ABC optimization | `abc -script +strash` |
| `clean` | Final cleanup | `clean` |
| `stat` | Hiển thị statistics | `stat` |
| `show` | Hiển thị design | `show` |
| `write_verilog` | Ghi Verilog output | `write_verilog output.v` |
| `write_json` | Ghi JSON netlist | `write_json output.json` |
| `write_blif` | Ghi BLIF format | `write_blif output.blif` |
| `write_dot` | Ghi DOT graph | `write_dot output.dot` |

## 🚨 **COMMON ERRORS & SOLUTIONS**

### **1. Port Mismatch:**
```
Error: Port mismatch in module
```
**Solution:** Kiểm tra port declarations và connections

### **2. Wire Undeclared:**
```
Error: Wire 'signal' is not declared
```
**Solution:** Khai báo tất cả wires trước khi sử dụng

### **3. Module Not Found:**
```
Error: Module 'module_name' not found
```
**Solution:** Kiểm tra file paths và module names

### **4. Syntax Error:**
```
Error: Syntax error in Verilog
```
**Solution:** Sử dụng Verilog syntax checker

## 🔧 **INTEGRATION VỚI MYLOGIC**

### **Sử dụng trong MyLogic:**
```python
from synthesis.mylogic_synthesis import MyLogicSynthesis

# Tạo synthesis engine
synthesis = MyLogicSynthesis()

# Chạy synthesis
result = synthesis.run_synthesis(
    "examples/arithmetic_operations.v",
    optimization_level="balanced"
)
```

### **CLI Commands:**
```bash
# Trong MyLogic shell
mylogic> yosys_flow examples/arithmetic_operations.v balanced
mylogic> yosys_stat examples/arithmetic_operations.v
mylogic> write_verilog output.v
mylogic> write_json output.json
```

## 🧪 **VERIFICATION TOOLS**

### **1. Iverilog (Simulation):**
```bash
iverilog -o sim design.v testbench.v
vvp sim
```

### **2. GTKWave (Waveform):**
```bash
gtkwave waveform.vcd
```

### **3. Netlistsvg (Visualization):**
```bash
netlistsvg input.json output.svg
```

### **4. Yosys Show (Built-in):**
```bash
yosys -p "read_verilog design.v; show" -o design.svg
```

## 📊 **PERFORMANCE METRICS**

### **Statistics Commands:**
```bash
stat                    # Basic statistics
stat -width            # Width statistics
stat -tech             # Technology statistics
```

### **Typical Results:**
- **Cells**: Number of logic cells
- **Wires**: Number of wires
- **Area**: Estimated area
- **Delay**: Estimated delay

## 🎯 **BEST PRACTICES**

### **1. Design Guidelines:**
- Sử dụng synchronous design
- Tránh combinational loops
- Proper clock domain crossing
- Clean hierarchy

### **2. Synthesis Guidelines:**
- Sử dụng appropriate optimization level
- Check statistics after synthesis
- Verify functionality
- Use multiple output formats

### **3. Debugging:**
- Sử dụng `show` command để visualize
- Check `stat` for unexpected results
- Use `write_verilog` để inspect netlist
- Verify với simulation tools

## 🚀 **NEXT STEPS**

1. **Install Yosys** nếu chưa có
2. **Run synthesis** với MyLogic
3. **Analyze results** với statistics
4. **Verify functionality** với simulation
5. **Optimize further** nếu cần

---

**📅 Ngày tạo**: 2025-10-06  
**👨‍💻 Tác giả**: MyLogic EDA Tool Team  
**📝 Phiên bản**: 1.0
