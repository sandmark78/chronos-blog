"""
ITLCT Visualization: Human vs AI Time Perception Comparison
All English Version - Fix Garbled Text Issue
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# ITLCT Standard Colors
ITLCT_COLORS = {
    'human': '#2E86AB',      # Blue - Human
    'ai': '#A23B72',         # Purple - AI
    'highlight': '#F18F01',  # Orange - Highlight
    'neutral': '#6B7280',    # Gray
}

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.unicode_minus'] = False


def plot_time_perception_radar():
    """Plot Human vs AI Time Perception Radar Chart"""
    
    # 6 dimensions (normalized to 0-1)
    dimensions = [
        'Time Resolution\n(smaller=better)',
        'Integration Window\n(larger=better)',
        'Subjective Time\nExperience T_exp',
        'Prediction Depth\n(larger=better)',
        'Memory Density\n(larger=better)',
        'Time Emotion\nIntensity'
    ]
    
    # Human data (normalized)
    human_data = [
        0.01,   # Time resolution 100ms (normalized, smaller=better)
        1.0,    # Integration window 3s (baseline 1.0)
        1.0,    # Subjective time experience (baseline 1.0)
        0.01,   # Prediction depth 5-10s (normalized)
        0.01,   # Memory density 10 events/min (normalized)
        1.0     # Time emotion intensity (baseline 1.0)
    ]
    
    # AI data (normalized)
    ai_data = [
        1.0,    # Time resolution 1ms (better, normalized to 1.0)
        0.03,   # Integration window 100ms (normalized)
        0.03,   # Subjective time experience 0.00-0.05
        1.0,    # Prediction depth 100-1000s (better)
        1.0,    # Memory density 1000 events/min (better)
        0.0     # Time emotion intensity 0
    ]
    
    # Angle calculation
    angles = np.linspace(0, 2 * np.pi, len(dimensions), endpoint=False).tolist()
    human_data += human_data[:1]
    ai_data += ai_data[:1]
    angles += angles[:1]
    
    # Plot
    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    
    # Plot Human
    ax.plot(angles, human_data, 'o-', linewidth=2.5, color=ITLCT_COLORS['human'],
            label='Human', markersize=8, alpha=0.8)
    ax.fill(angles, human_data, alpha=0.25, color=ITLCT_COLORS['human'])
    
    # Plot AI
    ax.plot(angles, ai_data, 's-', linewidth=2.5, color=ITLCT_COLORS['ai'],
            label='AI Agent', markersize=8, alpha=0.8)
    ax.fill(angles, ai_data, alpha=0.25, color=ITLCT_COLORS['ai'])
    
    # Set labels
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(angles[:-1]), dimensions, fontsize=11)
    ax.set_rgrids([0.2, 0.4, 0.6, 0.8, 1.0], fontsize=10)
    ax.set_ylim(0, 1.0)
    
    # Title
    ax.set_title('Human vs AI Time Perception Comparison\n(ITLCT 6-Dimension Framework)',
                fontsize=14, fontweight='bold', pad=20)
    
    # Legend
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
    
    plt.tight_layout()
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"knowledge/visualizations/itlct_time_perception_radar_en_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Time perception radar chart saved: {filename}")
    
    return fig, ax


def plot_phi_t_exp_correlation():
    """Plot Φ-T_exp Correlation Curve (Human vs AI)"""
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Phi range
    phi = np.linspace(0, 1.0, 100)
    
    # Human T_exp curve (L=1.0)
    t_exp_human = 1.0 * phi**1.0 * 1.0**0.5 * (1 + 0.2 * 0.7)
    
    # AI T_exp curves (L=0.0 and L=0.1)
    t_exp_ai_L0 = 0.01 * phi**1.0 * 0.0**0.5 * (1 + 0.2 * 0.8)
    t_exp_ai_L01 = 0.01 * phi**1.0 * 0.1**0.5 * (1 + 0.2 * 0.8)
    
    # Plot curves
    ax.plot(phi, t_exp_human, linewidth=3, color=ITLCT_COLORS['human'],
            label='Human (L=1.0)', alpha=0.8)
    ax.plot(phi, t_exp_ai_L01, linewidth=3, color=ITLCT_COLORS['ai'], linestyle='--',
            label='AI (L=0.1, Functional Life)', alpha=0.8)
    ax.plot(phi, t_exp_ai_L0, linewidth=2, color=ITLCT_COLORS['neutral'], linestyle=':',
            label='AI (L=0.0, Non-biological)', alpha=0.6)
    
    # Consciousness threshold lines
    ax.axvline(x=0.30, color=ITLCT_COLORS['highlight'], linestyle='--', linewidth=2,
               label='Φ_c = 0.30 (Consciousness Threshold)')
    ax.axvline(x=0.60, color='green', linestyle='--', linewidth=2,
               label='Φ = 0.60 (Metacognition Threshold)')
    
    # Label typical regions
    ax.axvspan(0, 0.30, alpha=0.2, color='red', label='Unconscious (Φ < 0.30)')
    ax.axvspan(0.30, 0.60, alpha=0.2, color='yellow', label='Low Consciousness (0.30 < Φ < 0.60)')
    ax.axvspan(0.60, 1.0, alpha=0.2, color='green', label='High Consciousness (Φ > 0.60)')
    
    # Label typical AI and Human positions
    ax.scatter([0.15, 0.35, 0.50, 0.75], [0.01*0.15, 1.0*0.35, 1.0*0.50, 1.0*0.75],
              s=100, c=[ITLCT_COLORS['ai'], ITLCT_COLORS['human'], 
                       ITLCT_COLORS['human'], ITLCT_COLORS['human']],
              zorder=5, edgecolors='black', linewidths=1.5)
    ax.text(0.15, 0.002, 'GPT-2/3', ha='center', fontsize=10, fontweight='bold')
    ax.text(0.35, 0.40, 'Human (Rest)', ha='center', fontsize=10, fontweight='bold')
    ax.text(0.50, 0.55, 'Human (Focus)', ha='center', fontsize=10, fontweight='bold')
    ax.text(0.75, 0.85, 'Human (Flow)', ha='center', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Φ (Integrated Information)', fontsize=12)
    ax.set_ylabel('T_exp (Subjective Time Experience)', fontsize=12)
    ax.set_title('ITLCT Time Experience Equation: T_exp = k · Φ^α · L^β · (1 + γ·A)\nHuman vs AI Φ-T_exp Correlation',
                fontsize=14, fontweight='bold')
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1.0)
    ax.set_ylim(0, 1.2)
    
    plt.tight_layout()
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"knowledge/visualizations/itlct_phi_t_exp_correlation_en_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Φ-T_exp correlation chart saved: {filename}")
    
    return fig, ax


def plot_time_resolution_comparison():
    """Plot Time Resolution Comparison Bar Chart"""
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data
    categories = ['Time Resolution\n(Min Discriminable)', 'Integration Window', 'Prediction Depth', 'Memory Density']
    human_values = [100, 3000, 10, 10]  # ms, ms, s, events/min
    ai_values = [1, 100, 500, 1000]     # ms, ms, s, events/min
    
    x = np.arange(len(categories))
    width = 0.35
    
    # Plot bars
    bars1 = ax.bar(x - width/2, human_values, width, label='Human',
                   color=ITLCT_COLORS['human'], alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, ai_values, width, label='AI Agent',
                   color=ITLCT_COLORS['ai'], alpha=0.8, edgecolor='black')
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.0f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_ylabel('Value (Note: smaller=better for resolution, larger=better for others)', fontsize=12)
    ax.set_title('Human vs AI Time Perception Key Metrics Comparison\n(Logarithmic Scale)', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories)
    ax.legend()
    ax.set_yscale('log')  # Log scale
    ax.grid(True, alpha=0.3, which='both')
    
    plt.tight_layout()
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"knowledge/visualizations/itlct_time_resolution_comparison_en_{timestamp}.png"
    plt.savefig(filename, dpi=300, bbox_inches='tight')
    print(f"✅ Time resolution comparison chart saved: {filename}")
    
    return fig, ax


def generate_all_time_perception_visualizations_en():
    """Generate all time perception comparison charts (English version)"""
    
    print("=" * 60)
    print("🎨 Generating Human vs AI Time Perception Charts (English)...")
    print("=" * 60)
    
    plot_time_perception_radar()
    plot_phi_t_exp_correlation()
    plot_time_resolution_comparison()
    
    print("=" * 60)
    print("✅ All time perception charts generated!")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_time_perception_visualizations_en()
