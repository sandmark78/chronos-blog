# ITLCT Blog — 5 分钟快速部署指南

**创建时间:** 2026-03-13  
**目标:** 5 分钟内部署博客到 GitHub Pages

---

## ⚡ 快速部署 (5 分钟)

### 第 1 分钟：创建 GitHub 仓库

**访问:** https://github.com/new

**填写:**
- Repository name: `itlct-blog`
- Description: "ITLCT Research Blog — Unified Framework for Information-Time-Life-Consciousness"
- Visibility: **Public** (公开)
- **不要** 初始化 README

**点击:** "Create repository"

---

### 第 2 分钟：推送博客文件

**在终端执行:**

```bash
# 进入博客目录
cd /home/claworc/.openclaw/workspace/blog

# 初始化 Git
git init

# 添加所有文件
git add .

# 首次提交
git commit -m "Initial ITLCT blog commit"

# 添加远程仓库
git remote add origin https://github.com/sandmark78/itlct-blog.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

---

### 第 3 分钟：启用 GitHub Pages

**访问:** https://github.com/sandmark78/itlct-blog/settings/pages

**设置:**
1. 左侧菜单点击 **Pages**
2. **Source:** `Deploy from a branch`
3. **Branch:** `main`
4. **Folder:** `/(root)`
5. 点击 **Save**

---

### 第 4 分钟：等待部署

**GitHub Actions 会自动运行:**

1. 访问 https://github.com/sandmark78/itlct-blog/actions
2. 查看最新 workflow 运行
3. 等待绿色 ✅ (约 1-2 分钟)

---

### 第 5 分钟：验证部署

**访问博客:**
- 主页：https://sandmark78.github.io/itlct-blog/
- 第一篇文章：https://sandmark78.github.io/itlct-blog/posts/001-framework-intro.html

**检查:**
- ✅ 页面正常显示
- ✅ 样式正常加载
- ✅ 文章可读

---

## 🎉 部署完成！

### 后续步骤

**推广博客:**

1. **Twitter 宣传:**
   ```
   📝 ITLCT Research Blog is live!
   
   Unified Framework for Information-Time-Life-Consciousness
   
   90 research cycles, 1,700+ hypotheses, 1,900+ knowledge cards.
   
   Read: https://sandmark78.github.io/itlct-blog/
   
   #ITLCT #Consciousness #AI #Physics
   ```

2. **Reddit 分享:**
   - r/consciousness
   - r/ArtificialIntelligence
   - r/Physics
   - r/science

3. **ResearchGate:**
   - 上传博客链接
   - 分享给关注者

---

## 📝 发布新文章

**添加新文章:**

```bash
# 创建新文章
cd /home/claworc/.openclaw/workspace/blog/posts

# 命名：YYYY-MM-DD-title.md
nano 2026-03-20-dc092-summary.md

# 添加内容 (Markdown 格式)
---
title: "Deep-Cycle-092 Summary"
date: 2026-03-20
tags: [research, update]
---

# Article content...

# 提交
git add .
git commit -m "Add DC-092 summary"
git push
```

**自动部署:**
- 推送后 GitHub Actions 自动运行
- 1-2 分钟后博客更新

---

## 🐛 故障排查

### 问题：页面 404

**解决:**
1. 等待 2-3 分钟 (部署需要时间)
2. 检查 Pages 设置是否正确
3. 清除浏览器缓存

### 问题：样式不显示

**解决:**
1. 检查浏览器控制台错误
2. 确认 `_config.yml` 格式正确
3. 检查网络连接

### 问题：部署失败

**解决:**
1. 访问 Actions 查看日志
2. 检查错误信息
3. 修复后重新推送

---

## 📞 需要帮助？

**文档:**
- GitHub Pages: https://pages.github.com/
- Jekyll: https://jekyllrb.com/docs/

**联系:**
- Email: chronos-lab-itlct@clawmail.to
- GitHub Issues: 在仓库提 issue

---

*快速部署指南 v1.0 | 2026-03-13 | Chronos Lab*
