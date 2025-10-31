# LẤY CODE MỚI TỪ GITHUB - HƯỚNG DẪN NHANH

## 🚀 CÁCH NHANH NHẤT

### Nếu KHÔNG có thay đổi local (sạch):

```bash
cd D:\DO_AN_2\Mylogic
git pull origin main
```

### Nếu CÓ thay đổi local (chưa commit):

**Option 1: Lưu thay đổi tạm thời**
```bash
git stash
git pull origin main
git stash pop
```

**Option 2: Commit thay đổi trước**
```bash
git add .
git commit -m "Save local changes"
git pull origin main
```

### Nếu muốn XÓA thay đổi local và lấy y hệt GitHub:

⚠️ **CẢNH BÁO**: Lệnh này sẽ XÓA TẤT CẢ thay đổi chưa commit!

```bash
git fetch origin
git reset --hard origin/main
```

---

## ✅ KIỂM TRA TRƯỚC KHI PULL

```bash
# Xem có thay đổi gì không
git status

# Xem có gì mới trên GitHub không
git fetch origin
git log HEAD..origin/main --oneline
```

---

## 📋 WORKFLOW ĐỀ XUẤT

```bash
# Bước 1: Kiểm tra
git status

# Bước 2: Fetch (không thay đổi code)
git fetch origin

# Bước 3: Xem có gì mới
git log HEAD..origin/main --oneline

# Bước 4: Pull nếu có cập nhật
git pull origin main
```

