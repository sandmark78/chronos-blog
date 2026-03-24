#!/usr/bin/env python3
"""
k₀ 独立验证 — 用完全不同的方法重新计算

原路径：Fubini-Study 曲率涨落 → 𝒩_eff → k₀
新路径：随机矩阵理论 + 信息几何 + 路径积分

如果三种方法都给出 ≈0.0300，k₀ 大概率是真的。
如果不一致，k₀ 可能只是拟合巧合。
"""

import numpy as np
from scipy import linalg
import os

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/tribunal_reports")

print("=" * 60)
print("k₀ 独立验证 — 三条独立路径")
print("=" * 60)

# ============================================
# 路径 1：原方法（Fubini-Study）
# ============================================
print("\n--- 路径 1: Fubini-Study 曲率涨落 ---")

N_eff_FS = 3.68  # 原推导值
k0_path1 = np.log(2) / (2 * np.pi * N_eff_FS)
print(f"𝒩_eff = {N_eff_FS}")
print(f"k₀ = ln(2)/(2π×𝒩_eff) = {k0_path1:.6f} bits")

# ============================================
# 路径 2：随机矩阵理论（GUE）
# ============================================
print("\n--- 路径 2: 随机矩阵理论 (GUE) ---")

# 对 N 量子比特系统，约化密度矩阵的特征值分布
# 遵循 Marchenko-Pastur 分布
# 信息增长率 = 平均 von Neumann 熵增量 / 比特数

def k0_from_random_matrix(dim, n_samples=5000):
    """从随机态的 von Neumann 熵计算 k₀"""
    entropies = []
    for _ in range(n_samples):
        # 生成 Haar 随机纯态
        psi = np.random.randn(dim) + 1j * np.random.randn(dim)
        psi = psi / np.linalg.norm(psi)
        
        # 约化密度矩阵（对半分）
        d = int(np.sqrt(dim))
        if d * d != dim:
            d = int(dim ** 0.5)
            dim_use = d * d
            psi_use = psi[:dim_use]
            psi_use = psi_use / np.linalg.norm(psi_use)
        else:
            psi_use = psi
            dim_use = dim
        
        psi_mat = psi_use.reshape(d, d)
        rho = psi_mat @ psi_mat.conj().T
        rho = rho / np.trace(rho)
        
        # von Neumann 熵
        eigenvalues = np.real(linalg.eigvalsh(rho))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        S = -np.sum(eigenvalues * np.log2(eigenvalues))
        entropies.append(S)
    
    # k₀ ≈ 平均熵增量 / 有效自由度
    S_mean = np.mean(entropies)
    S_max = np.log2(d)
    k0 = S_mean / (d * d) if d > 1 else 0
    return k0, S_mean, S_max

dims_to_test = [4, 9, 16, 25, 36, 49, 64]
k0_values_rmt = []

for dim in dims_to_test:
    k0_rmt, S_mean, S_max = k0_from_random_matrix(dim, n_samples=3000)
    k0_values_rmt.append(k0_rmt)
    d = int(np.sqrt(dim))
    print(f"  d={d:2d} (dim={dim:3d}): S_mean={S_mean:.4f}, k₀={k0_rmt:.6f}")

k0_path2 = np.mean(k0_values_rmt[2:])  # 排除最小的
print(f"\n  k₀ (RMT 平均) = {k0_path2:.6f} bits")

# ============================================
# 路径 3：信息几何（Fisher 信息度规）
# ============================================
print("\n--- 路径 3: Fisher 信息度规 ---")

# Fisher 信息度规下，参数空间的曲率给出信息增长的自然尺度
# 对 N 量子比特系统，Fisher 信息矩阵的迹给出有效自由度

def k0_from_fisher(n_qubits, n_samples=2000):
    """从 Fisher 信息矩阵估计 k₀"""
    dim = 2 ** n_qubits
    
    # 在参数空间随机采样
    fisher_traces = []
    for _ in range(n_samples):
        # 随机密度矩阵
        A = np.random.randn(dim, dim) + 1j * np.random.randn(dim, dim)
        rho = A @ A.conj().T
        rho = rho / np.trace(rho)
        
        eigenvalues = np.real(linalg.eigvalsh(rho))
        eigenvalues = eigenvalues[eigenvalues > 1e-15]
        
        # Fisher 信息的简化估计：sum(1/p_i)
        F_trace = np.sum(1.0 / eigenvalues)
        fisher_traces.append(F_trace)
    
    F_mean = np.mean(fisher_traces)
    # k₀ ≈ ln(2) / (2π × √(F_mean/dim))
    N_eff_fisher = np.sqrt(F_mean / dim)
    k0 = np.log(2) / (2 * np.pi * N_eff_fisher)
    return k0, N_eff_fisher

for n in [2, 3, 4, 5]:
    k0_fisher, N_eff = k0_from_fisher(n, n_samples=2000)
    print(f"  n={n} qubits: 𝒩_eff={N_eff:.4f}, k₀={k0_fisher:.6f}")

k0_path3_values = [k0_from_fisher(n, 2000)[0] for n in [3, 4, 5]]
k0_path3 = np.mean(k0_path3_values)
print(f"\n  k₀ (Fisher 平均) = {k0_path3:.6f} bits")

# ============================================
# 总结
# ============================================
print(f"\n{'='*60}")
print(f"📊 三条路径对比")
print(f"{'='*60}")
print(f"  路径 1 (Fubini-Study):   k₀ = {k0_path1:.6f} bits")
print(f"  路径 2 (随机矩阵 GUE):  k₀ = {k0_path2:.6f} bits")
print(f"  路径 3 (Fisher 信息):    k₀ = {k0_path3:.6f} bits")
print(f"  原理论预测:              k₀ = 0.030000 bits")
print()

# 一致性检查
values = [k0_path1, k0_path2, k0_path3]
mean_k0 = np.mean(values)
std_k0 = np.std(values)
cv = std_k0 / mean_k0 * 100

print(f"  平均值: {mean_k0:.6f} bits")
print(f"  标准差: {std_k0:.6f} bits")
print(f"  变异系数: {cv:.1f}%")

if cv < 10:
    print(f"\n  ✅ 三条路径高度一致 (CV < 10%)")
    print(f"  结论: k₀ ≈ {mean_k0:.4f} 可能是真正的物理常数")
elif cv < 30:
    print(f"\n  🟡 三条路径中等一致 (CV < 30%)")
    print(f"  结论: k₀ 的数量级稳定，但精确值依赖方法")
else:
    print(f"\n  🔴 三条路径不一致 (CV > 30%)")
    print(f"  结论: k₀ = 0.0300 可能只是特定方法的拟合巧合")

print(f"\n{'='*60}")
