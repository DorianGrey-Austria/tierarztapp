"""
BLENDER AUTO-EXPORT SCRIPT
===========================
Füge dieses Script in Blender's Text Editor ein und führe es aus.
Es exportiert automatisch dein aktuelles Modell für VetScan Pro.

So geht's:
1. In Blender: Scripting Tab öffnen
2. Text → New → Paste dieses Script
3. Run Script (oder Alt+P)
4. Modell wird automatisch exportiert!
"""

import bpy
import os
from pathlib import Path

def export_for_vetscan():
    """Export current Blender scene for VetScan Pro integration"""
    
    # Export-Pfad
    export_dir = Path("/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports")
    export_dir.mkdir(exist_ok=True)
    
    # Dateiname mit Timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_file = export_dir / f"bello_export_{timestamp}.glb"
    
    print("=" * 50)
    print("🐕 VetScan Pro - Blender Export")
    print("=" * 50)
    
    # Sammle Scene Info
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    total_verts = sum(len(obj.data.vertices) for obj in mesh_objects)
    total_faces = sum(len(obj.data.polygons) for obj in mesh_objects)
    
    print(f"📊 Scene Statistics:")
    print(f"   Mesh Objects: {len(mesh_objects)}")
    print(f"   Total Vertices: {total_verts:,}")
    print(f"   Total Faces: {total_faces:,}")
    
    # Export Settings für optimale Web-Performance
    try:
        bpy.ops.export_scene.gltf(
            filepath=str(export_file),
            
            # Format
            export_format='GLB',  # Binary format
            
            # Include
            use_selection=False,  # Export entire scene
            export_cameras=False,
            export_lights=False,
            
            # Mesh
            export_apply_modifiers=True,
            export_colors=True,
            export_normals=True,
            export_tangents=True,
            export_texcoords=True,
            
            # Materials
            export_materials='EXPORT',
            export_image_format='AUTO',
            
            # Compression
            export_draco_mesh_compression=False,  # Disable for compatibility
            
            # Transform
            export_yup=True,  # Y-up for Three.js
            
            # Animations (if any)
            export_animations=True,
            export_frame_range=False,
            
            # Extras
            export_extras=False,
            export_copyright="VetScan Pro 3000"
        )
        
        print(f"\n✅ Export successful!")
        print(f"📁 File: {export_file.name}")
        print(f"📊 Size: {os.path.getsize(export_file) / 1024:.1f} KB")
        
        # Erstelle auch Quick-Access Symlink
        quick_link = export_dir / "latest_export.glb"
        if quick_link.exists():
            quick_link.unlink()
        quick_link.symlink_to(export_file.name)
        print(f"🔗 Quick link: latest_export.glb")
        
        print("\n🌐 Next steps:")
        print("1. File is ready for import")
        print("2. Open: http://localhost:8081/vetscan-bello-3d-v7.html")
        print("3. Model will load automatically!")
        
        # Optional: Direkt im Browser öffnen
        # import webbrowser
        # webbrowser.open("http://localhost:8081/vetscan-bello-3d-v7.html")
        
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        print("\n💡 Troubleshooting:")
        print("- Check if you have objects in scene")
        print("- Ensure write permissions to export folder")
        print("- Try manual export: File → Export → glTF 2.0")
    
    print("\n" + "=" * 50)
    return export_file

# Führe Export aus
if __name__ == "__main__":
    export_file = export_for_vetscan()
    
    # Optional: Automatischer Re-Export bei Änderungen
    """
    # Uncomment für Auto-Export alle 10 Sekunden:
    import time
    def auto_export():
        export_for_vetscan()
        return 10.0  # Repeat every 10 seconds
    
    bpy.app.timers.register(auto_export)
    print("⏰ Auto-export activated (every 10s)")
    """