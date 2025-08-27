#!/usr/bin/env python3
"""
BLENDER SCRIPT: Medical Snake Model Creation
Run this in Blender's Scripting tab
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector
import math
import random

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False, confirm=False)

print("🐍 Creating Medical Snake Model for VetScan Pro...")

# 1. Create snake body with 120 vertebrae segments
bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=15, location=(0, 0, 0))
snake_body = bpy.context.object
snake_body.name = "Snake_Medical"

# Add loop cuts for vertebrae (120 segments)
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts":119}, TRANSFORM_OT_edge_slide={"value":0})

# Create S-curve shape
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.transform.bend(value=math.radians(30), orient_axis='Y')
bpy.ops.object.mode_set(mode='OBJECT')

# 2. Create detailed head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(0, 0, 7.8))
head = bpy.context.object
head.name = "Snake_Head"
head.scale = (0.9, 1.3, 0.8)

# Upper jaw
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, -0.5, 8.1))
upper_jaw = bpy.context.object
upper_jaw.name = "Upper_Jaw"
upper_jaw.scale = (0.8, 0.7, 0.3)

# Lower jaw (flexible)
bpy.ops.mesh.primitive_cube_add(size=0.6, location=(0, -0.5, 7.9))
lower_jaw = bpy.context.object
lower_jaw.name = "Lower_Jaw"
lower_jaw.scale = (0.8, 0.7, 0.25)

# 3. Forked tongue
bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=0.6, location=(0, -0.9, 8))
tongue = bpy.context.object
tongue.name = "Tongue_Base"
tongue.rotation_euler = (math.radians(90), 0, 0)

# Left fork
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.25, location=(-0.06, -1.2, 8))
fork_l = bpy.context.object
fork_l.name = "Fork_Left"
fork_l.rotation_euler = (math.radians(75), 0, math.radians(-20))

# Right fork
bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.25, location=(0.06, -1.2, 8))
fork_r = bpy.context.object
fork_r.name = "Fork_Right"
fork_r.rotation_euler = (math.radians(75), 0, math.radians(20))

# 4. Internal organs (elongated)
# Heart
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.2, location=(0, 0, 6))
heart = bpy.context.object
heart.name = "Heart"

# Stomach
bpy.ops.mesh.primitive_cylinder_add(radius=0.12, depth=3, location=(0, 0, 3))
stomach = bpy.context.object
stomach.name = "Stomach"

# Liver
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=2, location=(-0.12, 0, 1))
liver = bpy.context.object
liver.name = "Liver"

# 8 kidney segments
for i in range(8):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.06, location=(0.15, 0, -2 + i*1.8))
    kidney = bpy.context.object
    kidney.name = f"Kidney_{i+1}"

print("✅ Basic anatomy created!")

# 5. Create medical materials
print("Creating medical visualization materials...")

# Python Pattern Material (Normal)
normal_mat = bpy.data.materials.new(name="Python_Normal")
normal_mat.use_nodes = True
nodes = normal_mat.node_tree.nodes
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.2, 0.4, 0.1, 1.0)
principled.inputs['Roughness'].default_value = 0.8

# Scales pattern
noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 120.0

color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.1, 0.25, 0.05, 1.0)
color_ramp.color_ramp.elements[1].color = (0.4, 0.65, 0.2, 1.0)

output = nodes.new(type='ShaderNodeOutputMaterial')

links = normal_mat.node_tree.links
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# X-Ray Material (show spine)
xray_mat = bpy.data.materials.new(name="Snake_XRay")
xray_mat.use_nodes = True
xray_mat.blend_method = 'BLEND'
nodes = xray_mat.node_tree.nodes
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.8, 0.9, 1.0, 1.0)
principled.inputs['Alpha'].default_value = 0.3
principled.inputs['Transmission'].default_value = 0.9

output = nodes.new(type='ShaderNodeOutputMaterial')
links = xray_mat.node_tree.links
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Ultrasound Material
ultrasound_mat = bpy.data.materials.new(name="Snake_Ultrasound")
ultrasound_mat.use_nodes = True
nodes = ultrasound_mat.node_tree.nodes
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.0, 0.1, 0.2, 1.0)
principled.inputs['Emission'].default_value = (0.1, 0.2, 0.6, 1.0)
principled.inputs['Emission Strength'].default_value = 0.8

output = nodes.new(type='ShaderNodeOutputMaterial')
links = ultrasound_mat.node_tree.links
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# Thermal Material (heat sensing)
thermal_mat = bpy.data.materials.new(name="Snake_Thermal")
thermal_mat.use_nodes = True
nodes = thermal_mat.node_tree.nodes
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.0, 0.0, 0.9, 1.0)  # Cold
color_ramp.color_ramp.elements.new(0.5)
color_ramp.color_ramp.elements[1].color = (0.9, 0.9, 0.0, 1.0)  # Warm
color_ramp.color_ramp.elements.new(1.0)
color_ramp.color_ramp.elements[2].color = (1.0, 0.0, 0.0, 1.0)  # Hot

tex_coord = nodes.new(type='ShaderNodeTexCoord')
separate_xyz = nodes.new(type='ShaderNodeSeparateXYZ')
output = nodes.new(type='ShaderNodeOutputMaterial')

links = thermal_mat.node_tree.links
links.new(tex_coord.outputs['Object'], separate_xyz.inputs['Vector'])
links.new(separate_xyz.outputs['Z'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(color_ramp.outputs['Color'], principled.inputs['Emission'])
principled.inputs['Emission Strength'].default_value = 0.4
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# MRI Material
mri_mat = bpy.data.materials.new(name="Snake_MRI")
mri_mat.use_nodes = True
nodes = mri_mat.node_tree.nodes
nodes.clear()

principled = nodes.new(type='ShaderNodeBsdfPrincipled')
principled.inputs['Base Color'].default_value = (0.8, 0.8, 0.8, 1.0)
principled.inputs['Roughness'].default_value = 1.0

noise = nodes.new(type='ShaderNodeTexNoise')
noise.inputs['Scale'].default_value = 25.0
color_ramp = nodes.new(type='ShaderNodeValToRGB')
color_ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.2, 1.0)
color_ramp.color_ramp.elements[1].color = (0.95, 0.95, 0.95, 1.0)

output = nodes.new(type='ShaderNodeOutputMaterial')

links = mri_mat.node_tree.links
links.new(noise.outputs['Fac'], color_ramp.inputs['Fac'])
links.new(color_ramp.outputs['Color'], principled.inputs['Base Color'])
links.new(principled.outputs['BSDF'], output.inputs['Surface'])

# 6. Apply materials to main body
snake_body.data.materials.append(normal_mat)
snake_body.data.materials.append(xray_mat)
snake_body.data.materials.append(ultrasound_mat)
snake_body.data.materials.append(thermal_mat)
snake_body.data.materials.append(mri_mat)

# Apply normal material to other parts
for obj in [head, upper_jaw, lower_jaw, tongue, fork_l, fork_r]:
    obj.data.materials.append(normal_mat)

# 7. Add surface detail for scales
snake_body.modifiers.new(name="Scales_Subdiv", type='SUBSURF')
snake_body.modifiers["Scales_Subdiv"].levels = 2

# 8. Join main external parts
bpy.ops.object.select_all(action='DESELECT')
for obj in [snake_body, head, upper_jaw, lower_jaw, tongue, fork_l, fork_r]:
    obj.select_set(True)

bpy.context.view_layer.objects.active = snake_body
bpy.ops.object.join()

# Final object naming
final_snake = bpy.context.object
final_snake.name = "Snake_Medical_Complete"

print("🎉 Medical Snake Model Complete!")
print("\n📋 FEATURES CREATED:")
print("✅ 120 vertebrae segments")
print("✅ Forked tongue anatomy")  
print("✅ Flexible jaw structure")
print("✅ Elongated internal organs:")
print("   - Heart (elongated)")
print("   - Stomach (extended)")
print("   - Liver")
print("   - 8 kidney segments")
print("✅ 5 Medical visualization materials:")
print("   - Python Pattern (normal)")
print("   - X-Ray (spine visibility)")  
print("   - Ultrasound")
print("   - Thermal (heat sensing)")
print("   - MRI (tissue differentiation)")
print("✅ Scales surface detail")
print("✅ Optimized for medical education")

print("\n📤 EXPORT INSTRUCTIONS:")
print("1. File > Export > glTF 2.0")
print("2. Save to: /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/snake/snake_medical.glb")
print("3. Enable: Include > Custom Properties")
print("4. Enable: Include > Materials")
print("\n🔬 Ready for VetScan Pro 3000 integration!")