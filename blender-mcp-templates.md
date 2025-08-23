# 🎨 Blender MCP Templates für 20 Haustiere

## Template-Übersicht

### 1. quadruped_small.blend
**Für kleine Vierbeiner (1-15cm)**
- **Tiere**: Maus, Hamster, Degu, Gerbil
- **Basis-Proportionen**: Kompakter Körper, kurze Beine, großer Kopf relativ zum Körper
- **Anatomie-Punkte**: Herz (zentral), Lunge (oberer Brustbereich), Magen (Bauchbereich)

```python
# Blender MCP Commands für kleine Vierbeiner
def generate_small_quadruped(animal_type, color_variant, size):
    base_template = load_template("quadruped_small.blend")
    
    # Tier-spezifische Anpassungen
    if animal_type == "mouse":
        scale_ears(base_template, factor=0.8)
        set_tail_length(base_template, length=0.9)  # Lange Schwänze
    elif animal_type == "hamster":
        scale_body(base_template, width=1.3)  # Rundlichere Form
        set_tail_length(base_template, length=0.1)  # Kurze Schwänze
    
    apply_color_variation(base_template, color_variant)
    add_anatomy_markers(base_template, ["heart", "lungs", "stomach"])
    return base_template
```

### 2. quadruped_medium.blend  
**Für mittlere Vierbeiner (20-60cm)**
- **Tiere**: Hund, Katze, Kaninchen, Frettchen, Chinchilla
- **Basis-Proportionen**: Ausgewogene Proportionen, längere Beine
- **Anatomie-Punkte**: Detailliertere Organe (Herz, Lunge, Leber, Nieren)

```python
def generate_medium_quadruped(animal_type, breed_variant, size):
    base_template = load_template("quadruped_medium.blend")
    
    if animal_type == "dog":
        if breed_variant == "labrador":
            scale_body(base_template, length=1.2)
            set_ear_type(base_template, "floppy")
        elif breed_variant == "beagle":
            scale_body(base_template, length=1.0, height=0.8)
    
    elif animal_type == "cat":
        set_eye_shape(base_template, "almond")
        add_whiskers(base_template, length=0.3)
    
    elif animal_type == "rabbit":
        scale_ears(base_template, factor=2.0)  # Große Ohren
        set_hop_posture(base_template, enabled=True)
```

### 3. bird_base.blend
**Für Vögel aller Größen**
- **Tiere**: Wellensittich, Kanarienvogel, Nymphensittich, Papagei
- **Basis-Proportionen**: Vogelkörper, Flügel, Schnabel
- **Anatomie-Punkte**: Brustmuskel (Flugmuskel), Luftsäcke, Muskelmagen

```python
def generate_bird(bird_type, plumage_pattern, size):
    base_template = load_template("bird_base.blend")
    
    if bird_type == "budgie":  # Wellensittich
        set_beak_type(base_template, "small_curved")
        apply_stripe_pattern(base_template, plumage_pattern)
        
    elif bird_type == "parrot":
        set_beak_type(base_template, "large_curved") 
        scale_overall(base_template, factor=2.0)
        add_crest_feathers(base_template, prominent=True)
    
    add_feather_texture(base_template, pattern=plumage_pattern)
    add_anatomy_markers(base_template, ["air_sacs", "gizzard", "crop"])
```

### 4. reptile_base.blend
**Für Reptilien**
- **Tiere**: Schildkröte, Bartagame, Kornnatter
- **Basis-Proportionen**: Variable je nach Art
- **Anatomie-Punkte**: Spezielle Reptilien-Anatomie

```python  
def generate_reptile(reptile_type, shell_pattern, size):
    base_template = load_template("reptile_base.blend")
    
    if reptile_type == "turtle":
        add_shell(base_template, pattern=shell_pattern)
        set_retractable_head(base_template, True)
        
    elif reptile_type == "bearded_dragon":
        add_beard_spines(base_template)
        set_skin_texture(base_template, "scales")
        
    elif reptile_type == "corn_snake":
        remove_legs(base_template)
        set_body_type(base_template, "serpentine")
        apply_snake_pattern(base_template, pattern)
```

### 5. aquatic_base.blend
**Für Wassertiere**  
- **Tiere**: Goldfisch, Axolotl
- **Basis-Proportionen**: Stromlinienförmig
- **Anatomie-Punkte**: Kiemen, Schwimmblase, Seitenlinie

```python
def generate_aquatic(fish_type, color_variant, fin_type):
    base_template = load_template("aquatic_base.blend")
    
    if fish_type == "goldfish":
        set_fin_style(base_template, fin_type)  # fantail, single, etc.
        apply_metallic_coloring(base_template, color_variant)
        
    elif fish_type == "axolotl":
        add_external_gills(base_template)
        set_body_type(base_template, "salamander")
        add_leg_appendages(base_template, count=4)
    
    add_underwater_animation(base_template)
```

## Export Pipeline

### Multi-Quality Export System
```python
def export_animal_model(animal_template, quality_levels=['high', 'medium', 'low']):
    exports = {}
    
    for quality in quality_levels:
        # Quality-spezifische Einstellungen
        if quality == 'high':
            texture_resolution = 2048
            polygon_reduction = 1.0
        elif quality == 'medium':  
            texture_resolution = 1024
            polygon_reduction = 0.6
        elif quality == 'low':
            texture_resolution = 512
            polygon_reduction = 0.3
            
        # Model optimieren
        optimized_model = optimize_model(animal_template, polygon_reduction)
        apply_texture_resolution(optimized_model, texture_resolution)
        
        # Medical Shader Varianten
        medical_variants = {}
        for shader in ['normal', 'xray', 'ultrasound', 'thermal', 'mri']:
            shader_model = apply_medical_shader(optimized_model, shader)
            medical_variants[shader] = shader_model
            
        # GLB Export
        filename = f"{animal_template.name}_{quality}.glb"
        export_glb(optimized_model, filename, include_medical_variants=medical_variants)
        exports[quality] = filename
        
    return exports
```

## Medical Visualization Shaders

### X-Ray Shader
```glsl
// X-Ray Material für medizinische Visualisierung
material xray_material {
    transparent: true,
    opacity: 0.3,
    fresnel_factor: 0.8,
    bone_highlight: true,
    color: vec3(0.8, 0.9, 1.0)
}
```

### Ultrasound Shader  
```glsl
// Ultraschall-Simulation
material ultrasound_material {
    noise_scale: 0.5,
    scan_lines: true,
    grayscale: true,
    contrast: 1.8
}
```

### Thermal Shader
```glsl
// Wärmebild-Simulation
material thermal_material {
    temperature_map: true,
    color_range: [blue, green, yellow, red],
    heat_sources: ["heart", "muscles", "organs"]
}
```

## Automatisierte Scripts

### Batch-Generierung aller 20 Tiere
```bash
# Alle Level 1 Tiere generieren
./generate-all-level1.py

# Alle Level 2 Tiere generieren  
./generate-all-level2.py

# Vollständige Pipeline
./generate-complete-animal-set.py --quality=all --medical-shaders=all
```

### Qualitätskontrolle
```python
def validate_animal_model(model_path):
    checks = {
        'polygon_count': check_polygon_limit(model_path),
        'texture_resolution': check_texture_sizes(model_path), 
        'anatomy_points': validate_anatomy_markers(model_path),
        'medical_shaders': test_shader_variants(model_path),
        'file_size': check_file_size_limits(model_path)
    }
    
    return all(checks.values()), checks
```

## Integration Commands

### Test einzelnes Tier
```bash
# Blender MCP für spezifisches Tier
uvx blender-mcp
python scripts/generate-animal.py --animal=dog --breed=labrador --quality=high

# Test im Browser
python3 -m http.server 8080
# Öffne: http://localhost:8080/vetscan-bello-3d-v7.html
```

### Vollständige Integration
```bash
# Alle 20 Tiere generieren und exportieren
python scripts/generate-all-animals.py

# In HTML-Versionen integrieren
python scripts/integrate-models.py --target=all-html-versions

# Deployment vorbereiten
git add . && git commit -m "feat: Add 20 animals 3D models" && git push
```

## Troubleshooting

### Häufige Probleme
1. **Blender MCP nicht verfügbar**: Fallback auf procedurale Geometrie
2. **Zu hohe Polygon-Anzahl**: Automatische Reduktion aktivieren  
3. **Shader-Fehler**: Fallback auf Standard-Material
4. **Export-Fehler**: Modell-Validierung vor Export

### Performance-Optimierung
- **Desktop**: High-Quality Models (>10k Polygone)
- **Tablet**: Medium-Quality Models (5-10k Polygone)  
- **Mobile**: Low-Quality Models (<5k Polygone)
- **Progressive Loading**: Automatische Qualitätserkennung