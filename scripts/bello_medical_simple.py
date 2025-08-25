import bpy

print("🔬 Creating Simple Medical Visualization System")

def create_medical_materials():
    """Create simple but effective medical materials"""
    
    # X-RAY Material (blue transparent)
    xray_mat = bpy.data.materials.new(name="XRay_Mode")
    xray_mat.use_nodes = True
    bsdf = xray_mat.node_tree.nodes['Principled BSDF']
    bsdf.inputs[0].default_value = (0.3, 0.7, 1.0, 1.0)  # Blue
    bsdf.inputs['Alpha'].default_value = 0.2  # Very transparent
    xray_mat.blend_method = 'BLEND'
    
    # ULTRASOUND Material (yellowish grainy)
    ultrasound_mat = bpy.data.materials.new(name="Ultrasound_Mode")
    ultrasound_mat.use_nodes = True
    ultra_bsdf = ultrasound_mat.node_tree.nodes['Principled BSDF']
    ultra_bsdf.inputs[0].default_value = (0.9, 0.9, 0.7, 1.0)  # Yellow
    ultra_bsdf.inputs['Roughness'].default_value = 0.95  # Very rough
    
    # THERMAL Material (heat colors)
    thermal_mat = bpy.data.materials.new(name="Thermal_Mode")
    thermal_mat.use_nodes = True
    thermal_bsdf = thermal_mat.node_tree.nodes['Principled BSDF']
    thermal_bsdf.inputs[0].default_value = (1.0, 0.4, 0.1, 1.0)  # Orange-red
    thermal_bsdf.inputs['Emission Strength'].default_value = 0.3  # Glow
    thermal_bsdf.inputs['Emission Color'].default_value = (1.0, 0.6, 0.2, 1.0)
    
    # MRI Material (grayscale)
    mri_mat = bpy.data.materials.new(name="MRI_Mode")
    mri_mat.use_nodes = True
    mri_bsdf = mri_mat.node_tree.nodes['Principled BSDF']
    mri_bsdf.inputs[0].default_value = (0.6, 0.6, 0.6, 1.0)  # Gray
    
    print("   ✅ Medical materials created")
    return xray_mat, ultrasound_mat, thermal_mat, mri_mat

def create_anatomy_objects():
    """Create simple anatomical objects"""
    
    # Heart (red, slightly hidden)
    bpy.ops.mesh.primitive_uv_sphere_add(location=(1.2, 0, 1.1), radius=0.3)
    heart = bpy.context.object
    heart.name = "Medical_Heart"
    heart.hide_viewport = True  # Hidden by default
    
    # Create heart material
    heart_mat = bpy.data.materials.new(name="Heart_Red")
    heart_mat.use_nodes = True
    heart_bsdf = heart_mat.node_tree.nodes['Principled BSDF']
    heart_bsdf.inputs[0].default_value = (0.8, 0.1, 0.1, 0.8)  # Red
    heart_bsdf.inputs['Alpha'].default_value = 0.8
    heart_mat.blend_method = 'BLEND'
    heart.data.materials.append(heart_mat)
    
    # Lungs (pink, paired)
    for i, pos in enumerate([(0.8, 0.5, 1.2), (0.8, -0.5, 1.2)]):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos, radius=0.4)
        lung = bpy.context.object
        lung.name = f"Medical_Lung_{i+1}"
        lung.scale = (1.3, 0.7, 1.0)
        lung.hide_viewport = True
        
        # Lung material
        lung_mat = bpy.data.materials.new(name=f"Lung_Pink_{i+1}")
        lung_mat.use_nodes = True
        lung_bsdf = lung_mat.node_tree.nodes['Principled BSDF']
        lung_bsdf.inputs[0].default_value = (1.0, 0.7, 0.8, 0.7)  # Pink
        lung_bsdf.inputs['Alpha'].default_value = 0.7
        lung_mat.blend_method = 'BLEND'
        lung.data.materials.append(lung_mat)
    
    # Simple skeleton (spine)
    spine_positions = [(-1.5, 0, 1.2), (-0.5, 0, 1.3), (0.5, 0, 1.3), (1.5, 0, 1.2)]
    for i, pos in enumerate(spine_positions):
        bpy.ops.mesh.primitive_cube_add(size=0.2, location=pos)
        vertebra = bpy.context.object
        vertebra.name = f"Skeleton_Vertebra_{i+1}"
        vertebra.hide_viewport = True
        
        # Bone material
        bone_mat = bpy.data.materials.new(name=f"Bone_{i+1}")
        bone_mat.use_nodes = True
        bone_bsdf = bone_mat.node_tree.nodes['Principled BSDF']
        bone_bsdf.inputs[0].default_value = (0.9, 0.9, 0.8, 1.0)  # Bone white
        vertebra.data.materials.append(bone_mat)
    
    print("   ✅ Anatomy objects created")

def setup_visualization_collections():
    """Organize objects into collections for easy switching"""
    
    # Create collections
    collections_to_create = ['Normal_View', 'XRay_View', 'Ultrasound_View', 'Thermal_View', 'MRI_View']
    
    for coll_name in collections_to_create:
        if coll_name not in bpy.data.collections:
            collection = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(collection)
    
    print("   ✅ Visualization collections created")

def create_medical_camera_setup():
    """Position camera for optimal medical viewing"""
    
    # Medical examination camera position
    bpy.ops.object.camera_add(location=(6, -6, 4))
    med_camera = bpy.context.object
    med_camera.name = "Medical_Camera"
    med_camera.rotation_euler = (1.0, 0, 0.785)
    
    # Set as active camera
    bpy.context.scene.camera = med_camera
    
    # Medical lighting (bright, even illumination)
    bpy.ops.object.light_add(type='SUN', location=(4, 4, 8))
    med_light = bpy.context.object
    med_light.name = "Medical_Light"
    med_light.data.energy = 5
    med_light.data.color = (1.0, 0.98, 0.95)  # Clinical white
    
    print("   ✅ Medical camera and lighting setup")

# Execute medical system setup
print("🏥 Setting up medical visualization...")
xray_mat, ultrasound_mat, thermal_mat, mri_mat = create_medical_materials()
create_anatomy_objects()
setup_visualization_collections()
create_medical_camera_setup()

print("✅ Simple Medical Visualization System Complete!")
print()
print("🔬 Medical Modes Available:")
print("   1. Normal Mode: Regular Bello appearance")
print("   2. X-Ray Mode: Show skeleton (unhide Skeleton_ objects)")
print("   3. Ultrasound Mode: Show organs (unhide Medical_ organs)")  
print("   4. Thermal Mode: Apply thermal materials")
print("   5. MRI Mode: Apply MRI materials")
print()
print("💡 Toggle object visibility to switch between modes!")
print("🎮 Ready for integration with VetScan Pro game!")