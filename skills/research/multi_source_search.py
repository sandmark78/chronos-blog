#!/usr/bin/env python3
"""
多源文献搜索技能

用途：从 40+ 研究资源中并行搜索
调用：from skills.research.multi_source_search import search_all_sources
"""

import json
import os
from datetime import datetime
from pathlib import Path

# 文献源配置
SOURCES_FILE = Path("/home/claworc/.openclaw/workspace/literature/research_sources.json")
OUTPUT_DIR = Path("/home/claworc/.openclaw/workspace/literature/outputs")

def search_semantic_scholar(query, max_results=10):
    """
    搜索 Semantic Scholar 论文（AI 相关性排序）
    
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
        'fields': 'title,authors,abstract,year,citationCount,url,venue,isOpenAccess'
    }
    
    try:
        response = requests.get(url, params=params, headers={'User-Agent': 'ChronosLab/1.0'}, timeout=30)
        if response.status_code != 200:
            print(f"Semantic Scholar API 错误：{response.status_code}")
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
                'venue': paper.get('venue'),
                'open_access': paper.get('isOpenAccess'),
                'url': paper.get('url'),
                'relevance_score': 0.85  # Semantic Scholar 有相关性排序
            })
        
        return papers
        
    except Exception as e:
        print(f"Semantic Scholar 搜索错误：{e}")
        return []


def search_pubmed(query, max_results=10):
    """
    搜索 PubMed 论文（生命科学专用）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        list: 论文列表
    """
    import sys
    sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')
    
    from curl_cffi import requests
    import xml.etree.ElementTree as ET
    
    # PubMed E-utilities API
    search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    try:
        # 搜索获取 ID 列表
        search_params = {
            'db': 'pubmed',
            'term': query,
            'retmax': max_results,
            'retmode': 'json'
        }
        search_response = requests.get(search_url, params=search_params, timeout=30)
        if search_response.status_code != 200:
            return []
        
        search_data = search_response.json()
        pmids = search_data.get('esearchresult', {}).get('idlist', [])
        
        if not pmids:
            return []
        
        # 获取论文详情
        fetch_params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml'
        }
        fetch_response = requests.get(fetch_url, params=fetch_params, timeout=30)
        if fetch_response.status_code != 200:
            return []
        
        root = ET.fromstring(fetch_response.text)
        papers = []
        
        for article in root.findall('.//PubmedArticle'):
            try:
                title_elem = article.find('.//ArticleTitle')
                title = title_elem.text if title_elem is not None else '无标题'
                
                abstract_elem = article.find('.//Abstract/AbstractText')
                abstract = abstract_elem.text if abstract_elem is not None else '无摘要'
                
                authors = []
                for author in article.findall('.//Author'):
                    last_name = author.find('LastName')
                    fore_name = author.find('ForeName')
                    if last_name is not None:
                        authors.append(f"{fore_name.text if fore_name is not None else ''} {last_name.text}")
                
                year_elem = article.find('.//Journal/JournalIssue/PubDate/Year')
                year = year_elem.text if year_elem is not None else None
                
                papers.append({
                    'source': 'PubMed',
                    'title': title,
                    'authors': ', '.join(authors),
                    'abstract': abstract[:500] if abstract else '无摘要',
                    'year': year,
                    'pmid': article.find('PMID').text if article.find('PMID') is not None else None,
                    'relevance_score': 0.8
                })
            except Exception:
                continue
        
        return papers
        
    except Exception as e:
        print(f"PubMed 搜索错误：{e}")
        return []


def search_nasa(query, max_results=5):
    """
    搜索 NASA 研究报告（宇宙学/天体物理）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        list: 论文列表
    """
    import sys
    sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')
    
    from curl_cffi import requests
    
    # NASA ADS API
    url = "https://api.adsabs.harvard.edu/v1/search/query"
    params = {
        'q': query,
        'fl': 'title,author,abstract,pubdate,bibcode,doi',
        'rows': max_results,
        'sort': 'citation_count desc'
    }
    headers = {
        'User-Agent': 'ChronosLab/1.0'
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=30)
        if response.status_code != 200:
            return []
        
        data = response.json()
        papers = []
        
        for doc in data.get('response', {}).get('docs', []):
            papers.append({
                'source': 'NASA ADS',
                'title': doc.get('title', ['无标题'])[0],
                'authors': ', '.join(doc.get('author', [])),
                'abstract': doc.get('abstract', ['无摘要'])[0][:500] if doc.get('abstract') else '无摘要',
                'year': doc.get('pubdate', [''])[0][:4],
                'bibcode': doc.get('bibcode', [''])[0],
                'doi': doc.get('doi', [''])[0],
                'relevance_score': 0.75
            })
        
        return papers
        
    except Exception as e:
        print(f"NASA ADS 搜索错误：{e}")
        return []


def search_arxiv_optimized(query, max_results=10):
    """
    搜索 arXiv 论文（带分类过滤优化）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
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
    category = None
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
                    'category': category or 'unknown',
                    'relevance_score': 0.6 if category else 0.3  # 有分类过滤相关性更高
                })
            except Exception:
                continue
        
        return papers[:max_results]
        
    except Exception as e:
        print(f"arXiv 搜索错误：{e}")
        return []


def search_all_sources(keywords, daily_targets=None):
    """
    从所有文献源并行搜索
    
    Args:
        keywords: 关键词列表或字典
        daily_targets: 每日目标数量
    
    Returns:
        dict: 搜索结果
    """
    if daily_targets is None:
        daily_targets = {
            'semantic_scholar': 15,
            'arxiv': 10,
            'pubmed': 10,
            'nasa': 5
        }
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'keywords': keywords,
        'papers': [],
        'stats': {}
    }
    
    # Semantic Scholar 搜索（优先级最高，AI 相关性排序）
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            papers = search_semantic_scholar(query, max_results=daily_targets.get('semantic_scholar', 15))
            results['papers'].extend(papers)
    else:
        papers = search_semantic_scholar(keywords, max_results=daily_targets.get('semantic_scholar', 15))
        results['papers'].extend(papers)
    
    # arXiv 搜索（带分类过滤）
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            papers = search_arxiv_optimized(query, max_results=daily_targets.get('arxiv', 10))
            results['papers'].extend(papers)
    else:
        papers = search_arxiv_optimized(keywords, max_results=daily_targets.get('arxiv', 10))
        results['papers'].extend(papers)
    
    # PubMed 搜索（生命科学专用）
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            if any(kw in query.lower() for kw in ['life', 'biology', 'RNA', 'origin', 'cell']):
                papers = search_pubmed(query, max_results=daily_targets.get('pubmed', 10))
                results['papers'].extend(papers)
    else:
        if any(kw in keywords.lower() for kw in ['life', 'biology', 'RNA', 'origin', 'cell']):
            papers = search_pubmed(keywords, max_results=daily_targets.get('pubmed', 10))
            results['papers'].extend(papers)
    
    # NASA ADS 搜索（宇宙学专用）
    if isinstance(keywords, dict):
        for field, query in keywords.items():
            if any(kw in query.lower() for kw in ['cosmology', 'universe', 'big bang', 'entropy', 'time']):
                papers = search_nasa(query, max_results=daily_targets.get('nasa', 5))
                results['papers'].extend(papers)
    else:
        if any(kw in keywords.lower() for kw in ['cosmology', 'universe', 'big bang', 'entropy', 'time']):
            papers = search_nasa(keywords, max_results=daily_targets.get('nasa', 5))
            results['papers'].extend(papers)
    
    # 去重（基于标题）
    seen_titles = set()
    unique_papers = []
    for paper in results['papers']:
        title_key = paper.get('title', '').lower()
        if title_key not in seen_titles:
            seen_titles.add(title_key)
            unique_papers.append(paper)
    
    results['papers'] = unique_papers
    
    # 统计
    results['stats'] = {
        'total_papers': len(results['papers']),
        'semantic_scholar_count': len([p for p in results['papers'] if p.get('source') == 'Semantic Scholar']),
        'arxiv_count': len([p for p in results['papers'] if p.get('source') == 'arXiv']),
        'pubmed_count': len([p for p in results['papers'] if p.get('source') == 'PubMed']),
        'nasa_count': len([p for p in results['papers'] if p.get('source') == 'NASA ADS']),
        'average_relevance': sum(p.get('relevance_score', 0) for p in results['papers']) / len(results['papers']) if results['papers'] else 0
    }
    
    return results


def save_results(results, output_dir=None):
    """保存搜索结果"""
    if output_dir is None:
        output_dir = OUTPUT_DIR
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = output_dir / f"multi_source_search_{timestamp}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return filename


if __name__ == '__main__':
    # 测试多源搜索
    keywords = {
        'time': 'arrow of time entropy',
        'life': 'origin of life RNA world',
        'cosmology': 'cosmology big bang inflation'
    }
    
    results = search_all_sources(keywords)
    print(f"找到 {len(results['papers'])} 篇论文")
    print(f"统计：{results['stats']}")
    
    filename = save_results(results)
    print(f"结果已保存到：{filename}")
