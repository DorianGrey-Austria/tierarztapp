#!/usr/bin/env python3
"""
Quick Blender Export via MCP
Simplified export script that works with MCP
"""

import socket
import json
import time
from datetime import datetime
from pathlib import Path

def send_blender_command(code):
    """Send Python code to Blender via MCP"""
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
        
        response = sock.recv(16384).decode()
        sock.close()
        
        print("✅ Command sent to Blender")
        return json.loads(response) if response else None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

print("🐕 Quick Blender Export for VetScan Pro\n")

# Step 1: Get Scene Objects
print("📊 Getting scene information...")
scene_code = """
import bpy
objects = [obj.name for obj in bpy.data.objects if obj.type == 'MESH']
print(f"Mesh objects in scene: {objects}")
for obj in objects:
    verts = len(bpy.data.objects[obj].data.vertices)
    faces = len(bpy.data.objects[obj].data.polygons)
    print(f"  - {obj}: {verts} vertices, {faces} faces")
"""

response = send_blender_command(scene_code)
if response:
    print("Scene info retrieved!\n")

# Step 2: Simple Export
print("📦 Exporting all mesh objects...")
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

export_code = f"""
import bpy
from pathlib import Path

# Export path
export_path = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_path.mkdir(exist_ok=True)

# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Export as GLB
output_file = export_path / 'dog_export_{timestamp}.glb'
print(f"Exporting to: {{output_file}}")

try:
    bpy.ops.export_scene.gltf(
        filepath=str(output_file),
        export_format='GLB',
        use_selection=True,
        export_apply=True
    )
    print(f"✅ Export successful: {{output_file.name}}")
except Exception as e:
    print(f"❌ Export failed: {{e}}")
"""

response = send_blender_command(export_code)

# Step 3: Check for file
print("\n📁 Checking export directory...")
export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_file = export_dir / f'dog_export_{timestamp}.glb'

# Wait a moment for export to complete
time.sleep(2)

if export_file.exists():
    size_kb = export_file.stat().st_size / 1024
    print(f"✅ Export successful: {export_file.name} ({size_kb:.1f} KB)")
    print(f"\n🎉 The export watcher will automatically import this file!")
    print(f"Check: assets/models/animals/dog/")
else:
    print(f"⚠️ Export file not found yet.")
    print(f"Expected: {export_file}")
    print("\nTry manual export in Blender:")
    print("1. File → Export → glTF 2.0")
    print(f"2. Save to: {export_dir}")
    print("3. Format: GLB")

print("\n🌐 Test URL: http://localhost:8080/vetscan-bello-3d-v7.html")