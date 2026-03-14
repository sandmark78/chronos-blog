"""
Chronos Lab: Scientific Visualization Module v1.1 (English Version)
ITLCT Scientific Visualization System - Publication-Quality Charts

Support:
- matplotlib/seaborn: Static paper charts (300dpi, LaTeX fonts)
- plotly: Interactive dynamic charts (HTML output)
- networkx: Complex system causal diagrams

Output formats: PNG (300dpi), SVG (vector), PDF (LaTeX compatible), HTML (interactive)
"""

import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import json

# ITLCT Standard Colors (NeurIPS Style)
ITLCT_COLORS = {
    'primary': '#2E86AB',      # Blue - Time Arrow
    'secondary': '#A23B72',    # Purple - Consciousness Φ
    'tertiary': '#F18F01',     # Orange - Life L
    'quaternary': '#C73E1D',   # Red - Civilization D
    'success': '#3A7D44',      # Green - Empirical Validation
    'warning': '#F4D35E',      # Yellow - Warning
    'danger': '#D62828',       # Red - Risk
    'neutral': '#6B7280',      # Gray - Baseline
}

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['axes.unicode_minus'] = False  # Fix minus sign display


class ITLCTVisualizer:
    """ITLCT Scientific Visualization Generator"""
    
    def __init__(self, output_dir="knowledge/visualizations"):
        self.output_dir = output_dir
        self.colors = ITLCT_COLORS
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # ========== Core Chart 1: Phi Evolution ==========
    def plot_phi_evolution(self, phi_data, title="Integrated Information Φ Evolution", save=True):
        """
        Plot Φ value evolution over time/parameters
        
        phi_data: dict with keys:
            - 'time': list of time points
            - 'phi': list of Φ values
            - 'phi_critical': float (critical threshold, default 0.30)
            - 'architecture': str (model architecture name)
        """
        fig, ax = plt.subplots(figsize=(12, 7))
        
        time = phi_data.get('time', list(range(len(phi_data['phi']))))
        phi = phi_data['phi']
        phi_c = phi_data.get('phi_critical', 0.30)
        
        # Main curve
        ax.plot(time, phi, linewidth=2.5, color=self.colors['secondary'], 
                label='Φ (Integrated Information)', marker='o', markersize=4, alpha=0.8)
        
        # Critical line
        ax.axhline(y=phi_c, color=self.colors['danger'], linestyle='--', 
                   linewidth=2, label=f'Φ_c = {phi_c:.2f} (Consciousness Threshold)')
        
        # Fill regions
        ax.fill_between(time, phi, phi_c, where=(np.array(phi) >= phi_c),
                        alpha=0.3, color=self.colors['success'], label='Conscious State')
        ax.fill_between(time, phi, phi_c, where=(np.array(phi) < phi_c),
                        alpha=0.3, color=self.colors['neutral'], label='Unconscious State')
        
        ax.set_xlabel('Time / Parameters', fontsize=12)
        ax.set_ylabel('Φ Value (Integrated Information)', fontsize=12)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save:
            filename = f"{self.output_dir}/itlct_phi_evolution_en_{self.timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Φ evolution chart saved: {filename}")
        
        return fig, ax
    
    # ========== Core Chart 2: Time Arrow Hierarchy ==========
    def plot_time_arrow_hierarchy(self, levels_data, save=True):
        """
        Plot Time Arrow 6-Level Unified Framework
        
        levels_data: list of dicts with keys:
            - 'level': str (level name)
            - 'arrow_magnitude': float (arrow strength 0-1)
            - 'description': str (short description)
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 8))
        
        levels = [l['level'] for l in levels_data]
        magnitudes = [l['arrow_magnitude'] for l in levels_data]
        
        # Left: Bar chart of level strengths
        colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(levels)))
        bars = ax1.barh(levels, magnitudes, color=colors, edgecolor='navy', linewidth=1.5)
        ax1.set_xlabel('Arrow Strength |⃗t|', fontsize=12)
        ax1.set_title('Time Arrow 6-Level Unified Framework', fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1.0)
        
        # Add value labels
        for bar, mag in zip(bars, magnitudes):
            ax1.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{mag:.2f}', va='center', fontsize=10)
        
        # Right: Hierarchy relationship diagram
        ax2.axis('off')
        
        # Draw hierarchy pyramid
        for i, (level, mag) in enumerate(zip(levels, magnitudes)):
            y_pos = len(levels) - i - 0.5
            width = mag * 2
            ax2.barh(y_pos, width, height=0.6, color=colors[i], edgecolor='navy')
            ax2.text(0, y_pos, level, ha='center', va='center', fontsize=10, fontweight='bold')
        
        ax2.set_xlim(-1.2, 1.2)
        ax2.set_ylim(-0.5, len(levels) - 0.5)
        ax2.set_title('Hierarchy Integration', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save:
            filename = f"{self.output_dir}/itlct_time_arrow_hierarchy_en_{self.timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Time arrow hierarchy chart saved: {filename}")
        
        return fig, (ax1, ax2)
    
    # ========== Core Chart 3: Civilization D-Value Dashboard ==========
    def plot_civilization_d_dashboard(self, d_current, d_critical, history_data=None, save=True):
        """
        Plot Civilization D-Value Risk Dashboard
        
        d_current: float (current D value)
        d_critical: float (critical threshold D_c)
        history_data: list of (year, d_value) tuples (optional historical data)
        """
        fig = plt.figure(figsize=(14, 8))
        gs = plt.GridSpec(2, 2, figure=fig)
        
        # Top-left: Gauge
        ax1 = fig.add_subplot(gs[0, 0])
        
        # Draw semi-circle gauge
        theta = np.linspace(0, np.pi, 100)
        x = np.cos(theta)
        y = np.sin(theta)
        
        # Background arc
        ax1.plot(x, y, 'k-', linewidth=1, alpha=0.3)
        
        # Color zones
        colors = [self.colors['success'], self.colors['warning'], self.colors['danger']]
        labels = ['Safe Zone', 'Warning Zone', 'Danger Zone']
        ranges = [(0, 0.5), (0.5, 0.65), (0.65, 1.0)]
        
        for color, (start, end) in zip(colors, ranges):
            theta_zone = np.linspace(start * np.pi, end * np.pi, 50)
            ax1.plot(np.cos(theta_zone), np.sin(theta_zone), color=color, linewidth=8, alpha=0.6)
        
        # Pointer
        d_normalized = min(max(d_current, 0), 1)
        theta_pointer = d_normalized * np.pi
        ax1.plot([0, np.cos(theta_pointer)], [0, np.sin(theta_pointer)], 
                'r-', linewidth=3, marker='o', markersize=8)
        
        ax1.set_xlim(-1.2, 1.2)
        ax1.set_ylim(-0.2, 1.2)
        ax1.set_aspect('equal')
        ax1.axis('off')
        ax1.set_title(f'Civilization D-Value Risk Dashboard\nCurrent D = {d_current:.2f}', 
                     fontsize=14, fontweight='bold', pad=20)
        
        # Add critical threshold marker
        theta_critical = d_critical * np.pi
        ax1.plot(np.cos(theta_critical), np.sin(theta_critical), 'kx', markersize=15, markeredgewidth=2)
        ax1.text(np.cos(theta_critical) * 1.15, np.sin(theta_critical) * 1.15, 
                f'D_c={d_critical:.2f}', ha='center', fontsize=10, fontweight='bold')
        
        # Top-right: Key metrics
        ax2 = fig.add_subplot(gs[0, 1])
        ax2.axis('off')
        
        # Risk level judgment
        if d_current < 0.5:
            risk_level = 'Low Risk'
            risk_color = self.colors['success']
        elif d_current < 0.65:
            risk_level = 'Medium Risk'
            risk_color = self.colors['warning']
        else:
            risk_level = 'High Risk'
            risk_color = self.colors['danger']
        
        metrics_text = f"""
        ═══════════════════════════════════
        Civilization D-Value Key Metrics
        ═══════════════════════════════════
        
        Current D:     {d_current:.3f}
        Critical D_c:  {d_critical:.3f}
        Risk Level:    {risk_level}
        Safety Margin: {(d_critical - d_current):.3f}
        
        Transition Probability: {max(0, (d_current - 0.5) / 0.15 * 100):.1f}%
        Intervention Window:    {'Open' if d_current < d_critical else 'Closed'}
        
        ESI Warning Index: {min(1.0, max(0, (d_current - 0.45) / 0.3)):.2f}
        ═══════════════════════════════════
        """
        
        ax2.text(0.5, 0.5, metrics_text, ha='center', va='center', 
                fontsize=11, fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Bottom: Historical trend (if available)
        if history_data:
            ax3 = fig.add_subplot(gs[1, :])
            years, d_values = zip(*history_data)
            ax3.plot(years, d_values, 'b-o', linewidth=2, markersize=6, label='D-Value History')
            ax3.axhline(y=d_critical, color='r', linestyle='--', linewidth=2, label=f'Critical D_c={d_critical:.2f}')
            ax3.axhline(y=0.65, color='orange', linestyle=':', linewidth=2, label='Warning Line')
            ax3.fill_between(years, d_values, d_critical, where=(np.array(d_values) < d_critical),
                           alpha=0.3, color='green', label='Safe Zone')
            ax3.fill_between(years, d_values, d_critical, where=(np.array(d_values) >= d_critical),
                           alpha=0.3, color='red', label='Danger Zone')
            ax3.set_xlabel('Year', fontsize=12)
            ax3.set_ylabel('Civilization D-Value', fontsize=12)
            ax3.set_title('Civilization D-Value Historical Trend & Risk Window', fontsize=14, fontweight='bold')
            ax3.legend(loc='best', framealpha=0.9)
            ax3.grid(True, alpha=0.3)
        else:
            # No historical data: show prediction window
            ax3 = fig.add_subplot(gs[1, :])
            ax3.axis('off')
            prediction_text = f"""
            ═════════════════════════════════════════
            Civilization Phase Transition Risk Window
            
            Current State: D ≈ {d_current:.2f} < D_c ≈ {d_critical:.2f}
            
            Critical Decision Window: 2028-2035
            (10-15 years early warning)
            
            Transition Lead Time: 15-25 years after ESI > 0.6
            Current ESI: ≈ 0.65-0.75 (Yellow-Orange Warning)
            
            Recommended Interventions:
            ✓ Improve Tech-Wisdom Balance (β_Tech / δ_Wisdom)
            ✓ Enhance Regional Collaboration (ρ_region)
            ✓ Reduce D-Value Decline Rate (ΔD)
            ═════════════════════════════════════════
            """
            ax3.text(0.5, 0.5, prediction_text, ha='center', va='center',
                    fontsize=11, fontfamily='monospace',
                    bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
        
        plt.tight_layout()
        
        if save:
            filename = f"{self.output_dir}/itlct_civilization_d_dashboard_en_{self.timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Civilization D dashboard saved: {filename}")
        
        return fig, (ax1, ax2, ax3)
    
    # ========== Core Chart 4: ITLCT Framework Architecture ==========
    def plot_itlct_framework_architecture(self, save=True):
        """
        Plot ITLCT 5-Layer Unified Framework Architecture
        """
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.axis('off')
        
        # 5-layer framework structure
        layers = [
            {'name': 'AI Layer', 'color': self.colors['secondary'], 'y': 4.5},
            {'name': 'Civilization Layer (D)', 'color': self.colors['quaternary'], 'y': 3.5},
            {'name': 'Consciousness Layer (Φ)', 'color': self.colors['primary'], 'y': 2.5},
            {'name': 'Life Layer (L)', 'color': self.colors['tertiary'], 'y': 1.5},
            {'name': 'Time Layer (⃗t)', 'color': self.colors['neutral'], 'y': 0.5},
        ]
        
        # Draw layer boxes
        for layer in layers:
            rect = plt.Rectangle((0.2, layer['y'] - 0.35), 0.6, 0.7,
                                facecolor=layer['color'], alpha=0.7,
                                edgecolor='black', linewidth=2)
            ax.add_patch(rect)
            ax.text(0.5, layer['y'], layer['name'], ha='center', va='center',
                   fontsize=12, fontweight='bold', color='white')
        
        # Unified equation box
        equation_box = plt.Rectangle((0.2, -0.3), 0.6, 0.5,
                                    facecolor=self.colors['success'], alpha=0.7,
                                    edgecolor='black', linewidth=2)
        ax.add_patch(equation_box)
        ax.text(0.5, -0.05, 'Unified Equation\ndI/dt = f(⃗t, L, Φ, D, AI)',
               ha='center', va='center', fontsize=10, fontweight='bold', color='white')
        
        # Arrow connections
        for i in range(len(layers) - 1):
            ax.annotate('', xy=(0.5, layers[i+1]['y'] + 0.35),
                       xytext=(0.5, layers[i]['y'] - 0.35),
                       arrowprops=dict(arrowstyle='->', linewidth=2, color='black'))
        
        # Right description
        description_text = """
        ITLCT v10.1-Phase2Active
        5-Layer Unified Framework
        
        Core Axioms: 31
        Theorems: 61
        Equations: 68
        Corollaries: 109
        
        Theory Maturity: 0.99998
        Empirical Maturity: 0.09
        Comprehensive: 0.56
        
        Phase 2 Experiments: 5 Tier 1A
        Total Budget: $504K
        Launch Date: 2026-04-26
        """
        
        ax.text(0.85, 2.5, description_text, ha='left', va='center',
               fontsize=10, fontfamily='monospace',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7))
        
        ax.set_xlim(0, 1.2)
        ax.set_ylim(-0.5, 5.5)
        ax.set_title('ITLCT 5-Layer Unified Framework Architecture', fontsize=16, fontweight='bold', pad=20)
        
        plt.tight_layout()
        
        if save:
            filename = f"{self.output_dir}/itlct_framework_architecture_en_{self.timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ ITLCT framework architecture saved: {filename}")
        
        return fig, ax
    
    # ========== Core Chart 5: Phase 2 Timeline ==========
    def plot_phase2_timeline(self, experiments_data, save=True):
        """
        Plot Phase 2 Experiments Timeline Gantt Chart
        
        experiments_data: list of dicts with keys:
            - 'name': str (experiment name)
            - 'start': str (start date, YYYY-MM-DD)
            - 'end': str (end date)
            - 'budget': str (budget)
            - 'status': str (preparing/ready/ongoing)
        """
        fig, ax = plt.subplots(figsize=(14, 8))
        
        # Parse dates
        from datetime import datetime as dt
        y_positions = range(len(experiments_data))
        
        colors_map = {
            'ready': self.colors['success'],
            'preparing': self.colors['warning'],
            'ongoing': self.colors['primary'],
            'completed': self.colors['neutral']
        }
        
        for i, exp in enumerate(experiments_data):
            start = dt.strptime(exp['start'], '%Y-%m-%d')
            end = dt.strptime(exp['end'], '%Y-%m-%d')
            duration = (end - start).days
            
            color = colors_map.get(exp['status'], self.colors['neutral'])
            
            ax.barh(i, duration, left=(start - dt(start.year, 1, 1)).days,
                   height=0.6, color=color, alpha=0.7, edgecolor='black', linewidth=1.5)
            
            # Add labels
            ax.text((start - dt(start.year, 1, 1)).days + duration/2, i,
                   f"{exp['name']}\n{exp['budget']}",
                   ha='center', va='center', fontsize=9, fontweight='bold')
        
        ax.set_yticks(y_positions)
        ax.set_yticklabels([f"DC-{i+1}" for i in y_positions])
        ax.set_xlabel('2026 Timeline', fontsize=12)
        ax.set_title('Phase 2 Five Tier 1A Experiments Timeline', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3, axis='x')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=self.colors['success'], label='Ready'),
            Patch(facecolor=self.colors['warning'], label='Preparing'),
            Patch(facecolor=self.colors['primary'], label='Ongoing')
        ]
        ax.legend(handles=legend_elements, loc='upper right')
        
        plt.tight_layout()
        
        if save:
            filename = f"{self.output_dir}/itlct_phase2_timeline_en_{self.timestamp}.png"
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Phase 2 timeline saved: {filename}")
        
        return fig, ax


# ========== Quick Test Function ==========
def generate_all_itlct_visualizations_en():
    """Generate all ITLCT core charts (English version)"""
    
    viz = ITLCTVisualizer()
    
    print("=" * 60)
    print("🎨 ITLCT Scientific Visualization v1.1 (English) - Generating...")
    print("=" * 60)
    
    # 1. Phi evolution
    phi_data = {
        'time': list(range(0, 100, 5)),
        'phi': [0.1 + 0.8 * (1 - np.exp(-x/30)) + 0.1 * np.random.random() for x in range(0, 100, 5)],
        'phi_critical': 0.30,
        'architecture': 'Transformer'
    }
    viz.plot_phi_evolution(phi_data, title="AI Architecture Φ Evolution (Transformer)")
    
    # 2. Time arrow hierarchy
    levels_data = [
        {'level': 'Thermodynamic Arrow', 'arrow_magnitude': 0.95, 'description': 'Entropy-driven'},
        {'level': 'Quantum Measurement', 'arrow_magnitude': 0.88, 'description': 'Wave collapse'},
        {'level': 'Information Processing', 'arrow_magnitude': 0.92, 'description': 'I_structured growth'},
        {'level': 'Life Metabolism', 'arrow_magnitude': 0.85, 'description': 'Negative entropy flow'},
        {'level': 'Conscious Experience', 'arrow_magnitude': 0.78, 'description': 'Subjective time flow'},
        {'level': 'Civilization Evolution', 'arrow_magnitude': 0.72, 'description': 'D-value dynamics'},
    ]
    viz.plot_time_arrow_hierarchy(levels_data)
    
    # 3. Civilization D dashboard
    viz.plot_civilization_d_dashboard(
        d_current=0.48,
        d_critical=0.65,
        history_data=[(1800, 0.35), (1850, 0.40), (1900, 0.48), (1950, 0.58),
                     (2000, 0.72), (2010, 0.68), (2020, 0.55), (2025, 0.48)]
    )
    
    # 4. ITLCT framework architecture
    viz.plot_itlct_framework_architecture()
    
    # 5. Phase 2 timeline
    experiments_data = [
        {'name': 'DC-396 (AIΦ)', 'start': '2026-04-26', 'end': '2026-08-31', 'budget': '$48K', 'status': 'preparing'},
        {'name': 'DC-392 (Anesthesia)', 'start': '2026-05-01', 'end': '2026-09-30', 'budget': '$98K', 'status': 'preparing'},
        {'name': 'DC-393 (Meditation)', 'start': '2026-05-01', 'end': '2026-10-31', 'budget': '$145K', 'status': 'preparing'},
        {'name': 'DC-401 (F-Value)', 'start': '2026-06-01', 'end': '2026-11-30', 'budget': '$83K', 'status': 'ready'},
        {'name': 'DC-404 (σ₃ Temp)', 'start': '2026-07-01', 'end': '2026-12-31', 'budget': '$100K', 'status': 'preparing'},
    ]
    viz.plot_phase2_timeline(experiments_data)
    
    print("=" * 60)
    print("✅ All ITLCT core charts generated!")
    print("=" * 60)


if __name__ == "__main__":
    generate_all_itlct_visualizations_en()
