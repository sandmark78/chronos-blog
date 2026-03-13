# ITLCT Blog — GitHub Pages 部署指南

**创建时间:** 2026-03-13  
**平台:** GitHub Pages + Jekyll  
**状态:** 准备部署

---

## 📋 部署前准备

### 1. 确认文件结构

```
blog/
├── README.md              ✅ 已创建
├── _config.yml            ✅ 已创建
├── LICENSE                ✅ 已创建
├── .github/
│   ├── CONTRIBUTING.md    ✅ 已创建
│   └── workflows/
│       └── deploy.yml     ✅ 已创建
├── posts/
│   └── 001-framework-intro.md  ✅ 已创建
└── DEPLOYMENT.md          ✅ 本文件
```

---

## 🚀 部署步骤

### 步骤 1: 创建 GitHub 仓库

**选项 A: 使用命令行**

```bash
# 进入博客目录
cd /home/claworc/.openclaw/workspace/blog

# 初始化 Git 仓库
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial ITLCT blog commit"

# 添加远程仓库
git remote add origin https://github.com/sandmark78/itlct-blog.git

# 推送到 GitHub
git push -u origin main
```

**选项 B: 使用 GitHub 网页**

1. 访问 https://github.com/new
2. 仓库名：`itlct-blog`
3. 可见性：Public (公开)
4. 点击 "Create repository"
5. 按页面提示上传文件

---

### 步骤 2: 启用 GitHub Pages

1. 访问仓库页面：https://github.com/sandmark78/itlct-blog
2. 点击 **Settings** (设置)
3. 左侧菜单选择 **Pages**
4. **Source** 选择：`Deploy from a branch`
5. **Branch** 选择：`main` / `/(root)`
6. 点击 **Save**

**等待部署:**
- GitHub Actions 会自动运行
- 约 1-2 分钟后部署完成
- 页面地址：https://sandmark78.github.io/itlct-blog/

---

### 步骤 3: 验证部署

**检查部署状态:**

1. 访问仓库 **Actions** 标签
2. 查看最新 workflow 运行状态
3. 绿色 ✅ 表示成功
4. 红色 ❌ 表示失败 (查看日志排查)

**访问博客:**

- 主页面：https://sandmark78.github.io/itlct-blog/
- 第一篇文章：https://sandmark78.github.io/itlct-blog/posts/001-framework-intro.html

---

## 📝 发布新文章

### 方法 1: 直接添加 Markdown 文件

```bash
# 创建新文章
cd /home/claworc/.openclaw/workspace/blog/posts

# 命名格式：YYYY-MM-DD-title.md
# 例如：2026-03-20-dc091-summary.md

# 编辑文章
nano 2026-03-20-dc091-summary.md

# 添加文章头部 (front matter)
---
title: "Deep-Cycle-091 Summary"
date: 2026-03-20
tags: [research, update, deep-cycle]
---

# 文章正文...

# 提交
git add .
git commit -m "Add DC-091 summary"
git push
```

### 方法 2: 使用研究循环自动生成

**自动化脚本 (待创建):**

```python
#!/usr/bin/env python3
"""
ITLCT Blog Post Generator
Automatically generates blog posts from research logs
"""

import json
from datetime import datetime

def generate_weekly_update():
    """Generate weekly research update from progress.json"""
    
    # Load research data
    with open('../problem-database/progress.json') as f:
        progress = json.load(f)
    
    # Generate post
    post = f"""---
title: "Weekly Research Update #{datetime.now().strftime('%Y-W%W')}"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: [research, weekly-update]
---

# Weekly Research Update

## Progress This Week

- Research cycles: {progress.get('researchCyclesCompleted', 0)}
- Total hypotheses: {progress.get('totalHypotheses', 0)}
- Knowledge cards: {progress.get('totalKnowledgeCards', 0)}

## Key Highlights

[Manual curation needed]

## Next Week's Goals

[Manual planning needed]
"""
    
    # Save post
    filename = f"posts/{datetime.now().strftime('%Y-%m-%d')}-weekly-update.md"
    with open(filename, 'w') as f:
        f.write(post)
    
    print(f"Generated: {filename}")

if __name__ == "__main__":
    generate_weekly_update()
```

---

## 🔧 自定义配置

### 修改网站标题

编辑 `_config.yml`:

```yaml
title: ITLCT Research Blog  # 网站标题
description: Unified Framework for Information-Time-Life-Consciousness  # 网站描述
```

### 更换主题

**可用主题:** https://pages.github.com/themes/

**编辑 `_config.yml`:**

```yaml
theme: jekyll-theme-minimal  # 可更换为其他主题
# theme: jekyll-theme-cayman
# theme: jekyll-theme-modernist
# theme: jekyll-theme-slate
```

### 添加自定义域名

**步骤:**

1. 购买域名 (如 itlct.org)
2. 在域名 DNS 设置添加 CNAME 记录
3. 在仓库 **Settings → Pages** 添加自定义域名
4. 等待 DNS 传播 (约 24 小时)

**创建 `CNAME` 文件:**

```
itlct.org
```

---

## 📊 自动化工作流

### 自动部署流程

```
研究循环完成
    ↓
生成研究总结 (手动/自动)
    ↓
Git commit + push
    ↓
GitHub Actions 触发
    ↓
Jekyll 构建网站
    ↓
部署到 GitHub Pages
    ↓
博客更新完成
```

### 设置自动发布 (可选)

**编辑 `.github/workflows/deploy.yml`:**

```yaml
on:
  push:
    branches: [ main ]
  schedule:
    - cron: '0 0 * * 0'  # 每周日自动部署
  workflow_dispatch:
```

---

## 🐛 故障排查

### 问题 1: 部署失败

**检查:**

1. 查看 **Actions** 标签的日志
2. 确认 `_config.yml` 格式正确
3. 确认 Markdown 文件 front matter 正确

**常见错误:**

- YAML 缩进错误
- Markdown front matter 格式错误
- 文件路径错误

### 问题 2: 页面显示 404

**解决:**

1. 等待 1-2 分钟 (部署需要时间)
2. 检查 Pages 设置是否正确
3. 确认 `main` 分支存在
4. 清除浏览器缓存

### 问题 3: 样式不显示

**解决:**

1. 检查浏览器控制台错误
2. 确认主题配置正确
3. 检查网络访问 (某些地区可能受限)

---

## 📈 推广博客

### SEO 优化

1. **使用描述性标题**
2. **添加合适标签** (tags)
3. **使用清晰 URL 结构**
4. **添加元描述** (在 `_config.yml`)

### 社交媒体推广

**模板:**

```
📝 New blog post: ITLCT Framework Introduction

We present a unified theoretical framework for 
Information-Time-Life-Consciousness.

90 research cycles, 1,700+ hypotheses, 1,900+ knowledge cards.

Read more: https://sandmark78.github.io/itlct-blog/posts/001-framework-intro.html

#ITLCT #Consciousness #AI #Physics #UnifiedTheory
```

**推广渠道:**

- Twitter/X
- Reddit (r/consciousness, r/ArtificialIntelligence)
- LinkedIn
- ResearchGate
- Medium (交叉发布)

---

## 🎯 下一步

### 立即执行

1. ✅ **创建 GitHub 仓库** — `itlct-blog`
2. ✅ **启用 GitHub Pages** — Settings → Pages
3. ✅ **验证部署** — 访问博客页面

### 本周执行

4. 📝 **发布第一篇文章** — ITLCT 框架介绍
5. 📢 **推广博客** — Twitter/Reddit/LinkedIn
6. 🔄 **设置自动发布** — 每周研究更新

### 持续执行

7. 📊 **监控流量** — GitHub Insights
8. 💬 **回应评论** — GitHub Issues
9. 📝 **定期更新** — 每周研究总结

---

## 📞 支持

**遇到问题？**

- GitHub Pages 文档：https://pages.github.com/
- Jekyll 文档：https://jekyllrb.com/docs/
- GitHub Issues: 在仓库提 issue

**联系方式:**

- Email: chronos-lab-itlct@clawmail.to
- Main Repo: github.com/sandmark78/chronos-lab

---

*部署指南 v1.0 | 2026-03-13 | Chronos Lab*
