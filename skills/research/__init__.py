# Chronos Lab 研究技能库

"""
可复用的研究组件，避免重复造轮子

技能列表:
- create_knowledge_card: 创建知识卡片
- generate_research_log: 生成研究日志
- update_queue: 更新研究队列
- derive_new_questions: 衍生新问题
- link_knowledge: 建立知识关联
- generate_progress_report: 生成进度报告
"""

from .create_knowledge_card import create_card, batch_create_cards
from .generate_research_log import generate_log, generate_daily_summary
from .update_queue import (
    update_status, add_task, batch_add_tasks,
    get_next_task, update_progress
)
from .derive_new_questions import (
    derive_questions, derive_from_knowledge_conflict,
    derive_from_paper_insights, prioritize_questions
)
from .link_knowledge import (
    link_concepts, build_knowledge_graph, export_knowledge_graph
)
from .generate_progress_report import (
    generate_daily_report, generate_weekly_report, save_report
)

__all__ = [
    'create_card', 'batch_create_cards',
    'generate_log', 'generate_daily_summary',
    'update_status', 'add_task', 'batch_add_tasks', 'get_next_task', 'update_progress',
    'derive_questions', 'derive_from_knowledge_conflict', 'derive_from_paper_insights', 'prioritize_questions',
    'link_concepts', 'build_knowledge_graph', 'export_knowledge_graph',
    'generate_daily_report', 'generate_weekly_report', 'save_report'
]

__version__ = '1.0.0'
