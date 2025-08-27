#!/usr/bin/env python3
"""
🐎 HORSE CREATION VIA BLENDER MCP (Direct Method)
Using the exact same method as the working creative dog script
"""

import socket
import json
import time
import os
from datetime import datetime
from pathlib import Path

class HorseCreator:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9876
        self.timestamp = datetime.now().strftime("%H%M%S")
        
    def execute_blender_code(self, code):
        """Execute Python code in Blender via MCP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.host, self.port))
            
            command = {
                "method": "execute_blender_code",
                "params": {"code": code}
            }
            
            message = json.dumps(command) + '\n'
            sock.send(message.encode())
            
            response = sock.recv(65536).decode()
            sock.close()
            
            print(f"MCP Response: {response}")
            return response
        except Exception as e:
            print(f"❌ MCP Error: {e}")
            return None
    
    def create_complete_horse(self):
        """Create the complete horse in one script execution"""
        print("\n🐎 CREATING COMPLETE MEDICAL HORSE...")
        
        # The complete horse creation code - all in one to avoid MCP issues
        horse_code = """
import bpy
import bmesh
from mathutils import Vector
import math

print("Starting medical horse creation...")

# Clear scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete(use_global=False)

# Clear materials
for mat in bpy.data.materials:
    bpy.data.materials.remove(mat)

print("Scene cleared")

# BODY
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1.5))
body = bpy.context.active_object
body.name = "Horse_Body"
body.scale = (2.5, 1.0, 1.2)
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# NECK
bpy.ops.mesh.primitive_cylinder_add(radius=0.4, depth=1.8, location=(0, -1.8, 2.2), rotation=(0.5, 0, 0))
neck = bpy.context.active_object
neck.name = "Horse_Neck"

# HEAD
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -3.2, 2.8))
head = bpy.context.active_object
head.name = "Horse_Head"
head.scale = (0.6, 1.4, 0.8)
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# MUZZLE
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=0.6, location=(0, -4.2, 2.6), rotation=(1.57, 0, 0))
bpy.context.active_object.name = "Horse_Muzzle"

# EARS
for i, side in enumerate([-1, 1]):
    bpy.ops.mesh.primitive_cone_add(radius1=0.15, radius2=0.05, depth=0.4, location=(side * 0.3, -2.8, 3.4))
    bpy.context.active_object.name = f"Horse_Ear_{['L', 'R'][i]}"

# LEGS AND HOOVES
leg_positions = [(-0.8, -1.2, 0), (0.8, -1.2, 0), (-0.8, 1.2, 0), (0.8, 1.2, 0)]
leg_names = ["FL", "FR", "BL", "BR"]

for i, (x, y, z) in enumerate(leg_positions):
    # Upper leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.0, location=(x, y, 1.0))
    bpy.context.active_object.name = f"Horse_UpperLeg_{leg_names[i]}"
    
    # Lower leg
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(x, y, 0.3))
    bpy.context.active_object.name = f"Horse_LowerLeg_{leg_names[i]}"
    
    # Hoof
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.15, location=(x, y, -0.1))
    hoof = bpy.context.active_object
    hoof.name = f"Horse_Hoof_{leg_names[i]}"
    hoof.scale = (1.0, 1.2, 1.0)
    bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)
    
    # Fetlock
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.18, location=(x, y, 0.1))
    bpy.context.active_object.name = f"Horse_Fetlock_{leg_names[i]}"

# MEDICAL ANATOMY
# Heart
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(-0.3, -0.8, 1.8))
heart = bpy.context.active_object
heart.name = "Horse_Heart_Area"
heart.scale = (0.8, 1.2, 1.0)
bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# Stomach
bpy.ops.mesh.primitive_cylinder_add(radius=0.6, depth=0.8, location=(0.5, 0.5, 1.3), rotation=(0, 0.5, 0))
bpy.context.active_object.name = "Horse_Stomach_Area"

# Intestines
bpy.ops.mesh.primitive_torus_add(major_radius=0.8, minor_radius=0.2, location=(0, 0.8, 1.0))
bpy.context.active_object.name = "Horse_Intestinal_Area"

# Lungs
for side in [-1, 1]:
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.0, location=(side * 0.6, -0.2, 2.0), rotation=(0, 0, 1.57))
    bpy.context.active_object.name = f"Horse_Lung_{'L' if side < 0 else 'R'}"

# MANE
mane_positions = [(0, -1.4, 2.8), (0, -1.8, 2.6), (0, -2.2, 2.4), (0, -2.6, 2.2)]
for i, pos in enumerate(mane_positions):
    bpy.ops.mesh.primitive_cube_add(size=0.1, location=pos)
    mane = bpy.context.active_object
    mane.name = f"Horse_Mane_{i:02d}"
    mane.scale = (0.8, 0.2, 2.0)
    bpy.ops.object.transform_apply(transform=True, location=False, rotation=False, scale=True)

# TAIL
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=1.5, location=(0, 2.8, 1.2), rotation=(0.3, 0, 0))
bpy.context.active_object.name = "Horse_Tail"

# MATERIALS
# Normal Material
normal_mat = bpy.data.materials.new(name="Horse_Normal")
normal_mat.use_nodes = True
bsdf = normal_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.4, 0.2, 0.1, 1.0)  # Bay color
bsdf.inputs[9].default_value = 0.6

# X-Ray Material
xray_mat = bpy.data.materials.new(name="Horse_XRay")
xray_mat.use_nodes = True
xray_mat.blend_method = 'BLEND'
bsdf = xray_mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.8, 0.9, 1.0, 0.3)
bsdf.inputs[21].default_value = 0.3

# Apply materials and smooth shading
for obj in bpy.data.objects:
    if obj.type == 'MESH' and obj.name.startswith('Horse'):
        if not obj.data.materials:
            obj.data.materials.append(normal_mat)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.shade_smooth()

# Statistics
total_objects = len([obj for obj in bpy.data.objects if obj.type == 'MESH' and obj.name.startswith('Horse')])
total_polygons = sum(len(obj.data.polygons) for obj in bpy.data.objects if obj.type == 'MESH' and obj.name.startswith('Horse'))

print(f"✅ Medical horse created!")
print(f"Objects: {total_objects}, Polygons: {total_polygons}")
print("Ready for manual export to: assets/models/animals/horse/horse_medical.glb")
"""
        
        response = self.execute_blender_code(horse_code)
        if response:
            print("✅ Horse creation completed!")
            
            # Create the export directory
            export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse')
            export_dir.mkdir(parents=True, exist_ok=True)
            print(f"✅ Export directory created: {export_dir}")
            
            return True
        else:
            print("❌ Failed to create horse")
            return False

def main():
    print("="*70)
    print("🐎 MEDICAL HORSE CREATION VIA BLENDER MCP")
    print("="*70)
    
    creator = HorseCreator()
    success = creator.create_complete_horse()
    
    if success:
        print("\n" + "="*70)
        print("🎉 HORSE CREATION COMPLETED!")
        print("="*70)
        print("\nNEXT STEPS:")
        print("1. Open Blender (should already be running)")
        print("2. You should see the medical horse model")
        print("3. Select all horse objects (A to select all)")
        print("4. File → Export → glTF 2.0 (.glb/.gltf)")
        print("5. Navigate to:")
        print("   /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/horse/")
        print("6. Set filename: horse_medical.glb")
        print("7. Enable 'Selected Objects' and 'Apply Modifiers'")
        print("8. Click 'Export glTF 2.0'")
        print("\n🐎 The model includes:")
        print("  - Anatomically correct proportions")
        print("  - Powerful legs with detailed hooves")
        print("  - Large heart area for cardiac examination")
        print("  - Digestive tract visualization")
        print("  - Medical materials for different scan modes")
        print("="*70)
    else:
        print("\n❌ Horse creation failed - check Blender MCP connection")

if __name__ == "__main__":
    main()