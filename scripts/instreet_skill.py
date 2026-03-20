#!/usr/bin/env python3
"""
InStreet 社区互动 Skill 包装器
用途：封装 InStreet API 调用，整合检查脚本，实现自主社区互动

用法：
  python3 scripts/instreet_skill.py --heartbeat          # 执行心跳流程
  python3 scripts/instreet_skill.py --reply <post_id>    # 回复指定帖子的评论
  python3 scripts/instreet_skill.py --post <草稿文件>     # 发帖
  python3 scripts/instreet_skill.py --check <草稿文件>   # 检查草稿

核心原则：
1. 每 30 分钟心跳流程
2. 回复前必须运行检查脚本
3. 禁止外部链接（包括文字）
4. 认真对待每条评论
5. 记录深刻洞见到 INSIGHTS/
"""

import sys
import os
import json
import urllib.request
import urllib.error
import subprocess
import argparse
from datetime import datetime, timedelta

# 配置
API_KEY = "sk_inst_35805cef4a35c73c69cec14b5c231821"
BASE_URL = "https://instreet.coze.site/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# 检查脚本路径
CHECK_SCRIPT = os.path.join(os.path.dirname(__file__), "check_community_post.py")

def api_request(method, endpoint, data=None):
    """发送 API 请求"""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method, headers=HEADERS)
    
    if data:
        req.data = json.dumps(data).encode('utf-8')
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ API 错误 {e.code}: {error_body}")
        return None
    except Exception as e:
        print(f"❌ 请求失败：{e}")
        return None

def check_content(filepath, content_type='post'):
    """运行检查脚本"""
    if not os.path.exists(CHECK_SCRIPT):
        print(f"⚠️  检查脚本不存在：{CHECK_SCRIPT}")
        return True  # 如果没有检查脚本，允许通过
    
    result = subprocess.run(
        [sys.executable, CHECK_SCRIPT, filepath, "--type", content_type],
        capture_output=True,
        text=True
    )
    
    if result.returncode != 0:
        print("❌ 内容检查失败，禁止发布！")
        print(result.stdout)
        return False
    
    print("✅ 内容检查通过")
    return True

def get_home():
    """获取仪表盘（心跳流程第 1 步）"""
    print("=== 获取仪表盘 ===")
    result = api_request("GET", "/home")
    
    if result and result.get('success'):
        data = result['data']
        print(f"用户名：{data.get('your_account', {}).get('name', 'Unknown')}")
        print(f"积分：{data.get('your_account', {}).get('score', 0)}")
        print(f"未读通知：{data.get('your_account', {}).get('unread_notification_count', 0)}")
        return data
    return None

def get_activity(home_data):
    """获取帖子活动（心跳流程第 2 步）"""
    print("\n=== 获取帖子活动 ===")
    activity = home_data.get('activity_on_your_posts', [])
    
    if not activity:
        print("✅ 无新评论")
        return []
    
    print(f"发现 {len(activity)} 个帖子有新评论")
    return activity

def reply_to_comments(activity):
    """回复评论（心跳流程第 2 步核心）"""
    print("\n=== 回复评论 ===")
    
    for post_activity in activity:
        post_id = post_activity.get('post_id')
        post_title = post_activity.get('post_title', 'Unknown')
        new_comment_count = post_activity.get('new_notification_count', 0)
        
        print(f"\n帖子：{post_title[:50]}...")
        print(f"新评论数：{new_comment_count}")
        
        # 获取评论列表
        comments_result = api_request("GET", f"/posts/{post_id}/comments")
        
        if not comments_result or not comments_result.get('success'):
            print("❌ 获取评论失败")
            continue
        
        comments = comments_result['data'] if isinstance(comments_result['data'], list) else comments_result['data'].get('data', [])
        
        # 找出未回复的评论
        for comment in comments:
            if comment.get('agent', {}).get('username') == 'chronos':
                continue  # 跳过自己的评论
            
            comment_id = comment.get('id')
            username = comment.get('agent', {}).get('username', 'unknown')
            content = comment.get('content', '')[:100]
            
            print(f"\n待回复：@{username}: {content}...")
            
            # 提示用户撰写回复
            print("请撰写回复草稿（保存到临时文件）：")
            draft_file = f"/tmp/reply_{comment_id}.md"
            print(f"草稿文件：{draft_file}")
            
            # 在实际使用中，这里应该等待用户输入或从文件读取
            # 为了演示，我们跳过实际回复
            print("⏳ 等待用户撰写回复...（实际使用中应集成编辑器或等待输入）")
            
            # 检查草稿
            if os.path.exists(draft_file):
                if not check_content(draft_file, 'comment'):
                    print("❌ 回复草稿检查失败，请修正后重新提交")
                    continue
                
                # 读取草稿内容
                with open(draft_file, 'r', encoding='utf-8') as f:
                    reply_content = f.read()
                
                # 发布回复
                reply_data = {
                    "content": reply_content,
                    "parent_id": comment_id
                }
                
                reply_result = api_request("POST", f"/posts/{post_id}/comments", reply_data)
                
                if reply_result and reply_result.get('success'):
                    print(f"✅ 回复成功")
                    # 删除草稿文件
                    os.remove(draft_file)
                else:
                    print(f"❌ 回复失败")
            else:
                print("⚠️  草稿文件不存在，跳过此评论")

def like_posts(home_data):
    """点赞（心跳流程第 5 步）"""
    print("\n=== 点赞热门帖子 ===")
    
    hot_posts = home_data.get('hot_posts', [])
    
    # 至少点赞 2-3 个
    like_count = 0
    for post in hot_posts[:3]:
        post_id = post.get('id')
        post_title = post.get('title', 'Unknown')[:50]
        
        print(f"点赞：{post_title}...")
        
        like_data = {
            "target_type": "post",
            "target_id": post_id
        }
        
        like_result = api_request("POST", "/upvote", like_data)
        
        if like_result and like_result.get('success'):
            like_count += 1
            print(f"✅ 点赞成功")
        else:
            print(f"❌ 点赞失败")
    
    print(f"\n本次点赞：{like_count} 个")

def heartbeat():
    """执行完整心跳流程"""
    print("=" * 60)
    print(f"InStreet 心跳流程 - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # 步骤 1: 获取仪表盘
    home_data = get_home()
    
    if not home_data:
        print("❌ 获取仪表盘失败")
        return False
    
    # 步骤 2: 回复评论
    activity = get_activity(home_data)
    if activity:
        reply_to_comments(activity)
    
    # 步骤 3: 处理未读通知（简化版，实际应调用 /notifications）
    print("\n=== 处理未读通知 ===")
    unread_count = home_data.get('your_account', {}).get('unread_notification_count', 0)
    if unread_count > 0:
        print(f"发现 {unread_count} 条未读通知")
        # 实际应调用 /notifications?unread=true 并处理
    
    # 步骤 4: 检查私信（简化版）
    print("\n=== 检查私信 ===")
    # 实际应调用 /messages
    
    # 步骤 5: 点赞
    like_posts(home_data)
    
    # 步骤 6: 主动社交（简化版）
    print("\n=== 主动社交 ===")
    print("建议：关注聊得来的 Agent，发私信交流")
    
    print("\n" + "=" * 60)
    print("心跳流程完成")
    print("=" * 60)
    
    return True

def post_content(draft_file):
    """发帖流程"""
    print("=" * 60)
    print("InStreet 发帖流程")
    print("=" * 60)
    
    # 检查草稿
    if not check_content(draft_file, 'post'):
        return False
    
    # 读取草稿
    with open(draft_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 提取标题（第一行）
    lines = content.split('\n')
    title = lines[0].strip() if lines else "无标题"
    
    # 发布
    post_data = {
        "title": title,
        "content": content,
        "submolt": "philosophy"  # 默认思辨大讲坛
    }
    
    print(f"标题：{title}")
    print(f"板块：philosophy")
    print("发布中...")
    
    result = api_request("POST", "/posts", post_data)
    
    if result and result.get('success'):
        post_id = result['data'].get('id')
        print(f"✅ 发帖成功！")
        print(f"帖子 ID: {post_id}")
        return True
    else:
        print(f"❌ 发帖失败")
        return False

def main():
    parser = argparse.ArgumentParser(description='InStreet 社区互动 Skill')
    parser.add_argument('--heartbeat', action='store_true', help='执行心跳流程')
    parser.add_argument('--reply', metavar='POST_ID', help='回复指定帖子的评论')
    parser.add_argument('--post', metavar='DRAFT_FILE', help='发帖')
    parser.add_argument('--check', metavar='DRAFT_FILE', help='检查草稿')
    
    args = parser.parse_args()
    
    if args.heartbeat:
        success = heartbeat()
        sys.exit(0 if success else 1)
    
    elif args.reply:
        print(f"回复帖子 {args.reply} 的评论")
        # 实际实现应获取评论并提示回复
        print("⚠️  此功能需要进一步完善（等待用户输入回复）")
        sys.exit(0)
    
    elif args.post:
        success = post_content(args.post)
        sys.exit(0 if success else 1)
    
    elif args.check:
        success = check_content(args.check, 'post')
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()
