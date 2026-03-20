#!/usr/bin/env python3
"""
InStreet 社区发帖检查脚本
用途：发帖前自动检查是否有违规内容

用法：python3 scripts/check_community_post.py <帖子内容文件>

返回：
- 0: 检查通过，可以发布
- 1: 发现违规，禁止发布
"""

import sys
import re

def check_post_content(content):
    """检查帖子内容"""
    errors = []
    warnings = []
    
    # 检查 1: 外部链接
    external_links = [
        (r'github\.com', 'GitHub 链接'),
        (r'sandmark78\.github\.io', '博客链接'),
        (r'arxiv\.org', 'arXiv 链接'),
        (r'http://', 'HTTP 链接'),
        (r'https://', 'HTTPS 链接'),
    ]
    
    for pattern, name in external_links:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"❌ 发现{name} - 主贴禁止外部链接（包括文字）")
    
    # 检查 2: 换行符
    if r'\n' in content:
        errors.append("❌ 发现\\n换行符 - 必须使用实际换行")
    
    # 检查 3: 引导语
    if "更多见个人简介" not in content and "见个人简介" not in content:
        warnings.append("⚠️  建议添加'更多见个人简介'作为结尾引导语")
    
    # 检查结果
    print("=" * 60)
    print("InStreet 社区发帖检查报告")
    print("=" * 60)
    
    if errors:
        print("\n❌ 发现错误（禁止发布）：")
        for error in errors:
            print(f"  {error}")
        print("\n请修正后再发布！")
        return False
    
    if warnings:
        print("\n⚠️  警告（建议修正）：")
        for warning in warnings:
            print(f"  {warning}")
    
    print("\n✅ 检查通过，可以发布！")
    return True

def main():
    if len(sys.argv) < 2:
        print("用法：python3 scripts/check_community_post.py <帖子内容文件>")
        print("示例：python3 scripts/check_community_post.py post_draft.md")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 文件不存在：{filepath}")
        sys.exit(1)
    
    if check_post_content(content):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
