"""
🎨 MANUELLER EXPORT-SCRIPT FÜR BLENDER
=====================================

WICHTIG: KOPIERE DIESES SCRIPT IN BLENDER!

1. Öffne Blender
2. Gehe zum Scripting Tab
3. Text → New
4. Füge dieses Script ein
5. Run Script (▶️)

Das Script zeigt die kreativen Änderungen und exportiert!
"""

import bpy
import bmesh
from mathutils import Vector

print("\n" + "="*60)
print("🎨 KREATIVE HUNDE-TRANSFORMATION & EXPORT")
print("="*60)

# SCHRITT 1: FÜGE ROTES HALSBAND HINZU
print("\n📿 Füge rotes Halsband hinzu...")
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.5,
    minor_radius=0.1,
    location=(0, -0.5, 2.0),
    rotation=(1.57, 0, 0)
)
collar = bpy.context.active_object
collar.name = "Dog_Collar"

# Rotes Material
mat_collar = bpy.data.materials.new(name="Red_Collar")
mat_collar.use_nodes = True
mat_collar.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.1, 0.1, 1.0)
collar.data.materials.append(mat_collar)

# SCHRITT 2: FÜGE BUNTEN BALL HINZU
print("⚽ Füge Spielball hinzu...")
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.3,
    location=(1.5, 0, 0.3)
)
ball = bpy.context.active_object
ball.name = "Dog_Ball"

# Buntes Material
mat_ball = bpy.data.materials.new(name="Colorful_Ball")
mat_ball.use_nodes = True
mat_ball.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.6, 1.0, 1.0)
ball.data.materials.append(mat_ball)

# SCHRITT 3: FÜGE PARTY-HUT HINZU
print("🎩 Füge Party-Hut hinzu...")
bpy.ops.mesh.primitive_cone_add(
    radius1=0.5,
    radius2=0.05,
    depth=0.8,
    location=(0, -0.2, 3.2)
)
hat = bpy.context.active_object
hat.name = "Party_Hat"

# Pink Material
mat_hat = bpy.data.materials.new(name="Pink_Hat")
mat_hat.use_nodes = True
mat_hat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.2, 0.4, 1.0)
hat.data.materials.append(mat_hat)

# SCHRITT 4: ÄNDERE HAUPTOBJEKT-FARBE
print("🎨 Ändere Hundefarbe zu Lila...")
# Finde größtes Mesh (wahrscheinlich der Hund)
meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
if meshes:
    dog = max(meshes, key=lambda x: len(x.data.vertices))
    
    # Lila Material
    mat_dog = bpy.data.materials.new(name="Purple_Dog")
    mat_dog.use_nodes = True
    mat_dog.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.3, 0.9, 1.0)
    
    # Ersetze erstes Material oder füge hinzu
    if dog.data.materials:
        dog.data.materials[0] = mat_dog
    else:
        dog.data.materials.append(mat_dog)
    
    print(f"  ✅ Farbe von '{dog.name}' geändert!")

# SCHRITT 5: EXPORTIERE ALLES
print("\n📦 Exportiere kreativen Hund...")

# Wähle alle Objekte
bpy.ops.object.select_all(action='SELECT')

# Export-Pfade
export_paths = [
    '/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/dog/dog_creative.glb',
    '/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/dog_creative.glb'
]

for path in export_paths:
    try:
        bpy.ops.export_scene.gltf(
            filepath=path,
            export_format='GLB',
            use_selection=True,
            export_apply=True
        )
        print(f"  ✅ Exportiert nach: {path}")
    except:
        print(f"  ⚠️ Konnte nicht exportieren nach: {path}")

print("\n" + "="*60)
print("🎉 TRANSFORMATION & EXPORT ABGESCHLOSSEN!")
print("="*60)
print("\nDer kreative Hund hat jetzt:")
print("  📿 Rotes Halsband")
print("  ⚽ Bunten Spielball")
print("  🎩 Party-Hut")
print("  🎨 Lila Farbe")
print("\nTeste im Browser: http://localhost:8080/vetscan-bello-3d-v7.html")
print("="*60)