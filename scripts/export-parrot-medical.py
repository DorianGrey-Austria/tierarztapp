#!/usr/bin/env python3
"""
Export Parrot Medical Model to GLB - VetScan Pro 3000
Exports the created parrot model with all medical materials to GLB format
"""

import bpy
import os

def export_parrot_glb():
    """Export parrot model to GLB format"""
    
    # Set up export path
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/parrot/parrot_medical.glb"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    print(f"Exporting parrot model to: {export_path}")
    
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Export as GLB with medical materials
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        check_existing=False,
        export_format='GLB',
        use_selection=True,
        export_materials='EXPORT',
        export_colors=True,
        export_cameras=False,
        export_lights=False,
        export_texcoords=True,
        export_normals=True,
        export_draco_mesh_compression_enable=False,
        export_tangents=False,
        export_yup=True
    )
    
    print(f"✅ Parrot medical model exported successfully!")
    
    # Get file info
    if os.path.exists(export_path):
        file_size = os.path.getsize(export_path) / (1024 * 1024)  # MB
        print(f"📁 File size: {file_size:.2f} MB")
        
        # Count objects and materials
        mesh_count = len([obj for obj in bpy.context.scene.objects if obj.type == 'MESH'])
        material_count = len(bpy.data.materials)
        
        print(f"📊 Model statistics:")
        print(f"   - Mesh objects: {mesh_count}")
        print(f"   - Materials: {material_count}")
        print(f"   - Polygon count: {sum(len(obj.data.polygons) for obj in bpy.context.scene.objects if obj.type == 'MESH')}")
    
    return export_path

if __name__ == "__main__":
    export_path = export_parrot_glb()
    print(f"🦜 Medical Parrot Model ready for VetScan Pro 3000!")
    print(f"📍 Location: {export_path}")