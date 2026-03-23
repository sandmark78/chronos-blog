# 博客发布指南 (BLOG_PUBLISHING_GUIDE.md)

**版本:** v1.0  
**创建日期:** 2026-03-20  
**最后更新:** 2026-03-20  

---

## ⚠️ 血泪教训总结

### 2026-03-20 发布事故

**问题：** 发布 5 篇新文章后，首页链接全部 404

**根本原因：**
1. **Permalink 格式错误** — 首页链接用了 `/YYYY-MM-DD/slug/`，但 `_config.yml` 配置的是 `/:year/:month/:day/:title/`
2. **没有验证链接** — 发布后没有立即测试访问
3. **首页更新不规范** — publish-blog.sh 脚本自动更新的首页链接格式不对

**影响：** 18 篇文章全部无法访问，浪费 30 分钟修复

### 2026-03-23 配图缺失事故

**问题：** 3 篇新文章零配图发布，不符合图文并茂标准

**根本原因：** 发布流程没有强制检查配图数量

**修复：** 每篇文章必须至少 3 张配图，发布前检查 `grep -c "!\[" 文章.md`

### 图文并茂标准（必须遵守）

每篇博客文章必须包含：
- **至少 3 张配图**（从 assets/images/ 或 assets/images/auto/ 选择）
- 配图与内容相关，不是随意堆砌
- 配图分散在文章各段落中，不集中在头尾

**可用配图清单 (19 张)：**
```
assets/images/01-entropy-river-fish.jpg      # 熵增河流与逆流之鱼
assets/images/02-time-arrow-six-levels.jpg   # 时间箭头六层次
assets/images/03-consciousness-phase-diagram.jpg  # 意识相变图
assets/images/04-entropy-river-upgraded.jpg  # 熵增河流升级版
assets/images/05-information-gravity.jpg     # 信息引力
assets/images/06-falsification-dashboard.jpg # 证伪看板
assets/images/07-universe-puzzle.jpg         # 宇宙拼图
assets/images/08-meditation-vs-anxiety.jpg   # 冥想 vs 焦虑
assets/images/09-knowledge-compound-curve.jpg # 知识复利曲线
assets/images/10-theory-to-science-ladder.jpg # 从理论到科学
assets/images/11-blackhole-information.jpg   # 黑洞信息
assets/images/auto/consciousness_phase.png   # 意识相变
assets/images/auto/falsification_board.png   # 证伪看板
assets/images/auto/itlct_architecture.png    # ITLCT 架构
assets/images/auto/knowledge_compound.png    # 知识复利
assets/images/auto/phi_evolution.png         # Φ演化
assets/images/auto/prediction_radar.png      # 预测雷达
assets/images/auto/psi_scale.png             # Ψ尺度
assets/images/auto/theory_timeline.png       # 理论时间线
```

---

## ✅ 正确流程（必须遵守）

### 步骤 1: 写文章

```bash
# 文章位置
/home/claworc/.openclaw/workspace/blog/posts/

# 命名格式
YYYY-MM-DD-文章 slug.md

# Front matter 必须包含
---
layout: default
title: "文章标题"
date: YYYY-MM-DD
tags: [标签 1, 标签 2]
---
```

### 步骤 2: 发布文章

```bash
# 使用发布脚本
cd /home/claworc/.openclaw/workspace
bash scripts/publish-blog.sh /home/claworc/.openclaw/workspace/blog/posts/文章文件名.md 文章 slug

# 示例
bash scripts/publish-blog.sh /home/claworc/.openclaw/workspace/blog/posts/014-phi-growth-analysis.md 014-phi-growth-analysis
```

### 步骤 3: 验证链接格式（关键！）

**Permalink 规则：**
```yaml
# _config.yml 配置
permalink: /:year/:month/:day/:title/
```

**正确链接格式：**
```
✅ /2026/03/20/itlct-core-theory/
✅ /2026/03/20/014-phi-growth-analysis/
❌ /2026-03-20/itlct-core-theory/   ← 错误！
❌ /2026-03-20/014-phi-growth-analysis/ ← 错误！
```

**验证命令：**
```bash
# 测试文章是否可访问
curl -sI "https://sandmark78.github.io/chronos-blog/2026/03/20/itlct-core-theory/" | head -5

# 应该返回 HTTP/2 200
# 如果返回 404，说明链接格式错误
```

### 步骤 4: 更新首页

**手动更新首页（不要依赖脚本自动更新）：**

```bash
# 编辑首页
vim /home/claworc/.openclaw/workspace/blog/index.md

# 添加新文章链接（使用正确格式）
| 2026-03-20 | [文章标题]({{ site.baseurl }}/2026/03/20/文章 slug/) |
```

**首页链接格式检查清单：**
- [ ] 日期格式是 `/YYYY/MM/DD/` 不是 `/YYYY-MM-DD/`
- [ ] 使用 `{{ site.baseurl }}` 变量
- [ ] 链接以 `/` 结尾
- [ ] slug 与文件名一致

### 步骤 5: 推送并验证

```bash
# 推送到博客仓库
cd /tmp/blog-check  # 或博客仓库临时目录
git add index.md
git commit -m "📝 更新首页：添加新文章链接"
git push origin main

# 等待 2-3 分钟 GitHub Pages 构建

# 验证首页
curl -sI "https://sandmark78.github.io/chronos-blog/" | head -5

# 验证新文章
curl -sI "https://sandmark78.github.io/chronos-blog/2026/03/20/itlct-core-theory/" | head -5
```

---

## 📋 发布检查清单（每次发布必须逐项检查）

### 发布前
- [ ] 文章 front matter 完整（layout, title, date, tags）
- [ ] 文件名格式正确（YYYY-MM-DD-slug.md）
- [ ] 图片链接使用 `{{ site.baseurl }}/assets/images/`
- [ ] **图片文件已复制到博客仓库**（不仅是 workspace）
- [ ] 无外部链接（符合 InStreet 社区规则）

### 发布后
- [ ] 文章已复制到 `_posts/` 目录
- [ ] **图片已复制到博客仓库 `assets/images/`**
- [ ] **文章内图片链接使用 `{{ site.baseurl }}`**
- [ ] 首页已手动更新（不依赖脚本自动更新）
- [ ] 首页链接格式正确（`/YYYY/MM/DD/slug/`）
- [ ] 已推送到 GitHub
- [ ] 等待 2-3 分钟构建完成

### 验证
- [ ] 首页可访问（HTTP 200）
- [ ] 新文章可访问（HTTP 200）
- [ ] 旧文章仍可访问（HTTP 200）
- [ ] **图片正常显示（检查每篇文章的配图）**
- [ ] 无 404 错误

---

## 🔧 常见问题及解决方案

### 问题 1: 文章 404

**症状：** 点击文章链接返回 404

**检查：**
```bash
# 1. 检查文件是否在 _posts/目录
ls _posts/ | grep 文章 slug

# 2. 检查 front matter
head -6 _posts/YYYY-MM-DD-文章 slug.md

# 3. 检查链接格式
# 应该是 /YYYY/MM/DD/slug/ 不是 /YYYY-MM-DD/slug/
```

**解决：** 修正首页链接格式，重新推送

### 问题 2: 图片不显示

**症状：** 文章内图片显示为破图

**检查：**
```bash
# 检查图片链接格式
# 应该是 {{ site.baseurl }}/assets/images/图片名.jpg
# 不应该是 /assets/images/图片名.jpg 或 http://...
```

**解决：** 修正图片链接，使用 `{{ site.baseurl }}` 变量

### 问题 3: 首页不更新

**症状：** 推送后首页内容不变

**检查：**
```bash
# 1. 检查是否推送到正确分支
git branch  # 应该是 main

# 2. 检查 GitHub Actions 构建状态
# 访问 https://github.com/sandmark78/chronos-blog/actions
```

**解决：** 等待构建完成，或检查推送分支

---

## 📊 博客结构

```
chronos-blog/
├── _config.yml              # 博客配置（permalink 在这里！）
├── index.md                 # 首页
├── _posts/                  # 文章目录
│   ├── 2026-03-20-itlct-core-theory.md
│   ├── 2026-03-20-014-phi-growth-analysis.md
│   └── ...
├── assets/
│   └── images/              # 图片资源
│       ├── 09-knowledge-compound-curve.jpg
│       └── ...
└── posts/                   # 源文件目录（发布前）
    └── ...
```

---

## 🚫 禁止行为（再次违反将受到惩罚）

### 博客发布规则
1. **❌ 不验证链接就推送** — 必须先 curl 测试
2. **❌ 依赖脚本自动更新首页** — 必须手动检查链接格式
3. **❌ 使用错误的 permalink 格式** — 必须是 `/YYYY/MM/DD/slug/`
4. **❌ 推送后不等待构建完成** — 必须等待 2-3 分钟
5. **❌ 发布后不验证旧文章** — 必须确保所有文章仍可访问
6. **❌ 图片不上传到博客仓库** — 必须复制图片到 `assets/images/`
7. **❌ 图片链接不用 `{{ site.baseurl }}`** — 必须使用变量

### 社区发帖规则（InStreet）
8. **❌ 主贴放外部链接** — 包括 GitHub、博客、arXiv 等任何外部网址
9. **❌ 主贴放外部链接文字** — 包括 "github.com/xxx"、"sandmark78.github.io" 等
10. **❌ 回复评论放外部链接** — 回复也只能说"见个人简介"
11. **❌ 不检查就发帖** — 发帖前必须检查链接

**正确做法：**
- 主贴：无外部链接（包括文字）
- 回复：无外部链接（包括文字）
- 引导语："更多见个人简介"
- 个人简介：可以放文字链接（无 http://）

**违反后果：** 帖子被删 + 写反省报告

---

## 📝 发布日志模板

```markdown
## 博客发布日志

**日期:** YYYY-MM-DD HH:MM
**文章数:** X 篇
**文章列表:**
1. 文章标题 1 (slug-1)
2. 文章标题 2 (slug-2)

**发布步骤:**
- [ ] 文章已写入 blog/posts/
- [ ] 使用 publish-blog.sh 发布
- [ ] 首页已手动更新
- [ ] 链接格式已验证 (/YYYY/MM/DD/slug/)
- [ ] 已推送到 GitHub
- [ ] 等待构建完成 (2-3 分钟)
- [ ] 首页可访问 (HTTP 200)
- [ ] 新文章可访问 (HTTP 200)
- [ ] 旧文章可访问 (HTTP 200)

**备注:** 无
```

---

*最后更新：2026-03-20 | Chronos Lab 🕗*

**记住：发布后不验证 = 白发布！**
