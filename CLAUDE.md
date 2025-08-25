# CLAUDE.md - VetScan Pro 3000 Development Guide
**Updated: 25.08.2025 - Nach Blender MCP Durchbruch**

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
VetScan Pro 3000 - Educational veterinary medical scanner simulation game with multiple implementations:
- **12 Standalone HTML versions**: Self-contained files requiring no build process
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS  
- **3D Model Integration**: Advanced pipeline with Blender MCP integration and medical shaders
- **Live Deployment**: Auto-deployed to https://vibecoding.company via GitHub Actions

## Development Commands

### React Version (Port 3000)
```bash
npm install                    # Install dependencies
npm run dev                    # Start dev server (auto-opens browser)
npm run build                  # Build for production
npm run preview                # Preview production build
```

### Standalone HTML Testing
```bash
python3 -m http.server 8080    # Start local server
# Access: http://localhost:8080/[filename].html

# Alternative port if 8080 is busy:
python3 -m http.server 8081

# Kill existing server:
kill $(lsof -t -i:8080)
```

### 3D Workflow Commands
```bash
# Docker-based Blender MCP
./docker-start.sh              # Start full 3D pipeline
docker-compose ps              # Check status
docker-compose logs -f blender-mcp  # View logs
docker-compose down            # Stop services

# Scripts
npm run generate:shaders       # Generate medical shaders
npm run optimize:model         # Optimize 3D models
npm run test:integration -- --grep bello  # Run tests
```

## Key HTML Versions
1. **`vetscan-bello-3d-v7.html`** - Latest 3D with medical visualization modes
2. **`vetscan-detective.html`** - Educational detective gameplay (RECOMMENDED)
3. **`standalone.html`** - Most stable base version
4. **`vetscan-story-mode.html`** - Story campaign mode
5. **`vetscan-ultimate.html`** - 3D with career mode

## Architecture

### React Components
```
src/
├── main.jsx                   # Entry point
├── VetScanUltraAdvanced.jsx   # Main game component
├── components/
│   └── BelloViewer.jsx        # 3D model viewer
├── game/
│   ├── AnimalLoader.js        # Model loading with fallbacks
│   └── BelloModel.js          # Bello-specific logic
└── shaders/
    └── MedicalVisualization.js # Medical shaders
```

### Game Data (`veterinary-medical-data.js`)
- **20 Animal Species**: 100 individual patients
  - Level 1 (Ages 6-10): 10 pets → 60 patients
  - Level 2 (Ages 10-14): 10 animals → 40 patients
- Each species includes: patient profiles, symptom sets, vital ranges, 3D model config

### Python Scripts
- **Blender Export**: `bello_export_system.py`, `blender_auto_export.py`
- **Medical Visualization**: `medical-shaders.py`, `bello_medical_visualization.py`
- **MCP Server**: `blender-mcp-server.py`, `websocket-mcp-bridge.py`

## Deployment

### Auto-Deployment to Production
```bash
git add .
git commit -m "feat: Your changes"
git push origin main
# Automatically deploys to https://vibecoding.company
```

**Deployment Config**: `.github/workflows/deploy.yml`
- Triggers on push to `main`
- Deploys selected HTML files via FTP
- Auto-generates index.html landing page

### Version Updates (Required on Deployment)
Update version in:
1. HTML `<title>` tag
2. Header text in body
3. JavaScript `const VERSION`
4. JavaScript `const BUILD` (format: YYYY.MM.DD.XXX)

## 3D Model System

### Progressive Loading
1. Try `bello_high.glb` (2048px textures)
2. Fallback to `bello_medium.glb` (1024px)
3. Fallback to `bello_low.glb` (512px)
4. Use procedural model if no GLB available

### Medical Visualization Modes
- **Normal**: Standard realistic materials
- **X-Ray**: Fresnel transparency with bone highlighting
- **Ultrasound**: Noise patterns with scan lines
- **Thermal**: Temperature gradient mapping
- **MRI**: Grayscale tissue differentiation

### CDN Configuration
- Three.js r128 from unpkg.com
- Includes: GLTFLoader, DRACOLoader, OrbitControls

## 🎯 Blender MCP Integration - KRITISCHE REGELN

### ✅ WAS FUNKTIONIERT (Nach 25.08.2025 Durchbruch):
1. **MCP Konfiguration:** `.cursor/mcp.json` mit `uvx` command
2. **Port:** 9876 (WebSocket-Verbindung)
3. **Capabilities:**
   - Objekte erstellen ✅
   - Materialien ändern ✅
   - Transformationen ✅
   - Scene-Manipulation ✅
4. **Export:** Manuell via `BLENDER-EXPORT-MANUAL.py`

### ❌ NIEMALS WIEDER DIESE FEHLER:
```bash
# FALSCH - Öffnet neue Instanz (2GB RAM!)
subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender", "--python"])

# FALSCH - Wrong package manager
"command": "npx", "args": ["blender-mcp"]  # blender-mcp ist NICHT auf npm!

# FALSCH - Wrong config file
.cursor/settings.json  # Nutze .cursor/mcp.json!
```

### ✅ RICHTIGER WORKFLOW:
1. Blender GUI läuft bereits (PID finden mit `ps aux | grep Blender`)
2. MCP Addon aktiviert (N-Key → BlenderMCP Tab)
3. Cursor nutzt `.cursor/mcp.json` mit `uvx`
4. Kreative Änderungen via MCP
5. Export via Script in Blender

### Docker Setup
```yaml
# docker-compose.yml services:
- blender-mcp: Port 8765 (WebSocket), 8080 (Health)
- xvfb: Optional debug profile
```

## Testing & Debugging

### Browser Testing
- Chrome preferred (Cmd+Option+J for console)
- Hard reload: Cmd+Shift+R
- Test in incognito for service worker issues

### Common Fixes
- Port conflicts: Try 8081, 8082
- Cache issues: Hard reload browser
- Console errors: Check browser dev tools

## Port Configuration
- **3000**: React dev server (Vite)
- **8080**: Python HTTP server / Docker health check
- **8081**: Alternative Python server
- **8765**: Blender MCP WebSocket

## Notes
- No linting configured - rely on browser testing
- React version not auto-deployed (requires separate build)
- BMAD Method installed but core files pending