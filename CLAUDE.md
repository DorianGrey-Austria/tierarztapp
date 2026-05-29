# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational veterinary medical scanner simulation game ("VetScan Pro") with two parallel implementations:

- **Standalone HTML versions** (production): 20+ self-contained game files in the repo root (`vetscan-detective.html`, `vetscan-magic-v8.html`, `standalone.html`, etc.). Each includes all CSS/JS inline with no external dependencies. These are what gets deployed to https://vibecoding.company via GitHub Actions FTP to Hostinger.
- **React app** (development target): Vite + React 18 + Tailwind CSS + Three.js in `src/`. The `dist/` build output is NOT deployed -- only standalone HTML files go to production.

The root `index.html` is also a standalone game file (not the React app entry point). `vetscan-version-selector.html` and the CI-generated `deploy/index.html` serve as navigation hubs between game versions.

## Development Commands

```bash
# React app
npm install          # Install dependencies
npm run dev          # Managed Vite dev server on port 8035 (via port-manager.sh, auto-opens browser)
npm run dev:raw      # Direct Vite dev server on 8035 (bypasses port-manager)
npm run dev:stop     # Stop the registered app service
npm run build        # Production build to dist/
npm run preview      # Preview production build on 8035

# Standalone HTML testing
python3 -m http.server 8080   # Serve root dir, then access localhost:8080/<file>.html

# 3D pipeline
npm run optimize:model         # gltf-transform GLB optimization
npm run generate:shaders       # Generate medical shader files (scripts/generate-shaders.js)

# Blender MCP (Docker)
./docker-start.sh              # Start Blender MCP container
docker-compose ps              # Check status
python3 scripts/blender-mcp-health-check.py   # Health check (outputs JSON)

# Integration tests (Playwright -- requires a grep pattern argument)
npm run test:integration -- "pattern"
```

## Architecture

### React App (`src/`)

Entry point: `src/main.jsx` renders `VetScanUltraAdvanced` (the main game component, 36k, supports 20 animal species). A second large component `AnimalScannerPro.jsx` (26k) exists at `src/` root level.

Key layers:
- **3D Viewer**: `components/BelloViewer.jsx` (Three.js 3D viewer), `components/InteractiveAnatomy.js` (organ click zones)
- **Model Loading**: `game/AnimalLoader.js` (progressive quality: high/medium/low with DRACO fallback), `game/MultiSpeciesLoader.js`, `game/BelloModel.js`
- **Medical Shaders**: `shaders/MedicalVisualization.js` (X-Ray, Ultrasound, Thermal, MRI modes), `shaders/AdvancedMedicalShaders.js`
- **Performance**: `engine/PerformanceManager.js` (also lives at `components/PerformanceManager.js`)

### Game Data

`veterinary-medical-data.js` (root, 51k): Central medical database -- 20 species, 100+ patient profiles, medical conditions by severity, anatomy point mappings, breed-specific vital signs. Shared by both React and standalone versions.

`js/hyper3d-animals.js`: Additional animal data used by some standalone HTML versions (deployed alongside them).

### 3D Model Pipeline

Models in `assets/models/animals/<species>/` (currently: bello, cat, dog, parrot, rabbit) with quality tiers (`_high.glb`, `_medium.glb`, `_low.glb`) plus medical variants (`_medical.glb`, `_xray.glb`). Bello also has a `.blend` source file. The loader falls back to procedural geometry if GLB files fail to load.

The Blender MCP pipeline runs in Docker (`docker-compose.yml`): headless Blender with virtual display on ports 8765 (WebSocket) and 8080 (health endpoint). Blender MCP uses `uvx blender-mcp` (Python package via uvx), NOT npm/npx. Extensive automation scripts in `scripts/` handle model creation, export, and health checking.

### Deployment

GitHub Actions (`.github/workflows/deploy.yml`) on push to `main`:
1. Copies standalone HTML files + `assets/` + `public/` + `js/` into `deploy/`
2. Generates a version-selector `index.html` with links to all game variants
3. FTP-deploys to Hostinger (`/public_html/`)

Requires secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.

## Ports

| Port | Service |
|------|---------|
| 8035 | Vite dev server (React app) |
| 8080 | Python HTTP server / Blender MCP health |
| 8765 | Blender MCP WebSocket |

## Important Conventions

- Standalone HTML games are self-contained -- each file includes all CSS/JS inline. Do not add external dependencies to them.
- `.cursorrules` contains Blender MCP integration instructions for Cursor IDE -- not relevant for Claude Code.
- `.env.example` documents available config vars (Blender path, API keys, ports).
- `scripts/` contains 50+ Python/JS/shell scripts primarily for Blender model creation and export. Most are single-purpose automation scripts, not part of the app runtime.
