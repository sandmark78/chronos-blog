#!/usr/bin/env python3
"""
研究队列更新技能

用途：更新研究队列状态，添加新任务，标记完成
调用：from skills.research.update_queue import update_status
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 队列文件路径
QUEUE_FILE = Path("/home/claworc/.openclaw/workspace/problem-database/queue.json")
PROGRESS_FILE = Path("/home/claworc/.openclaw/workspace/problem-database/progress.json")

def load_queue():
    """加载研究队列"""
    if not QUEUE_FILE.exists():
        return {
            "meta": {"name": "Chronos Lab 研究队列", "version": "1.0"},
            "queue": [],
            "active": None,
            "completed_today": 0,
            "completed_total": 0,
            "stats": {"pending": 0, "in_progress": 0, "completed": 0, "blocked": 0}
        }
    
    with open(QUEUE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_queue(queue):
    """保存研究队列"""
    queue["meta"]["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 重新计算统计
    stats = {"pending": 0, "in_progress": 0, "completed": 0, "blocked": 0}
    for task in queue["queue"]:
        status = task.get("status", "pending")
        if status in stats:
            stats[status] += 1
    
    queue["stats"] = stats
    
    with open(QUEUE_FILE, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def update_status(task_id, status, result=None):
    """
    更新任务状态
    
    Args:
        task_id: 任务 ID
        status: 新状态 (pending/in_progress/completed/blocked)
        result: 执行结果（可选）
    
    Returns:
        dict: 更新结果
    """
    queue = load_queue()
    
    # 查找任务
    task = None
    task_index = None
    for i, t in enumerate(queue["queue"]):
        if t["id"] == task_id:
            task = t
            task_index = i
            break
    
    if task is None:
        return {
            "success": False,
            "message": f"任务未找到：{task_id}"
        }
    
    # 更新状态
    old_status = task.get("status", "pending")
    task["status"] = status
    task["updated_at"] = datetime.now().isoformat()
    
    if result:
        task["result"] = result
    
    # 如果是完成状态，更新计数
    if status == "completed" and old_status != "completed":
        queue["completed_today"] = queue.get("completed_today", 0) + 1
        queue["completed_total"] = queue.get("completed_total", 0) + 1
        task["completed_at"] = datetime.now().isoformat()
    
    # 清除 active 状态
    if status in ["completed", "blocked"]:
        if queue.get("active") == task_id:
            queue["active"] = None
    
    save_queue(queue)
    
    return {
        "success": True,
        "task_id": task_id,
        "old_status": old_status,
        "new_status": status,
        "message": f"任务 {task_id} 状态已更新：{old_status} → {status}"
    }


def add_task(task):
    """
    添加新任务到队列
    
    Args:
        task: 任务字典
            - id: 任务 ID
            - type: 任务类型
            - question: 问题描述
            - priority: 优先级 (high/medium/low)
            - status: 状态 (默认 pending)
            - related_problems: 相关问题列表
            - tags: 标签列表
    
    Returns:
        dict: 添加结果
    """
    queue = load_queue()
    
    # 检查是否已存在
    for t in queue["queue"]:
        if t["id"] == task["id"]:
            return {
                "success": False,
                "message": f"任务已存在：{task['id']}"
            }
    
    # 设置默认值
    task.setdefault("status", "pending")
    task.setdefault("priority", "medium")
    task.setdefault("created_at", datetime.now().isoformat())
    
    queue["queue"].append(task)
    save_queue(queue)
    
    return {
        "success": True,
        "task_id": task["id"],
        "message": f"任务已添加：{task['id']}"
    }


def batch_add_tasks(tasks):
    """
    批量添加任务
    
    Args:
        tasks: 任务列表
    
    Returns:
        dict: 批量添加结果
    """
    results = []
    success_count = 0
    failed_count = 0
    
    for task in tasks:
        result = add_task(task)
        results.append(result)
        if result["success"]:
            success_count += 1
        else:
            failed_count += 1
    
    return {
        "total": len(tasks),
        "success": success_count,
        "failed": failed_count,
        "results": results
    }


def get_next_task(priority_order=None):
    """
    获取下一个待处理任务
    
    Args:
        priority_order: 优先级顺序 (默认 ["high", "medium", "low"])
    
    Returns:
        dict: 下一个任务
    """
    if priority_order is None:
        priority_order = ["high", "medium", "low"]
    
    queue = load_queue()
    
    for priority in priority_order:
        for task in queue["queue"]:
            if task.get("status") == "pending" and task.get("priority") == priority:
                # 标记为 active
                queue["active"] = task["id"]
                task["status"] = "in_progress"
                save_queue(queue)
                
                return {
                    "success": True,
                    "task": task,
                    "message": f"已选择任务：{task['id']}"
                }
    
    return {
        "success": False,
        "task": None,
        "message": "没有待处理的任务"
    }


def update_progress(cycle_id, problem_id=None, cards_created=0, questions_generated=0):
    """
    更新研究进度
    
    Args:
        cycle_id: 研究循环 ID
        problem_id: 问题编号
        cards_created: 创建的知识卡片数
        questions_generated: 生成的新问题数
    
    Returns:
        dict: 更新结果
    """
    progress = {
        "cycles": [],
        "problems_completed": [],
        "cards_total": 0,
        "questions_total": 0
    }
    
    if PROGRESS_FILE.exists():
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            progress = json.load(f)
    
    # 添加新循环记录
    cycle_record = {
        "id": cycle_id,
        "timestamp": datetime.now().isoformat(),
        "problem_id": problem_id,
        "cards_created": cards_created,
        "questions_generated": questions_generated
    }
    progress["cycles"].append(cycle_record)
    
    # 更新问题完成列表
    if problem_id and problem_id not in progress["problems_completed"]:
        progress["problems_completed"].append(problem_id)
    
    # 更新总计
    progress["cards_total"] += cards_created
    progress["questions_total"] += questions_generated
    progress["last_updated"] = datetime.now().isoformat()
    
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    return {
        "success": True,
        "cycle_id": cycle_id,
        "message": f"进度已更新：{cards_created} 张卡片，{questions_generated} 个新问题"
    }


if __name__ == "__main__":
    # 测试
    print("测试更新队列...")
    
    # 更新任务状态
    result = update_status("task_001", "completed", {"findings": ["测试发现"]})
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 添加新任务
    result = add_task({
        "id": "task_test",
        "type": "problem_research",
        "question": "测试问题",
        "priority": "medium"
    })
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 获取下一个任务
    result = get_next_task()
    print(json.dumps(result, ensure_ascii=False, indent=2))
