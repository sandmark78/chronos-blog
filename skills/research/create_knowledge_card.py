#!/usr/bin/env python3
"""
知识卡片创建技能

用途：将研究成果固化为标准化知识卡片
调用：from skills.research.create_knowledge_card import create_card
"""

import os
import json
from datetime import datetime
from pathlib import Path

# 知识库根目录
KNOWLEDGE_ROOT = Path("/home/claworc/.openclaw/workspace/knowledge")

def create_card(title, category, content, sources=None, tags=None, related=None):
    """
    创建知识卡片
    
    Args:
        title: 卡片标题
        category: 分类 (时间/生命/宇宙/意识/复杂系统/信息)
        content: 卡片内容字典
            - definition: 定义
            - key_points: 关键观点列表
            - theories: 相关理论列表
            - scientists: 相关科学家列表
            - questions: 关联问题列表
            - open_questions: 开放问题列表
        sources: 引用来源列表
        tags: 标签列表
        related: 相关概念列表（用于双向链接）
    
    Returns:
        dict: 创建结果
            - success: bool
            - path: 文件路径
            - message: 消息
    """
    # 验证分类
    valid_categories = ["时间", "生命", "宇宙", "意识", "复杂系统", "信息", "研究日志", "思想实验"]
    if category not in valid_categories:
        return {
            "success": False,
            "path": None,
            "message": f"无效分类：{category}。有效分类：{valid_categories}"
        }
    
    # 创建分类目录
    category_dir = KNOWLEDGE_ROOT / category
    category_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    filename = title.replace(" ", "_").replace("/", "_") + ".md"
    filepath = category_dir / filename
    
    # 检查是否已存在
    if filepath.exists():
        return {
            "success": False,
            "path": str(filepath),
            "message": f"卡片已存在：{filepath}"
        }
    
    # 生成 Frontmatter
    frontmatter = {
        "title": title,
        "category": category,
        "tags": tags or [],
        "created": datetime.now().strftime("%Y-%m-%d"),
        "updated": datetime.now().strftime("%Y-%m-%d"),
        "sources": sources or []
    }
    
    # 生成相关内容
    content_md = []
    
    # Frontmatter
    content_md.append("---")
    for key, value in frontmatter.items():
        if isinstance(value, list):
            content_md.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
        else:
            content_md.append(f"{key}: {value}")
    content_md.append("---")
    content_md.append("")
    
    # 核心概念
    if "definition" in content:
        content_md.append("## 核心概念\n")
        content_md.append(content["definition"])
        content_md.append("")
    
    # 关键观点
    if "key_points" in content and content["key_points"]:
        content_md.append("## 关键观点\n")
        for point in content["key_points"]:
            content_md.append(f"- {point}")
        content_md.append("")
    
    # 相关理论
    if "theories" in content and content["theories"]:
        content_md.append("## 相关理论\n")
        for theory in content["theories"]:
            if theory.startswith("[["):
                content_md.append(f"- {theory}")
            else:
                content_md.append(f"- [[{theory}]]")
        content_md.append("")
    
    # 相关科学家
    if "scientists" in content and content["scientists"]:
        content_md.append("## 相关科学家\n")
        for scientist in content["scientists"]:
            content_md.append(f"- {scientist}")
        content_md.append("")
    
    # 关联问题
    if "questions" in content and content["questions"]:
        content_md.append("## 关联问题\n")
        for q in content["questions"]:
            content_md.append(f"- {q}")
        content_md.append("")
    
    # 开放问题
    if "open_questions" in content and content["open_questions"]:
        content_md.append("## 开放问题\n")
        for q in content["open_questions"]:
            content_md.append(f"- {q}")
        content_md.append("")
    
    # 相关知识（双向链接）
    if related:
        content_md.append("## 相关知识\n")
        for rel in related:
            if rel.startswith("[["):
                content_md.append(f"- {rel}")
            else:
                content_md.append(f"- [[{rel}]]")
        content_md.append("")
    
    # 写入文件
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(content_md))
    
    return {
        "success": True,
        "path": str(filepath),
        "message": f"知识卡片已创建：{filepath}"
    }


def batch_create_cards(cards):
    """
    批量创建知识卡片
    
    Args:
        cards: 卡片列表，每张卡片包含 title, category, content, sources, tags, related
    
    Returns:
        dict: 批量创建结果
            - total: 总数
            - success: 成功数
            - failed: 失败数
            - results: 详细结果列表
    """
    results = []
    success_count = 0
    failed_count = 0
    
    for card in cards:
        result = create_card(**card)
        results.append(result)
        if result["success"]:
            success_count += 1
        else:
            failed_count += 1
    
    return {
        "total": len(cards),
        "success": success_count,
        "failed": failed_count,
        "results": results
    }


if __name__ == "__main__":
    # 测试
    result = create_card(
        title="测试卡片",
        category="时间",
        content={
            "definition": "这是一个测试定义",
            "key_points": ["观点 1", "观点 2"],
            "theories": ["理论 1"],
            "questions": ["问题 #1"]
        },
        tags=["测试"],
        related=["熵增"]
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
