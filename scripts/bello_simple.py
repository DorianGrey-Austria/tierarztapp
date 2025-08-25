import bpy
from mathutils import Vector

print("🐕 Creating Bello - Simple Version")

# Clean up scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create main body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = 'Bello_Body'
body.scale = (2.5, 1.2, 1.0)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Add subdivision surface for organic look
modifier = body.modifiers.new(name='Subdivision', type='SUBSURF')
modifier.levels = 2

# Create head
bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3.5, 0, 1.2))
head = bpy.context.object
head.name = 'Bello_Head'
head.scale = (1.3, 0.9, 0.9)
bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

# Add subdivision to head
modifier = head.modifiers.new(name='Subdivision', type='SUBSURF')
modifier.levels = 2

# Create 4 legs
leg_positions = [(1.5, 0.8, 0.4), (1.5, -0.8, 0.4), (-1.5, 0.8, 0.4), (-1.5, -0.8, 0.4)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.2, location=pos)
    leg = bpy.context.object
    leg.name = f'Bello_Leg_{i+1}'

# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2, location=(-2.8, 0, 1.2))
tail = bpy.context.object
tail.name = 'Bello_Tail'
tail.rotation_euler = (0, 0.3, 0)

# Create ears
for i, pos in enumerate([(4.2, 0.6, 1.8), (4.2, -0.6, 1.8)]):
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=pos)
    ear = bpy.context.object
    ear.name = f'Bello_Ear_{i+1}'
    ear.scale = (0.8, 0.3, 1.2)
    ear.rotation_euler = (0.2, 0, -0.3)

# Create golden material
material = bpy.data.materials.new(name='Bello_Fur')
material.use_nodes = True
bsdf = material.node_tree.nodes['Principled BSDF']
bsdf.inputs[0].default_value = (0.8, 0.6, 0.3, 1.0)  # Golden color
bsdf.inputs[9].default_value = 0.8  # Roughness

# Apply material to all objects
for obj in bpy.data.objects:
    if obj.name.startswith('Bello_') and obj.type == 'MESH':
        obj.data.materials.append(material)

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun = bpy.context.object
sun.data.energy = 3

print("✅ Bello created successfully!")