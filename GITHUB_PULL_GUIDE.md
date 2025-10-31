# HƯỚNG DẪN LẤY CODE MỚI TỪ GITHUB

## 🔄 CÁC CÁCH LẤY CODE MỚI

### 1. **Pull (Lấy và Merge) - Khuyến nghị**

Nếu bạn đã có code local và muốn cập nhật từ GitHub:

```bash
# Xem thay đổi trên remote trước
git fetch origin

# Xem khác biệt giữa local và remote
git log HEAD..origin/main

# Pull code mới (tự động merge nếu không conflict)
git pull origin main

# Hoặc ngắn gọn hơn (nếu đã set upstream)
git pull
```

### 2. **Pull với Rebase (Giữ lịch sử sạch)**

Nếu muốn giữ lịch sử commit thẳng:

```bash
git pull --rebase origin main
```

### 3. **Reset về trạng thái GitHub (XÓA thay đổi local)**

⚠️ **CẢNH BÁO**: Lệnh này sẽ **XÓA TẤT CẢ** thay đổi local chưa commit!

```bash
# Xem thay đổi trước
git status

# Hard reset về trạng thái GitHub (XÓA thay đổi local)
git fetch origin
git reset --hard origin/main

# Hoặc force reset
git reset --hard origin/main
```

### 4. **Stash thay đổi local rồi Pull**

Nếu có thay đổi local nhưng muốn giữ lại:

```bash
# Lưu thay đổi local tạm thời
git stash

# Pull code mới
git pull origin main

# Lấy lại thay đổi local
git stash pop

# Nếu có conflict, giải quyết conflict rồi:
git add .
git commit -m "Merge stashed changes"
```

### 5. **Clone lại hoàn toàn (Nếu repository mới)**

Nếu chưa có code local:

```bash
cd D:\DO_AN_2
git clone <repository_url> Mylogic_new
# Ví dụ: git clone https://github.com/username/Mylogic.git Mylogic_new
```

---

## 📋 CÁC TÌNH HUỐNG THƯỜNG GẶP

### **Tình huống 1: Chưa commit thay đổi local**

```bash
# Xem thay đổi
git status

# Option A: Commit trước rồi pull
git add .
git commit -m "Save local changes"
git pull origin main

# Option B: Stash rồi pull
git stash
git pull origin main
git stash pop
```

### **Tình huống 2: Có conflict khi pull**

```bash
# Pull và có conflict
git pull origin main

# Xem files conflict
git status

# Giải quyết conflict trong files
# (mở file, tìm <<<<<<, ======, >>>>>> và sửa)

# Sau khi giải quyết xong
git add .
git commit -m "Resolve merge conflicts"
```

### **Tình huống 3: Muốn xem thay đổi trước khi pull**

```bash
# Fetch mà không merge
git fetch origin

# Xem khác biệt
git diff main origin/main

# Xem log commits mới
git log main..origin/main

# Nếu OK thì pull
git pull origin main
```

### **Tình huống 4: Đã commit local, muốn đồng bộ với GitHub**

```bash
# Push code local lên GitHub trước
git push origin main

# Nếu có conflict, GitHub sẽ từ chối → cần pull trước
git pull origin main
# Giải quyết conflict
git push origin main
```

---

## 🔧 CÁC LỆNH HỮU ÍCH

```bash
# Xem branch hiện tại
git branch

# Xem remote branches
git branch -r

# Xem tất cả branches
git branch -a

# Xem thay đổi giữa local và remote
git diff main origin/main

# Xem commits trên remote chưa có ở local
git log main..origin/main --oneline

# Xem commits ở local chưa push lên remote
git log origin/main..main --oneline
```

---

## ✅ CHECKLIST TRƯỚC KHI PULL

1. ✅ Kiểm tra thay đổi local: `git status`
2. ✅ Xem khác biệt với remote: `git fetch origin && git log HEAD..origin/main`
3. ✅ Commit hoặc stash thay đổi quan trọng
4. ✅ Backup code quan trọng (nếu cần)
5. ✅ Pull code mới

---

## 🚨 LƯU Ý QUAN TRỌNG

- **`git pull`**: Merge code mới với code local (an toàn)
- **`git reset --hard`**: XÓA code local, về y hệt GitHub (NGUY HIỂM)
- **`git fetch`**: Chỉ tải về thông tin, KHÔNG thay đổi code
- Luôn kiểm tra `git status` trước khi pull

---

## 📝 VÍ DỤ CỤ THỂ

```bash
# Ví dụ workflow an toàn:
cd D:\DO_AN_2\Mylogic

# 1. Xem trạng thái
git status

# 2. Nếu có thay đổi chưa commit, stash
git stash save "Backup before pull"

# 3. Fetch xem có gì mới không
git fetch origin

# 4. Xem commits mới
git log HEAD..origin/main --oneline

# 5. Pull code mới
git pull origin main

# 6. Lấy lại thay đổi local (nếu đã stash)
git stash pop
```

---

**Ngày tạo**: 2025-10-31  
**Phiên bản**: 1.0

