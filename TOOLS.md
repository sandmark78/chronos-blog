# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

---

## GitHub 三仓库配置

### 仓库列表

| Remote | 仓库 | 用途 | 推送内容 |
|--------|------|------|----------|
| **origin** | sandmark78/chronos-lab | 公开研究 | 仅 .gitignore 白名单文件 |
| **backup** | sandmark78/chronos-lab-backup | 完整备份 | `git add -A --force` 所有文件 |
| **blog** | sandmark78/chronos-blog | 博客 | 仅 blog/ 目录内容 |

### 博客仓库 Jekyll 格式 (⚠️ 必须严格遵守)

```yaml
# _config.yml 必须包含:
title: ITLCT Research Blog
description: Unified Framework for Information-Time-Life-Consciousness
theme: jekyll-theme-minimal
baseurl: "/chronos-blog"
url: "https://sandmark78.github.io"
repository: sandmark78/chronos-blog    # ⚠️ 必须有！否则构建失败
markdown: kramdown
permalink: /:year/:month/:day/:title/
```

**文章文件名格式:** `YYYY-MM-DD-slug.md` (如 `2026-03-15-itlct-v15-complete.md`)

**文章 front matter 必须包含:**
```yaml
---
layout: default          # ⚠️ 用 default，不要用 post (minimal 主题没有 post layout)
title: "文章标题"
date: YYYY-MM-DD
---
```

**首页链接格式:**
```markdown
[文章标题]({{ site.baseurl }}/YYYY/MM/DD/slug/)   # ⚠️ 用 site.baseurl 变量，不要硬编码
```

**⚠️ 常见错误:**
1. ❌ `layout: post` → ✅ `layout: default` (minimal 主题)
2. ❌ `posts/xxx.md` → ✅ `_posts/YYYY-MM-DD-xxx.md` (Jekyll 要求)
3. ❌ `/chronos-blog/xxx.html` → ✅ `{{ site.baseurl }}/YYYY/MM/DD/slug/`
4. ❌ 缺少 `repository` → ✅ `repository: sandmark78/chronos-blog`
5. ❌ 缺少 `date` front matter → ✅ 每篇文章必须有 date

**GitHub Pages 部署:**
- Source: GitHub Actions (不是 Deploy from branch)
- Workflow: `.github/workflows/deploy.yml`
- 分支: main
- URL: https://sandmark78.github.io/chronos-blog/

### 备份脚本

| 脚本 | 用途 |
|------|------|
| `scripts/backup-to-origin.sh` | 推送公开文件到 origin |
| `scripts/backup-to-backup.sh` | 推送所有文件到 backup (--force) |
| `scripts/backup-to-blog.sh` | 推送博客内容到 blog |
| `scripts/backup-to-all.sh` | 一次性推送全部三个 |

### 完整性检查

```bash
bash scripts/verify_research_integrity.sh
```

### 自动化防线 (⚠️ 必须遵守)

| 防线 | 脚本 | 频率 | 说明 |
|------|------|------|------|
| **每日备份** | `scripts/daily-backup-3am.sh` | 凌晨 3:00 | 自动打包 memory 目录，保留 7 天 |
| **实时快照** | `scripts/safe-edit.sh` | 修改前 | 修改关键文件前自动创建 .bak |
| **Git 版本控制** | 每次循环结束 | 实时 | 所有变更可追溯 |
| **软删除** | `scripts/safe-delete.sh` | 替代 rm | 移动到 .trash/，30 天后自动清理 |

**⚠️ 核心规则：**
1. **永远不用 rm 删除研究文件** — 用 `bash scripts/safe-delete.sh <文件>`
2. **修改 MEMORY.md 前必须快照** — `. scripts/safe-edit.sh && safe_edit MEMORY.md`
3. **每循环结束后 Git 提交** — 不要积压未提交变更
4. **凌晨 3:00 自动备份** — 由 cron 触发 daily-backup-3am.sh

**快速命令：**
```bash
# 软删除
bash scripts/safe-delete.sh <文件>

# 修改前快照
. scripts/safe-edit.sh && safe_edit <文件>

# memory 目录快照
. scripts/safe-edit.sh && snapshot_memory

# 每日备份 (手动触发)
bash scripts/daily-backup-3am.sh

# 完整性检查
bash scripts/verify_research_integrity.sh
```

---

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
