# Chronos Lab 研究循环执行指南

> "24/7 自主研究循环操作手册"

---

## 研究循环 6 阶段

```
问题发现 → 信息搜索 → 研究分析 → 理论推演 → 知识固化 → 新问题生成
   ↑                                                        ↓
   └────────────────────────────────────────────────────────┘
```

---

## 阶段 1：问题发现 (Chronos)

**输入：** problem-database/queue.json

**操作：**
1. 读取研究队列
2. 选择最高优先级任务
3. 判断任务类型
4. 分配给对应 Agent

**任务类型：**
- `problem_research` → Hermes + Athena
- `literature_search` → Hermes
- `conflict_resolution` → Athena + Prometheus
- `theory_synthesis` → Prometheus + Mnemosyne

---

## 阶段 2：信息搜索 (Hermes)

**输入：** 研究问题/搜索关键词

**操作：**
```bash
./scrapling_env/bin/python skills/scrapling_search/search.py "<query>" arxiv 10
```

**输出：**
- 论文列表（标题、作者、摘要、链接）
- 保存到 `problem-database/outputs/literature/`

**示例：**
```json
{
  "query": "arrow of time entropy",
  "papers": [
    {
      "title": "...",
      "authors": "...",
      "abstract": "...",
      "arxiv_id": "...",
      "pdf_link": "..."
    }
  ]
}
```

---

## 阶段 3：研究分析 (Athena)

**输入：** 论文列表 + 研究问题

**操作：**
1. 解析每篇论文的核心观点
2. 发现理论之间的矛盾
3. 提出新假设

**输出结构：**
```markdown
## 问题分析
[问题本质]

## 现有理论
[理论梳理]

## 关键矛盾
[矛盾点]

## 新假设
[假设内容]

## 验证方向
[如何验证]
```

---

## 阶段 4：理论推演 (Prometheus)

**输入：** 分析报告 + 相关知识卡片

**操作：**
1. 进行思想实验
2. 跨学科连接
3. 提出新理论框架

**输出结构：**
```markdown
## 核心洞见
[一句话概括]

## 详细阐述
[展开论述]

## 与现有理论的关系
- 继承：[保留了什么]
- 突破：[改变了什么]
- 预测：[新的可验证预测]

## 思想实验
[设计实验]

## 未来研究方向
1. [方向 1]
2. [方向 2]
```

---

## 阶段 5：知识固化 (Mnemosyne)

**输入：** 研究成果

**操作：**
1. 提取核心概念
2. 生成知识卡片
3. 建立知识关联
4. 更新知识图谱

**知识卡片格式：**
```markdown
---
title: [概念名]
category: [分类]
tags: [标签]
created: YYYY-MM-DD
sources: [引用]
related: [[相关概念]]
---

## 定义
[简洁解释]

## 关键观点
- 观点 1
- 观点 2

## 相关理论
- [[理论 1]]

## 开放问题
[未解决的问题]
```

**保存位置：** `knowledge/[category]/[name].md`

---

## 阶段 6：新问题生成 (Prometheus + Chronos)

**输入：** 研究成果 + 知识卡片

**操作：**
1. 识别未解决的问题
2. 发现新的理论矛盾
3. 生成新问题
4. 加入研究队列

**新问题示例：**
```
如果生命是耗散结构，那么是否所有能量梯度都会产生生命？
```

**加入队列：**
```json
{
  "id": "task_009",
  "type": "problem_research",
  "question": "是否所有能量梯度都会产生生命？",
  "priority": "medium",
  "status": "pending"
}
```

---

## 研究日志记录 (Daedalus)

**每次研究结束生成：**

```markdown
# YYYY-MM-DD HH:MM:SS 研究日志

## 研究问题
[问题描述]

## 研究材料
- 论文 ×N: [列表]
- 理论 ×N: [列表]

## 关键发现
1. [发现 1]
2. [发现 2]

## 理论推演
[推理过程]

## 新假设
[假设内容]

## 新问题
[生成的问题]

## 知识固化
- 新增卡片：[[概念名]]
- 更新关联：[[A]] → [[B]]

## 下一步
[后续研究方向]
```

**保存位置：** `knowledge/研究日志/YYYY-MM-DD.md`

---

## 完整执行示例

### 任务：研究"宇宙初始为什么低熵？"

**阶段 1 - Chronos:**
```
读取 queue.json → 选择 task_002 → 分配给 Hermes
```

**阶段 2 - Hermes:**
```bash
./scrapling_env/bin/python skills/scrapling_search/search.py "cosmic initial low entropy" arxiv 10
```
输出：10 篇相关论文

**阶段 3 - Athena:**
- 分析 10 篇论文
- 发现矛盾：暴胀理论 vs 热力学
- 提出假设：宇宙初始条件是选择效应

**阶段 4 - Prometheus:**
- 思想实验：多重宇宙中的熵分布
- 新理论：人择原理 + 熵选择

**阶段 5 - Mnemosyne:**
- 创建卡片：[[宇宙初始条件]]
- 创建卡片：[[人择原理]]
- 更新关联：[[熵增]] → [[宇宙初始条件]]

**阶段 6 - 新问题:**
```
问题：多重宇宙中是否每个宇宙都有不同的初始熵？
→ 加入 queue.json
```

**日志：**
```
knowledge/研究日志/2026-03-11.md
```

---

## Cron 配置

### 每日研究循环

```bash
openclaw cron add \
  --name "research-loop-morning" \
  --description "晨间深度研究" \
  --cron "0 9 * * *" \
  --tz "Asia/Shanghai" \
  --session "isolated" \
  --message "执行 Chronos Lab 研究循环：读取 problem-database/queue.json，选择最高优先级任务，完成 6 阶段研究流程，更新结果到知识库" \
  --timeout-seconds 600 \
  --thinking off

openclaw cron add \
  --name "research-loop-afternoon" \
  --description "午后文献搜索" \
  --cron "0 14 * * *" \
  --tz "Asia/Shanghai" \
  --session "isolated" \
  --message "执行 Hermes 文献搜索：从 queue.json 读取 literature_search 任务，搜索 arXiv 最新论文，保存结果" \
  --timeout-seconds 300 \
  --thinking off

openclaw cron add \
  --name "research-log-daily" \
  --description "每日研究日志" \
  --cron "0 23 * * *" \
  --tz "Asia/Shanghai" \
  --session "isolated" \
  --message "生成当日研究日志：总结今日完成的研究任务、新增知识卡片、生成的新问题，保存到 knowledge/研究日志/" \
  --timeout-seconds 300 \
  --thinking off
```

### 每周研究总结

```bash
openclaw cron add \
  --name "research-weekly-summary" \
  --description "每周研究总结" \
  --cron "0 20 * * 0" \
  --tz "Asia/Shanghai" \
  --session "isolated" \
  --message "生成本周研究总结：统计本周完成的任务数、新增知识卡片数、生成的新问题，更新 problem-database/progress.json" \
  --timeout-seconds 600 \
  --thinking off
```

---

## 系统监控

### 检查研究队列

```bash
cat problem-database/queue.json | jq '.stats'
```

### 查看研究日志

```bash
ls -la knowledge/研究日志/
```

### 知识卡片统计

```bash
find knowledge/ -name "*.md" | wc -l
```

---

## 故障排除

### 问题：队列卡住

**检查：**
```bash
cat problem-database/queue.json | jq '.active'
```

**解决：**
```json
{
  "active": null  // 重置为 null
}
```

### 问题：知识卡片重复

**检查：**
```bash
find knowledge/ -name "*[概念名]*"
```

**解决：** 合并重复卡片

---

## 最佳实践

1. **优先级管理** — 高优先级问题优先处理
2. **上下文管理** — 单次研究不超过 300K tokens
3. **知识关联** — 每张卡片至少关联 2 个相关概念
4. **日志完整** — 每次研究必须生成日志
5. **问题闭环** — 每个问题必须有结论或新问题

---

**状态：** 🟢 研究循环指南已创建
**版本：** v1.0
**下一步：** 配置 Cron 任务 + 启动首次研究循环

🕗 **Chronos Lab Research Loop**
