---
layout: default
title: ITLCT 研究博客
---

# ITLCT 研究博客

**信息 - 时间 - 生命 - 意识统一理论框架**

> "理论不是科学。只有当一个理论可以被设计实验击败时，它才开始接近科学。"

---

## 最新文章

{% for post in site.posts limit: 10 %}
- **{{ post.date | date: "%Y-%m-%d" }}**: [{{ post.title }}]({{ site.baseurl }}{{ post.url }})
{% endfor %}

---

## 所有文章

{% for post in site.posts %}
- **{{ post.date | date: "%Y-%m-%d" }}**: [{{ post.title }}]({{ site.baseurl }}{{ post.url }})
{% endfor %}

---

*ITLCT v24.14.72 | Chronos Lab*
