#!/usr/bin/env python3
"""
Simple Parrot GLB Export - VetScan Pro 3000
"""

import bpy
import os

def export_parrot():
    """Export parrot with minimal settings"""
    
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/parrot/parrot_medical.glb"
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    print(f"Exporting to: {export_path}")
    
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Simple GLB export
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB'
    )
    
    print("✅ Export complete!")
    
    # Check if file exists
    if os.path.exists(export_path):
        file_size = os.path.getsize(export_path) / (1024 * 1024)
        print(f"File size: {file_size:.2f} MB")
        
        mesh_count = len([obj for obj in bpy.context.scene.objects if obj.type == 'MESH'])
        total_polys = sum(len(obj.data.polygons) for obj in bpy.context.scene.objects if obj.type == 'MESH')
        
        print(f"Mesh objects: {mesh_count}")
        print(f"Total polygons: {total_polys}")
        print(f"Materials: {len(bpy.data.materials)}")
        
        return True
    else:
        print("❌ Export failed - file not found")
        return False

if __name__ == "__main__":
    success = export_parrot()
    if success:
        print("🦜 Parrot medical model ready for VetScan Pro 3000!")
    else:
        print("❌ Export failed")