# 🚨 GitHub Token 认证失败 - 紧急修复指南

**诊断时间:** 2026-03-27 10:35  
**状态:** GitHub Personal Access Token 已过期或被撤销

---

## 🔍 问题症状

```bash
git push origin master
# remote: Invalid username or token. Password authentication is not supported for Git operations.
# fatal: Authentication failed for 'https://github.com/sandmark78/chronos-lab.git/'
```

**影响范围:**
- ❌ chronos-lab 主仓库推送失败
- ❌ chronos-blog 博客仓库推送失败
- ❌ 所有使用 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 token 的操作

---

## 🛠️ 修复方案

### 方案 A: 生成新 Token（推荐）

**步骤:**

1. **访问 GitHub Token 设置页面**
   ```
   https://github.com/settings/tokens
   ```

2. **点击 "Generate new token (classic)"**

3. **填写信息:**
   - **Note:** `chronos-lab-2026`
   - **Expiration:** `No expiration` (或选择 1 年)
   - **Scopes:** 勾选以下权限:
     - ✅ `repo` (Full control of private repositories)
     - ✅ `workflow` (Update GitHub Action workflows)
     - ✅ `write:packages` (Upload packages to GitHub Package Registry)
     - ✅ `delete:packages` (Delete packages from GitHub Package Registry)

4. **点击 "Generate token"**

5. **复制新 Token** (只显示一次，立即复制！)
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

6. **更新本地配置:**
   ```bash
   # 清除旧凭据
   git config --global --unset credential.helper
   
   # 或者编辑凭据文件
   rm ~/.git-credentials
   
   # 使用新 token 推送一次（会提示输入用户名和密码）
   cd /home/claworc/.openclaw/workspace
   git push origin master
   # Username: sandmark78
   # Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (新 token)
   ```

---

### 方案 B: 使用 SSH（长期方案）

**步骤:**

1. **生成 SSH Key**
   ```bash
   ssh-keygen -t ed25519 -C "chronos-lab@sandmark78.github.com"
   ```

2. **添加 SSH Key 到 GitHub**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   # 复制输出内容
   ```
   
   访问: https://github.com/settings/keys
   点击 "New SSH key"，粘贴公钥

3. **更改 remote URL**
   ```bash
   cd /home/claworc/.openclaw/workspace
   git remote set-url origin git@github.com:sandmark78/chronos-lab.git
   git remote set-url blog git@github.com:sandmark78/chronos-blog.git
   ```

4. **测试连接**
   ```bash
   ssh -T git@github.com
   # 应该显示：Hi sandmark78! You've successfully authenticated
   ```

---

## 📊 当前待推送内容

**本地未推送提交:**
```
adfdd5b 🔄 更新 HEARTBEAT.md: PUA P9 行动完成 (10:33)
3b95fa4 📝 添加博客 Pages 修复总结 (分支不匹配问题)
```

**待部署博客内容:**
- 6 篇新文章 (016-021)
- .nojekyll 文件
- 更新的首页和贡献者页面

---

## ⏭️ 下一步

**需要 sandmark 处理:**

1. **生成新 Token** (5 分钟)
   - 访问 https://github.com/settings/tokens
   - 生成新 token

2. **更新凭据** (2 分钟)
   ```bash
   rm ~/.git-credentials
   cd /home/claworc/.openclaw/workspace
   git push origin master
   # 输入新 token
   ```

3. **验证博客推送** (5-10 分钟等待)
   - 推送到 blog 仓库 main 分支
   - 验证 GitHub Pages 构建

---

## 🔗 相关链接

- **Token 设置:** https://github.com/settings/tokens
- **SSH Key 设置:** https://github.com/settings/keys
- **chronos-lab 仓库:** https://github.com/sandmark78/chronos-lab
- **chronos-blog 仓库:** https://github.com/sandmark78/chronos-blog

---

*最后更新：2026-03-27 10:35 | Chronos Lab 🕗*
