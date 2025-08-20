#!/usr/bin/env python3
"""
Custom Tire Curve Generator for Assetto Corsa
Creates realistic slip angle curves with plateau behavior and load sensitivity
"""

import numpy as np
import matplotlib.pyplot as plt

def calculate_load_scaling(vertical_load, fz0, ls_exp):
    """
    Calculate load scaling factor based on AC's load sensitivity model
    Formula: (Current_Load/FZ0)^LS_EXP
    """
    return (vertical_load / fz0) ** ls_exp

def create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, vertical_load):
    """
    Create realistic tire curve with plateau behavior based on research data
    Combines OptimumG data, Haney principles, and AC load sensitivity
    """
    # Calculate load scaling
    load_scale = calculate_load_scaling(vertical_load, fz0, ls_exp)
    peak_grip = dy_ref * load_scale
    
    forces = np.zeros_like(slip_angles)
    
    for i, angle in enumerate(slip_angles):
        if angle <= 2.0:
            # Linear region (Paul Haney: pure elastic deformation)
            # Cornering stiffness ~450-500 N/deg from research
            cornering_stiffness = peak_grip / np.radians(6.0)  # Peak at 6°
            forces[i] = cornering_stiffness * np.radians(angle)
            
        elif angle <= 5.5:
            # Transitional region - approaching peak
            # Smooth transition from linear to plateau
            linear_force = cornering_stiffness * np.radians(2.0)
            transition_progress = (angle - 2.0) / (5.5 - 2.0)
            # Smooth S-curve transition
            transition_factor = 3 * transition_progress**2 - 2 * transition_progress**3
            forces[i] = linear_force + (peak_grip - linear_force) * transition_factor
            
        elif angle <= 8.0:
            # Plateau region (key improvement over AC default)
            # Based on OptimumG Tire B and racing tire characteristics
            plateau_factor = 1.0 - 0.02 * (angle - 5.5)  # Slight decline in plateau
            forces[i] = peak_grip * plateau_factor
            
        else:
            # Post-peak falloff
            # More realistic than AC's exponential decay
            plateau_end_force = peak_grip * 0.95  # Force at end of plateau
            
            if angle <= 12.0:
                # Moderate falloff (8-12°)
                falloff_progress = (angle - 8.0) / (12.0 - 8.0)
                # Keep ~75% grip at 12° (research-based)
                target_retention = 0.75
                forces[i] = plateau_end_force * (1.0 - falloff_progress * (1 - target_retention))
            else:
                # Steeper falloff beyond 12°
                initial_falloff = plateau_end_force * 0.75
                steep_progress = min((angle - 12.0) / 8.0, 1.0)  # Clamp at 20°
                # Asymptote to 60% retention (RT660-like)
                final_retention = 0.60
                forces[i] = initial_falloff * (final_retention + (1 - final_retention) * (1 - steep_progress))
    
    return forces

def generate_lut_file(slip_angles, forces, filename):
    """
    Generate AC-compatible LUT file
    Format: slip_angle|normalized_force
    """
    # Normalize forces to peak = 1.0
    peak_force = np.max(forces)
    normalized_forces = forces / peak_force
    
    with open(filename, 'w') as f:
        f.write("; Custom DY_CURVE for realistic slip angle behavior\n")
        f.write("; Generated from research data: OptimumG, Paul Haney, MATLAB Pacejka\n")
        f.write("; Includes plateau region (5.5-8°) and progressive falloff\n")
        f.write(";\n")
        f.write("; Format: slip_angle_degrees|normalized_lateral_force\n")
        f.write(";\n")
        
        for angle, force in zip(slip_angles, normalized_forces):
            f.write(f"{angle:.1f}|{force:.4f}\n")
    
    print(f"Generated LUT file: {filename}")
    return normalized_forces

def plot_load_sensitivity_analysis():
    """
    Analyze how different vertical loads affect the tire curve
    """
    # Current GT86 SSC parameters
    dy_ref = 1.26
    fz0 = 2494  # Reference load (N)
    ls_exp = 0.8119  # Load sensitivity exponent
    
    # Different vertical loads to test (N)
    # Representing different loading conditions
    loads = [2000, 2494, 3000, 3500, 4000]  # Light to heavy loading
    load_labels = ['Light (2000N)', 'Reference (2494N)', 'Medium (3000N)', 
                   'Heavy (3500N)', 'Very Heavy (4000N)']
    
    slip_angles = np.linspace(0, 15, 151)  # High resolution for LUT
    
    plt.figure(figsize=(14, 10))
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    colors = ['blue', 'red', 'green', 'orange', 'purple']
    
    # Plot 1: Load sensitivity curves
    for i, (load, label) in enumerate(zip(loads, load_labels)):
        forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, load)
        ax1.plot(slip_angles, forces, color=colors[i], linewidth=2, label=label)
    
    ax1.set_xlabel('Slip Angle (degrees)')
    ax1.set_ylabel('Lateral Force (Normalized)')
    ax1.set_title('Load Sensitivity Analysis - Custom Tire Curves')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.set_xlim(0, 15)
    
    # Plot 2: Zoom on plateau region
    for i, (load, label) in enumerate(zip(loads, load_labels)):
        forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, load)
        plateau_mask = (slip_angles >= 4) & (slip_angles <= 10)
        ax2.plot(slip_angles[plateau_mask], forces[plateau_mask], 
                color=colors[i], linewidth=2, label=label)
    
    ax2.set_xlabel('Slip Angle (degrees)')
    ax2.set_ylabel('Lateral Force (Normalized)')
    ax2.set_title('Plateau Region Detail (4-10°)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    
    # Plot 3: Load scaling factor
    load_range = np.linspace(1500, 4500, 100)
    scaling_factors = [calculate_load_scaling(load, fz0, ls_exp) for load in load_range]
    ax3.plot(load_range, scaling_factors, 'b-', linewidth=2)
    ax3.axvline(x=fz0, color='red', linestyle='--', alpha=0.7, label=f'FZ0 = {fz0}N')
    ax3.set_xlabel('Vertical Load (N)')
    ax3.set_ylabel('Grip Scaling Factor')
    ax3.set_title(f'Load Sensitivity (LS_EXP = {ls_exp})')
    ax3.grid(True, alpha=0.3)
    ax3.legend()
    
    # Plot 4: Comparison with current AC model
    reference_load = 2494
    current_forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, reference_load)
    
    # Simulate current AC exponential falloff
    ac_forces = np.zeros_like(slip_angles)
    peak_angle = 8.5
    falloff_level = 0.6
    falloff_speed = 8
    
    for i, angle in enumerate(slip_angles):
        if angle <= peak_angle:
            ac_forces[i] = dy_ref * np.radians(angle) / np.radians(peak_angle)
        else:
            excess = angle - peak_angle
            peak_force = dy_ref
            falloff_factor = np.exp(-falloff_speed * excess / peak_angle)
            ac_forces[i] = peak_force * (falloff_level + (1 - falloff_level) * falloff_factor)
    
    ax4.plot(slip_angles, current_forces, 'b-', linewidth=2, label='Custom Curve (Plateau)')
    ax4.plot(slip_angles, ac_forces, 'r--', linewidth=2, label='Current AC Model')
    ax4.set_xlabel('Slip Angle (degrees)')
    ax4.set_ylabel('Lateral Force (Normalized)')
    ax4.set_title('Custom vs Current AC Model')
    ax4.grid(True, alpha=0.3)
    ax4.legend()
    ax4.set_xlim(0, 15)
    
    plt.tight_layout()
    plt.savefig('/Users/ferchak/src/ssc-mod/research/load_sensitivity_analysis.png', 
                dpi=300, bbox_inches='tight')
    
    # Generate the actual LUT file for GT86 SSC
    reference_forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, reference_load)
    normalized_forces = generate_lut_file(slip_angles, reference_forces, 
                                        '/Users/ferchak/src/ssc-mod/research/dy_curve_custom.lut')
    
    # Print analysis
    print("\n" + "="*70)
    print("CUSTOM TIRE CURVE ANALYSIS")
    print("="*70)
    
    reference_forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, reference_load)
    peak_force = np.max(reference_forces)
    peak_angle_idx = np.argmax(reference_forces)
    peak_angle = slip_angles[peak_angle_idx]
    
    # Find plateau characteristics
    plateau_start = 5.5
    plateau_end = 8.0
    plateau_start_idx = np.argmin(np.abs(slip_angles - plateau_start))
    plateau_end_idx = np.argmin(np.abs(slip_angles - plateau_end))
    plateau_variation = (np.max(reference_forces[plateau_start_idx:plateau_end_idx]) - 
                        np.min(reference_forces[plateau_start_idx:plateau_end_idx])) / peak_force * 100
    
    # Find force retention at key angles
    angle_10_idx = np.argmin(np.abs(slip_angles - 10.0))
    angle_12_idx = np.argmin(np.abs(slip_angles - 12.0))
    angle_15_idx = np.argmin(np.abs(slip_angles - 15.0))
    
    retention_10 = reference_forces[angle_10_idx] / peak_force * 100
    retention_12 = reference_forces[angle_12_idx] / peak_force * 100
    retention_15 = reference_forces[angle_15_idx] / peak_force * 100
    
    print(f"Peak Grip: {peak_force:.3f} at {peak_angle:.1f}°")
    print(f"Plateau Region: {plateau_start}° to {plateau_end}° (variation: {plateau_variation:.1f}%)")
    print(f"Force Retention:")
    print(f"  At 10°: {retention_10:.1f}%")
    print(f"  At 12°: {retention_12:.1f}%")
    print(f"  At 15°: {retention_15:.1f}%")
    
    print(f"\nLoad Sensitivity Examples (LS_EXP = {ls_exp}):")
    for load in [2000, 3000, 4000]:
        scale = calculate_load_scaling(load, fz0, ls_exp)
        print(f"  {load}N load: {scale:.3f}x grip scaling ({scale*100-100:+.1f}%)")

if __name__ == "__main__":
    plot_load_sensitivity_analysis()