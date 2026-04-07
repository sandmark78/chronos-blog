# 博客发布检查清单 v2.0

**更新日期:** 2026-04-07  
**版本:** v2.0 (图片路径修复版)

---

## ✅ 发布前检查

### 1. 文章格式检查

- [ ] Front matter 完整 (layout, title, date)
- [ ] layout: default (不是 post)
- [ ] date: YYYY-MM-DD
- [ ] 文字编码 UTF-8

### 2. 图片路径检查 ⚠️ **关键**

**正确格式:**
```markdown
![描述]({{ site.baseurl }}/images/xxx.png)
```

**错误格式:**
```markdown
![描述](/chronos-blog/assets/images/xxx.png)  ❌
![描述](/assets/images/xxx.png)               ❌
![描述](images/xxx.png)                       ❌
```

**检查命令:**
```bash
grep "!\[" blog/posts/article.md | grep -v "{{ site.baseurl }}/images/"
```

**自动修复:**
```bash
sed -i 's|/chronos-blog/assets/images/|{{ site.baseurl }}/images/|g' article.md
sed -i 's|/assets/images/|{{ site.baseurl }}/images/|g' article.md
```

### 3. 图片文件位置

**图片必须放在:** `blog/images/` 目录

**不是:** `blog/assets/images/` ❌

**发布流程:**
1. 文章中使用 `{{ site.baseurl }}/images/` 路径
2. 图片文件复制到 `blog/images/` 目录
3. 推送到 GitHub 博客仓库

---

## 🚀 发布流程

### 方法 A: 使用发布脚本 (推荐)

```bash
bash scripts/publish-blog.sh blog/posts/article.md slug-name
```

**脚本自动完成:**
1. ✅ Jekyll 格式验证
2. ✅ 文字编码检查
3. ✅ 图片路径检查 + 自动修复
4. ✅ 复制到 _posts/目录
5. ✅ 更新首页
6. ✅ 提交并推送

### 方法 B: 手动发布

```bash
# 1. 克隆博客仓库
cd /tmp
git clone https://github.com/sandmark78/chronos-blog.git
cd chronos-blog

# 2. 复制文章
cp /path/to/article.md _posts/YYYY-MM-DD-slug.md

# 3. 复制图片
cp /path/to/images/*.png images/

# 4. 提交推送
git add -A
git commit -m "📝 发布新文章：文章标题"
git push origin main
```

---

## 📊 图片路径对照表

| 文章中的路径 | 渲染后的 URL | 状态 |
|-------------|-------------|------|
| `{{ site.baseurl }}/images/xxx.png` | `/chronos-blog/images/xxx.png` | ✅ 正确 |
| `/chronos-blog/assets/images/xxx.png` | `/chronos-blog/assets/images/xxx.png` | ❌ 404 |
| `/assets/images/xxx.png` | `/chronos-blog/assets/images/xxx.png` | ❌ 404 |
| `images/xxx.png` | `/chronos-blog/images/xxx.png` | ⚠️ 相对路径，不推荐 |

---

## 🔧 常见问题

### Q1: 图片不显示，404 错误

**原因:** 图片路径不正确 或 图片文件未上传

**解决:**
1. 检查文章中的图片路径是否为 `{{ site.baseurl }}/images/`
2. 检查图片文件是否在 `images/` 目录
3. 确认已推送到 GitHub

### Q2: 首页没有更新

**原因:** 文章 slug 与首页链接不匹配

**解决:**
1. 检查 `_config.yml` 中的 permalink 格式
2. 确认首页链接格式与 permalink 一致
3. 当前使用 `/:title.html` 格式

### Q3: 中文乱码

**原因:** 文件编码不是 UTF-8

**解决:**
```bash
# 检查编码
file -bi article.md

# 转换为 UTF-8
iconv -f GBK -t UTF-8 article.md -o article_utf8.md
```

---

## 📝 发布后验证

### 1. 检查文章页面

```
https://sandmark78.github.io/chronos-blog/slug.html
```

- [ ] 文章标题正确
- [ ] 文字无乱码
- [ ] 图片正常显示
- [ ] 格式排版正常

### 2. 检查首页

```
https://sandmark78.github.io/chronos-blog/
```

- [ ] 新文章出现在列表顶部
- [ ] 链接正确跳转到文章
- [ ] 所有旧文章链接正常

### 3. 检查图片 CDN

```
https://sandmark78.github.io/chronos-blog/images/xxx.png
```

- [ ] 图片可以独立访问
- [ ] 图片大小正常
- [ ] 图片内容正确

---

## 🎯 最佳实践

### 1. 图片命名规范

```
YYYY-MM-DD-描述.png  (推荐)
文章 slug-序号.png    (也可)
```

**示例:**
```
2026-04-04-pred1.png
dc565-01-phi-prime-concept.png
poc-01-blog-homepage.png
```

### 2. 图片数量建议

- 科普文章：3-5 张
- 技术文章：5-9 张
- 论文级文章：9-15 张

### 3. 图片大小控制

- 单张 < 10MB (GitHub 限制)
- 推荐 2-6MB (加载速度)
- 使用 2688×1536 (16:9) 或 1920×1080

---

## 📚 相关文档

- [DEPLOYMENT.md](DEPLOYMENT.md) — 完整部署指南
- [QUICK_DEPLOY.md](QUICK_DEPLOY.md) — 快速发布清单
- [publish-blog.sh](../scripts/publish-blog.sh) — 发布脚本源码

---

*最后更新：2026-04-07 | Chronos Lab*
