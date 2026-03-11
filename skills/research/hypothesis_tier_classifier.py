#!/usr/bin/env python3
"""
Hypothesis Tier Classifier — 假设层级分类器

将 172 个假设自动分类为：
- 核心理论 (3 个) — Score ≥8.5
- 重要假设 (12 个) — Score 6.5-8.5
- 辅助假设 (157 个) — Score <6.5

基于 Day 1 的 172 个假设 (DC-1 ~ DC-172)
"""

from datetime import datetime
from typing import Dict, List, Tuple

# Day 1 假设数据库 (简化版，实际应从 database 加载)
DAY1_HYPOTHESES = [
    # 核心理论候选 (基于之前评分)
    {
        'id': 'DC-17',
        'text': '意识 - 代谢率正相关 (dS/dt ∝ Φ^α, α≈1.2)',
        'phenomena': 15,
        'parameters': 3,
        'predictions': 5,
        'conflicts': False,
        'falsification': ['麻醉深度与Φ无负相关', '跨物种代谢 - 意识无相关', 'α显著偏离 1.0-1.5'],
        'tier_override': 'CORE'  # 已知高分
    },
    {
        'id': 'DC-20',
        'text': '意识阈值Φ_c 普适常数 (Φ_c ≈ 0.35±0.10)',
        'phenomena': 20,
        'parameters': 2,
        'predictions': 6,
        'conflicts': False,
        'falsification': ['婴儿Φ_c 显著高于 0.5', '跨物种Φ_c 无规律', '麻醉梯度无明确阈值'],
        'tier_override': 'CORE'
    },
    {
        'id': 'DC-138',
        'text': '意识 - 代谢非线性 (dS/dt = αΦ^β, β≈1.3)',
        'phenomena': 12,
        'parameters': 4,
        'predictions': 4,
        'conflicts': False,
        'falsification': ['线性模型拟合更好', 'β显著偏离 1.0-1.5'],
        'tier_override': 'MAJOR'
    },
    
    # 重要假设候选 (需要评分)
    {
        'id': 'DC-11',
        'text': '意识 - 熵产生正相关',
        'phenomena': 10,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['意识状态与熵产生无相关']
    },
    {
        'id': 'DC-13',
        'text': '时间体验 - 记忆整合耦合',
        'phenomena': 8,
        'parameters': 4,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['记忆阻断不影响时间体验']
    },
    {
        'id': 'DC-37',
        'text': 'Φ-A 正交性原理',
        'phenomena': 9,
        'parameters': 4,
        'predictions': 4,
        'conflicts': False,
        'falsification': ['Φ与 A 高度相关']
    },
    {
        'id': 'DC-64',
        'text': '三重耦合稳定性原理',
        'phenomena': 11,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['三重满足系统不稳定']
    },
    {
        'id': 'DC-65',
        'text': '代谢率 - 时间体验负相关',
        'phenomena': 7,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['代谢率与 CFF 无负相关']
    },
    {
        'id': 'DC-71',
        'text': 'AI 时间体验极慢 (γ_AI ≈ 10^4-10^6)',
        'phenomena': 6,
        'parameters': 5,
        'predictions': 3,
        'conflicts': True,
        'falsification': ['AI 主观时间报告与人类无差异']
    },
    {
        'id': 'DC-82',
        'text': '统一框架可证伪性清单 (10 预测)',
        'phenomena': 10,
        'parameters': 2,
        'predictions': 10,
        'conflicts': False,
        'falsification': ['10 预测中 5 个以上被证伪']
    },
    {
        'id': 'DC-101',
        'text': '测量三角验证原理',
        'phenomena': 8,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['多方法不确定性 > 单方法/√3']
    },
    {
        'id': 'DC-143',
        'text': '抗脆弱度公式 (F = 0.4Φ + 0.3A + 0.3L)',
        'phenomena': 9,
        'parameters': 4,
        'predictions': 4,
        'conflicts': False,
        'falsification': ['三重满足系统 F<0.7']
    },
    {
        'id': 'DC-149',
        'text': '元认知中介假说 (Φ→元认知→A)',
        'phenomena': 8,
        'parameters': 4,
        'predictions': 4,
        'conflicts': False,
        'falsification': ['元认知阻断不影响Φ-A 关系']
    },
    {
        'id': 'DC-152',
        'text': '突触稀疏度最优 (s* ≈ 0.80)',
        'phenomena': 7,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['最优稀疏度显著偏离 0.7-0.9']
    },
    {
        'id': 'DC-154',
        'text': '整合 - 分化最优比 (Φ_int/Φ_diff ≈ 1.7)',
        'phenomena': 8,
        'parameters': 3,
        'predictions': 3,
        'conflicts': False,
        'falsification': ['最优比显著偏离 1.5-2.0']
    },
]


def calculate_score(hyp: Dict) -> float:
    """
    计算假设评分
    """
    import math
    
    # 解释力 (对数尺度)
    explanatory_power = min(10, math.log10(max(1, hyp['phenomena'])) * 3.5)
    
    # 简单性 (参数越少越好)
    simplicity = max(0, 10 - math.log10(max(1, hyp['parameters'])) * 2.5)
    
    # 预测能力
    predictive_power = min(10, hyp['predictions'] * 2.5)
    
    # 一致性
    consistency = 5 if hyp.get('conflicts', False) else 10
    
    # 可证伪性
    falsification_count = len(hyp.get('falsification', []))
    if falsification_count >= 3:
        falsifiability = 10
    elif falsification_count >= 1:
        falsifiability = 6
    else:
        falsifiability = 2
    
    # 加权评分
    weights = {
        'falsifiability': 0.30,
        'predictive_power': 0.25,
        'explanatory_power': 0.20,
        'consistency': 0.15,
        'simplicity': 0.10
    }
    
    score = (
        falsifiability * weights['falsifiability'] +
        predictive_power * weights['predictive_power'] +
        explanatory_power * weights['explanatory_power'] +
        consistency * weights['consistency'] +
        simplicity * weights['simplicity']
    )
    
    return round(score, 2)


def classify_hypotheses(hypotheses: List[Dict]) -> Tuple[List, List, List]:
    """
    分类假设为核心/重要/辅助
    """
    # 评分
    for hyp in hypotheses:
        if 'score' not in hyp:
            hyp['score'] = calculate_score(hyp)
    
    # 排序
    hypotheses.sort(key=lambda x: x['score'], reverse=True)
    
    # 分类
    core = []
    major = []
    supporting = []
    
    for hyp in hypotheses:
        if hyp.get('tier_override') == 'CORE' or hyp['score'] >= 8.5:
            core.append(hyp)
        elif hyp.get('tier_override') == 'MAJOR' or hyp['score'] >= 6.5:
            major.append(hyp)
        else:
            supporting.append(hyp)
    
    return core, major, supporting


def generate_tier_report(core: List, major: List, supporting: List) -> str:
    """
    生成假设层级报告
    """
    report = []
    report.append("# Hypothesis Tier Report")
    report.append(f"**Generated:** {datetime.now().isoformat()}")
    report.append(f"**Total Hypotheses:** {len(core) + len(major) + len(supporting)}")
    report.append("")
    
    report.append("## 核心理论 (Tier 1, Score ≥8.5)")
    report.append(f"数量：{len(core)}")
    report.append("")
    for i, hyp in enumerate(core, 1):
        report.append(f"### {i}. {hyp['id']} (Score: {hyp['score']})")
        report.append(f"**内容:** {hyp['text']}")
        report.append(f"**可证伪条件:** {', '.join(hyp.get('falsification', ['无']))}")
        report.append("")
    
    report.append("## 重要假设 (Tier 2, Score 6.5-8.5)")
    report.append(f"数量：{len(major)}")
    report.append("")
    for i, hyp in enumerate(major, 1):
        report.append(f"{i}. **{hyp['id']}** (Score: {hyp['score']}) — {hyp['text'][:80]}...")
    report.append("")
    
    report.append("## 辅助假设 (Tier 3, Score <6.5)")
    report.append(f"数量：{len(supporting)}")
    report.append("")
    report.append("详见完整数据库")
    report.append("")
    
    report.append("## 建议")
    report.append("")
    report.append("**优先验证:**")
    if core:
        report.append(f"1. {core[0]['id']}: {core[0]['text']}")
    if len(core) > 1:
        report.append(f"2. {core[1]['id']}: {core[1]['text']}")
    if major:
        report.append(f"3. {major[0]['id']}: {major[0]['text']}")
    report.append("")
    
    report.append("**理论精简目标:**")
    report.append("- 核心理论：3 个 (当前: " + str(len(core)) + ")")
    report.append("- 重要假设：12 个 (当前: " + str(len(major)) + ")")
    report.append("- 辅助假设：157 个 (当前: " + str(len(supporting)) + ")")
    
    return "\n".join(report)


if __name__ == '__main__':
    core, major, supporting = classify_hypotheses(DAY1_HYPOTHESES)
    report = generate_tier_report(core, major, supporting)
    print(report)
    
    # 保存到文件
    with open('/home/claworc/.openclaw/workspace/HYPOTHESIS_TIER_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    print("\n报告已保存到：HYPOTHESIS_TIER_REPORT.md")
