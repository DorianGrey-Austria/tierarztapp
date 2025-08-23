# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 💡 Claude Code Professional Tips
For advanced workflows and productivity tips, see [Claude-Tipps.md](./Claude-Tipps.md)  
**Note**: These are optional recommendations to enhance productivity - adapt them to your workflow.

## Project Overview
VetScan Pro 3000 - Educational veterinary medical scanner simulation game with multiple implementations:
- **Standalone HTML versions**: 10+ self-contained HTML files requiring no build process
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **3D Model Integration**: Advanced 3D pipeline with Blender MCP integration
- **Live Deployment**: Automatically deployed to https://vibecoding.company via GitHub Actions

## Development Commands

### React Version
```bash
npm install                    # Install dependencies
npm run dev                    # Start dev server at http://localhost:3000
npm run build                  # Build for production
npm run preview                # Preview production build
```

### Standalone HTML Versions
```bash
python3 -m http.server 8080    # Start local server
# Access: http://localhost:8080/[filename].html

# Alternative port if 8080 is busy:
python3 -m http.server 8081
```

### 3D Workflow Commands
```bash
# Test Blender MCP connection
node scripts/test-mcp-connection.js

# Run 3D asset pipeline
./scripts/deploy-animal.sh

# Generate medical visualization shaders
npm run generate:shaders -- --model=bello

# Validate 3D model exports
npm run test:integration -- --model=bello

# Manual browser testing
python3 test-console-errors.py
```

## Architecture & File Structure

### HTML Versions Priority
**Production Versions:**
- `vetscan-detective.html` - 🎯 **RECOMMENDED**: Educational detective gameplay with Dr. Eule mentor
- `standalone.html` - 🛡️ **STABLE**: Most stable base version

**3D Scanner Versions:**
- `vetscan-bello-3d-v7.html` - ⚡ **VERSION 7**: Latest 3D with medical shaders (X-Ray, Ultrasound, Thermal, MRI)
- `vetscan-bello-3d.html` - 📦 **BACKUP**: Previous 3D version (v6)

**Story & Campaign Versions:**
- `vetscan-story-mode.html` - Story campaign with Dr. Sarah Miller
- `vetgame-missions.html` - Mission-based gameplay
- `vetscan-professional.html` - Professional medical simulation
- `vetscan-pro-leveling.html` - Level 1-50 RPG progression
- `vetscan-advanced.html` - Advanced medical features
- `vetscan-premium.html` - Premium UI version

**System Files:**
- `index.html` - Landing page with version selector (auto-generated on deployment)

### Core Game Data Structures
```javascript
// Shared disease presets
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
  }
  // ... other animals
}

// 3D Medical visualization modes
const medicalModes = {
  normal: 'Standard appearance',
  xray: 'Fresnel-based transparency',
  ultrasound: 'Noise-based textures',
  thermal: 'Temperature mapping',
  mri: 'Grayscale tissue differentiation'
}
```

## Deployment Process

### GitHub Actions Workflow
- **Trigger**: Push to `main` branch or manual workflow dispatch
- **Target**: https://vibecoding.company via FTP to Hostinger
- **Files Deployed**: Selected HTML versions + auto-generated landing page
- **Configuration**: `.github/workflows/deploy.yml`

### Manual Deployment
```bash
git add .
git commit -m "feat: Description of changes"
git push origin main
# Triggers automatic deployment
```

## Testing Requirements

### Browser Console Testing
```bash
# Start local server
python3 -m http.server 8080

# Run automated testing checklist
python3 test-console-errors.py

# Manual browser testing (Chrome preferred)
# Check console: Cmd+Option+J (Mac) or F12 (Windows/Linux)
# Test: Interactive elements, 3D visualization, form submissions
```

### Common Fixes
- **Port conflicts**: Use 8081, 8082 if 8080 busy
- **Kill existing server**: `kill $(lsof -t -i:8080)`
- **Browser cache**: Hard reload with Cmd+Shift+R
- **Service Worker conflicts**: Test in incognito mode

## Blender MCP Integration

### Setup Requirements
When Blender MCP becomes available in Claude Desktop:
```bash
# Install Blender MCP
uvx blender-mcp

# Test connection
node scripts/test-mcp-connection.js
```

### 3D Pipeline Commands (When Active)
```python
scene_info = get_scene_info()                    # Get Blender scene objects
bello_info = get_object_info("Bello")           # Get Bello model details
execute_blender_code(code="...")                # Run Python in Blender
screenshot = get_viewport_screenshot(max_size=1024)  # Render current view
```

### Export Pipeline Output
- `bello_high.glb` - 100% quality, 2048px textures
- `bello_medium.glb` - 50% quality, 1024px textures
- `bello_low.glb` - 25% quality, 512px textures
- Medical material variants (X-Ray, Ultrasound, Thermal, MRI)

## Version 7 Technical Details

### ⚠️ WICHTIG: Versionsnummern bei jedem Deployment
**Bei JEDEM Deployment MUSS die Versionsnummer erhöht werden!**
- **Format**: Major.Minor.Patch (z.B. 7.0.2)
- **Build**: YYYY.MM.DD.XXX (z.B. 2025.08.23.002)
- **Orte zum Updaten**:
  1. HTML `<title>` Tag
  2. Header im HTML Body
  3. JavaScript `const VERSION`
  4. JavaScript `const BUILD`
  5. Status Badge im UI
  6. Debug Info Panel

### CDN Configuration
- **Three.js**: r128 from unpkg CDN (funktioniert garantiert!)
- **Loaders**: GLTFLoader, DRACOLoader, OrbitControls
- **Compatibility**: Using unpkg instead of cdnjs (cdnjs lacks example files)

### Progressive Loading System
1. Attempts to load high-quality GLB first
2. Falls back to medium, then low quality
3. If no GLB available, uses procedural fallback model
4. Performance monitoring with polygon counter

### Medical Visualization Shaders
- **X-Ray**: Fresnel-based transparency with bone highlighting
- **Ultrasound**: Noise patterns with scan-line effects
- **Thermal**: Temperature gradient mapping
- **MRI**: Grayscale tissue differentiation
- **Normal**: Standard materials with realistic textures

## Performance Optimization

### Standalone HTML Files
- All code inline (no external dependencies)
- Optimized for direct browser execution
- .htaccess configured for HTTPS and compression

### React Version
- Vite for fast HMR during development
- Code splitting for production builds
- Lazy loading for heavy components

### 3D Assets
- Progressive quality loading based on device capabilities
- DRACO compression for GLB files
- Texture optimization per quality level

## Educational Features
- Dr. Eule mentor character providing guidance
- Comparison system showing normal vs. measured values
- Progressive difficulty levels
- Medical encyclopedia with 200+ animals
- Quiz system with explanations
- Achievement system encouraging learning