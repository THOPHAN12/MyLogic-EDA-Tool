# 👥 Team Roles and Permissions - Quyền Hạn và Trách Nhiệm

## 📋 **TÓM TẮT**

- **Quyền hạn**: Cả Thọ và Minh đều có quyền như nhau trên repository
- **Trách nhiệm**: Mỗi người chủ yếu đảm nhiệm branches của mình
- **Review**: Có thể review và merge code của nhau
- **Best Practice**: Nên có quy tắc rõ ràng về ai merge code của ai

---

## 🔐 **QUYỀN HẠN TRONG GIT**

### **1. Quyền trên Repository**

Nếu cả hai đều có quyền **Collaborator** hoặc **Admin** trên GitHub:

✅ **Cả hai đều có thể:**
- Tạo branches mới
- Push code lên branches
- Merge branches vào `develop`
- Tạo Pull Requests
- Review code của nhau
- Xóa branches (cẩn thận!)

### **2. Quyền trên Local Repository**

Trên máy local, mỗi người có **full quyền**:
- Tạo, xóa, merge branches
- Commit, push, pull
- Không có giới hạn

---

## 👨‍💻 **TRÁCH NHIỆM VÀ PHÂN CÔNG**

### **Thọ - Main Developer**

**Branches chính:**
- `feature/tho-library-loader`
- `feature/tho-technology-mapping`
- `feature/tho-synthesis-algorithms`

**Trách nhiệm:**
- ✅ Phát triển các tính năng core (library loader, technology mapping)
- ✅ Review code của Minh trước khi merge
- ✅ Merge code của Minh vào `develop` (nếu approve)
- ✅ Đảm bảo code quality
- ✅ Merge `develop` → `main` khi release

### **Minh - Collaborator**

**Branches chính:**
- `feature/minh-cli-improvements`
- `feature/minh-testing`
- `feature/minh-documentation`

**Trách nhiệm:**
- ✅ Phát triển các tính năng hỗ trợ (CLI, testing, docs)
- ✅ Review code của Thọ trước khi merge
- ✅ Merge code của Thọ vào `develop` (nếu approve)
- ✅ Đảm bảo testing và documentation
- ✅ Báo cáo bugs và issues

---

## 🔀 **QUY TẮC MERGE**

### **Quy Tắc 1: Code Review (Khuyên dùng)**

**Workflow:**
1. **Thọ** code trên `feature/tho-xxx`
2. **Thọ** tạo Pull Request: `feature/tho-xxx` → `develop`
3. **Minh** review code
4. **Minh** approve hoặc request changes
5. **Minh** merge vào `develop` (nếu approve)

**Tương tự:**
1. **Minh** code trên `feature/minh-xxx`
2. **Minh** tạo Pull Request: `feature/minh-xxx` → `develop`
3. **Thọ** review code
4. **Thọ** approve hoặc request changes
5. **Thọ** merge vào `develop` (nếu approve)

### **Quy Tắc 2: Self-Merge (Nếu tin tưởng)**

**Workflow:**
- Mỗi người tự merge branch của mình vào `develop`
- Nhưng vẫn nên có review trước khi merge

### **Quy Tắc 3: Owner Merge (An toàn nhất)**

**Workflow:**
- **Thọ** merge tất cả branches (của cả Thọ và Minh)
- **Minh** chỉ push code, không merge
- Đảm bảo code quality và consistency

---

## 📝 **RECOMMENDED WORKFLOW**

### **Scenario 1: Thọ phát triển tính năng mới**

```bash
# 1. Thọ tạo branch
git checkout develop
git pull origin develop
git checkout -b feature/tho-new-feature

# 2. Thọ code và commit
git add .
git commit -m "feat: Add new feature"
git push origin feature/tho-new-feature

# 3. Thọ tạo Pull Request trên GitHub
#    feature/tho-new-feature → develop

# 4. Minh review code
#    - Check logic
#    - Test functionality
#    - Comment nếu có vấn đề

# 5. Minh approve và merge (nếu OK)
#    Hoặc Thọ tự merge nếu Minh approve

# 6. Sau khi merge, cả hai sync
git checkout develop
git pull origin develop
```

### **Scenario 2: Minh phát triển tính năng mới**

```bash
# 1. Minh tạo branch
git checkout develop
git pull origin develop
git checkout -b feature/minh-new-feature

# 2. Minh code và commit
git add .
git commit -m "feat: Add new feature"
git push origin feature/minh-new-feature

# 3. Minh tạo Pull Request trên GitHub
#    feature/minh-new-feature → develop

# 4. Thọ review code
#    - Check logic
#    - Test functionality
#    - Comment nếu có vấn đề

# 5. Thọ approve và merge (nếu OK)
#    Hoặc Minh tự merge nếu Thọ approve

# 6. Sau khi merge, cả hai sync
git checkout develop
git pull origin develop
```

---

## ⚠️ **QUY TẮC QUAN TRỌNG**

### **1. KHÔNG merge code của chính mình mà không review**

❌ **Sai:**
```bash
# Thọ tự merge mà không có review
git checkout develop
git merge feature/tho-xxx
git push origin develop
```

✅ **Đúng:**
```bash
# Tạo Pull Request và chờ review
# Hoặc ít nhất tự review code trước khi merge
```

### **2. LUÔN sync với develop trước khi merge**

```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
# Resolve conflicts nếu có
```

### **3. KHÔNG force push lên shared branches**

❌ **Sai:**
```bash
git push --force origin develop  # NGUY HIỂM!
```

✅ **Đúng:**
```bash
git push origin develop  # Safe push
```

### **4. COMMUNICATE trước khi merge lớn**

- Thông báo trước khi merge feature lớn
- Đảm bảo không conflict với code của người kia
- Sync và test trước khi merge

---

## 🎯 **PHÂN CÔNG CỤ THỂ**

### **Thọ đảm nhiệm:**

1. **Core Algorithms:**
   - Logic synthesis (Strash, CSE, ConstProp, Balance)
   - Technology mapping
   - Library loading (Liberty, JSON)

2. **Architecture:**
   - Core module structure
   - Algorithm implementation
   - Performance optimization

3. **Review:**
   - Review code của Minh
   - Approve/Reject Pull Requests
   - Merge code vào `develop`

### **Minh đảm nhiệm:**

1. **Supporting Features:**
   - CLI improvements
   - Testing framework
   - Documentation

2. **Quality Assurance:**
   - Unit tests
   - Integration tests
   - Bug reports

3. **Review:**
   - Review code của Thọ
   - Approve/Reject Pull Requests
   - Merge code vào `develop`

---

## 🔍 **CODE REVIEW CHECKLIST**

### **Khi Review Code:**

- [ ] Code logic đúng chưa?
- [ ] Có test cases chưa?
- [ ] Có documentation chưa?
- [ ] Có lỗi syntax/linting không?
- [ ] Performance có OK không?
- [ ] Có conflict với code hiện tại không?
- [ ] Commit messages có rõ ràng không?

### **Approve nếu:**
- ✅ Code đúng logic
- ✅ Có tests
- ✅ Không có conflicts
- ✅ Code quality tốt

### **Request Changes nếu:**
- ❌ Có bugs
- ❌ Thiếu tests
- ❌ Code không rõ ràng
- ❌ Có conflicts

---

## 📊 **PERMISSION MATRIX**

| Action | Thọ | Minh | Notes |
|--------|-----|------|-------|
| Create branch | ✅ | ✅ | Cả hai đều có thể |
| Push to own branch | ✅ | ✅ | Cả hai đều có thể |
| Push to develop | ✅ | ✅ | Nên có review trước |
| Merge own PR | ✅ | ✅ | Nên có review trước |
| Merge other's PR | ✅ | ✅ | Sau khi review |
| Delete branch | ✅ | ✅ | Cẩn thận! |
| Force push | ⚠️ | ⚠️ | Chỉ khi cần thiết |

---

## 🚨 **XỬ LÝ CONFLICTS**

### **Khi có conflict:**

1. **Người tạo PR xử lý conflict:**
   ```bash
   git checkout feature/your-branch
   git merge develop
   # Resolve conflicts
   git add .
   git commit -m "fix: Resolve merge conflicts"
   git push origin feature/your-branch
   ```

2. **Người review kiểm tra lại:**
   - Check xem conflict đã được resolve đúng chưa
   - Approve nếu OK

---

## 💡 **BEST PRACTICES**

### **1. Communication**

- Thông báo khi bắt đầu feature mới
- Thông báo khi sắp merge
- Discuss về architecture changes

### **2. Code Review**

- Review kỹ trước khi merge
- Comment rõ ràng
- Approve/Reject dựa trên chất lượng code

### **3. Testing**

- Test trước khi push
- Đảm bảo không break existing features
- Run tests trước khi merge

### **4. Documentation**

- Update docs khi thêm feature mới
- Comment code rõ ràng
- Update README nếu cần

---

## 📚 **TÓM TẮT**

### **Quyền hạn:**
- ✅ Cả hai đều có quyền như nhau
- ✅ Cả hai đều có thể merge
- ✅ Cả hai đều có thể review

### **Trách nhiệm:**
- 👨‍💻 **Thọ**: Core algorithms, architecture, review code của Minh
- 👨‍💻 **Minh**: CLI, testing, docs, review code của Thọ

### **Quy tắc:**
- 🔍 **Luôn review** trước khi merge
- 🔄 **Luôn sync** với develop trước khi merge
- 💬 **Communicate** trước khi merge lớn
- ⚠️ **Không force push** lên shared branches

---

*Tài liệu này định nghĩa rõ quyền hạn và trách nhiệm cho team collaboration*

