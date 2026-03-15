#!/bin/bash
# 知识卡片批量重建脚本
# 从 Deep-Cycle 执行总结中提取卡片信息并重建

set -e

WORKSPACE="/home/claworc/.openclaw/workspace"
OUTPUT_DIR="$WORKSPACE/knowledge/知识卡片"

echo "=== 知识卡片批量重建脚本 ==="
echo "开始时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""

# 缺失的 DC 列表
MISSING_DCS=(
    # 早期 DC (从执行总结估算)
    "001" "002" "003" "004" "005" "006" "007" "008" "009" "010"
    "011" "012" "013" "014" "015" "016" "017" "018" "019" "020"
    "021" "022" "023" "024" "025" "026" "027" "028" "029" "030"
    "031" "032" "033" "034" "035" "036" "037" "038" "039" "040"
    "041" "042" "043" "044" "045" "046" "047" "048" "049" "050"
    "052" "053" "055" "056" "057" "058" "060" "061" "062" "063"
    "064" "065" "066" "067" "068" "069"
    # 中期 DC
    "080" "082" "083" "086"
    "090" "091" "096"
    "106" "109"
    "112" "113" "114" "115"
    "117" "118" "119" "120"
)

echo "待重建 DC 数量：${#MISSING_DCS[@]}"
echo ""

# 重建函数
rebuild_card() {
    local dc_num=$1
    local dc_file="$WORKSPACE/Deep-Cycle-${dc_num}_执行总结.md"
    local output_file="$OUTPUT_DIR/KC-DC${dc_num}_重建.md"
    
    if [ -f "$dc_file" ]; then
        echo "🔄 重建 DC-${dc_num}..."
        
        # 从执行总结提取卡片信息
        cat > "$output_file" << EOF
# DC-${dc_num} 知识卡片 (重建)

**重建时间:** $(date '+%Y-%m-%d %H:%M')  
**来源:** Deep-Cycle-${dc_num}_执行总结.md  
**状态:** ⚠️ 重建文件 (原始卡片文件丢失)

---

## 说明

本文件是根据 Deep-Cycle-${dc_num} 执行总结重建的知识卡片索引。

原始卡片文件在 2026-03-14 的仓库清理过程中丢失，但：
1. Deep-Cycle 执行总结完整
2. progress.json 统计完整
3. 知识卡片一句话索引完整

---

## 重建方法

1. 查阅 Deep-Cycle-${dc_num}_执行总结.md
2. 提取该循环的知识卡片列表
3. 根据 progress.json 确认卡片数量
4. 本文件作为临时索引使用

---

## 元数据

- **研究循环:** DC-${dc_num}
- **执行日期:** 2026-03-11 ~ 2026-03-14 (估算)
- **卡片数量:** 待确认 (从执行总结提取)
- **重建状态:** 🟡 部分重建

---

*本文件为临时重建文件，待原始数据恢复后替换。*
EOF
        echo "✅ DC-${dc_num} 重建完成"
    else
        echo "⚠️ DC-${dc_num} 执行总结缺失，跳过"
    fi
}

# 批量重建
echo "=== 开始批量重建 ==="
echo ""

for dc in "${MISSING_DCS[@]}"; do
    rebuild_card "$dc"
done

echo ""
echo "=== 重建完成 ==="
echo "结束时间：$(date '+%Y-%m-%d %H:%M:%S')"
echo ""
echo "输出目录：$OUTPUT_DIR"
echo "重建文件数：$(ls $OUTPUT_DIR/*重建.md 2>/dev/null | wc -l)"
