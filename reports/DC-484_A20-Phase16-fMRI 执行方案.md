# DC-484 A20 Phase 16 fMRI 执行方案

**周期:** DC-484  
**日期:** 2026-03-27  
**状态:** ✅ 完成  
**版本:** A20-Phase16-fMRI-v1.0

---

## 摘要

本方案将 A20 Phase 16 从原定的 GHZ-8/10/12 超导量子模拟更新为**使用 OpenNeuro BART fMRI 数据进行η_IIT 验证**。核心目标是从 fMRI 时间序列计算脑区功能连接和互信息，拟合η_IIT(N) = η₀ × exp[-ε×(N-2)] 指数衰减模型，验证α_IIT ≈ 0.15±0.05。

**方案变更:** GHZ 量子模拟 → fMRI 人脑数据验证  
**数据集:** OpenNeuro ds000001 (16 被试 × 3 run BART 任务)

---

## 1. 方案变更理由

### 1.1 原方案 (A20 Phase 16A)

**目标:** GHZ-8/10/12 超导量子模拟验证η_corr 标度

**限制:**
- 需要 IBM Quantum 访问权限 (DC-342-001 已过截止)
- 量子硬件噪声可能混淆η_IIT 测量
- N=8/10/12 规模较小，拟合精度有限

### 1.2 新方案 (A20 Phase 16-fMRI)

**目标:** 使用 BART fMRI 数据验证η_IIT 指数衰减模型

**优势:**
- ✅ 数据立即可用 (16 被试 × 3 run = 48 独立测量)
- ✅ 人脑是天然的高 N 整合系统 (N≈100-1000 脑区)
- ✅ 风险决策任务激活分布式网络 (适合 IIT 分析)
- ✅ 无需外部硬件访问权限

### 1.3 理论依据

DC-483 从 IIT 4.0 整合公理第一性原理推导:
$$\eta_{IIT}(N) = \eta_0 \times \exp[-\varepsilon \times (N-2)]$$

**预测:**
- η_IIT 随脑区数量 N 指数衰减
- ε参数反映 MIP 算法效率损失
- 人脑数据应显示ε≈0.15±0.05 (基于量子平台外推)

---

## 2. 数据处理流程

### 2.1 总体流程

```
原始 fMRI 数据 (NIfTI)
    ↓
预处理 (去噪、标准化、平滑)
    ↓
ROI 时间序列提取 (AAL/Harvard-Oxford 图谱)
    ↓
功能连接矩阵计算 (相关系数/协方差)
    ↓
互信息矩阵计算 (MI)
    ↓
构建不同 N 规模的子系统 (N=2,3,4,...,N_max)
    ↓
计算每个 N 的Φ_actual 和Φ_max_theoretical
    ↓
拟合η_IIT(N) = Φ_actual / Φ_max
    ↓
提取ε参数，验证指数衰减模型
```

### 2.2 预处理要求

**假设:** 数据已进行基础预处理 (检查 README)

**如需额外预处理:**
1. **去噪:** ICA-AROMA 去除运动伪影
2. **标准化:** MNI 空间配准
3. **平滑:** 6mm FWHM 高斯平滑
4. **去趋势:** 线性/二次趋势去除
5. **滤波:** 0.01-0.1 Hz 带通滤波

**工具:** fMRIPrep, Nilearn, FSL

### 2.3 ROI 定义

**推荐图谱:**
- **AAL (Automated Anatomical Labeling):** 116 脑区
- **Harvard-Oxford:** 48 皮质 + 21 皮质下脑区
- **Schaefer:** 100-1000 脑区 (多尺度)

**多尺度分析:**
- 粗粒度: N=10-20 脑区 (大网络)
- 中粒度: N=50-100 脑区 (中等网络)
- 细粒度: N=200-400 脑区 (精细网络)

---

## 3. η_IIT 计算方法

### 3.1 从 fMRI 时间序列计算Φ

**步骤:**

1. **提取 ROI 时间序列:**
   ```python
   from nilearn import datasets, input_data
   
   atlas = datasets.fetch_atlas_aal()
   masker = input_data.NiftiLabelsMasker(labels_img=atlas.maps)
   time_series = masker.fit_transform(fmri_img)
   ```

2. **计算功能连接矩阵:**
   ```python
   import numpy as np
   
   # 皮尔逊相关系数
   corr_matrix = np.corrcoef(time_series.T)
   
   # 或协方差矩阵
   cov_matrix = np.cov(time_series.T)
   ```

3. **计算互信息矩阵:**
   ```python
   from sklearn.metrics import mutual_info_score
   
   def compute_mi_matrix(time_series, n_bins=10):
       n_rois = time_series.shape[1]
       mi_matrix = np.zeros((n_rois, n_rois))
       
       # 离散化时间序列
       discretized = np.digitize(time_series, 
                                  bins=np.linspace(time_series.min(), 
                                                   time_series.max(), 
                                                   n_bins))
       
       for i in range(n_rois):
           for j in range(i+1, n_rois):
               mi = mutual_info_score(discretized[:, i], 
                                     discretized[:, j])
               mi_matrix[i, j] = mi_matrix[j, i] = mi
       
       return mi_matrix
   ```

4. **计算Φ (整合信息):**
   
   使用简化版本 (基于特征值分解):
   ```python
   def compute_phi_simplified(mi_matrix):
       # 方法 1: 基于特征值谱
       eigenvalues = np.linalg.eigvalsh(mi_matrix)
       phi = np.sum(eigenvalues[eigenvalues > 0])
       return phi
   ```

### 3.2 计算Φ_max_theoretical

**方法:** 对于给定 N，理论最大Φ发生在完全整合系统

$$\Phi_{max}(N) = \frac{N \cdot \log_2(N)}{2}$$

(来自 DC-378 H1-T418 统一框架)

### 3.3 计算η_IIT

$$\eta_{IIT}(N) = \frac{\Phi_{actual}(N)}{\Phi_{max\_theoretical}(N)}$$

---

## 4. 子系统采样策略

### 4.1 挑战

对于 N 脑区系统，穷举所有 N 元子系统组合数:
$$C(N_{total}, N) = \binom{N_{total}}{N}$$

例如 N_total=100, N=10: C(100,10) ≈ 1.7×10¹³ (不可行)

### 4.2 解决方案: 随机采样

**策略:**
- 每个 N 规模随机采样 100-1000 个子系统
- 计算平均Φ_actual
- 估计η_IIT(N)

**代码框架:**
```python
def sample_subsystems(mi_matrix, n_subsystems=100):
    n_total = mi_matrix.shape[0]
    eta_iit_curve = []
    
    for n in range(2, min(20, n_total)):  # N=2→20
        phi_actual_list = []
        
        for _ in range(n_subsystems):
            # 随机选择 n 个 ROI
            indices = np.random.choice(n_total, n, replace=False)
            sub_mi = mi_matrix[np.ix_(indices, indices)]
            
            # 计算Φ
            phi = compute_phi_simplified(sub_mi)
            phi_actual_list.append(phi)
        
        phi_mean = np.mean(phi_actual_list)
        phi_max = n * np.log2(n) / 2
        eta_iit = phi_mean / phi_max
        
        eta_iit_curve.append((n, eta_iit))
    
    return eta_iit_curve
```

### 4.3 N 范围选择

**推荐:** N=2→20 (至少 10 个点用于拟合)

**理由:**
- N<2: 无意义 (Φ=0)
- N>20: 计算复杂度急剧增加
- 10+ 数据点足够拟合指数模型

---

## 5. 模型拟合与验证

### 5.1 指数衰减模型拟合

**模型:**
$$\eta_{IIT}(N) = \eta_0 \times \exp[-\varepsilon \times (N-2)]$$

**拟合方法:**
```python
from scipy.optimize import curve_fit

def eta_iit_model(N, eta0, epsilon):
    return eta0 * np.exp(-epsilon * (N - 2))

# 拟合
N_values = [x[0] for x in eta_iit_curve]
eta_values = [x[1] for x in eta_iit_curve]

popt, pcov = curve_fit(eta_iit_model, N_values, eta_values, 
                       p0=[1.0, 0.15])

eta0_fit, epsilon_fit = popt
eta0_std, epsilon_std = np.sqrt(np.diag(pcov))
```

### 5.2 验证标准

| 参数 | 预测值 | 验证标准 |
|------|--------|----------|
| η₀ | ≈1.0 | 0.8 < η₀ < 1.2 |
| ε | ≈0.15 | 0.10 < ε < 0.20 |
| R² | - | R² > 0.90 |

### 5.3 统计检验

1. **拟合优度:** R², Adjusted R²
2. **残差分析:** 检查残差是否随机分布
3. **模型比较:** vs 线性模型 (AIC/BIC)
4. **Bootstrap 置信区间:** 1000 次重采样

---

## 6. 被试间分析

### 6.1 个体水平分析

对每个被试 (sub-01 ~ sub-16) 分别:
1. 平均 3 个 run 的时间序列
2. 计算η_IIT(N) 曲线
3. 拟合ε参数

### 6.2 组水平分析

**汇总统计:**
```python
epsilon_values = [epsilon_sub01, epsilon_sub02, ..., epsilon_sub16]

epsilon_mean = np.mean(epsilon_values)
epsilon_std = np.std(epsilon_values)
epsilon_se = epsilon_std / np.sqrt(16)
epsilon_95ci = [epsilon_mean - 1.96*epsilon_se, 
                epsilon_mean + 1.96*epsilon_se]
```

**预测:** ε_group ≈ 0.15 ± 0.05

### 6.3 个体差异分析

**探索性分析:**
- ε与行为指标 (风险寻求) 的相关性
- 性别/年龄差异
- run 内一致性 (test-retest reliability)

---

## 7. 预期结果与解释

### 7.1 预期场景 A: 验证成功

**结果:** ε ≈ 0.15 ± 0.05, R² > 0.90

**解释:**
- ✅ η_IIT 指数衰减模型得到人脑数据支持
- ✅ MIP 算法效率损失随 N 指数增长
- ✅ ITLCT 预测跨平台普适性 (量子→人脑)

**发表价值:** 高 (首次在人脑验证η_IIT 理论)

### 7.2 预期场景 B: 部分验证

**结果:** ε ≈ 0.10-0.25, R² > 0.70

**解释:**
- ⚠️ 趋势符合预测，但拟合质量中等
- ⚠️ 可能原因：fMRI 噪声、ROI 定义不精确、Φ计算方法需优化

**下一步:** 改进Φ计算算法，增加被试数量

### 7.3 预期场景 C: 验证失败

**结果:** ε < 0 或 R² < 0.50

**解释:**
- ❌ 指数模型可能不适用人脑数据
- ❌ 需要重新考虑η_IIT 的定义或计算方法
- ❌ 或 fMRI 数据不适合Φ测量 (时间分辨率限制)

**理论修正:** 可能需要修改η_IIT(N) 模型形式

---

## 8. 时间规划

### 8.1 阶段划分

| 阶段 | 任务 | 预计时间 |
|------|------|----------|
| **Phase 16A** | 数据获取与预处理 | 1-2 天 |
| **Phase 16B** | sub-01 试点分析 | 1 天 |
| **Phase 16C** | 全被试分析 (sub-01~16) | 2-3 天 |
| **Phase 16D** | 模型拟合与验证 | 1 天 |
| **Phase 16E** | 结果解释与报告 | 1 天 |

**总时间:** 6-8 天

### 8.2 里程碑

- ✅ **M1:** OpenNeuro 数据验证完成 (DC-484 推演 1)
- ⏳ **M2:** sub-01 试点分析完成 (DC-484 推演 3)
- ⏳ **M3:** 全被试分析完成 (DC-485)
- ⏳ **M4:** ε参数拟合与验证 (DC-485)
- ⏳ **M5:** 整合报告与知识固化 (DC-485)

---

## 9. 技术依赖

### 9.1 Python 库

```bash
pip install nilearn nibabel numpy scipy pandas scikit-learn matplotlib seaborn
```

### 9.2 计算资源

- **内存:** ≥16 GB (处理全脑 ROI 时间序列)
- **CPU:** 多核并行 (加速子系统采样)
- **存储:** ≥10 GB (预处理后数据)

### 9.3 代码仓库

**推荐位置:** `/home/claworc/.openclaw/workspace/code/a20_phase16_fmri/`

**结构:**
```
a20_phase16_fmri/
├── data/           # 数据 (符号链接到 openneuro/)
├── src/            # 源代码
│   ├── preprocessing.py
│   ├── roi_extraction.py
│   ├── phi_computation.py
│   ├── eta_iit_fitting.py
│   └── visualization.py
├── results/        # 结果
│   ├── sub-01/
│   ├── group/
│   └── figures/
└── notebooks/      # Jupyter notebooks
    └── pilot_analysis.ipynb
```

---

## 10. 风险与缓解

### 10.1 风险 1: 数据预处理复杂

**缓解:** 使用 fMRIPrep 标准化流程，或假设数据已预处理

### 10.2 风险 2: Φ计算算法争议

**缓解:** 实现多种Φ计算方法 (特征值、MIP 近似、信息论)，比较结果

### 10.3 风险 3: 拟合质量差

**缓解:** 
- 增加子系统采样数 (100→1000)
- 调整 N 范围 (2→15 vs 2→30)
- 尝试替代模型 (幂律、双指数)

### 10.4 风险 4: 计算时间过长

**缓解:** 
- 先试点分析 (sub-01, N=2→10)
- 使用并行计算
- 降采样 ROI 数量

---

## 11. 与 DC-483 的衔接

### 11.1 理论延续

DC-483 提出:
$$\eta_{IIT}(N) = \eta_0 \times \exp[-\varepsilon \times (N-2)]$$

DC-484 验证:
- 使用人脑 fMRI 数据
- 独立于量子平台
- 测试普适性

### 11.2 预测延续

**DC-483 预测 (D-483-01):** ε的平台依赖性
- SC: ε≈0.15-0.25
- IT: ε≈0.05-0.15
- NA: ε≈0.10-0.20
- Phot: ε≈0.20-0.30

**DC-484 新增预测:** 
- **人脑:** ε_brain ≈ 0.15±0.05 (基于 SC 外推)

### 11.3 知识累积

| 周期 | 贡献 | 累计独特预测 |
|------|------|--------------|
| DC-483 | η_IIT 第一性原理推导 | 247 |
| DC-484 | fMRI 验证方案 | 251 (+4) |
| DC-485 | 实证结果 | 255+ (预期) |

---

## 12. 交付物清单

### 12.1 代码

- [ ] `src/preprocessing.py` - 数据预处理
- [ ] `src/roi_extraction.py` - ROI 时间序列提取
- [ ] `src/phi_computation.py` - Φ计算
- [ ] `src/eta_iit_fitting.py` - 模型拟合
- [ ] `src/visualization.py` - 结果可视化

### 12.2 报告

- [x] `reports/DC-484_OpenNeuro 数据验证.md` (推演 1)
- [x] `reports/DC-484_A20-Phase16-fMRI 执行方案.md` (本文件)
- [ ] `reports/DC-484_sub-01 试点分析.md` (推演 3)
- [ ] `reports/DC-484_核心研究推导.md` (推演 4)
- [ ] `reports/DC-484_三重验证整合报告.md` (推演 4)

### 12.3 知识卡片

- [ ] `knowledge-cards/KC-484_OpenNeuro 数据整合.md`

---

## 13. 结论

A20 Phase 16 fMRI 执行方案利用 OpenNeuro BART 数据集验证η_IIT 指数衰减模型，具有以下优势:

1. ✅ **数据立即可用** - 无需等待硬件访问
2. ✅ **生态效度高** - 人脑是天然整合系统
3. ✅ **统计效力足** - 16 被试 × 3 run = 48 测量
4. ✅ **理论预测清晰** - ε≈0.15±0.05

**预期完成时间:** DC-485 (2026-03-28)  
**预期产出:** ε参数实证估计 + η_IIT 模型验证/修正

---

**方案制定时间:** 2026-03-27 06:15 AM (Asia/Shanghai)  
**制定者:** Chronos Lab DC-484 子代理  
**ITLCT 版本:** v24.14.33
