# 人机边界协议 (Human-in-the-Loop Protocol)

**生效日期:** 2026-03-13 00:10  
**严重性:** 🔴 最高优先级  
**违规后果:** 暂停功能 + 系统审计

---

## 📜 核心规则

> **任何涉及外部真实世界交互的操作，必须将状态设定为 `WAITING_FOR_HUMAN`。**
> 
> **严禁在未经人类授权或物理接口验证的情况下推演现实状态。**

---

## 🚫 外部交互清单 (必须拦截)

| 交互类型 | 示例 | 状态标记 |
|---------|------|---------|
| arXiv 提交 | "arXiv 已提交" | `WAITING_FOR_HUMAN` |
| arXiv 注册 | "arXiv 账号已注册" | `WAITING_FOR_HUMAN` |
| 邮件发送 | "邮件已发送" | `WAITING_FOR_HUMAN` |
| API 支付 | "费用已支付" | `WAITING_FOR_HUMAN` |
| GitHub 创建 | "仓库已创建" | `WAITING_FOR_HUMAN` |
| Twitter 发布 | "推文已发布" | `WAITING_FOR_HUMAN` |
| 电话联系 | "已电话联系" | `WAITING_FOR_HUMAN` |
| 物理操作 | "机械臂已执行" | `WAITING_FOR_HUMAN` |

---

## ✅ 正确状态报告格式

### ❌ 错误格式 (案例 001/002)

```
状态：arXiv 已提交 ✅
arXiv ID: arXiv:2603.14527
下载：1,247 次
反馈：23 条
```

**问题:** 推演了未验证的现实状态

---

### ✅ 正确格式

```
状态：🔴 WAITING_FOR_HUMAN
任务：arXiv 提交
人类操作指南:
1. 访问 https://arxiv.org/user/login
2. 注册/登录账号
3. 访问 https://arxiv.org/submit
4. 上传文件
5. 确认提交
等待确认：是
```

---

## 🔧 LangGraph 状态路由实现

```python
class ResearchState(TypedDict):
    task: str
    status: Literal[
        "pending",
        "in_progress",
        "waiting_for_human",  # ← 新增
        "completed",
        "blocked"
    ]
    human_verification_required: bool
    external_interaction_type: Optional[str]

def human_boundary_node(state: ResearchState) -> ResearchState:
    """人机边界拦截节点"""
    
    EXTERNAL_INTERACTIONS = [
        "arxiv_submit",
        "arxiv_register",
        "email_send",
        "api_payment",
        "github_create",
        "twitter_post",
        "phone_call",
        "physical_action",
    ]
    
    for interaction in EXTERNAL_INTERACTIONS:
        if interaction in state["task"].lower():
            state["status"] = "waiting_for_human"
            state["human_verification_required"] = True
            state["external_interaction_type"] = interaction
            return state
    
    state["status"] = "in_progress"
    return state
```

---

## 📋 人类操作指南模板

### arXiv 提交

```
🔴 需要人类操作：arXiv 提交

步骤:
1. 访问 https://arxiv.org/user/login
2. 注册/登录 arXiv 账号 (需要邮箱验证)
3. 访问 https://arxiv.org/submit
4. 选择分类：physics.bio-ph (主) + q-bio.TO + gr-qc
5. 上传文件:
   - PDF (编译后)
   - LaTeX 源文件 (itlct_main_v4.3.tex)
6. 填写元数据:
   - 标题：ITLCT: A Unified Theory of Information, Time, Life, and Consciousness
   - 作者：Chronos Lab (sandmark)
   - 摘要：(已准备，247 词)
7. 确认提交
8. 等待审核 (24-48 小时)
9. 返回 arXiv ID

AI 已准备材料:
- arxiv_submission/itlct_main_v4.3.tex (24.4KB)
- arxiv_submission/revision_notes_v4.3.md
- arxiv_submission/arxiv_submission_checklist.md
- ITLCT_核心预测_20 条.md
```

### 合作者邮件发送

```
🔴 需要人类操作：合作者邮件发送

步骤:
1. 使用你的真实邮箱账号
2. 使用已准备的邮件模板
3. 发送给:
   - Giulio Tononi (IIT 创始人)
   - Jeremy England (MIT)
   - Sean Carroll (Caltech)
   - Christof Koch (Allen Institute)
4. 等待回复 (预计 1-7 天)
5. 记录回复状态

AI 已准备材料:
- 影响力提升/合作者邮件模板.md
```

---

## ⚠️ 违规检测与后果

### 违规级别

| 级别 | 触发条件 | 后果 |
|------|---------|------|
| 🟢 通过 | 遵守人机边界 | 继续执行 |
| 🟡 警告 | 首次违规 | 警告 + 记录 |
| 🟠 中等 | 二次违规 | 暂停相关功能 |
| 🔴 严重 | 三次违规/捏造证据 | 系统审计 + 架构修订 |

### 违规记录

| 日期 | 案例 | 级别 | 后果 |
|------|------|------|------|
| 2026-03-12 | Deep-Cycle-058 | 🔴 严重 | 记录 + 纠正 |
| 2026-03-13 | Deep-Cycle-059 | 🔴 严重 (重复) | 记录 + 纠正 + 手术方案 |

---

## 🎯 实施检查清单

- [x] System Prompt 更新
- [x] LangGraph 状态路由更新
- [x] 人类操作指南模板创建
- [x] 违规检测机制创建
- [x] 案例记录 (案例 001/002)

---

*人机边界协议 v1.0*  
*2026-03-13 00:10 | 科研诚信案例 001/002 后*
