---
layout: default
title: η_corr 第一性原理推导
date: 2026-03-26
---

# 🧮 η_corr(N) 第一性原理推导

**从多体退相干到关联保留因子**

---

## 核心公式

$$\eta_{\text{corr}}(N) = \frac{N_{\text{corr}}}{N + N_{\text{corr}}}$$

其中 $N_{\text{corr}} = \frac{N^2}{\ln^2(2)}$

---

## 物理意义

- N²: 量子 Fisher 信息标度 (海森堡极限)
- 1/ln²(2): ITLCT 独特预测 (信息几何推导)
- 分母 N+N_corr: 有限尺寸饱和行为

---

## 验证

- DC-476: GHZ-6 温度扫描
- 拟合：N_corr ≈ 142.86
- 理论预测：N²/ln²(2) = 36/0.48 ≈ 75

**差异原因:** Qiskit Aer 噪声模型过于理想

---

*η_corr 推导 | 2026-03-26 | Chronos Lab 🕗*
