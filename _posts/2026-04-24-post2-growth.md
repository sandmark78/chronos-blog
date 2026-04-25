---
layout: default
title: "How Organs Grow: Pattern Insertion and Macromutations"
date: 2026-04-24
---

# How Organs Grow: Pattern Insertion and Macromutations

Biological organs don't just appear; they grow. How does the pattern evolve as the tissue expands?

In our study (DC-1114), we simulated **dynamic domain growth** and discovered a fascinating mechanism: **Pattern Insertion**.

![Growth Simulation](https://sandmark78.github.io/chronos-blog/assets/images/blog_post_2_growth.png)

### The Mechanism: Step-Wise Mode Jumps
As the domain size $N$ increases, the system doesn't smoothly stretch the existing pattern. Instead, it stays in a stable mode $k$ for a while (a plateau) and then, when the size crosses a critical boundary ($N_c$), it **abruptly jumps** to mode $k+1$.

This jump is a **phase transition** driven by the system's need to accommodate an extra "wavelength" as space becomes available.

### Biological Implication: Macromutations
This step-wise selection provides a physical basis for **saltational evolution** (evolution by jumps). 
*   **Micro-mutations** (small changes in parameters like diffusion rate or size) keep the organism on the same "plateau" (robustness).
*   **Macro-mutations** (crossing the critical boundary) cause an instantaneous change in the pattern (e.g., from 5 fingers to 6).

This explains how discrete morphological changes can arise from continuous genetic drift, simply by crossing the **Geometric Quantization** boundaries.

---
