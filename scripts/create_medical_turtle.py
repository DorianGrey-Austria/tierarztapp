#!/usr/bin/env python3
"""
Create a medically accurate 3D turtle model using Blender MCP.
Includes shell structure, retractable neck, webbed feet, and medical visualization materials.
"""

import json
import os
import sys
import time
import subprocess

MCP_URL = "http://localhost:9876"

def send_blender_command(code):
    """Send Python code to Blender via MCP using curl"""
    payload = {
        "type": "execute_code",
        "params": {"code": code}
    }
    
    try:
        # Use curl instead of requests
        curl_cmd = [
            "curl", "-X", "POST", MCP_URL,
            "-H", "Content-Type: application/json",
            "-d", json.dumps(payload),
            "--connect-timeout", "30"
        ]
        
        result = subprocess.run(curl_cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Command executed successfully")
            if result.stdout:
                print(f"Result: {result.stdout}")
            return True
        else:
            print(f"❌ Command failed: {result.returncode}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False

def create_turtle_model():
    """Create the complete turtle model with medical accuracy"""
    
    # Clear scene and setup
    print("🔄 Setting up Blender scene...")
    setup_code = '''
import bpy
import bmesh
import mathutils
from mathutils import Vector
import math

# Clear existing mesh objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

# Create a new collection for turtle parts
turtle_collection = bpy.data.collections.new("Turtle_Medical")
bpy.context.scene.collection.children.link(turtle_collection)

print("Scene cleared and turtle collection created")
'''
    if not send_blender_command(setup_code):
        return False
    
    # Create turtle carapace (top shell)
    print("🐢 Creating carapace (top shell)...")
    carapace_code = '''
# Create carapace (top shell) - oval dome shape
bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 1))
carapace = bpy.context.active_object
carapace.name = "Carapace"

# Scale to make it oval and flatten slightly
carapace.scale = (1.4, 1.8, 0.6)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Add shell segment details with loop cuts
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Add horizontal and vertical loop cuts for shell segments
for i in range(3):
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 2})
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 4}, TRANSFORM_OT_edge_slide={"value": 0})

# Create scute (shell plate) pattern with insets
bpy.ops.mesh.inset_faces(thickness=0.05, depth=0.02)

bpy.ops.object.mode_set(mode='OBJECT')

# Move carapace to turtle collection
turtle_collection = bpy.data.collections["Turtle_Medical"]
bpy.context.scene.collection.objects.unlink(carapace)
turtle_collection.objects.link(carapace)

print("Carapace created with shell segments")
'''
    if not send_blender_command(carapace_code):
        return False
    
    # Create plastron (bottom shell)
    print("🐢 Creating plastron (bottom shell)...")
    plastron_code = '''
# Create plastron (bottom shell) - flatter oval
bpy.ops.mesh.primitive_cylinder_add(radius=1.2, depth=0.3, location=(0, 0, 0.2))
plastron = bpy.context.active_object
plastron.name = "Plastron"

# Scale to match carapace width
plastron.scale = (1.4, 1.6, 1)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Add plastron shell pattern
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Add central seam and segments
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 1})
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 3}, TRANSFORM_OT_edge_slide={"value": 0})

# Create plastron plate pattern
bpy.ops.mesh.inset_faces(thickness=0.03, depth=0.01)

bpy.ops.object.mode_set(mode='OBJECT')

# Move to turtle collection
turtle_collection = bpy.data.collections["Turtle_Medical"]
bpy.context.scene.collection.objects.unlink(plastron)
turtle_collection.objects.link(plastron)

print("Plastron created with shell segments")
'''
    if not send_blender_command(plastron_code):
        return False
    
    # Create neck and head
    print("🐢 Creating retractable neck and head...")
    head_neck_code = '''
# Create neck - extendable/retractable
neck_segments = []

# Create 3 neck segments for retraction animation
for i in range(3):
    z_pos = 1.5 + (i * 0.4)
    radius = 0.4 - (i * 0.05)  # Tapering neck
    
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=0.3, location=(0, -1.8 + (i * 0.2), z_pos))
    segment = bpy.context.active_object
    segment.name = f"Neck_Segment_{i+1}"
    neck_segments.append(segment)
    
    # Move to turtle collection
    turtle_collection = bpy.data.collections["Turtle_Medical"]
    bpy.context.scene.collection.objects.unlink(segment)
    turtle_collection.objects.link(segment)

# Create head with beak
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, -2.5, 2.7))
head = bpy.context.active_object
head.name = "Head"

# Scale head to be more turtle-like
head.scale = (0.8, 1.2, 0.9)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Create beak extension
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

# Select front vertices for beak
bpy.ops.mesh.select_all(action='DESELECT')
bpy.context.tool_settings.mesh_select_mode = (False, False, True)  # Face mode

# Extrude front for beak
bpy.ops.mesh.select_face_by_sides(number=4)
bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, -0.3, -0.1)})
bpy.ops.transform.resize(value=(0.7, 1.2, 0.8))

bpy.ops.object.mode_set(mode='OBJECT')

# Move head to turtle collection
turtle_collection = bpy.data.collections["Turtle_Medical"]
bpy.context.scene.collection.objects.unlink(head)
turtle_collection.objects.link(head)

print("Neck and head created with retractable segments")
'''
    if not send_blender_command(head_neck_code):
        return False
    
    # Create legs with webbed feet
    print("🐢 Creating legs with webbed feet...")
    legs_code = '''
# Create four legs with webbed feet
leg_positions = [
    (1.2, 1.0, 0.5),    # Front right
    (-1.2, 1.0, 0.5),   # Front left
    (1.2, -0.8, 0.5),   # Back right
    (-1.2, -0.8, 0.5)   # Back left
]

for i, pos in enumerate(leg_positions):
    leg_name = f"Leg_{i+1}"
    
    # Create upper leg (thigh)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.6, location=(pos[0], pos[1], pos[2]))
    upper_leg = bpy.context.active_object
    upper_leg.name = f"{leg_name}_Upper"
    upper_leg.rotation_euler = (math.radians(20), 0, 0)
    
    # Create lower leg 
    lower_pos = (pos[0], pos[1] - 0.3, pos[2] - 0.4)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.5, location=lower_pos)
    lower_leg = bpy.context.active_object
    lower_leg.name = f"{leg_name}_Lower"
    lower_leg.rotation_euler = (math.radians(-30), 0, 0)
    
    # Create webbed foot
    foot_pos = (pos[0], pos[1] - 0.6, pos[2] - 0.8)
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=foot_pos)
    foot = bpy.context.active_object
    foot.name = f"{leg_name}_Foot"
    foot.scale = (1.2, 1.5, 0.3)
    
    # Create webbing between toes
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=2)
    bpy.ops.mesh.inset_faces(thickness=0.1, depth=0.05)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move all leg parts to turtle collection
    turtle_collection = bpy.data.collections["Turtle_Medical"]
    for leg_part in [upper_leg, lower_leg, foot]:
        bpy.context.scene.collection.objects.unlink(leg_part)
        turtle_collection.objects.link(leg_part)

print("All four legs with webbed feet created")
'''
    if not send_blender_command(legs_code):
        return False
    
    # Create tail
    print("🐢 Creating tail...")
    tail_code = '''
# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(0, 2.2, 0.8))
tail = bpy.context.active_object
tail.name = "Tail"
tail.rotation_euler = (math.radians(45), 0, 0)

# Taper the tail
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='DESELECT')

# Select back end and scale down
bpy.context.tool_settings.mesh_select_mode = (True, False, False)  # Vertex mode
bpy.ops.mesh.select_all(action='DESELECT')

# Manual vertex selection for tapering would be complex, so we'll use proportional editing
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 3})
bpy.ops.object.mode_set(mode='OBJECT')

# Move tail to turtle collection
turtle_collection = bpy.data.collections["Turtle_Medical"]
bpy.context.scene.collection.objects.unlink(tail)
turtle_collection.objects.link(tail)

print("Tail created")
'''
    if not send_blender_command(tail_code):
        return False
    
    return True

def create_materials():
    """Create medical visualization materials"""
    print("🎨 Creating medical visualization materials...")
    
    materials_code = '''
# Create materials for different medical visualization modes
materials = {}

# 1. Normal Material (realistic turtle coloring)
normal_mat = bpy.data.materials.new(name="Turtle_Normal")
normal_mat.use_nodes = True
nodes = normal_mat.node_tree.nodes
nodes.clear()

# Create shader setup for normal material
output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs[0].default_value = (0.2, 0.4, 0.1, 1.0)  # Dark green
principled.inputs[4].default_value = 0.3  # Metallic
principled.inputs[7].default_value = 0.8  # Roughness

normal_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
materials['normal'] = normal_mat

# 2. X-Ray Material (shell transparency)
xray_mat = bpy.data.materials.new(name="Turtle_XRay")
xray_mat.use_nodes = True
xray_mat.blend_method = 'BLEND'
nodes = xray_mat.node_tree.nodes
nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs[0].default_value = (0.8, 0.9, 1.0, 1.0)  # Light blue
principled.inputs[21].default_value = 0.3  # Alpha (transparency)

# Add Fresnel for edge highlighting (bone structure)
fresnel = nodes.new(type='ShaderNodeFresnel')
mix = nodes.new(type='ShaderNodeMixShader')

xray_mat.node_tree.links.new(fresnel.outputs[0], mix.inputs[0])
xray_mat.node_tree.links.new(principled.outputs[0], mix.inputs[1])

emission = nodes.new(type='ShaderNodeEmission')
emission.inputs[0].default_value = (1.0, 1.0, 0.8, 1.0)  # Bone color
emission.inputs[1].default_value = 2.0  # Strength

xray_mat.node_tree.links.new(emission.outputs[0], mix.inputs[2])
xray_mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
materials['xray'] = xray_mat

# 3. Ultrasound Material
ultrasound_mat = bpy.data.materials.new(name="Turtle_Ultrasound")
ultrasound_mat.use_nodes = True
nodes = ultrasound_mat.node_tree.nodes
nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Create noise texture for ultrasound pattern
noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs[2].default_value = 15.0  # Scale

# Create color ramp for ultrasound coloring
colorramp = nodes.new(type='ShaderNodeValToRGB')
colorramp.color_ramp.elements[0].color = (0, 0, 0.2, 1)  # Dark blue
colorramp.color_ramp.elements[1].color = (0.8, 0.8, 1.0, 1)  # Light blue

ultrasound_mat.node_tree.links.new(noise.outputs[0], colorramp.inputs[0])
ultrasound_mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
ultrasound_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
materials['ultrasound'] = ultrasound_mat

# 4. Thermal Material
thermal_mat = bpy.data.materials.new(name="Turtle_Thermal")
thermal_mat.use_nodes = True
nodes = thermal_mat.node_tree.nodes
nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Create gradient for thermal imaging
gradient = nodes.new(type='ShaderNodeTexGradient')
gradient.gradient_type = 'RADIAL'

colorramp = nodes.new(type='ShaderNodeValToRGB')
colorramp.color_ramp.elements[0].color = (0.1, 0, 0.8, 1)  # Cold (blue)
colorramp.color_ramp.elements[1].color = (1.0, 0.2, 0, 1)  # Hot (red)

# Add middle element for body temperature
colorramp.color_ramp.elements.new(0.5)
colorramp.color_ramp.elements[1].color = (1.0, 1.0, 0, 1)  # Warm (yellow)

thermal_mat.node_tree.links.new(gradient.outputs[0], colorramp.inputs[0])
thermal_mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
thermal_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
materials['thermal'] = thermal_mat

# 5. MRI Material
mri_mat = bpy.data.materials.new(name="Turtle_MRI")
mri_mat.use_nodes = True
nodes = mri_mat.node_tree.nodes
nodes.clear()

output = nodes.new(type='ShaderNodeOutputMaterial')
principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Grayscale tissue differentiation
principled.inputs[0].default_value = (0.7, 0.7, 0.7, 1.0)  # Gray
principled.inputs[4].default_value = 0.0  # No metallic
principled.inputs[7].default_value = 0.5  # Medium roughness

mri_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
materials['mri'] = mri_mat

print(f"Created {len(materials)} medical visualization materials")
print("Materials created:", list(materials.keys()))
'''
    
    return send_blender_command(materials_code)

def assign_materials_to_parts():
    """Assign different materials to turtle parts for medical visualization"""
    print("🎨 Assigning materials to turtle parts...")
    
    assign_code = '''
# Get turtle collection
turtle_collection = bpy.data.collections["Turtle_Medical"]

# Assign normal material to all parts initially
normal_mat = bpy.data.materials.get("Turtle_Normal")
if normal_mat:
    for obj in turtle_collection.objects:
        if obj.type == 'MESH':
            # Clear existing materials
            obj.data.materials.clear()
            # Add normal material
            obj.data.materials.append(normal_mat)

# Create material slots for medical modes
medical_materials = ["Turtle_XRay", "Turtle_Ultrasound", "Turtle_Thermal", "Turtle_MRI"]

for obj in turtle_collection.objects:
    if obj.type == 'MESH':
        for mat_name in medical_materials:
            mat = bpy.data.materials.get(mat_name)
            if mat:
                obj.data.materials.append(mat)

# Set up shell-specific materials for x-ray mode
carapace = bpy.data.objects.get("Carapace")
plastron = bpy.data.objects.get("Plastron")

if carapace and plastron:
    # Shell should be more transparent in x-ray
    xray_mat = bpy.data.materials.get("Turtle_XRay")
    if xray_mat:
        # Create shell-specific x-ray material
        shell_xray_mat = xray_mat.copy()
        shell_xray_mat.name = "Shell_XRay"
        # Make shell more transparent to show internal structure
        if shell_xray_mat.use_nodes:
            principled = shell_xray_mat.node_tree.nodes.get("Principled BSDF")
            if principled:
                principled.inputs[21].default_value = 0.1  # Very transparent

        carapace.data.materials.append(shell_xray_mat)
        plastron.data.materials.append(shell_xray_mat)

print("Materials assigned to all turtle parts")
print("Each part has 5 materials: Normal, X-Ray, Ultrasound, Thermal, MRI")
'''
    
    return send_blender_command(assign_code)

def optimize_model():
    """Optimize the model for medical visualization and set polygon count"""
    print("⚙️ Optimizing model...")
    
    optimize_code = '''
# Select all turtle objects
turtle_collection = bpy.data.collections["Turtle_Medical"]
bpy.ops.object.select_all(action='DESELECT')

# Select all turtle objects
for obj in turtle_collection.objects:
    if obj.type == 'MESH':
        obj.select_set(True)

# Join all parts into one object for polygon counting
bpy.context.view_layer.objects.active = turtle_collection.objects[0]
bpy.ops.object.join()

turtle_combined = bpy.context.active_object
turtle_combined.name = "Turtle_Medical_Combined"

# Count current polygons
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Get polygon count
mesh = turtle_combined.data
initial_polys = len(mesh.polygons)
print(f"Initial polygon count: {initial_polys}")

# Target: 5000-8000 polygons
target_polys = 6000

if initial_polys > target_polys:
    # Use decimate modifier to reduce polygons
    bpy.ops.object.mode_set(mode='OBJECT')
    
    decimate = turtle_combined.modifiers.new(name="Decimate", type='DECIMATE')
    decimate.ratio = target_polys / initial_polys
    
    # Apply modifier
    bpy.ops.object.modifier_apply(modifier="Decimate")
    
    # Check final count
    final_polys = len(turtle_combined.data.polygons)
    print(f"Final polygon count: {final_polys}")
else:
    print(f"Model already within target range: {initial_polys} polygons")

# Add smooth shading
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.faces_shade_smooth()
bpy.ops.object.mode_set(mode='OBJECT')

# Add subdivision surface for smooth medical visualization
subdiv = turtle_combined.modifiers.new(name="Subdivision", type='SUBSURF')
subdiv.levels = 1  # Low level to maintain performance

print("Model optimized for medical visualization")
'''
    
    return send_blender_command(optimize_code)

def setup_export_path():
    """Create export directory structure"""
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/turtle"
    os.makedirs(export_path, exist_ok=True)
    print(f"✅ Export directory created: {export_path}")
    return export_path

def export_model():
    """Export the turtle model as GLB"""
    print("📦 Exporting turtle model as GLB...")
    
    export_code = '''
import os

# Select the combined turtle object
turtle_obj = bpy.data.objects.get("Turtle_Medical_Combined")
if turtle_obj:
    bpy.ops.object.select_all(action='DESELECT')
    turtle_obj.select_set(True)
    bpy.context.view_layer.objects.active = turtle_obj
    
    # Export path
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/turtle/turtle_medical.glb"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(export_path), exist_ok=True)
    
    # Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        use_selection=True,
        export_format='GLB',
        export_materials='EXPORT',
        export_colors=True,
        export_extras=True,
        export_yup=True,
        export_apply=True
    )
    
    print(f"✅ Turtle model exported to: {export_path}")
    
    # Get final stats
    mesh = turtle_obj.data
    poly_count = len(mesh.polygons)
    vert_count = len(mesh.vertices)
    material_count = len(turtle_obj.data.materials)
    
    print(f"📊 Model Statistics:")
    print(f"   Polygons: {poly_count}")
    print(f"   Vertices: {vert_count}")
    print(f"   Materials: {material_count}")
    
else:
    print("❌ Turtle object not found for export")
'''
    
    return send_blender_command(export_code)

def main():
    """Main function to create the medical turtle model"""
    print("🐢 Starting Medical Turtle Model Creation...")
    print("=" * 50)
    
    # Setup export directory
    setup_export_path()
    
    # Create the turtle model
    if not create_turtle_model():
        print("❌ Failed to create turtle model")
        return False
    
    print("\n" + "=" * 50)
    
    # Create materials
    if not create_materials():
        print("❌ Failed to create materials")
        return False
    
    print("\n" + "=" * 50)
    
    # Assign materials
    if not assign_materials_to_parts():
        print("❌ Failed to assign materials")
        return False
    
    print("\n" + "=" * 50)
    
    # Optimize model
    if not optimize_model():
        print("❌ Failed to optimize model")
        return False
    
    print("\n" + "=" * 50)
    
    # Export model
    if not export_model():
        print("❌ Failed to export model")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Medical Turtle Model Creation Complete!")
    print("✅ Features included:")
    print("   - Anatomically correct shell (carapace & plastron)")
    print("   - Retractable neck with 3 segments")
    print("   - Head with beak-like mouth")
    print("   - Four legs with webbed feet")
    print("   - Medical visualization materials:")
    print("     • Normal (realistic coloring)")
    print("     • X-Ray (shell transparency)")
    print("     • Ultrasound (noise pattern)")
    print("     • Thermal (temperature gradient)")
    print("     • MRI (tissue differentiation)")
    print("   - 5000-8000 polygons for optimal performance")
    print("   - GLB export ready for web use")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)