#!/usr/bin/env python3
"""
Exp-006: 文明相变历史数据整理
Exp-008: 信息扩散 Twitter API 脚本
启动时间：2026-03-14 22:11
"""

import os
import json
from datetime import datetime

print("=" * 80)
print("🧪 Exp-006 & Exp-008 实验脚本部署")
print("=" * 80)

# ============================================================
# Exp-006: 文明相变历史数据整理
# ============================================================

print("\n【Exp-006】文明相变历史数据整理")
print("-" * 60)

EXP006_DIR = '/home/claworc/.openclaw/workspace/experiments/Exp-006_CivilizationTransition'
os.makedirs(EXP006_DIR, exist_ok=True)

# 创建数据整理脚本
data_collection_script = '''#!/usr/bin/env python3
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
'''

with open(os.path.join(EXP006_DIR, 'collect_historical_data.py'), 'w', encoding='utf-8') as f:
    f.write(data_collection_script)

print(f"✅ Exp-006 脚本已部署：{EXP006_DIR}")

# ============================================================
# Exp-008: 信息扩散 Twitter API 脚本
# ============================================================

print("\n【Exp-008】信息扩散 Twitter API 脚本")
print("-" * 60)

EXP008_DIR = '/home/claworc/.openclaw/workspace/experiments/Exp-008_InformationDiffusion'
os.makedirs(EXP008_DIR, exist_ok=True)

# 创建 Twitter API 脚本框架
twitter_script = '''#!/usr/bin/env python3
"""
信息扩散 Twitter 数据收集
需要 Twitter API v2 密钥
"""

import tweepy
import pandas as pd
from datetime import datetime, timedelta

# API 密钥 (需要从环境变量获取)
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
BEARER_TOKEN = "YOUR_BEARER_TOKEN"

# 认证
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# 搜索关键词
keywords = [
    "ITLCT",
    "consciousness research",
    "integrated information",
    "time arrow",
    "life origin"
]

# 时间范围
start_date = datetime.now() - timedelta(days=30)
end_date = datetime.now()

# 收集推文
tweets_data = []
for keyword in keywords:
    query = f"{keyword} -is:retweet -is:reply lang:en"
    
    tweets = client.search_recent_tweets(
        query=query,
        start_time=start_date,
        end_time=end_date,
        max_results=100
    )
    
    if tweets.data:
        for tweet in tweets.data:
            tweets_data.append({
                'id': tweet.id,
                'text': tweet.text,
                'created_at': tweet.created_at,
                'public_metrics': tweet.public_metrics
            })

# 保存数据
df = pd.DataFrame(tweets_data)
df.to_csv('twitter_diffusion_data.csv', index=False)
print(f"✅ Twitter 数据已保存：{len(df)} 条推文")
'''

with open(os.path.join(EXP008_DIR, 'twitter_api_collection.py'), 'w', encoding='utf-8') as f:
    f.write(twitter_script)

# 创建配置文件
exp008_config = {
    'experiment_id': 'Exp-008',
    'name': '信息扩散实验',
    'status': 'deployed',
    'deployment_time': datetime.now().isoformat(),
    'requirements': [
        'tweepy>=4.14.0',
        'pandas>=2.0.0',
        'Twitter API v2 密钥'
    ],
    'data_collection': {
        'keywords': keywords,
        'time_range_days': 30,
        'max_tweets_per_keyword': 100
    }
}

with open(os.path.join(EXP008_DIR, 'config.json'), 'w', encoding='utf-8') as f:
    json.dump(exp008_config, f, indent=2, ensure_ascii=False)

print(f"✅ Exp-008 脚本已部署：{EXP008_DIR}")

print("\n" + "=" * 80)
print("🎉 所有实验脚本部署完成！")
print("=" * 80)
print(f"\n部署的实验:")
print(f"  1. Exp-003: 时间体验操纵实验")
print(f"  2. Exp-006: 文明相变历史数据整理")
print(f"  3. Exp-008: 信息扩散 Twitter 数据收集")
print(f"\n✅ 今晚行动完成！")
