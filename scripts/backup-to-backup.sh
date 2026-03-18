#!/bin/bash
# Chronos Lab 备份仓库备份脚本 (完整备份)
# 用途：推送所有文件到 chronos-lab-backup (backup)
# 包括敏感文件和研究数据

set -e

WORKSPACE="/home/claworc/.openclaw/workspace"

echo "========================================"
echo "💾 备份到备份仓库 (backup) - 完整备份"
echo "========================================"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

cd "$WORKSPACE"

# 检查当前分支状态
echo "=== Git 状态检查 ==="
UNCOMMITTED=$(git status --porcelain | wc -l)
echo "未提交文件数：$UNCOMMITTED"

# 添加所有变更（包括通常被忽略的文件）
echo ""
echo "=== 添加所有文件 (包括敏感文件) ==="
git add -A --force 2>/dev/null || git add -A

# 检查是否有变更
if git diff --staged --quiet; then
    echo "✅ 无变更，跳过提交"
else
    echo "💾 提交完整备份..."
    git commit -m "💾 完整备份 $(date '+%Y-%m-%d %H:%M:%S')

- 完整工作区
- 研究成果
- 知识卡片
- 研究日志
- 记忆文件
- 问题数据库
- 原创假设
- 思想实验

备份时间：$(date -Iseconds)
"
fi

# 推送到 backup/master
echo ""
echo "=== 推送到 backup/master ==="
git push backup master

echo ""
echo "========================================"
echo "✅ 备份仓库 (完整) 备份完成"
echo "========================================"
echo ""
echo "📦 已备份内容:"
echo "  ✅ 所有研究循环 (DC-1~DC-274+)"
echo "  ✅ knowledge_cards/ - 知识卡片汇总"
echo "  ✅ research_logs/ - 深度研究日志"
echo "  ✅ memory/ - 日常记忆"
echo "  ✅ problem-database/ - 问题数据库"
echo "  ✅ hypotheses/ - 原创假设库"
echo "  ✅ thought_experiments/ - 思想实验"
echo "  ✅ derived_questions/ - 衍生问题"
echo "  ✅ scripts/ - 自动化脚本"
echo "  ✅ security_audits/ - 安全审计"
echo "  ✅ 所有配置和凭证"
