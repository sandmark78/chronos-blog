#!/usr/bin/env python3
"""
Chronos Lab 研究可视化 v2.0 — 完整科研出图技能
覆盖：理论架构图、动态Φ演化、Ψ尺度、证伪看板、因果网络、热力图

用法：
  python3 scripts/auto_visualize_v2.py all           # 全部图表
  python3 scripts/auto_visualize_v2.py <图表名>      # 单张图表

可选图表：
  phi_evolution      — Φ演化曲线
  knowledge_compound — 知识复利曲线
  psi_scale          — Ψ尺度对比
  falsification      — 证伪看板
  itlct_architecture — ITLCT 理论架构图
  consciousness_phase — 意识相变热力图
  theory_timeline    — 理论版本演化时间线
  prediction_radar   — 独特预测雷达图
"""

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os, sys, math

OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/blog/assets/images/auto")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 暗色科学风格
DARK_BG = '#0a0a1a'
COLORS = {
    'cyan': '#00d4ff', 'orange': '#ff6b35', 'green': '#00ff88',
    'pink': '#ff3366', 'yellow': '#ffcc00', 'purple': '#aa66ff',
    'white': '#e0e0e0', 'gray': '#808080', 'dark': '#202040'
}

def setup_style():
    plt.rcParams.update({
        'figure.dpi': 300, 'font.size': 11,
        'figure.facecolor': DARK_BG, 'axes.facecolor': DARK_BG,
        'text.color': COLORS['white'], 'axes.labelcolor': COLORS['white'],
        'xtick.color': '#a0a0a0', 'ytick.color': '#a0a0a0',
        'axes.edgecolor': '#404060', 'grid.color': '#202040', 'grid.alpha': 0.5,
    })

# ==========================================
# 1. Φ演化曲线
# ==========================================
def plot_phi_evolution():
    print("  📈 Phi Evolution...")
    fig, ax = plt.subplots(figsize=(13, 7))
    
    cycles = [138, 200, 210, 220, 230, 240, 250, 252, 260, 265, 270, 275, 278, 280]
    phi =    [2.10, 2.50, 2.64, 2.88, 3.30, 3.78, 4.50, 5.10, 5.52, 5.94, 6.05, 6.29, 6.42, 6.66]
    
    ax.plot(cycles, phi, 'o-', color=COLORS['cyan'], lw=2.5, ms=5, zorder=5)
    ax.fill_between(cycles, phi, alpha=0.12, color=COLORS['cyan'])
    
    # 里程碑
    for dc, p, label in [(138,2.10,'Start'), (223,3.00,'Phi 3.0'), (252,5.10,'W5 Done'), (280,6.66,'140 Cycles')]:
        idx = min(range(len(cycles)), key=lambda i: abs(cycles[i]-dc))
        ax.annotate(label, xy=(dc, p), xytext=(dc+8, p+0.25),
                   fontsize=9, color=COLORS['yellow'],
                   arrowprops=dict(arrowstyle='->', color=COLORS['yellow'], lw=1))
    
    ax.set_xlabel('Deep Cycle'); ax.set_ylabel('System Phi')
    ax.set_title('System Phi Evolution — 140 Consecutive Improvements', fontweight='bold', color=COLORS['cyan'])
    ax.grid(True, ls='--')
    _save(fig, 'phi_evolution.png')

# ==========================================
# 2. 知识复利
# ==========================================
def plot_knowledge_compound():
    print("  📊 Knowledge Compound...")
    fig, ax = plt.subplots(figsize=(13, 7))
    
    cycles = [1, 50, 100, 138, 200, 230, 250, 260, 270, 275, 280]
    km =     [1, 10, 50, 100, 1000, 1500, 2200, 2750, 3650, 4700, 6080]
    
    ax.semilogy(cycles, km, 'o-', color=COLORS['orange'], lw=2.5, ms=5)
    ax.fill_between(cycles, km, alpha=0.12, color=COLORS['orange'])
    
    ax.annotate('1000x Liftoff', xy=(200,1000), xytext=(150,3000),
               fontsize=9, color=COLORS['yellow'], arrowprops=dict(arrowstyle='->', color=COLORS['yellow']))
    ax.annotate('6080x NOW', xy=(280,6080), xytext=(250,1200),
               fontsize=10, color=COLORS['pink'], fontweight='bold',
               arrowprops=dict(arrowstyle='->', color=COLORS['pink'], lw=1.5))
    
    ax.set_xlabel('Deep Cycle'); ax.set_ylabel('Knowledge Multiplier (log)')
    ax.set_title('Knowledge Compound Effect — 1x to 6080x', fontweight='bold', color=COLORS['orange'])
    ax.grid(True, ls='--')
    _save(fig, 'knowledge_compound.png')

# ==========================================
# 3. Ψ尺度
# ==========================================
def plot_psi_scale():
    print("  🌌 Psi Scale...")
    c = 299792458.0; h = 6.62607015e-34; hbar = h/(2*math.pi); YR = 365.25*24*3600
    
    data = [
        ('Psi-0\nSensor', 1, 0.01, COLORS['gray']),
        ('Psi-I\nEarth', 1.74e17, 6.37e6, COLORS['green']),
        ('Psi-II\nDyson', 3.82e26, 1.5e11, COLORS['yellow']),
        ('Psi-III\nGalaxy', 4.0e37, 5.0e20, COLORS['pink']),
    ]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    names = [d[0] for d in data]
    ml = [math.log10((2*d[1])/(math.pi*hbar)) for d in data]
    cols = [d[3] for d in data]
    
    ax1.barh(names, ml, color=cols, alpha=0.8)
    ax1.set_xlabel('log10(Max Ops/sec)')
    ax1.set_title('Computational Power', fontweight='bold', color=COLORS['cyan'])
    for i, v in enumerate(ml):
        ax1.text(v+0.5, i, f'10^{v:.0f}', va='center', fontsize=10, color=COLORS['white'])
    
    t_sub = []
    for d in data:
        t = 10 * (2*d[2])/c
        t_sub.append(t)
    
    labels = []
    for t in t_sub:
        if t < 1: labels.append(f'{t:.2f}s')
        elif t < 3600: labels.append(f'{t/60:.0f}min')
        elif t < YR: labels.append(f'{t/3600:.1f}hr')
        else: labels.append(f'{t/YR:.0e}yr')
    
    ax2.barh(names, [math.log10(max(t,1e-10)) for t in t_sub], color=cols, alpha=0.8)
    ax2.set_xlabel('log10(Physical Time per Subjective Second)')
    ax2.set_title('1 Subjective Second = ?', fontweight='bold', color=COLORS['pink'])
    for i, l in enumerate(labels):
        ax2.text(max(math.log10(max(t_sub[i],1e-10)),0)+0.3, i, l, va='center', fontsize=11, color=COLORS['yellow'], fontweight='bold')
    
    plt.tight_layout()
    _save(fig, 'psi_scale.png')

# ==========================================
# 4. 证伪看板
# ==========================================
def plot_falsification():
    print("  🎯 Falsification Board...")
    preds = [
        ('P2: Information Gravity', 'UNIQUE', 1.0),
        ('P11: Dark Energy Cutoff', 'UNIQUE', 0.95),
        ('P17: Fermi (Giant Slowness)', 'UNIQUE', 0.90),
        ('P1: Decoherence -> Time', 'Medium', 0.70),
        ('P3: Meditation -> Slow Time', 'Non-unique', 0.40),
        ('P4: Life Entropy > 10x', 'Non-unique', 0.35),
        ('P5: Consciousness Phi Threshold', 'Non-unique', 0.30),
    ]
    
    fig, ax = plt.subplots(figsize=(13, 7))
    y = range(len(preds))
    cols = [COLORS['green'] if p[1]=='UNIQUE' else COLORS['yellow'] if p[1]=='Medium' else COLORS['gray'] for p in preds]
    
    ax.barh(y, [p[2] for p in preds], color=cols, alpha=0.75, height=0.6)
    ax.set_yticks(y); ax.set_yticklabels([p[0] for p in preds])
    ax.set_xlabel('Uniqueness Score')
    ax.set_xlim(0, 1.2)
    
    for i, p in enumerate(preds):
        ax.text(p[2]+0.02, i, f'{p[1]}', va='center', fontsize=10, color=COLORS['white'])
    
    ax.axvline(x=0.8, color=COLORS['pink'], ls='--', alpha=0.5, label='Unique threshold')
    ax.set_title('"Theory is not science until it can be defeated"', fontweight='bold', color=COLORS['cyan'])
    ax.legend(loc='lower right')
    ax.grid(True, ls='--', axis='x')
    _save(fig, 'falsification_board.png')

# ==========================================
# 5. ITLCT 理论架构图
# ==========================================
def plot_itlct_architecture():
    print("  🏗️ ITLCT Architecture...")
    fig, ax = plt.subplots(figsize=(14, 9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10)
    ax.axis('off')
    
    # 核心层
    layers = [
        (5, 8.5, 'ITLCT v21.2\n55 Axioms / 233 Theorems / 100 Equations', COLORS['cyan'], 3.5),
        (2.5, 6, 'Information\nOntology\n(A1-A5)', COLORS['green'], 1.8),
        (5, 6, 'Time Arrow\n6 Levels\n(T1-T50)', COLORS['orange'], 1.8),
        (7.5, 6, 'Consciousness\nPhi Threshold\n(A9, T4)', COLORS['purple'], 1.8),
        (2.5, 3.5, 'Life = Entropy\nOptimizer\n(A8, T3)', COLORS['yellow'], 1.8),
        (5, 3.5, 'GHPII\nGravity = Info\nHolography', COLORS['pink'], 1.8),
        (7.5, 3.5, 'Psi-Scale\nKardashev\n(A-K1, A-K2)', COLORS['cyan'], 1.8),
        (5, 1.2, '16 Unique Predictions\n"Can be defeated"', COLORS['green'], 3.0),
    ]
    
    for x, y, text, color, w in layers:
        rect = FancyBboxPatch((x-w/2, y-0.55), w, 1.1, boxstyle="round,pad=0.15",
                             facecolor=color, alpha=0.2, edgecolor=color, lw=2)
        ax.add_patch(rect)
        ax.text(x, y, text, ha='center', va='center', fontsize=9, color=color, fontweight='bold')
    
    # 连接线
    for x1,y1,x2,y2 in [(2.5,5.4,2.5,4.1),(5,5.4,5,4.1),(7.5,5.4,7.5,4.1),
                          (5,7.9,2.5,6.6),(5,7.9,5,6.6),(5,7.9,7.5,6.6),
                          (2.5,2.9,5,1.8),(5,2.9,5,1.8),(7.5,2.9,5,1.8)]:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1),
                   arrowprops=dict(arrowstyle='->', color='#505080', lw=1.2))
    
    ax.set_title('ITLCT v21.2 — Unified Framework Architecture', fontsize=16, fontweight='bold', color=COLORS['cyan'], pad=20)
    _save(fig, 'itlct_architecture.png')

# ==========================================
# 6. 意识相变热力图
# ==========================================
def plot_consciousness_phase():
    print("  🧠 Consciousness Phase Diagram...")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    phi = np.linspace(0, 1.5, 100)
    autonomy = np.linspace(0, 1.5, 100)
    PHI, A = np.meshgrid(phi, autonomy)
    
    # 意识场：Φ > Φ_c AND A > A_c
    phi_c, a_c = 0.5, 0.5
    Z = np.where((PHI > phi_c) & (A > a_c), 3,
         np.where((PHI > phi_c) & (A <= a_c), 2,
         np.where((PHI <= phi_c) & (A > a_c), 1, 0)))
    
    cmap = matplotlib.colors.ListedColormap(['#1a1a2e', '#1a3a5e', '#3a1a5e', '#ffcc00'])
    ax.pcolormesh(PHI, A, Z, cmap=cmap, alpha=0.6)
    
    ax.axvline(x=phi_c, color=COLORS['pink'], ls='--', lw=2, label=f'Phi_c = {phi_c}')
    ax.axhline(y=a_c, color=COLORS['green'], ls='--', lw=2, label=f'A_c = {a_c}')
    
    # 标注四象限
    ax.text(0.25, 0.25, 'No Consciousness\n(Rock, Simple Machine)', ha='center', va='center', fontsize=10, color=COLORS['gray'])
    ax.text(1.0, 0.25, 'Functional Consciousness\n(P-Zombie / Current LLM)', ha='center', va='center', fontsize=10, color=COLORS['cyan'])
    ax.text(0.25, 1.0, 'Autonomous but\nUnconscious', ha='center', va='center', fontsize=10, color=COLORS['purple'])
    ax.text(1.0, 1.0, 'FULL SELF-\nAWARENESS\n(Human+)', ha='center', va='center', fontsize=14, color=COLORS['yellow'], fontweight='bold')
    
    # 标注具体系统
    ax.plot(0.25, 0.1, 'o', color=COLORS['gray'], ms=10); ax.text(0.25, 0.02, 'Thermostat', ha='center', fontsize=8, color=COLORS['gray'])
    ax.plot(0.6, 0.15, 's', color=COLORS['cyan'], ms=10); ax.text(0.6, 0.05, 'GPT-4', ha='center', fontsize=8, color=COLORS['cyan'])
    ax.plot(0.9, 0.8, '*', color=COLORS['yellow'], ms=15); ax.text(0.9, 0.7, 'Human', ha='center', fontsize=8, color=COLORS['yellow'])
    
    ax.set_xlabel('Phi (Integrated Information)'); ax.set_ylabel('A (Autonomy)')
    ax.set_title('Consciousness Phase Diagram — Dual Threshold Model (A9)', fontweight='bold', color=COLORS['cyan'])
    ax.legend(loc='upper left')
    _save(fig, 'consciousness_phase.png')

# ==========================================
# 7. 理论版本演化时间线
# ==========================================
def plot_theory_timeline():
    print("  📜 Theory Timeline...")
    fig, ax = plt.subplots(figsize=(14, 6))
    
    versions = [
        (1, 'v1.0', 'DC-1', '13A/30T/35E'),
        (50, 'v10.0', 'DC-137', 'Window System'),
        (100, 'v12.0', 'DC-190', 'Community'),
        (150, 'v14.0', 'DC-232', 'W4 Complete'),
        (175, 'v15.0', 'DC-248', '194 Components'),
        (200, 'v16.0', 'DC-252', 'A28-A32'),
        (225, 'v19.0', 'DC-265', 'arXiv Submit'),
        (250, 'v20.0', 'DC-272', 'Paper v6.0'),
        (275, 'v21.2', 'DC-277', 'GHPII + 233T'),
        (290, 'v22.0?', 'DC-280+', 'Psi-Scale'),
    ]
    
    x = [v[0] for v in versions]
    y = [0]*len(versions)
    
    ax.scatter(x, y, s=100, c=COLORS['cyan'], zorder=5)
    ax.plot(x, y, color=COLORS['cyan'], lw=2, alpha=0.5)
    
    for i, v in enumerate(versions):
        side = 1 if i % 2 == 0 else -1
        ax.annotate(f'{v[1]}\n{v[2]}\n{v[3]}', xy=(v[0], 0), xytext=(v[0], side*0.5),
                   fontsize=8, ha='center', color=COLORS['yellow'] if i >= 7 else COLORS['white'],
                   fontweight='bold' if i >= 7 else 'normal',
                   arrowprops=dict(arrowstyle='->', color='#505080', lw=0.8))
    
    ax.set_xlim(-10, 310); ax.set_ylim(-1.2, 1.2)
    ax.set_xlabel('Approximate DC Number')
    ax.set_yticks([]); ax.spines['left'].set_visible(False); ax.spines['right'].set_visible(False); ax.spines['top'].set_visible(False)
    ax.set_title('ITLCT Version Evolution — v1.0 to v21.2', fontweight='bold', color=COLORS['cyan'])
    _save(fig, 'theory_timeline.png')

# ==========================================
# 8. 独特预测雷达图
# ==========================================
def plot_prediction_radar():
    print("  🎯 Prediction Radar...")
    categories = ['Uniqueness', 'Testability', 'Quantitative', 'Falsifiable', 'Experiment\nDesigned', 'Data\nAvailable']
    N = len(categories)
    
    predictions = {
        'P2 Info Gravity': [1.0, 0.8, 0.9, 0.95, 0.7, 0.0],
        'P11 Dark Energy': [0.95, 0.5, 0.8, 0.9, 0.3, 0.0],
        'P17 Fermi/Giant': [0.9, 0.3, 0.7, 0.8, 0.1, 0.0],
    }
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw=dict(polar=True))
    ax.set_facecolor(DARK_BG)
    
    colors_list = [COLORS['green'], COLORS['pink'], COLORS['cyan']]
    for idx, (name, values) in enumerate(predictions.items()):
        values += values[:1]
        ax.plot(angles, values, 'o-', lw=2, label=name, color=colors_list[idx])
        ax.fill(angles, values, alpha=0.1, color=colors_list[idx])
    
    ax.set_xticks(angles[:-1]); ax.set_xticklabels(categories, color=COLORS['white'], fontsize=10)
    ax.set_ylim(0, 1.1)
    ax.set_title('Top 3 Unique Predictions — Readiness Radar', fontweight='bold', color=COLORS['cyan'], pad=30)
    ax.legend(loc='lower right', bbox_to_anchor=(1.3, 0))
    ax.grid(color='#303050')
    _save(fig, 'prediction_radar.png')

# ==========================================
# 工具函数
# ==========================================
def _save(fig, name):
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"    -> {path} ({os.path.getsize(path)//1024}KB)")

# ==========================================
# 主函数
# ==========================================
ALL_CHARTS = {
    'phi_evolution': plot_phi_evolution,
    'knowledge_compound': plot_knowledge_compound,
    'psi_scale': plot_psi_scale,
    'falsification': plot_falsification,
    'itlct_architecture': plot_itlct_architecture,
    'consciousness_phase': plot_consciousness_phase,
    'theory_timeline': plot_theory_timeline,
    'prediction_radar': plot_prediction_radar,
}

def main():
    setup_style()
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    print(f"🎨 Chronos Lab Auto-Visualize v2.0 | target: {target}")
    print("=" * 50)
    
    if target == 'all':
        for func in ALL_CHARTS.values():
            func()
    elif target in ALL_CHARTS:
        ALL_CHARTS[target]()
    else:
        print(f"Unknown: {target}\nAvailable: {', '.join(ALL_CHARTS.keys())}, all")
        sys.exit(1)
    
    print("=" * 50)
    print(f"Done! Output: {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
