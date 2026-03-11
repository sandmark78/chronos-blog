#!/usr/bin/env python3
"""
Theory Score Engine — AI 科学家理论评分系统

基于奥卡姆剃刀原则 + 卡尔·波普尔可证伪性原则

评分维度：
1. 解释力 (Explanatory Power) — 能解释多少现象
2. 简单性 (Simplicity) — 假设数量/参数数量
3. 预测能力 (Predictive Power) — 可检验预测数量
4. 一致性 (Consistency) — 与现有理论兼容性
5. 可证伪性 (Falsifiability) — 是否有明确证伪条件
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

# 理论成熟度等级
class TheoryLevel:
    L0_IDEA = 0           # 想法
    L1_HYPOTHESIS = 1     # 假设
    L2_MODEL = 2          # 模型
    L3_THEORY = 3         # 理论
    L4_PREDICTIVE = 4     # 可预测理论
    L5_CONFIRMED = 5      # 已验证理论

# 假设层级
class HypothesisTier:
    CORE = "核心"         # 3个核心理论
    MAJOR = "重要"        # 12个重要假设
    SUPPORTING = "辅助"   # 30个辅助假设

def calculate_theory_score(
    explanatory_power: float,      # 0-10
    simplicity: float,              # 0-10 (越高越简洁)
    predictive_power: float,        # 0-10
    consistency: float,             # 0-10
    falsifiability: float           # 0-10
) -> Dict:
    """
    计算理论综合评分
    
    权重设计（基于科学哲学）：
    - 可证伪性：30% (波普尔核心原则)
    - 预测能力：25% (理论价值核心)
    - 解释力：20%
    - 一致性：15%
    - 简单性：10% (奥卡姆剃刀)
    """
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
    
    # 确定理论成熟度
    if score >= 9.0:
        level = TheoryLevel.L5_CONFIRMED
        level_name = "已验证理论"
    elif score >= 7.5:
        level = TheoryLevel.L4_PREDICTIVE
        level_name = "可预测理论"
    elif score >= 6.0:
        level = TheoryLevel.L3_THEORY
        level_name = "理论"
    elif score >= 4.0:
        level = TheoryLevel.L2_MODEL
        level_name = "模型"
    elif score >= 2.0:
        level = TheoryLevel.L1_HYPOTHESIS
        level_name = "假设"
    else:
        level = TheoryLevel.L0_IDEA
        level_name = "想法"
    
    # 确定假设层级
    if score >= 8.5:
        tier = HypothesisTier.CORE
    elif score >= 6.5:
        tier = HypothesisTier.MAJOR
    else:
        tier = HypothesisTier.SUPPORTING
    
    return {
        'score': round(score, 2),
        'level': level,
        'level_name': level_name,
        'tier': tier,
        'breakdown': {
            '可证伪性': round(falsifiability, 2),
            '预测能力': round(predictive_power, 2),
            '解释力': round(explanatory_power, 2),
            '一致性': round(consistency, 2),
            '简单性': round(simplicity, 2)
        },
        'weights': weights
    }


def evaluate_hypothesis(
    hypothesis_id: str,
    hypothesis_text: str,
    phenomena_explained: int,
    parameters_count: int,
    testable_predictions: int,
    conflicts_with_existing: bool,
    falsification_conditions: List[str]
) -> Dict:
    """
    评估单个假设
    
    评分规则：
    - 解释力：log10(现象数量) * 10
    - 简单性：10 - log10(参数数量) * 2
    - 预测能力：min(10, 可检验预测数 * 2)
    - 一致性：10 (无冲突) / 5 (有冲突但可调和) / 2 (严重冲突)
    - 可证伪性：10 (有明确条件) / 5 (模糊条件) / 0 (无条件)
    """
    import math
    
    # 解释力 (对数尺度)
    explanatory_power = min(10, math.log10(max(1, phenomena_explained)) * 3.5)
    
    # 简单性 (参数越少越好)
    simplicity = max(0, 10 - math.log10(max(1, parameters_count)) * 2.5)
    
    # 预测能力
    predictive_power = min(10, testable_predictions * 2.5)
    
    # 一致性
    if not conflicts_with_existing:
        consistency = 10
    else:
        consistency = 5  # 有冲突但可能是突破点
    
    # 可证伪性
    if len(falsification_conditions) >= 3:
        falsifiability = 10
    elif len(falsification_conditions) >= 1:
        falsifiability = 6
    else:
        falsifiability = 2
    
    score_result = calculate_theory_score(
        explanatory_power,
        simplicity,
        predictive_power,
        consistency,
        falsifiability
    )
    
    return {
        'id': hypothesis_id,
        'text': hypothesis_text,
        'score_result': score_result,
        'metrics': {
            'phenomena_explained': phenomena_explained,
            'parameters_count': parameters_count,
            'testable_predictions': testable_predictions,
            'conflicts_with_existing': conflicts_with_existing,
            'falsification_conditions_count': len(falsification_conditions)
        }
    }


def generate_theory_ranking_report(hypotheses: List[Dict]) -> str:
    """
    生成理论排名报告
    """
    # 评分并排序
    scored = []
    for hyp in hypotheses:
        result = evaluate_hypothesis(**hyp)
        scored.append(result)
    
    # 按评分排序
    scored.sort(key=lambda x: x['score_result']['score'], reverse=True)
    
    # 分类
    core = [h for h in scored if h['score_result']['tier'] == HypothesisTier.CORE]
    major = [h for h in scored if h['score_result']['tier'] == HypothesisTier.MAJOR]
    supporting = [h for h in scored if h['score_result']['tier'] == HypothesisTier.SUPPORTING]
    
    # 生成报告
    report = []
    report.append("# Theory Ranking Report")
    report.append(f"**Generated:** {datetime.now().isoformat()}")
    report.append(f"**Total Hypotheses:** {len(scored)}")
    report.append("")
    
    report.append("## 核心理论 (Top 3)")
    for i, h in enumerate(core[:3], 1):
        report.append(f"### {i}. {h['id']} (Score: {h['score_result']['score']})")
        report.append(f"**内容:** {h['text']}")
        report.append(f"**成熟度:** {h['score_result']['level_name']}")
        report.append(f"**评分分解:**")
        for k, v in h['score_result']['breakdown'].items():
            report.append(f"  - {k}: {v}")
        report.append("")
    
    report.append("## 重要假设 (Top 12)")
    for i, h in enumerate(major[:12], 1):
        report.append(f"{i}. **{h['id']}** (Score: {h['score_result']['score']}) - {h['text'][:100]}...")
    report.append("")
    
    report.append("## 辅助假设")
    report.append(f"共 {len(supporting)} 个，详见完整数据库")
    report.append("")
    
    report.append("## 科研质量指标")
    report.append(f"- 核心理论候选：{len(core)}")
    report.append(f"- 重要假设：{len(major)}")
    report.append(f"- 辅助假设：{len(supporting)}")
    report.append(f"- 平均评分：{sum(h['score_result']['score'] for h in scored)/len(scored):.2f}")
    
    return "\n".join(report)


if __name__ == '__main__':
    # 测试示例
    test_hypotheses = [
        {
            'hypothesis_id': 'DC-17',
            'hypothesis_text': '意识 - 代谢率正相关 (dS/dt ∝ Φ^α, α≈1.2)',
            'phenomena_explained': 15,
            'parameters_count': 3,
            'testable_predictions': 5,
            'conflicts_with_existing': False,
            'falsification_conditions': [
                '麻醉深度与Φ无负相关',
                '跨物种代谢 - 意识无相关',
                'α显著偏离 1.0-1.5 范围'
            ]
        },
        {
            'hypothesis_id': 'DC-20',
            'hypothesis_text': '意识阈值Φ_c 普适常数 (Φ_c ≈ 0.35±0.10)',
            'phenomena_explained': 20,
            'parameters_count': 2,
            'testable_predictions': 6,
            'conflicts_with_existing': False,
            'falsification_conditions': [
                '婴儿Φ_c 显著高于 0.5',
                '跨物种Φ_c 无规律',
                '麻醉梯度无明确阈值'
            ]
        },
        {
            'hypothesis_id': 'DC-138',
            'hypothesis_text': '意识 - 代谢非线性 (dS/dt = αΦ^β, β≈1.3)',
            'phenomena_explained': 12,
            'parameters_count': 4,
            'testable_predictions': 4,
            'conflicts_with_existing': False,
            'falsification_conditions': [
                '线性模型拟合更好',
                'β显著偏离 1.0-1.5'
            ]
        }
    ]
    
    report = generate_theory_ranking_report(test_hypotheses)
    print(report)
