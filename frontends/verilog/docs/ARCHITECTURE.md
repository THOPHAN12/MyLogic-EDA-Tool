# 🏗️ Kiến Trúc Parser - Tái Sử Dụng Code

## 📊 Kiến Trúc Sau Khi Refactor (LỒNG VÀO NHAU)

```
┌─────────────────────────────────────────────────────────────┐
│                    PARSER DISPATCHER                         │
│               (parser.py: _dispatch_assign_parser)           │
└─────────────────────────────────────────────────────────────┘
                           │
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
  ┌──────────┐    ┌─────────────────┐   ┌──────────┐
  │ Simple   │    │    Complex      │   │ Special  │
  │Expression│    │   Expression    │   │Operations│
  └──────────┘    └─────────────────┘   └──────────┘
        │                  │                  │
        │         ┌────────┴────────┐        │
        │         │                 │        │
        ▼         ▼                 ▼        ▼
  ┌──────────────────────────────────────────────┐
  │           OPERATION PARSERS                  │
  │  (operations/ - ĐƯỢC TÁI SỬ DỤNG)           │
  ├──────────────────────────────────────────────┤
  │  • bitwise.py    (&, |, ^, NAND, NOR, XNOR) │
  │  • arithmetic.py (+, -, *, /, %)            │
  │  • logical.py    (&&, ||, !)                │
  │  • comparison.py (==, !=, <, >, <=, >=)     │
  │  • shift.py      (<<, >>, <<<, >>>)         │
  │  • special.py    (ternary, concat, slice)   │
  └──────────────────────────────────────────────┘
                      │
                      ▼
              ┌──────────────┐
              │ NODE BUILDER │
              │ (Tạo nodes)  │
              └──────────────┘
```

## ✅ Lợi Ích Của Kiến Trúc Mới

### 1. **TÁI SỬ DỤNG CODE** (Code Reuse)

**TRƯỚC:**
```python
# expression_parser.py - DUPLICATE
def _operator_to_type(operator):
    return {'&': 'AND', '|': 'OR', ...}  # ❌ Duplicate

def create_node():
    # ❌ Duplicate logic từ bitwise.py
    operands = expr.split('&')
    node = create_operation_node('AND', operands)

# bitwise.py - ORIGINAL
def parse_and_operation():
    operands = expr.split('&')
    node = create_operation_node('AND', operands)
```

**SAU:**
```python
# expression_parser.py - TÁI SỬ DỤNG
def _parse_simple_sub_expression(expr, operator):
    if operator == '&':
        # ✅ TÁI SỬ DỤNG bitwise parser
        parse_bitwise_operation(builder, operator, temp, expr)
        return get_operation_node()

# bitwise.py - VẪN GIỮ NGUYÊN, được dùng lại
def parse_and_operation():
    operands = expr.split('&')
    node = create_operation_node('AND', operands)
```

### 2. **GIẢM CODE DUPLICATION**

| Aspect | Trước | Sau |
|--------|-------|-----|
| Operator mapping | 2 chỗ (bitwise + expression_parser) | 1 chỗ (operations/) |
| Parsing logic | 2 implementations | 1 implementation (tái sử dụng) |
| Maintenance | Sửa 2 chỗ | Sửa 1 chỗ |

### 3. **FLOW HIERARCHY** (Không Circular)

```
parser.py
  └─► expression_parser.py  (complex)
         └─► operations/bitwise.py  (simple)
         └─► operations/arithmetic.py  (simple)
         └─► operations/logical.py  (simple)
  └─► operations/bitwise.py  (direct, for simple cases)
```

**Quan trọng:** Flow chỉ đi **MỘT CHIỀU**
- ✅ `expression_parser` → `operations/*` (OK)
- ❌ `operations/*` → `expression_parser` (KHÔNG bao giờ)
- → **Không có circular dependency!**

## 📝 Chi Tiết Implementation

### Case 1: Simple Expression

```verilog
assign out = a & b;
```

**Flow:**
1. `parser.py` dispatcher: Không có parentheses
2. → Gọi trực tiếp `bitwise.parse_and_operation()`
3. Tạo nodes: `AND` + `BUF`

### Case 2: Complex Expression

```verilog
assign cout = (a & b) | (cin & (a ^ b));
```

**Flow:**
1. `parser.py` dispatcher: Có parentheses + nhiều operators
2. → Gọi `expression_parser.parse_complex_expression()`
3. Expression parser:
   ```
   Main operator: | (precedence thấp nhất, ngoài parens)
   Split:
     Left:  (a & b)        → simple
     Right: (cin & (a ^ b)) → complex
   
   Parse Left (a & b):
     ✅ TÁI SỬ DỤNG bitwise.parse_and_operation()
     → Tạo nodes: AND
   
   Parse Right (cin & (a ^ b)):
     Recursive:
       - Parse (a ^ b) → TÁI SỬ DỤNG bitwise.parse_xor_operation()
       - Parse cin & result → TÁI SỬ DỤNG bitwise.parse_and_operation()
   
   Combine với |:
     → Tạo nodes: OR
   ```

## 🎯 Kết Quả

### Trước Refactor:
```
expression_parser.py: 271 dòng
  - Có logic riêng để parse & | ^
  - Có mapping riêng operator → type
  - Không tái sử dụng operations/
```

### Sau Refactor:
```
expression_parser.py: ~350 dòng (thêm logic tái sử dụng)
  - ✅ TÁI SỬ DỤNG operations/ cho simple sub-expressions
  - ✅ Chỉ handle complex logic (parentheses, precedence)
  - ✅ Không duplicate mapping
  - ✅ Dễ maintain hơn
```

## 📊 Code Organization

```
frontends/verilog/
├── parser.py                    # Main dispatcher
├── expression_parser.py         # Complex expressions
│   └─► TÁI SỬ DỤNG ───┐
│                       │
└── operations/         │
    ├── arithmetic.py  ◄┘ # Simple expressions
    ├── bitwise.py     ◄┘ # ĐƯỢC TÁI SỬ DỤNG
    ├── logical.py     ◄┘
    ├── comparison.py  ◄┘
    ├── shift.py       ◄┘
    └── special.py     ◄┘
```

## 💡 Lợi Ích Thực Tế

### 1. Thêm Operator Mới
**Trước:** Sửa 2 chỗ
- operations/bitwise.py
- expression_parser.py

**Sau:** Sửa 1 chỗ
- operations/bitwise.py (expression_parser tự động tái sử dụng)

### 2. Fix Bug
**Trước:** Bug trong AND parsing
- Fix ở bitwise.py
- Nhưng expression_parser vẫn có bug (duplicate logic)

**Sau:** Bug trong AND parsing
- Fix ở bitwise.py
- ✅ Expression_parser tự động đúng (tái sử dụng)

### 3. Consistency
**Trước:** 2 implementations có thể khác nhau
- bitwise.py parse AND theo cách A
- expression_parser.py parse AND theo cách B
- ❌ Inconsistent behavior

**Sau:** 1 implementation duy nhất
- ✅ Consistent behavior
- ✅ Single source of truth

## 🎓 Best Practice Applied

1. **DRY Principle** (Don't Repeat Yourself)
   - ✅ Không duplicate code
   - ✅ Tái sử dụng existing logic

2. **Single Responsibility**
   - `operations/*`: Parse simple expressions
   - `expression_parser`: Handle complexity (parens, precedence)

3. **Dependency Direction**
   - ✅ One-way flow (no circular)
   - ✅ Clear hierarchy

4. **Maintainability**
   - ✅ Thay đổi ở 1 chỗ → apply everywhere
   - ✅ Dễ test
   - ✅ Dễ debug

---

**Kiến trúc này là BEST OF BOTH WORLDS:**
- Modular (tách biệt rõ ràng)
- Reusable (tái sử dụng code)
- Maintainable (dễ maintain)
- No duplication (không duplicate logic)

🎉 **DỄ QUẢN LÝ HƠN NHIỀU!**

