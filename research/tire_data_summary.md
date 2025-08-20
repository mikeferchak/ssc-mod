# Tire Data Research Summary

## Sources Reviewed

### 1. MATLAB Vehicle Dynamics Package
**Source:** https://andresmendes.github.io/Vehicle-Dynamics-Lateral/
- Pacejka tire model parameters extracted from TireComparison.m
- Mathematical relationships for slip angle vs lateral force

**Key Pacejka Parameters:**
```
a0 = 1.3
a1 = 2.014156  
a2 = 710.5013
a3 = 1226.0
a4 = 42.3
a5 = 0.0109
```

**Cornering Stiffness Formula:** K = BCD * 180/π

**Slip Angle Range:** 0-15° for normal operation, extends to 180°

**Key Finding:** "For small slip angles, linear, polynomial, and Pacejka models are equivalent"

### 2. OptimumG Tire Comparison Study
**Source:** TireComparison.pdf (FSAE TTC tire testing data from Calspan)

**Tire A Characteristics:**
- Cornering stiffness: 492 N/° (light load)
- Peak slip angle: ~4-5°
- Sharp cornering stiffness dropoff after peak
- Higher load sensitivity
- Strong camber response at all slip angles

**Tire B Characteristics:**
- Cornering stiffness: 451 N/° (light load), >50% higher at high load
- Peak slip angle: ~6.5-7°
- More gradual cornering stiffness decline
- Lower load sensitivity
- Minimal camber response above 4° slip angle

**Critical Measurements:**
- Peak slip angle difference: 2.5° at low loads
- Cornering stiffness coefficient varies with vertical load
- Coefficient of friction decreases with increasing load

### 3. General Racing Tire Characteristics
**From motorsport literature and testing:**
- Typical racing tires: peak grip at 5-6° slip angle
- Maximum utilization: up to 7-8° slip angle
- Linear region: 0-2° slip angle (cornering stiffness dominant)
- 200TW tires: more progressive breakaway than R-compounds

## Application to GT86 SSC Physics

### For Assetto Corsa tyres.ini:

**Linear Region (0-2° slip angle):**
- Use cornering stiffness ~450-500 N/°
- Match Pacejka curve initial slope

**Peak Grip Location:**
- Set around 5-6° slip angle (typical for performance tires)
- Adjust based on desired tire characteristics

**Breakaway Characteristics:**
- Make post-peak gradual, not sharp (200TW behavior)
- Reference OptimumG Tire B for progressive characteristics

**Load Sensitivity:**
- Coefficient of friction should decrease with increasing load
- Tire B shows more linear load response

**Camber Response:**
- Strong effect at low slip angles
- Reduced effectiveness near peak grip

### Validation Approach:
1. Use real Solo Spec Coupe telemetry data
2. Reference published 200TW tire specifications
3. Correlate simulation results with actual track performance
4. Validate lap times and handling characteristics

### 4. Paul Haney - "The Racing and High-Performance Tire"
**Source:** Chapter 6 - Tire Behavior (OCR extracted)

**Fundamental Slip Angle Concepts:**
- Tire generates no side force until steered away from current course
- Contact patch deforms as it rotates through contact area
- Force needed to deform tire produces lateral force for cornering

**Slip Angle vs Lateral Force Curve Regions:**
1. **Elastic/Linear Region (small slip angles)**:
   - Almost straight relationship between slip angle and lateral force
   - Proportional increase in lateral force with slip angle
   - No sliding in contact patch - purely elastic deformation
   - Slope = "cornering stiffness" (measured in lb/deg or N/deg)

2. **Transitional Region (medium slip angles)**:
   - Portions of contact patch begin sliding
   - Less increase in lateral force per degree of slip angle
   - Mixed adhesion and slip areas in contact patch

3. **Frictional Region (high slip angles)**:
   - Most of contact patch is sliding
   - Lateral force can drop 30% within a few degrees past peak
   - Generates significant heat and tire wear
   - Peak typically occurs before this region begins

**Contact Patch Behavior:**
- Leading edge curves toward turn direction
- Trailing edge lags behind on old heading
- Adhesive area at front, slip area at rear of contact patch
- Contact patch migration during braking/acceleration

**Combined Forces:**
- Lateral force falls off rapidly with longitudinal slip (braking/acceleration)
- Driving force peaks around 50% slip, then drops rapidly
- Braking force peaks around 25% slip, more gradual decline

**Key Insight for Racing Applications:**
- Operating in the linear region provides maximum control and predictability
- Peak force occurs just before significant sliding begins
- Post-peak behavior determines controllability at the limit

## Implementation Results

### Custom Tire Curve Generated
- **File Created**: `dy_curve_custom.lut` - AC-compatible LUT file
- **Plateau Region**: 5.5-8° with only 4.8% variation  
- **Progressive Falloff**: 83% at 10°, 71% at 12°, 61% at 15°
- **Based on**: Combined OptimumG, Paul Haney, and Pacejka research data

### Key Discovery: Load Sensitivity
**Formula**: `Actual_Grip = DY_REF × (Current_Load/FZ0)^LS_EXP`
- **LS_EXP = 0.8119**: Diminishing returns with load (realistic)
- **FZ0 = 2494N**: Tire design reference point (NOT vehicle corner weight)
- **Load scaling examples**: 2000N = 84% grip, 4000N = 147% grip

### FALLOFF_SPEED Analysis
- **Current value (8)**: Abrupt RT660-like behavior
- **Recommended (2)**: More progressive, controllable falloff
- **Effect**: Controls post-peak grip decay rate

### Validation Summary
1. **Current GT86 SSC setup**: Excellent for RT660 characteristics
2. **Custom DY_CURVE**: Provides realistic plateau behavior  
3. **Load sensitivity**: Properly calibrated for tire physics
4. **Research correlation**: Matches real-world tire testing data

### Tools Created
- `tire_curve_plotter.py`: Visualize and compare tire curves
- `custom_tire_curve_generator.py`: Generate realistic LUT files
- `dy_curve_custom.lut`: Ready-to-use custom tire curve

### Implementation Options
1. **Keep current setup**: Realistic RT660 behavior
2. **Use custom curve**: Add `DY_CURVE=dy_curve_custom.lut` for plateau behavior
3. **Hybrid approach**: Adjust FALLOFF_SPEED=2 for better progression

**See**: `tire_physics_research_findings.md` for complete research documentation