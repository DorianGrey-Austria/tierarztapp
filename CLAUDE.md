# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
VetScan Pro 3000 - An educational veterinary medical scanner simulation game with multiple HTML implementations:
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **Standalone HTML versions**: 10 self-contained HTML files requiring no build process
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

## Project Architecture

### Standalone HTML Versions (Primary Focus)
Each HTML file is completely self-contained with all code inline:
- **vetscan-detective.html** - 🎯 RECOMMENDED: Educational detective gameplay with Dr. Eule mentor
- **standalone.html** - Most stable base version, failsafe implementation
- **vetscan-ultimate.html** - 3D visualization with Three.js and career mode
- **vetscan-story-mode.html** - Story campaign with Dr. Sarah Miller
- **vetgame-missions.html** - Mission-based gameplay variant
- **vetscan-professional.html** - Professional medical simulation
- **vetscan-pro-leveling.html** - Level 1-50 progression with RPG elements
- **vetscan-advanced.html** - Advanced medical features
- **vetscan-premium.html** - Premium UI version with modern design
- **index.html** - Landing page with version selector (auto-generated on deployment)

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

# 2. Test in browser (Chrome preferred)
# Check for console errors: Cmd+Option+J
# Fix any JavaScript errors before proceeding

# 3. If port conflict:
kill $(lsof -t -i:8080)  # Kill existing server
python3 -m http.server 8081  # Use alternative port
```

### Common Issues & Solutions
- **Port conflicts**: Use ports 8081, 8082 if 8080 is busy
- **Browser cache**: Hard reload with Cmd+Shift+R or use incognito mode
- **Service Worker conflicts**: Test in incognito or clear site data
- **404 errors**: Ensure server is running and file paths are correct

## Version Information
- **Current Version**: 3.1.0
- **React**: 18.2.0 with createRoot API
- **Vite**: Configured for port 3000 with auto-open
- **Node**: Requires Node.js 18+

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