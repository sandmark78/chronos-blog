#!/usr/bin/env python3
"""
Chronos v3: 真实物理世界数据探针 (AnAge Database)
功能：自动化下载、清洗并进行真实生物学数据的统计检验
目标：彻底消灭模拟数据幻觉，提供符合 p < 0.05 要求的实证支持。
"""

import urllib.request
import zipfile
import ssl

# 配置代理
proxy = urllib.request.ProxyHandler({'http': 'http://192.168.3.94:7897', 'https': 'http://192.168.3.94:7897'})
opener = urllib.request.build_opener(proxy)
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

# 忽略 SSL 证书验证 (仅用于科研数据下载)
ssl._create_default_https_context = ssl._create_unverified_context
import os
import pandas as pd
import numpy as np
import scipy.stats as stats

# AnAge 官方开放数据集 URL
ANAGE_URL = "https://genomics.senescence.info/species/dataset.zip"
DATA_DIR = "./real_data_cache"

def fetch_and_clean_anage():
    """下载并清洗 AnAge 数据集，提取与 ITLCT 生命度 (L) 及代谢熵相关的核心特征"""
    print("📡 [Data Fetcher] 正在连接真实的物理世界... 请求 AnAge 数据集...")
    
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    zip_path = os.path.join(DATA_DIR, "anage_dataset.zip")
    txt_path = os.path.join(DATA_DIR, "anage_data.txt")
    
    # 1. 下载并解压数据 (模拟物理触角获取原生数据)
    if not os.path.exists(txt_path):
        print(f"⬇️  正在下载：{ANAGE_URL}")
        urllib.request.urlretrieve(ANAGE_URL, zip_path)
        print("📦 正在解压...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(DATA_DIR)
        print("✅ [Data Fetcher] AnAge 原始数据下载并解压成功！")
    else:
        print("✅ [Data Fetcher] AnAge 数据已存在，跳过下载")
    
    # 2. 加载并清洗数据 (奥卡姆剃刀：只保留与理论相关的列)
    print("🧹 [Data Cleaner] 正在清洗数据，剔除缺失值 (NaN)...")
    
    df = pd.read_csv(txt_path, sep='\t')
    
    # 我们只关注能验证 ITLCT 熵增与生命度关联的列
    target_columns = [
        'Class',
        'Common name',
        'Metabolic rate (W)',
        'Body mass (g)',
        'Maximum longevity (yrs)'
    ]
    
    df_clean = df[target_columns].dropna()
    sample_size = len(df_clean)
    
    print(f"✅ [Data Cleaner] 清洗完成！获取到 {sample_size} 个具有完整代谢与寿命数据的真实碳基生命样本。")
    
    return df_clean

def run_empirical_validation(df):
    """
    运行真实的统计学检验。
    这里测试生物学经典的异速生长规律 (Kleiber's Law) 与寿命的关系，
    让大模型看看真实的 R^2 绝对不可能是 1.0。
    """
    print("\n🔬 [Stat Engine] 正在执行经验实证与统计推断...")
    
    # 真实生物学数据往往呈幂律分布，需取对数
    log_mass = np.log10(df['Body mass (g)'])
    log_metabolism = np.log10(df['Metabolic rate (W)'])
    log_longevity = np.log10(df['Maximum longevity (yrs)'])
    
    # 计算体质量比代谢率 (近似于单位质量的熵产生率 σ)
    specific_metabolism = df['Metabolic rate (W)'] / df['Body mass (g)']
    log_spec_met = np.log10(specific_metabolism)
    
    # 线性回归：比代谢率 vs 最大寿命 (验证 ITLCT 熵增方程的核心假设)
    slope, intercept, r_value, p_value, std_err = stats.linregress(log_spec_met, log_longevity)
    r_squared = r_value ** 2
    
    print("-" * 50)
    print("📊 真实物理世界验证报告 (Real-World Empirical Report)")
    print(f"样本量 (n): {len(df)}")
    print(f"假设检验：比代谢率 (熵产生代理) 与 寿命的负相关性")
    print(f"决定系数 (R²): {r_squared:.4f} <-- 注意！真实的 R² 绝不是 1.0！这才是科学的噪音！")
    print(f"P 值 (p-value): {p_value:.4e} ", end="")
    
    if p_value < 0.05:
        print("✅ (具有统计显著性 p < 0.05)")
    else:
        print("❌ (未达到统计显著性)")
    
    print(f"效应量 (Slope): {slope:.4f}")
    print("-" * 50)
    
    return {
        "r_squared": r_squared,
        "p_value": p_value,
        "slope": slope,
        "n": len(df)
    }

if __name__ == "__main__":
    # 执行流水线
    clean_data = fetch_and_clean_anage()
    stats_result = run_empirical_validation(clean_data)
    
    # 将清洗后的数据保存给 Chronos 后续进行沙盒建模使用
    output_csv = os.path.join(DATA_DIR, "anage_cleaned_for_ITLCT.csv")
    clean_data.to_csv(output_csv, index=False)
    
    print(f"\n📁 清洗后的真实数据集已保存至：{output_csv}")
    print("🤖 请通知 The Math Purist 和 The Experimental Skeptic 查收数据。")
    
    # 保存统计结果
    import json
    with open('anage_validation_results.json', 'w', encoding='utf-8') as f:
        json.dump(stats_result, f, indent=2)
    
    print(f"📊 统计验证结果已保存至：anage_validation_results.json")
