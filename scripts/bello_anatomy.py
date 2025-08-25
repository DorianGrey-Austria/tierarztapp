import bpy
from mathutils import Vector
import bmesh

print("🫀 Creating Bello Anatomical System")

def create_skeleton():
    """Create simplified skeleton for X-ray visualization"""
    print("   Creating skeleton...")
    
    # Create skeleton collection
    if 'Bello_Skeleton' not in bpy.data.collections:
        skeleton_collection = bpy.data.collections.new('Bello_Skeleton')
        bpy.context.scene.collection.children.link(skeleton_collection)
    else:
        skeleton_collection = bpy.data.collections['Bello_Skeleton']
    
    # Spine/backbone (series of connected vertebrae)
    spine_positions = [
        (-2.0, 0, 1.2), (-1.0, 0, 1.3), (0, 0, 1.4), (1.0, 0, 1.3), (2.0, 0, 1.2), (3.0, 0, 1.1)
    ]
    
    for i, pos in enumerate(spine_positions):
        bpy.ops.mesh.primitive_cube_add(size=0.3, location=pos)
        vertebra = bpy.context.object
        vertebra.name = f'Spine_Vertebra_{i+1}'
        skeleton_collection.objects.link(vertebra)
        bpy.context.scene.collection.objects.unlink(vertebra)
    
    # Ribs (simplified)
    rib_positions = [
        (0.5, 0.8, 1.4), (0.5, -0.8, 1.4),  # Front ribs
        (0, 0.9, 1.3), (0, -0.9, 1.3),      # Middle ribs
        (-0.5, 0.8, 1.2), (-0.5, -0.8, 1.2)  # Back ribs
    ]
    
    for i, pos in enumerate(rib_positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.05, depth=1.5, location=pos)
        rib = bpy.context.object
        rib.name = f'Rib_{i+1}'
        rib.rotation_euler = (0, 0, 1.57)  # Horizontal
        skeleton_collection.objects.link(rib)
        bpy.context.scene.collection.objects.unlink(rib)
    
    # Skull (simplified)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(4.0, 0, 1.3))
    skull = bpy.context.object
    skull.name = 'Skull'
    skull.scale = (1.2, 0.8, 0.8)
    skeleton_collection.objects.link(skull)
    bpy.context.scene.collection.objects.unlink(skull)
    
    # Leg bones (simplified)
    leg_bone_positions = [
        (1.5, 0.8, 0.8), (1.5, -0.8, 0.8),    # Front legs
        (-1.5, 0.8, 0.8), (-1.5, -0.8, 0.8)   # Back legs
    ]
    
    for i, pos in enumerate(leg_bone_positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=0.8, location=pos)
        bone = bpy.context.object
        bone.name = f'Leg_Bone_{i+1}'
        skeleton_collection.objects.link(bone)
        bpy.context.scene.collection.objects.unlink(bone)
    
    # Skeleton material (for X-ray visualization)
    skeleton_mat = bpy.data.materials.new(name='Skeleton_Material')
    skeleton_mat.use_nodes = True
    bsdf = skeleton_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs[0].default_value = (0.9, 0.9, 0.8, 1.0)  # Bone white
    bsdf.inputs[9].default_value = 0.2  # Smooth bones
    
    # Apply to all skeleton objects
    for obj in skeleton_collection.objects:
        if obj.type == 'MESH':
            obj.data.materials.append(skeleton_mat)
    
    # Initially hide skeleton
    skeleton_collection.hide_viewport = True
    print("   ✅ Skeleton created")

def create_organs():
    """Create internal organs for ultrasound/MRI visualization"""
    print("   Creating organs...")
    
    # Create organs collection
    if 'Bello_Organs' not in bpy.data.collections:
        organs_collection = bpy.data.collections.new('Bello_Organs')
        bpy.context.scene.collection.children.link(organs_collection)
    else:
        organs_collection = bpy.data.collections['Bello_Organs']
    
    # Heart (animated later)
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(1.2, 0, 1.1))
    heart = bpy.context.object
    heart.name = 'Heart'
    heart.scale = (0.8, 1.2, 1.0)  # Heart shape
    organs_collection.objects.link(heart)
    bpy.context.scene.collection.objects.unlink(heart)
    
    # Lungs (two separate objects)
    lung_positions = [(0.8, 0.6, 1.3), (0.8, -0.6, 1.3)]
    for i, pos in enumerate(lung_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=pos)
        lung = bpy.context.object
        lung.name = f'Lung_{i+1}'
        lung.scale = (1.5, 0.8, 1.2)  # Lung shape
        organs_collection.objects.link(lung)
        bpy.context.scene.collection.objects.unlink(lung)
    
    # Liver
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=(0, 0.3, 0.8))
    liver = bpy.context.object
    liver.name = 'Liver'
    liver.scale = (1.5, 1.0, 0.6)
    organs_collection.objects.link(liver)
    bpy.context.scene.collection.objects.unlink(liver)
    
    # Stomach
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.4, location=(-0.5, 0, 0.9))
    stomach = bpy.context.object
    stomach.name = 'Stomach'
    stomach.scale = (1.2, 1.0, 0.8)
    organs_collection.objects.link(stomach)
    bpy.context.scene.collection.objects.unlink(stomach)
    
    # Kidneys
    kidney_positions = [(-1.0, 0.4, 1.0), (-1.0, -0.4, 1.0)]
    for i, pos in enumerate(kidney_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.2, location=pos)
        kidney = bpy.context.object
        kidney.name = f'Kidney_{i+1}'
        kidney.scale = (0.6, 1.2, 0.8)  # Kidney shape
        organs_collection.objects.link(kidney)
        bpy.context.scene.collection.objects.unlink(kidney)
    
    # Organ materials (different colors for educational purposes)
    organ_materials = {
        'Heart': (0.8, 0.2, 0.2, 0.8),      # Red heart
        'Lung': (0.8, 0.6, 0.8, 0.7),       # Pink lungs
        'Liver': (0.6, 0.3, 0.1, 0.8),      # Brown liver
        'Stomach': (0.9, 0.8, 0.6, 0.7),    # Yellow stomach
        'Kidney': (0.7, 0.3, 0.3, 0.8)      # Dark red kidneys
    }
    
    for obj in organs_collection.objects:
        if obj.type == 'MESH':
            mat_name = f'{obj.name}_Material'
            material = bpy.data.materials.new(name=mat_name)
            material.use_nodes = True
            bsdf = material.node_tree.nodes['Principled BSDF']
            
            # Set organ-specific color
            organ_type = obj.name.split('_')[0] if '_' in obj.name else obj.name
            if organ_type in organ_materials:
                bsdf.inputs[0].default_value = organ_materials[organ_type]
            else:
                bsdf.inputs[0].default_value = (0.8, 0.4, 0.4, 0.8)  # Default red
            
            # Make organs slightly transparent
            bsdf.inputs[21].default_value = 0.8  # Alpha
            material.blend_method = 'BLEND'
            
            obj.data.materials.append(material)
    
    # Initially hide organs
    organs_collection.hide_viewport = True
    print("   ✅ Organs created")

def create_blood_vessels():
    """Create simplified blood vessel system"""
    print("   Creating blood vessels...")
    
    # Create blood vessels collection
    if 'Bello_BloodVessels' not in bpy.data.collections:
        vessels_collection = bpy.data.collections.new('Bello_BloodVessels')
        bpy.context.scene.collection.children.link(vessels_collection)
    else:
        vessels_collection = bpy.data.collections['Bello_BloodVessels']
    
    # Main arteries (curves for organic flow)
    artery_points = [
        (1.2, 0, 1.1),    # Heart
        (0.5, 0, 1.0),    # Chest
        (-0.5, 0, 0.9),   # Abdomen
        (-1.5, 0, 0.8)    # Back
    ]
    
    # Create curve for main artery
    curve_data = bpy.data.curves.new('Main_Artery', type='CURVE')
    curve_data.dimensions = '3D'
    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(len(artery_points) - 1)
    
    for i, point in enumerate(artery_points):
        spline.bezier_points[i].co = point
        spline.bezier_points[i].handle_left = (point[0] - 0.5, point[1], point[2])
        spline.bezier_points[i].handle_right = (point[0] + 0.5, point[1], point[2])
    
    # Create curve object
    artery_obj = bpy.data.objects.new('Main_Artery', curve_data)
    vessels_collection.objects.link(artery_obj)
    
    # Add thickness to curve
    curve_data.bevel_depth = 0.05
    curve_data.bevel_resolution = 4
    
    # Blood vessel material
    vessel_mat = bpy.data.materials.new(name='BloodVessel_Material')
    vessel_mat.use_nodes = True
    bsdf = vessel_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs[0].default_value = (0.7, 0.1, 0.1, 0.9)  # Dark red
    bsdf.inputs[21].default_value = 0.6  # Semi-transparent
    vessel_mat.blend_method = 'BLEND'
    
    artery_obj.data.materials.append(vessel_mat)
    
    # Initially hide blood vessels
    vessels_collection.hide_viewport = True
    print("   ✅ Blood vessels created")

def setup_medical_materials():
    """Setup materials for different medical visualization modes"""
    print("   Setting up medical visualization materials...")
    
    # X-Ray Material (for skeleton)
    xray_mat = bpy.data.materials.new(name='XRay_Material')
    xray_mat.use_nodes = True
    bsdf = xray_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs[0].default_value = (0.1, 0.3, 0.8, 1.0)  # Blue tint
    bsdf.inputs[21].default_value = 0.3  # Very transparent
    bsdf.inputs[17].default_value = 1.0  # Full transmission
    xray_mat.blend_method = 'BLEND'
    
    # Ultrasound Material (grainy, echo-like)
    ultrasound_mat = bpy.data.materials.new(name='Ultrasound_Material')
    ultrasound_mat.use_nodes = True
    bsdf = ultrasound_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs[0].default_value = (0.8, 0.8, 0.6, 1.0)  # Yellowish
    bsdf.inputs[9].default_value = 0.9  # Very rough for grainy effect
    
    # Thermal Material (heat signature)
    thermal_mat = bpy.data.materials.new(name='Thermal_Material')
    thermal_mat.use_nodes = True
    bsdf = thermal_mat.node_tree.nodes['Principled BSDF']
    # Will be adjusted with color ramp for heat visualization
    bsdf.inputs[0].default_value = (1.0, 0.5, 0.0, 1.0)  # Orange heat
    bsdf.inputs[19].default_value = 0.5  # Slight emission
    
    print("   ✅ Medical materials created")

# Execute anatomy creation
create_skeleton()
create_organs()  
create_blood_vessels()
setup_medical_materials()

print("🎉 Bello anatomical system complete!")
print("💡 Use collections to toggle visibility:")
print("   - Bello_Skeleton (X-ray mode)")
print("   - Bello_Organs (Ultrasound/MRI)")
print("   - Bello_BloodVessels (Circulation)")