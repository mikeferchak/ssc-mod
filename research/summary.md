# Tire Model Tuning Summary

## Overview
Documentation of the process used to tune the Falken RT660 tire model in Assetto Corsa for the Solo Spec Coupe project, correlating simulation behavior with real-world performance data.

## Project Context
- **Vehicle**: Toyota GT86 Solo Spec Coupe (SCCA class)
- **Tire**: Falken RT660 225/45R17
- **Weight**: 2800 lbs with driver (2650 lbs race trim)
- **Weight Distribution**: 57.5% front / 42.5% rear (CG_LOCATION=0.575)
- **Real-world optimal pressures**: 31 PSI front / 29 PSI rear (hot)

## Initial Research Phase

### Documentation Approach
1. Created comprehensive inline documentation for all physics files
2. Researched Falken RT660 specifications and performance characteristics
3. Compiled real-world data in `research/rt660.md`
4. Added source documentation headers to all physics configuration files

### Key Research Findings
- RT660 has abrupt breakaway characteristics with peaky grip
- Optimal after one run but competitive immediately when cold
- Gets greasy when hot after just a few successive runs
- Stiff sidewalls provide responsive feel but narrow operating window

## Tire Model Tuning Process

### Step 1: Pressure Optimization
**Issue**: Simulation optimal pressures didn't match real-world setup
**Solution**: Updated `PRESSURE_IDEAL` values
- Front: 32 PSI → 31 PSI
- Rear: 30 PSI → 29 PSI

**Result**: Negligible real-world difference but proper correlation baseline

### Step 2: Temperature Profile Correction
**Issue**: All four tires heated equally, but in real life fronts get warm while rears stay cool
**Initial Approach**: Tried adjusting `FRICTION_K` values
- Front: 0.11 → 0.12
- Rear: 0.11 → 0.10

**Problem**: This was an artificial fix that didn't address root cause

### Step 3: Load-Based Heat Generation (Failed Approach)
**Theory**: Front-heavy weight distribution should naturally create more heat on fronts
**Attempted Solution**: Adjust `FZ0` (reference load) values to match actual corner weights
- Front: 2494N → 3580N (805 lbs actual load)
- Rear: 2494N → 2650N (595 lbs actual load)

**Result**: Made handling worse - fronts too sharp, rears too loose
**Key Learning**: `FZ0` is not about actual vehicle loads but tire design reference points

### Step 4: Return to Pragmatic FRICTION_K Approach
**Decision**: Revert `FZ0` to original 2494N, use different `FRICTION_K` values for front/rear
**Reasoning**: Simple, direct solution that addresses the specific temperature issue

### Step 5: Final Refinements
**User-Driven Adjustments**:
1. **Peak Slip Angle**: `FRICTION_LIMIT_ANGLE` 8.0° → 8.5° (less darty steering feel)
2. **Grip Balance**: Front `DY_REF` 1.27 → 1.26 (reduce front sharpness)
3. **Falloff Characteristics**: 
   - `FALLOFF_LEVEL` 0.65 → 0.6 (maintain abrupt character)
   - `FALLOFF_SPEED` 10 → 8 (slightly less harsh)
4. **Enhanced Temperature Differential**:
   - Front `FRICTION_K` 0.12 → 0.14 (more front heat)
   - Rear `FRICTION_K` 0.10 → 0.08 (less rear heat)
   - `ROLLING_K` reduced to 0.02 both ends

## Final Parameter Set

### Pressure Settings
- `PRESSURE_IDEAL`: 31F / 29R PSI (matches real-world optimal)
- `PRESSURE_STATIC`: 29.0F / 27R PSI (cold pressures)

### Grip Characteristics  
- `DY_REF`: 1.26F / 1.27R (slight front reduction for balance)
- `DX_REF`: 1.27 both ends (longitudinal grip)
- `FRICTION_LIMIT_ANGLE`: 8.5° both ends (peak slip angle)

### Falloff Behavior (Abrupt Breakaway Character)
- `FALLOFF_LEVEL`: 0.6 both ends (sharp dropoff after peak)
- `FALLOFF_SPEED`: 8 both ends (moderate transition rate)

### Thermal Model (Temperature Differential)
- `FRICTION_K`: 0.14F / 0.08R (75% more front heat generation)
- `ROLLING_K`: 0.02 both ends (reduced rolling resistance heat)
- `CORE_TRANSFER`: 0.0002 both ends (heat transfer rate)

## Key Learnings

### Technical Insights
1. **FZ0 Parameter**: Reference load for tire calibration, not actual vehicle corner weights
2. **FRICTION_K**: Direct heat generation from slip - pragmatic solution for temperature differentials
3. **Peak Slip Angle**: Major influence on steering feel and "dartiness"
4. **Falloff Parameters**: Control abrupt vs. progressive breakaway characteristics

### Process Methodology
1. **Research First**: Comprehensive documentation before making changes
2. **One Change at a Time**: Iterative approach with real-world validation
3. **Real-World Data Priority**: User experience trumps theoretical calculations
4. **Pragmatic Solutions**: Sometimes "fudging" numbers is the right approach

### Failed Approaches
- **Load-Based Heat**: Adjusting FZ0 for temperature differential (made handling worse)
- **Over-Engineering**: Trying to match exact physics when simple solutions work better

## Validation Results
- **Temperature Profile**: Fronts now warm after one run, rears stay cool ✓
- **Pressure Optimization**: Peak grip at real-world optimal pressures ✓  
- **Steering Feel**: Less darty with 8.5° peak slip angle ✓
- **Breakaway Character**: Maintains RT660's abrupt limit behavior ✓
- **Overall Balance**: Front sharpness reduced, maintains competitive characteristics ✓

## Future Refinement Areas
- Peak slip angle may need further adjustment based on extended testing
- Thermal model could be refined with more detailed real-world temperature data
- Falloff characteristics may benefit from fine-tuning with more track time

## Tools and Documentation
- **Research File**: `research/rt660.md` - Comprehensive RT660 tire data
- **Source Documentation**: Inline comments in all physics files with parameter explanations
- **Version Control**: Documented changes for future reference and rollback capability

---

*This summary serves as a reference for future tire model tuning projects and demonstrates the iterative process of correlating simulation physics with real-world vehicle behavior.*