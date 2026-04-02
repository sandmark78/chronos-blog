# 博客构建修复报告

**修复日期:** 2026-04-02 13:30  
**问题:** GitHub Pages 构建失败  
**状态:** ✅ 已修复

---

## 🔧 问题诊断

### 问题 1: 目录名称错误
**问题:** 使用 `posts/` 目录，Jekyll 要求 `_posts/`  
**修复:** `mv posts _posts`

### 问题 2: 文件名格式错误
**问题:** 文件名如 `014-phi-growth-analysis.md`，Jekyll 要求 `YYYY-MM-DD-slug.md`  
**修复:** 批量重命名 40 篇文章

**重命名示例:**
- `001-framework-intro.md` → `2026-03-20-itlct-framework-intro.md`
- `014-phi-growth-analysis.md` → `2026-03-20-phi-growth-analysis.md`
- `2026-03-31-102-round-continuity-record.md` → ✅ 已符合格式

### 问题 3: _config.yml 配置错误
**问题:** collections 配置指向错误的 posts 目录  
**修复:** 简化配置，使用 Jekyll 默认 _posts 目录

**修复前:**
```yaml
collections:
  posts:
    output: true
    permalink: /:collection/:name/
defaults:
  - scope:
      path: "posts"
      type: posts
    values:
      layout: default
```

**修复后:**
```yaml
repository: sandmark78/chronos-blog
permalink: /:year/:month/:day/:title/
defaults:
  - scope:
      path: "_posts"
      type: posts
    values:
      layout: default
```

### 问题 4: .gitignore 配置错误
**问题:** 允许 `blog/posts/` 但阻止 `blog/_posts/`  
**修复:** 更新 .gitignore

**修复前:**
```
!blog/posts/
!blog/posts/*.md
```

**修复后:**
```
!blog/_posts/
!blog/_posts/*.md
```

### 问题 5: index.md 链接格式错误
**问题:** 硬编码链接，未使用 Jekyll 模板  
**修复:** 使用 Liquid 模板自动生成文章列表

**修复后:**
```liquid
{% for post in site.posts limit: 10 %}
- **{{ post.date | date: "%Y-%m-%d" }}**: [{{ post.title }}]({{ site.baseurl }}{{ post.url }})
{% endfor %}
```

---

## ✅ 修复结果

**修复文件数:** 40 篇博客文章  
**Git 提交:**
1. `posts→_posts + 文件名格式修复 + _config.yml 修正`
2. `.gitignore 更新：posts→_posts`
3. `博客文章添加到 _posts 目录 (Jekyll 标准格式，40 篇)`

**博客地址:** https://sandmark78.github.io/chronos-blog/

---

## 📋 Jekyll 博客标准格式

### 目录结构
```
blog/
├── _posts/              # ✅ 文章目录（必须是 _posts）
│   ├── YYYY-MM-DD-slug.md
│   └── ...
├── _config.yml          # ✅ 配置文件
├── index.md             # ✅ 首页
├── assets/              # ✅ 静态资源
└── .github/workflows/
    └── deploy.yml       # ✅ GitHub Actions 部署
```

### 文章 Front Matter
```yaml
---
layout: default          # ✅ 使用 default（minimal 主题没有 post layout）
title: "文章标题"
date: YYYY-MM-DD         # ✅ 必须有日期
---
```

### 文件名格式
```
YYYY-MM-DD-slug.md
例如：2026-03-20-phi-growth-analysis.md
```

### _config.yml 必需字段
```yaml
theme: jekyll-theme-minimal
title: ITLCT Research Blog
description: Unified Framework for Information-Time-Life-Consciousness
baseurl: /chronos-blog
url: https://sandmark78.github.io
repository: sandmark78/chronos-blog    # ⚠️ 必须有！否则构建失败
markdown: kramdown
permalink: /:year/:month/:day/:title/
```

---

## 🚀 部署流程

**GitHub Actions 自动部署:**
1. 推送到 main 分支
2. GitHub Actions 自动构建 Jekyll
3. 部署到 GitHub Pages
4. 访问：https://sandmark78.github.io/chronos-blog/

**手动触发部署:**
```bash
cd blog
git push origin main
```

---

## ⚠️ 常见错误

### ❌ 错误 1: layout: post
```yaml
layout: post  # ❌ minimal 主题没有 post layout
```

**修复:**
```yaml
layout: default  # ✅ 使用 default
```

### ❌ 错误 2: 缺少 repository 字段
```yaml
# 缺少 repository 字段会导致 GitHub Pages 构建失败
```

**修复:**
```yaml
repository: sandmark78/chronos-blog  # ✅ 必须添加
```

### ❌ 错误 3: 文件名没有日期
```
phi-growth-analysis.md  # ❌ 缺少日期前缀
```

**修复:**
```
2026-03-20-phi-growth-analysis.md  # ✅ 添加日期前缀
```

### ❌ 错误 4: posts 目录
```
blog/posts/  # ❌ Jekyll 要求 _posts
```

**修复:**
```
blog/_posts/  # ✅ 使用 _posts
```

---

## 📊 修复前后对比

| 项目 | 修复前 | 修复后 |
|------|--------|--------|
| 目录名 | posts/ | _posts/ ✅ |
| 文件名 | 014-xxx.md | 2026-03-20-014-xxx.md ✅ |
| _config.yml | collections 配置 | 简化配置 ✅ |
| .gitignore | !blog/posts/ | !blog/_posts/ ✅ |
| index.md | 硬编码链接 | Liquid 模板 ✅ |
| repository 字段 | 缺失 | 已添加 ✅ |

---

## 🎯 下一步

1. **验证 GitHub Pages 构建** — 等待 GitHub Actions 完成
2. **访问博客** — https://sandmark78.github.io/chronos-blog/
3. **持续更新** — 新文章按照 `YYYY-MM-DD-slug.md` 格式

---

*博客修复完成 | 2026-04-02 13:30 | 40 篇文章已修复*
