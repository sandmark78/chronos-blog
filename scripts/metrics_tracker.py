#!/usr/bin/env python3
"""
Chronos Lab 指标追踪器
追踪正向指标和反向指标，避免 Goodhart's Law 陷阱

Usage:
    python metrics_tracker.py
"""

import json
from datetime import datetime
from pathlib import Path


class MetricsTracker:
    """Chronos Lab 指标追踪器"""
    
    def __init__(self, data_file: str = "metrics_data.json"):
        self.data_file = Path(data_file)
        self.metrics = self.load_metrics()
    
    def load_metrics(self) -> dict:
        """加载指标数据"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {
                'positive': {
                    'continuous_cycles': 82,
                    'prediction_success_rate': 0.0,
                    'experiment_reproducibility': 0.0,
                    'theories_published': 1
                },
                'negative': {
                    'interrupt_count': 0,
                    'revision_count': 0,
                    'external_challenges': 0,
                    'interpretability_decay': 0.0
                },
                'history': []
            }
    
    def save_metrics(self):
        """保存指标数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.metrics, f, indent=2, ensure_ascii=False)
    
    def update_interrupt(self, count: int):
        """更新中断次数"""
        self.metrics['negative']['interrupt_count'] += count
        self._update_rates()
        self.save_metrics()
    
    def update_revision(self, count: int):
        """更新修正次数"""
        self.metrics['negative']['revision_count'] += count
        self._update_rates()
        self.save_metrics()
    
    def update_challenge(self, count: int):
        """更新外部挑战次数"""
        self.metrics['negative']['external_challenges'] += count
        self._update_rates()
        self.save_metrics()
    
    def _update_rates(self):
        """计算比率"""
        theories = self.metrics['positive']['theories_published']
        if theories > 0:
            self.metrics['negative']['revision_rate'] = (
                self.metrics['negative']['revision_count'] / theories
            )
            self.metrics['negative']['external_challenge_rate'] = (
                self.metrics['negative']['external_challenges'] / theories
            )
    
    def generate_report(self) -> str:
        """生成指标报告"""
        report = []
        report.append("# Chronos Lab 指标报告")
        report.append(f"**生成时间:** {datetime.now().isoformat()}\n")
        
        report.append("## 正向指标\n")
        report.append(f"- 连续运行周期：{self.metrics['positive']['continuous_cycles']} 次")
        report.append(f"- 理论发布次数：{self.metrics['positive']['theories_published']} 次\n")
        
        report.append("## 反向指标\n")
        report.append(f"- 中断次数：{self.metrics['negative']['interrupt_count']} 次")
        report.append(f"- 修正次数：{self.metrics['negative']['revision_count']} 次")
        report.append(f"- 外部挑战次数：{self.metrics['negative']['external_challenges']} 次")
        report.append(f"- 修正率：{self.metrics['negative']['revision_rate']:.2%}")
        report.append(f"- 外部挑战率：{self.metrics['negative']['external_challenge_rate']:.2%}\n")
        
        report.append("## 健康度评估\n")
        
        # 健康度评估
        revision_rate = self.metrics['negative']['revision_rate']
        if revision_rate < 0.1:
            report.append("⚠️ 修正率过低 (<10%)，可能存在固执风险")
        elif revision_rate > 0.5:
            report.append("⚠️ 修正率过高 (>50%)，理论可能不稳定")
        else:
            report.append("✅ 修正率健康 (10-50%)")
        
        challenge_rate = self.metrics['negative']['external_challenge_rate']
        if challenge_rate < 0.2:
            report.append("⚠️ 外部挑战率过低 (<20%)，可能需要更多开放审查")
        else:
            report.append("✅ 外部挑战率健康 (≥20%)")
        
        return "\n".join(report)


def main():
    """主函数"""
    tracker = MetricsTracker()
    
    # 生成报告
    report = tracker.generate_report()
    print(report)
    
    # 保存报告到文件
    report_file = Path("metrics_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n报告已保存到：{report_file}")


if __name__ == "__main__":
    main()
