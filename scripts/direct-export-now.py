#!/usr/bin/env python3
"""
Direkter Export über MCP - Vereinfachte Version
"""

import socket
import json
import time

def send_to_blender(code):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect(('localhost', 9876))
        
        command = {
            "method": "execute_blender_code",
            "params": {"code": code}
        }
        
        sock.send((json.dumps(command) + '\n').encode())
        response = sock.recv(65536).decode()
        sock.close()
        
        return response
    except Exception as e:
        return f"Error: {e}"

print("🎨 EXPORTIERE KREATIVEN HUND DIREKT...")

# Simplified export
export_code = """
import bpy

# Select all
bpy.ops.object.select_all(action='SELECT')

# Direct export
path = '/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/dog/dog_creative.glb'
bpy.ops.export_scene.gltf(
    filepath=path,
    export_format='GLB',
    use_selection=True
)

print(f"EXPORTED TO: {path}")
"""

result = send_to_blender(export_code)
print(f"Result: {result[:200] if result else 'No response'}")

# Verify file
import os
path = '/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/dog/dog_creative.glb'
if os.path.exists(path):
    size = os.path.getsize(path) / 1024
    print(f"✅ SUCCESS! File created: {size:.1f} KB")
else:
    print("⚠️ File not found yet")