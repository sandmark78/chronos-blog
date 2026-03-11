# Scrapling Search Skill — 自适应网页搜索技能

> "免费、强大、抗反爬的网页搜索工具"

## 技能描述

基于 [Scrapling](https://github.com/D4Vinci/Scrapling) 构建的自适应网页搜索技能，用于：
- 从任意网站提取结构化数据
- 绕过反爬虫系统（Cloudflare Turnstile 等）
- 自适应网站结构变化
- 支持并发爬取和断点续传

## 安装

```bash
cd /home/claworc/.openclaw/workspace
python3 -m venv scrapling_env
./scrapling_env/bin/pip install scrapling curl_cffi browserforge
```

## 使用方法

### 基础使用

```python
from scrapling.fetchers import Fetcher

# 简单请求
response = Fetcher.get('https://example.com')
title = response.css('title::text').get()
links = response.css('a::attr(href)').getall()
```

### 高级功能

```python
from scrapling.fetchers import StealthyFetcher, DynamicFetcher

# 绕过反爬虫
page = StealthyFetcher.get('https://protected-site.com', headless=True)

# 动态网站（需要 JavaScript）
page = DynamicFetcher.get('https://spa-site.com', headless=True, network_idle=True)

# 自适应选择（网站结构变化后仍能定位元素）
products = page.css('.product', adaptive=True)
```

### Spider 爬虫

```python
from scrapling.spiders import Spider, Response

class MySpider(Spider):
    name = "demo"
    start_urls = ["https://example.com/"]
    
    async def parse(self, response: Response):
        for item in response.css('.product'):
            yield {"title": item.css('h2::text').get()}

MySpider().start()
```

## 选择器语法

| 类型 | 语法 | 示例 |
|------|------|------|
| CSS | `css()` | `response.css('.class::text').get()` |
| XPath | `xpath()` | `response.xpath('//div/text()').get()` |
| 正则 | `re()` | `response.re(r'\d+')` |
| 文本搜索 | `search()` | `response.search('keyword')` |

## 在 Chronos Lab 中的应用

### Hermes 信息搜集

```python
# 搜索学术论文
from scrapling.fetchers import Fetcher

def search_arxiv(query):
    url = f"https://arxiv.org/search/?query={query}&searchtype=all"
    response = Fetcher.get(url)
    papers = []
    for result in response.css('.arxiv-result'):
        papers.append({
            'title': result.css('.title::text').get(),
            'authors': result.css('.authors::text').get(),
            'abstract': result.css('.abstract::text').get(),
            'link': result.css('a.abs-button::attr(href)').get()
        })
    return papers
```

### 数据收集自动化

```python
# 批量收集研究数据
def collect_research_data(sources):
    results = []
    for source in sources:
        response = Fetcher.get(source['url'])
        data = response.css(source['selector']).getall()
        results.extend(data)
    return results
```

## 配置选项

```python
# 配置自适应模式
Fetcher.configure(adaptive=True)

# 配置代理
Fetcher.configure(proxy='http://proxy:port')

# 配置重试
Fetcher.configure(retries=3)
```

## 最佳实践

1. **尊重 robots.txt** — 检查网站的爬取规则
2. **添加延迟** — 避免对服务器造成压力
3. **使用自适应** — `adaptive=True` 让爬虫更健壮
4. **保存进度** — 长时间爬取使用断点续传
5. **错误处理** — 捕获异常并重试

## 输出格式

```json
{
  "source": "网址",
  "timestamp": "2026-03-11T00:00:00Z",
  "data": [
    {
      "title": "标题",
      "content": "内容",
      "metadata": {}
    }
  ]
}
```

## 集成到 Chronos Lab

此技能已集成到 Hermes Agent，用于：
- 自动搜索学术论文（arXiv）
- 收集研究数据
- 监控网站更新
- 批量提取信息

### 使用示例

```bash
# arXiv 搜索
./scrapling_env/bin/python skills/scrapling_search/search.py "time arrow entropy" arxiv 5

# 在 Python 中使用
from skills.sc rapling_search.search import AcademicSearch

searcher = AcademicSearch()
papers = searcher.search("origin of life", "arxiv", 10)
```

### Hermes Agent 调用

```python
# Chronos 调用 Hermes 进行信息搜集
hermes_search(query="time arrow thermodynamics", source="arxiv")
```

---

**技能状态:** 🟢 已安装并测试
**版本:** Scrapling v0.x + curl_cffi
**依赖:** Python 3.10+
**测试:** arXiv API ✅
