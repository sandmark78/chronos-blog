# 文献搜索执行日志 - 2026-03-11 08:20

## 任务信息
- **执行者**: Hermes (文献搜索 Agent)
- **触发**: cron job (research-literature-arxiv)
- **时间**: 2026-03-11 08:20 (Asia/Shanghai)

## 搜索任务

### 任务 1: arrow of time entropy
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_arrow_of_time_entropy.json`
- **质量评估**: ⚠️ arXiv API 返回的论文相关性较低
  - 主要返回的是 2026-03-08 的最新提交论文
  - arXiv API 按提交时间排序，而非相关性排序
  - 未找到直接讨论"时间箭头"与"熵"关系的经典论文

### 任务 2: origin of life RNA
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_origin_of_life_RNA.json`
- **质量评估**: ⚠️ arXiv API 返回的论文相关性较低
  - 同样返回的是最新提交论文
  - 未找到 RNA 世界假说、生命起源化学演化等核心文献

## 问题与改进建议

### 当前限制
1. **arXiv API 搜索算法**: 使用 `all:` 字段搜索，按提交时间排序，不保证相关性
2. **关键词匹配**: 简单关键词匹配，缺少语义理解
3. **结果过滤**: 无相关性评分或过滤机制

### 建议改进
1. **使用更精确的 arXiv 分类**: 
   - 时间/熵: `cat:physics.hist-ph` (物理学史与哲学) 或 `cat:cond-mat.stat-mech` (统计力学)
   - 生命起源: `cat:q-bio.BM` (生物分子) 或 `cat:physics.bio-ph` (生物物理)

2. **添加经典论文检索**: 
   - 考虑集成 Google Scholar API 或 Semantic Scholar API
   - 这些平台有更好的相关性排序和引用网络

3. **手动筛选关键论文**: 
   - Boltzmann 关于熵的原始工作
   - Prigogine 耗散结构理论
   - RNA World 假说核心文献 (Gilbert, 1986 等)

## 下一步行动
- [ ] 改进搜索脚本，支持 arXiv 分类过滤
- [ ] 集成 Semantic Scholar API 获取更高相关性结果
- [ ] 对已获取的论文进行人工筛选和标注
- [ ] 将关键论文添加到 knowledge/参考文献/ 目录

---

## 文献搜索执行日志 - 2026-03-11 11:22

### 任务信息
- **执行者**: Hermes (文献搜索 Agent)
- **触发**: cron job a607e20b (research-literature-arxiv)
- **时间**: 2026-03-11 11:22 (Asia/Shanghai)

### 搜索任务

#### 任务 1: arrow of time entropy
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_arrow_of_time_entropy.json`
- **质量评估**: ⚠️ arXiv API 继续返回低相关性论文
  - 返回论文主题：知识编译、超新星、暗物质、群体决策、Tetris 复杂度、LLM 诚实性、6G 频谱、生物信号模型、生成漂移、交替磁性
  - **无一篇直接讨论时间箭头或熵增方向性**
  - 确认：arXiv API 按提交时间排序，不适合主题检索

#### 任务 2: origin of life RNA
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_origin_of_life_RNA.json`
- **质量评估**: ⚠️ arXiv API 继续返回低相关性论文
  - 返回论文主题：生成模型、域适应、北极星磁场、引力子定理、CrOCl 磁性、YAG 陶瓷光谱、Transformer 修正、音视频学习、翻译语料库、中微子相互作用
  - **无一篇讨论生命起源或 RNA 世界假说**
  - 确认：arXiv API 不适合此类型检索

### 结论与建议

**核心问题**: arXiv API 的 `export.arxiv.org/api/query` 接口设计用于获取最新提交论文，而非主题相关检索。`search_query=all:query` 进行全文匹配但按 `submittedDate` 排序，导致结果与查询语义无关。

**建议行动**:
1. **改用 Semantic Scholar API** - 提供相关性排序和引用网络
2. **改用 Google Scholar** - 更好的学术检索，但需要 scraping 或 SerpAPI
3. **手动添加经典文献** - 对于时间箭头和生命起源，核心文献是已知的：
   - Boltzmann (1870s): 熵的统计解释
   - Prigogine (1970s): 耗散结构理论
   - Gilbert (1986): "The RNA World"
   - Joyce (2002): "The antiquity of RNA-based evolution"
   - Carroll: 时间箭头与宇宙学
4. **使用 arXiv 分类过滤** - 如 `cat:physics.hist-ph AND all:entropy`

**队列更新**: task_005 和 task_006 已标记为 completed，但需后续使用更好的搜索工具重新执行。

---

## 文献搜索执行日志 - 2026-03-11 11:50

### 任务信息
- **执行者**: Hermes (文献搜索 Agent)
- **触发**: cron job a607e20b (research-literature-arxiv)
- **时间**: 2026-03-11 11:50 (Asia/Shanghai)

### 搜索任务

#### 任务 1: arrow of time entropy
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_arrow_of_time_entropy.json`
- **质量评估**: ⚠️ arXiv API 继续返回低相关性论文
  - 返回论文主题：d-DNNF 编译、Ia 型超新星、暗物质再耦合、群体决策动力学、Tetris 复杂度、LLM 诚实性、6G 频谱、心电生物信号、生成漂移、交替磁性
  - **无一篇直接讨论时间箭头或熵增方向性**
  - 确认：arXiv API 按提交时间排序，不适合主题检索

#### 任务 2: origin of life RNA
- **状态**: 完成
- **结果数**: 10 篇
- **输出文件**: `problem-database/outputs/literature/search_origin_of_life_RNA.json`
- **质量评估**: ⚠️ arXiv API 继续返回低相关性论文
  - 返回论文主题：生成模型、域适应、北极星磁场、引力子定理、CrOCl 磁性、YAG 陶瓷光谱、Transformer 修正、音视频学习、翻译语料库、中微子相互作用
  - **无一篇讨论生命起源或 RNA 世界假说**
  - 确认：arXiv API 不适合此类型检索

### 结论

**重复确认**: 这是 cron job a607e20b 的第三次执行 (08:20, 11:22, 11:50)，每次结果相同——arXiv API 无法提供主题相关的学术文献检索。

**根本原因**: arXiv API (`export.arxiv.org/api/query`) 的设计目的是获取最新提交的论文，而非按相关性检索。`search_query=all:query` 进行全文匹配但按 `submittedDate` 降序排序，导致结果与查询语义无关。

**建议后续行动**:
1. **更换搜索工具** - 使用 Semantic Scholar API 或 Google Scholar (通过 SerpAPI)
2. **手动添加核心文献** - 对于 Chronos Lab 的研究方向，以下经典文献应优先添加：
   - 时间箭头：Boltzmann (1877), Prigogine (1977), Carroll (2010), Barbour (2012)
   - 生命起源：Orgel (2004), Joyce (2002), Gilbert (1986), Szostak (2012)
3. **改进搜索脚本** - 添加 arXiv 分类过滤、多源搜索、相关性评分

**队列状态**: task_005 和 task_006 已更新为 completed (11:50)，但需标记为需要更好的搜索工具重新执行。

---
*日志由 Hermes Agent 自动生成*
