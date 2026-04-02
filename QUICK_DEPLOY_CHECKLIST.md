# 博客快速部署检查清单

**版本:** v1.0  
**更新日期:** 2026-04-02

---

## 🚀 标准推送流程 (每次必做)

```bash
# 1. 进入博客目录
cd /home/claworc/.openclaw/workspace/blog

# 2. 检查状态
git status

# 3. 添加所有变更
git add -A

# 4. 提交
git commit -m '📝 博客更新：描述更新内容'

# 5. 推送到 chronos-blog 仓库
git push chronos-blog main
```

**等待:** 2-3 分钟 GitHub Pages 构建

**验证:** https://sandmark78.github.io/chronos-blog/

---

## ✅ 部署前检查 (5 项)

### 1. Jekyll Front Matter

```bash
# 检查最新文章
head -10 _posts/latest-article.md

# 必须包含:
# ---
# layout: default
# title: "文章标题"
# date: YYYY-MM-DD
# ---
```

### 2. _config.yml

```bash
# 检查 repository 字段
grep "^repository:" _config.yml

# 必须是:
# repository: sandmark78/chronos-blog
```

### 3. 图片链接

```bash
# 检查格式
grep "!\[" _posts/*.md | grep -v "site.baseurl" | grep -v "http"

# 正确格式:
# ![描述]({{ site.baseurl }}/assets/images/xxx.jpg)
```

### 4. 文件编码

```bash
# 检查 UTF-8
file -bi _posts/*.md | grep -v "utf-8"

# 如果有非 UTF-8，转换:
iconv -f GBK -t utf-8 file.md -o file.md.utf8 && mv file.md.utf8 file.md
```

### 5. Git 远程仓库

```bash
# 检查远程
git remote -v

# 应该有:
# chronos-blog  https://github.com/sandmark78/chronos-blog.git (fetch/push)
```

---

## ⚠️ 常见问题 (3 个)

### 404 错误

**原因:** 缺少 front matter 或 repository 字段

**解决:**
```bash
# 检查 front matter
head -5 _posts/xxx.md

# 检查 _config.yml
grep "^repository:" _config.yml
```

### 图片不显示

**原因:** 路径错误或未使用 site.baseurl

**解决:**
```bash
# 修正链接
sed -i 's/!\[.*\](\/assets/![描述]({{ site.baseurl }}\/assets/g' _posts/xxx.md
```

### 推送失败

**原因:** 远程仓库 URL 错误

**解决:**
```bash
# 更新远程
git remote set-url chronos-blog https://github.com/sandmark78/chronos-blog.git

# 重新推送
git push chronos-blog main
```

---

## 📊 当前状态

**仓库:** chronos-blog  
**分支:** main  
**文章数:** 40+ 篇  
**图片数:** 44 张  
**最新提交:** 10 张全新 Gemini 图片入库

**博客地址:** https://sandmark78.github.io/chronos-blog/

---

*快速部署检查清单 | v1.0 | 2026-04-02*
