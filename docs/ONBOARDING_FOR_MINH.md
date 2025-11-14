# 👋 Chào Mừng Minh Đến Với MyLogic EDA Tool!

## 🎯 **MỤC ĐÍCH**

Tài liệu này hướng dẫn **Minh** setup và bắt đầu làm việc với dự án MyLogic EDA Tool.

---

## ✅ **CHECKLIST SETUP**

### **Bước 1: Accept Invitation**

- [ ] Kiểm tra email từ GitHub
- [ ] Click link "View invitation"
- [ ] Click "Accept invitation"
- [ ] Xác nhận đã thấy repository trong GitHub

### **Bước 2: Clone Repository**

```bash
# Clone repository
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool
```

### **Bước 3: Setup Git Config**

```bash
# Kiểm tra config
git config --global user.name
git config --global user.email

# Nếu chưa có, setup:
git config --global user.name "Minh"
git config --global user.email "your-email@example.com"  # Email GitHub của bạn
```

### **Bước 4: Fetch và Checkout Develop**

```bash
# Fetch tất cả branches
git fetch origin

# Checkout develop
git checkout develop
git pull origin develop
```

### **Bước 5: Test Push**

```bash
# Tạo test branch
git checkout -b feature/minh-test-setup develop

# Tạo test file
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "test: Verify push access"
git push -u origin feature/minh-test-setup

# Xóa test file
git rm TEST.md
git commit -m "chore: Remove test file"
git push origin feature/minh-test-setup
```

---

## 📚 **TÀI LIỆU CẦN ĐỌC**

### **Bắt buộc đọc:**

1. **`docs/QUICK_START_GIT.md`** ⭐
   - Quick start guide cho Git workflow
   - Các lệnh cơ bản
   - Workflow hàng ngày

2. **`docs/TEAM_ROLES_AND_PERMISSIONS.md`** ⭐
   - Quyền hạn và trách nhiệm
   - Quy tắc merge
   - Code review checklist

3. **`README.md`**
   - Tổng quan về dự án
   - Cách chạy tool
   - Các tính năng

### **Nên đọc:**

4. **`docs/GIT_WORKFLOW.md`**
   - Chi tiết Git workflow
   - Merge strategies
   - Conflict resolution

5. **`docs/ADDING_COLLABORATOR.md`**
   - Cách thêm collaborator (nếu cần thêm người khác)

---

## 🎯 **BRANCHES CỦA MINH**

Bạn có các branches sẵn có:

- `feature/minh-cli-improvements` - Cải thiện CLI
- `feature/minh-testing` - Testing framework
- `feature/minh-documentation` - Documentation

### **Checkout branch:**

```bash
# List branches
git branch -a

# Checkout branch của bạn
git checkout feature/minh-cli-improvements
git pull origin feature/minh-cli-improvements
```

### **Tạo branch mới:**

```bash
# Sử dụng helper script (Windows)
.\scripts\git_helper.ps1 new-feature minh-<tên-feature>

# Hoặc manual
git checkout develop
git pull origin develop
git checkout -b feature/minh-<tên-feature>
```

---

## 🚀 **WORKFLOW HÀNG NGÀY**

### **1. Bắt đầu ngày làm việc:**

```bash
# Sync với develop
.\scripts\git_helper.ps1 sync

# Hoặc manual
git checkout develop
git pull origin develop
git checkout feature/minh-your-branch
git merge develop
```

### **2. Code và commit:**

```bash
# Làm việc trên feature branch
git checkout feature/minh-your-branch

# Code...
# Test...

# Commit
git add .
git commit -m "feat: Add feature X"
```

### **3. Push lên remote:**

```bash
# Sử dụng helper
.\scripts\git_helper.ps1 push-feature

# Hoặc manual
git push origin feature/minh-your-branch
```

### **4. Khi xong feature:**

```bash
# 1. Đảm bảo code đã được test
# 2. Đảm bảo đã sync với develop
.\scripts\git_helper.ps1 sync

# 3. Tạo Pull Request trên GitHub
#    - Vào: https://github.com/THOPHAN12/MyLogic-EDA-Tool
#    - Click "New Pull Request"
#    - Chọn: feature/minh-your-branch → develop
#    - Mô tả thay đổi
#    - Request review từ Thọ

# 4. Chờ Thọ review và merge
```

---

## 📝 **COMMIT MESSAGE FORMAT**

Sử dụng format chuẩn:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### **Types:**

- `feat`: Tính năng mới
- `fix`: Sửa lỗi
- `docs`: Tài liệu
- `style`: Format code
- `refactor`: Refactor code
- `test`: Tests
- `chore`: Maintenance

### **Examples:**

```bash
git commit -m "feat(cli): Add library file selection"
git commit -m "fix(test): Fix import errors in test suite"
git commit -m "docs: Update technology mapping guide"
git commit -m "test: Add unit tests for library loader"
```

---

## 🔍 **CODE REVIEW PROCESS**

### **Khi tạo Pull Request:**

1. **Mô tả rõ ràng:**
   - Feature làm gì?
   - Tại sao cần feature này?
   - Có test cases không?

2. **Request review:**
   - Tag @Thọ để review
   - Đảm bảo code đã được test

3. **Chờ feedback:**
   - Thọ sẽ review code
   - Có thể request changes
   - Sửa theo feedback

4. **Merge:**
   - Sau khi được approve
   - Thọ hoặc bạn có thể merge

---

## ⚠️ **QUY TẮC QUAN TRỌNG**

### **1. LUÔN sync với develop trước khi merge**

```bash
.\scripts\git_helper.ps1 sync
```

### **2. KHÔNG force push lên shared branches**

❌ **Sai:**
```bash
git push --force origin develop  # NGUY HIỂM!
```

✅ **Đúng:**
```bash
git push origin feature/minh-your-branch  # Safe
```

### **3. COMMUNICATE trước khi merge lớn**

- Thông báo Thọ trước khi merge feature lớn
- Đảm bảo không conflict

### **4. TEST trước khi push**

- Chạy tests
- Kiểm tra không break existing features

---

## 🛠️ **HELPER SCRIPTS**

Sử dụng helper scripts để dễ làm việc:

```powershell
# Setup branches
.\scripts\git_helper.ps1 setup

# Tạo feature mới
.\scripts\git_helper.ps1 new-feature minh-<tên-feature>

# Sync với develop
.\scripts\git_helper.ps1 sync

# Check status
.\scripts\git_helper.ps1 status

# Push feature branch
.\scripts\git_helper.ps1 push-feature

# List branches
.\scripts\git_helper.ps1 list-branches
```

---

## 🎓 **HỌC HỎI**

### **Nếu không biết làm gì:**

1. **Đọc tài liệu:**
   - `docs/QUICK_START_GIT.md`
   - `docs/TEAM_ROLES_AND_PERMISSIONS.md`

2. **Xem code hiện có:**
   - Xem cách Thọ code
   - Học từ examples

3. **Hỏi Thọ:**
   - Tạo issue trên GitHub
   - Hoặc liên hệ trực tiếp

---

## 📊 **TRÁCH NHIỆM CỦA MINH**

### **Bạn chủ yếu đảm nhiệm:**

1. **CLI Improvements:**
   - Cải thiện user experience
   - Thêm commands mới
   - Fix bugs trong CLI

2. **Testing:**
   - Viết unit tests
   - Viết integration tests
   - Đảm bảo code coverage

3. **Documentation:**
   - Update docs
   - Viết guides
   - Cải thiện README

4. **Code Review:**
   - Review code của Thọ
   - Approve/Reject Pull Requests
   - Đưa ra feedback

---

## 🚨 **TROUBLESHOOTING**

### **Lỗi thường gặp:**

1. **Permission denied:**
   - Kiểm tra đã accept invitation chưa
   - Kiểm tra remote URL

2. **Branch not found:**
   - Fetch branches: `git fetch origin`
   - Checkout branch: `git checkout -b feature/xxx origin/feature/xxx`

3. **Merge conflicts:**
   - Sync với develop trước
   - Resolve conflicts
   - Test lại

4. **Import errors:**
   - Kiểm tra Python path
   - Install dependencies: `pip install -r requirements.txt`

---

## 📞 **LIÊN HỆ**

- **GitHub Issues**: https://github.com/THOPHAN12/MyLogic-EDA-Tool/issues
- **Repository**: https://github.com/THOPHAN12/MyLogic-EDA-Tool

---

## 🎉 **CHÚC MỪNG!**

Bạn đã sẵn sàng bắt đầu làm việc với dự án MyLogic EDA Tool!

**Next Steps:**
1. ✅ Đọc `docs/QUICK_START_GIT.md`
2. ✅ Đọc `docs/TEAM_ROLES_AND_PERMISSIONS.md`
3. ✅ Checkout branch của bạn
4. ✅ Bắt đầu code!

---

*Chúc bạn làm việc vui vẻ! 🚀*

