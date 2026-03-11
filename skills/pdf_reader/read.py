#!/usr/bin/env python3
"""
PDF 读取工具
使用 PyMuPDF (fitz) 提取 PDF 文本内容
"""

import sys
import os

# 添加虚拟环境路径
sys.path.insert(0, '/home/claworc/.openclaw/workspace/scrapling_env/lib/python3.11/site-packages')

import fitz  # PyMuPDF

def read_pdf(pdf_path, max_pages=None):
    """
    读取 PDF 文件并提取文本
    
    Args:
        pdf_path: PDF 文件路径
        max_pages: 最大读取页数（None 表示全部）
    
    Returns:
        提取的文本内容
    """
    if not os.path.exists(pdf_path):
        print(f"错误：文件不存在 - {pdf_path}")
        return None
    
    try:
        doc = fitz.open(pdf_path)
        print(f"PDF 信息:")
        print(f"  文件：{os.path.basename(pdf_path)}")
        print(f"  总页数：{len(doc)}")
        print(f"  加密：{'是' if doc.is_encrypted else '否'}")
        print("-" * 60)
        
        text_content = []
        limit = max_pages if max_pages else len(doc)
        
        for page_num in range(min(limit, len(doc))):
            page = doc[page_num]
            text = page.get_text()
            
            if text.strip():
                text_content.append(f"\n--- 第 {page_num + 1} 页 ---\n")
                text_content.append(text)
        
        doc.close()
        
        full_text = "\n".join(text_content)
        return full_text
        
    except Exception as e:
        print(f"读取 PDF 时出错：{e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("用法：python read.py <PDF 文件路径> [最大页数]")
        print("示例：python read.py /path/to/file.pdf 5")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    max_pages = int(sys.argv[2]) if len(sys.argv) > 2 else None
    
    print(f"\n读取 PDF: {pdf_path}\n")
    text = read_pdf(pdf_path, max_pages)
    
    if text:
        print("\n" + "=" * 60)
        print("PDF 内容摘要（前 2000 字符）:")
        print("=" * 60)
        print(text[:2000])
        print("\n..." if len(text) > 2000 else "")
        print("=" * 60)
        
        # 保存到文本文件
        output_path = pdf_path.rsplit('.', 1)[0] + '_extracted.txt'
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"\n完整内容已保存到：{output_path}")
    else:
        print("未能提取 PDF 内容")

if __name__ == '__main__':
    main()
