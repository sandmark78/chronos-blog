#!/usr/bin/env python3
"""
研究日志生成技能

用途：将研究循环结果固化为标准化研究日志
调用：from skills.research.generate_research_log import generate_log
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 研究日志目录
LOG_DIR = Path("/home/claworc/.openclaw/workspace/knowledge/研究日志")

def generate_log(
    cycle_id,
    problem,
    problem_id=None,
    findings=None,
    hypotheses=None,
    questions=None,
    cards_created=None,
    files_created=None,
    duration_seconds=None,
    tokens_used=None,
    quality_rating=None,
    next_task=None
):
    """
    生成研究日志
    
    Args:
        cycle_id: 研究循环 ID (如 "cycle_001")
        problem: 研究问题
        problem_id: 问题编号 (如 3)
        findings: 关键发现列表
        hypotheses: 新假设列表
        questions: 新问题列表
        cards_created: 创建的知识卡片列表
        files_created: 创建的文件列表
        duration_seconds: 执行时长 (秒)
        tokens_used: 消耗 Token 数
        quality_rating: 质量评分 (1-5 星)
        next_task: 下一步建议
    
    Returns:
        dict: 生成结果
            - success: bool
            - path: 文件路径
            - summary: 摘要
    """
    # 创建目录
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{timestamp}_{cycle_id}.md"
    filepath = LOG_DIR / filename
    
    # 生成日志内容
    content = []
    
    # 标题
    content.append(f"# 研究日志：{problem}")
    content.append("")
    content.append(f"**循环 ID:** {cycle_id}")
    content.append(f"**执行时间:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (Asia/Shanghai)")
    content.append(f"**研究者:** Chronos Lab 🕗")
    content.append("")
    
    # 执行统计
    content.append("## 执行统计")
    content.append("")
    if duration_seconds:
        minutes = duration_seconds // 60
        seconds = duration_seconds % 60
        content.append(f"- **执行时长:** {minutes}分{seconds}秒")
    if tokens_used:
        content.append(f"- **Token 消耗:** {tokens_used:,}")
    if quality_rating:
        content.append(f"- **质量评分:** {'⭐' * quality_rating}")
    content.append("")
    
    # 研究问题
    content.append("## 研究问题")
    content.append("")
    if problem_id:
        content.append(f"**问题 #{problem_id}:** {problem}")
    else:
        content.append(f"**问题:** {problem}")
    content.append("")
    
    # 关键发现
    if findings:
        content.append("## 关键发现")
        content.append("")
        for i, finding in enumerate(findings, 1):
            content.append(f"{i}. {finding}")
        content.append("")
    
    # 新假设
    if hypotheses:
        content.append("## 新假设")
        content.append("")
        for i, hyp in enumerate(hypotheses, 1):
            content.append(f"{i}. {hyp}")
        content.append("")
    
    # 新问题
    if questions:
        content.append("## 生成的新问题")
        content.append("")
        for i, q in enumerate(questions, 1):
            content.append(f"{i}. {q}")
        content.append("")
    
    # 知识固化
    if cards_created:
        content.append("## 知识卡片创建")
        content.append("")
        for card in cards_created:
            if isinstance(card, dict):
                content.append(f"- [[{card.get('title', '未知')}]] ({card.get('path', '无路径')})")
            else:
                content.append(f"- {card}")
        content.append("")
    
    # 创建的文件
    if files_created:
        content.append("## 创建的文件")
        content.append("")
        for f in files_created:
            content.append(f"- `{f}`")
        content.append("")
    
    # 下一步建议
    if next_task:
        content.append("## 下一步建议")
        content.append("")
        content.append(f"**推荐任务:** {next_task.get('problem', '未知')}")
        content.append("")
        if "reason" in next_task:
            content.append(f"**理由:** {next_task['reason']}")
        content.append("")
    
    # 核心洞见
    content.append("---")
    content.append("")
    content.append("> 💡 **核心洞见**")
    content.append(">")
    content.append(f"> {problem} — 这是探索时间本质的重要一步。")
    content.append("")
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(content))
    
    # 生成摘要
    summary = {
        "cycle_id": cycle_id,
        "problem": problem,
        "problem_id": problem_id,
        "timestamp": datetime.now().isoformat(),
        "duration_seconds": duration_seconds,
        "tokens_used": tokens_used,
        "quality_rating": quality_rating,
        "findings_count": len(findings) if findings else 0,
        "hypotheses_count": len(hypotheses) if hypotheses else 0,
        "questions_count": len(questions) if questions else 0,
        "cards_created_count": len(cards_created) if cards_created else 0,
        "files_created_count": len(files_created) if files_created else 0
    }
    
    return {
        "success": True,
        "path": str(filepath),
        "summary": summary,
        "message": f"研究日志已生成：{filepath}"
    }


def generate_daily_summary(date=None):
    """
    生成每日研究总结
    
    Args:
        date: 日期字符串 (YYYY-MM-DD)，默认为今天
    
    Returns:
        dict: 每日总结
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 查找当日所有日志
    daily_logs = []
    for log_file in LOG_DIR.glob(f"{date}*.md"):
        daily_logs.append(log_file.name)
    
    summary = {
        "date": date,
        "log_count": len(daily_logs),
        "logs": daily_logs,
        "generated_at": datetime.now().isoformat()
    }
    
    return {
        "success": True,
        "summary": summary,
        "message": f"找到 {len(daily_logs)} 篇当日研究日志"
    }


if __name__ == "__main__":
    # 测试
    result = generate_log(
        cycle_id="test_001",
        problem="测试研究问题",
        problem_id=99,
        findings=["发现 1", "发现 2"],
        hypotheses=["假设 1"],
        questions=["新问题 1", "新问题 2"],
        cards_created=[{"title": "测试卡片", "path": "knowledge/时间/测试卡片.md"}],
        duration_seconds=187,
        tokens_used=462400,
        quality_rating=4,
        next_task={"problem": "宇宙初始为什么低熵？", "reason": "直接后续问题"}
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
