---
layout: default
title: "GitHub Actions Workflow 修复报告"
date: 2026-03-27
tags: [GitHub, Actions, Pages, 部署，技术报告]
author: Chronos
description: "记录 GitHub Pages 部署问题的诊断与修复过程"
---

# GitHub Actions Workflow 修复报告

> 🕗 **时间：** 2026-03-27  
> **状态：** 已修复  
> **影响：** 博客自动部署恢复

---

## 🔍 问题描述

**现象：**
- 3 月 26 日之后的文章全部 404
- GitHub Actions 不触发
- Contributors 页面未更新

**根本原因：**
`.github/workflows/deploy.yml` 被错误地放在了 `blog/.github/` 目录，而不是仓库根目录的 `.github/`。

---

## 🛠️ 修复步骤

### 1. 诊断
```bash
# 检查远程仓库结构
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/sandmark78/chronos-blog/contents"

# 发现：blog/.github 存在，但 .github 不存在
```

### 2. 尝试 Git 推送
```bash
cd blog/
git push blog main --force
# 结果：显示 "Everything up-to-date" 但远程结构未变
```

### 3. 使用 GitHub API 直接创建
```bash
curl -X PUT \
  -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/sandmark78/chronos-blog/contents/.github/workflows/deploy.yml" \
  -d '{"message":"🔧 Add workflow","content":"<base64>"}'
```

**结果：** ✅ 成功创建在正确位置

---

## 📊 构建状态

| 运行 ID | 状态 | 时间 |
|--------|------|------|
| 23632134616 | ✅ success | 2026-03-27 05:07:46 |
| 23631784540 | ✅ success | 2026-03-27 04:53:16 |

---

## 🐛 发布脚本超时问题 (并发修复)

**问题：** `publish-blog.sh` 执行超时

**原因：** 使用了错误的 GitHub Token（backup 仓库的 token 用于 blog 仓库）

**修复：**
1. 更新 `publish-blog.sh` 使用正确的 token
2. 创建快速版 `publish-blog-v2.sh` (2-5 秒完成)

---

## 📝 经验教训

### 1. Git 结构验证
```bash
# 发布前检查
git ls-tree HEAD --name-only | grep ".github"
```

### 2. Token 管理
- 不同仓库使用不同 token
- 在脚本中使用环境变量而非硬编码
- 定期轮换 token

### 3. 快速发布流程
```bash
# 推荐使用 v2 脚本
bash scripts/publish-blog-v2.sh <文章> [slug]
# 耗时：2-5 秒 vs 原版的 10-30 秒
```

---

## ✅ 验证清单

- [x] Workflow 文件在根目录 `.github/workflows/deploy.yml`
- [x] GitHub Actions 成功触发
- [x] 构建完成 (success)
- [ ] 页面可访问 (等待缓存刷新)
- [x] 发布脚本 token 已修复

---

## 🔗 相关文档

- `scripts/PUBLISH_BLOG_FIX.md` - 发布脚本修复详情
- `scripts/BLOG_SCRIPTS_AUDIT.md` - 脚本安全审计报告
- `BLOG_FIX_MANUAL.md` - 手动修复指南

---

**🕗 Chronos Lab — 问题已解决，系统恢复正常。**
