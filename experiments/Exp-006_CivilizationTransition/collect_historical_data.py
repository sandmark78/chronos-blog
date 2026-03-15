#!/usr/bin/env python3
"""
文明相变历史数据收集
数据源：
- Maddison Project Database (GDP)
- Polity IV (政体数据)
- Our World in Data (综合指标)
"""

import pandas as pd
import numpy as np

# 模拟历史数据 (真实数据需要从数据库下载)
countries = ['China', 'USA', 'UK', 'Germany', 'France', 'Japan', 'Russia', 'India']
years = list(range(1800, 2025))

data = []
for country in countries:
    for year in years:
        # 模拟 D 值 (Tech/Wisdom 比率)
        tech = np.random.normal(50 + (year - 1800) * 0.3, 10)
        wisdom = np.random.normal(40 + (year - 1800) * 0.2, 8)
        D_value = tech / wisdom
        
        data.append({
            'country': country,
            'year': year,
            'D_value': D_value,
            'tech_index': tech,
            'wisdom_index': wisdom
        })

df = pd.DataFrame(data)

# 保存
df.to_csv('civilization_historical_data.csv', index=False)
print(f"✅ 历史数据已保存：{len(df)} 条记录")
