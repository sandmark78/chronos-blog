#!/usr/bin/env python3
"""
新问题衍生技能

用途：基于研究结果自动生成新的研究问题
调用：from skills.research.derive_new_questions import derive_questions
"""

import json
from datetime import datetime

def derive_questions(problem, findings, hypotheses, context=None):
    """
    基于研究结果衍生新问题
    
    Args:
        problem: 原始研究问题
        findings: 关键发现列表
        hypotheses: 新假设列表
        context: 上下文信息（可选）
    
    Returns:
        list: 新问题列表，每个问题包含：
            - id: 任务 ID
            - type: 任务类型
            - question: 问题描述
            - priority: 优先级
            - source: 来源问题
            - derivation_type: 衍生类型
            - tags: 标签
    """
    new_questions = []
    question_counter = 1
    
    # 衍生类型 1: 深入探索（针对发现的细节）
    for finding in findings:
        if "因为" in finding or "由于" in finding:
            new_questions.append({
                "id": f"task_derive_{question_counter:03d}",
                "type": "problem_research",
                "question": f"为什么{finding.split('因为')[-1] if '因为' in finding else finding}？",
                "priority": "medium",
                "source": problem,
                "derivation_type": "deep_dive",
                "tags": ["深入探索", "因果分析"]
            })
            question_counter += 1
    
    # 衍生类型 2: 假设验证（针对新假设）
    for hyp in hypotheses:
        new_questions.append({
            "id": f"task_derive_{question_counter:03d}",
            "type": "hypothesis_validation",
            "question": f"如何验证：{hyp}？",
            "priority": "high",
            "source": problem,
            "derivation_type": "validation",
            "tags": ["假设验证", "实验设计"]
        })
        question_counter += 1
    
    # 衍生类型 3: 跨领域连接
    if context:
        if "时间" in problem or "熵" in problem:
            new_questions.append({
                "id": f"task_derive_{question_counter:03d}",
                "type": "cross_domain",
                "question": "这个理论如何应用到生命起源问题？",
                "priority": "medium",
                "source": problem,
                "derivation_type": "cross_domain",
                "tags": ["跨领域", "生命起源"]
            })
            question_counter += 1
        
        if "生命" in problem:
            new_questions.append({
                "id": f"task_derive_{question_counter:03d}",
                "type": "cross_domain",
                "question": "这个发现是否适用于非生物复杂系统？",
                "priority": "medium",
                "source": problem,
                "derivation_type": "cross_domain",
                "tags": ["跨领域", "复杂系统"]
            })
            question_counter += 1
    
    # 衍生类型 4: 反向思考
    new_questions.append({
        "id": f"task_derive_{question_counter:03d}",
        "type": "reverse_thinking",
        "question": f"如果{problem.replace('为什么', '').replace('？', '').replace('?', '')}不成立，会怎样？",
        "priority": "low",
        "source": problem,
        "derivation_type": "reverse",
        "tags": ["反向思考", "思想实验"]
    })
    question_counter += 1
    
    # 衍生类型 5: 统一理论
    if len(findings) >= 2 or len(hypotheses) >= 2:
        new_questions.append({
            "id": f"task_derive_{question_counter:03d}",
            "type": "theory_synthesis",
            "question": "如何将这些发现统一到一个理论框架中？",
            "priority": "high",
            "source": problem,
            "derivation_type": "synthesis",
            "tags": ["统一理论", "综合"]
        })
        question_counter += 1
    
    return new_questions


def derive_from_knowledge_conflict(theory_a, theory_b, conflict_description):
    """
    基于理论冲突衍生问题
    
    Args:
        theory_a: 理论 A
        theory_b: 理论 B
        conflict_description: 冲突描述
    
    Returns:
        dict: 衍生问题
    """
    return {
        "id": f"task_conflict_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "conflict_resolution",
        "question": f"如何调和{theory_a}与{theory_b}之间的矛盾？",
        "priority": "high",
        "conflict": {
            "theory_a": theory_a,
            "theory_b": theory_b,
            "description": conflict_description
        },
        "derivation_type": "conflict",
        "tags": ["理论冲突", "调和"]
    }


def derive_from_paper_insights(paper_title, paper_insights, gap_identified):
    """
    基于论文洞察衍生问题
    
    Args:
        paper_title: 论文标题
        paper_insights: 论文洞察列表
        gap_identified: 识别的研究空白
    
    Returns:
        dict: 衍生问题
    """
    return {
        "id": f"task_paper_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "type": "literature_followup",
        "question": f"如何填补这个研究空白：{gap_identified}？",
        "priority": "medium",
        "source_paper": paper_title,
        "insights": paper_insights,
        "gap": gap_identified,
        "derivation_type": "literature",
        "tags": ["文献跟进", "研究空白"]
    }


def prioritize_questions(questions, criteria=None):
    """
    对问题进行优先级排序
    
    Args:
        questions: 问题列表
        criteria: 排序标准（默认基于核心问题关联度）
    
    Returns:
        list: 排序后的问题列表
    """
    # 核心问题权重
    core_keywords = ["时间", "熵", "生命", "起源", "宇宙", "意识", "信息"]
    
    def calculate_priority(question):
        score = 0
        text = question.get("question", "") + " " + " ".join(question.get("tags", []))
        
        # 核心关键词
        for keyword in core_keywords:
            if keyword in text:
                score += 2
        
        # 优先级基础分
        priority_map = {"high": 10, "medium": 5, "low": 1}
        score += priority_map.get(question.get("priority", "medium"), 0)
        
        # 衍生类型权重
        type_weights = {
            "validation": 3,  # 假设验证优先
            "synthesis": 3,   # 综合优先
            "conflict": 3,    # 冲突解决优先
            "deep_dive": 2,
            "cross_domain": 2,
            "reverse": 1,
            "literature": 2
        }
        score += type_weights.get(question.get("derivation_type"), 1)
        
        return score
    
    return sorted(questions, key=calculate_priority, reverse=True)


if __name__ == "__main__":
    # 测试
    questions = derive_questions(
        problem="为什么时间只有一个方向？",
        findings=[
            "时间箭头来自熵增",
            "因为宇宙初始低熵",
            "生命是局部熵减系统"
        ],
        hypotheses=[
            "时间是信息变化的度量",
            "生命是熵增的催化剂"
        ],
        context={"domain": "physics"}
    )
    
    print(f"衍生出 {len(questions)} 个新问题:\n")
    for q in questions:
        print(f"[{q['priority']}] {q['question']}")
        print(f"  来源：{q['source']}")
        print(f"  类型：{q['derivation_type']}")
        print()
