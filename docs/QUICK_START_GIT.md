# 🚀 Quick Start - Git Workflow cho Team

## 👥 **THÀNH VIÊN**

- **Thọ**: Main developer
- **Minh**: Collaborator

> **Lưu ý về Quyền Hạn**: Cả Thọ và Minh đều có quyền như nhau trên repository. Mỗi người chủ yếu đảm nhiệm branches của mình, nhưng có thể review và merge code của nhau. Xem chi tiết tại `docs/TEAM_ROLES_AND_PERMISSIONS.md`.

---

## ⚡ **SETUP NHANH**

### **1. Clone và Setup (Lần đầu)**

```bash
# Clone repository
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool

# Setup branches
git checkout develop
git pull origin develop
```

### **2. Tạo Feature Branch Mới**

**Thọ:**
```bash
# Sử dụng helper script (Linux/Mac)
./scripts/git_helper.sh new-feature tho-<feature-name>

# Hoặc PowerShell (Windows)
.\scripts\git_helper.ps1 new-feature tho-<feature-name>

# Hoặc manual
git checkout develop
git pull origin develop
git checkout -b feature/tho-<feature-name>
```

**Minh:**
```bash
# Sử dụng helper script
./scripts/git_helper.sh new-feature minh-<feature-name>

# Hoặc manual
git checkout develop
git pull origin develop
git checkout -b feature/minh-<feature-name>
```

---

## 📝 **WORKFLOW HÀNG NGÀY**

### **Bước 1: Sync với Develop**

```bash
# Sử dụng helper
./scripts/git_helper.sh sync

# Hoặc manual
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
```

### **Bước 2: Code và Commit**

```bash
# Làm việc trên feature branch
git checkout feature/your-branch

# Code...
# Test...

# Commit
git add .
git commit -m "feat: Add new feature X"
```

### **Bước 3: Push lên Remote**

```bash
# Sử dụng helper
./scripts/git_helper.sh push-feature

# Hoặc manual
git push origin feature/your-branch
```

---

## 🔀 **MERGE CODE**

### **Option 1: Merge qua Pull Request (Khuyên dùng)**

1. **Tạo Pull Request trên GitHub:**
   - Vào: https://github.com/THOPHAN12/MyLogic-EDA-Tool
   - Click "New Pull Request"
   - Chọn: `feature/your-branch` → `develop`
   - Review code
   - Click "Merge"

2. **Sau khi merge:**
   ```bash
   git checkout develop
   git pull origin develop
   ```

### **Option 2: Merge Local**

**Thọ merge code của Minh:**
```bash
git checkout develop
git pull origin develop
git merge feature/minh-<feature-name>
git push origin develop
```

**Minh merge code của Thọ:**
```bash
git checkout develop
git pull origin develop
git merge feature/tho-<feature-name>
git push origin develop
```

---

## 🛠️ **HELPER SCRIPTS**

### **Linux/Mac (Bash)**

```bash
# Setup branches
./scripts/git_helper.sh setup

# Tạo feature mới
./scripts/git_helper.sh new-feature tho-library-loader

# Sync với develop
./scripts/git_helper.sh sync

# Check status
./scripts/git_helper.sh status

# Push feature branch
./scripts/git_helper.sh push-feature

# Merge feature vào develop
./scripts/git_helper.sh merge-feature feature/tho-library-loader

# List branches
./scripts/git_helper.sh list-branches
```

### **Windows (PowerShell)**

```powershell
# Setup branches
.\scripts\git_helper.ps1 setup

# Tạo feature mới
.\scripts\git_helper.ps1 new-feature tho-library-loader

# Sync với develop
.\scripts\git_helper.ps1 sync

# Check status
.\scripts\git_helper.ps1 status

# Push feature branch
.\scripts\git_helper.ps1 push-feature

# Merge feature vào develop
.\scripts\git_helper.ps1 merge-feature feature/tho-library-loader

# List branches
.\scripts\git_helper.ps1 list-branches
```

---

## 📋 **COMMIT MESSAGE FORMAT**

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
git commit -m "feat(library): Add Liberty format parser"
git commit -m "fix(mapping): Fix function conversion bug"
git commit -m "docs: Update technology mapping guide"
git commit -m "test: Add unit tests for library loader"
```

---

## 🌳 **BRANCH STRUCTURE**

```
main (production)
  └── develop (development)
      ├── feature/tho-library-loader
      ├── feature/tho-technology-mapping
      ├── feature/tho-synthesis-algorithms
      ├── feature/minh-cli-improvements
      ├── feature/minh-testing
      └── feature/minh-documentation
```

---

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **1. Luôn sync trước khi merge**
```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
```

### **2. Commit thường xuyên**
- Commit nhỏ, thường xuyên
- Mỗi commit là một thay đổi logic

### **3. Push thường xuyên**
- Backup code
- Share với team

### **4. Review code trước khi merge**
- Check logic
- Test functionality
- Review code quality

---

## 🚨 **XỬ LÝ CONFLICTS**

### **Khi có conflict:**

```bash
# 1. Git sẽ báo conflict
# 2. Mở file conflict
# 3. Tìm markers:
#    <<<<<<< HEAD (code của bạn)
#    =======
#    >>>>>>> feature/other (code của người khác)

# 4. Sửa conflict, giữ code đúng
# 5. Xóa markers
# 6. Add và commit
git add .
git commit -m "fix: Resolve merge conflicts"
```

---

## 📚 **TÀI LIỆU THAM KHẢO**

- Chi tiết: Xem `docs/GIT_WORKFLOW.md`
- GitHub: https://github.com/THOPHAN12/MyLogic-EDA-Tool

---

*Happy Coding! 🎉*

