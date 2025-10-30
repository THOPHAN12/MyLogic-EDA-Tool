# Verilog Parser Documentation Index

## 📚 Documentation Structure

Thư mục này chứa tất cả documentation cho Verilog Parser module.

---

## 📖 Available Documents

### 1. [README.md](README.md)
**Mục đích:** Comprehensive documentation cho Verilog Parser

**Nội dung:**
- Overview và tổng quan
- Cấu trúc module chi tiết
- Chi tiết từng component (constants, tokenizer, node_builder, etc.)
- Usage guide với examples
- Testing guide
- Performance comparison (trước/sau refactor)
- How to extend parser

**Đối tượng:** Developers cần hiểu và sử dụng parser

---

### 2. [ARCHITECTURE.md](ARCHITECTURE.md)
**Mục đích:** Deep dive vào kiến trúc và code reuse strategy

**Nội dung:**
- Architecture diagram (hierarchy flow)
- Code reuse explanation
- Expression parser & operations integration
- Dependency direction (no circular)
- Best practices applied
- Flow chi tiết cho simple và complex expressions

**Đối tượng:** Developers cần hiểu design decisions và maintain code

---

## 🎯 Khi Nào Dùng Document Nào?

| Tình Huống | Document |
|------------|----------|
| Muốn hiểu parser làm gì | README.md |
| Cần examples usage | README.md |
| Muốn thêm operator mới | README.md (Adding New Operations) |
| Hiểu tại sao design như vậy | ARCHITECTURE.md |
| Hiểu code reuse strategy | ARCHITECTURE.md |
| Debug complex expression | ARCHITECTURE.md |
| Maintain existing code | Cả 2 documents |

---

## 📁 Documentation Organization

```
verilog/
├── docs/                         # 📚 DOCUMENTATION (Học thuật)
│   ├── INDEX.md                  # File này - Navigation
│   ├── README.md                 # Comprehensive guide
│   └── ARCHITECTURE.md           # Design & architecture
│
├── core/                         # 🎯 CORE IMPLEMENTATION (Organized)
│   ├── __init__.py
│   ├── constants.py              # Regex patterns & constants
│   ├── tokenizer.py              # Tokenization & cleaning
│   ├── node_builder.py           # Node creation & wires
│   ├── parser.py                 # Main parser logic
│   └── expression_parser.py     # Complex expressions
│
└── operations/                   # 🔧 OPERATION PARSERS (Modular)
    ├── __init__.py
    ├── arithmetic.py             # +, -, *, /, %
    ├── bitwise.py                # &, |, ^, ~, NAND, NOR, XNOR
    ├── logical.py                # &&, ||, !
    ├── comparison.py             # ==, !=, <, >, <=, >=
    ├── shift.py                  # <<, >>, <<<, >>>
    └── special.py                # ternary, concat, slice
```

**Lợi ích của cấu trúc này:**
- ✅ **Separation of Concerns**: Documentation, Core, Operations tách biệt
- ✅ **Clear Hierarchy**: `docs/` → `core/` → `operations/`
- ✅ **Easy Navigation**: Biết đi đâu tìm gì
- ✅ **Professional**: Follow chuẩn học thuật và industry best practices
- ✅ **Scalable**: Dễ thêm docs/features mới

---

## 🔗 External Documentation

### Project Level
- **Main Project README**: [../../../README.md](../../../README.md)
- **Frontends Overview**: [../../README.md](../../README.md)

### API References
- **API Documentation**: [../../../docs/00_overview/api_reference.md](../../../docs/00_overview/api_reference.md)

---

## 📝 Documentation Standards

### 1. **Format**
- Markdown (.md) format
- Tiếng Việt với technical terms tiếng Anh
- Code blocks với syntax highlighting

### 2. **Structure**
- Clear headings hierarchy (H1 → H2 → H3)
- Table of contents cho docs dài
- Examples cho mọi concept

### 3. **Content**
- Giải thích "tại sao" không chỉ "như thế nào"
- Visual diagrams khi có thể
- Before/after comparisons
- Use cases thực tế

### 4. **Maintenance**
- Update khi code thay đổi
- Version trong document nếu cần
- Date của update cuối

---

## 🎓 Academic Standards Applied

Folder **`docs/`** follow các best practices học thuật:

1. **Separation of Concerns**
   - Documentation riêng khỏi implementation
   - Easy to read without code clutter

2. **Hierarchical Organization**
   - INDEX cho navigation
   - README cho overview
   - Specialized docs cho deep dives

3. **Comprehensive Coverage**
   - What, Why, How
   - Examples và use cases
   - Architecture reasoning

4. **Maintainability**
   - Clear structure
   - Easy to update
   - Consistent format

---

## 🚀 Quick Navigation

**Tôi muốn...**

- **Bắt đầu sử dụng parser** → [README.md](README.md) Section "Usage"
- **Hiểu cấu trúc code** → [README.md](README.md) Section "Cấu Trúc Module"
- **Thêm operator mới** → [README.md](README.md) Section "Adding New Operations"
- **Hiểu design decisions** → [ARCHITECTURE.md](ARCHITECTURE.md)
- **Fix bug trong complex expr** → [ARCHITECTURE.md](ARCHITECTURE.md) Section "Flow"
- **Understand code reuse** → [ARCHITECTURE.md](ARCHITECTURE.md) Section "Code Reuse"

---

## 📊 Documentation Metrics

| Metric | Value |
|--------|-------|
| **Total Docs** | 3 files |
| **Total Lines** | ~850 lines |
| **Language** | Tiếng Việt + English terms |
| **Format** | Markdown |
| **Diagrams** | ASCII art + text |
| **Code Examples** | 20+ examples |
| **Coverage** | Comprehensive |

---

## 💡 Tips for Readers

1. **Start with README.md** - Comprehensive overview
2. **Dive into ARCHITECTURE.md** - When you need to understand "why"
3. **Use INDEX.md** - For navigation và quick reference
4. **Check code comments** - Docstrings in source files
5. **Try examples** - Best way to learn

---

## 🔄 Update History

| Date | Document | Change |
|------|----------|--------|
| Oct 2024 | All | Initial creation after refactoring |
| Oct 2024 | ARCHITECTURE.md | Added code reuse section |
| Oct 2024 | INDEX.md | Created navigation guide |

---

**Happy Reading!** 📖

*For questions or improvements, contact MyLogic Team*

