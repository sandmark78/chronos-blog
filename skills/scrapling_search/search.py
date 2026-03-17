#!/usr/bin/env python3
"""
arXiv Literature Search Script
Searches arXiv for academic papers based on keywords.
"""

import json
import urllib.request
import urllib.parse
from datetime import datetime
from pathlib import Path

def search_arxiv(keywords, max_results=10):
    """
    Search arXiv API for papers matching keywords.
    
    Args:
        keywords: List of search terms
        max_results: Maximum number of results to return
    
    Returns:
        List of paper dictionaries with title, authors, abstract, url, published
    """
    base_url = "http://export.arxiv.org/api/query"
    
    # Build search query - use phrases for multi-word keywords
    search_terms = []
    for k in keywords:
        if ' ' in k:
            search_terms.append(f'all:"{k}"')
        else:
            search_terms.append(f'all:{k}')
    search_query = " AND ".join(search_terms)
    
    # Build URL manually to avoid double-encoding
    params = f"search_query={urllib.parse.quote(search_query)}&start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    full_url = f"{base_url}?{params}"
    
    print(f"Searching arXiv for: {' '.join(keywords)}")
    print(f"URL: {full_url}")
    
    try:
        with urllib.request.urlopen(full_url, timeout=30) as response:
            xml_data = response.read().decode('utf-8')
        
        # Parse XML manually (simple parsing for arXiv API)
        entries = parse_arxiv_xml(xml_data)
        return entries
    
    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []

def parse_arxiv_xml(xml_data):
    """
    Parse arXiv API XML response.
    
    Args:
        xml_data: Raw XML string from arXiv API
    
    Returns:
        List of paper dictionaries
    """
    import xml.etree.ElementTree as ET
    
    # Define namespaces
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'arxiv': 'http://arxiv.org/schemas/atom'
    }
    
    try:
        root = ET.fromstring(xml_data)
        entries = []
        
        for entry in root.findall('atom:entry', namespaces):
            paper = {}
            
            # Title
            title_elem = entry.find('atom:title', namespaces)
            paper['title'] = title_elem.text.strip() if title_elem is not None else 'No title'
            
            # Authors
            authors = []
            for author in entry.findall('atom:author', namespaces):
                name_elem = author.find('atom:name', namespaces)
                if name_elem is not None:
                    authors.append(name_elem.text)
            paper['authors'] = authors
            
            # Published date
            published_elem = entry.find('atom:published', namespaces)
            paper['published'] = published_elem.text if published_elem is not None else 'Unknown'
            
            # Abstract
            summary_elem = entry.find('atom:summary', namespaces)
            paper['abstract'] = summary_elem.text.strip() if summary_elem is not None else 'No abstract'
            
            # arXiv ID and URL
            id_elem = entry.find('atom:id', namespaces)
            paper['arxiv_id'] = id_elem.text if id_elem is not None else 'Unknown'
            paper['url'] = paper['arxiv_id'].replace('http://arxiv.org/abs/', 'https://arxiv.org/abs/')
            
            # Categories
            categories = []
            for category in entry.findall('atom:category', namespaces):
                term = category.get('term')
                if term:
                    categories.append(term)
            paper['categories'] = categories
            
            entries.append(paper)
        
        return entries
    
    except Exception as e:
        print(f"Error parsing XML: {e}")
        return []

def save_results(results, output_path, keywords):
    """
    Save search results to JSON file.
    
    Args:
        results: List of paper dictionaries
        output_path: Path to output directory
        keywords: Search keywords used
    """
    output_file = Path(output_path) / f"search_{'_'.join(keywords).replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    output_data = {
        'search_metadata': {
            'keywords': keywords,
            'search_date': datetime.now().isoformat(),
            'total_results': len(results),
            'search_engine': 'arxiv'
        },
        'papers': results
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"Results saved to: {output_file}")
    return str(output_file)

def main():
    """Main entry point for CLI usage."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python search.py <keyword1> [keyword2] ... [--output <dir>] [--max <n>]")
        sys.exit(1)
    
    # Parse arguments
    keywords = []
    output_dir = "./outputs"
    max_results = 10
    
    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--output':
            output_dir = sys.argv[i + 1]
            i += 2
        elif arg == '--max':
            max_results = int(sys.argv[i + 1])
            i += 2
        else:
            keywords.append(arg)
            i += 1
    
    if not keywords:
        print("Error: No keywords provided")
        sys.exit(1)
    
    # Search
    results = search_arxiv(keywords, max_results)
    
    # Save
    output_file = save_results(results, output_dir, keywords)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Search Summary")
    print(f"{'='*60}")
    print(f"Keywords: {' '.join(keywords)}")
    print(f"Results found: {len(results)}")
    print(f"Output file: {output_file}")
    
    if results:
        print(f"\nTop 3 results:")
        for i, paper in enumerate(results[:3], 1):
            print(f"\n{i}. {paper['title']}")
            print(f"   Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
            print(f"   Published: {paper['published'][:10]}")
            print(f"   URL: {paper['url']}")

if __name__ == '__main__':
    main()
