# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Educational veterinary medical scanner simulation game with multiple implementations:
- **Standalone HTML versions**: Self-contained files requiring no build process (multiple versions: detective, ultimate, story-mode, etc.)
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **3D Model Integration**: Three.js-based visualization with medical shaders and progressive loading
- **Auto-deployment**: Pushes to main branch deploy to https://vibecoding.company via GitHub Actions

## Development Commands
```bash
# React development
npm install                    # Install dependencies
npm run dev                    # Start dev server on port 3000 (auto-opens browser)
npm run build                  # Build for production
npm run preview                # Preview production build

# 3D workflow
npm run optimize:model         # Optimize GLB models using gltf-transform
npm run generate:shaders       # Generate medical shaders
npm run test:integration -- --grep <pattern>  # Run Playwright tests with pattern
```

```bash
# Standalone HTML testing
python3 -m http.server 8080    # Start local server
# Access: http://localhost:8080/[filename].html

# Alternative port if 8080 is busy:
python3 -m http.server 8081

# Kill existing server:
kill $(lsof -t -i:8080)
```

```bash
# Docker-based 3D pipeline
./docker-start.sh              # Start Blender MCP services (comprehensive startup script)
docker-compose ps              # Check container status
docker-compose logs -f blender-mcp  # View logs
docker-compose down            # Stop services
```

## Architecture
### React Components
- `src/main.jsx`: Entry point with React 18
- `src/VetScanUltraAdvanced.jsx`: Main game component with 20 animal species support
- `src/components/BelloViewer.jsx`: 3D model viewer with Three.js integration
- `src/components/InteractiveAnatomy.js`: Anatomy interaction system
- `src/game/AnimalLoader.js`: Progressive model loading (high/medium/low quality) with DRACO compression
- `src/game/MultiSpeciesLoader.js`: Multi-animal loading system
- `src/shaders/MedicalVisualization.js`: Medical visualization modes (X-Ray, Ultrasound, Thermal, MRI)
- `src/shaders/AdvancedMedicalShaders.js`: Advanced shader system
- `src/engine/PerformanceManager.js`: Performance optimization

### Game Data Architecture
`veterinary-medical-data.js`: Comprehensive medical database with:
- 20 animal species (pets, livestock, exotic animals)
- 100+ individual patient profiles with personality traits
- Medical conditions categorized by severity (emergency, routine, chronic)
- 3D model configurations with anatomy point mapping
- Breed-specific vital sign ranges

### Key Scripts and Utilities
- `scripts/blender-mcp-health-check.py`: Test Blender MCP connection with JSON health reports
- `scripts/blender_auto_export.py`: Automated GLB export with quality levels
- `scripts/generate-shaders.js`: Medical shader generation
- `scripts/blender_mcp_animal_generator.py`: Procedural animal generation
- `docker-start.sh`: Comprehensive Docker startup with health checks

## Deployment System

```bash
git add .
git commit -m "feat: Your changes"
git push origin main
# Automatically deploys to https://vibecoding.company via GitHub Actions
```

**Deployment Configuration:**
- **GitHub Actions**: `.github/workflows/deploy.yml` handles FTP deployment to Hostinger
- **Multi-version deployment**: Copies all HTML versions (standalone, detective, ultimate, story-mode, etc.)
- **Asset pipeline**: Includes JS, assets, public directories
- **Security headers**: .htaccess with compression, caching, and security headers
- **Performance**: DRACO compression enabled for 3D models

## 3D Model System Architecture

**Progressive Loading System:**
- High quality models: Full detail with DRACO compression
- Medium quality: 50% polygon reduction
- Low quality: 25% polygon reduction
- Fallback: Procedural generation if models fail to load

**Model Storage Structure:**
```
assets/models/animals/
├── bello/ (primary test animal)
│   ├── bello_high.glb
│   ├── bello_medium.glb
│   ├── bello_low.glb
│   ├── bello_medical.glb
│   └── bello_xray.glb
├── cat/, dog/, horse/, rabbit/ (various quality levels)
└── fallbacks/ (procedural models)
```

**Medical Visualization Modes:**
- Normal: Standard rendering
- X-Ray: Fresnel-based transparency with emission
- Ultrasound: Wave-based visualization
- Thermal: Heat mapping
- MRI: Cross-sectional views

## Blender MCP Integration

**Docker Architecture:**
- **Container**: `vetscan_blender_mcp` runs on port 8765 (WebSocket) and 8080 (health check)
- **Volumes**: Model exports, Blender projects, custom scripts
- **Environment**: Headless Blender with virtual display
- **Health checks**: Automated container health monitoring

**MCP Configuration** (`.cursor/mcp.json`):
- **blender-mcp**: Uses `uvx blender-mcp` (Python package, not npm)
- **filesystem**: Project file access
- **git**: Version control operations
- **memory**: Persistent context storage

**Key MCP Tools:**
- `execute_blender_code()`: Run Python scripts in Blender
- `get_scene_info()`: Scene object information
- `get_viewport_screenshot()`: Visual validation
- `generate_hyper3d_model_via_text()`: Text-to-3D generation

## Port Configuration
- **3000**: React dev server (Vite)
- **8080**: Python HTTP server / Docker health check
- **8765**: Blender MCP WebSocket (primary)
- **8081**: Alternative Python server
- **5900**: VNC port for debug containers

## Testing Strategy

**Testing Methods:**
- **Browser console**: Runtime error detection
- **Playwright**: Integration testing with `npm run test:integration`
- **Python server**: Manual testing of standalone HTML versions
- **Health checks**: Automated Blender MCP connection testing

**Test Files:**
- `tests/blender_integration/`: Blender MCP integration tests
- `test-results/`: Integration test results
- Health check logs: `blender_mcp_health_*.json`

## MCP Integration Details

**Critical Configuration Notes:**
- **Blender MCP**: MUST use `uvx blender-mcp` (Python package via uvx, not npm)
- **Auto-approval**: Extensive list of pre-approved MCP operations
- **Project root**: `/Users/doriangrey/Desktop/coding/tierarztspiel`
- **Blender path**: `/Applications/Blender.app/Contents/MacOS/Blender`

## BMAD Method Framework

**AI-Driven Development System:**
- **Installation**: `npx bmad-method install` (v4.40.0 successfully installed)
- **Expansion packs**: 2D game dev, Unity, creative writing, DevOps
- **Agents**: Product Owner, Scrum Master, Developer, Tester, Architect
- **Commands**: `npx bmad-method list:expansions`, `npx bmad-method status`

## Dependencies and Technology Stack

**Core Technologies:**
- React 18.2.0 with Vite 5.1.0
- Three.js 0.179.0 for 3D rendering
- Tailwind CSS with PostCSS and Autoprefixer
- DRACO 3D compression for model optimization
- Lucide React for UI icons

**Development Tools:**
- gltf-transform for model optimization
- Playwright for integration testing
- Docker for Blender MCP containerization
- GitHub Actions for CI/CD