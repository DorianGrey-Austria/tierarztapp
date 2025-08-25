import bpy
import os

print("📦 Fixed GLB Export for Bello")

def export_bello_fixed():
    """Export Bello with correct Blender 4.4 parameters"""
    
    # Create export directory
    export_dir = "assets/models/animals/bello"
    os.makedirs(export_dir, exist_ok=True)
    print(f"   Created directory: {export_dir}")
    
    # Export variants with corrected parameters
    variants = [
        {'name': 'bello_high', 'objects': ['Bello_Body', 'Bello_Head']},
        {'name': 'bello_medium', 'objects': ['Bello_Med_Body', 'Bello_Med_Head']},  
        {'name': 'bello_xray', 'objects': ['Bello_Body', 'Skeleton_Vertebra']},
        {'name': 'bello_medical', 'objects': ['Bello_Body', 'Medical_Heart']}
    ]
    
    for variant in variants:
        print(f"   Exporting {variant['name']}...")
        
        # Select relevant objects
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select all Bello objects for comprehensive export
        for obj in bpy.data.objects:
            if (obj.name.startswith('Bello_') or 
                obj.name.startswith('Medical_') or 
                obj.name.startswith('Skeleton_')):
                if obj.type == 'MESH':
                    obj.select_set(True)
        
        # Export path
        export_path = f"{export_dir}/{variant['name']}.glb"
        
        try:
            # Corrected GLB export parameters for Blender 4.4
            bpy.ops.export_scene.gltf(
                filepath=export_path,
                use_selection=True,
                export_format='GLB',
                export_materials='EXPORT',
                export_texcoords=True,
                export_normals=True,
                export_tangents=False,
                export_animations=False,
                export_cameras=False,
                export_lights=False,
                export_apply=True
            )
            print(f"      ✅ Successfully exported: {variant['name']}.glb")
            
        except Exception as e:
            print(f"      ❌ Export failed for {variant['name']}: {str(e)}")
    
    print("   ✅ Fixed export complete")

def create_simple_blend_file():
    """Save the current scene as a .blend file for manual export"""
    
    blend_path = "assets/models/animals/bello/bello_complete.blend"
    
    try:
        bpy.ops.wm.save_as_mainfile(filepath=blend_path)
        print(f"   ✅ Saved Blender file: {blend_path}")
        print("   💡 You can manually export GLB files from this .blend file")
    except Exception as e:
        print(f"   ❌ Failed to save .blend file: {str(e)}")

# Execute fixed export
export_bello_fixed()
create_simple_blend_file()

print("🎉 FIXED EXPORT COMPLETE!")
print("📁 Files available for manual export if needed")