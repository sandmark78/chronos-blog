#!/usr/bin/env python3
"""
知识关联建立技能

用途：自动建立知识卡片之间的关联
调用：from skills.research.link_knowledge import link_concepts
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

# 知识库根目录
KNOWLEDGE_ROOT = Path("/home/claworc/.openclaw/workspace/knowledge")

def find_related_cards(title, content, threshold=0.3):
    """
    查找相关概念卡片
    
    Args:
        title: 当前卡片标题
        content: 当前卡片内容
        threshold: 相似度阈值
    
    Returns:
        list: 相关卡片列表
    """
    related = []
    
    # 提取关键词
    keywords = extract_keywords(title, content)
    
    # 遍历所有知识卡片
    for md_file in KNOWLEDGE_ROOT.rglob("*.md"):
        if md_file.name == f"{title}.md":
            continue  # 跳过自己
        
        # 读取文件内容
        with open(md_file, 'r', encoding='utf-8') as f:
            file_content = f.read()
        
        # 计算相似度
        file_keywords = extract_keywords(md_file.stem, file_content)
        similarity = calculate_similarity(keywords, file_keywords)
        
        if similarity >= threshold:
            related.append({
                "title": md_file.stem,
                "path": str(md_file.relative_to(KNOWLEDGE_ROOT)),
                "similarity": similarity,
                "shared_keywords": list(set(keywords) & set(file_keywords))
            })
    
    # 按相似度排序
    related.sort(key=lambda x: x["similarity"], reverse=True)
    
    return related[:5]  # 返回前 5 个最相关的


def extract_keywords(title, content):
    """
    提取关键词
    
    Args:
        title: 标题
        content: 内容
    
    Returns:
        list: 关键词列表
    """
    # 预定义核心概念词库
    core_concepts = [
        "时间", "熵", "生命", "宇宙", "意识", "信息", "复杂系统",
        "箭头", "热力学", "演化", "自组织", "涌现", "因果",
        "Big Bang", "Inflation", "RNA", "DNA", "Quantum"
    ]
    
    keywords = []
    text = title + " " + content
    
    # 匹配核心概念
    for concept in core_concepts:
        if concept in text:
            keywords.append(concept)
    
    return keywords


def calculate_similarity(keywords_a, keywords_b):
    """
    计算关键词相似度 (Jaccard 相似度)
    
    Args:
        keywords_a: 关键词列表 A
        keywords_b: 关键词列表 B
    
    Returns:
        float: 相似度 (0-1)
    """
    if not keywords_a or not keywords_b:
        return 0.0
    
    set_a = set(keywords_a)
    set_b = set(keywords_b)
    
    intersection = len(set_a & set_b)
    union = len(set_a | set_b)
    
    return intersection / union if union > 0 else 0.0


def link_concepts(card_path, auto_link=True, max_links=5):
    """
    为知识卡片建立关联
    
    Args:
        card_path: 卡片路径
        auto_link: 是否自动查找关联
        max_links: 最大关联数
    
    Returns:
        dict: 关联结果
    """
    card_file = Path(card_path)
    
    if not card_file.exists():
        return {
            "success": False,
            "message": f"卡片不存在：{card_path}"
        }
    
    # 读取卡片内容
    with open(card_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 查找相关卡片
    related_cards = []
    if auto_link:
        related_cards = find_related_cards(card_file.stem, content)
    
    # 检查是否已有"相关知识"部分
    if "## 相关知识" in content:
        # 更新现有部分
        return {
            "success": False,
            "message": "卡片已有关联部分，需要手动更新",
            "related_cards": related_cards
        }
    
    # 添加"相关知识"部分
    if related_cards:
        content += "\n\n## 相关知识\n\n"
        for card in related_cards[:max_links]:
            content += f"- [[{card['title']}]] (相似度：{card['similarity']:.2f})\n"
        
        # 写回文件
        with open(card_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return {
            "success": True,
            "message": f"已建立 {len(related_cards[:max_links])} 个关联",
            "related_cards": related_cards[:max_links]
        }
    
    return {
        "success": True,
        "message": "未找到相关卡片",
        "related_cards": []
    }


def build_knowledge_graph():
    """
    构建知识图谱
    
    Returns:
        dict: 知识图谱数据
            - nodes: 节点列表
            - edges: 边列表
    """
    nodes = []
    edges = []
    
    # 遍历所有知识卡片
    for md_file in KNOWLEDGE_ROOT.rglob("*.md"):
        # 读取 Frontmatter
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析 Frontmatter
        title = md_file.stem
        category = md_file.parent.name
        
        # 添加节点
        nodes.append({
            "id": title,
            "title": title,
            "category": category,
            "path": str(md_file.relative_to(KNOWLEDGE_ROOT))
        })
        
        # 查找引用（[[xxx]] 格式）
        references = re.findall(r'\[\[([^\]]+)\]\]', content)
        for ref in references:
            edges.append({
                "source": title,
                "target": ref,
                "type": "reference"
            })
    
    return {
        "nodes": nodes,
        "edges": edges,
        "generated_at": datetime.now().isoformat(),
        "total_nodes": len(nodes),
        "total_edges": len(edges)
    }


def export_knowledge_graph(output_path=None):
    """
    导出知识图谱
    
    Args:
        output_path: 输出路径（默认保存到 problem-database/）
    
    Returns:
        dict: 导出结果
    """
    if output_path is None:
        output_path = Path("/home/claworc/.openclaw/workspace/problem-database/knowledge_graph.json")
    
    graph = build_knowledge_graph()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    
    return {
        "success": True,
        "path": str(output_path),
        "nodes": graph["total_nodes"],
        "edges": graph["total_edges"]
    }


if __name__ == "__main__":
    # 测试
    print("测试知识关联...")
    
    # 构建知识图谱
    graph = build_knowledge_graph()
    print(f"知识图谱：{graph['total_nodes']} 个节点，{graph['total_edges']} 条边")
    
    # 导出图谱
    result = export_knowledge_graph()
    print(json.dumps(result, ensure_ascii=False, indent=2))
