# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational veterinary medical scanner simulation game ("VetScan Pro 3000"). Live at https://vibecoding.company. GitHub: `DorianGrey-Austria/tierarztapp`.

Two parallel implementations:

- **Standalone HTML versions** (production): 38 self-contained game files in the repo root. Each includes all CSS/JS inline. These are what gets deployed via GitHub Actions FTP to Hostinger.
- **React app** (development target): Vite + React 18 + Tailwind CSS + Three.js in `src/`. The `dist/` build is NOT deployed -- only standalone HTML files go to production.

The root `index.html` is a standalone game file (not the React app entry point). `vetscan-version-selector.html` and the CI-generated `deploy/index.html` serve as navigation hubs.

The 43 HTML files fall into two groups:
- **19 professional learning tools** registered in the `js/vetscan-shared.js` TOOLS array (clinical-exam, ddx-trainer, bone-atlas, parasite-atlas, etc.) -- these use the shared module system and appear in the navigation bar.
- **24 legacy/game HTML files** (standalone.html, vetscan-detective.html, vetscan-magic-v8.html, etc.) -- fully self-contained, no shared modules.

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

# Blender integration tests (Python, requires Docker container running)
python3 -m pytest tests/blender_integration/
```

## Architecture

### React App (`src/`)

Entry point: `src/main.jsx` renders `VetScanUltraAdvanced` (imported from `src/VetScanUltraAdvanced.jsx`, ~36KB, supports 20 animal species). A second large component `AnimalScannerPro.jsx` (~26KB) exists at `src/` root level.

Vite config is minimal (`vite.config.js`): React plugin, strict port 8035, auto-open browser. Tailwind config (`tailwind.config.js`) has no custom theme extensions.

Key layers:
- **3D Viewer**: `components/BelloViewer.jsx` (Three.js 3D viewer), `components/InteractiveAnatomy.js` (organ click zones)
- **Model Loading**: `game/AnimalLoader.js` (progressive quality: high/medium/low with DRACO fallback), `game/MultiSpeciesLoader.js`, `game/BelloModel.js`
- **Medical Shaders**: `shaders/MedicalVisualization.js` (X-Ray, Ultrasound, Thermal, MRI modes), `shaders/AdvancedMedicalShaders.js`
- **Performance**: `engine/PerformanceManager.js` (also lives at `components/PerformanceManager.js`)

### Standalone Shared Modules (`js/`)

The 16 professional learning tools share runtime code via `<script>` tags:

- `js/vetscan-shared.js`: Navigation bar, localStorage progress tracking, dark mode, print support, design tokens (CSS variables). Contains the canonical TOOLS registry (IDs, filenames, categories) -- this is the **source of truth** for all tool metadata. Exposes a global `VetScan` object with `getProgress()`, `saveProgress(toolId, data)`, `saveScore(toolId, score, maxScore)`, `getToolProgress(toolId)`.
- `js/vetscan-pro.js`: Professional polish layer -- toast notifications, keyboard shortcuts, ARIA/WCAG enhancements (44px touch targets, focus-visible, prefers-reduced-motion), service worker registration. Must be loaded **after** `vetscan-shared.js`.
- `js/hyper3d-animals.js`: Animal data for the 3D viewer and showcase HTML files.

### Game Data

`veterinary-medical-data.js` (root, ~51KB): Central medical database -- 20 species, 100+ patient profiles, medical conditions by severity, anatomy point mappings, breed-specific vital signs. Shared by both React and standalone versions.

### 3D Assets (`assets/models/`)

Seven model categories:
- `animals/<species>/` -- 31 species directories with quality tiers (`_high.glb`, `_medium.glb`, `_low.glb`) plus medical variants (`_medical.glb`, `_xray.glb`)
- `organs/` -- Individual organ models (heart, brain, liver, lungs, kidney, etc.)
- `pathology/` -- 30 pathology-specific models in subdirectories (fracture, hip-dysplasia, hcm-heart, pancreatitis, etc.)
- `instruments/` -- Medical instruments (stethoscope, syringe, thermometer, ultrasound-probe, etc.)
- `bones/` -- 20 skeletal models (dog/cat/horse/cow/rabbit skulls, long bones, spine segments, 3 orthopedic implants)
- `parasites/` -- 10 parasite models (roundworm, tapeworm, flea, tick, heartworm, hookworm, coccidia, giardia, ear/sarcoptic mites)
- `special/` -- Life stage models (puppy, kitten, foal, pregnant variants, embryo)

The loader falls back to procedural Three.js geometry if GLB files fail to load.

### Blender MCP Pipeline

Runs in Docker (`docker-compose.yml`): headless Blender with virtual display on ports 8765 (WebSocket) and 8080 (health endpoint). Uses `uvx blender-mcp` (Python package via uvx), NOT npm/npx. Automation scripts in `scripts/` handle model creation, export, and health checking.

**Important**: `.cursorrules` contains Blender MCP instructions written for Cursor IDE that reference direct tool calls like `execute_blender_code()` and `get_scene_info()`. Claude Code does NOT have MCP tool access to Blender -- it can only start the Docker container and run scripts against it. Ignore the `.cursorrules` directives about direct Blender access.

### Service Worker (`sw.js`)

Cache name: `vetscan-pro-v1`. Strategy: cache-first for `.glb` models (stable assets), network-first for HTML/JS/CSS. Provides offline support for all learning tools and 3D models.

### Deployment

GitHub Actions (`.github/workflows/deploy.yml`) on push to `main`:
1. Copies standalone HTML files + `assets/` + `public/` + `js/` + `sw.js` into `deploy/`
2. Generates a version-selector `index.html` with links to all game variants
3. Creates `.htaccess` (HTTPS redirect, gzip, GLB MIME types, caching headers)
4. FTP-deploys to Hostinger (`/public_html/`)

Requires secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`.

**When adding a new HTML file**: you must also add a `cp <file>.html deploy/` line in the deploy workflow, or it won't reach production.

## Ports

| Port | Service |
|------|---------|
| 8035 | Vite dev server (React app) |
| 8080 | Python HTTP server / Blender MCP health |
| 8765 | Blender MCP WebSocket |

## Important Conventions

- Standalone HTML games are self-contained -- do not add external dependencies. The only shared scripts are in `js/` (loaded via relative `<script src="js/...">` tags).
- **Adding a new professional learning tool requires three steps:**
  1. Register in `js/vetscan-shared.js` TOOLS array (id, name, file, icon, category)
  2. Add `cp <file>.html deploy/` line in `.github/workflows/deploy.yml`
  3. Include shared module script tags: `<script src="js/vetscan-shared.js"></script>` then `<script src="js/vetscan-pro.js"></script>`
- Quality tier naming: `<species>_high.glb` (original), `<species>_medium.glb` (50% decimation), `<species>_low.glb` (25% decimation).
- `.env.example` documents available config vars (Blender path, API keys, ports).
- `scripts/` contains 50+ Python/JS/shell scripts primarily for Blender model creation and export. Most are single-purpose automation scripts, not part of the app runtime.
- No Playwright config file exists in the repo root -- the `test:integration` npm script calls `playwright test --grep` directly. Install Playwright browsers with `npx playwright install` before first run.
