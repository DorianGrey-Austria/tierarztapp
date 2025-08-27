#!/usr/bin/env python3
"""
Guinea Pig Medical Model Creator for VetScan Pro 3000
Creates medically accurate guinea pig with 5000-8000 polygons
Focus: Vitamin C dependency, dental health, cecotrophy
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector
import math
import os

def clear_scene():
    """Clear existing objects"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    print("🧹 Scene cleared")

def create_guinea_pig_body():
    """Create guinea pig body with accurate proportions"""
    # Guinea pigs are compact, barrel-shaped rodents
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, location=(0, 0, 0))
    body = bpy.context.active_object
    body.name = "GuineaPig_Body"
    
    # Guinea pig proportions: compact, wider than tall
    body.scale = (1.3, 0.9, 0.65)  # Length, width, height
    bpy.ops.object.transform_apply(transform=True, scale=True)
    
    # Add subdivision for medical detail
    bpy.context.view_layer.objects.active = body
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    
    # Shape the body to be more guinea pig-like
    bm = bmesh.from_mesh(body.data)
    bmesh.ops.smooth_vert(bm, verts=bm.verts, factor=0.5, repeat=1)
    bm.to_mesh(body.data)
    bm.free()
    
    bpy.ops.object.mode_set(mode='OBJECT')
    print("✅ Guinea pig body created")
    return body

def create_guinea_pig_head():
    """Create guinea pig head with distinctive features"""
    # Head is rounded, not as pointed as other rodents
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(1.1, 0, 0.1))
    head = bpy.context.active_object
    head.name = "GuineaPig_Head"
    
    # Guinea pig head proportions
    head.scale = (0.8, 1.0, 0.9)
    bpy.ops.object.transform_apply(transform=True, scale=True)
    
    # Add detail for medical scanning
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    print("✅ Guinea pig head created")
    return head

def create_guinea_pig_ears():
    """Create small guinea pig ears"""
    ears = []
    
    # Guinea pigs have small, rounded ears
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.12, 
            location=(1.2, side * 0.25, 0.25)
        )
        ear = bpy.context.active_object
        ear.name = f"GuineaPig_Ear_{'L' if side < 0 else 'R'}"
        
        # Scale to guinea pig ear proportions
        ear.scale = (0.6, 1.2, 0.4)
        bpy.ops.object.transform_apply(transform=True, scale=True)
        
        ears.append(ear)
    
    print("✅ Guinea pig ears created")
    return ears

def create_guinea_pig_teeth():
    """Create prominent incisors - key for guinea pig dental health"""
    teeth = []
    
    # Guinea pigs have continuously growing incisors (important medical feature)
    for side in [-1, 1]:
        # Upper incisors
        bpy.ops.mesh.primitive_cube_add(
            size=0.03,
            location=(1.35, side * 0.08, 0.05)
        )
        tooth = bpy.context.active_object
        tooth.name = f"GuineaPig_UpperIncisor_{'L' if side < 0 else 'R'}"
        tooth.scale = (1.5, 0.5, 0.8)
        bpy.ops.object.transform_apply(transform=True, scale=True)
        teeth.append(tooth)
        
        # Lower incisors
        bpy.ops.mesh.primitive_cube_add(
            size=0.025,
            location=(1.37, side * 0.08, -0.05)
        )
        tooth = bpy.context.active_object
        tooth.name = f"GuineaPig_LowerIncisor_{'L' if side < 0 else 'R'}"
        tooth.scale = (1.2, 0.5, 0.8)
        bpy.ops.object.transform_apply(transform=True, scale=True)
        teeth.append(tooth)
    
    print("✅ Guinea pig teeth created (continuous growth feature)")
    return teeth

def create_guinea_pig_legs():
    """Create short guinea pig legs"""
    legs = []
    
    # Guinea pigs have short, sturdy legs
    positions = [
        (0.6, -0.5, -0.5),   # Front left
        (0.6, 0.5, -0.5),    # Front right
        (-0.3, -0.5, -0.5),  # Back left
        (-0.3, 0.5, -0.5)    # Back right
    ]
    
    for i, pos in enumerate(positions):
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.08,
            depth=0.3,
            location=pos
        )
        leg = bpy.context.active_object
        leg.name = f"GuineaPig_Leg_{i+1}"
        
        # Rotate to proper angle
        leg.rotation_euler = (0, 0, 0)
        bpy.ops.object.transform_apply(transform=True, rotation=True)
        
        legs.append(leg)
    
    print("✅ Guinea pig legs created")
    return legs

def create_guinea_pig_feet():
    """Create guinea pig feet with toes"""
    feet = []
    
    # Guinea pigs have 4 toes front, 3 toes back
    foot_positions = [
        (0.6, -0.5, -0.65),   # Front left
        (0.6, 0.5, -0.65),    # Front right  
        (-0.3, -0.5, -0.65),  # Back left
        (-0.3, 0.5, -0.65)    # Back right
    ]
    
    for i, pos in enumerate(foot_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=0.1,
            location=pos
        )
        foot = bpy.context.active_object
        foot.name = f"GuineaPig_Foot_{i+1}"
        
        # Scale to guinea pig foot proportions
        foot.scale = (1.2, 0.8, 0.5)
        bpy.ops.object.transform_apply(transform=True, scale=True)
        
        feet.append(foot)
    
    print("✅ Guinea pig feet created")
    return feet

def create_digestive_system_markers():
    """Create internal markers for cecotrophy and vitamin C processing"""
    markers = []
    
    # Cecum marker (important for cecotrophy)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.15,
        location=(-0.2, 0, -0.2)
    )
    cecum = bpy.context.active_object
    cecum.name = "GuineaPig_Cecum_Marker"
    cecum.display_type = 'WIRE'  # Make it visible in wireframe for medical view
    markers.append(cecum)
    
    # Liver marker (vitamin C processing)
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=0.1,
        location=(0.3, 0.2, 0.1)
    )
    liver = bpy.context.active_object
    liver.name = "GuineaPig_Liver_Marker"
    liver.display_type = 'WIRE'
    markers.append(liver)
    
    print("✅ Digestive system markers created for medical visualization")
    return markers

def join_all_objects():
    """Join all objects into single mesh"""
    # Select all objects
    bpy.ops.object.select_all(action='SELECT')
    
    # Join all objects
    bpy.ops.object.join()
    
    # Rename final object
    guinea_pig = bpy.context.active_object
    guinea_pig.name = "GuineaPig_Medical_Complete"
    
    print("✅ All objects joined into single mesh")
    return guinea_pig

def optimize_geometry(obj):
    """Optimize geometry for 5000-8000 polygon target"""
    # Get current polygon count
    bpy.context.view_layer.objects.active = obj
    current_polys = len(obj.data.polygons)
    
    print(f"Current polygon count: {current_polys}")
    
    if current_polys > 8000:
        # Add decimate modifier to reduce polygons
        decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
        decimate.ratio = 7000 / current_polys  # Target 7000 polygons
        bpy.ops.object.modifier_apply(modifier=decimate.name)
        
        new_polys = len(obj.data.polygons)
        print(f"✅ Decimated to {new_polys} polygons")
    
    elif current_polys < 5000:
        # Add subdivision to increase detail
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.subdivide(number_cuts=1)
        bpy.ops.object.mode_set(mode='OBJECT')
        
        new_polys = len(obj.data.polygons)
        print(f"✅ Subdivided to {new_polys} polygons")
    
    return obj

def main():
    """Create complete guinea pig medical model"""
    print("🐹 Creating Medically Accurate Guinea Pig Model")
    print("=" * 50)
    
    # Clear scene
    clear_scene()
    
    # Create guinea pig parts
    body = create_guinea_pig_body()
    head = create_guinea_pig_head()
    ears = create_guinea_pig_ears()
    teeth = create_guinea_pig_teeth()
    legs = create_guinea_pig_legs()
    feet = create_guinea_pig_feet()
    digestive_markers = create_digestive_system_markers()
    
    # Join all parts
    final_model = join_all_objects()
    
    # Optimize geometry
    optimize_geometry(final_model)
    
    # Final polygon count
    final_polys = len(final_model.data.polygons)
    print(f"🎯 Final model: {final_polys} polygons")
    
    if 5000 <= final_polys <= 8000:
        print("✅ Polygon count within target range!")
    else:
        print("⚠️  Polygon count outside target range")
    
    print("\n🏥 Medical Features Included:")
    print("- Continuously growing incisors (dental health)")
    print("- Cecum markers (cecotrophy)")
    print("- Liver markers (vitamin C processing)")
    print("- Compact body structure")
    print("- Short legs (posture issues)")
    
    print("\n🎨 Ready for material creation...")
    
    return final_model

if __name__ == "__main__":
    main()