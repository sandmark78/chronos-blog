#!/usr/bin/env python3
"""
进度报告生成技能

用途：生成研究进度报告（日报/周报/月报）
调用：from skills.research.generate_progress_report import generate_report
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# 文件路径
PROGRESS_FILE = Path("/home/claworc/.openclaw/workspace/problem-database/progress.json")
QUEUE_FILE = Path("/home/claworc/.openclaw/workspace/problem-database/queue.json")
LOG_DIR = Path("/home/claworc/.openclaw/workspace/knowledge/研究日志")

def generate_daily_report(date=None):
    """
    生成日报
    
    Args:
        date: 日期字符串 (YYYY-MM-DD)，默认为今天
    
    Returns:
        dict: 日报内容
    """
    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")
    
    # 查找当日日志
    daily_logs = []
    for log_file in LOG_DIR.glob(f"{date}*.md"):
        daily_logs.append(log_file.name)
    
    # 加载进度
    progress = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress = json.load(f)
    
    # 筛选当日循环
    daily_cycles = [
        c for c in progress.get("cycles", [])
        if c.get("timestamp", "").startswith(date)
    ]
    
    # 统计
    cards_today = sum(c.get("cards_created", 0) for c in daily_cycles)
    questions_today = sum(c.get("questions_generated", 0) for c in daily_cycles)
    
    # 加载队列
    queue = {}
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            queue = json.load(f)
    
    report = {
        "type": "daily",
        "date": date,
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "research_cycles": len(daily_cycles),
            "cards_created": cards_today,
            "questions_generated": questions_today,
            "logs_created": len(daily_logs),
            "tasks_completed": queue.get("completed_today", 0),
            "tasks_pending": queue.get("stats", {}).get("pending", 0)
        },
        "cycles": daily_cycles,
        "logs": daily_logs,
        "queue_status": queue.get("stats", {})
    }
    
    return {
        "success": True,
        "report": report,
        "markdown": format_report_markdown(report)
    }


def generate_weekly_report():
    """
    生成周报
    
    Returns:
        dict: 周报内容
    """
    today = datetime.now()
    week_start = today - timedelta(days=today.weekday())
    week_start = week_start.replace(hour=0, minute=0, second=0)
    
    # 加载进度
    progress = {}
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress = json.load(f)
    
    # 筛选本周循环
    weekly_cycles = [
        c for c in progress.get("cycles", [])
        if datetime.fromisoformat(c.get("timestamp", "1970-01-01")) >= week_start
    ]
    
    # 统计
    cards_week = sum(c.get("cards_created", 0) for c in weekly_cycles)
    questions_week = sum(c.get("questions_generated", 0) for c in weekly_cycles)
    problems_week = len(set(c.get("problem_id") for c in weekly_cycles if c.get("problem_id")))
    
    # 加载队列
    queue = {}
    if QUEUE_FILE.exists():
        with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
            queue = json.load(f)
    
    report = {
        "type": "weekly",
        "week_start": week_start.strftime("%Y-%m-%d"),
        "week_end": today.strftime("%Y-%m-%d"),
        "generated_at": datetime.now().isoformat(),
        "summary": {
            "research_cycles": len(weekly_cycles),
            "problems_studied": problems_week,
            "cards_created": cards_week,
            "questions_generated": questions_week,
            "tasks_completed_total": queue.get("completed_total", 0),
            "tasks_pending": queue.get("stats", {}).get("pending", 0)
        },
        "cycles": weekly_cycles,
        "progress": {
            "problems_completed": progress.get("problems_completed", []),
            "cards_total": progress.get("cards_total", 0),
            "questions_total": progress.get("questions_total", 0)
        },
        "queue_status": queue.get("stats", {})
    }
    
    return {
        "success": True,
        "report": report,
        "markdown": format_report_markdown(report)
    }


def format_report_markdown(report):
    """
    将报告格式化为 Markdown
    
    Args:
        report: 报告字典
    
    Returns:
        str: Markdown 格式的报告
    """
    lines = []
    
    # 标题
    if report["type"] == "daily":
        lines.append(f"# 研究日报 ({report['date']})")
    else:
        lines.append(f"# 研究周报 ({report['week_start']} ~ {report['week_end']})")
    
    lines.append("")
    lines.append(f"**生成时间:** {report['generated_at']}")
    lines.append("")
    
    # 摘要
    lines.append("## 摘要")
    lines.append("")
    summary = report["summary"]
    for key, value in summary.items():
        lines.append(f"- **{key}:** {value}")
    lines.append("")
    
    # 研究循环详情
    if report.get("cycles"):
        lines.append("## 研究循环")
        lines.append("")
        for cycle in report["cycles"]:
            lines.append(f"### {cycle.get('id', '未知')}")
            lines.append(f"- 问题：{cycle.get('problem', '未知')}")
            lines.append(f"- 卡片：{cycle.get('cards_created', 0)} 张")
            lines.append(f"- 问题：{cycle.get('questions_generated', 0)} 个")
            lines.append("")
    
    # 队列状态
    if report.get("queue_status"):
        lines.append("## 队列状态")
        lines.append("")
        for status, count in report["queue_status"].items():
            lines.append(f"- {status}: {count}")
        lines.append("")
    
    return "\n".join(lines)


def save_report(report, output_dir=None):
    """
    保存报告到文件
    
    Args:
        report: 报告字典
        output_dir: 输出目录
    
    Returns:
        dict: 保存结果
    """
    if output_dir is None:
        output_dir = Path("/home/claworc/.openclaw/workspace/problem-database/outputs/reports")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    report_type = report["type"]
    if report_type == "daily":
        filename = f"daily_{report['date']}.md"
    else:
        filename = f"weekly_{report['week_start']}.md"
    
    filepath = output_dir / filename
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report["markdown"])
    
    return {
        "success": True,
        "path": str(filepath),
        "message": f"报告已保存：{filepath}"
    }


if __name__ == "__main__":
    # 测试日报
    report = generate_daily_report()
    print(report["markdown"])
    
    # 保存
    result = save_report(report)
    print(json.dumps(result, ensure_ascii=False, indent=2))
