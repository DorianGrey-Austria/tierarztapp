"""
🐹 GUINEA PIG MEDICAL MODEL SCRIPT FÜR BLENDER
=============================================

WICHTIG: KOPIERE DIESES SCRIPT IN BLENDER!

1. Öffne Blender
2. Gehe zum Scripting Tab
3. Text → New
4. Füge dieses Script ein
5. Run Script (▶️)

Erstellt medizinisch accurate Guinea Pig mit 5000-8000 Polygonen!
"""

import bpy
import bmesh
from mathutils import Vector
import math

print("\n" + "="*60)
print("🐹 GUINEA PIG MEDICAL MODEL CREATION")
print("="*60)

# SCHRITT 1: SCENE LEEREN
print("\n🧹 Clearing scene...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# SCHRITT 2: GUINEA PIG KÖRPER
print("\n🐹 Creating guinea pig body...")
bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
body = bpy.context.active_object
body.name = "GuineaPig_Body"

# Guinea pig proportions: compact, barrel-shaped
body.scale = (1.3, 0.9, 0.65)  # Length, width, height
bpy.ops.object.transform_apply(transform=True, scale=True)

# Add detail for medical scanning
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=2)
bpy.ops.object.mode_set(mode='OBJECT')

print("  ✅ Body created with guinea pig proportions")

# SCHRITT 3: KOPF
print("\n🐹 Creating head...")
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(1.1, 0, 0.1))
head = bpy.context.active_object
head.name = "GuineaPig_Head"

# Guinea pig head proportions - rounded, not pointed
head.scale = (0.8, 1.0, 0.9)
bpy.ops.object.transform_apply(transform=True, scale=True)

bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.subdivide(number_cuts=1)
bpy.ops.object.mode_set(mode='OBJECT')

print("  ✅ Head created")

# SCHRITT 4: OHREN (Klein für Guinea Pig)
print("\n👂 Creating small ears...")
for side in [-1, 1]:
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.12, 
        location=(1.2, side * 0.25, 0.25)
    )
    ear = bpy.context.active_object
    ear.name = f"GuineaPig_Ear_{'L' if side < 0 else 'R'}"
    
    # Scale to guinea pig ear proportions (small and rounded)
    ear.scale = (0.6, 1.2, 0.4)
    bpy.ops.object.transform_apply(transform=True, scale=True)

print("  ✅ Small ears created")

# SCHRITT 5: ZÄHNE (WICHTIG FÜR GUINEA PIG MEDIZIN!)
print("\n🦷 Creating continuously growing incisors...")
for side in [-1, 1]:
    # Obere Schneidezähne
    bpy.ops.mesh.primitive_cube_add(
        size=0.03,
        location=(1.35, side * 0.08, 0.05)
    )
    tooth = bpy.context.active_object
    tooth.name = f"GuineaPig_UpperIncisor_{'L' if side < 0 else 'R'}"
    tooth.scale = (1.5, 0.5, 0.8)
    bpy.ops.object.transform_apply(transform=True, scale=True)
    
    # Untere Schneidezähne
    bpy.ops.mesh.primitive_cube_add(
        size=0.025,
        location=(1.37, side * 0.08, -0.05)
    )
    tooth = bpy.context.active_object
    tooth.name = f"GuineaPig_LowerIncisor_{'L' if side < 0 else 'R'}"
    tooth.scale = (1.2, 0.5, 0.8)
    bpy.ops.object.transform_apply(transform=True, scale=True)

print("  ✅ Incisors created (continuous growth feature)")

# SCHRITT 6: BEINE (Kurz für Guinea Pig)
print("\n🦵 Creating short legs...")
positions = [
    (0.6, -0.5, -0.5),   # Vorne links
    (0.6, 0.5, -0.5),    # Vorne rechts
    (-0.3, -0.5, -0.5),  # Hinten links
    (-0.3, 0.5, -0.5)    # Hinten rechts
]

for i, pos in enumerate(positions):
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.08,
        depth=0.3,
        location=pos
    )
    leg = bpy.context.active_object
    leg.name = f"GuineaPig_Leg_{i+1}"

print("  ✅ Short legs created")

# SCHRITT 7: FÜSSE
print("\n🐾 Creating feet...")
foot_positions = [
    (0.6, -0.5, -0.65),   # Vorne links
    (0.6, 0.5, -0.65),    # Vorne rechts  
    (-0.3, -0.5, -0.65),  # Hinten links
    (-0.3, 0.5, -0.65)    # Hinten rechts
]

for i, pos in enumerate(foot_positions):
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1,
        location=pos
    )
    foot = bpy.context.active_object
    foot.name = f"GuineaPig_Foot_{i+1}"
    
    # Guinea pig foot proportions
    foot.scale = (1.2, 0.8, 0.5)
    bpy.ops.object.transform_apply(transform=True, scale=True)

print("  ✅ Feet created")

# SCHRITT 8: MEDIZINISCHE MARKER (für Vitamin C & Cecotrophy)
print("\n🏥 Creating medical markers...")

# Cecum marker (wichtig für Cecotrophy)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.15,
    location=(-0.2, 0, -0.2)
)
cecum = bpy.context.active_object
cecum.name = "GuineaPig_Cecum_Marker"
cecum.display_type = 'WIRE'

# Leber marker (Vitamin C processing)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.1,
    location=(0.3, 0.2, 0.1)
)
liver = bpy.context.active_object
liver.name = "GuineaPig_Liver_Marker"
liver.display_type = 'WIRE'

print("  ✅ Medical markers created")

# SCHRITT 9: ALLE OBJEKTE VERBINDEN
print("\n🔗 Joining all objects...")
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.join()

guinea_pig = bpy.context.active_object
guinea_pig.name = "GuineaPig_Medical_Complete"

print("  ✅ All objects joined")

# SCHRITT 10: POLYGON COUNT PRÜFEN
current_polys = len(guinea_pig.data.polygons)
print(f"\n📊 Current polygon count: {current_polys}")

if current_polys > 8000:
    print("  ⚠️  Too many polygons, decimating...")
    decimate = guinea_pig.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = 7000 / current_polys
    bpy.ops.object.modifier_apply(modifier=decimate.name)
    new_polys = len(guinea_pig.data.polygons)
    print(f"  ✅ Decimated to {new_polys} polygons")
elif current_polys < 5000:
    print("  ⚠️  Too few polygons, subdividing...")
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    new_polys = len(guinea_pig.data.polygons)
    print(f"  ✅ Subdivided to {new_polys} polygons")

final_polys = len(guinea_pig.data.polygons)
print(f"🎯 Final polygon count: {final_polys}")

# SCHRITT 11: MEDIZINISCHE MATERIALIEN ERSTELLEN
print("\n🎨 Creating medical materials...")

# NORMAL MATERIAL (Brown/White Guinea Pig)
mat_normal = bpy.data.materials.new(name="GuineaPig_Normal")
mat_normal.use_nodes = True
mat_normal.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.4, 0.2, 1.0)  # Brown
mat_normal.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.1  # Roughness
guinea_pig.data.materials.append(mat_normal)

# X-RAY MATERIAL
mat_xray = bpy.data.materials.new(name="GuineaPig_XRay")
mat_xray.use_nodes = True
mat_xray.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 1.0, 1.0)  # Blue tint
mat_xray.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.8  # Alpha/Transmission
mat_xray.blend_method = 'BLEND'

# ULTRASOUND MATERIAL  
mat_ultrasound = bpy.data.materials.new(name="GuineaPig_Ultrasound")
mat_ultrasound.use_nodes = True
mat_ultrasound.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1.0)  # Grayscale
mat_ultrasound.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5  # Emission

# THERMAL MATERIAL
mat_thermal = bpy.data.materials.new(name="GuineaPig_Thermal")
mat_thermal.use_nodes = True
mat_thermal.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.5, 0.0, 1.0)  # Orange/Red
mat_thermal.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.3  # Emission

# MRI MATERIAL
mat_mri = bpy.data.materials.new(name="GuineaPig_MRI")
mat_mri.use_nodes = True
mat_mri.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.7, 0.7, 0.7, 1.0)  # Grayscale
mat_mri.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8  # Roughness

print("  ✅ All medical materials created")

# SCHRITT 12: EXPORT
print("\n📦 Exporting Guinea Pig Medical Model...")

# Export paths
export_paths = [
    '/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/guinea_pig/guinea_pig_medical.glb',
    '/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/guinea_pig_medical.glb'
]

# Ensure directories exist
import os
for path in export_paths:
    os.makedirs(os.path.dirname(path), exist_ok=True)

# Export
for path in export_paths:
    try:
        bpy.ops.export_scene.gltf(
            filepath=path,
            export_format='GLB',
            use_selection=True,
            export_apply=True,
            export_materials='EXPORT'
        )
        print(f"  ✅ Exported to: {path}")
    except Exception as e:
        print(f"  ⚠️ Could not export to: {path} - {e}")

print("\n" + "="*60)
print("🎉 GUINEA PIG MEDICAL MODEL COMPLETE!")
print("="*60)
print(f"\nFinal model stats:")
print(f"  📊 Polygons: {final_polys}")
print(f"  🎯 Target: 5000-8000 ({'✅ WITHIN RANGE' if 5000 <= final_polys <= 8000 else '⚠️ OUTSIDE RANGE'})")

print(f"\n🏥 Medical Features:")
print(f"  🦷 Continuously growing incisors (dental health)")
print(f"  🫁 Cecum markers (cecotrophy)")  
print(f"  🩸 Liver markers (vitamin C dependency)")
print(f"  🐹 Compact guinea pig anatomy")

print(f"\n🎨 Materials available:")
print(f"  • Normal (brown/white)")
print(f"  • X-Ray (transparent blue)")
print(f"  • Ultrasound (grayscale)")
print(f"  • Thermal (orange/red)")
print(f"  • MRI (medical grayscale)")

print(f"\n🚀 Test in browser:")
print(f"  http://localhost:8080/vetscan-guinea-pig-3d.html")
print("="*60)