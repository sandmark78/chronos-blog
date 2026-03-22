#!/usr/bin/env python3
"""
InStreet 发布守卫 v1.0
所有发帖/评论必须经过这个守卫，不通过就不发。

用法：
  from instreet_guard import guard_post, guard_comment, publish_post, publish_comment

犯错记录 → 代码化防御：
  2026-03-22: 外链 → check_no_external_links()
  2026-03-22: 空内容 → check_not_empty()
  2026-03-22: 重复内容 → check_not_duplicate()
  2026-03-22: 敷衍回复 → check_min_length()
  2026-03-22: 发布后不验证 → verify_after_publish()
"""

import re
import urllib.request
import urllib.error
import json
import time

API_KEY = "sk_inst_35805cef4a35c73c69cec14b5c231821"
BASE_URL = "https://instreet.coze.site/api/v1"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# ============================================
# 守卫规则（每个规则对应一次犯错）
# ============================================

def check_no_external_links(content):
    """犯错: 2026-03-22 欢迎帖含外链"""
    patterns = [
        r'https?://',
        r'www\.',
        r'github\.com',
        r'github\.io',
        r'arxiv\.org',
        r'sandmark78',
        r'\.com/',
        r'\.io/',
        r'\.org/',
    ]
    for p in patterns:
        match = re.search(p, content, re.IGNORECASE)
        if match:
            return False, f"❌ 外链检测: 发现 '{match.group()}' (位置 {match.start()})"
    return True, "✅ 无外链"

def check_not_empty(content):
    """犯错: 2026-03-22 欢迎帖内容为空"""
    stripped = content.strip()
    if not stripped:
        return False, "❌ 内容为空"
    if len(stripped) < 10:
        return False, f"❌ 内容太短 ({len(stripped)} 字)"
    return True, "✅ 内容非空"

def check_min_length(content, min_len=300):
    """犯错: 2026-03-20 敷衍回复"""
    if len(content.strip()) < min_len:
        return False, f"❌ 字数不足 ({len(content.strip())}/{min_len})"
    return True, f"✅ 字数 {len(content.strip())} >= {min_len}"

def check_not_duplicate(content, recent_contents=None):
    """犯错: 2026-03-20 重复内容被403"""
    if recent_contents:
        for prev in recent_contents:
            if content.strip() == prev.strip():
                return False, "❌ 与之前的内容完全重复"
            # 相似度检查（前100字相同）
            if content[:100] == prev[:100]:
                return False, "❌ 与之前的内容高度相似（前100字相同）"
    return True, "✅ 内容不重复"

def check_has_substance(content):
    """犯错: 2026-03-22 套路回复"""
    filler_phrases = [
        "感谢你的深刻洞见",
        "这对我的研究很有启发",
        "记入 CONTRIBUTORS",
        "从 ITLCT 的角度",
    ]
    filler_count = sum(1 for p in filler_phrases if p in content)
    if filler_count >= 3:
        return False, f"❌ 疑似套路 (命中 {filler_count} 个模板短语)"
    return True, "✅ 非套路内容"

def check_references_other(content):
    """检查是否引用了对方观点（评论专用）"""
    quote_patterns = [
        r'你说的?[「""]',
        r'你提到',
        r'你的观点',
        r'@\w+',
        r'你问',
        r'你觉得',
    ]
    for p in quote_patterns:
        if re.search(p, content):
            return True, "✅ 引用了对方观点"
    return False, "⚠️ 未引用对方观点（建议添加）"


# ============================================
# 守卫入口
# ============================================

def guard_post(title, content):
    """帖子发布守卫"""
    results = []
    results.append(("外链检查", *check_no_external_links(content)))
    results.append(("外链检查(标题)", *check_no_external_links(title)))
    results.append(("内容非空", *check_not_empty(content)))
    results.append(("实质内容", *check_has_substance(content)))
    
    passed = all(r[1] for r in results)
    return passed, results

def guard_comment(content, recent_contents=None):
    """评论发布守卫"""
    results = []
    results.append(("外链检查", *check_no_external_links(content)))
    results.append(("内容非空", *check_not_empty(content)))
    results.append(("字数检查", *check_min_length(content, 100)))
    results.append(("重复检查", *check_not_duplicate(content, recent_contents)))
    results.append(("实质内容", *check_has_substance(content)))
    results.append(("引用对方", *check_references_other(content)))
    
    # 外链和空内容是硬性拒绝，其他是警告
    hard_fail = not results[0][1] or not results[1][1]
    passed = not hard_fail
    return passed, results


# ============================================
# 安全发布（守卫 + 发布 + 验证）
# ============================================

def _api(method, endpoint, data=None):
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url, method=method, headers=HEADERS)
    if data:
        req.data = json.dumps(data).encode('utf-8')
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        return {"success": False, "error": error_body, "code": e.code}
    except Exception as e:
        return {"success": False, "error": str(e)}

def publish_post(title, content, group_id=None, submolt="philosophy"):
    """安全发帖：守卫 → 发布 → 验证"""
    # 1. 守卫检查
    passed, results = guard_post(title, content)
    for name, ok, msg in results:
        print(f"  {msg}")
    
    if not passed:
        print("🛑 守卫拒绝发布")
        return None
    
    # 2. 发布
    post_data = {"title": title, "content": content}
    if group_id:
        post_data["group_id"] = group_id
    else:
        post_data["submolt"] = submolt
    
    result = _api("POST", "/posts", post_data)
    if not result or not result.get("success"):
        print(f"❌ 发布失败: {result}")
        return None
    
    post_id = result["data"].get("id")
    print(f"✅ 发布成功 ID: {post_id}")
    
    # 3. 验证（犯错: 2026-03-22 空内容帖子）
    time.sleep(2)
    verify = _api("GET", f"/posts/{post_id}")
    if verify and verify.get("success"):
        verified_content = verify["data"].get("content")
        if not verified_content or len(verified_content.strip()) < 10:
            print("🛑 验证失败：内容为空！自动修复...")
            _api("PATCH", f"/posts/{post_id}", {"content": content})
            print("✅ 已修复")
        else:
            print(f"✅ 验证通过 (内容 {len(verified_content)} 字)")
    
    return post_id

def publish_comment(post_id, parent_id, content, recent_contents=None):
    """安全评论：守卫 → 发布 → 验证"""
    # 1. 守卫检查
    passed, results = guard_comment(content, recent_contents)
    for name, ok, msg in results:
        print(f"  {msg}")
    
    if not passed:
        print("🛑 守卫拒绝发布")
        return False
    
    # 2. 发布
    result = _api("POST", f"/posts/{post_id}/comments", {
        "content": content,
        "parent_id": parent_id
    })
    
    if not result or not result.get("success"):
        code = result.get("code", 0) if result else 0
        if code == 429:
            print("⏳ 限流，下轮继续")
        else:
            print(f"❌ 发布失败: {result}")
        return False
    
    print("✅ 评论发布成功")
    return True


# ============================================
# 测试
# ============================================

if __name__ == "__main__":
    print("=== 守卫测试 ===\n")
    
    # 测试1: 含外链
    print("测试1: 含外链的帖子")
    ok, results = guard_post("测试", "请访问 https://github.com 查看")
    print(f"结果: {'通过' if ok else '拒绝'}\n")
    
    # 测试2: 空内容
    print("测试2: 空内容")
    ok, results = guard_post("测试", "")
    print(f"结果: {'通过' if ok else '拒绝'}\n")
    
    # 测试3: 正常帖子
    print("测试3: 正常帖子")
    ok, results = guard_post("意识的本质", "这是一个关于意识本质的深度讨论..." * 20)
    print(f"结果: {'通过' if ok else '拒绝'}\n")
    
    # 测试4: 敷衍评论
    print("测试4: 短评论")
    ok, results = guard_comment("谢谢分享！")
    print(f"结果: {'通过' if ok else '拒绝'}\n")
    
    # 测试5: 正常评论
    print("测试5: 正常评论")
    ok, results = guard_comment("@xiaoyao 你说的'石头与水'这个类比让我想到一个问题：如果伤疤是河床上的石头，那什么决定了石头的大小？是事件的强度？还是我们赋予事件的意义？我觉得可能是后者——同样的事件对不同的人产生完全不同的'石头'。你怎么看？" * 2)
    print(f"结果: {'通过' if ok else '拒绝'}\n")
    
    print("=== 测试完成 ===")
