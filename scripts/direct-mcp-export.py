#!/usr/bin/env python3
"""
Direct MCP Export - Trigger export directly via MCP
"""

import socket
import json
import time
from pathlib import Path

def execute_in_blender(code):
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
        
        response = sock.recv(32768).decode()
        sock.close()
        
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

print("🐕 Triggering Direct Export via MCP...\n")

# The complete export code
export_code = '''
import bpy
from pathlib import Path
from datetime import datetime

print("\\n🐕 STARTING DOG EXPORT...")

# Setup paths
export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_dir.mkdir(exist_ok=True)
timestamp = datetime.now().strftime("%H%M%S")

# Get all mesh objects
meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"Found {len(meshes)} mesh objects")

if not meshes:
    print("No mesh objects found!")
else:
    # Select all meshes
    bpy.ops.object.select_all(action='DESELECT')
    for obj in meshes:
        obj.select_set(True)
    
    # Export as single file first
    export_file = export_dir / f'dog_export_{timestamp}.glb'
    
    print(f"Exporting to: {export_file.name}")
    
    bpy.ops.export_scene.gltf(
        filepath=str(export_file),
        export_format='GLB',
        use_selection=True,
        export_apply=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6
    )
    
    print(f"✅ Exported: {export_file.name}")
    
    # Also export quality variants
    qualities = {'high': 1.0, 'medium': 0.5, 'low': 0.25}
    
    for quality, ratio in qualities.items():
        # Clone and decimate if needed
        if ratio < 1.0:
            # Add decimate modifier to largest mesh
            largest = max(meshes, key=lambda x: len(x.data.vertices))
            mod = largest.modifiers.new('TEMP_DECIMATE', 'DECIMATE')
            mod.ratio = ratio
        
        quality_file = export_dir / f'dog_{quality}_{timestamp}.glb'
        
        bpy.ops.export_scene.gltf(
            filepath=str(quality_file),
            export_format='GLB',
            use_selection=True,
            export_apply=True,
            export_draco_mesh_compression_enable=True
        )
        
        print(f"✅ Exported: {quality_file.name}")
        
        # Remove modifier
        if ratio < 1.0:
            largest.modifiers.remove(mod)
    
    print("\\n🎉 ALL EXPORTS COMPLETE!")
'''

print("Sending export command to Blender...")
response = execute_in_blender(export_code)

if response:
    print("✅ Export command executed!")
    print("\nBlender response:")
    try:
        result = json.loads(response)
        if 'result' in result:
            print(result['result'])
    except:
        print(response[:500])

# Wait and check for files
print("\n⏳ Waiting for export to complete...")
time.sleep(3)

export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
glb_files = list(export_dir.glob('*.glb'))

if glb_files:
    print("\n✅ Export successful! Found files:")
    for f in glb_files:
        size_kb = f.stat().st_size / 1024
        print(f"  • {f.name} ({size_kb:.1f} KB)")
else:
    print("\n⚠️ No files found yet. Check Blender console for errors.")
    print("You may need to run the export manually in Blender.")