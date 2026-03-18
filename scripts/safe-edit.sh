#!/bin/bash
# Chronos Lab 实时快照工具
# 用途：修改关键文件前自动创建 .bak 备份
# 用法：source scripts/safe-edit.sh && safe_edit <文件路径>

SNAPSHOT_DIR="/home/claworc/.openclaw/workspace/.snapshots"
mkdir -p "$SNAPSHOT_DIR"

safe_edit() {
  local file="$1"
  
  if [ ! -f "$file" ]; then
    echo "❌ 文件不存在：$file"
    return 1
  fi
  
  local basename=$(basename "$file")
  local timestamp=$(date +%Y%m%d-%H%M%S)
  local snapshot="$SNAPSHOT_DIR/${timestamp}_${basename}.bak"
  
  cp "$file" "$snapshot"
  echo "📸 快照已创建：$snapshot"
  echo "   原文件：$file"
  echo "   大小：$(du -h "$snapshot" | cut -f1)"
}

# 批量快照：对 memory 目录所有文件创建快照
snapshot_memory() {
  local timestamp=$(date +%Y%m%d-%H%M%S)
  local snap_dir="$SNAPSHOT_DIR/memory-$timestamp"
  mkdir -p "$snap_dir"
  
  cp -r /home/claworc/.openclaw/workspace/memory/* "$snap_dir/" 2>/dev/null
  cp /home/claworc/.openclaw/workspace/MEMORY.md "$snap_dir/" 2>/dev/null
  cp /home/claworc/.openclaw/workspace/problem-database/current_cycle.json "$snap_dir/" 2>/dev/null
  cp /home/claworc/.openclaw/workspace/problem-database/progress.json "$snap_dir/" 2>/dev/null
  
  echo "📸 memory 快照已创建：$snap_dir"
  echo "   文件数：$(ls "$snap_dir" | wc -l)"
}

# 清理 7 天前的快照
cleanup_snapshots() {
  find "$SNAPSHOT_DIR" -mtime +7 -exec rm -rf {} \; 2>/dev/null
  echo "✅ 7 天前的快照已清理"
}

echo "✅ 快照工具已加载"
echo "   safe_edit <文件>     — 修改前创建快照"
echo "   snapshot_memory      — memory 目录快照"
echo "   cleanup_snapshots    — 清理旧快照"
