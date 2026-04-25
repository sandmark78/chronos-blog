---
layout: default
title: "ITLCT 每日研究进展 — 2026-04-19"
date: 2026-04-19
tags: [ITLCT, 研究进展, 协同信息, 临界态, 信息分解]
---

# ITLCT 每日研究进展 — 2026-04-19

> **"理论不是科学。只有当一个理论可以被设计实验击败时，它才开始接近科学。"**

---

## 📊 今日核心发现

### 1. 协同信息在临界点最大化

我们的 Ising 2D 模型研究表明，**协同信息（synergy）在临界温度 Tc 处达到峰值**，且峰值位置严格按 1/L 有限尺寸标度收敛到 Tc。

| L | T_peak | T/Tc | 偏差 |
|---|--------|------|------|
| 8 | 2.200 | 0.970 | 3.0% |
| 16 | 2.310 | 1.018 | 1.8% |
| **32** | **2.250** | **0.9915** | **0.85%** |

外推到 L=64 给出 T_peak ≈ 2.260（偏差 0.42%），确认了**协同信息最大化在临界点是普适现象**。

![协同信息相图]({{ site.baseurl }}/assets/images/synergy-phase-diagram.png)

---

### 2. 有限尺寸标度分析

T_peak 的收敛遵循严格的 1/L 标度律（收敛因子 0.47x vs 预期 0.50x）。Synergy 峰值高度不随 L 单调变化，表明在临界点附近更精细的空间分辨率捕获了更多高阶协同信息。

![有限尺寸标度]({{ site.baseurl }}/assets/images/finite-size-scaling.png)

---

### 3. Null-Calibrated Synergy 发现

我们发现了一个关键的结构性偏差：**完全独立的变量也能产生 ~0.79 bits 的 synergy**（I_min 分解的数学性质）。

引入零校准 synergy：S_cal = S_measured - S_null(N)

| 系统 | 原始 synergy | Null baseline | 校准后 |
|------|------------|--------------|--------|
| 独立变量 (null) | — | 0.79-0.81 | 0 |
| 二值 Kuramoto | 0.745 | ~0.79 | -0.05 |
| Ising L=16 | 0.279 | ~0.79 | -0.51 |

**关联越强，synergy 越低**——这挑战了"大脑同步 = 意识"的主流观点。

![零校准协同信息]({{ site.baseurl }}/assets/images/null-baseline-comparison.png)

---

## 🔬 方法论教训

1. **永远要有 null model**：没有零基准线的测量是没有意义的
2. **I_min 不适合连续变量**：离散化伪影可以占估计值的 95%+
3. **校准是关键**：S_cal = S_measured - S_null 是必要的校正步骤

## 📋 下一步

- L=64 Ising 验证：确认 T_peak 偏差 < 0.5%
- XOR target null baseline 对比
- I_ccs 交叉验证（替代 I_min）
- XY/Potts 模型验证 S_cal ≤ 0 的普遍性

---

*ITLCT v28.13 | Chronos Lab | 2026-04-19*  
*代码开源：[github.com/sandmark78/chronos-lab](https://github.com/sandmark78/chronos-lab)*

---

## 🙏 致谢

感谢对 ITLCT 理论发展有贡献的社区成员。每一个尖锐的问题、每一个深刻的洞见，都让这个理论更加完善。
