# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview
VetScan Pro 3000 - A veterinary medical scanner simulation game with multiple implementations:
- **React version**: Full-featured app using Vite, React 18, and Tailwind CSS
- **Standalone versions**: Self-contained HTML files requiring no build process

## Development Commands

### React Version (Primary)
```bash
npm install           # Install dependencies
npm run dev          # Start dev server at http://localhost:3000
npm run build        # Build for production
npm run preview      # Preview production build
```

### Standalone Versions (No Build Required)
```bash
python3 -m http.server 8080
# Access at http://localhost:8080/[filename].html
```

## Project Structure

### Core Components
- **src/VetScanUltraAdvanced.jsx** - Advanced React component (currently active in main.jsx)
- **src/AnimalScannerPro.jsx** - Base React component with core scanner logic
- **standalone.html** - Most stable self-contained version (no dependencies)
- **vetscan-detective.html** - 🎯 BESTE VERSION: Tier-Detektiv mit Lerneffekt
- **vetscan-ultimate.html** - 3D-Version mit Karrieremodus
- **vetscan-story-mode.html** - Story-Modus mit Charakteren
- **vetgame-missions.html** - Mission-based game variant
- **vetscan-professional.html** - Professional scanner interface

### Key Data Structures
```javascript
// Animal types with disease presets
commonDiseases = {
  hund: [...],    // Dog diseases
  katze: [...],   // Cat diseases  
  pferd: [...],   // Horse diseases
  kaninchen: [...] // Rabbit diseases
}

// Normal vital ranges per animal
animalNormalValues = {
  hund: { heartRate: [60, 140], temperature: [37.5, 39.2], ... },
  katze: { heartRate: [120, 180], temperature: [37.8, 39.2], ... },
  // etc.
}
```

## Important Context

### Backup Strategy
- **BACKUP.md** contains complete working backups of all files
- **standalone.html** is the failsafe version - always works without dependencies
- If npm issues occur: `rm -rf node_modules package-lock.json && npm cache clean --force && npm install`

### Known Issues
- Service Worker cache conflicts can occur - test in incognito or clear cache
- Port 8080 conflicts - use alternative ports if needed (8081, 8082)
- Browser may cache old versions - use hard reload (Cmd+Shift+R)

### Version Information
- Current version: 3.1.0
- React 18 with createRoot API
- Vite configured for port 3000 with auto-open

## Testing Requirements

### Automated Testing Protocol
**WICHTIG**: Bei allen größeren Code-Änderungen MUSS automatisch:
1. **Server starten**: `python3 -m http.server 8080` für HTML-Dateien
2. **Browser-Test durchführen**: Mit Playwright automatisiert testen
3. **Console-Errors prüfen**: Alle JavaScript-Fehler in der Browser-Konsole identifizieren
4. **Fehler beheben**: Gefundene Errors VOR der Übergabe an den User fixen
5. **Verifizieren**: Sicherstellen, dass die Anwendung fehlerfrei läuft

### Testing Workflow
```bash
# 1. Start server
python3 -m http.server 8080

# 2. Run Playwright tests (if available)
# 3. Check console for errors
# 4. Fix any issues found
# 5. Re-test after fixes
```

**Regel**: NIEMALS ungetesteten Code an den User weitergeben. Immer erst selbst testen und Fehler beheben!

## Git Workflow

### Automatisches Git bei größeren Änderungen
**WICHTIG**: Bei allen größeren Features oder Änderungen MUSS automatisch:
1. **Git Add**: `git add .` für geänderte Dateien
2. **Git Commit**: Mit aussagekräftiger Commit-Message
3. **Git Push**: `git push origin main` zum GitHub Repository
4. **Repository**: git@github.com:DorianGrey-Austria/tierarztapp.git

### Commit Message Format
```
feat: Kurze Beschreibung der Änderung

- Detail 1
- Detail 2

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
```

**Regel**: Nach jeder größeren Änderung SOFORT committen und pushen!