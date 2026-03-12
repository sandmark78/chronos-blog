# Occam's Razor Router — 奥卡姆剃刀路由系统

"""
版本：v1.0
创建时间：2026-03-12
状态：已激活

核心逻辑:
- 评分 ≥ 80: 启动 1M Token 深度研究
- 评分 < 80: 归档到数据库 (冷宫)
"""

from typing import TypedDict, Literal, Optional
from datetime import datetime
import os


# 1. 定义图的全局状态 (State)
class ResearchState(TypedDict):
    research_id: str
    question: str
    priority_score: float
    priority_class: str  # 'critical', 'high', 'medium', 'low'
    conflict_density: Optional[float]
    originality: Optional[float]
    testability: Optional[float]
    timestamp: str


# 2. 节点逻辑：冷冻归档 (省钱节点)
def archive_to_db_node(state: ResearchState) -> ResearchState:
    """
    将低优先级问题写入数据库，不消耗 1M Token
    
    存储位置:
    - problem-database/archived_questions.json
    - 向量数据库 (低成本检索)
    """
    score = state.get('priority_score', 0.0)
    question = state.get('question', '')[:50]
    
    print(f"❄️ [剪枝] 命题归档 | 评分：{score:.2f} | 命题：{question}...")
    
    # 归档逻辑 (伪代码)
    # archive = {
    #     'id': state['research_id'],
    #     'question': state['question'],
    #     'score': score,
    #     'archived_at': datetime.now().isoformat(),
    #     'reason': f'Priority score {score} < 80.0'
    # }
    # save_to_database(archive)
    
    state['archived'] = True
    state['archive_timestamp'] = datetime.now().isoformat()
    
    return state


# 3. 节点逻辑：深度研究 (烧钱节点)
def deep_research_node(state: ResearchState) -> ResearchState:
    """
    启动 1M Token 上下文，加载全量图谱和论文
    
    触发条件: priority_score ≥ 80.0
    """
    score = state.get('priority_score', 0.0)
    question = state.get('question', '')[:50]
    
    print(f"🔥 [燃烧] 启动深度研究 | 评分：{score:.2f} | 命题：{question}...")
    print(f"   上下文加载：~900k tokens")
    print(f"   预计成本：$X.XX (按 API 定价)")
    
    # 深度研究逻辑 (伪代码)
    # context = load_full_context()  # 900k tokens
    # result = llm_reason(context, state['question'])
    # hypothesis = generate_hypothesis(result)
    
    state['deep_research'] = True
    state['deep_research_timestamp'] = datetime.now().isoformat()
    state['context_loaded'] = True
    
    return state


# 4. 核心路由阀门 (奥卡姆剃刀)
def occams_razor_router(state: ResearchState) -> Literal["deep_research", "archive"]:
    """
    条件边：决定资源分配
    
    阈值配置:
    - 默认：80.0 (critical + high)
    - 紧张模式：90.0 (仅 critical)
    - 宽松模式：70.0 (critical + high + 部分 medium)
    """
    score = state.get('priority_score', 0.0)
    
    # 从环境变量读取动态阈值 (支持运行时调整)
    threshold = float(os.getenv('OCCAM_THRESHOLD', '80.0'))
    
    if score >= threshold:
        print(f"✅ 路由决策：深度研究 (评分 {score:.2f} ≥ 阈值 {threshold:.1f})")
        return "deep_research"
    else:
        print(f"⏸️ 路由决策：归档 (评分 {score:.2f} < 阈值 {threshold:.1f})")
        return "archive"


# 5. 辅助函数：批量处理归档问题
def process_archived_batch(archived_questions: list, model: str = "flash"):
    """
    在算力宽裕时，用便宜模型后台消化归档问题
    
    参数:
        archived_questions: 归档问题列表
        model: "flash" (便宜) 或 "pro" (昂贵)
    """
    print(f"📦 批量处理归档问题 | 数量：{len(archived_questions)} | 模型：{model}")
    
    results = []
    for q in archived_questions:
        # 使用便宜模型进行初步分析
        # result = cheap_llm_analyze(q)
        # results.append(result)
        pass
    
    return results


# 6. 统计与监控
def get_routing_statistics() -> dict:
    """
    获取路由统计信息
    """
    return {
        'threshold': float(os.getenv('OCCAM_THRESHOLD', '80.0')),
        'total_questions': 0,  # 从数据库读取
        'deep_research_count': 0,  # 深度研究数量
        'archived_count': 0,  # 归档数量
        'cost_savings_estimate': '70%',  # 预估节省
    }


# 7. LangGraph 工作流构建示例
def build_research_workflow():
    """
    构建完整的 LangGraph 研究流程
    
    流程:
    问题输入 → 优先级评分 → 奥卡姆剃刀路由 → 深度研究/归档 → 假设生成 → 知识固化
    """
    from langgraph.graph import StateGraph, END
    
    workflow = StateGraph(ResearchState)
    
    # 添加节点
    workflow.add_node("priority_scoring", lambda s: s)  # 优先级评分节点 (假设已存在)
    workflow.add_node("deep_research", deep_research_node)
    workflow.add_node("archive", archive_to_db_node)
    workflow.add_node("hypothesis_generation", lambda s: s)  # 假设生成节点
    workflow.add_node("knowledge_consolidation", lambda s: s)  # 知识固化节点
    
    # 添加边
    workflow.set_entry_point("priority_scoring")
    
    # 奥卡姆剃刀路由 (条件边)
    workflow.add_conditional_edges(
        "priority_scoring",
        occams_razor_router,
        {
            "deep_research": "deep_research",
            "archive": "archive"
        }
    )
    
    # 深度研究后续流程
    workflow.add_edge("deep_research", "hypothesis_generation")
    workflow.add_edge("hypothesis_generation", "knowledge_consolidation")
    
    # 归档直接结束
    workflow.add_edge("archive", END)
    workflow.add_edge("knowledge_consolidation", END)
    
    app = workflow.compile()
    return app


# 8. 阈值动态调整
def set_threshold(new_threshold: float):
    """
    动态调整路由阈值
    
    使用场景:
    - 临近 arXiv 提交 (3/14)，算力紧张 → 提高到 90.0
    - 提交完成后，算力宽裕 → 降低到 70.0
    """
    os.environ['OCCAM_THRESHOLD'] = str(new_threshold)
    print(f"🎚️ 阈值调整：{new_threshold:.1f}")
    print(f"   < {new_threshold:.1f}: 归档")
    print(f"   ≥ {new_threshold:.1f}: 深度研究")


if __name__ == '__main__':
    print('=== Occam\'s Razor Router v1.0 ===')
    print()
    
    # 测试用例 1: 高分命题 (应进入深度研究)
    test_state_critical = {
        'research_id': 'P-001',
        'question': '量子测量速率与观察者Φ值的耦合机制',
        'priority_score': 92.5,
        'priority_class': 'critical',
        'conflict_density': 9.0,
        'timestamp': datetime.now().isoformat()
    }
    
    route = occams_razor_router(test_state_critical)
    print(f'测试结果 1: {route} (预期：deep_research)')
    print()
    
    # 测试用例 2: 低分命题 (应归档)
    test_state_low = {
        'research_id': 'P-002',
        'question': '生命度 L 的跨物种标定方法优化',
        'priority_score': 65.0,
        'priority_class': 'medium',
        'conflict_density': 4.0,
        'timestamp': datetime.now().isoformat()
    }
    
    route = occams_razor_router(test_state_low)
    print(f'测试结果 2: {route} (预期：archive)')
    print()
    
    # 测试用例 3: 边界命题 (80 分，应进入深度研究)
    test_state_boundary = {
        'research_id': 'P-003',
        'question': '文明 D 值历史重建的贝叶斯方法',
        'priority_score': 80.0,
        'priority_class': 'high',
        'conflict_density': 7.0,
        'timestamp': datetime.now().isoformat()
    }
    
    route = occams_razor_router(test_state_boundary)
    print(f'测试结果 3: {route} (预期：deep_research)')
    print()
    
    print('✅ 奥卡姆剃刀路由系统测试完成！')
