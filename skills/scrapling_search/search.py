#!/usr/bin/env python3
"""
Chronos Lab 统一搜索接口
整合 arXiv、Google Scholar 等学术搜索源
"""

import sys
sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')

from curl_cffi import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Optional

class AcademicSearch:
    """学术搜索工具类"""
    
    def __init__(self):
        self.headers = {'User-Agent': 'ChronosLab/1.0 (sandmark; research bot)'}
    
    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict]:
        """搜索 arXiv"""
        url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=30)
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
                        'abstract': abstract,
                        'arxiv_id': arxiv_id,
                        'pdf_link': pdf_link,
                        'link': arxiv_id
                    })
                except Exception:
                    continue
            
            return papers
        except Exception as e:
            print(f"arXiv 搜索错误：{e}")
            return []
    
    def search(self, query: str, source: str = 'arxiv', max_results: int = 10) -> List[Dict]:
        """统一搜索接口"""
        if source == 'arxiv':
            return self.search_arxiv(query, max_results)
        else:
            return self.search_arxiv(query, max_results)
    
    def save_results(self, papers: List[Dict], query: str, filename: Optional[str] = None) -> str:
        """保存搜索结果"""
        if not filename:
            filename = f'search_{query.replace(" ", "_")[:50]}.json'
        
        output = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'count': len(papers),
            'papers': papers
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        return filename

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法：python search.py <查询词> [来源] [最大结果数]")
        print("示例：python search.py 'time arrow entropy' arxiv 5")
        sys.exit(1)
    
    query = sys.argv[1]
    source = sys.argv[2] if len(sys.argv) > 2 else 'arxiv'
    max_results = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    
    searcher = AcademicSearch()
    papers = searcher.search(query, source, max_results)
    
    if papers:
        print(f"\n{'='*60}")
        print(f"找到 {len(papers)} 篇论文\n")
        
        for i, paper in enumerate(papers, 1):
            print(f"[{i}] {paper['title']}")
            print(f"    作者：{paper['authors']}")
            print(f"    来源：{paper['source']}")
            print(f"    链接：{paper['link']}")
            print(f"    摘要：{paper['abstract'][:200]}...\n")
        
        filename = searcher.save_results(papers, query)
        print(f"结果已保存到 {filename}")
    else:
        print("未找到论文")

if __name__ == '__main__':
    main()
