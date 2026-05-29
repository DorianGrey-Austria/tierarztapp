# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project Overview

Educational veterinary medical scanner simulation game ("VetScan Pro") with two parallel implementations:
- **Standalone HTML versions**: 20+ self-contained game files in the repo root (detective, story-mode, pro-leveling, etc.) — each is a single HTML file that runs directly in a browser
- **React app**: Vite + React 18 + Tailwind CSS + Three.js in `src/` — the main development target for 3D features

Auto-deploys to https://vibecoding.company on push to `main` via GitHub Actions FTP to Hostinger.

## Development Commands

```bash
# React app
npm install          # Install dependencies
npm run dev          # Managed Vite dev server on port 8035 (auto-opens browser)
npm run dev:raw      # Direct Vite dev server on 8035
npm run dev:stop     # Stop only the registered app service
npm run build        # Production build to dist/
npm run preview      # Preview production build

# Standalone HTML testing
python3 -m http.server 8080   # Serve root dir, access at localhost:8080/<file>.html

# 3D pipeline
npm run optimize:model         # gltf-transform GLB optimization
npm run generate:shaders       # Generate medical shader files

# Blender MCP (Docker)
./docker-start.sh              # Start Blender MCP container
docker-compose ps              # Check status
python3 scripts/blender-mcp-health-check.py   # Health check (outputs JSON)
```

**Note:** `npm run test:integration` is defined as `playwright test --grep` which requires a pattern argument: `npm run test:integration -- "pattern"`.

## Architecture

### React App (`src/`)

Entry point: `src/main.jsx` renders `VetScanUltraAdvanced` (the main game component, supports 20 animal species).

Key layers:
- **Components**: `BelloViewer.jsx` (Three.js 3D viewer), `InteractiveAnatomy.js` (organ interaction)
- **Game logic**: `game/AnimalLoader.js` (progressive model loading: high/medium/low quality with DRACO), `game/MultiSpeciesLoader.js`
- **Shaders**: `shaders/MedicalVisualization.js` (X-Ray, Ultrasound, Thermal, MRI modes), `shaders/AdvancedMedicalShaders.js`
- **Engine**: `engine/PerformanceManager.js` (runtime optimization)

### Game Data

`veterinary-medical-data.js` (root): Central medical database — 20 species, 100+ patient profiles, medical conditions by severity, anatomy point mappings, breed-specific vital signs. Shared by both React and standalone versions.

### 3D Model Pipeline

Models live in `assets/models/animals/<species>/` with quality tiers (`_high.glb`, `_medium.glb`, `_low.glb`) plus medical variants (`_medical.glb`, `_xray.glb`). The loader falls back to procedural generation if GLB files fail to load.

The Blender MCP pipeline runs in Docker (`docker-compose.yml`): headless Blender on ports 8765 (WebSocket) and 8080 (health). Extensive automation scripts in `scripts/` handle export, generation, and health checking.

**Critical**: Blender MCP uses `uvx blender-mcp` (Python package via uvx), NOT npm/npx.

### Deployment

GitHub Actions (`.github/workflows/deploy.yml`) copies standalone HTML files, `assets/`, `public/`, and `js/` to a `deploy/` folder, generates a version-selector `index.html`, and FTP-deploys to Hostinger. Requires `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` secrets. The React app's `dist/` build is NOT deployed — only the standalone HTML versions go to production.

## Ports

| Port | Service |
|------|---------|
| 3000 | Vite dev server |
| 8080 | Python HTTP server / Blender MCP health |
| 8765 | Blender MCP WebSocket |

## Important Conventions

- Standalone HTML games are self-contained — each file includes all CSS/JS inline. Do not add external dependencies to them.
- The `vetscan-version-selector.html` and the generated `index.html` in deploy serve as navigation hubs between game versions.
- `.cursorrules` grants full Blender MCP access with no confirmation prompts — relevant for Cursor IDE, not Codex.
- `.env.example` documents available config vars (Blender path, API keys, ports).
