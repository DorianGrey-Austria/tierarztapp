#!/usr/bin/env python3
"""
Direct Bello Export - No dependencies required
Runs Blender in background mode to export the dog model
"""

import subprocess
import os
from pathlib import Path

# Configuration
PROJECT_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = PROJECT_ROOT / "assets" / "models" / "animals" / "bello"
BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"

# Ensure output directory exists
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Blender Python script to create and export Bello
blender_script = '''
import bpy
import os
from mathutils import Vector

print("🐕 Creating Bello dog model for VetScan Pro")

# Clear existing scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.object
sun.data.energy = 2

# Create Bello dog model (simplified but recognizable)
print("   Building Bello body parts...")

# Body (main torso)
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = "Bello_Body"
body.scale = (2.5, 1.2, 1)

# Apply smooth shading to body
bpy.ops.object.shade_smooth()

# Head 
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(2.8, 0, 1.3))
head = bpy.context.object
head.name = "Bello_Head"
head.scale = (1.2, 1, 1)

# Snout (muzzle)
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(3.8, 0, 1.1))
snout = bpy.context.object
snout.name = "Bello_Snout"
snout.scale = (1.5, 0.8, 0.6)

# Ears
for i, side in enumerate([0.5, -0.5]):
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(2.5, side * 0.8, 1.9))
    ear = bpy.context.object
    ear.name = f"Bello_Ear_{i+1}"
    ear.scale = (0.8, 0.3, 1.2)
    ear.rotation_euler = (0, 0.3 if side > 0 else -0.3, 0)

# Legs (4 cylinders)
leg_positions = [
    (1.5, 0.7, 0),   # Front right
    (1.5, -0.7, 0),  # Front left
    (-1.5, 0.7, 0),  # Back right
    (-1.5, -0.7, 0)  # Back left
]

for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.8, location=pos)
    leg = bpy.context.object
    leg.name = f"Bello_Leg_{i+1}"

# Tail
bpy.ops.mesh.primitive_cone_add(vertices=8, radius1=0.3, depth=2, location=(-2.8, 0, 1.5))
tail = bpy.context.object
tail.name = "Bello_Tail"
tail.rotation_euler = (0, 1.5, 0)

print("   Adding materials...")

# Create brown fur material
fur_material = bpy.data.materials.new(name="BelloFur")
fur_material.use_nodes = True
bsdf = fur_material.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.6, 0.4, 0.2, 1.0)  # Brown color
bsdf.inputs[7].default_value = 0.8  # Roughness

# Create black material for nose
nose_material = bpy.data.materials.new(name="BelloNose")
nose_material.use_nodes = True
nose_bsdf = nose_material.node_tree.nodes["Principled BSDF"]
nose_bsdf.inputs[0].default_value = (0.1, 0.1, 0.1, 1.0)  # Black
nose_bsdf.inputs[7].default_value = 0.3  # Shiny

# Apply materials
for obj in bpy.data.objects:
    if obj.name.startswith("Bello_") and obj.type == 'MESH':
        if "Snout" in obj.name:
            # Use black for snout/nose
            obj.data.materials.append(nose_material)
        else:
            # Use brown fur for everything else
            obj.data.materials.append(fur_material)

print("   Joining all parts into single mesh...")

# Select all Bello parts
bpy.ops.object.select_all(action='DESELECT')
bello_parts = [obj for obj in bpy.data.objects if obj.name.startswith("Bello_")]

for obj in bello_parts:
    obj.select_set(True)

# Set body as active and join
if bello_parts:
    bpy.context.view_layer.objects.active = bpy.data.objects["Bello_Body"]
    bpy.ops.object.join()
    
    # Rename to just "Bello"
    bpy.context.object.name = "Bello"

print("   Exporting models...")

# Export paths
exports = [
    ("OUTPUT_DIR/bello_high.glb", {"export_draco_mesh_compression_enable": True, "export_draco_mesh_compression_level": 6}),
    ("OUTPUT_DIR/bello_medium.glb", {"export_draco_mesh_compression_enable": True, "export_draco_mesh_compression_level": 4}),
    ("OUTPUT_DIR/bello_low.glb", {"export_draco_mesh_compression_enable": False})
]

for output_path, settings in exports:
    # Make path absolute
    full_path = output_path.replace("OUTPUT_DIR", "''' + str(OUTPUT_DIR) + '''")
    
    print(f"   Exporting to {full_path}...")
    
    # Export settings optimized for Three.js
    bpy.ops.export_scene.gltf(
        filepath=full_path,
        export_format='GLB',
        export_yup=True,  # Three.js uses Y-up
        export_apply=True,  # Apply modifiers
        export_animations=False,  # No animations for now
        export_materials='EXPORT',
        export_colors=True,
        export_cameras=False,
        export_lights=False,
        **settings
    )
    
    # Check file size
    import os
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        print(f"   ✅ Exported: {os.path.basename(full_path)} ({size:,} bytes)")

print("🎉 Bello export complete!")
'''

# Save the Blender script
script_path = PROJECT_ROOT / "scripts" / "temp_bello_export.py"
with open(script_path, 'w') as f:
    f.write(blender_script)

print("🐕 VetScan Pro - Bello Model Export")
print("=" * 50)
print(f"📁 Output directory: {OUTPUT_DIR}")
print(f"🔧 Using Blender at: {BLENDER_PATH}")
print()

# Check if Blender exists
if not Path(BLENDER_PATH).exists():
    print("❌ Blender not found at expected location")
    print("💡 Please install Blender or update BLENDER_PATH in this script")
    exit(1)

print("🚀 Running Blender export...")

# Run Blender in background mode
try:
    result = subprocess.run(
        [BLENDER_PATH, "--background", "--python", str(script_path)],
        capture_output=True,
        text=True,
        timeout=60
    )
    
    # Print Blender output
    if result.stdout:
        for line in result.stdout.split('\n'):
            if line and not line.startswith('Blender'):
                print(f"   {line}")
    
    if result.returncode == 0:
        print()
        print("✅ Export completed successfully!")
        print(f"📦 Models exported to: {OUTPUT_DIR}")
        
        # List exported files
        print("\n📋 Exported files:")
        for file in OUTPUT_DIR.glob("*.glb"):
            size = file.stat().st_size
            print(f"   - {file.name}: {size:,} bytes")
            
    else:
        print("❌ Export failed with errors:")
        if result.stderr:
            print(result.stderr)
            
except subprocess.TimeoutExpired:
    print("❌ Export timed out after 60 seconds")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
finally:
    # Clean up temp script
    if script_path.exists():
        script_path.unlink()
        print("🧹 Cleaned up temporary files")