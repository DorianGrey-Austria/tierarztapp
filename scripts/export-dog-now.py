"""
🐕 BLENDER DOG EXPORT SCRIPT - COPY THIS INTO BLENDER!
=======================================================

ANLEITUNG:
1. Öffne Blender mit deinem Hund-Modell
2. Wechsle zum "Scripting" Tab (oben)
3. Klicke "New" im Text Editor
4. Kopiere dieses komplette Script
5. Klicke "Run Script" ▶️

Das Script exportiert automatisch 3 Qualitätsstufen!
"""

import bpy
import os
from pathlib import Path
from datetime import datetime

print("\n" + "="*60)
print("🐕 VetScan Pro - Professional Dog Export Pipeline")
print("="*60)

# Configuration
export_base = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_base.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# Analyze Scene
print("\n📊 Scene Analysis:")
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
total_verts = sum(len(obj.data.vertices) for obj in mesh_objects)
total_faces = sum(len(obj.data.polygons) for obj in mesh_objects)

print(f"  • Mesh Objects: {len(mesh_objects)}")
print(f"  • Total Vertices: {total_verts:,}")
print(f"  • Total Faces: {total_faces:,}")
print(f"  • Objects found: {[obj.name for obj in mesh_objects]}")

# Find the main dog object (largest mesh)
if mesh_objects:
    dog_object = max(mesh_objects, key=lambda x: len(x.data.vertices))
    print(f"\n🎯 Main object identified: {dog_object.name}")
    print(f"  • Vertices: {len(dog_object.data.vertices):,}")
    print(f"  • Faces: {len(dog_object.data.polygons):,}")
else:
    print("❌ No mesh objects found in scene!")
    raise Exception("No mesh objects to export")

# Prepare for export
print("\n🔧 Preparing Export...")

# Clean up the mesh
bpy.context.view_layer.objects.active = dog_object
bpy.ops.object.select_all(action='DESELECT')
dog_object.select_set(True)

# Switch to edit mode for cleanup
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Remove doubles
bpy.ops.mesh.remove_doubles(threshold=0.001)

# Recalculate normals
bpy.ops.mesh.normals_make_consistent(inside=False)

# Back to object mode
bpy.ops.object.mode_set(mode='OBJECT')

print("  ✅ Mesh cleaned and optimized")

# Quality Export Settings
quality_settings = {
    'high': {
        'suffix': '_high',
        'decimate': None,
        'texture_limit': 2048,
        'draco': True,
        'description': 'Full quality for desktop'
    },
    'medium': {
        'suffix': '_medium',
        'decimate': 0.5,
        'texture_limit': 1024,
        'draco': True,
        'description': 'Balanced for most devices'
    },
    'low': {
        'suffix': '_low',
        'decimate': 0.25,
        'texture_limit': 512,
        'draco': True,
        'description': 'Optimized for mobile'
    }
}

# Export each quality level
print("\n📦 Starting Multi-Quality Export...")

for quality_name, settings in quality_settings.items():
    print(f"\n  Exporting {quality_name.upper()} quality...")
    print(f"    {settings['description']}")
    
    # Apply decimation if needed
    modifier_applied = False
    if settings['decimate']:
        decimate_mod = dog_object.modifiers.new("EXPORT_DECIMATE", 'DECIMATE')
        decimate_mod.ratio = settings['decimate']
        modifier_applied = True
        
        # Get new polycount
        depsgraph = bpy.context.evaluated_depsgraph_get()
        eval_obj = dog_object.evaluated_get(depsgraph)
        new_faces = len(eval_obj.data.polygons)
        print(f"    Faces reduced to: {new_faces:,}")
    
    # Export path
    export_file = export_base / f"dog{settings['suffix']}_{timestamp}.glb"
    
    # Export with optimal settings
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(export_file),
            
            # Format
            export_format='GLB',
            
            # Include
            use_selection=True,
            export_apply=True,
            
            # Mesh
            export_draco_mesh_compression_enable=settings['draco'],
            export_draco_mesh_compression_level=6,
            
            # Materials & Textures
            export_materials='EXPORT',
            export_image_format='AUTO',
            export_texture_dir='',
            
            # Animation
            export_animations=True,
            export_frame_range=False,
            
            # Optimization
            export_optimize_animation_size=True,
            
            # Excluded
            export_cameras=False,
            export_lights=False
        )
        
        # Check file size
        file_size = export_file.stat().st_size / (1024 * 1024)
        print(f"    ✅ Exported: {export_file.name}")
        print(f"    📏 Size: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"    ❌ Export failed: {e}")
    
    # Remove temporary modifier
    if modifier_applied:
        dog_object.modifiers.remove(decimate_mod)

# Special Medical/Complete Export (all objects)
print(f"\n  Exporting MEDICAL quality (all layers)...")
bpy.ops.object.select_all(action='SELECT')

medical_file = export_base / f"dog_medical_{timestamp}.glb"
try:
    bpy.ops.export_scene.gltf(
        filepath=str(medical_file),
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_draco_mesh_compression_enable=True
    )
    
    file_size = medical_file.stat().st_size / (1024 * 1024)
    print(f"    ✅ Exported: {medical_file.name}")
    print(f"    📏 Size: {file_size:.2f} MB")
except Exception as e:
    print(f"    ❌ Export failed: {e}")

# Summary
print("\n" + "="*60)
print("🎉 EXPORT COMPLETED SUCCESSFULLY!")
print("="*60)

print(f"\n📁 Files exported to:")
print(f"   {export_base}")

print("\n📋 Created files:")
for f in export_base.glob(f"dog*_{timestamp}.glb"):
    size_mb = f.stat().st_size / (1024 * 1024)
    print(f"   • {f.name} ({size_mb:.2f} MB)")

print("\n🚀 Next Steps:")
print("   1. Files will be auto-imported by the watcher")
print("   2. Check: assets/models/animals/dog/")
print("   3. Test: http://localhost:8080/vetscan-bello-3d-v7.html")

print("\n✨ Your dog is ready for VetScan Pro!")
print("="*60)