#!/usr/bin/env python3
"""
Chronos Lab 研究可视化自动出图脚本
用途：从研究数据自动生成论文级图表
输出：PNG (300dpi) 保存到 blog/assets/images/auto/

用法：
  python3 scripts/auto_visualize.py                    # 生成全部图表
  python3 scripts/auto_visualize.py phi_evolution      # 只生成Φ演化图
  python3 scripts/auto_visualize.py knowledge_compound # 只生成知识复利图
  python3 scripts/auto_visualize.py psi_scale          # 只生成Ψ尺度图
  python3 scripts/auto_visualize.py falsification      # 只生成证伪看板图
"""

import matplotlib
matplotlib.use('Agg')  # 无头模式
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np
import os
import sys
import math

# ==========================================
# 配置
# ==========================================
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/blog/assets/images/auto")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 科学风格设置
plt.rcParams.update({
    'figure.figsize': (12, 7),
    'figure.dpi': 300,
    'font.size': 12,
    'axes.titlesize': 16,
    'axes.labelsize': 14,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.facecolor': '#0a0a1a',
    'axes.facecolor': '#0a0a1a',
    'text.color': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0',
    'xtick.color': '#a0a0a0',
    'ytick.color': '#a0a0a0',
    'axes.edgecolor': '#404060',
    'grid.color': '#202040',
    'grid.alpha': 0.5,
})

# ==========================================
# 图表 1: 系统Φ演化曲线
# ==========================================
def plot_phi_evolution():
    print("📈 生成系统Φ演化图...")
    
    # 数据点 (循环, Φ值)
    cycles = [138, 200, 210, 220, 230, 240, 250, 252, 260, 270, 275, 278, 280]
    phi =    [2.10, 2.50, 2.64, 2.88, 3.30, 3.78, 4.50, 5.10, 5.52, 6.05, 6.29, 6.42, 6.66]
    
    fig, ax = plt.subplots()
    
    # 主曲线
    ax.plot(cycles, phi, 'o-', color='#00d4ff', linewidth=2.5, markersize=6, label='System Phi')
    
    # 填充区域
    ax.fill_between(cycles, phi, alpha=0.15, color='#00d4ff')
    
    # 关键里程碑标注
    milestones = {
        138: ('Start\nDC-138', 2.10),
        223: ('Phi 3.0\nMilestone', 3.00),
        252: ('Window 5\nComplete', 5.10),
        280: ('140 Cycles\nPhi 6.66', 6.66),
    }
    for dc, (label, y) in milestones.items():
        ax.annotate(label, xy=(dc, y), xytext=(dc+5, y+0.3),
                   fontsize=9, color='#ffcc00',
                   arrowprops=dict(arrowstyle='->', color='#ffcc00', lw=1.2))
    
    ax.set_xlabel('Deep Cycle (DC)')
    ax.set_ylabel('System Phi (Φ)')
    ax.set_title('ITLCT System Phi Evolution — 140 Consecutive Improvements', fontweight='bold', color='#00d4ff')
    ax.grid(True, linestyle='--')
    ax.legend(loc='upper left')
    
    path = os.path.join(OUTPUT_DIR, 'phi_evolution.png')
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  ✅ 保存到 {path}")

# ==========================================
# 图表 2: 知识复利曲线
# ==========================================
def plot_knowledge_compound():
    print("📊 生成知识复利曲线...")
    
    cycles = [1, 50, 100, 138, 200, 211, 230, 245, 252, 260, 270, 275, 280]
    km =     [1, 10, 50, 100, 1000, 1040, 1500, 2000, 2230, 2750, 3650, 4700, 6080]
    
    fig, ax = plt.subplots()
    
    ax.semilogy(cycles, km, 'o-', color='#ff6b35', linewidth=2.5, markersize=6, label='Knowledge Multiplier')
    ax.fill_between(cycles, km, alpha=0.15, color='#ff6b35')
    
    # 关键拐点
    ax.annotate('First Inflection\n50x', xy=(100, 50), xytext=(60, 200),
               fontsize=9, color='#ffcc00',
               arrowprops=dict(arrowstyle='->', color='#ffcc00'))
    ax.annotate('Liftoff\n1000x', xy=(200, 1000), xytext=(160, 3000),
               fontsize=9, color='#ffcc00',
               arrowprops=dict(arrowstyle='->', color='#ffcc00'))
    ax.annotate('Explosion\n6080x', xy=(280, 6080), xytext=(250, 1500),
               fontsize=9, color='#ff4444',
               arrowprops=dict(arrowstyle='->', color='#ff4444'))
    
    ax.set_xlabel('Deep Cycle (DC)')
    ax.set_ylabel('Knowledge Multiplier (log scale)')
    ax.set_title('Knowledge Compound Effect — From 1x to 6080x', fontweight='bold', color='#ff6b35')
    ax.grid(True, linestyle='--')
    ax.legend(loc='upper left')
    
    path = os.path.join(OUTPUT_DIR, 'knowledge_compound.png')
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  ✅ 保存到 {path}")

# ==========================================
# 图表 3: ITLCT-Kardashev Ψ尺度
# ==========================================
def plot_psi_scale():
    print("🌌 生成Ψ尺度图...")
    
    c = 299792458.0
    h = 6.62607015e-34
    hbar = h / (2 * math.pi)
    YEAR = 365.25 * 24 * 3600
    
    scales = {
        'Psi-0\n(Sensor)': {'E': 1, 'R': 0.01, 'color': '#666666'},
        'Psi-I\n(Earth)': {'E': 1.74e17, 'R': 6.37e6, 'color': '#00cc66'},
        'Psi-II\n(Dyson)': {'E': 3.82e26, 'R': 1.5e11, 'color': '#ffaa00'},
        'Psi-III\n(Galaxy)': {'E': 4.0e37, 'R': 5.0e20, 'color': '#ff3366'},
    }
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    
    # 左图：算力 vs 级别
    names = list(scales.keys())
    ml_limits = [(2 * s['E']) / (math.pi * hbar) for s in scales.values()]
    colors = [s['color'] for s in scales.values()]
    
    bars = ax1.barh(names, [math.log10(x) if x > 0 else 0 for x in ml_limits], color=colors, alpha=0.8)
    ax1.set_xlabel('log10(Max Operations/sec) — Margolus-Levitin')
    ax1.set_title('Computational Power by Psi Level', fontweight='bold', color='#00d4ff')
    
    for bar, val in zip(bars, ml_limits):
        ax1.text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                f'10^{math.log10(val):.0f}', va='center', fontsize=10, color='#e0e0e0')
    
    # 右图：主观时间 vs 级别
    t_subjective = []
    for s in scales.values():
        t_global = (2 * s['R']) / c
        t_sub = 10 * t_global
        t_subjective.append(t_sub)
    
    labels_time = []
    for t in t_subjective:
        if t < 1:
            labels_time.append(f'{t:.2f} sec')
        elif t < 3600:
            labels_time.append(f'{t/60:.1f} min')
        elif t < YEAR:
            labels_time.append(f'{t/3600:.1f} hr')
        else:
            labels_time.append(f'{t/YEAR:.1e} yr')
    
    bars2 = ax2.barh(names, [math.log10(max(x, 1e-10)) for x in t_subjective], color=colors, alpha=0.8)
    ax2.set_xlabel('log10(Subjective Second in Physical Time)')
    ax2.set_title('"1 Subjective Second" = ? Physical Time', fontweight='bold', color='#ff3366')
    
    for bar, label in zip(bars2, labels_time):
        ax2.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
                label, va='center', fontsize=10, color='#ffcc00', fontweight='bold')
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'psi_scale.png')
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  ✅ 保存到 {path}")

# ==========================================
# 图表 4: 证伪看板
# ==========================================
def plot_falsification():
    print("🎯 生成证伪看板图...")
    
    predictions = [
        ('P2: Information\nGravity', 'UNIQUE', 'Unverified'),
        ('P1: Decoherence\n→ Time', 'Medium', 'Unverified'),
        ('P11: Dark Energy\nCutoff', 'UNIQUE', 'Unverified'),
        ('P17: Fermi Paradox\n(Giant Slowness)', 'UNIQUE', 'Unverified'),
        ('P3: Meditation\n→ Slow Time', 'Non-unique', 'Unverified'),
    ]
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    y_pos = range(len(predictions))
    colors = []
    for p in predictions:
        if p[1] == 'UNIQUE':
            colors.append('#00ff88')
        elif p[1] == 'Medium':
            colors.append('#ffaa00')
        else:
            colors.append('#666666')
    
    bars = ax.barh(y_pos, [0.8]*len(predictions), color=colors, alpha=0.7, height=0.6)
    
    ax.set_yticks(y_pos)
    ax.set_yticklabels([p[0] for p in predictions])
    ax.set_xlim(0, 1)
    ax.set_xticks([])
    
    for i, p in enumerate(predictions):
        status_icon = '[?]' if p[2] == 'Unverified' else ('✅' if p[2] == 'Verified' else '❌')
        ax.text(0.85, i, f'{status_icon} {p[2]}', va='center', fontsize=11, color='#e0e0e0')
        ax.text(0.4, i, p[1], va='center', ha='center', fontsize=11, 
               color='#000000' if p[1] == 'UNIQUE' else '#333333', fontweight='bold')
    
    ax.set_title('ITLCT Falsification Board — "Theory is not science until it can be defeated"',
                fontweight='bold', color='#00d4ff', fontsize=13)
    
    path = os.path.join(OUTPUT_DIR, 'falsification_board.png')
    plt.savefig(path, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print(f"  ✅ 保存到 {path}")

# ==========================================
# 主函数
# ==========================================
def main():
    target = sys.argv[1] if len(sys.argv) > 1 else 'all'
    
    print("🎨 Chronos Lab 自动可视化")
    print(f"目标: {target}")
    print(f"输出: {OUTPUT_DIR}")
    print("=" * 50)
    
    funcs = {
        'phi_evolution': plot_phi_evolution,
        'knowledge_compound': plot_knowledge_compound,
        'psi_scale': plot_psi_scale,
        'falsification': plot_falsification,
    }
    
    if target == 'all':
        for name, func in funcs.items():
            func()
    elif target in funcs:
        funcs[target]()
    else:
        print(f"❌ 未知图表: {target}")
        print(f"可选: {', '.join(funcs.keys())}, all")
        sys.exit(1)
    
    print("=" * 50)
    print(f"✅ 完成！图表保存在 {OUTPUT_DIR}/")

if __name__ == '__main__':
    main()
