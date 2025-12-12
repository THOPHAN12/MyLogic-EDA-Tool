#!/bin/bash
###############################################################################
# Script làm sạch và tổ chức lại files ở root level
###############################################################################

set -e

PROJECT_ROOT="/home/thophan/DO_AN_1/MyLogic-EDA-Tool"
cd "$PROJECT_ROOT"

echo "════════════════════════════════════════════════════════════"
echo "  🧹 LÀM SẠCH VÀ TỔ CHỨC LẠI ROOT LEVEL"
echo "════════════════════════════════════════════════════════════"
echo ""

# Files cần giữ ở root (core files)
CORE_FILES=(
    "mylogic.py"
    "constants.py"
    "setup.py"
    "requirements.txt"
    "README.md"
    "README_COMPLETE.md"
    "LICENSE"
    ".gitignore"
)

# Kiểm tra và di chuyển các files không cần thiết ở root
echo "[1/4] Kiểm tra files ở root level..."
ROOT_FILES=$(find . -maxdepth 1 -type f ! -name ".git*" -exec basename {} \;)

echo "Files hiện tại ở root:"
for file in $ROOT_FILES; do
    if [[ " ${CORE_FILES[@]} " =~ " ${file} " ]]; then
        echo "  ✅ $file (core file - giữ lại)"
    else
        echo "  ⚠️  $file (có thể di chuyển)"
    fi
done
echo ""

# Tạo thư mục scripts nếu chưa có
echo "[2/4] Tổ chức script files..."
if [ -d "scripts" ]; then
    echo "  ✅ Thư mục scripts đã có"
else
    mkdir -p scripts
    echo "  ✅ Đã tạo thư mục scripts"
fi
echo ""

# Di chuyển các script files nếu có ở root
echo "[3/4] Di chuyển script files..."
for file in *.sh; do
    if [ -f "$file" ] && [ "$file" != "cleanup_root.sh" ]; then
        mv "$file" scripts/ 2>/dev/null && echo "  ✅ Moved $file → scripts/" || true
    fi
done
echo ""

# Tạo .gitkeep cho thư mục trống
echo "[4/4] Tạo .gitkeep cho thư mục trống..."
for dir in tests/integration tests/fixtures data/outputs data/temp; do
    if [ -d "$dir" ] && [ -z "$(ls -A $dir 2>/dev/null)" ]; then
        touch "$dir/.gitkeep"
        echo "  ✅ Created $dir/.gitkeep"
    fi
done
echo ""

echo "════════════════════════════════════════════════════════════"
echo "  ✅ HOÀN TẤT"
echo "════════════════════════════════════════════════════════════"
echo ""
echo "📁 Cấu trúc root level (chỉ core files):"
for file in "${CORE_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    fi
done
echo ""
echo "📁 Scripts: scripts/"
echo "📁 Tests: tests/"
echo "📁 Reports: reports/"
echo "📁 Logs: logs/"
echo "📁 Config: config/"
echo ""

