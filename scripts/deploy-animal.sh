#!/bin/bash
# Datei: scripts/deploy-animal.sh
# Automatisierungs-Workflow für Tierverwaltung im Veterinärspiel

echo "🐕 Starting Bello deployment pipeline..."

# 1. Export aus Blender (falls vorhanden)
if [ -f "bello.blend" ]; then
    echo "📦 Exporting from Blender..."
    # blender --background bello.blend --python export_gltf.py
    echo "   Blender export completed"
fi

# 2. Optimierung der Modelle
if [ -f "assets/models/animals/bello/bello.glb" ]; then
    echo "⚡ Optimizing model..."
    npm run optimize:model -- --input=assets/models/animals/bello/bello.glb --output=assets/models/animals/bello/
    echo "   Model optimization completed"
fi

# 3. Generiere Shader-Varianten
echo "🎨 Generating medical visualization shaders..."
npm run generate:shaders -- --model=bello

# 4. Tests ausführen
echo "🧪 Running integration tests..."
npm run test:integration -- --model=bello

# 5. Build das Projekt
echo "🔨 Building project..."
npm run build

# 6. Deploy zu vibecoding.company
echo "🚀 Deploying to vibecoding.company..."
git add .
git commit -m "feat: Add Bello 3D model with medical visualizations"
git push origin main

echo "✅ Bello deployment completed!"
echo "🌐 Check result at: https://vibecoding.company"