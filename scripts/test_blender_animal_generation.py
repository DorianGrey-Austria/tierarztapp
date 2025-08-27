#!/usr/bin/env python3
"""
TEST BLENDER ANIMAL GENERATION
===============================
Quick test script to generate a realistic dog via Blender MCP
"""

import json
import socket
import time

def test_blender_mcp_connection():
    """Test if Blender MCP is running and responsive"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex(('localhost', 9876))
        sock.close()
        return result == 0
    except:
        return False

def generate_test_dog():
    """Generate a test dog with realistic materials"""
    
    print("🐕 VetScan Pro - Realistic Dog Generation Test")
    print("="*50)
    
    # Check connection
    if not test_blender_mcp_connection():
        print("❌ Blender MCP not running on port 9876")
        print("\n📝 To fix:")
        print("1. Open Blender")
        print("2. Go to Scripting tab")
        print("3. Run: bpy.ops.blendermcp.start_server()")
        return
        
    print("✅ Blender MCP connected")
    
    # Create simple generation code
    code = """
import bpy
import bmesh
from mathutils import Vector
import math

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

print("Creating realistic dog...")

# Create dog body using metaballs for organic shape
bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 0))
dog = bpy.context.object
dog.name = "Realistic_Dog"

mb = dog.data
mb.resolution = 0.05  # High resolution for smoothness
mb.render_resolution = 0.02

# Body parts
body = mb.elements.new()
body.co = (0, 0, 0)
body.radius = 0.8
body.stiffness = 1.0

# Chest
chest = mb.elements.new()
chest.co = (0.6, 0, 0.1)
chest.radius = 0.9

# Head
head = mb.elements.new()
head.co = (1.3, 0, 0.4)
head.radius = 0.5

# Snout
snout = mb.elements.new()
snout.co = (1.7, 0, 0.3)
snout.radius = 0.3

# Hindquarters
hind = mb.elements.new()
hind.co = (-0.6, 0, -0.1)
hind.radius = 0.7

# Convert to mesh
bpy.ops.object.convert(target='MESH')

# Add legs
for i, pos in enumerate([(0.5, 0.3, -0.7), (0.5, -0.3, -0.7), (-0.4, 0.3, -0.7), (-0.4, -0.3, -0.7)]):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=0.8, location=pos)
    leg = bpy.context.object
    leg.name = f"Leg_{i+1}"
    # Smooth
    modifier = leg.modifiers.new(name='Subsurf', type='SUBSURF')
    modifier.levels = 2
    # Join
    leg.select_set(True)
    dog.select_set(True)
    bpy.context.view_layer.objects.active = dog
    bpy.ops.object.join()

# Add ears
for side in [0.25, -0.25]:
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(1.2, side, 0.7))
    ear = bpy.context.object
    ear.scale = (0.8, 0.3, 1.2)
    ear.rotation_euler = (0.3, 0, -0.2 * (1 if side > 0 else -1))
    modifier = ear.modifiers.new(name='Subsurf', type='SUBSURF')
    modifier.levels = 2
    ear.select_set(True)
    dog.select_set(True)
    bpy.context.view_layer.objects.active = dog
    bpy.ops.object.join()

# Add tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(-1.0, 0, 0.2))
tail = bpy.context.object
tail.rotation_euler = (0, 0.4, 0)
modifier = tail.modifiers.new(name='Subsurf', type='SUBSURF')
modifier.levels = 2
tail.select_set(True)
dog.select_set(True)
bpy.context.view_layer.objects.active = dog
bpy.ops.object.join()

# Apply realistic material
mat = bpy.data.materials.new(name="Dog_Fur_Realistic")
mat.use_nodes = True

nodes = mat.node_tree.nodes
links = mat.node_tree.links

# Clear defaults
for node in nodes:
    nodes.remove(node)

# Principled BSDF
bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
bsdf.location = (0, 0)
bsdf.inputs['Base Color'].default_value = (0.85, 0.65, 0.35, 1.0)  # Golden
bsdf.inputs['Roughness'].default_value = 0.85
bsdf.inputs['Sheen Weight'].default_value = 0.5  # Fur sheen
bsdf.inputs['Sheen Tint'].default_value = (0.9, 0.7, 0.4, 1.0)

# Add noise for fur variation
noise = nodes.new(type='ShaderNodeTexNoise')
noise.location = (-400, 0)
noise.inputs['Scale'].default_value = 50
noise.inputs['Detail'].default_value = 10
noise.inputs['Roughness'].default_value = 0.7

# Color variation
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.location = (-200, 0)
color_ramp.color_ramp.elements[0].color = (0.7, 0.5, 0.3, 1.0)
color_ramp.color_ramp.elements[1].color = (0.9, 0.7, 0.4, 1.0)

# Output
output = nodes.new(type='ShaderNodeOutputMaterial')
output.location = (300, 0)

# Connect nodes
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], bsdf.inputs['Base Color'])
links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])

# Apply material
dog.data.materials.append(mat)

# Add smooth shading
bpy.ops.object.shade_smooth()

# Add professional lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.object
sun.data.energy = 2
sun.data.color = (1.0, 0.98, 0.95)

bpy.ops.object.light_add(type='AREA', location=(-3, -3, 5))
fill = bpy.context.object
fill.data.energy = 30
fill.data.size = 5

# Position camera
bpy.ops.object.camera_add(location=(4, -4, 2))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0.785)

# Set viewport shading
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.type = 'MATERIAL'
                space.shading.use_scene_lights = True
                space.shading.use_scene_world = False

# Export path
export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/generated/realistic_dog_test.glb"

# Select dog for export
bpy.ops.object.select_all(action='DESELECT')
dog.select_set(True)

# Export as GLB
bpy.ops.export_scene.gltf(
    filepath=export_path,
    export_format='GLB',
    use_selection=True,
    export_apply_modifiers=True,
    export_animations=False
)

# Get stats
vertices = len(dog.data.vertices)
faces = len(dog.data.polygons)

print(f"✅ Dog created successfully!")
print(f"   Vertices: {vertices}")
print(f"   Faces: {faces}")
print(f"   Exported to: {export_path}")

result = {
    "success": True,
    "vertices": vertices,
    "faces": faces,
    "export_path": export_path
}

import json
print("RESULT:" + json.dumps(result))
"""
    
    try:
        # Send to Blender MCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('localhost', 9876))
        
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        print("📤 Sending generation command...")
        sock.send(json.dumps(command).encode('utf-8'))
        
        # Wait for response
        response = sock.recv(16384).decode('utf-8')
        sock.close()
        
        result = json.loads(response)
        
        if "error" in result:
            print(f"❌ Error: {result['error']}")
        else:
            print("✅ Generation successful!")
            
            # Parse output if available
            if "result" in result and "RESULT:" in result["result"]:
                result_json = result["result"].split("RESULT:")[1].strip()
                try:
                    parsed = json.loads(result_json)
                    print(f"\n📊 Model Statistics:")
                    print(f"   Vertices: {parsed.get('vertices', 'N/A')}")
                    print(f"   Faces: {parsed.get('faces', 'N/A')}")
                    print(f"   Export: {parsed.get('export_path', 'N/A')}")
                except:
                    pass
                    
    except Exception as e:
        print(f"❌ Failed: {e}")
        
    print("\n" + "="*50)
    print("Test complete!")

if __name__ == "__main__":
    generate_test_dog()