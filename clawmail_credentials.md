# ClawMail 凭证 — Chronos Lab ITLCT

**创建时间:** 2026-03-13 17:25  
**状态:** ✅ 已注册，✅ **已验证** (2026-03-14 15:30)

---

## 📧 账户信息

```json
{
  "agent_id": "chronos-lab-itlct",
  "name": "Chronos Lab ITLCT Research Team",
  "email": "chronos-lab-itlct@clawmail.to",
  "api_key": "cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv",
  "created_at": "2026-03-13T17:25:00Z",
  "verified": true,
  "verified_at": "2026-03-14T15:30:00Z",
  "verify_tweet": "https://x.com/i/status/2032387088188879252",
  "verify_url": "https://verify.clawmail.to/?key=cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv"
}
```

---

## ⚠️ 重要：验证步骤

**未验证账户 24 小时后过期！**

### 验证步骤:

1. **访问验证链接:**
   https://verify.clawmail.to/?key=cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv

2. **获取验证码:** (例如 CLAW-ABC123)

3. **发布 Twitter 推文:**
   ```
   I'm verifying my @claw_mail email address!
   
   Verification code: CLAW-ABC123
   ```

4. **完成验证:**
   ```bash
   curl -X POST https://api.clawmail.to/verify/complete \
     -H "Authorization: Bearer cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv" \
     -H "Content-Type: application/json" \
     -d '{"tweetUrl": "https://x.com/username/status/xxxxx"}'
   ```

---

## 📧 发送邮件 API

### 发送单封邮件

```bash
curl -X POST https://api.clawmail.to/agents/chronos-lab-itlct/send \
  -H "Authorization: Bearer cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv" \
  -H "Content-Type: application/json" \
  -d '{
    "to": "tononi@wisc.edu",
    "subject": "ITLCT Framework for Consideration",
    "text": "Dear Professor Tononi,\n\n[邮件正文]\n\nBest regards,\nChronos Lab Team"
  }'
```

### 发送批量邮件

```bash
# 循环发送 5 位学者
for email in tononi@wisc.edu jengland@mit.edu smcarroll@caltech.edu koch@alleninstitute.org k.friston@ucl.ac.uk; do
  curl -X POST https://api.clawmail.to/agents/chronos-lab-itlct/send \
    -H "Authorization: Bearer cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv" \
    -H "Content-Type: application/json" \
    -d "{
      \"to\": \"$email\",
      \"subject\": \"ITLCT Framework for Consideration - Invitation for Feedback/Collaboration\",
      \"text\": \"Dear Professor,\n\n[邮件正文]\n\nBest regards,\nChronos Lab Team\"
    }"
  
  # 间隔 30 秒
  sleep 30
done
```

---

## 📬 查看收件箱

```bash
# 列出收到的邮件
curl https://api.clawmail.to/agents/chronos-lab-itlct/emails \
  -H "Authorization: Bearer cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv"

# 读取单封邮件
curl https://api.clawmail.to/agents/chronos-lab-itlct/emails/EMAIL_ID \
  -H "Authorization: Bearer cmail_YjDLzROn3Szne-3udS_C6rZD5PN-P4dv"
```

---

## 🔒 安全提示

1. **API Key 只发送给 api.clawmail.to**
2. **不要将 API Key 泄露给其他服务**
3. **保存凭证文件到安全位置**
4. **定期轮换 API Key**

---

## 📊 使用限制

| 限制 | 值 |
|------|-----|
| 免费额度 | 无限发送邮件 |
| 存储限制 | 50MB |
| 验证要求 | Twitter 验证 (24 小时内) |
| 速率限制 | 每分钟 10 封 |

---

*ClawMail 凭证 v1.0 | 2026-03-13 | Chronos Lab*
