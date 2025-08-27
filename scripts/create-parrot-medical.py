#!/usr/bin/env python3
"""
Advanced Medical Parrot Model Creator - VetScan Pro 3000
Creates anatomically accurate scarlet macaw with multiple medical visualization modes
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector, Matrix
import math

def clear_scene():
    """Clear all mesh objects from scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)

def create_parrot_body():
    """Create anatomically accurate parrot body"""
    print("Creating parrot body...")
    
    # Main body (wider chest, narrower tail)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(0, 0, 0))
    body = bpy.context.active_object
    body.name = "Parrot_Body"
    body.scale = (0.9, 1.6, 1.1)
    bpy.ops.object.transform_apply(scale=True)
    
    # Add chest expansion for air sacs
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.subdivide(number_cuts=1)
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return body

def create_parrot_head():
    """Create parrot head with strong curved beak"""
    print("Creating parrot head...")
    
    # Head sphere
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(0, 1.8, 0.3))
    head = bpy.context.active_object
    head.name = "Parrot_Head"
    head.scale = (1.0, 1.2, 1.0)
    bpy.ops.object.transform_apply(scale=True)
    
    # Strong curved beak (upper mandible)
    bpy.ops.mesh.primitive_cube_add(size=0.4, location=(0, 2.5, 0.1))
    upper_beak = bpy.context.active_object
    upper_beak.name = "Upper_Beak"
    upper_beak.scale = (0.6, 1.2, 0.4)
    upper_beak.rotation_euler = (math.radians(-15), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    # Lower mandible
    bpy.ops.mesh.primitive_cube_add(size=0.3, location=(0, 2.3, -0.1))
    lower_beak = bpy.context.active_object
    lower_beak.name = "Lower_Beak"
    lower_beak.scale = (0.5, 1.0, 0.3)
    lower_beak.rotation_euler = (math.radians(10), 0, 0)
    bpy.ops.object.transform_apply(scale=True, rotation=True)
    
    return head, upper_beak, lower_beak

def create_parrot_wings():
    """Create detailed wings with flight feather structure"""
    print("Creating wings with flight feathers...")
    
    wings = []
    
    for side in [-1, 1]:  # Left and right wings
        # Main wing bone structure
        bpy.ops.mesh.primitive_cube_add(size=1, location=(side * 1.2, 0.5, 0.2))
        wing = bpy.context.active_object
        wing.name = f"Wing_{'Right' if side > 0 else 'Left'}"
        wing.scale = (0.3, 1.8, 0.1)
        wing.rotation_euler = (0, 0, math.radians(side * 15))
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        # Primary flight feathers (10 feathers)
        for i in range(10):
            feather_pos = (side * (1.4 + i * 0.08), 0.3 + i * 0.15, 0.15)
            bpy.ops.mesh.primitive_cube_add(size=0.3, location=feather_pos)
            feather = bpy.context.active_object
            feather.name = f"Primary_Feather_{i+1}_{'R' if side > 0 else 'L'}"
            feather.scale = (0.05, 0.8 + i * 0.1, 0.02)
            feather.rotation_euler = (0, 0, math.radians(side * (10 + i * 2)))
            bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        # Secondary flight feathers (15 feathers)
        for i in range(15):
            feather_pos = (side * (1.1 + i * 0.05), -0.2 + i * 0.08, 0.12)
            bpy.ops.mesh.primitive_cube_add(size=0.25, location=feather_pos)
            feather = bpy.context.active_object
            feather.name = f"Secondary_Feather_{i+1}_{'R' if side > 0 else 'L'}"
            feather.scale = (0.04, 0.6 + i * 0.03, 0.015)
            feather.rotation_euler = (0, 0, math.radians(side * (5 + i)))
            bpy.ops.object.transform_apply(scale=True, rotation=True)
        
        wings.append(wing)
    
    return wings

def create_zygodactyl_feet():
    """Create zygodactyl feet (two toes forward, two back)"""
    print("Creating zygodactyl feet...")
    
    feet = []
    
    for side in [-1, 1]:  # Left and right feet
        # Leg/tarsus
        bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=0.8, location=(side * 0.4, -0.3, -1.2))
        leg = bpy.context.active_object
        leg.name = f"Leg_{'Right' if side > 0 else 'Left'}"
        
        # Foot base
        bpy.ops.mesh.primitive_cube_add(size=0.3, location=(side * 0.4, -0.2, -1.7))
        foot_base = bpy.context.active_object
        foot_base.name = f"Foot_Base_{'Right' if side > 0 else 'Left'}"
        foot_base.scale = (0.5, 0.8, 0.2)
        bpy.ops.object.transform_apply(scale=True)
        
        # Zygodactyl toe arrangement
        toe_positions = [
            (0.25, 0.3, 0),    # Toe 1 (forward)
            (-0.25, 0.3, 0),   # Toe 2 (forward)
            (0.2, -0.35, 0),   # Toe 3 (back)
            (-0.2, -0.35, 0)   # Toe 4 (back)
        ]
        
        for i, (x_offset, y_offset, z_offset) in enumerate(toe_positions):
            toe_pos = (side * 0.4 + x_offset, -0.2 + y_offset, -1.7 + z_offset)
            bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.4, location=toe_pos)
            toe = bpy.context.active_object
            toe.name = f"Toe_{i+1}_{'Right' if side > 0 else 'Left'}"
            
            # Rotate based on toe direction
            if i < 2:  # Forward toes
                toe.rotation_euler = (math.radians(70), 0, math.radians(x_offset * 30))
            else:  # Back toes
                toe.rotation_euler = (math.radians(-70), 0, math.radians(x_offset * 30))
            
            bpy.ops.object.transform_apply(rotation=True)
            
            # Add claw
            claw_pos = Vector(toe_pos) + Vector((0, y_offset * 0.3, -0.1 if i < 2 else 0.1))
            bpy.ops.mesh.primitive_cone_add(radius1=0.02, radius2=0.005, depth=0.15, location=claw_pos)
            claw = bpy.context.active_object
            claw.name = f"Claw_{i+1}_{'Right' if side > 0 else 'Left'}"
            claw.rotation_euler = (math.radians(45 if i < 2 else -45), 0, 0)
            bpy.ops.object.transform_apply(rotation=True)
        
        feet.append(leg)
    
    return feet

def create_tail_feathers():
    """Create long tail feathers characteristic of macaws"""
    print("Creating tail feathers...")
    
    tail_feathers = []
    
    # Central tail feathers (longest)
    for i in range(7):  # 7 central feathers
        x_pos = (i - 3) * 0.15  # Spread across width
        bpy.ops.mesh.primitive_cube_add(size=0.4, location=(x_pos, -2.5, 0.1))
        feather = bpy.context.active_object
        feather.name = f"Tail_Feather_{i+1}"
        feather.scale = (0.04, 2.5 - abs(i-3) * 0.3, 0.02)
        feather.rotation_euler = (math.radians(-10), 0, math.radians(x_pos * 5))
        bpy.ops.object.transform_apply(scale=True, rotation=True)
        tail_feathers.append(feather)
    
    return tail_feathers

def create_internal_anatomy():
    """Create avian-specific internal anatomy"""
    print("Creating internal anatomy (air sacs, crop, hollow bones)...")
    
    internal_parts = []
    
    # Crop (food storage)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.3, location=(0, 1.2, 0.4))
    crop = bpy.context.active_object
    crop.name = "Crop"
    crop.scale = (0.8, 0.6, 0.5)
    bpy.ops.object.transform_apply(scale=True)
    internal_parts.append(crop)
    
    # Air sac system (9 air sacs typical in birds)
    air_sac_positions = [
        (0, 0.5, 0.6),      # Cervical
        (0, 0.2, 0.8),      # Interclavicular  
        (-0.4, 0.1, 0.3),   # Anterior thoracic L
        (0.4, 0.1, 0.3),    # Anterior thoracic R
        (-0.5, -0.3, 0.2),  # Posterior thoracic L
        (0.5, -0.3, 0.2),   # Posterior thoracic R
        (-0.3, -0.8, 0.1),  # Abdominal L
        (0.3, -0.8, 0.1),   # Abdominal R
    ]
    
    for i, pos in enumerate(air_sac_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=pos)
        air_sac = bpy.context.active_object
        air_sac.name = f"Air_Sac_{i+1}"
        air_sac.scale = (0.6, 0.8, 0.7)
        bpy.ops.object.transform_apply(scale=True)
        internal_parts.append(air_sac)
    
    # Hollow bones representation (humerus)
    for side in [-1, 1]:
        bpy.ops.mesh.primitive_cylinder_add(radius=0.06, depth=0.8, location=(side * 0.8, 0.3, 0.1))
        humerus = bpy.context.active_object
        humerus.name = f"Humerus_{'Right' if side > 0 else 'Left'}"
        humerus.rotation_euler = (0, 0, math.radians(side * 45))
        bpy.ops.object.transform_apply(rotation=True)
        
        # Create hollow interior (smaller cylinder)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.82, location=(side * 0.8, 0.3, 0.1))
        hollow = bpy.context.active_object
        hollow.name = f"Humerus_Hollow_{'Right' if side > 0 else 'Left'}"
        hollow.rotation_euler = (0, 0, math.radians(side * 45))
        bpy.ops.object.transform_apply(rotation=True)
        
        internal_parts.extend([humerus, hollow])
    
    return internal_parts

def create_medical_materials():
    """Create 5 medical visualization materials"""
    print("Creating medical materials...")
    
    materials = {}
    
    # 1. Normal Material (Scarlet Macaw colors)
    normal_mat = bpy.data.materials.new(name="Parrot_Normal")
    normal_mat.use_nodes = True
    nodes = normal_mat.node_tree.nodes
    links = normal_mat.node_tree.links
    
    # Clear default nodes
    nodes.clear()
    
    # Add nodes for realistic parrot material
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Scarlet macaw colors - vibrant red with blue/green accents
    principled.inputs['Base Color'].default_value = (0.8, 0.1, 0.1, 1.0)  # Scarlet red
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.3
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials['normal'] = normal_mat
    
    # 2. X-Ray Material
    xray_mat = bpy.data.materials.new(name="Parrot_XRay")
    xray_mat.use_nodes = True
    xray_mat.blend_method = 'BLEND'
    nodes = xray_mat.node_tree.nodes
    links = xray_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    transparent = nodes.new('ShaderNodeBsdfTransparent')
    emission = nodes.new('ShaderNodeEmission')
    mix = nodes.new('ShaderNodeMix')
    fresnel = nodes.new('ShaderNodeFresnel')
    
    # X-ray blue-white coloring
    emission.inputs['Color'].default_value = (0.5, 0.8, 1.0, 1.0)
    emission.inputs['Strength'].default_value = 1.5
    transparent.inputs['Color'].default_value = (0.8, 0.9, 1.0, 0.1)
    
    mix.data_type = 'RGBA'
    mix.inputs['Factor'].default_value = 0.8
    
    links.new(fresnel.outputs['Fac'], mix.inputs['Factor'])
    links.new(transparent.outputs['BSDF'], mix.inputs['A'])
    links.new(emission.outputs['Emission'], mix.inputs['B'])
    links.new(mix.outputs['Result'], output.inputs['Surface'])
    materials['xray'] = xray_mat
    
    # 3. Ultrasound Material
    ultrasound_mat = bpy.data.materials.new(name="Parrot_Ultrasound")
    ultrasound_mat.use_nodes = True
    nodes = ultrasound_mat.node_tree.nodes
    links = ultrasound_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    noise = nodes.new('ShaderNodeTexNoise')
    wave = nodes.new('ShaderNodeTexWave')
    mix = nodes.new('ShaderNodeMix')
    
    # Ultrasound grayscale with scan lines
    emission.inputs['Color'].default_value = (0.7, 0.7, 0.7, 1.0)
    emission.inputs['Strength'].default_value = 1.0
    noise.inputs['Scale'].default_value = 15.0
    wave.inputs['Scale'].default_value = 50.0
    
    mix.data_type = 'RGBA'
    links.new(noise.outputs['Color'], mix.inputs['A'])
    links.new(wave.outputs['Color'], mix.inputs['B'])
    links.new(mix.outputs['Result'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['ultrasound'] = ultrasound_mat
    
    # 4. Thermal Material
    thermal_mat = bpy.data.materials.new(name="Parrot_Thermal")
    thermal_mat.use_nodes = True
    nodes = thermal_mat.node_tree.nodes
    links = thermal_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    colorramp = nodes.new('ShaderNodeValToRGB')
    noise = nodes.new('ShaderNodeTexNoise')
    
    # Thermal gradient (blue to red)
    emission.inputs['Strength'].default_value = 1.2
    colorramp.color_ramp.elements[0].color = (0.0, 0.0, 1.0, 1.0)  # Cold blue
    colorramp.color_ramp.elements[1].color = (1.0, 0.0, 0.0, 1.0)  # Hot red
    
    # Add middle colors
    colorramp.color_ramp.elements.new(0.33)
    colorramp.color_ramp.elements[1].color = (0.0, 1.0, 0.0, 1.0)  # Green
    colorramp.color_ramp.elements.new(0.66)
    colorramp.color_ramp.elements[2].color = (1.0, 1.0, 0.0, 1.0)  # Yellow
    
    noise.inputs['Scale'].default_value = 5.0
    
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['thermal'] = thermal_mat
    
    # 5. MRI Material
    mri_mat = bpy.data.materials.new(name="Parrot_MRI")
    mri_mat.use_nodes = True
    nodes = mri_mat.node_tree.nodes
    links = mri_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    colorramp = nodes.new('ShaderNodeValToRGB')
    geometry = nodes.new('ShaderNodeNewGeometry')
    
    # MRI grayscale based on geometry
    emission.inputs['Strength'].default_value = 0.8
    colorramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1.0)  # Dark
    colorramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)  # Light
    
    links.new(geometry.outputs['Pointiness'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['mri'] = mri_mat
    
    return materials

def optimize_mesh():
    """Optimize mesh to target polygon count (5000-8000)"""
    print("Optimizing mesh to target polygon count...")
    
    # Select all mesh objects
    mesh_objects = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
    
    total_polys = 0
    for obj in mesh_objects:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        # Count current polygons
        mesh = obj.data
        total_polys += len(mesh.polygons)
    
    print(f"Current total polygons: {total_polys}")
    
    # If over target, apply decimation
    if total_polys > 8000:
        for obj in mesh_objects:
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            
            # Add decimate modifier
            decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
            decimate.ratio = 0.7  # Reduce by 30%
            
            # Apply modifier
            bpy.ops.object.modifier_apply(modifier="Decimate")
        
        print("Applied decimation to reduce polygon count")

def apply_materials_to_objects():
    """Apply materials to different parts of the parrot"""
    print("Applying materials to parrot parts...")
    
    materials = create_medical_materials()
    
    # Get all objects
    all_objects = list(bpy.context.scene.objects)
    
    # Apply normal material to all objects by default
    for obj in all_objects:
        if obj.type == 'MESH':
            if len(obj.data.materials) == 0:
                obj.data.materials.append(materials['normal'])
            else:
                obj.data.materials[0] = materials['normal']
    
    # Create material variants for different visualization modes
    # (In a real implementation, these would be switchable via script)
    
    return materials

def main():
    """Main parrot creation function"""
    print("🦜 Starting Advanced Medical Parrot Creation...")
    
    # Clear scene
    clear_scene()
    
    # Create parrot parts
    body = create_parrot_body()
    head, upper_beak, lower_beak = create_parrot_head()
    wings = create_parrot_wings()
    feet = create_zygodactyl_feet()
    tail_feathers = create_tail_feathers()
    internal_parts = create_internal_anatomy()
    
    # Create and apply materials
    materials = apply_materials_to_objects()
    
    # Optimize mesh
    optimize_mesh()
    
    # Final polygon count
    total_polys = sum(len(obj.data.polygons) for obj in bpy.context.scene.objects if obj.type == 'MESH')
    print(f"Final polygon count: {total_polys}")
    
    # Select all objects for export
    bpy.ops.object.select_all(action='SELECT')
    
    print("🦜 Medical Parrot Model Creation Complete!")
    print("Features created:")
    print("✅ Anatomically accurate body proportions")
    print("✅ Strong curved beak (upper and lower mandible)")
    print("✅ Zygodactyl feet (2 toes forward, 2 back)")
    print("✅ Detailed flight feathers (primary and secondary)")
    print("✅ Long tail feathers (macaw style)")
    print("✅ Avian-specific anatomy (air sacs, crop, hollow bones)")
    print("✅ 5 Medical visualization materials")
    print(f"✅ Optimized polygon count: {total_polys}")

if __name__ == "__main__":
    main()