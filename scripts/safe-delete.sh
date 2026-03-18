#!/bin/bash
# Chronos Lab 软删除工具
# 用途：替代 rm，移动文件到 .trash/ 目录
# 用法：bash scripts/safe-delete.sh <文件或目录>

TRASH_DIR="/home/claworc/.openclaw/workspace/.trash"
TIMESTAMP=$(date +%Y%m%d-%H%M%S)

mkdir -p "$TRASH_DIR"

if [ -z "$1" ]; then
  echo "用法：bash scripts/safe-delete.sh <文件或目录>"
  echo "文件会被移动到 .trash/ 而不是永久删除"
  exit 1
fi

for target in "$@"; do
  if [ ! -e "$target" ]; then
    echo "❌ 不存在：$target"
    continue
  fi
  
  basename=$(basename "$target")
  dest="$TRASH_DIR/${TIMESTAMP}_${basename}"
  mv "$target" "$dest"
  echo "🗑️ 已移到回收站：$target → $dest"
done

# 清理 30 天前的回收站文件
find "$TRASH_DIR" -mtime +30 -exec rm -rf {} \; 2>/dev/null
echo "✅ 30 天前的回收站文件已自动清理"
