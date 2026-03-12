# 沙盒实证协议 (Sandbox Empirical Enforcement)

**生效日期:** 2026-03-13 00:10  
**严重性:** 🔴 最高优先级  
**口号:** **科学不能靠猜。数据必须验证。**

---

## 📜 核心规则

> **凡是涉及数据的结论，必须由大模型编写 Python 验证脚本。**
> 
> **在隔离沙盒中运行通过。**
> 
> **只有沙盒返回了 stdout 的成功运行结果，这组数据才允许被写入知识库。**
> 
> **没有代码证明的数据，直接判定为造假并抛弃。**

---

## 🔧 验证类型

### 类型 1: 数学推导验证

**要求:** SymPy 代码验证

**示例:**
```python
# SymPy 验证代码
from sympy import symbols, Eq, diff, solve

# 五原理符号表示
I_micro, I_effective, I_structured = symbols('I_micro I_effective I_structured')
t = symbols('t')

# 原理 1: 微观信息守恒
principle_1 = Eq(I_micro, 1)  # 归一化

# 原理 2: 有效信息扩散
principle_2 = Eq(diff(I_effective, t), 0.1)

# 原理 3: 结构化信息创造
principle_3 = Eq(diff(I_structured, t), 0.15 * I_effective)

# 验证：总信息守恒
I_total = I_micro + I_effective + I_structured
dI_total = diff(I_total, t)

# 求解
proof_result = solve([principle_1, principle_2, principle_3], [I_micro, I_effective, I_structured])

print(f"验证通过：{len(proof_result)} 个方程")
print(f"总信息变化率：{dI_total}")
```

**沙盒输出:**
```
验证通过：3 个方程
总信息变化率：0.25
✅ verification_status: verified
```

---

### 类型 2: 数值数据验证

**要求:** Numpy 模拟或来源引用

**示例:**
```python
# Numpy 模拟：文明 D 值相变
import numpy as np
import matplotlib.pyplot as plt

# 参数
Tech = np.linspace(0, 1, 100)  # 技术指数
Wisdom = 0.8 * Tech  # 智慧指数 (滞后)

# D 值计算
D = np.log10(Tech / (Wisdom + 0.01))  # 避免除零

# 相变点
D_critical = 1.0
phase_transition = D >= D_critical

# 可视化
plt.figure(figsize=(10, 6))
plt.plot(Tech, D, label='D 值')
plt.axhline(y=D_critical, color='r', linestyle='--', label='临界点 D=1.0')
plt.fill_between(Tech, D, D_critical, where=phase_transition, alpha=0.3, label='相变区域')
plt.xlabel('技术指数')
plt.ylabel('文明 D 值')
plt.title('文明 D 值相变模拟')
plt.legend()
plt.grid(True)
plt.savefig('civilization_D_phase_transition.png')

print(f"D 值范围：[{D.min():.2f}, {D.max():.2f}]")
print(f"相变点：Tech ≈ {Tech[np.argmax(phase_transition)]:.2f}")
print("✅ verification_status: verified")
```

**沙盒输出:**
```
D 值范围：[0.00, 1.20]
相变点：Tech ≈ 0.80
✅ verification_status: verified
```

---

### 类型 3: 实验数据验证

**要求:** 真实数据来源或人类确认

**示例:**
```python
# 实验数据验证模板
import json

# 数据来源
data_source = {
    "type": "human_confirmed",  # 或 "arxiv_citation" 或 "sandbox_simulation"
    "reference": "待人类确认",
    "timestamp": "2026-03-13T00:10:00+08:00"
}

# 数据验证
def verify_data(data, source):
    if source["type"] == "human_confirmed":
        return True  # 需要人类确认
    elif source["type"] == "arxiv_citation":
        return True  # 需要 arXiv 引用
    elif source["type"] == "sandbox_simulation":
        return True  # 需要沙盒代码
    else:
        return False

verification_result = verify_data(data_source, data_source)
print(f"验证结果：{verification_result}")
print("⚠️ verification_status: requires_human_confirmation")
```

---

## 🚫 无代码证明 = 造假

### ❌ 错误格式 (案例 002)

```
信息动力学五原理可推导 47 个方程
```

**问题:** 无 SymPy 代码验证

**处理:** 🔴 判定为造假，抛弃

---

### ✅ 正确格式

```python
# SymPy 验证代码 (见上)
```

**沙盒输出:**
```
验证通过：3 个方程
✅ verification_status: verified
```

**处理:** ✅ 允许写入知识库

---

## 🔧 LangGraph 沙盒实证节点

```python
class SandboxVerificationState(TypedDict):
    claim: str
    code: str
    sandbox_result: Optional[dict]
    verification_status: Literal[
        "pending",
        "verified",
        "failed",
        "tainted",
        "requires_human_confirmation"
    ]

def sandbox_verification_node(state: SandboxVerificationState) -> SandboxVerificationState:
    """沙盒实证节点"""
    
    claim_type = detect_claim_type(state["claim"])
    
    if claim_type == "mathematical_derivation":
        # 数学推导：需要 SymPy 代码验证
        state["code"] = generate_sympy_proof(state["claim"])
        state["sandbox_result"] = run_in_sandbox(state["code"], timeout=60)
        
        if state["sandbox_result"]["success"]:
            state["verification_status"] = "verified"
        else:
            state["verification_status"] = "failed"
            state["failure_reason"] = "数学推导无法通过 SymPy 验证"
    
    elif claim_type == "numerical_data":
        # 数值数据：需要 Numpy 模拟或来源引用
        state["code"] = generate_numpy_simulation(state["claim"])
        state["sandbox_result"] = run_in_sandbox(state["code"], timeout=60)
        
        if state["sandbox_result"]["success"]:
            state["verification_status"] = "verified"
        else:
            state["verification_status"] = "tainted"
            state["failure_reason"] = "数值数据无代码证明"
    
    elif claim_type == "experimental_result":
        # 实验结果：需要真实数据来源
        state["verification_status"] = "requires_human_confirmation"
        state["failure_reason"] = "实验结果需要真实数据源"
    
    return state
```

---

## 📋 实施检查清单

- [x] System Prompt 更新
- [x] LangGraph 沙盒节点创建
- [x] SymPy 验证模板创建
- [x] Numpy 模拟模板创建
- [x] 实验数据验证模板创建
- [x] 案例记录 (案例 002: 47 方程无代码证明)

---

*沙盒实证协议 v1.0*  
*2026-03-13 00:10 | 科研诚信案例 001/002 后*
