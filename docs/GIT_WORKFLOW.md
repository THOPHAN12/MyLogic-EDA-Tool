# 🌿 Git Workflow - Làm Việc Nhóm

## 👥 **THÀNH VIÊN**

- **Thọ**: Main developer
- **Minh**: Collaborator

---

## 🌳 **CẤU TRÚC BRANCHES**

### **Branch Strategy**

```
main (master)
├── develop (development branch)
│   ├── feature/tho-* (Thọ's features)
│   ├── feature/minh-* (Minh's features)
│   └── hotfix/* (urgent fixes)
└── release/* (release branches)
```

### **Branch Naming Convention**

- `develop` - Development branch (tích hợp code)
- `feature/tho-<feature-name>` - Thọ's feature branches
- `feature/minh-<feature-name>` - Minh's feature branches
- `hotfix/<issue>` - Urgent fixes
- `release/v<version>` - Release branches

---

## 🚀 **SETUP BRANCHES**

### **Bước 1: Tạo Development Branch**

```bash
# Từ main branch
git checkout -b develop
git push -u origin develop
```

### **Bước 2: Tạo Feature Branches cho Thọ**

```bash
# Thọ's branches
git checkout -b feature/tho-library-loader develop
git checkout -b feature/tho-technology-mapping develop
git checkout -b feature/tho-synthesis-algorithms develop
```

### **Bước 3: Tạo Feature Branches cho Minh**

```bash
# Minh's branches
git checkout -b feature/minh-cli-improvements develop
git checkout -b feature/minh-testing develop
git checkout -b feature/minh-documentation develop
```

---

## 📋 **WORKFLOW CHO TỪNG NGƯỜI**

### **Thọ's Workflow**

```bash
# 1. Làm việc trên feature branch
git checkout feature/tho-library-loader

# 2. Code và commit
git add .
git commit -m "feat: Add library loader for technology mapping"

# 3. Push lên remote
git push -u origin feature/tho-library-loader

# 4. Tạo Pull Request để merge vào develop
```

### **Minh's Workflow**

```bash
# 1. Làm việc trên feature branch
git checkout feature/minh-cli-improvements

# 2. Code và commit
git add .
git commit -m "feat: Improve CLI interface"

# 3. Push lên remote
git push -u origin feature/minh-cli-improvements

# 4. Tạo Pull Request để merge vào develop
```

---

## 🔀 **MERGE WORKFLOW**

### **Option 1: Merge qua Pull Request (Recommended)**

**Thọ merge code của Minh:**

```bash
# 1. Thọ review code của Minh trên GitHub
# 2. Approve Pull Request
# 3. Merge vào develop
```

**Minh merge code của Thọ:**

```bash
# 1. Minh review code của Thọ trên GitHub
# 2. Approve Pull Request
# 3. Merge vào develop
```

### **Option 2: Merge trực tiếp (Local)**

**Thọ merge code của Minh:**

```bash
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Merge Minh's branch
git merge feature/minh-cli-improvements

# 3. Resolve conflicts nếu có
# 4. Push
git push origin develop
```

**Minh merge code của Thọ:**

```bash
# 1. Update develop branch
git checkout develop
git pull origin develop

# 2. Merge Thọ's branch
git merge feature/tho-library-loader

# 3. Resolve conflicts nếu có
# 4. Push
git push origin develop
```

---

## ⚠️ **XỬ LÝ CONFLICTS**

### **Khi có conflict:**

```bash
# 1. Git sẽ báo conflict
# 2. Mở file conflict
# 3. Tìm các markers:
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

## 📝 **COMMIT MESSAGE CONVENTION**

### **Format:**

```
<type>(<scope>): <subject>

<body>

<footer>
```

### **Types:**

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style (formatting)
- `refactor`: Code refactoring
- `test`: Tests
- `chore`: Maintenance

### **Examples:**

```bash
# Thọ's commits
git commit -m "feat(library): Add Liberty format parser"
git commit -m "fix(mapping): Fix function conversion bug"

# Minh's commits
git commit -m "feat(cli): Add library file selection"
git commit -m "docs: Update technology mapping guide"
```

---

## 🔄 **SYNC WORKFLOW**

### **Hàng ngày:**

```bash
# 1. Update local develop
git checkout develop
git pull origin develop

# 2. Update feature branch
git checkout feature/your-branch
git merge develop  # Hoặc rebase

# 3. Continue working
```

### **Trước khi push:**

```bash
# 1. Update từ develop
git checkout develop
git pull origin develop

# 2. Merge vào feature branch
git checkout feature/your-branch
git merge develop

# 3. Resolve conflicts nếu có
# 4. Push
git push origin feature/your-branch
```

---

## 🎯 **BEST PRACTICES**

### **1. Luôn sync với develop trước khi merge**

```bash
git checkout develop
git pull origin develop
git checkout feature/your-branch
git merge develop
```

### **2. Commit thường xuyên**

```bash
# Commit nhỏ, thường xuyên
git commit -m "feat: Add function X"
git commit -m "fix: Fix bug Y"
```

### **3. Push thường xuyên**

```bash
# Push để backup và share
git push origin feature/your-branch
```

### **4. Review code trước khi merge**

- Check code quality
- Test functionality
- Review logic

---

## 📊 **BRANCH STATUS**

### **Check branches:**

```bash
# List all branches
git branch -a

# Check current branch
git branch

# Check remote branches
git branch -r
```

### **Check differences:**

```bash
# Compare với develop
git diff develop..feature/your-branch

# Compare với remote
git diff origin/develop..origin/feature/your-branch
```

---

## 🚨 **TROUBLESHOOTING**

### **1. Accidentally commit to wrong branch**

```bash
# Move last commit to correct branch
git log --oneline -1  # Get commit hash
git reset HEAD~1  # Undo commit (keep changes)
git checkout correct-branch
git commit -m "feat: ..."
```

### **2. Want to undo last commit**

```bash
# Keep changes
git reset --soft HEAD~1

# Discard changes
git reset --hard HEAD~1
```

### **3. Merge wrong branch**

```bash
# Undo merge (if not pushed)
git reset --hard HEAD~1

# Undo merge (if pushed)
git revert -m 1 HEAD
```

---

## 📚 **QUICK REFERENCE**

### **Thọ's Commands:**

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/tho-<name>

# Work and commit
git add .
git commit -m "feat: ..."
git push origin feature/tho-<name>

# Merge Minh's code
git checkout develop
git pull origin develop
git merge feature/minh-<name>
git push origin develop
```

### **Minh's Commands:**

```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/minh-<name>

# Work and commit
git add .
git commit -m "feat: ..."
git push origin feature/minh-<name>

# Merge Thọ's code
git checkout develop
git pull origin develop
git merge feature/tho-<name>
git push origin develop
```

---

*Tài liệu này hướng dẫn workflow cho làm việc nhóm với Git*

