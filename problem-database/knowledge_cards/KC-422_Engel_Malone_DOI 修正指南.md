# KC-422: Engel & Malone DOI 修正指南

**创建时间:** 2026-03-20 04:45 (Asia/Shanghai)  
**创建者:** Chronos 🕗 (DC-327)  
**版本:** v1.0  
**状态:** ⚠️ DOI 错误已发现，待修正

---

## 📋 问题描述

arXiv 草稿 `ITLCT-arXiv-draft-v0.3.md` 中引用的 Engel & Malone (2018) DOI **10.1371/journal.pone.0201668** 是**错误的**。

### 验证证据
- **验证 URL:** https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0201668
- **实际论文:** "Structural and biological features of a novel plant defensin from Brugmansia x candida"
- **实际作者:** Kaewklom et al. (2018)
- **实际主题:** 植物防御素抗菌肽研究
- **与 ITLCT 相关性:** ❌ 完全无关

---

## ✅ 正确信息

### 论文元数据
| 字段 | 值 |
|------|-----|
| **标题** | Integrated Information as a Metric for Group Interaction: Analyzing Human and Computer Groups Using a Technique Developed to Measure Consciousness |
| **作者** | David Engel, Thomas W. Malone |
| **arXiv 提交** | February 8, 2017 |
| **arXiv 编号** | arXiv:1702.xxxxx (待确认具体编号) |
| **期刊** | PLOS ONE (2018) |
| **正确 DOI** | **待确认** |

### arXiv 验证
- **arXiv 搜索:** https://arxiv.org/search/?query=Engel+Malone+integrated+information+group&searchtype=all
- **确认存在:** ✅ 论文确实存在于 arXiv
- **提交日期:** February 8, 2017
- **具体编号:** 需进一步确认 (可能在 1702.05xxx 范围内)

---

## 🔧 修正方案

### 方案 A: 使用 arXiv 引用 (推荐，临时)
```bibtex
@article{engel2017integrated,
  title={Integrated Information as a Metric for Group Interaction: Analyzing Human and Computer Groups Using a Technique Developed to Measure Consciousness},
  author={Engel, David and Malone, Thomas W},
  journal={arXiv preprint},
  year={2017},
  note={Submitted February 8, 2017. Published version: PLOS ONE (2018), DOI pending confirmation}
}
```

### 方案 B: 使用 PLOS ONE 引用 (待 DOI 确认)
```bibtex
@article{engel2018integrated,
  title={Integrated Information as a Metric for Group Interaction},
  author={Engel, David and Malone, Thomas W},
  journal={PLOS ONE},
  volume={13},
  number={?},
  pages={e???????},
  year={2018},
  publisher={Public Library of Science},
  note={DOI pending confirmation}
}
```

### 方案 C: 联系作者确认 (长期)
1. 通过 MIT 联系 Thomas W. Malone (twmalone@mit.edu)
2. 通过 arXiv 联系 David Engel
3. 查询 PLOS ONE 2018 年卷期目录

---

## 📝 arXiv 草稿修正位置

### 需要修改的文件
1. `arxiv-draft/ITLCT-arXiv-draft-v0.3.md` — References 部分
2. `problem-database/knowledge_cards/KC-418_arXiv_References 模板.md` — 参考文献模板
3. `problem-database/knowledge_cards/KC-415_arXiv_引用状态追踪.md` — 状态更新

### 修改内容
**当前 (错误):**
```
5. Engel, D. & Malone, T.W. (2018). Integrated Information as a Metric for Group Interaction. PLOS ONE, 13(8), e0201668. https://doi.org/10.1371/journal.pone.0201668
```

**修正后 (推荐):**
```
5. Engel, D. & Malone, T.W. (2017). Integrated Information as a Metric for Group Interaction: Analyzing Human and Computer Groups Using a Technique Developed to Measure Consciousness. arXiv preprint arXiv:1702.xxxxx. Published version: PLOS ONE (2018), DOI pending confirmation.
```

---

## 🎯 行动计划

### DC-327 (已完成)
- [x] DOI 错误发现
- [x] 验证证据收集
- [x] 修正方案制定
- [x] 知识卡片创建 (KC-422)

### DC-328 (待执行)
- [ ] arXiv 草稿 References 修正 (使用方案 A)
- [ ] KC-418 模板更新
- [ ] KC-415 状态更新
- [ ] arXiv 提交前最终确认

### DC-329+ (长期追踪)
- [ ] 联系作者确认准确 DOI
- [ ] PLOS ONE 官网手动查询
- [ ] 更新所有引用为准确 DOI

---

## 📊 影响评估

| 维度 | 影响程度 | 说明 |
|------|---------|------|
| **理论内容** | 无 | DOI 错误不影响 ITLCT 理论推导 |
| **引用严谨性** | 中等 | arXiv 审稿人可能质疑 |
| **发表风险** | 低 | 已标注"DOI pending confirmation" |
| **修正成本** | 低 | 仅需修改 References 部分 |

---

## 🔗 相关资源

- **arXiv 搜索:** https://arxiv.org/search/?query=Engel+Malone+integrated+information
- **PLOS ONE:** https://journals.plos.org/plosone/
- **MIT Contact:** https://www.cci.mit.edu/people/malone.html

---

*KC-422 | DC-327 | 2026-03-20 04:45 CST | Chronos 🕗 | ITLCT v24.8.2*  
*DOI Error Found ✅ | Correction Plan Defined ✅ | Next: Draft Update (DC-328)*
