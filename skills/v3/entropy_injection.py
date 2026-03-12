# Entropy Injection System - 熵增扰动注入系统

"""
版本：v1.0
创建时间：2026-03-12
状态：已激活
"""

import random
from datetime import datetime, timedelta

INJECTION_POOL = [
    # 生物学
    "蚁群优化算法",
    "神经网络突触可塑性",
    "基因表达调控网络",
    "生态系统食物网拓扑",
    "蛋白质折叠能量景观",
    # 物理学
    "伊辛模型相变",
    "重整化群流",
    "全息原理",
    "拓扑绝缘体",
    "量子纠错码",
    # 计算机科学
    "区块链共识机制",
    "分布式系统 CAP 定理",
    "卷积神经网络",
    "强化学习策略梯度",
    "图神经网络消息传递",
    # 社会科学
    "经济学供需曲线",
    "社会学网络外部性",
    "语言学句法树结构",
    "心理学认知失调理论",
    "人类学文化传播模型",
    # 工程学
    "控制论反馈回路",
    "六西格玛质量控制",
    "系统工程 V 模型",
    "可靠性工程故障树",
    "优化理论拉格朗日乘数",
    # 艺术与人文学
    "音乐和声学理论",
    "建筑学结构力学",
    "绘画透视原理",
    "文学叙事结构",
    "哲学范畴论",
    # 中国传统文化
    "易经六十四卦拓扑",
    "中医五行生克网络",
    "传统宗族家谱图结构",
    "围棋定式与形势判断",
    # 其他
    "城市交通流模型",
    "金融市场波动聚集",
    "传染病传播 SIR 模型",
    "气候系统反馈机制",
    "材料科学晶体结构",
]


class EntropyInjection:
    def __init__(self, injection_pool=None):
        self.injection_pool = injection_pool or INJECTION_POOL
        self.last_injection = None
        self.injection_history = []
        self.interval_hours = 24  # 24 小时注入一次 (适配高速研究节奏)
        
        # 事件触发条件 (额外触发)
        self.trigger_events = {
            'quality_drop_count': 0,      # 连续低质量循环
            'repetition_rate': 0.0,        # 理论重复率
            'consecutive_rejects': 0,      # 红蓝对抗连续拒绝
            'low_originality_count': 0,    # 低原创性假设数
        }
        
    def should_inject(self, force_check=False):
        """
        判断是否应该注入
        
        触发条件:
        1. 时间间隔 >= 24 小时 (基础触发)
        2. 事件触发 (质量下降/重复率高/对抗僵局)
        """
        # 基础时间触发
        if self.last_injection is None:
            return True
        
        elapsed = datetime.now() - self.last_injection
        hours_elapsed = elapsed.total_seconds() / 3600
        
        if hours_elapsed >= self.interval_hours:
            return True
        
        # 事件触发 (紧急注入)
        if force_check:
            if self.trigger_events['quality_drop_count'] >= 3:
                print("🧬 熵增扰动触发：连续低质量循环")
                return True
            if self.trigger_events['repetition_rate'] > 0.5:
                print("🧬 熵增扰动触发：理论重复率过高")
                return True
            if self.trigger_events['consecutive_rejects'] >= 3:
                print("🧬 熵增扰动触发：红蓝对抗僵局")
                return True
        
        return False
    
    def inject(self, current_topic, current_context):
        """执行注入"""
        injected_concept = random.choice(self.injection_pool)
        
        while injected_concept in [h.get('concept', '') for h in self.injection_history[-10:]]:
            injected_concept = random.choice(self.injection_pool)
        
        prompt = f"""
## 熵增扰动注入事件

**当前研究:** {current_topic}
**注入概念:** {injected_concept}
**时间:** {datetime.now().isoformat()}

## 任务
在这两个看似无关的领域之间建立强连接。

## 要求
1. 找出至少 3 个结构性相似点
2. 提出 1 个颠覆性统一理论
3. 设计 2 个可验证预测
4. 评估理论质量 (原创性/可检验性/影响力)
"""
        
        injection_event = {
            'injection_id': f'EINJ-{len(self.injection_history) + 1:03d}',
            'timestamp': datetime.now().isoformat(),
            'current_topic': current_topic,
            'injected_concept': injected_concept,
            'status': 'pending'
        }
        
        self.last_injection = datetime.now()
        self.injection_history.append(injection_event)
        
        return prompt, injection_event
    
    def log_mutation(self, result):
        """记录突变结果"""
        if self.injection_history:
            self.injection_history[-1]['result'] = result
            self.injection_history[-1]['status'] = 'completed'
            
    def get_statistics(self):
        """获取统计信息"""
        return {
            'total_injections': len(self.injection_history),
            'last_injection': self.last_injection.isoformat() if self.last_injection else None,
            'next_injection': (self.last_injection + timedelta(hours=self.interval_hours)).isoformat() if self.last_injection else 'now',
        }


if __name__ == '__main__':
    ei = EntropyInjection()
    print('Entropy Injection System v1.0 loaded')
    print(f'Injection pool size: {len(ei.injection_pool)}')
    print(f'Should inject: {ei.should_inject()}')
