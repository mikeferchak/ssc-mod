#!/usr/bin/env python3
"""
Assetto Corsa Tire Curve Plotter
Plot slip angle vs lateral force curves based on AC tire model and research data
"""

import numpy as np
import matplotlib.pyplot as plt

def ac_tire_model(slip_angle, dy_ref, friction_limit_angle, falloff_level, falloff_speed):
    """
    Assetto Corsa brush tire model approximation
    Based on research of AC's custom brush model implementation
    """
    slip_rad = np.radians(slip_angle)
    friction_limit_rad = np.radians(friction_limit_angle)
    
    # Linear region up to peak
    linear_force = dy_ref * slip_rad
    
    # Calculate forces for the entire range
    forces = np.zeros_like(slip_angle)
    
    for i, angle in enumerate(slip_angle):
        if angle <= friction_limit_angle:
            # Linear region - pure elastic deformation
            forces[i] = dy_ref * np.radians(angle)
        else:
            # Post-peak region with falloff
            excess_angle = angle - friction_limit_angle
            peak_force = dy_ref * friction_limit_rad
            
            # Exponential falloff approximation
            falloff_factor = np.exp(-falloff_speed * excess_angle / friction_limit_angle)
            post_peak_force = peak_force * (falloff_level + (1 - falloff_level) * falloff_factor)
            forces[i] = post_peak_force
    
    return forces

def plot_falloff_speed_analysis():
    """
    Analyze the effect of FALLOFF_SPEED parameter on tire curves
    """
    # Slip angle range (degrees)
    slip_angles = np.linspace(0, 15, 100)
    
    # Fixed parameters for FALLOFF_SPEED analysis
    dy_ref = 1.26
    friction_limit_angle = 8.5
    falloff_level = 0.6
    
    # Different FALLOFF_SPEED values to test
    falloff_speeds = [2, 4, 6, 8, 12, 16]
    
    plt.figure(figsize=(14, 10))
    
    # Create subplots for detailed analysis
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    colors = ['blue', 'green', 'orange', 'red', 'purple', 'brown']
    
    for i, speed in enumerate(falloff_speeds):
        forces = ac_tire_model(slip_angles, dy_ref, friction_limit_angle, falloff_level, speed)
        
        # Full curve
        ax1.plot(slip_angles, forces, color=colors[i], linewidth=2, 
                label=f'FALLOFF_SPEED = {speed}')
        
        # Zoomed post-peak region
        post_peak_mask = slip_angles >= friction_limit_angle
        ax2.plot(slip_angles[post_peak_mask], forces[post_peak_mask], 
                color=colors[i], linewidth=2, label=f'Speed = {speed}')
    
    # Format first subplot (full curve)
    ax1.set_xlabel('Slip Angle (degrees)')
    ax1.set_ylabel('Lateral Force (Normalized)')
    ax1.set_title('FALLOFF_SPEED Parameter Analysis\nFull Slip Angle Range')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    ax1.axvline(x=friction_limit_angle, color='red', linestyle='--', alpha=0.7, 
                label=f'Peak at {friction_limit_angle}°')
    ax1.set_xlim(0, 15)
    ax1.set_ylim(0, 0.2)
    
    # Format second subplot (post-peak detail)
    ax2.set_xlabel('Slip Angle (degrees)')
    ax2.set_ylabel('Lateral Force (Normalized)')
    ax2.set_title('Post-Peak Behavior Detail (Slip Angle > 8.5°)')
    ax2.grid(True, alpha=0.3)
    ax2.legend()
    ax2.set_xlim(8.5, 15)
    
    plt.tight_layout()
    plt.savefig('/Users/ferchak/src/ssc-mod/research/falloff_speed_analysis.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Calculate metrics for each FALLOFF_SPEED
    print("\n" + "="*70)
    print("FALLOFF_SPEED PARAMETER ANALYSIS")
    print("="*70)
    print(f"Fixed Parameters: DY_REF={dy_ref}, FRICTION_LIMIT_ANGLE={friction_limit_angle}°, FALLOFF_LEVEL={falloff_level}")
    print()
    
    for speed in falloff_speeds:
        forces = ac_tire_model(slip_angles, dy_ref, friction_limit_angle, falloff_level, speed)
        
        # Find force at specific angles past peak
        angle_10 = np.argmin(np.abs(slip_angles - 10.0))
        angle_12 = np.argmin(np.abs(slip_angles - 12.0))
        angle_15 = np.argmin(np.abs(slip_angles - 15.0))
        
        peak_force = np.max(forces)
        force_at_10 = forces[angle_10]
        force_at_12 = forces[angle_12]
        force_at_15 = forces[angle_15]
        
        retention_10 = (force_at_10 / peak_force) * 100
        retention_12 = (force_at_12 / peak_force) * 100
        retention_15 = (force_at_15 / peak_force) * 100
        
        print(f"FALLOFF_SPEED = {speed:2d}:")
        print(f"  Force retention at 10°: {retention_10:5.1f}%")
        print(f"  Force retention at 12°: {retention_12:5.1f}%") 
        print(f"  Force retention at 15°: {retention_15:5.1f}%")
        print(f"  Rate of decay: {(retention_10 - retention_15)/(15-10):4.1f}% per degree")
        print()

def plot_tire_comparison():
    """
    Plot tire curves comparing GT86 SSC setup with research data
    """
    # Slip angle range (degrees)
    slip_angles = np.linspace(0, 15, 100)
    
    # GT86 SSC Current Parameters
    dy_ref_current = 1.26  # Current DY_REF
    friction_limit_current = 8.5  # Current FRICTION_LIMIT_ANGLE
    falloff_level_current = 0.6  # Current FALLOFF_LEVEL  
    falloff_speed_current = 8  # Current FALLOFF_SPEED
    
    # Research-based parameters (from OptimumG and Haney data)
    dy_ref_research = 1.30  # Higher peak grip (Tire B characteristics)
    friction_limit_research = 6.0  # Peak at 6° (typical racing tire)
    falloff_level_research = 0.75  # More gradual falloff (progressive)
    falloff_speed_research = 4  # Slower falloff rate
    
    # Conservative street tire parameters  
    dy_ref_street = 1.10  # Lower peak grip
    friction_limit_street = 4.5  # Earlier peak (street tire)
    falloff_level_street = 0.8  # Very gradual falloff
    falloff_speed_street = 2  # Slow falloff
    
    # Calculate forces
    forces_current = ac_tire_model(slip_angles, dy_ref_current, friction_limit_current, 
                                  falloff_level_current, falloff_speed_current)
    
    forces_research = ac_tire_model(slip_angles, dy_ref_research, friction_limit_research,
                                   falloff_level_research, falloff_speed_research)
    
    forces_street = ac_tire_model(slip_angles, dy_ref_street, friction_limit_street,
                                 falloff_level_street, falloff_speed_street)
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot curves
    plt.plot(slip_angles, forces_current, 'r-', linewidth=2, 
             label=f'GT86 SSC Current (RT660)\nPeak: {friction_limit_current}°, Falloff: {falloff_level_current}')
    
    plt.plot(slip_angles, forces_research, 'b-', linewidth=2,
             label=f'Research Optimized\nPeak: {friction_limit_research}°, Falloff: {falloff_level_research}')
             
    plt.plot(slip_angles, forces_street, 'g--', linewidth=2,
             label=f'Street Tire Reference\nPeak: {friction_limit_street}°, Falloff: {falloff_level_street}')
    
    # Add research reference lines
    plt.axvline(x=5.5, color='orange', linestyle=':', alpha=0.7, 
                label='Typical Racing Tire Peak (5-6°)')
    plt.axvline(x=8.5, color='red', linestyle=':', alpha=0.7,
                label='Current GT86 SSC Peak (8.5°)')
    
    # Formatting
    plt.xlabel('Slip Angle (degrees)', fontsize=12)
    plt.ylabel('Lateral Force (Normalized)', fontsize=12)
    plt.title('Assetto Corsa Tire Model: Slip Angle vs Lateral Force\nGT86 SSC vs Research Data', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.legend(fontsize=10)
    
    # Add annotations for key regions
    plt.annotate('Linear Region\n(Pure Elastic)', xy=(2, 0.5), xytext=(3, 0.8),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
                fontsize=9, ha='center', color='gray')
    
    plt.annotate('Transitional Region\n(Mixed Slip/Adhesion)', xy=(5, 1.1), xytext=(7, 1.4),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
                fontsize=9, ha='center', color='gray')
    
    plt.annotate('Post-Peak Region\n(Sliding Dominant)', xy=(10, 0.7), xytext=(12, 1.0),
                arrowprops=dict(arrowstyle='->', color='gray', alpha=0.7),
                fontsize=9, ha='center', color='gray')
    
    plt.xlim(0, 15)
    plt.ylim(0, 1.6)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('/Users/ferchak/src/ssc-mod/research/tire_curves_comparison.png', 
                dpi=300, bbox_inches='tight')
    plt.show()
    
    # Print analysis
    print("\n" + "="*60)
    print("TIRE CURVE ANALYSIS")
    print("="*60)
    
    print(f"\nCURRENT GT86 SSC SETUP:")
    print(f"  Peak Slip Angle: {friction_limit_current}°")
    print(f"  Peak Force: {max(forces_current):.3f}")
    print(f"  Falloff Level: {falloff_level_current} ({falloff_level_current*100:.0f}% retention)")
    print(f"  Cornering Stiffness (0-2°): {(forces_current[np.where(slip_angles <= 2)[0][-1]] / np.radians(2)):.2f}")
    
    print(f"\nRESEARCH OPTIMIZED SETUP:")
    print(f"  Peak Slip Angle: {friction_limit_research}°")
    print(f"  Peak Force: {max(forces_research):.3f}")
    print(f"  Falloff Level: {falloff_level_research} ({falloff_level_research*100:.0f}% retention)")
    print(f"  Cornering Stiffness (0-2°): {(forces_research[np.where(slip_angles <= 2)[0][-1]] / np.radians(2)):.2f}")
    
    print(f"\nRECOMMENDATIONS:")
    current_peak = max(forces_current)
    research_peak = max(forces_research)
    
    if research_peak > current_peak:
        print(f"  • Consider increasing DY_REF to {dy_ref_research} for +{((research_peak/current_peak-1)*100):.1f}% peak grip")
    
    if friction_limit_research < friction_limit_current:
        print(f"  • Consider reducing FRICTION_LIMIT_ANGLE to {friction_limit_research}° for more typical racing tire behavior")
        
    if falloff_level_research > falloff_level_current:
        print(f"  • Consider increasing FALLOFF_LEVEL to {falloff_level_research} for more progressive breakaway")

if __name__ == "__main__":
    # Run FALLOFF_SPEED analysis first
    plot_falloff_speed_analysis()
    
    # Then run the general comparison
    plot_tire_comparison()