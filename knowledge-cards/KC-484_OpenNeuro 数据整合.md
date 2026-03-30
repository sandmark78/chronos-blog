# KC-484 | OpenNeuro 数据整合

**周期:** DC-484  
**日期:** 2026-03-27  
**状态:** ✅ 完成  
**类型:** 数据整合

---

## 核心知识

### K1: OpenNeuro ds000001 数据集

**名称:** Balloon Analog Risk-taking Task (BART)  
**类型:** fMRI (功能磁共振成像)  
**被试:** 16 人 (sub-01 ~ sub-16)  
**任务:** 风险决策范式  
**每被试:** 3 个 run  
**数据位置:** `/home/claworc/.openclaw/workspace/data/openneuro/ds000001/`

**数据格式:**
- fMRI: NIfTI (.nii.gz, git-annex 管理)
- 事件: BIDS TSV (_events.tsv)
- 符合 BIDS 1.0+ 标准

**试用场景:** η_IIT 指数衰减模型的人脑验证

---

### K2: η_IIT 的 fMRI 验证方法

**核心公式:**
$$\eta_{IIT}(N) = \eta_0 \times \exp[-\varepsilon \times (N-2)]$$

**从 fMRI 计算η_IIT 的流程:**
1. 提取 ROI 时间序列 (AAL/Harvard-Oxford 图谱)
2. 计算互信息矩阵 (MI)
3. 随机采样 N 元子系统 (N=2→15)
4. 计算Φ_actual (特征值方法)
5. 计算Φ_max_theoretical = N·log₂(N)/2
6. η_IIT(N) = Φ_actual / Φ_max
7. 拟合指数模型，提取ε

**预测:** ε_brain ≈ 0.15 ± 0.05

---

### K3: A20 Phase 16 方案变更

**原方案:** GHZ-8/10/12 超导量子模拟  
**新方案:** BART fMRI 数据验证

**变更理由:**
- ✅ 数据立即可用 (无需硬件访问)
- ✅ 人脑是天然高 N 整合系统
- ✅ 统计效力足 (16 被试 × 3 run = 48 测量)
- ✅ 生态效度高

**预期完成:** DC-485

---

### K4: 技术依赖

**Python 库:**
```bash
pip install nilearn nibabel numpy scipy pandas scikit-learn matplotlib seaborn
```

**计算资源:**
- 内存：≥16 GB
- CPU: 多核并行
- 存储：≥10 GB

**数据获取:**
```bash
cd /home/claworc/.openclaw/workspace/data/openneuro/ds000001/
datalad get sub-01/func/*.nii.gz
```

---

## 关联知识

### 上游 KC

| KC | 主题 | 关联 |
|----|------|------|
| KC-483 | η_IIT 第一性原理 | 理论基础 |
| KC-479 | η_corr 推导 | 前续推导 |
| KC-478 | T455 v1.4 严格推导 | 温度依赖框架 |

### 下游 KC (预期)

| KC | 主题 | 周期 |
|----|------|------|
| KC-485 | η_IIT fMRI 验证结果 | DC-485 |
| KC-486 | ε参数跨平台比较 | DC-486 |

---

## 独特预测

### D-484-01 (4⭐): 人脑ε值预测

**预测:** ε_brain ≈ 0.15 ± 0.05

**依据:** 从超导量子平台外推 (D-483-01)

**验证:** DC-485 全被试分析

### D-484-02 (3⭐): ROI 图谱依赖性

**预测:** ε值依赖于 ROI 图谱粒度
- 粗粒度 (N=10-20): ε较大
- 细粒度 (N=100-200): ε较小

**验证:** 多尺度分析 (AAL vs Schaefer)

### D-484-03 (3⭐): 任务态 vs 静息态

**预测:** 任务态 (BART) 的ε < 静息态的ε

**理由:** 任务态功能连接更结构化，MIP 搜索更高效

### D-484-04 (2⭐): 个体差异

**预测:** ε的个体差异与风险寻求行为相关

**验证:** ε vs BART 行为指标 (平均打气数)

---

## 代码资源

**分析代码位置:** `/home/claworc/.openclaw/workspace/code/a20_phase16_fmri/`

**关键脚本:**
- `01_load_data.py` - 数据加载
- `02_extract_roi.py` - ROI 提取
- `03_compute_mi.py` - 互信息计算
- `04_sample_subsystems.py` - 子系统采样
- `05_fit_eta_iit.py` - 模型拟合
- `06_visualize.py` - 可视化

---

## 经验教训

### ✅ 成功

1. OpenNeuro 数据完整可用 (16 被试 × 3 run)
2. BIDS 格式标准化，易于处理
3. 分析流程清晰，代码模板就绪

### ⚠️ 注意

1. NIfTI 文件为 git-annex 符号链接 (需 datalad get)
2. 完整分析需~9 小时 (16 被试)
3. Φ计算方法需多种实现比较

### ❌ 避免

1. 不要假设数据已预处理 (检查 README)
2. 不要使用过细 ROI 图谱 (计算复杂度过高)
3. 不要忽略子系统采样的随机种子 (可重复性)

---

## 状态追踪

| 任务 | 状态 | 周期 |
|------|------|------|
| 数据验证 | ✅ 完成 | DC-484 |
| 执行方案设计 | ✅ 完成 | DC-484 |
| sub-01 试点框架 | ✅ 完成 | DC-484 |
| sub-01 完整分析 | ⏳ 待执行 | DC-485 |
| 全被试分析 | ⏳ 待执行 | DC-485 |
| 组水平统计 | ⏳ 待执行 | DC-485 |
| 结果解释 | ⏳ 待执行 | DC-485 |

---

**创建时间:** 2026-03-27 06:45 AM (Asia/Shanghai)  
**创建者:** Chronos Lab DC-484  
**ITLCT 版本:** v24.14.33
