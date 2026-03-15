#!/bin/bash
# Chronos Lab 自动备份脚本
# 用途：每日凌晨备份到私密 GitHub 仓库
# 设置：crontab -e → 0 3 * * * /path/to/this/script.sh

set -e

# ==================== 配置区 ====================

# 本地工作目录
WORKSPACE_DIR="/home/claworc/.openclaw/workspace"

# 备份临时目录
BACKUP_DIR="/tmp/chronos-backup-$(date +%Y%m%d-%H%M%S)"

# GitHub 仓库信息（需要修改）
GITHUB_USER="sandmark78"
GITHUB_REPO="chronos-lab-backup"
GITHUB_BRANCH="main"

# Git 用户信息
GIT_USER_NAME="Chronos Backup Bot"
GIT_USER_EMAIL="backup@chronos-lab.local"

# ==================== 不要修改以下 ====================

echo "🔄 [$(date '+%Y-%m-%d %H:%M:%S')] 开始备份..."

# 创建备份目录
mkdir -p "$BACKUP_DIR"
cd "$BACKUP_DIR"

# 使用 HTTPS + Token 认证
GITHUB_TOKEN="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"
REPO_URL="https://${GITHUB_USER}:${GITHUB_TOKEN}@github.com/${GITHUB_USER}/${GITHUB_REPO}.git"

# 克隆仓库（如果存在）
if [ -d "$GITHUB_REPO" ]; then
    echo "📂 使用现有仓库..."
    cd "$GITHUB_REPO"
    git pull origin "$GITHUB_BRANCH" || true
else
    echo "📥 克隆仓库..."
    git clone --depth 1 "$REPO_URL" "$GITHUB_REPO"
    cd "$GITHUB_REPO"
fi

# 配置 Git
git config user.name "$GIT_USER_NAME"
git config user.email "$GIT_USER_EMAIL"

# 同步文件（排除敏感文件）
echo "📦 同步文件..."
mkdir -p ./workspace
cp -r "$WORKSPACE_DIR"/* ./workspace/ 2>/dev/null || true

# 删除敏感文件
cd ./workspace
rm -rf .git/ node_modules/ __pycache__/ *.pyc .DS_Store 2>/dev/null || true
rm -f openclaw.json *.log 2>/dev/null || true
rm -rf scrapling_env/ agents/ memory/ .openclaw/ 2>/dev/null || true
rm -f MEMORY.md 2>/dev/null || true
cd ..

# 检查变更
if [ -z "$(git status --porcelain)" ]; then
    echo "✅ 无变更，跳过提交"
    exit 0
fi

# 提交并推送
echo "💾 提交变更..."
git add -A
git commit -m "🔄 自动备份 $(date '+%Y-%m-%d %H:%M:%S')

自动备份 Chronos Lab 工作区
- 知识卡片
- 研究日志
- 理论框架
- 实验方案

备份时间：$(date -Iseconds)
"

echo "📤 推送到 GitHub..."
git push origin "$GITHUB_BRANCH"

# 清理
echo "🧹 清理临时文件..."
cd /
rm -rf "$BACKUP_DIR"

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 备份完成！"
