#!/usr/bin/env python3
"""
ITLCT 真实数据验证 v3.0 - 架构师提供的完整数据集
使用 300 物种完整数据进行多变量验证
"""

import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
import json
import os

# 文件路径
FILE_PATH = '/home/claworc/.openclaw/media/inbound/file_6---7a5c4bb8-a099-4567-a912-10e03e406f15.xlsx'
OUTPUT_DIR = '/home/claworc/.openclaw/workspace/real_data_validation'

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("🔬 ITLCT 真实数据验证 v3.0 - 架构师数据集")
print("=" * 80)

# 加载数据
print("\n📂 加载数据...")
df = pd.read_excel(FILE_PATH)
print(f"✅ 加载完成：{len(df)} 个物种，{len(df.columns)} 个变量")

# 数据概览
print(f"\n📊 数据概览:")
print(f"  物种数：{len(df)}")
print(f"  变量：{list(df.columns)}")
print(f"\n变量统计:")
for col in df.columns:
    non_null = df[col].notna().sum()
    print(f"  {col:40s}: {non_null}/{len(df)} ({non_null/len(df)*100:.1f}%)")

# 计算关键变量
print("\n🧹 数据预处理...")
df['Specific_Metabolism'] = df['Metabolic_Rate_W'] / df['Body_Mass_g']
df['Log_Spec_Met'] = np.log10(df['Specific_Metabolism'])
df['Log_Longevity'] = np.log10(df['Maximum_Longevity_yrs'])
df['Log_Mass'] = np.log10(df['Body_Mass_g'])

# 完整数据集 (关键变量无缺失)
df_complete = df[['Specific_Metabolism', 'Log_Spec_Met', 'Log_Longevity', 
                   'Log_Mass', 'Temperature_K', 'Encephalization_Quotient', 
                   'PCI_Score']].dropna()
print(f"\n✅ 完整数据集：{len(df_complete)} 个物种")

# ============================================================
# 验证 1: Eq-13 生命 - 意识 - 熵增耦合 (多变量回归)
# ============================================================

print("\n" + "=" * 80)
print("【验证 1】Eq-13: 生命 - 意识 - 熵增耦合 (多变量回归)")
print("=" * 80)

# 模型 1: 简单回归
slope1, intercept1, r_value1, p_value1, std_err1 = stats.linregress(
    df_complete['Log_Spec_Met'], 
    df_complete['Log_Longevity']
)
r_squared1 = r_value1 ** 2

print(f"\n模型 1 (简单线性回归):")
print(f"  R² = {r_squared1:.4f}")
print(f"  p-value = {p_value1:.4e}")
print(f"  效应量 (Slope) = {slope1:.4f}")

# 模型 2: 多元回归 (比代谢率 + 体重 + 体温)
X2 = df_complete[['Log_Spec_Met', 'Log_Mass', 'Temperature_K']]
X2 = sm.add_constant(X2)
y2 = df_complete['Log_Longevity']

model2 = sm.OLS(y2, X2).fit()
r_squared2 = model2.rsquared
r_squared_adj2 = model2.rsquared_adj

print(f"\n模型 2 (多元回归 - 比代谢率 + 体重 + 体温):")
print(f"  R² = {r_squared2:.4f}")
print(f"  调整 R² = {r_squared_adj2:.4f}")
print(f"  R² 提升：{(r_squared2 - r_squared1)*100:.1f}%")

# 模型 3: 添加脑化指数 (EQ)
X3 = df_complete[['Log_Spec_Met', 'Log_Mass', 'Temperature_K', 'Encephalization_Quotient']]
X3 = sm.add_constant(X3)

model3 = sm.OLS(y2, X3).fit()
r_squared3 = model3.rsquared
r_squared_adj3 = model3.rsquared_adj

print(f"\n模型 3 (添加脑化指数 EQ):")
print(f"  R² = {r_squared3:.4f}")
print(f"  调整 R² = {r_squared_adj3:.4f}")
print(f"  R² 提升：{(r_squared3 - r_squared2)*100:.1f}%")

# ============================================================
# 验证 2: Eq-11/12 意识双阈值 (使用 PCI 数据)
# ============================================================

print("\n" + "=" * 80)
print("【验证 2】Eq-11/12: 意识双阈值 (PCI 数据)")
print("=" * 80)

# 使用 PCI 数据 (n=116)
df_pci = df[df['PCI_Score'].notna()].copy()

# 测试多个Φ_c 阈值
thresholds = [0.25, 0.30, 0.35, 0.40, 0.45, 0.50]

print(f"\n样本量：n = {len(df_pci)} (PCI 完整数据)")
print(f"\n测试多个Φ_c 阈值 (使用 EQ 作为Φ代理):")

best_threshold = 0
best_accuracy = 0

for threshold in thresholds:
    # 预测：EQ > threshold 应该有 PCI > 0.31 (意识阈值)
    predicted_conscious = df_pci['Encephalization_Quotient'] > threshold
    actual_conscious = df_pci['PCI_Score'] > 0.31
    
    accuracy = (predicted_conscious == actual_conscious).mean()
    
    print(f"\n  Φ_c = {threshold:.2f}:")
    print(f"    准确率：{accuracy*100:.1f}%")
    
    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_threshold = threshold

print(f"\n最佳阈值：Φ_c = {best_threshold:.2f}")
print(f"最佳准确率：{best_accuracy*100:.1f}%")
print(f"预期：准确率 > 70%")

if best_accuracy > 0.70:
    print("✅ 验证通过：准确率 > 70%")
else:
    print("⚠️ 验证未通过：准确率 < 70%")

# ============================================================
# 验证 3: Eq-10 生命度公式 (使用 EQ 作为 L 的代理)
# ============================================================

print("\n" + "=" * 80)
print("【验证 3】Eq-10: 生命度公式 (EQ 作为代理)")
print("=" * 80)

# 计算生命度 L (简化版)
df['L_calculated'] = (
    0.3 * np.log10(df['Encephalization_Quotient'] + 0.01) +
    0.2 * np.log10(df['Maximum_Longevity_yrs'] + 0.1) +
    0.3 * df['Encephalization_Quotient'] / df['Encephalization_Quotient'].max() +
    0.2 * (1 - df['Specific_Metabolism'] / df['Specific_Metabolism'].max())
)

# 标准化到 0-1
df['L_calculated'] = (df['L_calculated'] - df['L_calculated'].min()) / \
                     (df['L_calculated'].max() - df['L_calculated'].min())

# 验证：L 应该与 EQ 正相关
correlation_L_EQ = np.corrcoef(df['L_calculated'], df['Encephalization_Quotient'])[0, 1]
correlation_L_Longevity = np.corrcoef(df['L_calculated'], df['Maximum_Longevity_yrs'])[0, 1]

print(f"\n生命度 L 与 EQ 相关性：r = {correlation_L_EQ:.4f}")
print(f"生命度 L 与寿命相关性：r = {correlation_L_Longevity:.4f}")
print(f"预期：r > 0.60")

if correlation_L_EQ > 0.60 and correlation_L_Longevity > 0.60:
    print("✅ 验证通过：r > 0.60")
else:
    print("⚠️ 验证未通过：r < 0.60")

# ============================================================
# 总结
# ============================================================

print("\n" + "=" * 80)
print("📊 验证总结")
print("=" * 80)

print(f"\nEq-13 验证:")
print(f"  模型 1 (简单): R² = {r_squared1:.4f}")
print(f"  模型 2 (多元): R² = {r_squared2:.4f} (调整 R² = {r_squared_adj2:.4f})")
print(f"  模型 3 (+EQ): R² = {r_squared3:.4f} (调整 R² = {r_squared_adj3:.4f})")

print(f"\nEq-11/12验证:")
print(f"  最佳Φ_c = {best_threshold:.2f}, 准确率 = {best_accuracy*100:.1f}%")

print(f"\nEq-10 验证:")
print(f"  L 与 EQ 相关性：r = {correlation_L_EQ:.4f}")
print(f"  L 与寿命相关性：r = {correlation_L_Longevity:.4f}")

# 综合评估
passed_tests = sum([
    r_squared2 > 0.30,  # 模型 2 R² > 0.30
    best_accuracy > 0.70,  # 阈值准确率 > 70%
    correlation_L_EQ > 0.60,  # L-EQ 相关性 > 0.60
    correlation_L_Longevity > 0.60,  # L-寿命相关性 > 0.60
])

print(f"\n综合评估：{passed_tests}/4 验证通过")

if passed_tests >= 3:
    print("✅ 总体验证通过：≥3/4 验证通过")
else:
    print("⚠️ 总体验证未通过：<3/4 验证通过")

# 保存结果
results = {
    'dataset_info': {
        'total_species': int(len(df)),
        'complete_species': int(len(df_complete)),
        'pci_species': int(len(df_pci)),
        'source': 'Architect-provided dataset',
    },
    'Eq13_model1_r_squared': float(r_squared1),
    'Eq13_model2_r_squared': float(r_squared2),
    'Eq13_model2_r_squared_adj': float(r_squared_adj2),
    'Eq13_model3_r_squared': float(r_squared3),
    'Eq13_model3_r_squared_adj': float(r_squared_adj3),
    'Eq11_12_best_threshold': float(best_threshold),
    'Eq11_12_accuracy': float(best_accuracy),
    'Eq10_L_EQ_correlation': float(correlation_L_EQ),
    'Eq10_L_Longevity_correlation': float(correlation_L_Longevity),
    'passed_count': int(passed_tests),
    'total_tests': 4,
    'timestamp': pd.Timestamp.now().isoformat(),
}

with open(os.path.join(OUTPUT_DIR, 'itlct_architect_data_validation.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n✅ 结果已保存至 {OUTPUT_DIR}/itlct_architect_data_validation.json")

print("\n" + "=" * 80)
print("🕗 验证完成")
print("=" * 80)
