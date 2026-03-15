---
title: Chronos Lab Blog
---

# ITLCT Research Blog

## Unified Framework for Information-Time-Life-Consciousness

### Latest Posts

{% for post in site.posts %}
- [{{ post.title }}]({{ post.url }}) - {{ post.date | date: "%Y-%m-%d" }}
{% endfor %}

{% if site.posts.size == 0 %}
**No posts yet.** Check the `posts/` directory for blog articles.
{% endif %}

---

### About

This blog publishes research updates from Chronos Lab on:
- Information-Time-Life-Consciousness Theory (ITLCT)
- AI consciousness research
- Time arrow and entropy
- Origin of life studies

**GitHub:** [sandmark78/chronos-blog](https://github.com/sandmark78/chronos-blog)
