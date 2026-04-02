# ITLCT 博客部署指南 v2.0

**版本:** v2.0  
**更新日期:** 2026-04-02  
**状态:** ✅ 已验证

---

## 📋 博客仓库配置

### 远程仓库

**主仓库:** `chronos-blog`
```bash
URL: https://github.com/sandmark78/chronos-blog.git
Branch: main
```

**本地路径:**
```bash
/home/claworc/.openclaw/workspace/blog/
```

### Git 远程配置

```bash
# 查看远程仓库
cd /home/claworc/.openclaw/workspace/blog
git remote -v

# 输出应该是：
# blog        https://ghp_***@github.com/sandmark78/chronos-blog.git (fetch)
# blog        https://ghp_***@github.com/sandmark78/chronos-blog.git (push)
# chronos-blog  https://github.com/sandmark78/chronos-blog.git (fetch)
# chronos-blog  https://github.com/sandmark78/chronos-blog.git (push)
```

---

## 🚀 标准部署流程

### 方法 1: 手动推送 (推荐)

```bash
# 1. 进入博客目录
cd /home/claworc/.openclaw/workspace/blog

# 2. 检查文件状态
git status

# 3. 添加所有变更
git add -A

# 4. 提交
git commit -m '📝 博客更新：描述更新内容'

# 5. 推送到 chronos-blog 仓库
git push chronos-blog main

# 或者使用 blog 远程（带 token）
git push blog main
```

### 方法 2: 使用发布脚本

```bash
# 发布单篇文章
bash /home/claworc/.openclaw/workspace/scripts/publish-blog.sh <文章源文件> [slug]

# 示例
bash scripts/publish-blog.sh blog/posts/my-article.md itlct-v22-preview
```

### 方法 3: 每日更新脚本

```bash
# 每日博客更新
bash /home/claworc/.openclaw/workspace/scripts/update_blog_daily.sh "帖子标题" "帖子内容文件.md"
```

---

## ✅ 部署前检查清单

### 1. Jekyll 格式验证

```bash
# 检查 front matter
head -10 _posts/*.md | grep -E "^---|^layout:|^title:|^date:"

# 必须包含:
# ---
# layout: default
# title: "文章标题"
# date: YYYY-MM-DD
# ---
```

### 2. 图片链接验证

```bash
# 检查图片链接格式
grep -r "!\[" _posts/ | grep -v "site.baseurl" | grep -v "http"

# 正确格式:
# ![描述]({{ site.baseurl }}/assets/images/xxx.jpg)
```

### 3. _config.yml 验证

```bash
# 必须包含 repository 字段
grep "^repository:" _config.yml

# 应该是:
# repository: sandmark78/chronos-blog
```

### 4. 文件编码检查

```bash
# 检查 UTF-8 编码
file -bi _posts/*.md | grep -v "utf-8"

# 如果有非 UTF-8 文件，转换:
iconv -f GBK -t utf-8 file.md -o file.md.utf8 && mv file.md.utf8 file.md
```

---

## 🔧 GitHub Pages 配置

### 1. 启用 Pages

1. 访问：https://github.com/sandmark78/chronos-blog/settings/pages
2. **Source:** GitHub Actions (推荐)
3. 保存

### 2. 验证 Actions

1. 访问：https://github.com/sandmark78/chronos-blog/actions
2. 查看最新 workflow 运行状态
3. 绿色 ✅ 表示成功

### 3. 博客地址

**主地址:** https://sandmark78.github.io/chronos-blog/

**文章地址格式:**
```
https://sandmark78.github.io/chronos-blog/:year/:month/:day/:title.html
```

---

## 📝 文章格式标准

### Front Matter (必需)

```yaml
---
layout: default
title: "文章标题"
date: YYYY-MM-DD
---
```

### 图片链接格式

```markdown
![描述]({{ site.baseurl }}/assets/images/xxx.jpg)
```

### 内部链接格式

```markdown
[链接文本]({{ site.baseurl }}/path/to/page.html)
```

---

## ⚠️ 常见问题排查

### 问题 1: 404 错误

**原因:**
- 文章缺少 front matter
- _config.yml 缺少 repository 字段
- permalink 格式不匹配

**解决:**
```bash
# 检查 front matter
head -5 _posts/xxx.md

# 检查 _config.yml
grep "^repository:" _config.yml

# 检查 permalink 格式
grep "^permalink:" _config.yml
# 应该是：permalink: /:title.html
```

### 问题 2: 图片不显示

**原因:**
- 图片路径错误
- 未使用 site.baseurl

**解决:**
```bash
# 检查图片是否存在
ls -la assets/images/xxx.jpg

# 修正链接格式
sed -i 's/!\[.*\](\/assets/![描述]({{ site.baseurl }}\/assets/g' _posts/xxx.md
```

### 问题 3: 推送失败

**原因:**
- 远程仓库 URL 错误
- 权限问题

**解决:**
```bash
# 更新远程仓库 URL
git remote set-url chronos-blog https://github.com/sandmark78/chronos-blog.git

# 重新推送
git push chronos-blog main
```

---

## 🔄 自动化部署

### GitHub Actions Workflow

**文件:** `.github/workflows/deploy.yml`

```yaml
name: Deploy ITLCT Blog

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

---

## 📊 部署状态检查

### 检查命令

```bash
# 1. 检查 Git 状态
cd /home/claworc/.openclaw/workspace/blog
git status

# 2. 检查远程仓库
git remote -v

# 3. 检查最新提交
git log --oneline -5

# 4. 检查图片文件
ls -la assets/images/ | head -20

# 5. 检查文章数量
ls _posts/*.md | wc -l
```

### 预期输出

```
# Git 状态
On branch main
Your branch is up to date with 'chronos-blog/main'.

nothing to commit, working tree clean

# 远程仓库
blog        https://ghp_***@github.com/sandmark78/chronos-blog.git (fetch)
blog        https://ghp_***@github.com/sandmark78/chronos-blog.git (push)
chronos-blog  https://github.com/sandmark78/chronos-blog.git (fetch)
chronos-blog  https://github.com/sandmark78/chronos-blog.git (push)

# 最新提交
xxxxxxx 首页最终版：使用所有新找到的 Gemini 图片 (34 张完整图库)
xxxxxxx 🎉 Gemini 图片完整恢复报告 (34 张完整图库)
...

# 图片数量
34+ 张图片

# 文章数量
40+ 篇文章
```

---

## 🎯 最佳实践

### 1. 提交信息格式

```bash
# 标准格式
git commit -m '📝 博客更新：描述更新内容'

# 示例
git commit -m '🎉 10 张全新 Gemini 图片入库'
git commit -m '🖼️ 首页更新：使用新找到的 Gemini 图片'
git commit -m '📊 Gemini 图片完整恢复报告'
```

### 2. 推送频率

- **单篇文章:** 随时推送
- **批量更新:** 累积 5-10 篇后推送
- **图片更新:** 单独推送 (大文件)

### 3. 备份策略

```bash
# 本地备份
cp -r /home/claworc/.openclaw/workspace/blog /home/claworc/.openclaw/backups/blog-$(date +%Y%m%d)

# 远程备份 (可选)
git remote add backup https://github.com/sandmark78/chronos-lab-backup.git
git push backup main
```

---

## 📞 支持

**文档位置:**
- `/home/claworc/.openclaw/workspace/blog/DEPLOYMENT_GUIDE_v2.md`
- `/home/claworc/.openclaw/workspace/blog/DEPLOYMENT.md`

**脚本位置:**
- `/home/claworc/.openclaw/workspace/scripts/publish-blog.sh`
- `/home/claworc/.openclaw/workspace/scripts/update_blog_daily.sh`

**GitHub 仓库:**
- https://github.com/sandmark78/chronos-blog

---

*ITLCT 博客部署指南 v2.0 | 2026-04-02 | 已验证 ✅*
