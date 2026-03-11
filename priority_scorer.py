#!/usr/bin/env python3
"""
研究优先级评分器

用途：计算研究问题的优先级分数
调用：from priority_scorer import calculate_priority
"""

import json
from datetime import datetime
from pathlib import Path

# 问题数据库路径
PROBLEMS_FILE = Path("/home/claworc/.openclaw/workspace/problem-database/problems.json")

def calculate_priority(
    importance: float,
    knowledge_gap: float,
    cross_domain: float,
    novelty: float
) -> dict:
    """
    计算优先级分数
    
    Args:
        importance: 科学重要性 (0-10)
        knowledge_gap: 知识缺口 (0-10)
        cross_domain: 跨学科价值 (0-10)
        novelty: 新颖性 (0-10)
    
    Returns:
        dict: 优先级结果
    """
    # 权重
    weights = {
        'importance': 0.4,
        'knowledge_gap': 0.3,
        'cross_domain': 0.2,
        'novelty': 0.1
    }
    
    # 计算总分
    score = (
        importance * weights['importance'] +
        knowledge_gap * weights['knowledge_gap'] +
        cross_domain * weights['cross_domain'] +
        novelty * weights['novelty']
    )
    
    # 优先级分类
    if score >= 8.0:
        priority = "critical"
        description = "立即研究 - 核心问题"
    elif score >= 6.0:
        priority = "high"
        description = "高优先级 - 重要问题"
    elif score >= 4.0:
        priority = "medium"
        description = "中等优先级"
    else:
        priority = "low"
        description = "低优先级 - 可延后"
    
    return {
        'score': round(score, 2),
        'priority': priority,
        'description': description,
        'breakdown': {
            'importance': {'score': importance, 'weight': weights['importance']},
            'knowledge_gap': {'score': knowledge_gap, 'weight': weights['knowledge_gap']},
            'cross_domain': {'score': cross_domain, 'weight': weights['cross_domain']},
            'novelty': {'score': novelty, 'weight': weights['novelty']}
        }
    }


def score_problem(problem_id: int) -> dict:
    """
    为特定问题评分
    
    Args:
        problem_id: 问题编号
    
    Returns:
        dict: 评分结果
    """
    # 核心问题预定义评分
    core_problems = {
        3: {'importance': 10, 'gap': 8, 'cross': 9, 'novelty': 7},    # 时间箭头
        32: {'importance': 10, 'gap': 9, 'cross': 8, 'novelty': 8},   # 宇宙初始低熵
        35: {'importance': 9, 'gap': 8, 'cross': 9, 'novelty': 8},    # 生命低熵维持
        61: {'importance': 9, 'gap': 8, 'cross': 9, 'novelty': 9},    # 生命是信息系统
        92: {'importance': 10, 'gap': 10, 'cross': 10, 'novelty': 10}, # 时间生命意识统一
        98: {'importance': 10, 'gap': 9, 'cross': 10, 'novelty': 9},   # 信息是宇宙基础
    }
    
    if problem_id in core_problems:
        scores = core_problems[problem_id]
        result = calculate_priority(
            scores['importance'],
            scores['gap'],
            scores['cross'],
            scores['novelty']
        )
        result['problem_id'] = problem_id
        return result
    else:
        # 默认评分
        return calculate_priority(5, 5, 5, 5)


def score_all_problems() -> dict:
    """
    为所有 100 个问题评分
    
    Returns:
        dict: 所有问题的评分
    """
    results = {
        'timestamp': datetime.now().isoformat(),
        'problems': [],
        'summary': {
            'critical': 0,
            'high': 0,
            'medium': 0,
            'low': 0
        }
    }
    
    for problem_id in range(1, 101):
        result = score_problem(problem_id)
        results['problems'].append(result)
        results['summary'][result['priority']] += 1
    
    # 按分数排序
    results['problems'].sort(key=lambda x: x['score'], reverse=True)
    
    return results


def update_queue_with_priority():
    """
    更新研究队列优先级
    """
    # 加载队列
    queue_file = Path("/home/claworc/.openclaw/workspace/problem-database/queue.json")
    if not queue_file.exists():
        return
    
    with open(queue_file, 'r', encoding='utf-8') as f:
        queue = json.load(f)
    
    # 为每个任务计算优先级
    for task in queue.get('queue', []):
        if 'problem_id' in task:
            priority_result = score_problem(task['problem_id'])
            task['priority_score'] = priority_result['score']
            task['calculated_priority'] = priority_result['priority']
    
    # 保存更新
    with open(queue_file, 'w', encoding='utf-8') as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)
    
    return queue


if __name__ == '__main__':
    # 测试核心问题评分
    print("核心问题优先级评分:\n")
    
    for problem_id in [3, 32, 35, 61, 92, 98]:
        result = score_problem(problem_id)
        print(f"Problem #{problem_id}:")
        print(f"  分数：{result['score']}")
        print(f"  优先级：{result['priority']}")
        print(f"  说明：{result['description']}")
        print()
    
    # 更新队列
    update_queue_with_priority()
    print("研究队列优先级已更新")
