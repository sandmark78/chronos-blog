# Chronos Lab GitHub 私密备份设置指南

## 📋 第一步：创建私密仓库

1. 访问 https://github.com/new
2. 填写：
   - **Repository name:** `chronos-lab-backup`
   - **Description:** Chronos Lab 私密备份仓库
   - **Visibility:** 🔒 **Private**（重要！）
3. 点击 **Create repository**

---

## 🔐 第二步：配置 SSH 认证（如果没有）

```bash
# 生成 SSH key
ssh-keygen -t ed25519 -C "chronos-backup@$(hostname)"

# 查看公钥
cat ~/.ssh/id_ed25519.pub

# 添加到 GitHub:
# 1. 访问 https://github.com/settings/keys
# 2. 点击 "New SSH key"
# 3. 粘贴公钥内容
# 4. 保存
```

---

## ⚙️ 第三步：测试备份脚本

```bash
# 编辑脚本，修改 GitHub 用户名
nano /home/claworc/.openclaw/workspace/scripts/backup-to-github.sh

# 修改这一行：
GITHUB_USER="sandmark78"  # 改成你的用户名

# 测试运行
/home/claworc/.openclaw/workspace/scripts/backup-to-github.sh
```

---

## ⏰ 第四步：设置定时任务（每天凌晨 3 点）

```bash
# 编辑 crontab
crontab -e

# 添加这一行：
0 3 * * * /home/claworc/.openclaw/workspace/scripts/backup-to-github.sh >> /var/log/chronos-backup.log 2>&1

# 保存退出
```

---

## 📊 第五步：验证备份

```bash
# 查看备份日志
tail -f /var/log/chronos-backup.log

# 手动触发一次备份
/home/claworc/.openclaw/workspace/scripts/backup-to-github.sh

# 检查 GitHub 仓库
# 访问 https://github.com/sandmark78/chronos-lab-backup
```

---

## 🔒 备份内容

### ✅ 会备份
- 知识卡片 (`knowledge/`)
- 研究日志 (`knowledge/研究日志/`)
- 理论框架 (`CHRONOS*.md`)
- 实验方案
- 技能文件 (`skills/`)
- 问题数据库 (`problem-database/`)
- 文献摘要 (`literature/`)

### ❌ 不备份（敏感文件）
- `openclaw.json` — 配置文件（含 API key）
- `MEMORY.md` — 核心记忆
- `memory/` — 每日记忆
- `agents/` — Agent 配置
- `.openclaw/` — 系统目录
- `scrapling_env/` — 环境变量

---

## 🛠️ 故障排除

### 问题 1: SSH 认证失败
```bash
# 测试 SSH 连接
ssh -T git@github.com

# 如果失败，重新添加 SSH key
```

### 问题 2: 仓库不存在
```bash
# 确认仓库已创建且为 Private
# 访问 https://github.com/你的用户名/chronos-lab-backup
```

### 问题 3: 权限不足
```bash
# 确保脚本有执行权限
chmod +x /home/claworc/.openclaw/workspace/scripts/backup-to-github.sh
```

---

## 📈 备份策略

| 类型 | 频率 | 时间 |
|------|------|------|
| 自动备份 | 每日 | 凌晨 3:00 |
| 手动备份 | 按需 | `./backup-to-github.sh` |
| 保留策略 | 无限 | Git 历史 |

---

## 🎯 快速命令

```bash
# 手动备份
/home/claworc/.openclaw/workspace/scripts/backup-to-github.sh

# 查看备份状态
git -C /tmp/chronos-backup-*/ chronos-lab-backup status

# 查看备份日志
tail -50 /var/log/chronos-backup.log

# 测试 crontab
grep backup /var/log/syslog | tail -10
```

---

*设置完成后，系统将每天凌晨 3 点自动备份到 GitHub 私密仓库！*
