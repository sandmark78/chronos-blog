#!/usr/bin/env python3
"""
多源文献搜索技能

用途：从 40+ 研究资源中搜索和抓取文献
调用：from skills.research.search_literature import search_all_sources
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 文献源配置
SOURCES_FILE = Path("/home/claworc/.openclaw/workspace/literature/research_sources.json")
OUTPUT_DIR = Path("/home/claworc/.openclaw/workspace/literature/outputs")

def load_sources():
    """加载文献源配置"""
    if not SOURCES_FILE.exists():
        return {"categories": {}}
    
    with open(SOURCES_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def search_arxiv(query, max_results=10, category=None):
    """
    搜索 arXiv 论文（带分类过滤优化）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
        category: arXiv 分类（如 physics.hist-ph）
    
    Returns:
        list: 论文列表
    """
    import sys
    sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')
    
    from curl_cffi import requests
    import xml.etree.ElementTree as ET
    from urllib.parse import quote
    
    # 关键词到分类的自动映射
    keyword_to_category = {
        'entropy': 'physics.gen-ph',
        'time': 'physics.gen-ph',
        'arrow of time': 'physics.gen-ph',
        'thermodynamics': 'physics.gen-ph',
        'origin of life': 'q-bio.BM',
        'RNA': 'q-bio.BM',
        'abiogenesis': 'q-bio.BM',
        'cosmology': 'astro-ph.CO',
        'big bang': 'astro-ph.CO',
        'complex systems': 'nlin.AO',
        'self-organization': 'nlin.AO',
        'information theory': 'cs.IT',
        'consciousness': 'q-bio.NC'
    }
    
    # 自动选择分类
    if category is None:
        for keyword, cat in keyword_to_category.items():
            if keyword.lower() in query.lower():
                category = cat
                break
    
    # 构建查询（分类过滤 + 关键词）
    if category:
        search_query = f"cat:{category}+AND+all:{quote(query)}"
    else:
        search_query = f"all:{quote(query)}"
    
    url = f"http://export.arxiv.org/api/query?search_query={search_query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    try:
        response = requests.get(url, headers={'User-Agent': 'ChronosLab/1.0'}, timeout=30)
        if response.status_code != 200:
            return []
        
        root = ET.fromstring(response.text)
        ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
        
        papers = []
        for entry in root.findall('atom:entry', ns):
            try:
                title_elem = entry.find('atom:title', ns)
                title = ' '.join(title_elem.text.split()) if title_elem is not None else '无标题'
                
                authors = []
                for author in entry.findall('atom:author', ns):
                    name_elem = author.find('atom:name', ns)
                    if name_elem is not None and name_elem.text:
                        authors.append(name_elem.text)
                
                summary_elem = entry.find('atom:summary', ns)
                abstract = ' '.join(summary_elem.text.split()) if summary_elem is not None else '无摘要'
                
                id_elem = entry.find('atom:id', ns)
                arxiv_id = id_elem.text if id_elem is not None else None
                pdf_link = f"https://arxiv.org/pdf/{arxiv_id.split('/')[-1]}" if arxiv_id else None
                
                papers.append({
                    'source': 'arXiv',
                    'title': title,
                    'authors': ', '.join(authors),
                    'abstract': abstract[:500],
                    'arxiv_id': arxiv_id,
                    'pdf_link': pdf_link,
                    'category': category or 'unknown'
                })
            except Exception:
                continue
        
        return papers[:max_results]
        
    except Exception as e:
        print(f"arXiv 搜索错误：{e}")
        return []


def search_semantic_scholar(query, max_results=10):
    """
    搜索 Semantic Scholar 论文
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        list: 论文列表
    """
    import sys
    sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')
    
    from curl_cffi import requests
    
    url = "https://api.semanticscholar.org/graph/v1/paper/search"
    params = {
        'query': query,
        'limit': max_results,
        'fields': 'title,authors,abstract,year,citationCount,url'
    }
    
    try:
        response = requests.get(url, params=params, headers={'User-Agent': 'ChronosLab/1.0'}, timeout=30)
        if response.status_code != 200:
            return []
        
        data = response.json()
        papers = []
        
        for paper in data.get('data', []):
            papers.append({
                'source': 'Semantic Scholar',
                'title': paper.get('title', '无标题'),
                'authors': ', '.join([a['name'] for a in paper.get('authors', [])]),
                'abstract': paper.get('abstract', '无摘要')[:500] if paper.get('abstract') else '无摘要',
                'year': paper.get('year'),
                'citations': paper.get('citationCount'),
                'url': paper.get('url')
            })
        
        return papers
        
    except Exception as e:
        print(f"Semantic Scholar 搜索错误：{e}")
        return []


def search_all_sources(keywords, daily_targets=None):
    """
    从所有文献源搜索
    
    Args:
        keywords: 关键词列表或字典
        daily_targets: 每日目标数量
    
    Returns:
        dict: 搜索结果
    """
    if daily_targets is None:
        daily_targets = {
            'arxiv': 20,
            'semantic_scholar': 20,
            'nature': 5,
            'nasa': 5,
            'santa_fe': 5
        }
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'keywords': keywords,
        'papers': [],
        'stats': {}
    }
    
    # arXiv 搜索
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            papers = search_arxiv(query, max_results=daily_targets.get('arxiv', 20))
            results['papers'].extend(papers)
    else:
        papers = search_arxiv(keywords, max_results=daily_targets.get('arxiv', 20))
        results['papers'].extend(papers)
    
    # Semantic Scholar 搜索
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            papers = search_semantic_scholar(query, max_results=daily_targets.get('semantic_scholar', 20))
            results['papers'].extend(papers)
    else:
        papers = search_semantic_scholar(keywords, max_results=daily_targets.get('semantic_scholar', 20))
        results['papers'].extend(papers)
    
    # 统计
    results['stats'] = {
        'total_papers': len(results['papers']),
        'arxiv_count': len([p for p in results['papers'] if p.get('source') == 'arXiv']),
        'semantic_scholar_count': len([p for p in results['papers'] if p.get('source') == 'Semantic Scholar'])
    }
    
    return results


def save_results(results, output_dir=None):
    """保存搜索结果"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = output_dir / f"literature_search_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return filename


if __name__ == '__main__':
    # 测试
    keywords = {
        'time': 'arrow of time entropy',
        'life': 'origin of life RNA world',
        'cosmology': 'cosmology big bang inflation'
    }
    
    results = search_all_sources(keywords)
    print(f"找到 {len(results['papers'])} 篇论文")
    
    filename = save_results(results)
    print(f"结果已保存到：{filename}")
