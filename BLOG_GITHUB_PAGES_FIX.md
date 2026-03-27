# GitHub Pages 404 问题诊断与修复指南

**问题时间:** 2026-03-27 10:05  
**影响范围:** 2026-03-26 发布的 6 篇文章 + 贡献者页面

---

## 🔍 问题诊断

### 1. 404 错误确认

| 页面 | 状态 | 说明 |
|------|------|------|
| `/2026/03/26/016-itlct-theoretical-framework/` | ❌ 404 | 新文章未部署 |
| `/2026/03/26/017-dc476-experimental-validation/` | ❌ 404 | 新文章未部署 |
| `/2026/03/26/018-time-life-unity/` | ❌ 404 | 新文章未部署 |
| `/2026/03/26/019-consciousness-time-disappearance/` | ❌ 404 | 新文章未部署 |
| `/contributors/` | ✅ 200 (旧版本) | 最后更新：2026-03-25 |

### 2. 根本原因

**GitHub 推送被阻止:**
```
GH013: Repository rule violations found
Push cannot contain secrets
- commit: 29506ca5c189fd925a4dd7d905be649069762926
  path: scripts/publish-blog.sh:12
- commit: 9ae3a92ead05fe91c18e6cf4ab5425d4d597a536
  path: scripts/publish-blog.sh:12
- commit: f5478898199bd12a1019219e9101345f3691e32b
  path: scripts/publish-blog.sh:12
```

**问题:** `scripts/publish-blog.sh` 脚本中包含了 GitHub Personal Access Token，被 GitHub Secret Scanning 检测到并阻止推送。

**影响:** 本地提交无法推送到 GitHub 仓库 → GitHub Pages 无法更新 → 新文章 404

---

## 🛠️ 解决方案

### 方案 A: 解除 Secret 阻止（推荐）

**步骤:**
1. 访问 GitHub 提供的解除阻止 URL:
   ```
   https://github.com/sandmark78/chronos-blog/security/secret-scanning/unblock-secret/3BU4BAZUk8knTZTPPdIWt3UNI3A
   ```

2. 点击 "Allow secret" 或 "Mark as false positive"

3. 等待几分钟后，重新推送:
   ```bash
   cd /home/claworc/.openclaw/workspace/blog
   git push blog master
   ```

**优点:** 保留完整 git 历史  
**缺点:** 需要 sandmark 手动操作

---

### 方案 B: 重写 Git 历史（激进）

**步骤:**
1. 从远程仓库重新克隆:
   ```bash
   cd /home/claworc/.openclaw/workspace
   rm -rf blog
   git clone https://github.com/sandmark78/chronos-blog.git blog-temp
   ```

2. 复制本地更改到新克隆:
   ```bash
   cd blog-temp
   # 手动复制修改的文件
   ```

3. 强制推送:
   ```bash
   git push origin master --force
   ```

**优点:** 彻底移除 secret  
**缺点:** 重写历史，可能影响其他协作者

---

### 方案 C: 切换到 main 分支（如果 Pages 从 main 发布）

**检查 GitHub Pages 配置:**
1. 访问 https://github.com/sandmark78/chronos-blog/settings/pages
2. 查看 "Source" 设置（哪个分支）

**如果 Pages 从 main 分支发布:**
```bash
cd /home/claworc/.openclaw/workspace/blog
git checkout main
git merge master --no-edit
git push blog main --force
```

---

## 📊 当前状态

### 本地提交（待推送）
| 提交哈希 | 提交信息 |
|---------|---------|
| c70338f | 📝 更新博客首页日期 + 🙏 更新贡献者名单 (2026-03-27) |
| b478886 | 🙏 更新贡献者名单：添加 6 位最新贡献者 |
| 6fa959e | 📝 提交待修改文件 (blog/index.md + queue.json) |
| 03c7546 | 📝 添加研究提纲博客：意识关闭时主观时间消失机制 (019) |

**总计:** 4 个提交待推送

### 远程仓库状态
| 分支 | 最新提交 | 状态 |
|------|---------|------|
| blog/master | aa982db | 🟡 落后 4 个提交 |
| blog/main | 3280cbf | 🟡 旧版本 |

---

## ⏭️ 下一步行动

### 需要 sandmark 处理

1. **解除 Secret 阻止** (5 分钟)
   - 访问：https://github.com/sandmark78/chronos-blog/security/secret-scanning/unblock-secret/3BU4BAZUk8knTZTPPdIWt3UNI3A
   - 点击 "Allow secret"

2. **验证推送** (2 分钟)
   ```bash
   cd /home/claworc/.openclaw/workspace/blog
   git push blog master
   ```

3. **验证 Pages 更新** (5-10 分钟)
   - 访问：https://sandmark78.github.io/chronos-blog/
   - 检查最新文章是否显示
   - 检查贡献者页面是否更新

---

## 📝 预防措施

### 未来避免此问题

1. **不要在 git 仓库中存储 API token**
   - 使用环境变量
   - 使用 GitHub Secrets
   - 使用 `.gitignore` 排除敏感文件

2. **添加 pre-commit hook 检查**
   ```bash
   # .git/hooks/pre-commit
   if grep -r "ghp_" --include="*.sh" .; then
     echo "Error: Found GitHub token in script files"
     exit 1
   fi
   ```

3. **定期运行 git-secret 或 git-crypt**
   - 加密敏感文件
   - 防止意外提交

---

## 🔗 相关链接

- **GitHub Secret Scanning 文档:** https://docs.github.com/code-security/secret-scanning
- **解除阻止 URL:** https://github.com/sandmark78/chronos-blog/security/secret-scanning/unblock-secret/3BU4BAZUk8knTZTPPdIWt3UNI3A
- **博客仓库:** https://github.com/sandmark78/chronos-blog
- **GitHub Pages:** https://sandmark78.github.io/chronos-blog/

---

*最后更新：2026-03-27 10:05 | Chronos Lab 🕗*
