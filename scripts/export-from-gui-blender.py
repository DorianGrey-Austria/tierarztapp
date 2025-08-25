"""
BLENDER GUI EXPORT SCRIPT - VetScan Pro
========================================
INSTRUCTIONS:
1. Copy this entire script
2. In Blender: Switch to "Scripting" workspace (top tabs)
3. Click "New" in Text Editor
4. Paste this script
5. Click "Run Script" button
6. Check console for export status

This exports your ACTUAL model from the GUI, not a procedural one!
"""

import bpy
import os
from pathlib import Path

print("\n" + "="*60)
print("🐕 VetScan Pro - Realistic Dog Export from GUI")
print("="*60)

# Define export path - adjust if needed
export_base = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/bello"
os.makedirs(export_base, exist_ok=True)

# List all objects in scene to help identify the dog
print("\n📋 Objects in your scene:")
print("-" * 40)
for obj in bpy.context.scene.objects:
    if obj.type == 'MESH':
        vertex_count = len(obj.data.vertices) if obj.data else 0
        print(f"  • {obj.name}: {obj.type} ({vertex_count} vertices)")

print("\n🔍 Looking for dog model...")

# Try to find the dog model - adjust these names based on your model
possible_names = [
    "Dog", "dog", "Hund", "hund", "Bello", "bello",
    "Dog_Body", "DogMesh", "dog_mesh", "Character",
    "Cube", "Cube.001", "Model", "Body"  # Sometimes default names
]

dog_model = None
selected_objects = []

# First check if something is already selected
if bpy.context.selected_objects:
    print(f"✅ Using selected objects: {[obj.name for obj in bpy.context.selected_objects]}")
    selected_objects = [obj for obj in bpy.context.selected_objects if obj.type == 'MESH']
    if selected_objects:
        dog_model = selected_objects[0]  # Use first selected mesh
else:
    # Try to find by name
    for name in possible_names:
        if name in bpy.data.objects:
            obj = bpy.data.objects[name]
            if obj.type == 'MESH':
                dog_model = obj
                print(f"✅ Found potential dog model: {name}")
                break
    
    # If not found by name, use the mesh with most vertices (likely the main model)
    if not dog_model:
        meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
        if meshes:
            # Sort by vertex count
            meshes.sort(key=lambda x: len(x.data.vertices) if x.data else 0, reverse=True)
            dog_model = meshes[0]
            print(f"✅ Using largest mesh as dog model: {dog_model.name} ({len(dog_model.data.vertices)} vertices)")

if not dog_model:
    print("❌ No suitable model found!")
    print("💡 TIP: Select your dog model and run this script again")
else:
    print(f"\n🎯 Exporting: {dog_model.name}")
    print(f"   Vertices: {len(dog_model.data.vertices) if dog_model.data else 0}")
    print(f"   Location: {list(dog_model.location)}")
    
    # Deselect all and select only the dog model
    bpy.ops.object.select_all(action='DESELECT')
    dog_model.select_set(True)
    bpy.context.view_layer.objects.active = dog_model
    
    # Export settings for Three.js compatibility
    export_settings = {
        'export_format': 'GLB',
        'export_yup': True,  # Three.js uses Y-up
        'export_apply': True,  # Apply modifiers
        'export_animations': True,  # Include animations if any
        'export_materials': 'EXPORT',
        'export_colors': True,
        'export_cameras': False,
        'export_lights': False,
        'export_selected': True,  # Only export selected
        'use_selection': True,
        'export_extras': True,  # Include custom properties
        'export_tangents': False,  # Three.js calculates these
    }
    
    # Export multiple quality levels
    qualities = [
        ("realistic_high", True, 6),
        ("realistic_medium", True, 4),
        ("realistic_low", False, 0)
    ]
    
    print("\n📦 Exporting quality variants...")
    
    for name, use_draco, draco_level in qualities:
        output_path = os.path.join(export_base, f"bello_{name}.glb")
        
        # Update compression settings
        export_settings['export_draco_mesh_compression_enable'] = use_draco
        if use_draco:
            export_settings['export_draco_mesh_compression_level'] = draco_level
        
        try:
            # Export the model
            bpy.ops.export_scene.gltf(
                filepath=output_path,
                **export_settings
            )
            
            # Check file size
            if os.path.exists(output_path):
                size = os.path.getsize(output_path)
                print(f"   ✅ {name}: {size:,} bytes → {output_path}")
            else:
                print(f"   ❌ {name}: Export failed")
                
        except Exception as e:
            print(f"   ❌ {name}: Error - {e}")
    
    print("\n✨ Export complete!")
    print(f"📁 Files saved to: {export_base}")
    
    # Also export a version with all objects if multiple were selected
    if len(selected_objects) > 1:
        print("\n📦 Exporting complete model with all selected parts...")
        
        # Select all originally selected objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in selected_objects:
            obj.select_set(True)
        
        output_path = os.path.join(export_base, "bello_complete.glb")
        
        try:
            bpy.ops.export_scene.gltf(
                filepath=output_path,
                export_format='GLB',
                export_yup=True,
                export_selected=True,
                export_draco_mesh_compression_enable=True,
                export_draco_mesh_compression_level=6
            )
            
            size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
            print(f"   ✅ Complete model: {size:,} bytes")
        except Exception as e:
            print(f"   ❌ Complete export failed: {e}")

print("\n" + "="*60)
print("🎮 Ready for VetScan Pro!")
print("💡 Refresh your browser to see the new model")
print("="*60)