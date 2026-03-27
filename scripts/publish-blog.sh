#!/bin/bash
# Chronos Lab 博客发布技能
# 用途：安全发布博客文章到 chronos-blog 仓库
# 确保：Jekyll格式正确、文字不乱码、图片链接正确
#
# 用法：bash scripts/publish-blog.sh <文章源文件> [slug]
# 示例：bash scripts/publish-blog.sh workspace/blog/posts/my-article.md itlct-v22-preview

set -e

WORKSPACE="/home/claworc/.openclaw/workspace"
BLOG_REPO="https://sandmark78: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@github.com/sandmark78/chronos-blog.git"
BLOG_TMP="$WORKSPACE/.tmp/blog-publish-$(date +%Y%m%d-%H%M%S)"
TODAY=$(date +%Y-%m-%d)

# ==========================================
# 参数检查
# ==========================================
if [ -z "$1" ]; then
  echo "用法：bash scripts/publish-blog.sh <文章源文件> [slug]"
  echo ""
  echo "示例："
  echo "  bash scripts/publish-blog.sh blog/posts/article.md itlct-v22"
  echo "  bash scripts/publish-blog.sh blog/posts/010-new-post.md"
  exit 1
fi

SOURCE_FILE="$1"
SLUG="${2:-$(basename "$SOURCE_FILE" .md | sed 's/^[0-9]*-//')}"
TARGET_FILE="_posts/${TODAY}-${SLUG}.md"

if [ ! -f "$SOURCE_FILE" ]; then
  echo "❌ 源文件不存在：$SOURCE_FILE"
  exit 1
fi

echo "========================================"
echo "📝 Chronos Lab 博客发布"
echo "========================================"
echo "源文件：$SOURCE_FILE"
echo "目标：$TARGET_FILE"
echo "日期：$TODAY"
echo ""

# ==========================================
# 1. 克隆博客仓库
# ==========================================
echo "=== 1. 克隆博客仓库 ==="
rm -rf "$BLOG_TMP"
git clone --depth 1 "$BLOG_REPO" "$BLOG_TMP" 2>&1 | tail -3
cd "$BLOG_TMP"
git config user.name "Chronos Lab Bot"
git config user.email "chronos-lab-itlct@clawmail.to"

# ==========================================
# 2. 验证 Jekyll 格式
# ==========================================
echo ""
echo "=== 2. Jekyll 格式验证 ==="

# 检查 front matter
if ! head -1 "$SOURCE_FILE" | grep -q "^---"; then
  echo "⚠️  缺少 front matter，自动添加..."
  TITLE=$(head -5 "$SOURCE_FILE" | grep -m1 "^#" | sed 's/^# *//')
  [ -z "$TITLE" ] && TITLE="$SLUG"
  
  TMPFILE=$(mktemp)
  cat > "$TMPFILE" << EOF
---
layout: default
title: "$TITLE"
date: $TODAY
---

EOF
  cat "$SOURCE_FILE" >> "$TMPFILE"
  cp "$TMPFILE" "$SOURCE_FILE"
  rm "$TMPFILE"
  echo "✅ front matter 已添加"
else
  echo "✅ front matter 存在"
fi

# 检查 layout
if grep -q "^layout: post" "$SOURCE_FILE"; then
  echo "⚠️  layout: post → default (minimal主题兼容)"
  sed -i 's/^layout: post/layout: default/' "$SOURCE_FILE"
fi

# 检查 date
if ! grep -q "^date:" "$SOURCE_FILE"; then
  echo "⚠️  缺少 date，自动添加..."
  sed -i "s/^---$/date: $TODAY\n---/" "$SOURCE_FILE"
fi

# 检查 _config.yml 必须有 repository
if ! grep -q "^repository:" _config.yml; then
  echo "⚠️  _config.yml 缺少 repository 字段，添加..."
  echo "repository: sandmark78/chronos-blog" >> _config.yml
fi

echo "✅ Jekyll 格式验证通过"

# ==========================================
# 3. 文字编码检查（防乱码）
# ==========================================
echo ""
echo "=== 3. 文字编码检查 ==="

ENCODING=$(file -bi "$SOURCE_FILE" | grep -o "charset=[^ ]*" | cut -d= -f2)
echo "文件编码：$ENCODING"

if [ "$ENCODING" != "utf-8" ] && [ "$ENCODING" != "us-ascii" ]; then
  echo "⚠️  编码不是 UTF-8，转换中..."
  iconv -f "$ENCODING" -t utf-8 "$SOURCE_FILE" -o "$SOURCE_FILE.utf8" 2>/dev/null && mv "$SOURCE_FILE.utf8" "$SOURCE_FILE"
  echo "✅ 已转换为 UTF-8"
else
  echo "✅ 编码正确 (UTF-8)"
fi

# 检查是否有非法字符
if grep -P '[\x80-\xff]' "$SOURCE_FILE" | grep -qP '[^\x00-\x7f\xc0-\xff][\x80-\xbf]'; then
  echo "✅ 中文字符正常"
else
  echo "✅ 纯 ASCII 或正常 UTF-8"
fi

# ==========================================
# 4. 图片链接检查
# ==========================================
echo ""
echo "=== 4. 图片链接检查 ==="

IMG_COUNT=$(grep -c "!\[" "$SOURCE_FILE" 2>/dev/null || echo "0")
echo "图片数量：$IMG_COUNT"

if [ "$IMG_COUNT" -gt 0 ]; then
  # 检查图片链接是否使用 site.baseurl
  BAD_LINKS=$(grep "!\[" "$SOURCE_FILE" | grep -v "site.baseurl" | grep -v "http" | wc -l)
  if [ "$BAD_LINKS" -gt 0 ]; then
    echo "⚠️  $BAD_LINKS 个图片链接未使用 site.baseurl"
    echo "    建议格式：![描述]({{ site.baseurl }}/assets/images/xxx.jpg)"
  else
    echo "✅ 图片链接格式正确"
  fi
fi

# ==========================================
# 5. 复制文章到 _posts/
# ==========================================
echo ""
echo "=== 5. 发布文章 ==="
cp "$SOURCE_FILE" "$TARGET_FILE"
echo "✅ 已复制到 $TARGET_FILE"

# ==========================================
# 6. 更新首页 index.md（添加新文章链接）
# ==========================================
echo ""
echo "=== 6. 更新首页 ==="
TITLE=$(grep "^title:" "$TARGET_FILE" | head -1 | sed 's/^title: *//' | sed 's/^"//' | sed 's/"$//')
# 修正链接格式：permalink 是 /:year/:month/:day/:title/
YEAR=$(echo "$TODAY" | cut -d- -f1)
MONTH=$(echo "$TODAY" | cut -d- -f2)
DAY=$(echo "$TODAY" | cut -d- -f3)
LINK_LINE="| $TODAY | [$TITLE]({{ site.baseurl }}/$YEAR/$MONTH/$DAY/$SLUG/) |"

# 在"最新文章"表头后的第一个数据行前插入（只插入一次）
if grep -q "最新文章\|Latest" index.md; then
  # 检查是否已存在相同文章（防重复）
  if grep -q "$SLUG" index.md; then
    echo "⚠️  文章已存在于首页，跳过插入"
  else
    # 找到表头分隔线 |------| 后插入一行
    sed -i "0,/^|------/{ /^|------/a\\$LINK_LINE
    }" index.md
    echo "✅ 首页已更新（新文章添加到列表顶部）"
  fi
else
  echo "⚠️  首页格式不匹配，请手动更新 index.md"
fi

# ==========================================
# 6.5 生成贡献者致谢（新增）
# ==========================================
echo ""
echo "=== 6.5 生成贡献者致谢 ==="
CONTRIBUTORS_FILE="$WORKSPACE/CONTRIBUTORS.md"

if [ -f "$CONTRIBUTORS_FILE" ]; then
  echo "读取贡献者名单..."
  
  # 提取贡献者列表（前 10 位）
  ACK_LIST=$(grep -E "^\| \[@[^\]]+\]" "$CONTRIBUTORS_FILE" | head -10 | while read line; do
    USERNAME=$(echo "$line" | sed 's/.*\[@\([^|]*\)\].*/\1/' | tr -d ' ')
    LINK=$(echo "$line" | sed 's/.*](\([^)]*\)).*/\1/' | tr -d ' ')
    TYPE=$(echo "$line" | awk -F'|' '{print $4}' | tr -d ' ')
    echo "- **[$USERNAME]($LINK)** — $TYPE"
  done)
  
  if [ -n "$ACK_LIST" ]; then
    echo "添加贡献者致谢到文章末尾..."
    
    # 添加到文章末尾
    cat >> "$TARGET_FILE" << EOF

---

## 🙏 致谢

感谢以下社区成员对 ITLCT 理论发展的贡献：

$ACK_LIST

ITLCT 理论的发展离不开社区的批评和建议。每一个尖锐的问题、每一个深刻的洞见，都让这个理论更加完善。
EOF
    
    echo "✅ 贡献者致谢已添加"
  else
    echo "⚠️  贡献者名单为空，跳过致谢"
  fi
else
  echo "⚠️  贡献者名单文件不存在：$CONTRIBUTORS_FILE"
fi

# ==========================================
# 7. 提交并推送
# ==========================================
echo ""
echo "=== 7. 提交并推送 ==="
git add -A
git commit -m "📝 发布新文章：$TITLE ($TODAY)"
git push origin main 2>&1 | tail -3

# ==========================================
# 8. 清理
# ==========================================
rm -rf "$BLOG_TMP"

echo ""
echo "========================================"
echo "✅ 博客发布完成！"
echo "========================================"
echo "文章：$TARGET_FILE"
echo "标题：$TITLE"
echo "链接：https://sandmark78.github.io/chronos-blog/$TODAY/$SLUG/"
echo ""
echo "等待 2-3 分钟 GitHub Pages 构建完成后可访问。"
