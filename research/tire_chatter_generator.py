#!/usr/bin/env python3
"""
Tire Chatter LUT Generator
Creates experimental tire curves with progressive noise beyond 10° slip angle
to simulate real tire chattering/juddering behavior
"""

import numpy as np
import matplotlib.pyplot as plt

def create_chatter_tire_curve(slip_angles, dy_ref, fz0, ls_exp, vertical_load, 
                             chatter_start=10.0, chatter_intensity=0.15, 
                             chatter_frequency=2.0):
    """
    Create tire curve with progressive chatter noise beyond specified slip angle
    
    Args:
        slip_angles: Array of slip angles in degrees
        dy_ref: Lateral grip coefficient at reference load
        fz0: Reference load in Newtons
        ls_exp: Load sensitivity exponent
        vertical_load: Current vertical load
        chatter_start: Slip angle where chatter begins (degrees)
        chatter_intensity: Maximum amplitude of chatter noise (0-1)
        chatter_frequency: Frequency scaling factor for chatter oscillations
    """
    from custom_tire_curve_generator import calculate_load_scaling, create_realistic_tire_curve
    
    # Start with the base realistic curve
    base_forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, vertical_load)
    
    # Add progressive chatter noise beyond chatter_start angle
    chattering_forces = base_forces.copy()
    
    for i, angle in enumerate(slip_angles):
        if angle >= chatter_start:
            # Calculate chatter progression (0 at start, 1 at max angle)
            chatter_progress = min((angle - chatter_start) / (20.0 - chatter_start), 1.0)
            
            # Create multiple frequency components for realistic chatter
            # High frequency component (main chatter)
            high_freq = np.sin(angle * chatter_frequency * 8) * 0.6
            # Medium frequency component (secondary oscillation)
            med_freq = np.sin(angle * chatter_frequency * 3) * 0.3
            # Low frequency component (major fluctuation)
            low_freq = np.sin(angle * chatter_frequency * 1) * 0.1
            
            # Combine frequencies with phase shifts for complexity
            noise_component = (high_freq + 
                             med_freq * np.cos(angle * 0.7) + 
                             low_freq * np.sin(angle * 1.3))
            
            # Apply progressive intensity scaling
            scaled_noise = noise_component * chatter_intensity * chatter_progress
            
            # Add randomization to make it less predictable
            random_factor = (np.sin(angle * 13.7) * 0.1 + np.cos(angle * 7.3) * 0.05)
            
            # Apply noise to base force (ensuring we don't go negative)
            chattering_forces[i] = max(base_forces[i] * (1 + scaled_noise + random_factor * chatter_progress), 
                                     base_forces[i] * 0.1)  # Minimum 10% of base force
    
    return chattering_forces

def generate_experimental_curves():
    """
    Generate multiple experimental tire curves with different chatter characteristics
    """
    # Current GT86 SSC parameters
    dy_ref = 1.26
    fz0 = 2494  # Reference load (N)
    ls_exp = 0.8119  # Load sensitivity exponent
    reference_load = 2494
    
    slip_angles = np.linspace(0, 20, 201)  # Higher resolution for smooth curves
    
    # Different chatter configurations to test
    chatter_configs = [
        {"name": "Subtle Chatter", "intensity": 0.08, "frequency": 1.5, "start": 12.0},
        {"name": "Moderate Chatter", "intensity": 0.15, "frequency": 2.0, "start": 10.0},
        {"name": "Aggressive Chatter", "intensity": 0.25, "frequency": 3.0, "start": 9.0},
        {"name": "High-Freq Buzz", "intensity": 0.12, "frequency": 4.0, "start": 11.0}
    ]
    
    # Create base curve for comparison
    from custom_tire_curve_generator import create_realistic_tire_curve
    base_forces = create_realistic_tire_curve(slip_angles, dy_ref, fz0, ls_exp, reference_load)
    
    plt.figure(figsize=(16, 12))
    
    # Plot 1: Full curves comparison
    plt.subplot(2, 2, 1)
    plt.plot(slip_angles, base_forces, 'k-', linewidth=2, label='Base Curve (No Chatter)')
    
    colors = ['blue', 'red', 'green', 'orange']
    chatter_curves = {}
    
    for i, config in enumerate(chatter_configs):
        forces = create_chatter_tire_curve(slip_angles, dy_ref, fz0, ls_exp, reference_load,
                                         chatter_start=config["start"],
                                         chatter_intensity=config["intensity"],
                                         chatter_frequency=config["frequency"])
        chatter_curves[config["name"]] = forces
        plt.plot(slip_angles, forces, color=colors[i], linewidth=1.5, 
                label=f'{config["name"]} (I:{config["intensity"]}, F:{config["frequency"]})')
    
    plt.axvline(x=10, color='gray', linestyle='--', alpha=0.7, label='Typical Chatter Start')
    plt.xlabel('Slip Angle (degrees)')
    plt.ylabel('Lateral Force (Normalized)')
    plt.title('Tire Curves with Progressive Chatter Beyond Limit')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.xlim(0, 20)
    
    # Plot 2: Zoom on chatter region
    plt.subplot(2, 2, 2)
    plt.plot(slip_angles, base_forces, 'k-', linewidth=2, label='Base Curve')
    
    for i, (name, forces) in enumerate(chatter_curves.items()):
        plt.plot(slip_angles, forces, color=colors[i], linewidth=1.5, label=name)
    
    plt.xlim(8, 16)
    plt.xlabel('Slip Angle (degrees)')
    plt.ylabel('Lateral Force (Normalized)')
    plt.title('Chatter Region Detail (8-16°)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 3: Chatter amplitude analysis
    plt.subplot(2, 2, 3)
    chatter_region = (slip_angles >= 10) & (slip_angles <= 16)
    
    for i, (name, forces) in enumerate(chatter_curves.items()):
        # Calculate RMS of chatter noise
        base_smooth = np.interp(slip_angles[chatter_region], slip_angles, base_forces)
        noise = forces[chatter_region] - base_smooth
        rms_noise = np.sqrt(np.mean(noise**2))
        
        plt.plot(slip_angles[chatter_region], noise, color=colors[i], 
                linewidth=1, label=f'{name} (RMS: {rms_noise:.3f})')
    
    plt.xlabel('Slip Angle (degrees)')
    plt.ylabel('Chatter Noise Amplitude')
    plt.title('Chatter Noise Components')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Plot 4: Frequency analysis
    plt.subplot(2, 2, 4)
    
    # Analyze frequency content of chatter
    sample_region = (slip_angles >= 10) & (slip_angles <= 15)
    sample_angles = slip_angles[sample_region]
    
    for i, (name, forces) in enumerate(chatter_curves.items()):
        sample_forces = forces[sample_region]
        
        # Simple frequency analysis via derivative
        force_derivative = np.gradient(sample_forces)
        plt.plot(sample_angles[1:], np.abs(force_derivative[1:]), 
                color=colors[i], linewidth=1.5, label=f'{name} Variation')
    
    plt.xlabel('Slip Angle (degrees)')
    plt.ylabel('Force Variation Rate')
    plt.title('Chatter Activity Level')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/Users/ferchak/src/ssc-mod/research/tire_chatter_analysis.png', 
                dpi=300, bbox_inches='tight')
    
    # Generate LUT files for testing
    generate_chatter_lut_files(slip_angles, chatter_curves, dy_ref)
    
    # Print analysis
    print("\n" + "="*70)
    print("TIRE CHATTER SIMULATION ANALYSIS")
    print("="*70)
    
    for name, forces in chatter_curves.items():
        config = next(c for c in chatter_configs if c["name"] == name)
        
        # Find maximum chatter amplitude
        chatter_region_forces = forces[(slip_angles >= 10) & (slip_angles <= 16)]
        base_region_forces = base_forces[(slip_angles >= 10) & (slip_angles <= 16)]
        
        max_positive_excursion = np.max(chatter_region_forces - base_region_forces)
        max_negative_excursion = np.min(chatter_region_forces - base_region_forces)
        
        print(f"\n{name}:")
        print(f"  Chatter starts at: {config['start']}°")
        print(f"  Intensity setting: {config['intensity']}")
        print(f"  Frequency setting: {config['frequency']}")
        print(f"  Max positive variation: +{max_positive_excursion:.3f}")
        print(f"  Max negative variation: {max_negative_excursion:.3f}")
        print(f"  Total chatter range: {max_positive_excursion - max_negative_excursion:.3f}")

def generate_chatter_lut_files(slip_angles, chatter_curves, dy_ref):
    """
    Generate LUT files for each chatter configuration
    """
    for name, forces in chatter_curves.items():
        # Normalize forces to peak = 1.0
        peak_force = np.max(forces)
        normalized_forces = forces / peak_force
        
        # Create filename
        safe_name = name.lower().replace(' ', '_').replace('-', '_')
        filename = f'/Users/ferchak/src/ssc-mod/research/dy_curve_chatter_{safe_name}.lut'
        
        with open(filename, 'w') as f:
            f.write(f"; Experimental chatter tire curve: {name}\n")
            f.write("; WARNING: This is experimental and may cause unrealistic behavior\n")
            f.write("; Progressive chatter noise beyond 10° slip angle\n")
            f.write("; Simulates tire juddering/chattering at extreme slip angles\n")
            f.write(";\n")
            f.write("; Format: slip_angle_degrees|normalized_lateral_force\n")
            f.write(";\n")
            
            for angle, force in zip(slip_angles, normalized_forces):
                f.write(f"{angle:.1f}|{force:.4f}\n")
        
        print(f"Generated experimental LUT: {filename}")

if __name__ == "__main__":
    generate_experimental_curves()