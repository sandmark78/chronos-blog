# Chronos Lab 研究技能库

> "避免重复造轮子 - 可复用研究组件"

**版本：** v1.0  
**创建日期：** 2026-03-11

---

## 技能列表

| 技能 | 用途 | 调用方式 |
|------|------|----------|
| `create_knowledge_card` | 创建知识卡片 | Python API |
| `generate_research_log` | 生成研究日志 | Python API |
| `update_queue_status` | 更新队列状态 | Python API |
| `derive_new_questions` | 衍生新问题 | Python API |
| `link_knowledge` | 建立知识关联 | Python API |
| `search_arxiv` | arXiv 论文搜索 | CLI / Python |
| `generate_progress_report` | 生成进度报告 | Python API |
| `analyze_paper_batch` | 批量论文分析 | Python API |

---

## 使用示例

### 创建知识卡片

```python
from skills.research.create_knowledge_card import create_card

create_card(
    title="熵增原理",
    category="时间",
    content={
        "定义": "孤立系统的熵永不减少",
        "关键观点": ["..."],
        "相关理论": ["热力学第二定律"],
        "关联问题": ["问题 #3"]
    },
    sources=["..."]
)
```

### 生成研究日志

```python
from skills.research.generate_research_log import generate_log

generate_log(
    cycle_id="cycle_001",
    problem="为什么时间只有一个方向？",
    findings=["..."],
    new_hypotheses=["..."],
    new_questions=["..."],
    cards_created=["..."]
)
```

### 更新队列

```python
from skills.research.update_queue import update_status

update_status(
    task_id="task_001",
    status="completed",
    add_tasks=[{"id": "task_009", "question": "..."}]
)
```

---

## 技能位置

```
skills/research/
├── README.md                      # 本文件
├── create_knowledge_card.py       # 知识卡片创建
├── generate_research_log.py       # 研究日志生成
├── update_queue.py                # 队列状态更新
├── derive_new_questions.py        # 新问题衍生
├── link_knowledge.py              # 知识关联建立
├── search_arxiv.py                # arXiv 搜索
├── generate_progress_report.py    # 进度报告生成
└── analyze_paper_batch.py         # 批量论文分析
```

---

## 设计原则

1. **单一职责** — 每个技能只做一件事
2. **可组合** — 技能可以链式调用
3. **幂等性** — 重复调用不会产生副作用
4. **自包含** — 不依赖外部状态
5. **可测试** — 每个技能都有单元测试

---

**状态：** 🟢 技能库已创建
**下一步：** 逐步将重复工作封装成技能
