#!/usr/bin/env python3
"""
Create Donut via MCP - Reproduce the "Glücksfall" donut scenario
This script uses the existing MCP infrastructure to:
1. Get scene information
2. Remove all mesh objects  
3. Create a donut (torus) with chocolate icing and colorful sprinkles
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
        print(f"Error connecting to MCP: {e}")
        return None

print("🍩 Creating Donut via MCP - Reproducing the 'Glücksfall' scenario...\n")

# Step 1: Get scene information
print("Step 1: Getting scene information...")
scene_info_code = '''
import bpy

print("\\n=== SCENE INFORMATION ===")
print(f"Active scene: {bpy.context.scene.name}")
print(f"Total objects: {len(bpy.data.objects)}")

# List all objects
for obj in bpy.data.objects:
    print(f"  - {obj.name} ({obj.type})")

# List mesh objects specifically
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"\\nMesh objects: {len(mesh_objects)}")
for obj in mesh_objects:
    print(f"  - {obj.name} (vertices: {len(obj.data.vertices)})")

print("=== END SCENE INFO ===\\n")
'''

response = execute_in_blender(scene_info_code)
if response:
    try:
        result = json.loads(response)
        if 'result' in result:
            print(result['result'])
    except:
        print(response[:1000])

print("\nStep 2: Removing all mesh objects...")

# Step 2: Remove all mesh objects
clear_scene_code = '''
import bpy

print("\\n=== CLEARING SCENE ===")
# Select all mesh objects
bpy.ops.object.select_all(action='DESELECT')
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

print(f"Removing {len(mesh_objects)} mesh objects...")
for obj in mesh_objects:
    bpy.data.objects.remove(obj, do_unlink=True)

print(f"Scene cleared! Remaining objects: {len(bpy.data.objects)}")
print("=== SCENE CLEARED ===\\n")
'''

response = execute_in_blender(clear_scene_code)
if response:
    try:
        result = json.loads(response)
        if 'result' in result:
            print(result['result'])
    except:
        print(response[:500])

print("\nStep 3: Creating the 'Glücksfall' donut...")

# Step 3: Create donut with chocolate icing and sprinkles
donut_creation_code = '''
import bpy
import bmesh
import mathutils
from mathutils import Vector
import random

print("\\n=== CREATING GLÜCKSFALL DONUT ===")

# Create the base donut (torus)
bpy.ops.mesh.primitive_torus_add(
    location=(0, 0, 0),
    major_radius=2.0,
    minor_radius=0.8,
    major_segments=48,
    minor_segments=24
)

donut = bpy.context.active_object
donut.name = "Glücksfall_Donut"
print("✅ Base donut created!")

# Create chocolate icing material
icing_material = bpy.data.materials.new(name="Chocolate_Icing")
icing_material.use_nodes = True
bsdf = icing_material.node_tree.nodes["Principled BSDF"]

# Chocolate brown color
bsdf.inputs[0].default_value = (0.2, 0.1, 0.05, 1.0)  # Base Color (dark brown)
bsdf.inputs[1].default_value = 0.3  # Metallic
bsdf.inputs[7].default_value = 0.8  # Roughness

# Apply icing material to donut
donut.data.materials.append(icing_material)
print("✅ Chocolate icing material applied!")

# Create colorful sprinkles
sprinkle_colors = [
    (1.0, 0.2, 0.2, 1.0),  # Red
    (0.2, 1.0, 0.2, 1.0),  # Green  
    (0.2, 0.2, 1.0, 1.0),  # Blue
    (1.0, 1.0, 0.2, 1.0),  # Yellow
    (1.0, 0.2, 1.0, 1.0),  # Magenta
    (0.2, 1.0, 1.0, 1.0),  # Cyan
]

print("Creating colorful sprinkles...")
for i in range(200):  # 200 sprinkles
    # Create small cylinder for sprinkle
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=0.15,
        location=(0, 0, 10)  # Start above donut
    )
    
    sprinkle = bpy.context.active_object
    sprinkle.name = f"Sprinkle_{i:03d}"
    
    # Random position on top of donut
    angle = random.uniform(0, 6.28318)  # 2*pi
    distance = random.uniform(1.2, 2.8)  # Within donut radius
    x = distance * mathutils.Matrix.Rotation(angle, 4, 'Z')[0][0]
    y = distance * mathutils.Matrix.Rotation(angle, 4, 'Z')[1][0]
    z = 0.9 + random.uniform(-0.1, 0.1)  # Slightly above donut
    
    sprinkle.location = (x, y, z)
    
    # Random rotation
    sprinkle.rotation_euler = (
        random.uniform(0, 6.28318),
        random.uniform(0, 6.28318), 
        random.uniform(0, 6.28318)
    )
    
    # Create and assign random colored material
    color = random.choice(sprinkle_colors)
    sprinkle_material = bpy.data.materials.new(name=f"Sprinkle_Color_{i}")
    sprinkle_material.use_nodes = True
    sprinkle_bsdf = sprinkle_material.node_tree.nodes["Principled BSDF"]
    sprinkle_bsdf.inputs[0].default_value = color
    sprinkle_bsdf.inputs[1].default_value = 0.1  # Less metallic
    sprinkle_bsdf.inputs[7].default_value = 0.2  # More glossy
    
    sprinkle.data.materials.append(sprinkle_material)

print("✅ 200 colorful sprinkles added!")

# Add some lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.active_object
sun.data.energy = 3.0
print("✅ Lighting added!")

# Position camera for nice view
if bpy.data.objects.get("Camera"):
    camera = bpy.data.objects["Camera"]
    camera.location = (7, -7, 5)
    camera.rotation_euler = (1.1, 0, 0.785)  # Look at donut
    print("✅ Camera positioned!")

print("\\n🍩 GLÜCKSFALL DONUT COMPLETE! 🍩")
print("The dog has been transformed into a delicious donut!")
print(f"Created: 1 chocolate donut + 200 colorful sprinkles")
print("=== DONUT CREATION FINISHED ===\\n")
'''

response = execute_in_blender(donut_creation_code)
if response:
    try:
        result = json.loads(response)
        if 'result' in result:
            print(result['result'])
    except:
        print(response[:1000])

print("\n🎉 Donut creation complete!")
print("The 'Glücksfall' scenario has been reproduced - the dog has been transformed into a donut!")

# Optional: Export the donut
print("\nExporting the donut...")
export_code = '''
import bpy
from pathlib import Path

export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_dir.mkdir(exist_ok=True)

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export the donut scene
export_file = export_dir / 'glucksfall_donut.glb'
bpy.ops.export_scene.gltf(
    filepath=str(export_file),
    export_format='GLB',
    export_apply=True,
    export_draco_mesh_compression_enable=True
)

print(f"✅ Donut exported to: {export_file.name}")
'''

response = execute_in_blender(export_code)
if response:
    try:
        result = json.loads(response)
        if 'result' in result:
            print(result['result'])
    except:
        print(response[:500])