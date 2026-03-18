#!/bin/bash
# Chronos Lab 每日凌晨备份脚本
# 用途：每日 3:00 自动打包 memory 目录 + 关键文件
# 保留最近 7 天备份

WORKSPACE="/home/claworc/.openclaw/workspace"
BACKUP_DIR="/home/claworc/.openclaw/backups/daily"
TIMESTAMP=$(date +%Y-%m-%d)

mkdir -p "$BACKUP_DIR"

echo "🔒 [$(date '+%Y-%m-%d %H:%M:%S')] 每日备份开始"

# 打包 memory + problem-database + MEMORY.md
tar -czf "$BACKUP_DIR/memory-$TIMESTAMP.tar.gz" \
  -C "$WORKSPACE" \
  memory/ \
  problem-database/ \
  MEMORY.md \
  TOOLS.md \
  IDENTITY.md \
  SOUL.md \
  USER.md \
  2>/dev/null

echo "✅ 备份完成：$BACKUP_DIR/memory-$TIMESTAMP.tar.gz"
echo "   大小：$(du -h "$BACKUP_DIR/memory-$TIMESTAMP.tar.gz" | cut -f1)"

# 保留最近 7 天，清理旧备份
cd "$BACKUP_DIR"
ls -t memory-*.tar.gz 2>/dev/null | tail -n +8 | xargs -r rm --
echo "✅ 保留最近 7 天备份，旧备份已清理"

# Git 提交
cd "$WORKSPACE"
git add -A 2>/dev/null
if ! git diff --staged --quiet 2>/dev/null; then
  git commit -m "🔒 每日自动备份 $TIMESTAMP" 2>/dev/null
  git push origin master 2>/dev/null
  git push backup master --force 2>/dev/null
  echo "✅ Git 已提交并推送"
else
  echo "✅ 无变更，跳过 Git 提交"
fi

echo "🔒 [$(date '+%Y-%m-%d %H:%M:%S')] 每日备份完成"
