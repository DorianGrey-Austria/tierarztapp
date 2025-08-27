# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
Educational veterinary medical scanner simulation game with multiple implementations:
- **Standalone HTML versions**: Self-contained files requiring no build process
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **3D Model Integration**: Three.js-based visualization with medical shaders
- **Auto-deployment**: Pushes to main branch deploy to https://vibecoding.company via GitHub Actions

## Development Commands
```bash
# React development
npm install                    # Install dependencies
npm run dev                    # Start dev server on port 3000 (auto-opens browser)
npm run build                  # Build for production
npm run preview                # Preview production build

# 3D workflow
npm run optimize:model         # Optimize GLB models
npm run generate:shaders       # Generate medical shaders
npm run test:integration -- --grep <pattern>  # Run specific tests
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
./docker-start.sh              # Start Blender MCP services
docker-compose ps              # Check container status
docker-compose logs -f blender-mcp  # View logs
docker-compose down            # Stop services
```


## Architecture
### React Components
- `src/main.jsx`: Entry point
- `src/VetScanUltraAdvanced.jsx`: Main game component
- `src/components/BelloViewer.jsx`: 3D model viewer
- `src/game/AnimalLoader.js`: Progressive model loading with quality levels and fallbacks
- `src/shaders/MedicalVisualization.js`: Medical visualization modes (X-Ray, Ultrasound, Thermal, MRI)

### Game Data
`veterinary-medical-data.js` contains 20 animal species with 100 individual patients, including patient profiles, symptom sets, vital ranges, and 3D model configurations.

### Key Scripts
- `scripts/blender-mcp-health-check.py`: Test Blender MCP connection
- `scripts/blender_auto_export.py`: Automated GLB export
- `docker-start.sh`: Initialize Docker-based 3D pipeline

## Deployment

```bash
git add .
git commit -m "feat: Your changes"
git push origin main
# Automatically deploys to https://vibecoding.company via GitHub Actions
```

Deployment is configured in `.github/workflows/deploy.yml` and triggers on push to main branch.

## 3D Model System

Models are loaded progressively from high to low quality with automatic fallback to procedural models. The AnimalLoader class handles model loading, medical visualization modes, and interactive zones.

Visualization modes: Normal, X-Ray, Ultrasound, Thermal, MRI

## Blender MCP Integration

Blender MCP runs in Docker container on port 8765 (WebSocket) and 8080 (health check). Use `./docker-start.sh` to start services. Health check: `python3 scripts/blender-mcp-health-check.py`


## Port Configuration
- **3000**: React dev server (Vite)
- **8080**: Python HTTP server / Docker health check
- **8765**: Blender MCP WebSocket
- **8081**: Alternative Python server

## Testing

No formal test framework configured. Testing is done via:
- Browser console for runtime errors
- `npm run test:integration` for Playwright tests (when available)
- Manual testing with Python HTTP server