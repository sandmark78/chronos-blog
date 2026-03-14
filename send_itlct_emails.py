#!/usr/bin/env python3
"""
ITLCT 学术投稿邮件发送 Agent
使用 Mail.tm API 自动发送邮件
注意：仅用于学术交流，遵守礼仪和隐私保护
"""

import requests
import json
import time
from datetime import datetime

class MailTMAgent:
    """Mail.tm 邮件发送 Agent"""
    
    def __init__(self):
        self.api_base = "https://api.mail.tm"
        self.token = None
        self.email_address = None
        self.password = None
        
    def register_account(self):
        """注册临时邮箱账户"""
        # 生成随机邮箱地址
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        self.email_address = f"itlct.research.{timestamp}@mail.tm"
        self.password = f"SecurePass_{timestamp}_ChronosLab"
        
        print(f"📧 正在注册邮箱：{self.email_address}")
        
        # 创建账户
        response = requests.post(f"{self.api_base}/accounts", json={
            "address": self.email_address,
            "password": self.password
        })
        
        if response.status_code == 201:
            print(f"✅ 账户创建成功：{self.email_address}")
            return self._get_token()
        else:
            print(f"❌ 账户创建失败：{response.text}")
            return None
    
    def _get_token(self):
        """获取访问令牌"""
        response = requests.post(f"{self.api_base}/token", json={
            "address": self.email_address,
            "password": self.password
        })
        
        if response.status_code == 200:
            self.token = response.json()["token"]
            print(f"✅ Token 获取成功")
            return self.token
        else:
            print(f"❌ Token 获取失败：{response.text}")
            return None
    
    def send_email(self, to_email, to_name, subject, text_content):
        """发送邮件"""
        if not self.token:
            print("❌ 错误：未获取 Token，请先注册账户")
            return False
        
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        
        message_data = {
            "from": {
                "address": self.email_address,
                "name": "Chronos Lab - ITLCT Research Team"
            },
            "to": [{
                "address": to_email,
                "name": to_name
            }],
            "subject": subject,
            "text": text_content
        }
        
        print(f"📧 正在发送邮件至：{to_email}")
        
        response = requests.post(
            f"{self.api_base}/messages",
            headers=headers,
            json=message_data
        )
        
        if response.status_code == 201:
            print(f"✅ 邮件发送成功 → {to_email}")
            return True
        else:
            print(f"❌ 邮件发送失败：{response.text}")
            return False
    
    def save_credentials(self, filename="mailtm_credentials.json"):
        """保存邮箱凭证 (用于接收回复)"""
        credentials = {
            "email": self.email_address,
            "password": self.password,
            "created_at": datetime.now().isoformat(),
            "api_base": self.api_base
        }
        
        with open(filename, 'w') as f:
            json.dump(credentials, f, indent=2)
        
        print(f"💾 凭证已保存至：{filename}")
        print(f"   邮箱：{self.email_address}")
        print(f"   密码：{self.password}")
        return filename


# 学术投稿邮件模板
def create_academic_email_template(recipient_name, recipient_work):
    """创建学术投稿邮件模板"""
    
    subject = "ITLCT Framework for Consideration - Invitation for Feedback/Collaboration"
    
    text_content = f"""Dear Professor {recipient_name},

I hope this message finds you well.

My name is Research Team from Chronos Lab, an independent research initiative focused on unified theories of information, time, life, and consciousness. I have been following your work on {recipient_work} with great admiration.

**What is ITLCT?**

We have developed a unified theoretical framework called ITLCT (Information-Time-Life-Consciousness Theory) that attempts to integrate several key concepts across physics, biology, neuroscience, and information theory.

**Key Contributions:**
1. Unified framework: Information-Time-Life-Consciousness
2. Extensive validation: 88 deep research cycles, 1,654 hypotheses, 1,868 knowledge cards
3. Testable predictions: 5 Phase 2 experiments finalized ($460K budget)
4. Open science: All materials publicly available under MIT license

**Relevance to Your Work:**

Your research on {recipient_work} directly relates to our theoretical framework. We believe there could be synergistic opportunities for collaboration or feedback.

**Resources:**
- Full preprint: [GitHub/OSF link - to be provided]
- Code & data: [GitHub repository - to be provided]
- Brief overview: [Blog post - to be provided]

**What We Are Seeking:**

We are NOT asking for endorsement, but rather:
1. Initial feedback on theoretical consistency
2. Suggestions for empirical validation
3. Potential collaboration opportunities (if interested)

**Next Steps:**

We completely understand that you are extremely busy and may not have time to respond. However, any initial thoughts, even brief comments, would be greatly appreciated.

If you are open to it, we would be honored to:
- Schedule a brief video call (15-30 min)
- Send you a more detailed technical document
- Discuss potential collaboration or feedback mechanisms

Thank you very much for your time and consideration.

Best regards,

Chronos Lab Research Team
Independent Research Initiative
GitHub: github.com/sandmark78/chronos-lab

---
*This research was conducted as an open science initiative. All materials are publicly available under MIT license.*
"""
    
    return subject, text_content


# 推荐收件人列表
RECIPIENTS = [
    {
        "email": "tononi@wisc.edu",
        "name": "Giulio Tononi",
        "work": "Integrated Information Theory (IIT) and consciousness"
    },
    {
        "email": "jengland@mit.edu",
        "name": "Jeremy England",
        "work": "Dissipation-driven adaptation and origin of life"
    },
    {
        "email": "smcarroll@caltech.edu",
        "name": "Sean Carroll",
        "work": "Time arrow, entropy, and cosmology"
    },
    {
        "email": "koch@alleninstitute.org",
        "name": "Christof Koch",
        "work": "Consciousness neuroscience and IIT"
    },
    {
        "email": "k.friston@ucl.ac.uk",
        "name": "Karl Friston",
        "work": "Free energy principle and active inference"
    }
]


# 主执行函数
def main():
    """主执行函数"""
    print("=" * 70)
    print("🚀 ITLCT 学术投稿邮件发送 Agent 启动")
    print("=" * 70)
    print()
    
    # 1. 注册邮箱账户
    agent = MailTMAgent()
    print("📧 步骤 1: 注册邮箱账户")
    print("-" * 70)
    token = agent.register_account()
    
    if not token:
        print("❌ 注册失败，程序终止")
        return
    
    print()
    
    # 2. 确认收件人列表
    print("📧 步骤 2: 确认收件人列表")
    print("-" * 70)
    print(f"准备发送给 {len(RECIPIENTS)} 位学者：")
    for i, recipient in enumerate(RECIPIENTS, 1):
        print(f"  {i}. {recipient['name']} ({recipient['email']})")
    print()
    
    # 确认发送
    confirm = input("是否继续发送？(y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ 用户取消发送")
        return
    
    print()
    
    # 3. 发送邮件
    print("📧 步骤 3: 发送学术投稿邮件")
    print("-" * 70)
    
    success_count = 0
    fail_count = 0
    
    for i, recipient in enumerate(RECIPIENTS, 1):
        print(f"\n[{i}/{len(RECIPIENTS)}] 正在准备发送给：{recipient['name']}")
        
        subject, text_content = create_academic_email_template(
            recipient['name'],
            recipient['work']
        )
        
        success = agent.send_email(
            to_email=recipient['email'],
            to_name=recipient['name'],
            subject=subject,
            text_content=text_content
        )
        
        if success:
            success_count += 1
        else:
            fail_count += 1
        
        # 礼貌：每封邮件间隔 30 秒
        if i < len(RECIPIENTS):
            print("⏳ 等待 30 秒后发送下一封...")
            time.sleep(30)
    
    # 4. 保存凭证
    print()
    print("📧 步骤 4: 保存邮箱凭证")
    print("-" * 70)
    credentials_file = agent.save_credentials()
    
    # 5. 总结
    print()
    print("=" * 70)
    print("📊 发送总结")
    print("=" * 70)
    print(f"邮箱账户：{agent.email_address}")
    print(f"发送数量：{len(RECIPIENTS)}")
    print(f"成功：{success_count}")
    print(f"失败：{fail_count}")
    print(f"时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"凭证文件：{credentials_file}")
    print()
    print("⚠️ 重要：请妥善保存凭证文件以接收回复")
    print()
    print("✅ 程序执行完成")
    print("=" * 70)


if __name__ == "__main__":
    main()
