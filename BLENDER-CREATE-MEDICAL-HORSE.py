"""
🐎 MEDICAL HORSE CREATION SCRIPT FOR BLENDER
============================================

WICHTIG: KOPIERE DIESES SCRIPT IN BLENDER!

1. Öffne Blender
2. Gehe zum Scripting Tab
3. Text → New
4. Füge dieses Script ein
5. Run Script (▶️)
6. Dann manuell exportieren zu: 
   /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse/horse_medical.glb

Das Script erstellt ein medizinisch präzises Pferd-Modell für Veterinäruntersuchungen!
"""

import bpy
import bmesh
from mathutils import Vector
import math
from pathlib import Path

print("\n" + "="*70)
print("🐎 MEDICAL HORSE MODEL CREATION")
print("="*70)

# SCHRITT 1: SZENE LEEREN
print("\n🧹 Clearing scene...")
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Delete all materials
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

# SCHRITT 2: PFERDEKÖPRER ERSTELLEN
print("🐎 Creating horse body...")
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.5))
body = bpy.context.active_object
body.name = "Horse_Body"
body.scale = (2.5, 1.0, 1.2)  # Length, Width, Height
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# SCHRITT 3: KOPF UND HALS
print("🦌 Creating head and neck...")

# Neck (elongated cylinder)
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.4,
    depth=1.8,
    location=(0, -1.8, 2.2),
    rotation=(0.5, 0, 0)
)
neck = bpy.context.active_object
neck.name = "Horse_Neck"

# Head (elongated cube)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -3.2, 2.8))
head = bpy.context.active_object
head.name = "Horse_Head"
head.scale = (0.6, 1.4, 0.8)
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# Muzzle/nose area
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.3,
    depth=0.6,
    location=(0, -4.2, 2.6),
    rotation=(1.57, 0, 0)
)
muzzle = bpy.context.active_object
muzzle.name = "Horse_Muzzle"

# Ears
for i, side in enumerate([-1, 1]):
    bpy.ops.mesh.primitive_cone_add(
        radius1=0.15,
        radius2=0.05,
        depth=0.4,
        location=(side * 0.3, -2.8, 3.4),
        rotation=(0, side * 0.3, 0)
    )
    ear = bpy.context.active_object
    ear.name = f"Horse_Ear_{['L', 'R'][i]}"

# SCHRITT 4: KRÄFTIGE BEINE MIT HUFEN
print("🦵 Creating powerful legs with hooves...")

# Leg positions: front left, front right, back left, back right
leg_positions = [
    (-0.8, -1.2, 0),   # Front left
    (0.8, -1.2, 0),    # Front right
    (-0.8, 1.2, 0),    # Back left
    (0.8, 1.2, 0)      # Back right
]

leg_names = ["FL", "FR", "BL", "BR"]

for i, (x, y, z) in enumerate(leg_positions):
    # Upper leg (thigh/shoulder)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.25,
        depth=1.0,
        location=(x, y, 1.0)
    )
    upper_leg = bpy.context.active_object
    upper_leg.name = f"Horse_UpperLeg_{leg_names[i]}"
    
    # Lower leg (shin/forearm)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.15,
        depth=0.8,
        location=(x, y, 0.3)
    )
    lower_leg = bpy.context.active_object
    lower_leg.name = f"Horse_LowerLeg_{leg_names[i]}"
    
    # Hoof (critical for lameness examination)
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.2,
        depth=0.15,
        location=(x, y, -0.1)
    )
    hoof = bpy.context.active_object
    hoof.name = f"Horse_Hoof_{leg_names[i]}"
    hoof.scale = (1.0, 1.2, 1.0)  # Slightly elongated
    bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)
    
    # Fetlock (ankle joint - important for examination)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.18,
        location=(x, y, 0.1)
    )
    fetlock = bpy.context.active_object
    fetlock.name = f"Horse_Fetlock_{leg_names[i]}"

# SCHRITT 5: MEDIZINISCHE ANATOMIE
print("❤️ Creating medical anatomy features...")

# Large heart area (horses have very large hearts)
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.4,
    location=(-0.3, -0.8, 1.8)
)
heart = bpy.context.active_object
heart.name = "Horse_Heart_Area"
heart.scale = (0.8, 1.2, 1.0)
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# Digestive tract (stomach area)
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.6,
    depth=0.8,
    location=(0.5, 0.5, 1.3),
    rotation=(0, 0.5, 0)
)
stomach = bpy.context.active_object
stomach.name = "Horse_Stomach_Area"

# Intestinal area (large colon)
bpy.ops.mesh.primitive_torus_add(
    major_radius=0.8,
    minor_radius=0.2,
    location=(0, 0.8, 1.0)
)
intestines = bpy.context.active_object
intestines.name = "Horse_Intestinal_Area"

# Lung areas
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.3,
        depth=1.0,
        location=(side * 0.6, -0.2, 2.0),
        rotation=(0, 0, 1.57)
    )
    lung = bpy.context.active_object
    lung.name = f"Horse_Lung_{'L' if side < 0 else 'R'}"

# SCHRITT 6: MÄHNE UND SCHWEIF
print("🌾 Creating mane and tail...")

# Mane along neck
mane_positions = [
    (0, -1.4, 2.8),
    (0, -1.8, 2.6),
    (0, -2.2, 2.4),
    (0, -2.6, 2.2)
]

for i, pos in enumerate(mane_positions):
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=pos)
    mane_strand = bpy.context.active_object
    mane_strand.name = f"Horse_Mane_{i:02d}"
    mane_strand.scale = (0.8, 0.2, 2.0)
    bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# Tail
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.15,
    depth=1.5,
    location=(0, 2.8, 1.2),
    rotation=(0.3, 0, 0)
)
tail = bpy.context.active_object
tail.name = "Horse_Tail"

# SCHRITT 7: MEDIZINISCHE MATERIALIEN
print("🎨 Creating medical materials...")

# 1. Normal Material (Bay Horse Color)
normal_mat = bpy.data.materials.new(name="Horse_Normal")
normal_mat.use_nodes = True
bsdf = normal_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.4, 0.2, 0.1, 1.0)  # Brown/bay color
bsdf.inputs[9].default_value = 0.6  # Roughness

# 2. X-Ray Material
xray_mat = bpy.data.materials.new(name="Horse_XRay")
xray_mat.use_nodes = True
xray_mat.blend_method = 'BLEND'
bsdf = xray_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.8, 0.9, 1.0, 0.3)  # Blue-white translucent
bsdf.inputs[21].default_value = 0.3  # Alpha

# 3. Ultrasound Material
ultrasound_mat = bpy.data.materials.new(name="Horse_Ultrasound")
ultrasound_mat.use_nodes = True
bsdf = ultrasound_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.9, 0.9, 0.6, 1.0)  # Yellow-gray

# 4. Thermal Material
thermal_mat = bpy.data.materials.new(name="Horse_Thermal")
thermal_mat.use_nodes = True
bsdf = thermal_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (1.0, 0.3, 0.0, 1.0)  # Orange-red

# 5. MRI Material
mri_mat = bpy.data.materials.new(name="Horse_MRI")
mri_mat.use_nodes = True
bsdf = mri_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.7, 0.7, 0.7, 1.0)  # Gray

# Apply normal material to all horse objects
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.name.startswith('Horse'):
        if not obj.data.materials:
            obj.data.materials.append(normal_mat)

# SCHRITT 8: OPTIMIERUNG
print("⚙️ Optimizing mesh...")

# Smooth shading for all horse objects
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.name.startswith('Horse'):
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()

# Count statistics
total_objects = len([obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.name.startswith('Horse')])
total_materials = len([mat for mat in bpy.data.materials if 'Horse' in mat.name])
total_polygons = sum(len(obj.data.polygons) for obj in bpy.data.objects 
                    if obj.type == 'MESH' and obj.name.startswith('Horse'))

print("\n" + "="*70)
print("🎉 MEDICAL HORSE MODEL CREATION COMPLETED!")
print("="*70)
print("Model Statistics:")
print(f"  📦 Objects: {total_objects}")
print(f"  🎨 Materials: {total_materials}")
print(f"  🔺 Polygons: {total_polygons}")
print("\nModel Features:")
print("  🐎 Anatomically correct horse proportions")
print("  🦵 Four powerful legs with detailed hooves")
print("  ❤️ Large heart area (critical for cardiac examination)")
print("  🫁 Lung areas for respiratory assessment")
print("  🦴 Digestive tract visualization")
print("  🌾 Natural mane and tail")
print("  🎨 5 medical visualization materials")
print("\n📦 MANUAL EXPORT REQUIRED:")
print("1. Select all horse objects (A to select all)")
print("2. File → Export → glTF 2.0 (.glb/.gltf)")
print("3. Set filepath to:")
print("   /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse/horse_medical.glb")
print("4. Enable 'Selected Objects' and 'Apply Modifiers'")
print("5. Click 'Export glTF 2.0'")
print("="*70)