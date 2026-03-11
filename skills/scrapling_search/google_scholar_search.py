#!/usr/bin/env python3
"""
Google Scholar 搜索工具
使用 Scrapling 从 Google Scholar 搜索并提取论文信息

注意：Google Scholar 有反爬虫措施，建议使用 StealthyFetcher
"""

import sys
sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')

from scrapling.fetchers import StealthyFetcher
from urllib.parse import quote
import json
from datetime import datetime

def search_scholar(query, max_results=10):
    """
    搜索 Google Scholar 论文
    
    Args:
        query: 搜索关键词
        max_results: 最大结果数
    
    Returns:
        论文列表
    """
    encoded_query = quote(query)
    url = f"https://scholar.google.com/scholar?q={encoded_query}&hl=zh-CN&num={max_results}"
    
    print(f"搜索 Google Scholar: {query}")
    print(f"URL: {url}\n")
    
    # 使用 StealthyFetcher 绕过反爬虫
    try:
        response = StealthyFetcher.get(url, headless=True, network_idle=True)
    except Exception as e:
        print(f"获取页面失败：{e}")
        print("尝试使用普通 Fetcher...")
        from scrapling.fetchers import Fetcher
        response = Fetcher.get(url)
    
    if response.status != 200:
        print(f"错误：状态码 {response.status}")
        return []
    
    # 提取论文信息
    papers = []
    results = response.css('.gs_r')
    
    for result in results[:max_results]:
        try:
            title_elem = result.css('.gs_rt a')
            title = title_elem.css('::text').get().strip() if title_elem else '无标题'
            link = title_elem.css('::attr(href)').get() if title_elem else None
            
            authors_elem = result.css('.gs_a')
            authors = authors_elem.css('::text').get() if authors_elem else '未知作者'
            
            abstract_elem = result.css('.gs_rs')
            abstract = abstract_elem.css('::text').get().strip() if abstract_elem else '无摘要'
            
            cited_by_elem = result.css('.gs_fl a[href*="citedby"]')
            cited_by = cited_by_elem.css('::text').get() if cited_by_elem else '0'
            
            paper = {
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'link': link,
                'cited_by': cited_by
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
        print(f"    引用：{paper['cited_by']}")
        print(f"    链接：{paper['link']}")
        print(f"    摘要：{paper['abstract'][:200]}...\n")
    
    return papers

def save_to_json(papers, filename='scholar_results.json'):
    """保存结果到 JSON"""
    if not papers:
        return
    
    output = {
        'query': papers[0]['title'] if papers else '',
        'timestamp': datetime.now().isoformat(),
        'count': len(papers),
        'papers': papers
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 {filename}")

if __name__ == '__main__':
    # 测试搜索
    query = "origin of life RNA world" if len(sys.argv) < 2 else sys.argv[1]
    papers = search_scholar(query, max_results=5)
    
    if papers:
        format_output(papers)
        save_to_json(papers, f'scholar_{query.replace(" ", "_")}.json')
    else:
        print("未找到论文")
