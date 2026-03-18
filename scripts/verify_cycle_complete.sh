#!/bin/bash
# Chronos Lab 循环完整性验证 v2.0
# 每轮循环结束后必须运行，6项缺一不通过

WORKSPACE="/home/claworc/.openclaw/workspace"
DC=$1

if [ -z "$DC" ]; then
  DC=$(grep -o '"current_cycle": *[0-9]*' "$WORKSPACE/problem-database/current_cycle.json" | grep -o '[0-9]*')
fi

echo "🔍 DC-$DC 循环完整性验证"
echo "=========================="

PASS=0
FAIL=0

check() {
  local name="$1"
  local pattern="$2"
  local dir="$3"
  if ls "$WORKSPACE/$dir/" 2>/dev/null | grep -qE "$pattern"; then
    echo "✅ $name"
    PASS=$((PASS+1))
  else
    echo "❌ $name — 缺失！"
    FAIL=$((FAIL+1))
  fi
}

check "1. 核心产出 (knowledge/)" "DC-$DC\|T2[0-9][0-9]\|ITLCT\|GHPII" "knowledge"
check "2. 知识卡片" "DC-$DC" "knowledge_cards"
check "3. 研究日志" "DC-$DC\|Deep-Cycle-$DC" "research_logs"
check "4. current_cycle.json" "" "problem-database"

# 检查 current_cycle.json 是否更新到当前循环
CURRENT=$(grep -o '"current_cycle": *[0-9]*' "$WORKSPACE/problem-database/current_cycle.json" | grep -o '[0-9]*')
if [ "$CURRENT" -ge "$DC" ]; then
  echo "✅ 4. current_cycle = DC-$CURRENT"
  PASS=$((PASS+1))
else
  echo "❌ 4. current_cycle = DC-$CURRENT (应为 DC-$DC)"
  FAIL=$((FAIL+1))
fi

# 检查 memory
TODAY=$(date +%Y-%m-%d)
if grep -q "DC-$DC" "$WORKSPACE/memory/$TODAY.md" 2>/dev/null; then
  echo "✅ 5. memory/$TODAY.md 包含 DC-$DC"
  PASS=$((PASS+1))
else
  echo "❌ 5. memory/$TODAY.md 未包含 DC-$DC"
  FAIL=$((FAIL+1))
fi

echo ""
echo "=========================="
echo "结果: $PASS 通过 / $FAIL 失败"

if [ $FAIL -eq 0 ]; then
  echo "🎉 DC-$DC 完整性验证通过！可以推送。"
  exit 0
else
  echo "⛔ DC-$DC 有 $FAIL 项缺失，禁止推送！先补全再推。"
  exit 1
fi
