#!/usr/bin/env python3
"""
VetScan Pro 3000 - Bello 3D Model Creator
Creates comprehensive dog model with medical visualization capabilities
"""

import bpy
import bmesh
from mathutils import Vector
import math

def clear_scene():
    """Clean up the scene completely"""
    print('🧹 Cleaning up scene...')
    
    # Select all objects and delete
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Clear materials
    for material in bpy.data.materials:
        bpy.data.materials.remove(material)
    
    print('✅ Scene cleared!')

def setup_lighting_and_camera():
    """Setup professional lighting and camera for medical visualization"""
    print('💡 Setting up lighting and camera...')
    
    # Main sun light for overall illumination
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.object
    sun.name = 'VetScan_Sun'
    sun.data.energy = 3
    sun.rotation_euler = (0.785, 0, 0.785)  # 45° angle
    
    # Secondary area light for fill lighting
    bpy.ops.object.light_add(type='AREA', location=(-3, 3, 8))
    fill_light = bpy.context.object
    fill_light.name = 'VetScan_Fill'
    fill_light.data.energy = 1.5
    fill_light.rotation_euler = (0.5, 0, -0.5)
    
    # Camera positioned for optimal medical view
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.object
    camera.name = 'VetScan_Camera'
    camera.rotation_euler = (1.1, 0, 0.785)
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    print('✅ Lighting and camera setup complete!')

def create_bello_base_geometry():
    """Create the main body structure of Bello"""
    print('🐕 Creating Bello base geometry...')
    
    # Create main collection for organization
    if 'Bello_Dog' not in bpy.data.collections:
        bello_collection = bpy.data.collections.new('Bello_Dog')
        bpy.context.scene.collection.children.link(bello_collection)
    else:
        bello_collection = bpy.data.collections['Bello_Dog']
    
    # 1. BODY (Main torso)
    print('   Creating body...')
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
    body = bpy.context.object
    body.name = 'Bello_Body'
    
    # Scale to dog proportions
    body.scale = (2.5, 1.2, 1.0)  # Longer and narrower
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add subdivision for organic shape
    modifier = body.modifiers.new(name='Subdivision', type='SUBSURF')
    modifier.levels = 2
    
    # Move to collection (safe approach)
    if body.name not in bello_collection.objects:
        bello_collection.objects.link(body)
    if body.name in bpy.context.scene.collection.objects:
        bpy.context.scene.collection.objects.unlink(body)
    
    # 2. HEAD
    print('   Creating head...')
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(3.5, 0, 1.2))
    head = bpy.context.object
    head.name = 'Bello_Head'
    
    # Dog head proportions (elongated snout)
    head.scale = (1.3, 0.9, 0.9)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Subdivision for organic head
    modifier = head.modifiers.new(name='Subdivision', type='SUBSURF')
    modifier.levels = 2
    
    # Move to collection
    bello_collection.objects.link(head)
    bpy.context.scene.collection.objects.unlink(head)
    
    # 3. LEGS (4 legs for quadruped)
    print('   Creating legs...')
    leg_positions = [
        (1.5, 0.8, 0.4),    # Front right
        (1.5, -0.8, 0.4),   # Front left
        (-1.5, 0.8, 0.4),   # Back right
        (-1.5, -0.8, 0.4)   # Back left
    ]
    
    for i, pos in enumerate(leg_positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=1.2, location=pos)
        leg = bpy.context.object
        leg.name = f'Bello_Leg_{i+1}'
        
        # Realistic leg proportions
        leg.scale = (1.0, 1.0, 1.5)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Light subdivision
        modifier = leg.modifiers.new(name='Subdivision', type='SUBSURF')
        modifier.levels = 1
        
        # Move to collection
        bello_collection.objects.link(leg)
        bpy.context.scene.collection.objects.unlink(leg)
    
    # 4. TAIL
    print('   Creating tail...')
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2, location=(-2.8, 0, 1.2))
    tail = bpy.context.object
    tail.name = 'Bello_Tail'
    
    # Friendly dog tail position (slightly up)
    tail.rotation_euler = (0, 0.3, 0)
    tail.scale = (0.8, 0.8, 1.2)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Subdivision
    modifier = tail.modifiers.new(name='Subdivision', type='SUBSURF')
    modifier.levels = 1
    
    # Move to collection
    bello_collection.objects.link(tail)
    bpy.context.scene.collection.objects.unlink(tail)
    
    # 5. EARS
    print('   Creating ears...')
    ear_positions = [
        (4.2, 0.6, 1.8),    # Right ear
        (4.2, -0.6, 1.8)    # Left ear
    ]
    
    for i, pos in enumerate(ear_positions):
        bpy.ops.mesh.primitive_cube_add(size=1, location=pos)
        ear = bpy.context.object
        ear.name = f'Bello_Ear_{i+1}'
        
        # Floppy ear shape
        ear.scale = (0.8, 0.3, 1.2)
        ear.rotation_euler = (0.2, 0, -0.3)  # Hanging ears
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        
        # Subdivision for soft ears
        modifier = ear.modifiers.new(name='Subdivision', type='SUBSURF')
        modifier.levels = 2
        
        # Move to collection
        bello_collection.objects.link(ear)
        bpy.context.scene.collection.objects.unlink(ear)
    
    print('✅ Bello base geometry created!')

def create_base_material():
    """Create the basic golden retriever material"""
    print('🎨 Creating base material...')
    
    # Create golden retriever material
    bello_material = bpy.data.materials.new(name='Bello_Golden_Fur')
    bello_material.use_nodes = True
    
    # Get the principled BSDF node
    bsdf = bello_material.node_tree.nodes['Principled BSDF']
    
    # Golden retriever colors
    bsdf.inputs[0].default_value = (0.8, 0.6, 0.3, 1.0)  # Base Color: Golden
    bsdf.inputs[4].default_value = 0.0    # Metallic: 0
    bsdf.inputs[9].default_value = 0.8    # Roughness: rough for fur effect
    
    # Apply to all body parts
    body_parts = ['Bello_Body', 'Bello_Head', 'Bello_Leg_1', 'Bello_Leg_2', 
                  'Bello_Leg_3', 'Bello_Leg_4', 'Bello_Tail', 'Bello_Ear_1', 'Bello_Ear_2']
    
    for part_name in body_parts:
        if part_name in bpy.data.objects:
            obj = bpy.data.objects[part_name]
            # Clear existing materials
            obj.data.materials.clear()
            # Add new material
            obj.data.materials.append(bello_material)
    
    print('✅ Base material applied!')

def setup_anatomy_collections():
    """Setup collections for medical visualization layers"""
    print('🫀 Setting up anatomy collections...')
    
    anatomy_collections = [
        'Bello_Skeleton',       # For X-ray visualization
        'Bello_Organs',         # For ultrasound/MRI
        'Bello_Muscles',        # For anatomy learning
        'Bello_BloodVessels',   # For circulation visualization
        'Bello_Nervous'         # For nervous system
    ]
    
    for collection_name in anatomy_collections:
        if collection_name not in bpy.data.collections:
            collection = bpy.data.collections.new(collection_name)
            bpy.context.scene.collection.children.link(collection)
            # Initially hide anatomy layers
            collection.hide_viewport = True
            print(f'   Created {collection_name}')
    
    print('✅ Anatomy collections ready!')

def setup_viewport():
    """Configure viewport for optimal viewing"""
    print('🖼️ Setting up viewport...')
    
    # Set viewport to material preview for immediate visual feedback
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for space in area.spaces:
                if space.type == 'VIEW_3D':
                    space.shading.type = 'MATERIAL'  # Material preview
                    space.overlay.show_overlays = True
                    space.overlay.show_wireframes = False
                    break
    
    print('✅ Viewport configured!')

def create_bello_model():
    """Main function to create the complete Bello model"""
    print('🚀 Starting Bello 3D Model Creation for VetScan Pro...')
    print('=' * 60)
    
    # Execute creation steps
    clear_scene()
    setup_lighting_and_camera()
    create_bello_base_geometry()
    create_base_material()
    setup_anatomy_collections()
    setup_viewport()
    
    # Final statistics
    bello_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Bello_')]
    bello_collections = [coll for coll in bpy.data.collections if 'Bello' in coll.name]
    
    print('=' * 60)
    print('🎉 BELLO MODEL CREATION COMPLETE!')
    print()
    print('📊 Model Statistics:')
    print(f'   - Objects created: {len(bello_objects)}')
    print(f'   - Collections: {len(bello_collections)}')
    print(f'   - Materials: 1 base material')
    print()
    print('🔬 Ready for medical visualization development!')
    print('💡 Next steps: Add skeleton, organs, and medical shaders')
    
    return True

if __name__ == "__main__":
    create_bello_model()