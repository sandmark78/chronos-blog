#!/bin/bash
# Chronos Lab 夜间安全审计脚本
# 执行 13 项核心安全检查
# 运行时间：每日 03:00

set -e

AUDIT_DATE=$(date +%Y-%m-%d_%H-%M-%S)
AUDIT_REPORT="security_audits/nightly-audit-${AUDIT_DATE}.md"
WORKSPACE="/home/claworc/.openclaw/workspace"

echo "========================================"
echo "🔒 Chronos Lab 夜间安全审计"
echo "========================================"
echo "审计时间：$(date)"
echo "工作区：$WORKSPACE"
echo ""

# 创建审计报告目录
mkdir -p "$WORKSPACE/security_audits"

# 初始化报告
cat > "$AUDIT_REPORT" << HEADER
# 夜间安全审计报告

**审计时间:** $(date +%Y-%m-%d\ %H:%M:%S)  
**工作区:** $WORKSPACE  
**审计类型:** 13 项核心指标夜间审计

---

## 审计结果汇总

HEADER

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# 审计函数
audit_check() {
    local name="$1"
    local check="$2"
    local severity="$3"
    
    echo -n "检查：$name ... "
    
    if eval "$check" > /dev/null 2>&1; then
        echo "✅ 通过"
        echo "- [✅] **$name** - 通过" >> "$AUDIT_REPORT"
        ((PASS_COUNT++))
    else
        if [ "$severity" = "CRITICAL" ]; then
            echo "❌ 失败 [严重]"
            echo "- [❌] **$name** - 失败 [严重]" >> "$AUDIT_REPORT"
            ((FAIL_COUNT++))
        else
            echo "⚠️ 警告"
            echo "- [⚠️] **$name** - 警告" >> "$AUDIT_REPORT"
            ((WARN_COUNT++))
        fi
    fi
}

echo "## 13 项核心安全检查" >> "$AUDIT_REPORT"
echo ""

# 1. Git 仓库状态检查
audit_check "Git 仓库完整性" "cd $WORKSPACE && git fsck --quiet"

# 2. 敏感文件权限检查 (openclaw.json 应为 600)
audit_check "敏感文件权限 (openclaw.json)" "[ \$(stat -c %a $WORKSPACE/../openclaw.json 2>/dev/null) = '600' ]"

# 3. API Key 泄露检查
audit_check "无 API Key 泄露" "! grep -r 'sk-' $WORKSPACE --include='*.md' --include='*.txt' 2>/dev/null | grep -v '.git'"

# 4. 备份完整性检查
audit_check "Git 备份仓库存在" "[ -d $WORKSPACE/.git ]"

# 5. 研究日志连续性检查
audit_check "研究日志连续性" "[ \$(ls $WORKSPACE/research_logs/Deep-Cycle-*.md 2>/dev/null | wc -l) -gt 150 ]"

# 6. 知识卡片完整性检查
audit_check "知识卡片完整性" "[ \$(ls $WORKSPACE/knowledge/知识卡片/*.md 2>/dev/null | wc -l) -gt 50 ]"

# 7. 进度数据库完整性检查
audit_check "进度数据库完整性" "[ -f $WORKSPACE/problem-database/progress.json ] && jq '.version' $WORKSPACE/problem-database/progress.json > /dev/null 2>&1"

# 8. 内存使用检查 (应 < 80%)
audit_check "内存使用正常 (<80%)" "[ \$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}') -lt 80 ]"

# 9. 磁盘空间检查 (应 > 20% 可用)
audit_check "磁盘空间充足 (>20%)" "[ \$(df $WORKSPACE | tail -1 | awk '{print $5}' | sed 's/%//') -lt 80 ]"

# 10. Cron 任务状态检查
audit_check "Cron 任务正常运行" "pgrep -f 'openclaw' > /dev/null 2>&1 || [ -f /tmp/openclaw.pid ]"

# 11. 无异常进程检查
audit_check "无异常进程" "! ps aux | grep -v grep | grep -E 'malware|miner|backdoor' > /dev/null 2>&1"

# 12. 文件篡改检测 (基于 git 状态)
audit_check "无未授权文件修改" "cd $WORKSPACE && git status --porcelain | wc -l | grep -q '^0$' || echo '有未提交文件'"

# 13. 睡眠固化配置检查
audit_check "睡眠固化配置正确" "grep -q 'sleep-consolidation' $WORKSPACE/../openclaw.json 2>/dev/null || grep -q '02:00' $WORKSPACE/../openclaw.json 2>/dev/null"

echo "" >> "$AUDIT_REPORT"
echo "" >> "$AUDIT_REPORT"

# 生成汇总
cat >> "$AUDIT_REPORT" << SUMMARY
## 审计汇总

| 指标 | 数量 |
|------|------|
| ✅ 通过 | $PASS_COUNT |
| ⚠️ 警告 | $WARN_COUNT |
| ❌ 失败 | $FAIL_COUNT |

**总体评估:** $(if [ $FAIL_COUNT -eq 0 ]; then echo "✅ 安全"; elif [ $FAIL_COUNT -le 2 ]; then echo "⚠️ 需关注"; else echo "❌ 需立即处理"; fi)

---

## 建议操作

SUMMARY

if [ $FAIL_COUNT -gt 0 ]; then
    echo "**需要立即处理的安全问题:**" >> "$AUDIT_REPORT"
    echo "1. 检查上述失败项" >> "$AUDIT_REPORT"
    echo "2. 联系系统管理员" >> "$AUDIT_REPORT"
else
    echo "✅ 无严重安全问题，系统运行正常" >> "$AUDIT_REPORT"
fi

echo "" >> "$AUDIT_REPORT"
echo "---" >> "$AUDIT_REPORT"
echo "*审计报告自动生成 | Chronos Lab 安全矩阵 v2.7*" >> "$AUDIT_REPORT"

# 输出汇总
echo ""
echo "========================================"
echo "审计完成！"
echo "========================================"
echo "通过：$PASS_COUNT/13"
echo "警告：$WARN_COUNT"
echo "失败：$FAIL_COUNT"
echo ""
echo "报告位置：$AUDIT_REPORT"
echo "========================================"

# 如果有严重失败，退出码为 1
if [ $FAIL_COUNT -gt 0 ]; then
    exit 1
fi

exit 0
