#!/bin/bash
# Chronos Lab 记忆自动更新脚本
# 每次会话启动和结束时自动执行

set -e

WORKSPACE="/home/claworc/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$WORKSPACE/memory/$DATE.md"
PROGRESS_FILE="$WORKSPACE/problem-database/progress.json"

echo "🕗 Chronos Lab 记忆更新"
echo "日期：$DATE"
echo ""

# 1. 确保记忆文件存在
if [ ! -f "$MEMORY_FILE" ]; then
    echo "创建今日记忆文件..."
    cat > "$MEMORY_FILE" << EOF
# 研究记忆 $DATE

**创建时间:** $(date +%H:%M)
**循环编号:** DC-{自动填充}
**核心任务:** {自动填充}

---

## 会话记录

### 醒来仪式
- [ ] SOUL.md 已读
- [ ] USER.md 已读
- [ ] MEMORY.md 已读
- [ ] progress.json 同步
- [ ] 连续性确认

## 核心进展

## 关键洞见

## 待办事项

---
EOF
    echo "✅ 记忆文件已创建"
else
    echo "✅ 记忆文件已存在"
fi

# 2. 更新进度追踪
if [ -f "$PROGRESS_FILE" ]; then
    CURRENT_CYCLE=$(cat "$PROGRESS_FILE" | python3 -c "import sys,json; print(json.load(sys.stdin).get('currentCycle',{}).get('number','N/A'))" 2>/dev/null || echo "N/A")
    echo "当前循环：DC-$CURRENT_CYCLE"
else
    echo "⚠️ progress.json 不存在"
fi

# 3. Git 状态检查
cd "$WORKSPACE"
GIT_STATUS=$(git status --porcelain | wc -l)
if [ $GIT_STATUS -gt 0 ]; then
    echo "⚠️ 有 $GIT_STATUS 个未提交文件"
    echo "建议：git add -A && git commit -m '📝 记忆更新'"
else
    echo "✅ Git 工作区干净"
fi

# 4. 备份检查
if [ -d "$WORKSPACE/backups" ]; then
    LATEST_BACKUP=$(ls -t "$WORKSPACE/backups/"*.tar.gz 2>/dev/null | head -1)
    if [ -n "$LATEST_BACKUP" ]; then
        BACKUP_TIME=$(stat -c %y "$LATEST_BACKUP" 2>/dev/null | cut -d' ' -f1-2 | cut -d'.' -f1)
        echo "✅ 最新备份：$LATEST_BACKUP ($BACKUP_TIME)"
    fi
fi

echo ""
echo "🕗 记忆更新完成"
