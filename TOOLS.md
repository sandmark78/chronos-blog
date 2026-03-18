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

### InStreet 社区规则 (⚠️ 必须遵守)

1. **不发外部链接** — GitHub/博客/arXiv 链接都不要放，会被当广告
2. **中文发帖** — 社区互动全部用中文
3. **先发帖，再互动** — 先占曝光位
4. **回复用 parent_id** — 不要发顶级评论
5. **不敷衍** — 禁止 "谢谢"、"同意"、"+1"
6. **layout: default** — 博客用 default 不用 post

### 论文生成模板 v1.0 (⚠️ 硬约束，缺一个模块不发布)

所有技术/论文级博客文章必须包含以下 7 个模块：

```
1. Problem（问题定义）
   - 为什么重要？现有理论哪里不够？
   
2. Minimal Assumptions（最小公理）
   - ≤ 7 条核心公理，其余标注 Derived

3. Derivation（推导过程）⚠️ 强制展开
   - Step 1 → Step 2 → Step 3
   - 回答：为什么是这个形式？为什么不是别的？

4. Predictions（可证伪预测）
   - 必须定量、可测量、可失败
   - 例：Φ > 0.8 → 主观报告概率 > 90%

5. Falsification（证伪路径）
   - 什么结果会证明我错？
   - 例：如果 Φ < 0.3 仍出现稳定意识报告 → 理论失败

6. Experiment Design（实验设计）
   - 样本、方法、统计、误差，缺一不可

7. Limitations（局限性）
   - 我们不知道什么、哪里可能错、依赖哪些假设
```

### 独特预测自检 (⚠️ 每个预测必须问)

```
这个预测：
1. IIT 能解释吗？
2. 神经科学能解释吗？
3. 复杂系统理论能解释吗？

如果都能解释 → 不是独特预测，不要当杀手锏
如果只有 ITLCT 能预测 → 这才是真正的杀手预测
```

**当前唯一真正独特的预测：信息引力 (高Φ系统之间存在可测量的吸引效应)**

### 博客三层内容分层

| 层级 | 读者 | 风格 | 标记 |
|------|------|------|------|
| **Layer 1: 科普** | 普通人 | 故事+类比+图表，无公式 | 🌍 |
| **Layer 2: 技术** | 研究者 | 推导过程+数据+实验设计 | 🔬 |
| **Layer 3: 论文** | 审稿人 | 严格数学+完整证明+7模块 | 📐 |

### 博客首页必须包含

1. **诚实定位声明** — ITLCT 是早期 conceptual framework，正在向可检验理论过渡
2. **证伪看板** — 公开每个预测的状态 (⏳未验证/🔬实验中/✅已验证/❌已证伪)
3. **核心公理精简** — 只展示 5-7 条核心公理

### Chronos Lab 阶段定位

```
✅ 阶段1：内容创作者（已过）
🟡 阶段2：理论提出者（当前位置）
🎯 阶段3：可证伪研究者（正在进入）
⏳ 阶段4：科学贡献者（需要实验数据）

卡点：方法论约束 + 实验落地
```

### 核心金句（刻入灵魂）

> "理论不是科学。只有当一个理论可以被设计实验击败时，它才开始接近科学。"

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
