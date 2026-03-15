#!/bin/bash
# Chronos Lab 博客每日更新脚本
# 用法：./scripts/update_blog_daily.sh "帖子标题" "帖子内容文件.md"

set -e

DATE=$(date +%Y-%m-%d)
TITLE_SLUG=$(echo "$1" | tr ' ' '-' | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9-]//g')
POST_FILE="_posts/${DATE}-${TITLE_SLUG}.md"

echo "📝 创建博客文章：$POST_FILE"

# 创建 front matter
cat > "$POST_FILE" << EOF
---
title: "$1"
date: $DATE
layout: post
tags: research, ITLCT, consciousness, AI, daily-update
excerpt: "Daily research update from Chronos Lab."
---

EOF

# 添加内容
if [ -f "$2" ]; then
  cat "$2" >> "$POST_FILE"
  echo "✅ 内容来自：$2"
else
  echo "⚠️ 内容文件不存在：$2"
fi

# 提交并推送
git add "$POST_FILE"
git commit -m "📝 博客更新：$1 ($DATE)"
git push blog main

echo "✅ 博客更新完成！"
echo "🌐 查看：https://sandmark78.github.io/chronos-blog/$DATE/$TITLE_SLUG/"
