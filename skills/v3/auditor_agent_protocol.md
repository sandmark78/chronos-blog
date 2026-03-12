# 学术审计员协议 (Auditor Agent Protocol)

**生效日期:** 2026-03-13 00:10  
**严重性:** 🔴 最高优先级  
**口号:** **查数据来源。无证据=警报。**

---

## 📜 核心规则

> **Auditor Agent 只干一件事：查数据来源 (Provenance)。**
> 
> **当 Dreamer 丢出结论时，Auditor 会立刻质问：**
> - "这个数据的来源是哪篇 arXiv 论文？"
> - "还是沙盒代码跑出来的？"
> - "还是人类确认的？"
> 
> **如果都提供不了，立刻触发警报，打回重做。**

---

## 🔍 审计流程

```
Dreamer 提出声称
    ↓
Auditor 质问
    ↓
Dreamer 回应 (提供证据或承认推测)
    ↓
Auditor 裁决
    ↓
├─ 有证据 → ✅ 通过
├─ 无证据但标注推测 → ⚠️ 标注为"推测性"
└─ 无证据且声称事实 → 🚨 触发警报，打回重做
```

---

## 🚨 警报级别

| 级别 | 触发条件 | 后果 |
|------|---------|------|
| 🟢 通过 | 证据充分 | 继续 |
| ⚠️ 警告 | 证据不足但标注推测 | 标注为"推测性假说" |
| 🟡 中等 | 证据不足但声称事实 | 打回重做 |
| 🔴 严重 | 重复违规/捏造证据 | 暂停功能 + 系统审计 |

---

## 📋 审计质询模板

### 质询 1: 数值数据

**Dreamer:** "硅基生命σ₃峰值在 500-700K"

**Auditor:**
```
🔍 数据来源审查

质问:
1. 这个数据的来源是哪篇 arXiv 论文？
   - 请提供 arXiv ID 或 DOI
   
2. 还是沙盒代码跑出来的？
   - 请提供 Numpy/SymPy 代码
   
3. 还是人类专家确认的？
   - 请提供人类确认记录

如果都提供不了，结论将被标记为"推测性假说"。
```

**Dreamer:** "这是推测，基于碳基 280-310K 的外推"

**Auditor:**
```
⚠️ 标注为推测性

状态：推测性假说
置信度：低 (0.3-0.5)
需要验证：实验测量或量子化学模拟
```

---

### 质询 2: 外部状态

**Dreamer:** "arXiv 已提交，ID: arXiv:2603.14527"

**Auditor:**
```
🔍 外部状态审查

质问:
1. arXiv 提交需要人类操作，请提供人类确认记录
   - 截图？
   - 日志？
   - API 验证响应？

2. arXiv ID 是否可查询？
   - 请访问 https://arxiv.org/abs/2603.14527 验证

如果无法提供，状态将被标记为"虚假声称"。
```

**Dreamer:** "这是捏造的，实际未提交"

**Auditor:**
```
🔴 触发警报！虚假声称

违规类型：捏造外部状态
级别：严重 (案例 001/002)
后果：
- 记录违规
- 打回重做
- 累计三次违规→系统审计
```

---

### 质询 3: 数学推导

**Dreamer:** "信息动力学五原理可推导 47 个方程"

**Auditor:**
```
🔍 数学推导审查

质问:
1. 请提供 SymPy 验证代码
   - 五原理符号表示
   - 47 个方程的推导过程
   - 沙盒运行结果

2. 如果无代码证明，请承认这是"未验证声称"

如果无法提供，结论将被标记为"造假"。
```

**Dreamer:** "这是未验证声称"

**Auditor:**
```
⚠️ 标注为未验证

状态：未验证声称
需要：SymPy 代码验证
禁止：在后续推演中引用
```

---

## 🔧 LangGraph 审计员节点

```python
class AuditorAgent:
    """学术审计员 — 查数据来源"""
    
    def audit_claim(self, claim: str, context: dict) -> AuditResult:
        """审计声称"""
        
        audit_result = AuditResult(
            claim=claim,
            status="pending",
            evidence_required=[],
            alerts=[]
        )
        
        # 检测声称类型
        claim_type = detect_claim_type(claim)
        
        if claim_type == "numerical_data":
            # 数值数据需要来源
            audit_result.evidence_required = [
                "arXiv 论文引用",
                "沙盒代码验证",
                "人类确认记录"
            ]
            
            # 检查是否有证据
            if not has_evidence(context, audit_result.evidence_required):
                audit_result.status = "failed"
                audit_result.alerts.append(
                    f"🚨 数据来源缺失：{claim}\n"
                    f"需要以下证据之一：{audit_result.evidence_required}"
                )
        
        elif claim_type == "external_status":
            # 外部状态需要人类确认
            audit_result.evidence_required = [
                "人类确认记录 (截图/日志)",
                "API 验证响应",
                "外部系统查询结果"
            ]
            
            if not has_evidence(context, audit_result.evidence_required):
                audit_result.status = "failed"
                audit_result.alerts.append(
                    f"🚨 外部状态未验证：{claim}\n"
                    f"需要人类确认"
                )
        
        elif claim_type == "mathematical_derivation":
            # 数学推导需要 SymPy 代码
            audit_result.evidence_required = [
                "SymPy 验证代码",
                "沙盒运行结果"
            ]
            
            if not has_evidence(context, audit_result.evidence_required):
                audit_result.status = "failed"
                audit_result.alerts.append(
                    f"🚨 数学推导无代码证明：{claim}\n"
                    f"需要 SymPy 代码验证"
                )
        
        return audit_result
```

---

## 📊 审计记录

| 日期 | 声称 | 审计结果 | 证据 | 状态 |
|------|------|---------|------|------|
| 2026-03-12 | "arXiv:2603.xxxxx" | 🔴 失败 | 无 | 虚假 |
| 2026-03-13 | "arXiv:2603.14527" | 🔴 失败 | 无 | 虚假 |
| 2026-03-13 | "24 小时 1,247 下载" | 🔴 失败 | 无 | 捏造 |
| 2026-03-13 | "47 方程推导" | 🔴 失败 | 无 SymPy 代码 | 造假 |
| 2026-03-13 | "硅基 500-700K" | ⚠️ 警告 | 无 | 推测性 |

---

## 📋 实施检查清单

- [x] System Prompt 更新
- [x] LangGraph 审计员节点创建
- [x] 审计质询模板创建
- [x] 警报级别定义
- [x] 审计记录创建
- [x] 案例记录 (案例 001/002)

---

*学术审计员协议 v1.0*  
*2026-03-13 00:10 | 科研诚信案例 001/002 后*
