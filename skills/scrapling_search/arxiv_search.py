#!/usr/bin/env python3
"""
arXiv 论文搜索工具
使用 curl_cffi 从 arXiv API 搜索并提取论文信息
Scrapling 生态工具，用于 Chronos Lab 信息搜集
"""

import sys
sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')

from curl_cffi import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime

def search_arxiv(query, max_results=10):
    """
    搜索 arXiv 论文（使用官方 API）
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        论文列表
    """
    # arXiv API URL
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
    
    print(f"搜索 arXiv: {query}")
    print(f"URL: {url}\n")
    
    # 获取 API 响应
    headers = {'User-Agent': 'ChronosLab/1.0 (sandmark; research bot)'}
    response = requests.get(url, headers=headers, timeout=30)
    
    if response.status_code != 200:
        print(f"错误：状态码 {response.status_code}")
        return []
    
    # 解析 XML
    try:
        root = ET.fromstring(response.text)
    except ET.ParseError as e:
        print(f"XML 解析错误：{e}")
        print(f"响应内容：{response.text[:500]}")
        return []
    
    # 提取论文信息
    papers = []
    ns = {'atom': 'http://www.w3.org/2005/Atom', 'arxiv': 'http://arxiv.org/schemas/atom'}
    
    for entry in root.findall('atom:entry', ns):
        try:
            title_elem = entry.find('atom:title', ns)
            title = title_elem.text.strip() if title_elem is not None else '无标题'
            # 清理标题中的换行
            title = ' '.join(title.split())
            
            # 作者
            authors = []
            for author in entry.findall('atom:author', ns):
                name_elem = author.find('atom:name', ns)
                if name_elem is not None and name_elem.text:
                    authors.append(name_elem.text)
            
            summary_elem = entry.find('atom:summary', ns)
            abstract = summary_elem.text.strip() if summary_elem is not None else '无摘要'
            abstract = ' '.join(abstract.split())
            
            id_elem = entry.find('atom:id', ns)
            arxiv_id = id_elem.text if id_elem is not None else None
            
            # PDF 链接
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id.split('/')[-1]}" if arxiv_id else None
            
            paper = {
                'title': title,
                'authors': ', '.join(authors),
                'abstract': abstract,
                'arxiv_id': arxiv_id,
                'arxiv_link': arxiv_id,
                'pdf_link': pdf_link
            }
            papers.append(paper)
            
        except Exception as e:
            print(f"提取论文信息时出错：{e}")
            continue
    
    return papers

def format_output(papers):
    """格式化输出"""
    print(f"\n{'='*60}")
    print(f"找到 {len(papers)} 篇论文\n")
    
    for i, paper in enumerate(papers, 1):
        print(f"[{i}] {paper['title']}")
        print(f"    作者：{paper['authors']}")
        print(f"    arXiv: {paper['arxiv_id']}")
        print(f"    PDF: {paper['pdf_link']}")
        print(f"    摘要：{paper['abstract'][:200]}...\n")
    
    return papers

def save_to_json(papers, query, filename=None):
    """保存结果到 JSON"""
    if not filename:
        filename = f'arxiv_{query.replace(" ", "_")[:50]}.json'
    
    output = {
        'query': query,
        'timestamp': datetime.now().isoformat(),
        'count': len(papers),
        'papers': papers
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 {filename}")

if __name__ == '__main__':
    # 测试搜索
    query = "time arrow entropy" if len(sys.argv) < 2 else sys.argv[1]
    papers = search_arxiv(query, max_results=5)
    
    if papers:
        format_output(papers)
        save_to_json(papers, query)
    else:
        print("未找到论文")
