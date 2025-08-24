# VetScan Pro 3000 - 3D Model Library

## Ordnerstruktur

```
models/
├── animals/                    # Tiermodelle für medizinische Simulation
│   ├── dog/                   # Hundemodelle (Bello-Varianten)
│   │   ├── high/              # Hohe Qualität (2048px Texturen)
│   │   ├── medium/            # Mittlere Qualität (1024px Texturen)
│   │   └── low/               # Niedrige Qualität (512px Texturen)
│   ├── cat/                   # Katzenmodelle
│   ├── horse/                 # Pferdemodelle
│   └── rabbit/                # Kaninchenmodelle
└── fallbacks/                 # Fallback-Geometrie für fehlende Modelle
```

## Datei-Konventionen

### Naming Schema:
- **Hauptmodell**: `{animal}_main.glb` (z.B. `bello_main.glb`)
- **Claude Desktop Export**: `{animal}_claude_desktop.glb`
- **Variations**: `{animal}_{breed}_{variation}.glb`

### Qualitätsstufen:

#### High Quality (`high/`)
- Polygon Count: 10,000-50,000 tris
- Texture Resolution: 2048x2048px
- Materials: Full PBR with Normal/Roughness Maps
- Target: Desktop, High-End Mobile

#### Medium Quality (`medium/`)
- Polygon Count: 5,000-15,000 tris
- Texture Resolution: 1024x1024px
- Materials: Simplified PBR
- Target: Standard Mobile, Tablets

#### Low Quality (`low/`)
- Polygon Count: 1,000-5,000 tris
- Texture Resolution: 512x512px
- Materials: Basic Diffuse Only
- Target: Low-End Mobile, Fallback

## Medical Visualizations

Alle Modelle unterstützen folgende medizinische Visualisierungsmodi:

1. **Normal Mode**: Realistic fur/skin textures
2. **X-Ray Mode**: Transparent with skeletal structure
3. **Ultrasound Mode**: Grayscale with internal organs
4. **Thermal Mode**: Heat signature visualization
5. **MRI Mode**: Cross-sectional medical imaging

## Import Guidelines

### Aus Blender exportieren:
```python
# Blender Export Settings
Format: GLB (Binary)
Include: Materials, Textures, Animations
Transform: +Y Up, Apply Transform
Geometry: Apply Modifiers, Export Normals
```

### Three.js Integration:
```javascript
// Progressive Loading Example
const loader = new GLTFLoader();
const qualities = ['high', 'medium', 'low'];

async function loadModelProgressive(animal, quality = 'medium') {
    try {
        const path = `/models/animals/${animal}/${quality}/${animal}_main.glb`;
        const gltf = await loader.loadAsync(path);
        return gltf.scene;
    } catch (error) {
        // Fallback to lower quality
        if (quality !== 'low') {
            return await loadModelProgressive(animal, 'low');
        }
        throw error;
    }
}
```

## Current Models

### 🐕 **Bello (Dog)**
- **Source**: Claude Desktop Export
- **Status**: ⏳ Pending Import
- **Variants**: Golden Retriever, Labrador
- **Medical Features**: Full anatomy, organ mapping

### 🐱 **Katze (Cat)**
- **Status**: 📋 Planned
- **Variants**: Hauskatze, Siamkatze

### 🐴 **Pferd (Horse)**  
- **Status**: 📋 Planned
- **Variants**: Warmblut, Pony

### 🐰 **Kaninchen (Rabbit)**
- **Status**: 📋 Planned
- **Variants**: Zwergkaninchen, Widder

## Performance Guidelines

### Loading Optimization:
1. **Start with Medium Quality** als Default
2. **Detect Device Capabilities** via WebGL
3. **Preload Critical Models** (Bello als Hauptcharakter)
4. **Lazy Load** andere Tiere nur bei Bedbedarf

### Memory Management:
- **Dispose unused models** when switching animals
- **Share materials** zwischen ähnlichen Modellen
- **Use texture atlasing** für mehrere Objekte

## Deployment

Models werden automatisch mit GitHub Actions deployed:
- **Target**: https://vibecoding.company/models/
- **CDN**: Über GitHub Pages verfügbar
- **Caching**: Browser-Cache für bessere Performance

## Troubleshooting

### Häufige Probleme:

1. **Model lädt nicht**: 
   - Check Browser Console für CORS/404 Errors
   - Verify file path und naming convention

2. **Performance schlecht**:
   - Fallback zu niedrigerer Qualität
   - Check polygon count in Blender

3. **Texturen fehlen**:
   - Verify Material Export in Blender
   - Check texture path references

4. **Medical Shader funktionieren nicht**:
   - Check Material Node Setup
   - Verify Shader compatibility mit Three.js

---

**Last Updated**: 24.08.2025  
**Version**: 1.0.0  
**Contact**: VetScan Pro 3000 Development Team