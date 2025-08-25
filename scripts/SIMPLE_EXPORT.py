"""
🐕 SUPER SIMPLE EXPORT - KOPIERE DIESES IN BLENDER!
"""

import bpy

# EINFACHER EXPORT - NUR 1 BEFEHL!
bpy.ops.export_scene.gltf(
    filepath="/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/dog.glb",
    export_format='GLB'
)

print("✅ FERTIG! Datei exportiert nach watched_exports/dog.glb")