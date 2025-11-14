# 👥 Hướng Dẫn Thêm Collaborator vào Dự Án

## 📋 **TÓM TẮT**

Hướng dẫn chi tiết để thêm **Minh** (hoặc bất kỳ collaborator nào) vào dự án MyLogic EDA Tool trên GitHub.

---

## 🔐 **BƯỚC 1: THÊM COLLABORATOR TRÊN GITHUB**

### **Thọ thực hiện (Repository Owner):**

1. **Vào GitHub Repository:**
   - Truy cập: https://github.com/THOPHAN12/MyLogic-EDA-Tool
   - Đăng nhập vào tài khoản GitHub của Thọ

2. **Vào Settings:**
   - Click tab **"Settings"** ở trên cùng repository
   - Hoặc truy cập trực tiếp: https://github.com/THOPHAN12/MyLogic-EDA-Tool/settings

3. **Vào Collaborators:**
   - Trong menu bên trái, click **"Collaborators"** (hoặc **"Access"** → **"Collaborators"**)
   - Hoặc truy cập: https://github.com/THOPHAN12/MyLogic-EDA-Tool/settings/access

4. **Thêm Collaborator:**
   - Click nút **"Add people"** hoặc **"Invite a collaborator"**
   - Nhập **username GitHub của Minh** hoặc **email của Minh**
   - Chọn quyền: **Write** (để có thể push, merge)
   - Click **"Add [username] to this repository"**

5. **Gửi lời mời:**
   - GitHub sẽ gửi email mời đến Minh
   - Minh cần accept invitation qua email

### **Quyền hạn (Permissions):**

- **Read**: Chỉ đọc (không đủ)
- **Write**: Đọc và ghi (khuyên dùng) ✅
- **Admin**: Full quyền (không cần thiết)

**Khuyên dùng: Chọn "Write"** để Minh có thể:
- ✅ Push code
- ✅ Tạo branches
- ✅ Merge branches
- ✅ Tạo Pull Requests
- ❌ Không thể xóa repository

---

## 📧 **BƯỚC 2: MINH ACCEPT INVITATION**

### **Minh thực hiện:**

1. **Kiểm tra email:**
   - Mở email từ GitHub (noreply@github.com)
   - Subject: "THOPHAN12 invited you to collaborate on THOPHAN12/MyLogic-EDA-Tool"

2. **Accept invitation:**
   - Click link **"View invitation"** trong email
   - Hoặc vào: https://github.com/THOPHAN12/MyLogic-EDA-Tool/invitations
   - Click nút **"Accept invitation"**

3. **Xác nhận:**
   - Minh sẽ thấy repository trong danh sách repositories
   - Có thể clone và push code

---

## 💻 **BƯỚC 3: MINH SETUP LOCAL REPOSITORY**

### **Minh thực hiện trên máy của mình:**

### **3.1. Clone Repository:**

```bash
# Clone repository
git clone https://github.com/THOPHAN12/MyLogic-EDA-Tool.git
cd MyLogic-EDA-Tool
```

### **3.2. Setup Git Config (Nếu chưa có):**

```bash
# Kiểm tra config hiện tại
git config --global user.name
git config --global user.email

# Nếu chưa có, setup:
git config --global user.name "Minh"
git config --global user.email "minh@example.com"  # Email GitHub của Minh
```

### **3.3. Fetch tất cả branches:**

```bash
# Fetch tất cả branches từ remote
git fetch origin

# Xem tất cả branches
git branch -a
```

### **3.4. Checkout develop branch:**

```bash
# Checkout develop branch
git checkout develop

# Pull latest code
git pull origin develop
```

### **3.5. Tạo feature branch cho Minh:**

```bash
# Tạo branch mới cho Minh
git checkout -b feature/minh-setup develop

# Hoặc checkout branch có sẵn
git checkout feature/minh-cli-improvements
git pull origin feature/minh-cli-improvements
```

---

## 🔧 **BƯỚC 4: VERIFY SETUP**

### **Minh kiểm tra:**

```bash
# 1. Kiểm tra remote URL
git remote -v
# Output nên có:
# origin  https://github.com/THOPHAN12/MyLogic-EDA-Tool.git (fetch)
# origin  https://github.com/THOPHAN12/MyLogic-EDA-Tool.git (push)

# 2. Kiểm tra branches
git branch -a
# Nên thấy:
# * develop
#   feature/minh-cli-improvements
#   feature/minh-testing
#   feature/minh-documentation
#   remotes/origin/develop
#   remotes/origin/feature/minh-cli-improvements
#   ...

# 3. Test push (tạo test commit)
echo "# Test" >> TEST.md
git add TEST.md
git commit -m "test: Verify push access"
git push origin feature/minh-setup

# 4. Xóa test file
git rm TEST.md
git commit -m "chore: Remove test file"
git push origin feature/minh-setup
```

---

## 📝 **BƯỚC 5: SETUP SSH (TÙY CHỌN - Khuyên dùng)**

### **Minh setup SSH key (để không cần nhập password mỗi lần):**

### **5.1. Tạo SSH Key:**

```bash
# Tạo SSH key mới
ssh-keygen -t ed25519 -C "minh@example.com"

# Nhấn Enter để chấp nhận default location
# Nhập passphrase (hoặc Enter để bỏ qua)
```

### **5.2. Thêm SSH Key vào GitHub:**

```bash
# Copy public key
cat ~/.ssh/id_ed25519.pub
# Hoặc Windows:
type %USERPROFILE%\.ssh\id_ed25519.pub
```

1. Vào GitHub: https://github.com/settings/keys
2. Click **"New SSH key"**
3. **Title**: "MyLogic Development"
4. **Key**: Paste nội dung public key
5. Click **"Add SSH key"**

### **5.3. Đổi remote URL sang SSH:**

```bash
# Kiểm tra remote hiện tại
git remote -v

# Đổi sang SSH
git remote set-url origin git@github.com:THOPHAN12/MyLogic-EDA-Tool.git

# Verify
git remote -v
```

---

## 🚀 **BƯỚC 6: MINH BẮT ĐẦU LÀM VIỆC**

### **Workflow đầu tiên của Minh:**

```bash
# 1. Sync với develop
git checkout develop
git pull origin develop

# 2. Tạo feature branch mới
git checkout -b feature/minh-first-feature develop

# 3. Code và commit
# ... làm việc ...
git add .
git commit -m "feat: Add first feature"

# 4. Push lên remote
git push -u origin feature/minh-first-feature

# 5. Tạo Pull Request trên GitHub
# Vào: https://github.com/THOPHAN12/MyLogic-EDA-Tool
# Click "New Pull Request"
# Chọn: feature/minh-first-feature → develop
```

---

## ✅ **CHECKLIST CHO MINH**

Sau khi setup, Minh nên kiểm tra:

- [ ] ✅ Đã accept invitation trên GitHub
- [ ] ✅ Đã clone repository thành công
- [ ] ✅ Đã checkout develop branch
- [ ] ✅ Đã pull latest code từ develop
- [ ] ✅ Đã test push thành công
- [ ] ✅ Đã đọc `docs/QUICK_START_GIT.md`
- [ ] ✅ Đã đọc `docs/TEAM_ROLES_AND_PERMISSIONS.md`
- [ ] ✅ Đã hiểu workflow và quy tắc merge

---

## 🛠️ **TROUBLESHOOTING**

### **Lỗi 1: Permission denied (publickey)**

**Nguyên nhân:** Chưa setup SSH key hoặc remote URL chưa đúng

**Giải pháp:**
```bash
# Kiểm tra SSH connection
ssh -T git@github.com

# Nếu lỗi, setup SSH key (xem Bước 5)
# Hoặc dùng HTTPS với Personal Access Token
```

### **Lỗi 2: Remote: Permission denied**

**Nguyên nhân:** Chưa accept invitation hoặc không có quyền Write

**Giải pháp:**
1. Kiểm tra email invitation
2. Accept invitation trên GitHub
3. Kiểm tra quyền trong Settings → Collaborators

### **Lỗi 3: Branch not found**

**Nguyên nhân:** Chưa fetch branches từ remote

**Giải pháp:**
```bash
# Fetch tất cả branches
git fetch origin

# Checkout branch
git checkout -b feature/minh-xxx origin/feature/minh-xxx
```

### **Lỗi 4: Cannot push to protected branch**

**Nguyên nhân:** Đang cố push trực tiếp lên `main` hoặc `develop` (nếu được protect)

**Giải pháp:**
- Chỉ push lên feature branches
- Merge vào develop qua Pull Request

---

## 📚 **TÀI LIỆU THAM KHẢO CHO MINH**

Sau khi được thêm vào dự án, Minh nên đọc:

1. **`docs/QUICK_START_GIT.md`** - Quick start guide
2. **`docs/GIT_WORKFLOW.md`** - Chi tiết Git workflow
3. **`docs/TEAM_ROLES_AND_PERMISSIONS.md`** - Quyền hạn và trách nhiệm
4. **`README.md`** - Tổng quan về dự án

---

## 🎯 **TÓM TẮT QUY TRÌNH**

### **Thọ (Repository Owner):**

1. ✅ Vào GitHub → Settings → Collaborators
2. ✅ Add people → Nhập username/email của Minh
3. ✅ Chọn quyền "Write"
4. ✅ Gửi invitation

### **Minh (Collaborator):**

1. ✅ Accept invitation qua email
2. ✅ Clone repository
3. ✅ Setup Git config
4. ✅ Fetch và checkout develop
5. ✅ Test push
6. ✅ Bắt đầu làm việc!

---

## 💡 **LƯU Ý QUAN TRỌNG**

1. **Minh cần có tài khoản GitHub** trước khi được thêm
2. **Minh cần accept invitation** trước khi có thể push
3. **Nên dùng SSH** để tránh nhập password mỗi lần
4. **Luôn sync với develop** trước khi bắt đầu feature mới
5. **Đọc tài liệu** trước khi bắt đầu code

---

*Tài liệu này hướng dẫn chi tiết cách thêm collaborator vào dự án*

