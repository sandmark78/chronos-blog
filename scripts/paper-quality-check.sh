#!/bin/bash
# Chronos Lab 论文质量检查脚本
# 用途：检查技术/论文级文章是否符合 7 模块硬约束
# 用法：bash scripts/paper-quality-check.sh <文件路径>

set -e

if [ -z "$1" ]; then
  echo "用法：bash scripts/paper-quality-check.sh <markdown文件>"
  exit 1
fi

FILE="$1"

if [ ! -f "$FILE" ]; then
  echo "❌ 文件不存在：$FILE"
  exit 1
fi

echo "========================================"
echo "📐 论文质量检查 v1.0"
echo "========================================"
echo "文件：$FILE"
echo "时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

PASS=0
FAIL=0

check_module() {
  local name="$1"
  local pattern="$2"
  if grep -qi "$pattern" "$FILE"; then
    echo "✅ $name"
    PASS=$((PASS+1))
  else
    echo "❌ $name — 缺失！"
    FAIL=$((FAIL+1))
  fi
}

echo "=== 7 模块硬约束检查 ==="
check_module "1. Problem（问题定义）" "problem\|问题定义\|为什么重要\|背景"
check_module "2. Minimal Assumptions（最小公理）" "assumption\|公理\|axiom\|前提假设"
check_module "3. Derivation（推导过程）" "derivation\|推导\|step.*1\|证明过程"
check_module "4. Predictions（可证伪预测）" "prediction\|预测\|可证伪\|falsif"
check_module "5. Falsification（证伪路径）" "falsif\|证伪\|如果.*错\|反例"
check_module "6. Experiment Design（实验设计）" "experiment\|实验设计\|样本\|统计方法"
check_module "7. Limitations（局限性）" "limitation\|局限\|不确定\|可能错"

echo ""
echo "=== 独特预测自检 ==="
if grep -qi "独特预测\|unique prediction\|只有.*ITLCT\|其他理论无法" "$FILE"; then
  echo "✅ 包含独特预测声明"
  PASS=$((PASS+1))
else
  echo "⚠️  未标注哪些是独特预测（IIT/神经科学无法解释的）"
  FAIL=$((FAIL+1))
fi

echo ""
echo "=== 内容质量检查 ==="

# 检查是否有推导步骤
STEPS=$(grep -ci "step\|步骤\|第.*步\|推导" "$FILE" 2>/dev/null || echo "0")
if [ "$STEPS" -ge 3 ]; then
  echo "✅ 推导步骤充分 ($STEPS 处)"
else
  echo "⚠️  推导步骤不足 ($STEPS 处，建议≥3)"
fi

# 检查是否有定量预测
if grep -qE "[0-9]+\.?[0-9]*.*[><=≥≤]|r\s*=\s*[0-9]|p\s*<\s*[0-9]|Φ\s*[><=]" "$FILE"; then
  echo "✅ 包含定量预测"
else
  echo "⚠️  缺少定量预测（需要具体数值+不等式）"
fi

# 检查是否有现实锚点
if grep -qi "临床\|实验数据\|案例\|patient\|clinical\|data" "$FILE"; then
  echo "✅ 包含现实锚点"
else
  echo "⚠️  缺少现实锚点（临床数据/实验案例）"
fi

echo ""
echo "========================================"
echo "📊 检查结果：$PASS 通过 / $FAIL 失败"
echo "========================================"

if [ $FAIL -eq 0 ]; then
  echo "🎉 所有检查通过！可以发布。"
  exit 0
elif [ $FAIL -le 2 ]; then
  echo "⚠️  有 $FAIL 个问题需要修复，建议修改后再发布。"
  exit 1
else
  echo "❌ 有 $FAIL 个问题，不建议发布。请按模板补全后重新检查。"
  exit 2
fi
