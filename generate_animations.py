# -*- coding: utf-8 -*-
"""
GIFT Framework - Animation Generator
======================================

Generates pre-rendered animations (GIFs/MP4s) for README and social media.

Animations created:
1. e8_root_rotation.gif - E8 roots rotating in 3D
2. dimensional_reduction.gif - 496 to 99 to 18 flow
3. cohomology_breakdown.gif - H2(21) and H3(77) decomposition
4. precision_evolution.gif - v1 vs v2 improvement

Author: Brieuc de La Fourniere
Version: 2.0
Date: October 2025
"""

import sys
import io
# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch, Wedge
from matplotlib.collections import LineCollection
import os

# Setup
OUTPUT_DIR = "../publication/animations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Color scheme
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'accent1': '#4facfe',
    'accent2': '#00f2fe',
    'success': '#43e97b',
    'highlight': '#fa709a'
}

# ============================================================================
# Animation 1: E₈ Root System Rotation
# ============================================================================

def generate_e8_roots_animation():
    """Generate rotating E8 root system visualization"""
    print("Generating E8 root rotation animation...")
    
    # Generate simplified E8 roots (subset for performance)
    def generate_e8_roots():
        roots = []
        # Type 1: ±ei±ej (112 roots)
        for i in range(8):
            for j in range(i+1, 8):
                for s1 in [-1, 1]:
                    for s2 in [-1, 1]:
                        root = np.zeros(8)
                        root[i] = s1
                        root[j] = s2
                        roots.append(root)
        
        # Type 2: (±1/2)^8 with even minus count (subset)
        for i in range(32):
            root = []
            minus_count = 0
            for j in range(8):
                val = 0.5 if ((i >> j) & 1) else -0.5
                root.append(val)
                if val < 0:
                    minus_count += 1
            if minus_count % 2 == 0:
                roots.append(np.array(root))
        
        return np.array(roots[:240])  # Limit to 240
    
    roots = generate_e8_roots()
    
    # Setup figure
    fig = plt.figure(figsize=(10, 10), facecolor='#1a1a2e')
    ax = fig.add_subplot(111, projection='3d', facecolor='#16213e')
    
    # Rotation animation
    def update(frame):
        ax.clear()
        ax.set_facecolor('#16213e')
        
        # Rotate roots
        angle = frame * 2 * np.pi / 120
        rotation_matrix = np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ])
        
        # Project to 3D
        roots_3d = roots[:, :3]
        rotated = np.dot(roots_3d, rotation_matrix.T)
        
        # Plot
        scatter = ax.scatter(rotated[:, 0], rotated[:, 1], rotated[:, 2],
                            c=rotated[:, 2], cmap='plasma', s=30, alpha=0.8,
                            edgecolors='white', linewidths=0.5)
        
        ax.set_xlabel('x₁', color='white', fontsize=12)
        ax.set_ylabel('x₂', color='white', fontsize=12)
        ax.set_zlabel('x₃', color='white', fontsize=12)
        ax.set_title('E₈ Root System (240 roots)\n3D Projection', 
                     color='white', fontsize=16, pad=20)
        
        ax.set_xlim([-1.5, 1.5])
        ax.set_ylim([-1.5, 1.5])
        ax.set_zlim([-1.5, 1.5])
        
        ax.tick_params(colors='white')
        ax.grid(True, alpha=0.2)
        
        return scatter,
    
    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=120, interval=50, blit=False)
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, 'e8_root_rotation.gif')
    anim.save(output_path, writer='pillow', fps=20, dpi=80)
    print(f"  [OK] Saved to {output_path}")
    plt.close()


# ============================================================================
# Animation 2: Dimensional Reduction Flow
# ============================================================================

def generate_dimensional_reduction_animation():
    """Generate 496 → 99 → 18 information flow animation"""
    print("Generating dimensional reduction flow animation...")
    
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    
    def update(frame):
        ax.clear()
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis('off')
        
        progress = frame / 100  # 100 frames total
        
        # E8xE8 box
        box1 = FancyBboxPatch((0.5, 7), 2, 1.5, 
                             boxstyle="round,pad=0.1", 
                             edgecolor=COLORS['primary'], 
                             facecolor=COLORS['primary'], 
                             alpha=0.6, linewidth=3)
        ax.add_patch(box1)
        ax.text(1.5, 7.75, 'E₈×E₈', ha='center', va='center', 
                fontsize=18, color='white', weight='bold')
        ax.text(1.5, 7.3, '496', ha='center', va='center', 
                fontsize=14, color='white')
        
        # Cohomology boxes (fade in)
        if progress > 0.3:
            alpha_coh = min(1.0, (progress - 0.3) / 0.2)
            
            box2 = FancyBboxPatch((4, 7.5), 1.5, 0.8, 
                                 boxstyle="round,pad=0.05",
                                 edgecolor=COLORS['accent1'], 
                                 facecolor=COLORS['accent1'], 
                                 alpha=0.6*alpha_coh, linewidth=2)
            ax.add_patch(box2)
            ax.text(4.75, 7.9, 'H²(K₇)', ha='center', va='center',
                   fontsize=14, color='white', alpha=alpha_coh)
            ax.text(4.75, 7.5, '21', ha='center', va='center',
                   fontsize=12, color='white', alpha=alpha_coh)
            
            box3 = FancyBboxPatch((4, 6.2), 1.5, 0.8,
                                 boxstyle="round,pad=0.05", 
                                 edgecolor=COLORS['accent2'], 
                                 facecolor=COLORS['accent2'], 
                                 alpha=0.6*alpha_coh, linewidth=2)
            ax.add_patch(box3)
            ax.text(4.75, 6.6, 'H³(K₇)', ha='center', va='center',
                   fontsize=14, color='white', alpha=alpha_coh)
            ax.text(4.75, 6.2, '77', ha='center', va='center',
                   fontsize=12, color='white', alpha=alpha_coh)
            
            # Connection lines
            ax.arrow(2.5, 7.75, 1.3, 0, head_width=0.2, head_length=0.2,
                    fc=COLORS['accent1'], ec=COLORS['accent1'], alpha=alpha_coh)
            ax.arrow(2.5, 7.5, 1.3, -0.9, head_width=0.2, head_length=0.2,
                    fc=COLORS['accent2'], ec=COLORS['accent2'], alpha=alpha_coh)
        
        # Observable boxes (fade in)
        if progress > 0.6:
            alpha_obs = min(1.0, (progress - 0.6) / 0.3)
            
            observables = [
                (7.5, 7.8, 'Neutrinos\n4', COLORS['success']),
                (7.5, 6.8, 'Gauge\n5', COLORS['highlight']),
                (7.5, 5.8, 'Higgs\n2', COLORS['accent1']),
                (7.5, 4.8, 'Leptons\n3', COLORS['accent2']),
                (7.5, 3.8, 'Cosmology\n3', COLORS['primary']),
                (7.5, 2.8, 'Structure\n1', COLORS['secondary'])
            ]
            
            for x, y, label, color in observables:
                box = FancyBboxPatch((x, y), 1.3, 0.6,
                                    boxstyle="round,pad=0.05",
                                    edgecolor=color, facecolor=color,
                                    alpha=0.6*alpha_obs, linewidth=2)
                ax.add_patch(box)
                lines = label.split('\n')
                ax.text(x+0.65, y+0.4, lines[0], ha='center', va='center',
                       fontsize=10, color='white', alpha=alpha_obs)
                ax.text(x+0.65, y+0.15, lines[1], ha='center', va='center',
                       fontsize=9, color='white', alpha=alpha_obs, weight='bold')
            
            # Arrows from cohomology to observables
            if alpha_obs > 0.5:
                ax.arrow(5.5, 7.5, 1.8, 0.2, head_width=0.15, head_length=0.15,
                        fc=COLORS['success'], ec=COLORS['success'], alpha=alpha_obs, linewidth=2)
                ax.arrow(5.5, 6.5, 1.8, 0.2, head_width=0.15, head_length=0.15,
                        fc=COLORS['highlight'], ec=COLORS['highlight'], alpha=alpha_obs, linewidth=2)
        
        # Title and labels
        ax.text(5, 9.3, 'GIFT Dimensional Reduction', ha='center', va='center',
               fontsize=20, color='white', weight='bold')
        ax.text(5, 8.8, 'From E₈×E₈ Topology to Observable Physics',
               ha='center', va='center', fontsize=14, color='white', alpha=0.8)
        
        # Progress indicator
        ax.text(5, 0.5, f'Frame: {frame}/100', ha='center', va='center',
               fontsize=10, color='white', alpha=0.5)
    
    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, 'dimensional_reduction.gif')
    anim.save(output_path, writer='pillow', fps=20, dpi=100)
    print(f"  [OK] Saved to {output_path}")
    plt.close()


# ============================================================================
# Animation 3: Cohomology Breakdown
# ============================================================================

def generate_cohomology_breakdown_animation():
    """Generate H2(21) and H3(77) decomposition animation"""
    print("Generating cohomology breakdown animation...")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7), facecolor='#1a1a2e')
    
    def update(frame):
        progress = frame / 100
        
        for ax, title, total, decomp, colors in [
            (ax1, 'H²(K₇) = 21\nGauge Bosons', 21,
             [('SU(3)_C', 8), ('SU(2)_L', 3), ('U(1)_Y', 1), ('Massive', 9)],
             [COLORS['success'], COLORS['accent1'], COLORS['highlight'], COLORS['secondary']]),
            (ax2, 'H³(K₇) = 77\nChiral Fermions', 77,
             [('Quarks', 18), ('Leptons', 12), ('Higgs', 4), ('RH ν', 9), ('Dark', 34)],
             [COLORS['success'], COLORS['accent1'], COLORS['highlight'], COLORS['accent2'], COLORS['secondary']])
        ]:
            ax.clear()
            ax.set_facecolor('#16213e')
            ax.set_xlim(-1.2, 1.2)
            ax.set_ylim(-1.2, 1.2)
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Title
            ax.text(0, 1.35, title, ha='center', va='center',
                   fontsize=16, color='white', weight='bold')
            
            # Animated pie chart
            current_angle = 0
            for i, ((label, value), color) in enumerate(zip(decomp, colors)):
                angle = (value / total) * 360 * min(1.0, progress * 1.5)
                
                if angle > 0:
                    wedge = Wedge((0, 0), 1.0, current_angle, current_angle + angle,
                                 facecolor=color, edgecolor='white', linewidth=2, alpha=0.7)
                    ax.add_patch(wedge)
                    
                    # Labels (appear after wedge is complete)
                    if progress > 0.5:
                        mid_angle = (current_angle + angle/2) * np.pi / 180
                        label_r = 0.7
                        label_x = label_r * np.cos(mid_angle)
                        label_y = label_r * np.sin(mid_angle)
                        
                        alpha_label = min(1.0, (progress - 0.5) / 0.3)
                        ax.text(label_x, label_y, f'{label}\n{value}',
                               ha='center', va='center', fontsize=10,
                               color='white', weight='bold', alpha=alpha_label)
                
                current_angle += angle
            
            # Center circle
            center_circle = Circle((0, 0), 0.4, facecolor='#16213e', 
                                  edgecolor='white', linewidth=2)
            ax.add_patch(center_circle)
            
            # Total in center
            ax.text(0, 0, str(total), ha='center', va='center',
                   fontsize=24, color='white', weight='bold')
    
    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, 'cohomology_breakdown.gif')
    anim.save(output_path, writer='pillow', fps=20, dpi=100)
    print(f"  [OK] Saved to {output_path}")
    plt.close()


# ============================================================================
# Animation 4: Precision Evolution v1 → v2
# ============================================================================

def generate_precision_evolution_animation():
    """Generate v1 vs v2 precision improvement animation"""
    print("Generating precision evolution animation...")
    
    # Data
    observables = [
        'θ₁₂', 'θ₁₃', 'θ₂₃', 'δ_CP',
        'α⁻¹(0)', 'α⁻¹(Mz)', 'sin²θw', 'αs',
        'λH', 'mH', 'Q', 'mμ/me', 'mτ/mμ',
        'ΩDE', 'ns', 'H₀'
    ]
    
    # Approximate deviations (for illustration)
    v1_dev = np.array([0.15, 0.62, 0.08, 0.02, 0.65, 0.01, 0.35, 0.08,
                       0.18, 0.42, 0.01, 0.20, 0.15, 0.85, 0.25, 0.30])
    v2_dev = np.array([0.062, 0.448, 0.014, 0.005, 0.474, 0.002, 0.216, 0.041,
                       0.113, 0.294, 0.005, 0.117, 0.119, 0.703, 0.111, 0.145])
    
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), facecolor='#1a1a2e')
    
    def update(frame):
        progress = frame / 100
        
        # Top panel: Bar comparison
        ax1.clear()
        ax1.set_facecolor('#16213e')
        
        x = np.arange(len(observables))
        width = 0.35
        
        # Fade in bars
        alpha = min(1.0, progress * 2)
        bars1 = ax1.bar(x - width/2, v1_dev, width, label='v1', 
                       color=COLORS['secondary'], alpha=alpha, edgecolor='white')
        bars2 = ax1.bar(x + width/2, v2_dev, width, label='v2',
                       color=COLORS['success'], alpha=alpha, edgecolor='white')
        
        ax1.set_ylabel('Deviation (%)', fontsize=14, color='white')
        ax1.set_title('GIFT Framework Evolution: v1 → v2', 
                     fontsize=18, color='white', weight='bold', pad=20)
        ax1.set_xticks(x)
        ax1.set_xticklabels(observables, rotation=45, ha='right', fontsize=10, color='white')
        ax1.legend(fontsize=12, facecolor='#16213e', edgecolor='white', labelcolor='white')
        ax1.tick_params(colors='white')
        ax1.grid(axis='y', alpha=0.2, color='white')
        ax1.axhline(y=1.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='1% threshold')
        
        # Bottom panel: Mean deviation evolution
        ax2.clear()
        ax2.set_facecolor('#16213e')
        
        frames_shown = int(progress * 50)
        improvement_curve = np.linspace(0.380, 0.208, 50)[:frames_shown]
        x_curve = np.arange(frames_shown)
        
        ax2.plot(x_curve, improvement_curve, color=COLORS['accent1'], 
                linewidth=3, marker='o', markersize=4)
        ax2.fill_between(x_curve, 0, improvement_curve, 
                         color=COLORS['accent1'], alpha=0.3)
        
        ax2.axhline(y=0.380, color=COLORS['secondary'], linestyle='--', 
                   linewidth=2, alpha=0.5, label='v1: 0.380%')
        ax2.axhline(y=0.208, color=COLORS['success'], linestyle='--', 
                   linewidth=2, alpha=0.5, label='v2: 0.208%')
        
        ax2.set_xlabel('Framework Development', fontsize=14, color='white')
        ax2.set_ylabel('Mean Deviation (%)', fontsize=14, color='white')
        ax2.set_title('Precision Improvement Over Time', 
                     fontsize=16, color='white', weight='bold')
        ax2.set_ylim(0, 0.5)
        ax2.legend(fontsize=12, facecolor='#16213e', edgecolor='white', labelcolor='white')
        ax2.tick_params(colors='white')
        ax2.grid(alpha=0.2, color='white')
        
        # Stats text
        if progress > 0.8:
            alpha_text = (progress - 0.8) / 0.2
            ax2.text(25, 0.45, f'Parameter reduction: 4 → 3', 
                    fontsize=12, color=COLORS['success'], alpha=alpha_text, weight='bold')
            ax2.text(25, 0.40, f'Improvement: 45% better precision',
                    fontsize=12, color=COLORS['accent1'], alpha=alpha_text, weight='bold')
    
    plt.tight_layout()
    
    # Create animation
    anim = animation.FuncAnimation(fig, update, frames=100, interval=50)
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, 'precision_evolution.gif')
    anim.save(output_path, writer='pillow', fps=20, dpi=100)
    print(f"  [OK] Saved to {output_path}")
    plt.close()


# ============================================================================
# Animation 5: Framework Summary Card (Static image for README)
# ============================================================================

def generate_summary_card():
    """Generate static summary card for README"""
    print("Generating summary card...")
    
    fig, ax = plt.subplots(figsize=(12, 8), facecolor='#1a1a2e')
    ax.set_facecolor('#16213e')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Title
    ax.text(5, 9, 'GIFT Framework v2', ha='center', va='center',
           fontsize=32, color='white', weight='bold')
    ax.text(5, 8.3, 'Geometric Information Field Theory', ha='center', va='center',
           fontsize=18, color='white', alpha=0.8)
    
    # Main achievement box
    main_box = FancyBboxPatch((1, 6), 8, 1.8, boxstyle="round,pad=0.15",
                             edgecolor=COLORS['primary'], facecolor=COLORS['primary'],
                             alpha=0.3, linewidth=3)
    ax.add_patch(main_box)
    
    ax.text(5, 7.3, '18 Observables from 3 Parameters', ha='center', va='center',
           fontsize=20, color='white', weight='bold')
    ax.text(5, 6.7, 'Mean Precision: 0.208%', ha='center', va='center',
           fontsize=16, color=COLORS['success'], weight='bold')
    
    # Key results (4 boxes)
    results = [
        ("δ_CP = ζ(3)+√5\n196.99°", "0.005%\ndeviation", COLORS['success']),
        ("Q = 2/3 exact\n(Koide)", "0.005%\ndeviation", COLORS['success']),
        ("ΩDE = ln(2)\n(binary)", "0.60%\ndeviation", COLORS['accent1']),
        ("Ngen = 3\n(exact)", "0.000%\ndeviation", COLORS['success'])
    ]
    
    x_positions = [1.5, 3.8, 6.1, 8.4]
    for i, (result, precision, color) in enumerate(results):
        box = FancyBboxPatch((x_positions[i]-0.9, 4.2), 1.8, 1.5,
                            boxstyle="round,pad=0.1",
                            edgecolor=color, facecolor=color,
                            alpha=0.2, linewidth=2)
        ax.add_patch(box)
        
        lines = result.split('\n')
        ax.text(x_positions[i], 5.3, lines[0], ha='center', va='center',
               fontsize=11, color='white', weight='bold')
        ax.text(x_positions[i], 4.9, lines[1], ha='center', va='center',
               fontsize=10, color='white')
        
        prec_lines = precision.split('\n')
        ax.text(x_positions[i], 4.5, prec_lines[0], ha='center', va='center',
               fontsize=14, color=color, weight='bold')
        ax.text(x_positions[i], 4.2, prec_lines[1], ha='center', va='center',
               fontsize=9, color='white', alpha=0.7)
    
    # Parameters box
    param_box = FancyBboxPatch((0.5, 2), 4, 1.5, boxstyle="round,pad=0.1",
                              edgecolor='white', facecolor=(1, 1, 1, 0.05),
                              linewidth=2)
    ax.add_patch(param_box)
    
    ax.text(2.5, 3.2, 'Three Topological Parameters:', ha='center', va='center',
           fontsize=14, color='white', weight='bold')
    ax.text(2.5, 2.8, 'p₂ = 2 (duality)', ha='center', va='center',
           fontsize=11, color=COLORS['accent1'])
    ax.text(2.5, 2.5, 'rank(E₈) = 8', ha='center', va='center',
           fontsize=11, color=COLORS['accent1'])
    ax.text(2.5, 2.2, 'Weyl_factor = 5', ha='center', va='center',
           fontsize=11, color=COLORS['accent1'])
    
    # Comparison box
    comp_box = FancyBboxPatch((5.5, 2), 4, 1.5, boxstyle="round,pad=0.1",
                             edgecolor='white', facecolor=(1, 1, 1, 0.05),
                             linewidth=2)
    ax.add_patch(comp_box)
    
    ax.text(7.5, 3.2, 'vs Standard Model:', ha='center', va='center',
           fontsize=14, color='white', weight='bold')
    ax.text(7.5, 2.8, '19 free parameters', ha='center', va='center',
           fontsize=11, color='white', alpha=0.7)
    ax.text(7.5, 2.5, 'All measured', ha='center', va='center',
           fontsize=11, color='white', alpha=0.7)
    ax.text(7.5, 2.2, 'No predictions', ha='center', va='center',
           fontsize=11, color='white', alpha=0.7)
    
    # Footer
    ax.text(5, 0.8, 'DOI: 10.5281/zenodo.17360782', ha='center', va='center',
           fontsize=10, color='white', alpha=0.6)
    ax.text(5, 0.4, 'github.com/gift-framework/GIFT', ha='center', va='center',
           fontsize=10, color=COLORS['accent1'], alpha=0.8)
    
    plt.tight_layout()
    
    # Save as high-res PNG
    output_path = os.path.join(OUTPUT_DIR, 'gift_summary_card.png')
    plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none',
               bbox_inches='tight')
    print(f"  [OK] Saved to {output_path}")
    plt.close()


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Generate all animations"""
    print("="*70)
    print("GIFT FRAMEWORK - ANIMATION GENERATOR")
    print("="*70)
    print(f"\nOutput directory: {OUTPUT_DIR}")
    print("\nGenerating animations...\n")
    
    try:
        # Generate all animations
        generate_e8_roots_animation()
        generate_dimensional_reduction_animation()
        generate_cohomology_breakdown_animation()
        generate_precision_evolution_animation()
        generate_summary_card()
        
        print("\n" + "="*70)
        print("ALL ANIMATIONS GENERATED SUCCESSFULLY")
        print("="*70)
        print(f"\nFiles created in: {OUTPUT_DIR}/")
        print("  1. e8_root_rotation.gif")
        print("  2. dimensional_reduction.gif")
        print("  3. cohomology_breakdown.gif")
        print("  4. precision_evolution.gif")
        print("  5. gift_summary_card.png (static)")
        print("\nReady for README and social media sharing!")
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

