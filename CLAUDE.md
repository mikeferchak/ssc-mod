# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Assetto Corsa car modification project for a Toyota GT86 SSC (Solo Spec Coupe). This mod is based on a real-life race car competing in the SCCA Solo Spec Coupe class. The project contains car assets, configuration files, and textures for the racing simulation game Assetto Corsa.

### Real-World Correlation
- Based on actual SCCA Solo Spec Coupe race car
- Real-life performance data available for correlation and validation
- All modifications are off-the-shelf parts with published specifications
- Physics settings should reflect real-world performance characteristics

## Project Structure

- `ks_toyota_gt86_SSC/` - Main car mod directory containing all game assets
  - `data/` - Car physics and behavior configuration files (.ini format)
  - `skins/` - Different paint schemes and liveries for the car
  - `texture/` - Car textures and materials (.dds format)
  - `sfx/` - Sound effects and audio files
  - `ui/` - User interface assets and car information
  - `animations/` - Car animation files (.ksanim format)
  - `*.kn5` - 3D model files for different levels of detail (LOD)
- `unpacked_model/` - Contains unpacked 3D model files (.FBX format) and textures

## Key Configuration Files

### Car Physics and Behavior
- `data/car.ini` - Main car configuration (mass, graphics offsets, fuel, controls)
- `data/engine.ini` - Engine specifications and performance curves
- `data/suspensions.ini` - Suspension setup and geometry
- `data/tyres.ini` - Tire physics and grip characteristics
- `data/aero.ini` - Aerodynamic properties

### Car Information
- `ui/ui_car.json` - Car metadata, specifications, and torque/power curves displayed in game

## Asset Types

### Textures
- `.dds` files - DirectDraw Surface textures optimized for game engines
- Naming conventions: `_D` (diffuse), `_NM` (normal map), `_MAP` (material properties)

### Models
- `.kn5` files - Assetto Corsa's proprietary 3D model format
- Multiple LOD (Level of Detail) versions for performance optimization

### Skins/Liveries
Each skin directory contains:
- `livery.png` - Preview image
- `skin.ini` - Skin configuration
- `ui_skin.json` - Skin metadata for UI
- Various texture files specific to that livery

## Working with This Project

### Modifying Car Physics
Edit files in the `data/` directory. Key files:
- Adjust performance: `engine.ini`, `power.lut`, `throttle.lut`
- Modify handling: `suspensions.ini`, `tyres.ini`
- Change aerodynamics: `aero.ini`, wing curve `.lut` files

### Physics Validation Approach
When modifying physics parameters:
1. Reference real-world data from the actual Solo Spec Coupe car
2. Use published specifications for off-the-shelf modifications
3. Correlate simulation results with real-world performance data
4. Validate lap times and handling characteristics against actual track data

### Adding New Liveries
1. Create new directory in `skins/`
2. Add required texture files
3. Configure `skin.ini` and `ui_skin.json`

### Asset Pipeline
- Original models are in `.FBX` format (in `unpacked_model/`)
- Converted to `.kn5` format for game use
- Textures should be in `.dds` format for optimal performance

## Documentation Approach

All key physics configuration files have been documented with inline comments explaining parameters, units, and typical value ranges. This documentation is based on community research and real-world correlation data.

### Documented Physics Files
- `car.ini` - Main vehicle configuration (mass, graphics, controls, fuel)
- `engine.ini` - Engine performance and behavior parameters
- `suspensions.ini` - Suspension geometry, spring rates, damping
- `tyres.ini` - Tire physics including grip, pressure, and wear characteristics
- `aero.ini` - Aerodynamic wing definitions and coefficients

When modifying physics parameters, always reference the inline comments for parameter explanations and validate changes against real-world data from the actual Solo Spec Coupe.

## File Formats
- `.ini` - Configuration files using Windows INI format
- `.json` - Car and skin metadata
- `.lut` - Lookup tables for physics curves (space-separated values)
- `.kn5` - Assetto Corsa 3D model format
- `.dds` - DirectDraw Surface texture format
- `.ksanim` - Assetto Corsa animation format