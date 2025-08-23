# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
VetScan Pro 3000 - An educational veterinary medical scanner simulation game with multiple HTML implementations:
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **Standalone HTML versions**: 10 self-contained HTML files requiring no build process
- **3D Model Integration**: Advanced 3D pipeline with Blender MCP integration (see [3dworkflowBlender.md](./3dworkflowBlender.md))
- **Live Deployment**: Automatically deployed to https://vibecoding.company via GitHub Actions

## Development Commands

### React Version (uses Vite)
```bash
npm install           # Install dependencies
npm run dev          # Start dev server at http://localhost:3000
npm run build        # Build for production
npm run preview      # Preview production build
```

### Standalone HTML Versions (No Build Required)
```bash
python3 -m http.server 8080    # Start local server
# Then access: http://localhost:8080/[filename].html

# Alternative port if 8080 is busy:
python3 -m http.server 8081
```

### 3D Workflow & Blender Integration
```bash
# Test Blender MCP connection (when available)
node scripts/test-mcp-connection.js

# Run 3D asset pipeline
./scripts/deploy-animal.sh

# Generate medical visualization shaders
npm run generate:shaders -- --model=bello

# Validate 3D model exports and test integration
npm run test:integration -- --model=bello

# Manual browser testing for console errors
python3 test-console-errors.py
```

## Project Architecture

### Standalone HTML Versions (Primary Focus)
Each HTML file is completely self-contained with all code inline:

#### 🏆 **Production Versions**
- **vetscan-detective.html** - 🎯 **RECOMMENDED**: Educational detective gameplay with Dr. Eule mentor
- **standalone.html** - 🛡️ **STABLE**: Most stable base version, failsafe implementation

#### 🚀 **3D Medical Scanner Versions**  
- **vetscan-bello-3d-v7.html** - ⚡ **VERSION 7**: Latest 3D Bello viewer with enhanced medical shaders
- **vetscan-bello-3d.html** - 📦 **BACKUP**: Previous 3D version (v6)
- **vetscan-ultimate.html** - 3D visualization with Three.js and career mode

#### 📖 **Story & Campaign Versions**
- **vetscan-story-mode.html** - Story campaign with Dr. Sarah Miller
- **vetgame-missions.html** - Mission-based gameplay variant
- **vetscan-professional.html** - Professional medical simulation
- **vetscan-pro-leveling.html** - Level 1-50 progression with RPG elements
- **vetscan-advanced.html** - Advanced medical features
- **vetscan-premium.html** - Premium UI version with modern design

#### 🔧 **System Files**
- **index.html** - Landing page with version selector (auto-generated on deployment)

### 3D Model System
- **assets/models/animals/bello/** - Bello 3D model variants (high/medium/low quality)
- **src/game/AnimalLoader.js** - Progressive 3D model loading system
- **src/shaders/MedicalVisualization.js** - Medical visualization shader system
- **src/components/BelloViewer.jsx** - React 3D viewer component
- **scripts/deploy-animal.sh** - Automated 3D pipeline deployment
- **scripts/generate-shaders.js** - Medical shader generation system

### React Components (Secondary)
- **src/main.jsx** - Entry point, currently renders VetScanUltraAdvanced
- **src/VetScanUltraAdvanced.jsx** - Advanced React component (active)
- **src/AnimalScannerPro.jsx** - Base React component with core logic

### Core Game Data Structures
All versions share these common structures:
```javascript
// Disease presets per animal type
commonDiseases = {
  hund: ['Herzinsuffizienz', 'Diabetes', ...],
  katze: ['Niereninsuffizienz', 'Hyperthyreose', ...],
  pferd: ['Kolik', 'Hufrehe', ...],
  kaninchen: ['E. cuniculi', 'Zahnprobleme', ...]
}

// Normal vital ranges
animalNormalValues = {
  hund: { 
    heartRate: [60, 140], 
    temperature: [37.5, 39.2],
    bloodPressure: [110, 160]
  },
  // ... other animals
}
```

### 3D Medical Visualization System
The 3D system extends the core game with advanced medical visualizations:
```javascript
// Medical visualization modes
const medicalModes = {
  normal: 'Standard appearance with original materials',
  xray: 'Fresnel-based transparency showing bone structure',
  ultrasound: 'Noise-based textures with scan-line effects',
  thermal: 'Temperature mapping with heat color gradients',
  mri: 'MRI-style grayscale with tissue differentiation'
}

// Interactive organ zones for Bello
const bellaInteractiveZones = [
  { name: 'head', organs: ['brain', 'eyes', 'ears'], radius: 0.6 },
  { name: 'chest', organs: ['heart', 'lungs'], radius: 0.8 },
  { name: 'abdomen', organs: ['stomach', 'liver', 'kidneys'], radius: 0.8 },
  { name: 'legs', organs: ['bones', 'joints', 'muscles'], radius: 1.2 }
]

// Progressive loading configuration
const modelQuality = {
  high: { polygons: '100%', textures: '2048px', use: 'close examination' },
  medium: { polygons: '50%', textures: '1024px', use: 'normal gameplay' },
  low: { polygons: '25%', textures: '512px', use: 'overview/mobile' }
}
```

## Deployment & Version Control

### Automatic Deployment
- **GitHub Actions**: Configured in `.github/workflows/deploy.yml`
- **Trigger**: Automatically deploys on push to `main` branch
- **Target**: https://vibecoding.company via FTP to Hostinger
- **Files Deployed**: Selected HTML versions (6 main variants) + auto-generated landing page

### Git Repository
```bash
# Remote: git@github.com:DorianGrey-Austria/tierarztapp.git

# After major changes, commit and push:
git add .
git commit -m "feat: Description of changes"
git push origin main
# This triggers automatic deployment
```

## Testing Protocol

### Browser Testing Requirements
When making significant changes to HTML files:
```bash
# 1. Start local server
python3 -m http.server 8080

# 2. Run automated browser testing checklist
python3 test-console-errors.py

# 3. Manual testing in browser (Chrome preferred)
# Check for console errors: Cmd+Option+J (Mac) or F12 (Windows/Linux)
# Test interactive elements, 3D visualization, form submissions

# 4. If port conflict:
kill $(lsof -t -i:8080)  # Kill existing server
python3 -m http.server 8081  # Use alternative port
```

### Common Issues & Solutions
- **Port conflicts**: Use ports 8081, 8082 if 8080 is busy
- **Browser cache**: Hard reload with Cmd+Shift+R or use incognito mode
- **Service Worker conflicts**: Test in incognito or clear site data
- **404 errors**: Ensure server is running and file paths are correct

## Blender MCP Integration

### 🎯 3D Workflow Pipeline (Advanced)
**Reference: [3dworkflowBlender.md](./3dworkflowBlender.md) for complete documentation**

#### Current Status
- ⏳ **Blender MCP Server**: Awaiting activation in Claude Desktop
- ✅ **Pipeline Architecture**: Fully documented and ready
- ✅ **Fallback System**: Working 3D viewer with procedural Bello model

#### When Blender MCP is Available
```python
# These commands will be available for direct Blender control:
scene_info = get_scene_info()                    # Get all objects in Blender scene
bello_info = get_object_info(object_name="Bello") # Get Bello model details
execute_blender_code(code="...")                  # Run Python code in Blender
screenshot = get_viewport_screenshot(max_size=1024) # Render current view

# Automated export pipeline will generate:
# - bello_high.glb (100% quality)
# - bello_medium.glb (50% quality)  
# - bello_low.glb (25% quality)
# - Medical material variants (X-Ray, Ultrasound, Thermal)
```

#### 3D Asset Integration Workflow
1. **Blender MCP connects** → Access to live Blender session
2. **Model validation** → Check Bello mesh integrity
3. **Multi-quality export** → Generate GLB files with compression
4. **Medical material creation** → Apply shader materials in Blender
5. **Automated testing** → Validate all exports
6. **Three.js integration** → Update web viewer
7. **Live deployment** → Push to vibecoding.company

## Version Information
- **Current Version**: 3.1.0 (Project) / 7.0.0 (3D Scanner)
- **React**: 18.2.0 with createRoot API  
- **Vite**: Configured for dev server (default port 5173)
- **Node**: Requires Node.js 18+
- **Three.js**: r128 (v7) - stable, r179 (React) - latest
- **Additional Dependencies**: Lucide React (icons), Tailwind CSS (styling), Playwright (testing)

## 📋 Version 7 Changelog (Bello 3D Scanner)

### ⚡ Version 7.0.0 - "Medical Scanner Pro" (2025-08-23)
**🚨 CRITICAL FIX: CDN Compatibility Issue**

#### 🛠️ **Technical Fixes**
- **CDN Repair**: Fixed broken Three.js r144 + mixed CDN providers
- **Compatibility**: Downgrade to proven Three.js r128 + official threejs.org CDNs  
- **Geometry Fix**: CapsuleGeometry → CylinderGeometry (r128 compatibility)
- **Loader Fix**: GLTFLoader, DRACOLoader, OrbitControls now load correctly

#### ✨ **Enhanced Features**
- **Medical Shaders**: Professional-grade X-Ray, Ultrasound, Thermal, MRI visualization
- **Progressive Loading**: Smart GLB file detection with graceful fallback
- **Enhanced Fallback Model**: Realistic procedural dog with snout, eyes, ears
- **Performance Monitoring**: Polygon counter, loading progress tracking
- **5 Scanner Modes**: Normal, X-Ray, Ultrasound, Thermal, MRI

#### 🏗️ **Architecture**
- **Version Management**: v7 (latest) + v6 (backup) system
- **Production Ready**: Console error-free, browser tested
- **Mobile Compatible**: Responsive design, touch controls

#### 🎯 **Status**
- **Recommended**: vetscan-detective.html (stable educational gameplay)
- **Latest 3D**: vetscan-bello-3d-v7.html (advanced medical visualization)  
- **Backup**: vetscan-bello-3d.html (previous version)

## Educational Features
The game includes several pedagogical elements:
- Comparison system showing normal vs. measured values
- Dr. Eule mentor character providing guidance
- Progressive difficulty levels
- Medical encyclopedia with 200+ animals
- Quiz system with explanations
- Achievement system to encourage learning

## Performance Considerations
- Standalone HTML files are optimized for direct browser execution
- No external dependencies in HTML versions (all code inline)
- React version uses Vite for fast HMR during development
- Deployment includes .htaccess for HTTPS forcing and compression