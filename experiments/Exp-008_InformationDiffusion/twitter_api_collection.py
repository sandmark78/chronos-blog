#!/usr/bin/env python3
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
