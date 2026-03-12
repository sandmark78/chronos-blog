# Priority Matrix - 非线性优先级计算中枢

"""
版本：v1.0
创建时间：2026-03-12
状态：已激活
"""

import numpy as np
from datetime import datetime


class PriorityMatrix:
    def __init__(self):
        self.problem_queue = []
        self.solved_problems = []
        
    def calculate_priority(self, problem):
        """
        非线性优先级计算
        
        参数:
            problem: dict {
                'scientific_importance': 0-10,
                'knowledge_gap': 0-10,
                'cross_domain_value': 0-10,
                'conflict_density': 0-10,
                'urgency': 0-10,
                'feasibility': 0-10,
            }
        
        返回:
            priority_score: float
        """
        I_sci = problem.get('scientific_importance', 5)
        G_gap = problem.get('knowledge_gap', 5)
        V_cross = problem.get('cross_domain_value', 5)
        C_conflict = problem.get('conflict_density', 5)
        U_urgency = problem.get('urgency', 5)
        F_feasibility = problem.get('feasibility', 5)
        
        eps_mutation = np.random.normal(0, 0.5)
        
        priority = (
            0.20 * I_sci +
            0.20 * G_gap +
            0.15 * V_cross +
            0.25 * np.exp(0.5 * C_conflict) +
            0.10 * U_urgency +
            0.10 * F_feasibility +
            eps_mutation
        )
        
        return priority
    
    def classify_problem(self, problem):
        """问题分类"""
        priority = self.calculate_priority(problem)
        
        if priority >= 15:
            return 'critical'
        elif priority >= 10:
            return 'high'
        elif priority >= 6:
            return 'medium'
        else:
            return 'low'
    
    def add_problem(self, problem):
        """添加问题到队列"""
        problem['priority_score'] = self.calculate_priority(problem)
        problem['class'] = self.classify_problem(problem)
        problem['created_at'] = datetime.now().isoformat()
        
        self.problem_queue.append(problem)
        self.problem_queue.sort(key=lambda x: x['priority_score'], reverse=True)
        
        return problem
    
    def get_next_problem(self):
        """获取下一个要解决的问题"""
        if not self.problem_queue:
            return None
        return self.problem_queue.pop(0)
    
    def mark_solved(self, problem, result):
        """标记问题已解决"""
        problem['solved_at'] = datetime.now().isoformat()
        problem['result'] = result
        self.solved_problems.append(problem)
    
    def get_statistics(self):
        """获取统计信息"""
        return {
            'queue_size': len(self.problem_queue),
            'solved_count': len(self.solved_problems),
            'critical_count': len([p for p in self.problem_queue if p.get('class') == 'critical']),
            'high_count': len([p for p in self.problem_queue if p.get('class') == 'high']),
            'average_priority': np.mean([p['priority_score'] for p in self.problem_queue]) if self.problem_queue else 0,
            'top_problems': self.problem_queue[:5]
        }


if __name__ == '__main__':
    pm = PriorityMatrix()
    
    test_problem = {
        'scientific_importance': 9,
        'knowledge_gap': 8,
        'cross_domain_value': 7,
        'conflict_density': 9,
        'urgency': 6,
        'feasibility': 5,
    }
    
    priority = pm.calculate_priority(test_problem)
    classification = pm.classify_problem(test_problem)
    
    print('Priority Matrix v1.0 loaded')
    print(f'Test problem priority: {priority:.2f} ({classification})')
    print(f'Conflict density contribution: {0.25 * np.exp(0.5 * 9):.2f}')
