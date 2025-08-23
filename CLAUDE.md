# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
npm run dev                    # Start dev server (Vite)
npm run build                  # Build for production
npm run preview                # Preview production build
```

### Standalone HTML Versions
```bash
python3 -m http.server 8080    # Start local server
# Access: http://localhost:8080/[filename].html

# Alternative port if 8080 is busy:
python3 -m http.server 8081

# Kill existing server on port:
kill $(lsof -t -i:8080)
```

### 3D Workflow Commands
```bash
# Test Blender MCP connection
node scripts/test-mcp-connection.js

# Run 3D asset pipeline
./scripts/deploy-animal.sh

# Generate medical visualization shaders
npm run generate:shaders -- --model=bello

# Optimize 3D models
npm run optimize:model -- --input=path/to/model.glb --output=path/to/output/

# Run integration tests for specific model
npm run test:integration -- --model=bello

# Manual browser console testing
python3 test-console-errors.py
```

## Architecture & File Structure

### Key HTML Versions (Priority Order)
1. **`vetscan-bello-3d-v7.html`** - VERSION 7: Latest 3D with medical shaders (X-Ray, Ultrasound, Thermal, MRI)
2. **`vetscan-detective.html`** - RECOMMENDED: Educational detective gameplay with Dr. Eule mentor
3. **`standalone.html`** - STABLE: Most stable base version
4. **`vetscan-story-mode.html`** - Story campaign with Dr. Sarah Miller
5. **`index.html`** - Auto-generated landing page (created during deployment)

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

### Automatic Deployment via GitHub Actions
```bash
git add .
git commit -m "feat: Description of changes"
git push origin main
# Triggers automatic deployment to https://vibecoding.company
```

**Deployment Configuration**: `.github/workflows/deploy.yml`
- **Trigger**: Push to `main` branch or manual workflow dispatch
- **Target**: https://vibecoding.company via FTP to Hostinger
- **Files**: Selected HTML versions + auto-generated index.html

## Version Management

### Update Version Numbers on Every Deployment
**Locations to update:**
1. HTML `<title>` Tag
2. Header in HTML Body
3. JavaScript `const VERSION` (e.g., "7.0.2")
4. JavaScript `const BUILD` (format: "YYYY.MM.DD.XXX")
5. Status Badge in UI
6. Debug Info Panel

### CDN Configuration (Version 7)
- **Three.js**: r128 from unpkg CDN (stable, working)
- **Loaders**: GLTFLoader, DRACOLoader, OrbitControls
- **Note**: Using unpkg instead of cdnjs (cdnjs lacks example files)

## Progressive Loading System (3D Models)
1. Attempts to load high-quality GLB first (`bello_high.glb`)
2. Falls back to medium quality (`bello_medium.glb`)
3. Falls back to low quality (`bello_low.glb`)
4. If no GLB available, uses procedural fallback model
5. Performance monitoring with polygon counter

## Medical Visualization Shaders
- **X-Ray**: Fresnel-based transparency with bone highlighting
- **Ultrasound**: Noise patterns with scan-line effects
- **Thermal**: Temperature gradient mapping
- **MRI**: Grayscale tissue differentiation
- **Normal**: Standard materials with realistic textures

## Testing & Quality Assurance

### Browser Console Testing
```bash
# Chrome (preferred): Cmd+Option+J (Mac) or F12 (Windows/Linux)
# Test: Interactive elements, 3D visualization, form submissions
# Clear cache: Cmd+Shift+R (hard reload)
```

### Integration Tests
```bash
npm run test:integration -- --model=bello  # Playwright tests for specific model
```

### Common Fixes
- **Port conflicts**: Use 8081, 8082 if 8080 busy
- **Browser cache**: Hard reload with Cmd+Shift+R
- **Service worker conflicts**: Test in incognito mode
- **Console errors**: Check browser console for errors

## Blender MCP Integration

### When Blender MCP is Available
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

## Performance Optimization

### Standalone HTML Files
- All code inline (no external dependencies)
- Optimized for direct browser execution
- `.htaccess` configured for HTTPS and compression

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

## 20-Haustiere-System (100 Patienten)

### Tier-Kategorisierung nach Schwierigkeit
**STUFE 1 (6-10 Jahre) - 10 Basis-Haustiere:**
1. **Hund** - Klassiker mit vielen Rassen
2. **Katze** - Beliebtestes Haustier
3. **Kaninchen** - Häufiges Kleintier
4. **Meerschweinchen** - Beliebtes Kindertier
5. **Hamster** - Goldhamster/Zwerghamster
6. **Wellensittich** - Häufigster Ziervogel
7. **Goldfisch** - Erstes Aquarientier
8. **Schildkröte** - Land-/Wasserschildkröten
9. **Kanarienvogel** - Singvogel-Klassiker
10. **Maus** - Kleines Nagetier

**STUFE 2 (10-14 Jahre) - 10 Fortgeschrittene Tiere:**
11. **Frettchen** - Exotisches Raubtier
12. **Bartagame** - Beliebte Echse
13. **Ratte** - Intelligentes Nagetier
14. **Chinchilla** - Weiches Fell, spezielle Pflege
15. **Nymphensittich** - Größerer Vogel
16. **Papagei** - Sprechender Vogel
17. **Kornnatter** - Ungiftige Schlange
18. **Degu** - Soziales Nagetier
19. **Axolotl** - Wasserlebewesen
20. **Igel** - Stacheliges Säugetier

### Patient-Generator System
```javascript
// 100 individuelle Patienten aus 20 Tierarten
// Jedes Tier hat 5 verschiedene Patienten mit:
// - Individuellen Namen (Bello, Luna, Max, etc.)
// - Verschiedenen Altersgruppen
// - Unterschiedlichen Persönlichkeiten
// - 5 rotierenden Symptom-Sets pro Tierart

const patientDistribution = {
  level1: 60, // 60 Patienten aus einfachen Tieren (6 pro Tier)
  level2: 40  // 40 Patienten aus komplexen Tieren (4 pro Tier)
}
```

### Extended Animal Data Structure
```javascript
{
  id: 'dog',
  name: 'Hund',
  category: 'pet',
  difficulty: 'beginner', // beginner/intermediate/advanced
  ageGroup: '6-10',       // Altersempfehlung für Kinder
  
  // 3D-Modell-Konfiguration für Blender MCP
  model3D: {
    baseTemplate: 'quadruped_medium.blend',
    anatomyPoints: { heart: {x,y,z}, lungs: {x,y,z}, ... },
    colorVariations: ['brown', 'black', 'white', 'spotted'],
    sizeVariations: ['small', 'medium', 'large']
  },
  
  // 5 Patienten-Profile pro Tier
  patientProfiles: [
    { name: 'Bello', age: 3, breed: 'Labrador', personality: 'friendly' },
    { name: 'Luna', age: 7, breed: 'Schäferhund', personality: 'nervous' },
    // ... 3 weitere
  ],
  
  // 5 Symptom-Sets für Variation
  symptomSets: [
    { symptoms: ['Husten', 'Fieber'], diagnosis: 'Erkältung' },
    { symptoms: ['Erbrechen', 'Durchfall'], diagnosis: 'Magen-Darm' },
    // ... 3 weitere
  ],
  
  // Pädagogische Elemente
  education: {
    funFacts: ['Hunde riechen 10.000x besser als Menschen'],
    memoryTricks: ['H.U.N.D = Herz, Urin, Nase, Darm prüfen']
  }
}
```

## Blender MCP Animal Templates

### Template-Bibliothek für 3D-Modelle
```bash
# Template-Generierung für verschiedene Tiergruppen
scripts/generate-animal-model.js --template=quadruped_small --animal=hamster
scripts/generate-animal-model.js --template=bird_base --animal=wellensittich  
scripts/generate-animal-model.js --template=reptile_base --animal=schildkroete
scripts/generate-animal-model.js --template=aquatic_base --animal=goldfisch

# Blender MCP Templates (bereit für Integration)
templates/
├── quadruped_small.blend    # Hamster, Maus, Meerschweinchen
├── quadruped_medium.blend   # Hund, Katze, Kaninchen, Frettchen
├── bird_base.blend          # Wellensittich, Kanarienvogel, Papagei
├── reptile_base.blend       # Schildkröte, Bartagame, Kornnatter
└── aquatic_base.blend       # Goldfisch, Axolotl
```

### 3D Model Commands (Blender MCP Active)
```python
# Tier-Modell generieren
animal_model = generate_animal_model("dog", template="quadruped_medium")
animal_model.set_color_variation("brown")
animal_model.set_size("medium")
animal_model.add_anatomy_points(["heart", "lungs", "stomach"])

# Multi-Quality Export
export_glb(animal_model, quality="high")    # Für Desktop
export_glb(animal_model, quality="medium")  # Für Tablets
export_glb(animal_model, quality="low")     # Für Mobile

# Medical Shader Application
apply_medical_shader(animal_model, mode="xray")
apply_medical_shader(animal_model, mode="ultrasound")
```