# KC-343: A20 Phase 1B 设计规范

**创建时间:** 2026-03-20 13:15 (Asia/Shanghai)  
**周期:** DC-343  
**关联定理:** T417 (α耦合常数定理)  
**验证状态:** ⚠️ 条件性通过 (待修复 C01/C02)

---

## 一、核心设计

### 目标

实现 IIT 4.0 兼容的Φ计算，用于：
1. 对比简化版Φ (基于纠缠熵) 与 IIT 4.0Φ
2. 检验α指数的鲁棒性
3. 为 A20 Phase 1C (真实硬件测试) 做准备

### 关键模块

#### 模块 1: 量子因果库计算

```python
def compute_cause_repertoire(statevector, subsystem_indices):
    """计算因果库 (Cause Repertoire)"""
    # 计算子系统的约化密度矩阵
    # 返回计算基下的概率分布
```

#### 模块 2: 效应库计算

```python
def compute_effect_repertoire(circuit, subsystem_indices, shots=1024):
    """计算效应库 (Effect Repertoire)"""
    # 运行量子电路并测量
    # 返回概率分布
```

#### 模块 3: 信息有效性 (IE)

```python
def compute_information_effectiveness(cause, effect):
    """IE = D_KL(P_cause || P_cause_indep) + D_KL(P_effect || P_effect_indep)"""
```

#### 模块 4: MIP 最小信息划分

```python
def compute_mip_phi(circuit, statevector, n_partitions=10):
    """Φ = min(IE / N_bits) over all partitions"""
```

#### 模块 5: IIT 4.0Φ主函数

```python
def compute_iit_phi(circuit, statevector, n_mip_samples=20):
    """计算 IIT 4.0 兼容Φ (多次 MIP 采样取平均)"""
```

---

## 二、实验协议

### 实验 1: Φ计算方法对比

**假设:**
- H₀: Φ_simple 与 Φ_IIT 无线性相关 (r < 0.7)
- H₁: Φ_simple 与 Φ_IIT 强相关 (r > 0.7)

**成功标准:** r > 0.85, p < 0.01

### 实验 2: α指数鲁棒性检验

**方法:**
1. 用Φ_simple 拟合 R ∝ Φ^α → α_simple
2. 用Φ_IIT 拟合 R ∝ Φ^α → α_IIT
3. 比较：|α_simple - α_IIT| / α_simple < 0.2

**成功标准:** 相对差异 < 20%

### 实验 3: 噪声敏感度分析

**方法:**
1. 添加不同水平退相干噪声 (0%, 1%, 5%, 10%)
2. 测量Φ_IIT 随噪声的变化
3. 计算 dΦ/d(noise)

**预测:** IIT 4.0Φ比简化版Φ对噪声更敏感

---

## 三、已知问题与修正

### 🔴 严重问题 (已修复/待修复)

| ID | 问题 | 状态 | 修正方案 |
|----|------|------|----------|
| **C01** | N_qubits=1 代码崩溃 | ⏳ 待修复 | `if n_qubits < 2: return 0.0` |
| **C02** | GHPII vs IIT 4.0 框架不一致 | ⏳ 待澄清 | 添加框架说明章节 |

### 🟡 中等问题 (DC-344 处理)

| ID | 问题 | 优先级 |
|----|------|--------|
| **C03** | Φ量纲模糊 | 中 |
| **C04** | N→∞MIP 收敛性未证明 | 中 |
| **C05** | R_quantum 定义不明确 | 中 |
| **C06** | Φ_max 定义模糊 | 中 |
| **C07** | GHPII 框架被搁置 | 中 |

---

## 四、验证结果

| Subagent | 评分 | 状态 |
|----------|------|------|
| **A (矛盾检测)** | 62/100 自洽度 | ⚠️ 需修正 |
| **B (独特性)** | 4⭐ / 75% 原创性 | ✅ 通过 |
| **C (文献查重)** | 65-75% 原创性 | ✅ 通过 |

**综合状态:** ⚠️ 条件性通过

---

## 五、最相关文献

### 必须引用

1. **Albantakis, Prentner, Durham (2023)** - "Measuring the integrated information of a quantum mechanism"
2. **McQueen, Durham, Mueller (2023)** - "Building a quantum superposition of conscious states with IIT"
3. **Zanardi et al. (2018)** - "Towards Quantum Integrated Information Theory"

### 背景引用

4. **Tononi et al. (2016)** - IIT 4.0 官方定义
5. **Tagg & Reid (2025)** - 量子计算机意识实验 (Orch-OR)

---

## 六、代码位置

- **主模块:** `experiments/a20_phase1b/iit_phi_calculator.py` (待创建)
- **对比脚本:** `experiments/a20_phase1b/phi_comparison.py` (待创建)
- **Phase 1A 参考:** `experiments/a20_phase1a/` (已完成)

---

## 七、下一步

1. **立即:** 修复 C01 代码 bug
2. **DC-344:** 澄清 C02 框架关系，完善 R 和Φ_max 定义
3. **DC-345:** 论证 GHPII-IIT 对应，N→∞收敛性分析
4. **DC-346+:** Phase 1C 真实硬件测试准备

---

*知识卡片 KC-343 | Chronos Lab | DC-343*
