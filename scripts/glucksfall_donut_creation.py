
import bpy
import bmesh
import mathutils
from mathutils import Vector
import random

print("\n=== 🍩 GLÜCKSFALL DONUT CREATION 🍩 ===")
print("Reproducing the 'Glücksfall' where the dog turned into a donut...")

# Step 1: Clear the scene of mesh objects
print("\n=== Step 1: Clearing scene ===")
bpy.ops.object.select_all(action='DESELECT')
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']

print(f"Removing {len(mesh_objects)} mesh objects...")
for obj in mesh_objects:
    bpy.data.objects.remove(obj, do_unlink=True)

print("Scene cleared!")

# Step 2: Create the base donut (torus)
print("\n=== Step 2: Creating donut base ===")
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

# Step 3: Create chocolate icing material
print("\n=== Step 3: Adding chocolate icing ===")
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

# Step 4: Create colorful sprinkles
print("\n=== Step 4: Adding colorful sprinkles ===")
sprinkle_colors = [
    (1.0, 0.2, 0.2, 1.0),  # Red
    (0.2, 1.0, 0.2, 1.0),  # Green  
    (0.2, 0.2, 1.0, 1.0),  # Blue
    (1.0, 1.0, 0.2, 1.0),  # Yellow
    (1.0, 0.2, 1.0, 1.0),  # Magenta
    (0.2, 1.0, 1.0, 1.0),  # Cyan
]

sprinkles_created = 0
for i in range(100):  # 100 sprinkles for performance
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
    sprinkles_created += 1

print(f"✅ {sprinkles_created} colorful sprinkles added!")

# Step 5: Improve lighting
print("\n=== Step 5: Setting up lighting ===")
# Remove default light if it exists
if bpy.data.objects.get("Light"):
    bpy.data.objects.remove(bpy.data.objects["Light"], do_unlink=True)

# Add multiple lights for better visualization
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
sun1 = bpy.context.active_object
sun1.name = "Sun_Main"
sun1.data.energy = 5.0

bpy.ops.object.light_add(type='SUN', location=(-5, -5, 8))
sun2 = bpy.context.active_object
sun2.name = "Sun_Fill"
sun2.data.energy = 3.0

print("✅ Professional lighting setup complete!")

# Step 6: Position camera for perfect donut view
print("\n=== Step 6: Camera positioning ===")
if bpy.data.objects.get("Camera"):
    camera = bpy.data.objects["Camera"]
    camera.location = (6, -6, 4)
    camera.rotation_euler = (1.2, 0, 0.785)  # Look at donut from nice angle
    
    # Make sure it's the active camera
    bpy.context.scene.camera = camera
    print("✅ Camera positioned for perfect donut view!")

# Step 7: Final scene organization
print("\n=== Step 7: Final touches ===")

# Select the main donut for a nice final view
bpy.ops.object.select_all(action='DESELECT')
if "Glücksfall_Donut" in bpy.data.objects:
    bpy.data.objects["Glücksfall_Donut"].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects["Glücksfall_Donut"]

# Update the viewport
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        area.spaces[0].shading.type = 'MATERIAL'  # Show materials
        break

print("\n🎉 GLÜCKSFALL DONUT COMPLETE! 🎉")
print("=" * 50)
print("🐕 → 🍩 The dog has been transformed into a delicious donut!")
print(f"Created: 1 chocolate donut with {sprinkles_created} colorful sprinkles")
print("Lighting: Professional 2-point setup")
print("Camera: Positioned for perfect view")
print("Viewport: Set to Material Preview mode")
print("=" * 50)
print("\nThe 'Glücksfall' scenario has been successfully reproduced!")
