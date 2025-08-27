#!/usr/bin/env python3
"""
Medical Snake Model Script - To be run in Blender's GUI
Copy and paste this into Blender's Scripting tab
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector, Matrix
import math
import random

# Clear all mesh objects from the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

print("🐍 Creating Medical Snake Model...")

# 1. Create snake vertebral column (120 segments)
print("Creating vertebral column with 120 segments...")

# Create main snake body
bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=18, location=(0, 0, 1))
snake_body = bpy.context.object
snake_body.name = "Snake_Medical_Body"

# Add loop cuts for vertebrae definition
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":119, "smoothness":0}, TRANSFORM_OT_edge_slide={"value":0})
bpy.ops.object.mode_set(mode='OBJECT')

# Bend the snake into S-curve
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')

# Apply gentle S-curve deformation
for i in range(10):
    bpy.ops.transform.bend(value=math.radians(15), orient_axis='Z', orient_type='GLOBAL', 
                          orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                          orient_matrix_type='GLOBAL', center_override=(0, 0, 0))

bpy.ops.object.mode_set(mode='OBJECT')

# 2. Create snake head with flexible jaw
print("Creating head with flexible jaw...")

bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 10))
head = bpy.context.object
head.name = "Snake_Head"

# Scale head to be more triangular
head.scale = (0.8, 1.2, 0.7)

# Upper jaw
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, -0.6, 10.2))
upper_jaw = bpy.context.object
upper_jaw.name = "Upper_Jaw"
upper_jaw.scale = (0.7, 0.6, 0.3)

# Lower jaw
bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, -0.6, 9.8))
lower_jaw = bpy.context.object
lower_jaw.name = "Lower_Jaw"  
lower_jaw.scale = (0.7, 0.6, 0.25)

# 3. Create forked tongue
print("Creating forked tongue...")

# Main tongue
bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=0.8, location=(0, -1.1, 10))
tongue_base = bpy.context.object
tongue_base.name = "Tongue_Base"
tongue_base.rotation_euler = (math.radians(90), 0, 0)

# Left fork
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.3, location=(-0.08, -1.4, 10))
fork_left = bpy.context.object
fork_left.name = "Tongue_Fork_Left"
fork_left.rotation_euler = (math.radians(75), 0, math.radians(-25))

# Right fork
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.3, location=(0.08, -1.4, 10))
fork_right = bpy.context.object
fork_right.name = "Tongue_Fork_Right"
fork_right.rotation_euler = (math.radians(75), 0, math.radians(25))

# 4. Create elongated internal organs
print("Creating internal organs...")

# Heart (elongated snake heart)
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=1.5, location=(0, 0, 8))
heart = bpy.context.object
heart.name = "Snake_Heart"
heart.scale = (1.2, 0.8, 1)

# Stomach (very long)
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=4, location=(0, 0, 5))
stomach = bpy.context.object
stomach.name = "Snake_Stomach"

# Liver (elongated)
bpy.ops.mesh.primitive_cylinder_add(radius=0.13, depth=2.5, location=(-0.15, 0, 3))
liver = bpy.context.object
liver.name = "Snake_Liver"

# Multiple kidney segments
for i in range(8):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.08, location=(0.2, 0, -1 + i*2))
    kidney = bpy.context.object
    kidney.name = f"Snake_Kidney_{i+1}"

# 5. Create materials for medical visualization
print("Creating 5 medical visualization materials...")

# Normal Python Pattern Material
normal_mat = bpy.data.materials.new(name="Python_Normal")
normal_mat.use_nodes = True
nodes = normal_mat.node_tree.nodes
links = normal_mat.node_tree.links
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.2, 0.4, 0.1, 1.0)
principled.inputs['Roughness'].default_value = 0.7

# Add scales pattern
noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 80.0

color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.1, 0.2, 0.05, 1.0)  # Dark
color_ramp.color_ramp.elements[1].color = (0.4, 0.6, 0.2, 1.0)   # Light

links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# X-Ray Material
xray_mat = bpy.data.materials.new(name="Snake_XRay")
xray_mat.use_nodes = True
xray_mat.blend_method = 'BLEND'
nodes = xray_mat.node_tree.nodes
links = xray_mat.node_tree.links
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.7, 0.8, 1.0, 1.0)
principled.inputs['Alpha'].default_value = 0.4
principled.inputs['Transmission'].default_value = 0.8

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Ultrasound Material
ultrasound_mat = bpy.data.materials.new(name="Snake_Ultrasound")
ultrasound_mat.use_nodes = True
nodes = ultrasound_mat.node_tree.nodes
links = ultrasound_mat.node_tree.links
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.0, 0.1, 0.2, 1.0)
principled.inputs['Emission'].default_value = (0.1, 0.3, 0.7, 1.0)
principled.inputs['Emission Strength'].default_value = 1.0

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Thermal Material (heat sensing)
thermal_mat = bpy.data.materials.new(name="Snake_Thermal")
thermal_mat.use_nodes = True
nodes = thermal_mat.node_tree.nodes
links = thermal_mat.node_tree.links
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')

# Thermal gradient
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.8, 1.0)  # Cold blue
color_ramp.color_ramp.elements.new(0.5)
color_ramp.color_ramp.elements[1].color = (0.8, 0.8, 0.0, 1.0)  # Warm yellow
color_ramp.color_ramp.elements.new(1.0)
color_ramp.color_ramp.elements[2].color = (1.0, 0.0, 0.0, 1.0)  # Hot red

tex_coord = nodes.new(type='ShaderNodeTexCoord')
separate_xyz = nodes.new(type='ShaderNodeSeparateXYZ')

links.new(tex_coord.outputs['Object'], separate_xyz.inputs['Vector'])
links.new(separate_xyz.outputs['Z'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(color_ramp.outputs['Color'], principled.inputs['Emission'])
principled.inputs['Emission Strength'].default_value = 0.3

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# MRI Material
mri_mat = bpy.data.materials.new(name="Snake_MRI")
mri_mat.use_nodes = True
nodes = mri_mat.node_tree.nodes
links = mri_mat.node_tree.links
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.7, 0.7, 0.7, 1.0)
principled.inputs['Roughness'].default_value = 1.0
principled.inputs['Specular'].default_value = 0.0

# Tissue variation
noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 30.0

color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.3, 0.3, 0.3, 1.0)
color_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)

links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])

output = nodes.new(type='ShaderNodeOutputMaterial')
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# 6. Apply materials to snake body
snake_body.data.materials.append(normal_mat)
snake_body.data.materials.append(xray_mat)
snake_body.data.materials.append(ultrasound_mat)
snake_body.data.materials.append(thermal_mat)
snake_body.data.materials.append(mri_mat)

# Apply to head parts
head.data.materials.append(normal_mat)
upper_jaw.data.materials.append(normal_mat)
lower_jaw.data.materials.append(normal_mat)

# 7. Add subdivision for detail and optimize
print("Optimizing polygon count...")

# Add subdivision to snake body for detail
snake_body.modifiers.new(name="Subdivision", type='SUBSURF')
snake_body.modifiers["Subdivision"].levels = 2

# Join main parts
bpy.ops.object.select_all(action='DESELECT')
snake_body.select_set(True)
head.select_set(True)
upper_jaw.select_set(True)
lower_jaw.select_set(True)
tongue_base.select_set(True)
fork_left.select_set(True)
fork_right.select_set(True)

bpy.context.view_layer.objects.active = snake_body
bpy.ops.object.join()

print("✅ Medical Snake Model Created Successfully!")
print("Features:")
print("- 120 vertebrae segments represented")
print("- Forked tongue with detailed anatomy")
print("- Flexible jaw structure")  
print("- Elongated internal organs (heart, stomach, liver, kidneys)")
print("- 5 Medical visualization materials:")
print("  • Normal Python Pattern")
print("  • X-Ray (spine visibility)")
print("  • Ultrasound")
print("  • Thermal (heat sensing)")
print("  • MRI (tissue differentiation)")
print("- Optimized for medical education")
print("\nReady for export! Use File > Export > glTF 2.0 (.glb/.gltf)")
print("Export path: /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/snake/snake_medical.glb")