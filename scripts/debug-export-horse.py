#!/usr/bin/env python3
"""
🔍 DEBUG HORSE EXPORT
Check what happened with the export and retry if needed
"""

import socket
import json
import os
from pathlib import Path

def execute_blender_code(code):
    """Execute Python code in Blender via MCP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect(('localhost', 9876))
        
        command = {
            "method": "execute_blender_code",
            "params": {"code": code}
        }
        
        message = json.dumps(command) + '\n'
        sock.send(message.encode())
        
        response = sock.recv(65536).decode()
        sock.close()
        
        return response
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

# Check what objects exist in Blender
print("🔍 Checking Blender scene objects...")

check_code = """
import bpy
from pathlib import Path

print("=== BLENDER SCENE ANALYSIS ===")

# List all objects
print(f"Total objects in scene: {len(bpy.data.objects)}")
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        polys = len(obj.data.polygons)
        print(f"  📦 {obj.name}: {polys} polygons")

# Check materials
print(f"\\nTotal materials: {len(bpy.data.materials)}")
for mat in bpy.data.materials:
    print(f"  🎨 {mat.name}")

# Create export directory
export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse')
export_dir.mkdir(parents=True, exist_ok=True)
print(f"\\n📁 Created export directory: {export_dir}")

# Try export again with debugging
horse_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.name.startswith('Horse')]
print(f"\\n🐎 Found {len(horse_objects)} horse objects to export")

if horse_objects:
    # Select all horse objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in horse_objects:
        obj.select_set(True)
        print(f"  ✓ Selected: {obj.name}")
    
    # Export
    export_file = export_dir / 'horse_medical.glb'
    print(f"\\n📦 Attempting export to: {export_file}")
    
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(export_file),
            export_format='GLB',
            use_selection=True,
            export_apply=True,
            export_draco_mesh_compression_enable=True,
            export_materials='EXPORT'
        )
        
        # Check if file was created
        if export_file.exists():
            size = export_file.stat().st_size
            print(f"✅ SUCCESS! File exported: {export_file.name} ({size} bytes)")
        else:
            print("❌ Export failed - file not created")
    
    except Exception as e:
        print(f"❌ Export error: {e}")

else:
    print("❌ No horse objects found to export!")
    print("   Creating a simple test horse...")
    
    # Create a simple horse if none exists
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    body = bpy.context.active_object
    body.name = "Horse_Body_Simple"
    body.scale = (2, 1, 1)
    
    print("✅ Simple horse body created")
"""

result = execute_blender_code(check_code)
if result:
    print(result)
else:
    print("❌ Could not connect to Blender MCP")

# Check if file exists on filesystem
export_path = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse/horse_medical.glb')
if export_path.exists():
    size = export_path.stat().st_size
    print(f"\n✅ File exists on filesystem: {export_path} ({size} bytes)")
else:
    print(f"\n❌ File not found: {export_path}")
    
    # Check parent directories
    parent = export_path.parent
    if parent.exists():
        print(f"📁 Parent directory exists: {parent}")
        print("Contents:")
        for item in parent.iterdir():
            print(f"  - {item.name}")
    else:
        print(f"❌ Parent directory doesn't exist: {parent}")