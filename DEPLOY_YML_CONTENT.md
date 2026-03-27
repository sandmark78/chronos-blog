# 在 GitHub 上手动创建 deploy.yml

**访问:** https://github.com/sandmark78/chronos-blog

## 步骤

### 1. 添加文件
- 点击 "Add file" 按钮
- 选择 "Create new file"

### 2. 输入文件名
在文件名输入框中输入：
```
.github/workflows/deploy.yml
```

### 3. 粘贴以下内容

```yaml
name: Deploy ITLCT Blog

on:
  push:
    branches: [ main ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: "pages"
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Build with Jekyll
        uses: actions/jekyll-build-pages@v1
        with:
          source: ./
          destination: ./_site

      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3

  deploy:
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    runs-on: ubuntu-latest
    needs: build
    steps:
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 4. 提交
- 滚动到页面底部
- 在 "Commit new file" 框中输入提交信息：`🔧 Add GitHub Pages deployment workflow`
- 点击 "Commit new file" 按钮

### 5. 验证
等待 5-10 分钟后访问：
- https://github.com/sandmark78/chronos-blog/actions (查看 Actions 是否触发)
- https://sandmark78.github.io/chronos-blog/ (查看博客是否正常)

---

*创建时间：2026-03-27 12:28*
