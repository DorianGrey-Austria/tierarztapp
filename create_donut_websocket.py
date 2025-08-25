#!/usr/bin/env python3
"""
Create Donut via WebSocket MCP - Reproduce the "Glücksfall" donut scenario
This script uses WebSocket to connect to the Blender MCP server and:
1. Get scene information
2. Remove all mesh objects  
3. Create a donut (torus) with chocolate icing and colorful sprinkles
"""

import asyncio
import websockets
import json

async def send_mcp_command(websocket, method, params=None):
    """Send MCP command and get response"""
    request = {
        "id": 1,
        "method": method,
        "params": params or {}
    }
    
    await websocket.send(json.dumps(request))
    response = await websocket.recv()
    return json.loads(response)

async def create_donut_via_mcp():
    """Main function to create donut via MCP WebSocket"""
    
    print("🍩 Creating Donut via WebSocket MCP - Reproducing the 'Glücksfall' scenario...\n")
    
    try:
        # Connect to Blender MCP WebSocket server
        uri = "ws://localhost:8765"
        print(f"Connecting to {uri}...")
        
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to Blender MCP Server!")
            
            # Step 1: Get scene information
            print("\n=== Step 1: Getting scene information ===")
            response = await send_mcp_command(websocket, "get_scene_info")
            
            if response.get('result'):
                scene_info = response['result']
                print(f"Objects in scene: {scene_info.get('objects', [])}")
                print(f"Meshes: {scene_info.get('meshes', [])}")
                print(f"Materials: {scene_info.get('materials', [])}")
            
            # Step 2: Remove all mesh objects
            print("\n=== Step 2: Clearing scene of mesh objects ===")
            clear_code = '''
import bpy

print("\\n=== CLEARING SCENE ===")
# Select all mesh objects and delete them
bpy.ops.object.select_all(action='DESELECT')
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

print(f"Removing {len(mesh_objects)} mesh objects...")
for obj in mesh_objects:
    bpy.data.objects.remove(obj, do_unlink=True)

print(f"Scene cleared! Remaining objects: {len(bpy.data.objects)}")
print("=== SCENE CLEARED ===")
'''
            
            response = await send_mcp_command(websocket, "execute_blender_code", {"code": clear_code})
            if response.get('result', {}).get('success'):
                print("✅ Scene cleared successfully!")
            else:
                print(f"⚠️ Clear scene result: {response}")
            
            # Step 3: Create the Glücksfall donut
            print("\n=== Step 3: Creating the 'Glücksfall' donut ===")
            donut_code = '''
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
sprinkles_collection = []

for i in range(150):  # 150 sprinkles
    # Create small cylinder for sprinkle
    bpy.ops.mesh.primitive_cylinder_add(
        radius=0.02,
        depth=0.15,
        location=(0, 0, 10)  # Start above donut
    )
    
    sprinkle = bpy.context.active_object
    sprinkle.name = f"Sprinkle_{i:03d}"
    sprinkles_collection.append(sprinkle)
    
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

print(f"✅ {len(sprinkles_collection)} colorful sprinkles added!")

# Add some lighting for better visibility
if bpy.data.objects.get("Light"):
    light = bpy.data.objects["Light"]
    light.data.energy = 5.0
else:
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 5.0
    print("✅ Lighting improved!")

# Position camera for nice view
if bpy.data.objects.get("Camera"):
    camera = bpy.data.objects["Camera"]
    camera.location = (7, -7, 5)
    camera.rotation_euler = (1.1, 0, 0.785)  # Look at donut
    print("✅ Camera positioned!")

print("\\n🍩 GLÜCKSFALL DONUT COMPLETE! 🍩")
print("The dog has been transformed into a delicious donut!")
print(f"Created: 1 chocolate donut + {len(sprinkles_collection)} colorful sprinkles")
print("=== DONUT CREATION FINISHED ===")
'''
            
            response = await send_mcp_command(websocket, "execute_blender_code", {"code": donut_code})
            if response.get('result', {}).get('success'):
                print("✅ Donut created successfully!")
                print("Output:", response['result'].get('output', ''))
            else:
                print(f"⚠️ Donut creation result: {response}")
            
            # Step 4: Get final scene info
            print("\n=== Step 4: Final scene verification ===")
            response = await send_mcp_command(websocket, "get_scene_info")
            
            if response.get('result'):
                scene_info = response['result']
                print(f"Final objects: {scene_info.get('objects', [])}")
                print(f"Final meshes: {scene_info.get('meshes', [])}")
                print(f"Materials created: {len(scene_info.get('materials', []))}")
            
            # Step 5: Export the donut
            print("\n=== Step 5: Exporting the Glücksfall donut ===")
            export_params = {
                "filepath": "/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/glucksfall_donut.glb",
                "quality": "high"
            }
            
            response = await send_mcp_command(websocket, "export_gltf", export_params)
            if response.get('result', {}).get('success'):
                export_info = response['result']
                print(f"✅ Donut exported to: {export_info['filepath']}")
                print(f"File size: {export_info['file_size']} bytes")
            else:
                print(f"⚠️ Export result: {response}")
            
            # Step 6: Take a screenshot
            print("\n=== Step 6: Taking a screenshot ===")
            screenshot_params = {
                "filepath": "/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/glucksfall_donut.png",
                "max_size": 1024
            }
            
            response = await send_mcp_command(websocket, "get_viewport_screenshot", screenshot_params)
            if response.get('result', {}).get('success'):
                screenshot_info = response['result']
                print(f"✅ Screenshot saved to: {screenshot_info['filepath']}")
                print(f"Image size: {screenshot_info['width']}x{screenshot_info['height']}")
            else:
                print(f"⚠️ Screenshot result: {response}")
            
    except websockets.exceptions.ConnectionRefused:
        print("❌ Could not connect to Blender MCP server!")
        print("Make sure the MCP server is running on ws://localhost:8765")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n🎉 Glücksfall donut creation complete!")
    print("The dog has been successfully transformed into a donut with chocolate icing and sprinkles!")

if __name__ == "__main__":
    # Install websockets if not available
    try:
        import websockets
    except ImportError:
        print("Installing websockets...")
        import subprocess
        subprocess.check_call(["pip3", "install", "websockets"])
        import websockets
    
    asyncio.run(create_donut_via_mcp())