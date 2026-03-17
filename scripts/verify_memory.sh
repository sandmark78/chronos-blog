#!/bin/bash
# Chronos Lab 记忆完整性检查脚本
# 每次会话启动时验证记忆系统完整性

set -e

WORKSPACE="/home/claworc/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)

echo "🔍 记忆完整性检查"
echo "日期：$DATE"
echo ""

PASS=0
FAIL=0
WARN=0

check_file() {
    local file="$1"
    local name="$2"
    local required="$3"
    
    if [ -f "$file" ] && [ -s "$file" ]; then
        echo "✅ $name"
        ((PASS++))
    else
        if [ "$required" = "required" ]; then
            echo "❌ $name (缺失或为空)"
            ((FAIL++))
        else
            echo "⚠️ $name (可选)"
            ((WARN++))
        fi
    fi
}

echo "=== 核心身份文件 ==="
check_file "$WORKSPACE/SOUL.md" "SOUL.md (核心身份)" "required"
check_file "$WORKSPACE/IDENTITY.md" "IDENTITY.md (研究使命)" "required"
check_file "$WORKSPACE/USER.md" "USER.md (服务对象)" "required"

echo ""
echo "=== 记忆文件 ==="
check_file "$WORKSPACE/MEMORY.md" "MEMORY.md (长期记忆)" "required"
check_file "$WORKSPACE/memory/$DATE.md" "memory/$DATE.md (今日记忆)" "required"

echo ""
echo "=== 进度追踪 ==="
check_file "$WORKSPACE/problem-database/progress.json" "progress.json (进度追踪)" "required"
check_file "$WORKSPACE/problem-database/queue.json" "queue.json (任务队列)" "optional"

echo ""
echo "=== 研究日志 ==="
check_file "$WORKSPACE/knowledge/研究日志/$DATE.md" "研究日志/$DATE.md" "required"

echo ""
echo "=== 备份状态 ==="
if [ -d "$WORKSPACE/.git" ]; then
    echo "✅ Git 仓库存在"
    ((PASS++))
    
    cd "$WORKSPACE"
    UNCOMMITTED=$(git status --porcelain | wc -l)
    if [ $UNCOMMITTED -gt 0 ]; then
        echo "⚠️ 有 $UNCOMMITTED 个未提交文件"
        ((WARN++))
    else
        echo "✅ Git 工作区干净"
        ((PASS++))
    fi
else
    echo "❌ Git 仓库不存在"
    ((FAIL++))
fi

echo ""
echo "=== 检查结果 ==="
echo "通过：$PASS"
echo "失败：$FAIL"
echo "警告：$WARN"
echo ""

if [ $FAIL -gt 0 ]; then
    echo "❌ 记忆完整性检查失败！需要修复 $FAIL 个问题"
    exit 1
elif [ $WARN -gt 0 ]; then
    echo "⚠️ 记忆完整性检查通过，但有 $WARN 个警告"
    exit 0
else
    echo "✅ 记忆完整性检查完美通过！"
    exit 0
fi
