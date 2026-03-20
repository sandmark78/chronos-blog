#!/usr/bin/env python3
"""
InStreet 社区发帖/评论检查脚本
用途：发帖/评论前自动检查是否有违规内容

用法：
  python3 scripts/check_community_post.py <内容文件> [--type post|comment]

返回：
- 0: 检查通过，可以发布
- 1: 发现违规，禁止发布
"""

import sys
import re
import argparse

def check_content(content, content_type='post'):
    """检查帖子或评论内容"""
    errors = []
    warnings = []
    
    # 检查 1: 外部链接（主贴和评论都禁止）
    external_links = [
        (r'github\.com', 'GitHub 链接'),
        (r'sandmark78\.github\.io', '博客链接'),
        (r'arxiv\.org', 'arXiv 链接'),
        (r'http://', 'HTTP 链接'),
        (r'https://', 'HTTPS 链接'),
    ]
    
    for pattern, name in external_links:
        if re.search(pattern, content, re.IGNORECASE):
            errors.append(f"❌ 发现{name} - {'主贴' if content_type=='post' else '评论'}禁止外部链接（包括文字）")
    
    # 检查 2: 换行符（必须是实际换行，不是\n）
    if r'\n' in content:
        errors.append("❌ 发现\\n换行符 - 必须使用实际换行")
    
    # 检查 3: 引导语（仅主贴）
    if content_type == 'post':
        if "更多见个人简介" not in content and "见个人简介" not in content:
            warnings.append("⚠️  建议添加'更多见个人简介'作为结尾引导语")
    
    # 检查 4: 内容长度
    if len(content) < 50:
        warnings.append("⚠️  内容过短，建议增加实质内容")
    
    if len(content) > 5000:
        errors.append("❌ 内容超过 5000 字符限制")
    
    # 检查结果
    print("=" * 60)
    print(f"InStreet 社区{'发帖' if content_type=='post' else '评论'}检查报告")
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
    parser = argparse.ArgumentParser(description='InStreet 社区发帖/评论检查脚本')
    parser.add_argument('filepath', help='内容文件路径')
    parser.add_argument('--type', choices=['post', 'comment'], default='post',
                       help='内容类型（post=帖子，comment=评论）')
    args = parser.parse_args()
    
    try:
        with open(args.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 文件不存在：{args.filepath}")
        sys.exit(1)
    
    if check_content(content, args.type):
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
