import bpy
from mathutils import Vector
import math

print("🔬 Setting up Medical Visualization System for Bello")

def create_visualization_collections():
    """Create organized collections for different medical views"""
    print("   Creating medical collections...")
    
    collections = {
        'Bello_Normal': 'Normal veterinary view',
        'Bello_XRay': 'X-Ray skeleton view', 
        'Bello_Ultrasound': 'Ultrasound organ view',
        'Bello_Thermal': 'Thermal heat signature',
        'Bello_MRI': 'MRI tissue differentiation'
    }
    
    for coll_name, description in collections.items():
        if coll_name not in bpy.data.collections:
            collection = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(collection)
            print(f"      Created: {coll_name}")

def create_medical_shaders():
    """Create specialized shaders for medical visualization"""
    print("   Creating medical shaders...")
    
    # X-RAY SHADER (Blue transparent with bone highlights)
    xray_mat = bpy.data.materials.new(name="Medical_XRay")
    xray_mat.use_nodes = True
    xray_nodes = xray_mat.node_tree.nodes
    xray_links = xray_mat.node_tree.links
    
    xray_nodes.clear()
    output = xray_nodes.new(type='ShaderNodeOutputMaterial')
    bsdf = xray_nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # X-Ray blue with high transparency
    bsdf.inputs[0].default_value = (0.2, 0.6, 1.0, 1.0)  # Blue
    bsdf.inputs[21].default_value = 0.15  # Very transparent
    bsdf.inputs[17].default_value = 0.8   # High transmission
    xray_mat.blend_method = 'BLEND'
    
    xray_links.new(bsdf.outputs[0], output.inputs[0])
    
    # ULTRASOUND SHADER (Grainy yellow-green medical look)
    ultrasound_mat = bpy.data.materials.new(name="Medical_Ultrasound")
    ultrasound_mat.use_nodes = True
    ultra_nodes = ultrasound_mat.node_tree.nodes
    ultra_links = ultrasound_mat.node_tree.links
    
    ultra_nodes.clear()
    ultra_output = ultra_nodes.new(type='ShaderNodeOutputMaterial')
    ultra_bsdf = ultra_nodes.new(type='ShaderNodeBsdfPrincipled')
    noise_tex = ultra_nodes.new(type='ShaderNodeTexNoise')
    
    # Ultrasound colors (yellowish-green)
    ultra_bsdf.inputs[0].default_value = (0.8, 0.9, 0.6, 1.0)
    ultra_bsdf.inputs[9].default_value = 0.95  # Very rough for grainy effect
    
    # Add noise for ultrasound grain
    noise_tex.inputs[2].default_value = 15.0  # Scale
    ultra_links.new(noise_tex.outputs[0], ultra_bsdf.inputs[0])
    ultra_links.new(ultra_bsdf.outputs[0], ultra_output.inputs[0])
    
    # THERMAL SHADER (Heat gradient from blue to red)
    thermal_mat = bpy.data.materials.new(name="Medical_Thermal")
    thermal_mat.use_nodes = True
    thermal_nodes = thermal_mat.node_tree.nodes
    thermal_links = thermal_mat.node_tree.links
    
    thermal_nodes.clear()
    thermal_output = thermal_nodes.new(type='ShaderNodeOutputMaterial')
    thermal_bsdf = thermal_nodes.new(type='ShaderNodeBsdfPrincipled')
    color_ramp = thermal_nodes.new(type='ShaderNodeValToRGB')
    coord = thermal_nodes.new(type='ShaderNodeTexCoord')
    
    # Setup thermal gradient (blue = cold, red = warm)
    color_ramp.color_ramp.elements[0].color = (0.0, 0.2, 1.0, 1.0)  # Cold blue
    color_ramp.color_ramp.elements[1].color = (1.0, 0.3, 0.0, 1.0)  # Warm red
    
    # Add emission for heat glow
    thermal_bsdf.inputs[19].default_value = 0.3  # Emission strength
    
    thermal_links.new(coord.outputs[2], color_ramp.inputs[0])  # Use Z coordinate for gradient
    thermal_links.new(color_ramp.outputs[0], thermal_bsdf.inputs[0])
    thermal_links.new(color_ramp.outputs[0], thermal_bsdf.inputs[19])  # Emission color
    thermal_links.new(thermal_bsdf.outputs[0], thermal_output.inputs[0])
    
    # MRI SHADER (Grayscale with tissue differentiation)
    mri_mat = bpy.data.materials.new(name="Medical_MRI")
    mri_mat.use_nodes = True
    mri_nodes = mri_mat.node_tree.nodes
    mri_links = mri_mat.node_tree.links
    
    mri_nodes.clear()
    mri_output = mri_nodes.new(type='ShaderNodeOutputMaterial')
    mri_bsdf = mri_nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # MRI grayscale appearance
    mri_bsdf.inputs[0].default_value = (0.7, 0.7, 0.7, 1.0)  # Gray
    mri_bsdf.inputs[9].default_value = 0.3  # Smooth for MRI look
    
    mri_links.new(mri_bsdf.outputs[0], mri_output.inputs[0])
    
    return xray_mat, ultrasound_mat, thermal_mat, mri_mat

def setup_skeleton_for_xray():
    """Create visible skeleton for X-ray mode"""
    print("   Creating X-ray skeleton...")
    
    # Simple spine (vertebrae chain)
    spine_positions = [Vector((-2.0 + i*0.8, 0, 1.2 + math.sin(i*0.5)*0.1)) for i in range(8)]
    
    for i, pos in enumerate(spine_positions):
        bpy.ops.mesh.primitive_cube_add(size=0.25, location=pos)
        vertebra = bpy.context.object
        vertebra.name = f"Skeleton_Vertebra_{i+1}"
        vertebra.hide_viewport = True  # Hidden by default
    
    # Ribs (simplified)
    rib_positions = [
        (0.5, 0.7, 1.3), (0.5, -0.7, 1.3),   # Front ribs
        (0, 0.8, 1.2), (0, -0.8, 1.2),       # Middle ribs  
        (-0.5, 0.7, 1.1), (-0.5, -0.7, 1.1)  # Back ribs
    ]
    
    for i, pos in enumerate(rib_positions):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.04, depth=1.2, location=pos)
        rib = bpy.context.object
        rib.name = f"Skeleton_Rib_{i+1}"
        rib.rotation_euler = (0, 0, 1.57)  # Horizontal
        rib.hide_viewport = True
    
    # Skull outline
    bpy.ops.mesh.primitive_cube_add(size=0.8, location=(4.0, 0, 1.3))
    skull = bpy.context.object
    skull.name = "Skeleton_Skull"
    skull.scale = (1.2, 0.8, 0.8)
    skull.hide_viewport = True

def create_organ_system():
    """Create detailed organ system for ultrasound/MRI"""
    print("   Creating organ system...")
    
    # Enhanced heart with anatomical shape
    bpy.ops.mesh.primitive_uv_sphere_add(location=(1.2, 0, 1.1), radius=0.35)
    heart = bpy.context.object
    heart.name = "Organ_Heart"
    heart.scale = (0.8, 1.3, 1.1)  # Heart proportions
    heart.hide_viewport = True
    
    # Lungs with proper positioning
    lung_positions = [(0.8, 0.6, 1.3), (0.8, -0.6, 1.3)]
    for i, pos in enumerate(lung_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos, radius=0.45)
        lung = bpy.context.object
        lung.name = f"Organ_Lung_{i+1}"
        lung.scale = (1.4, 0.8, 1.2)
        lung.hide_viewport = True
    
    # Liver (largest internal organ)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0.3, 0.8), size=0.7)
    liver = bpy.context.object
    liver.name = "Organ_Liver"  
    liver.scale = (1.6, 1.1, 0.7)
    liver.hide_viewport = True
    
    # Stomach
    bpy.ops.mesh.primitive_uv_sphere_add(location=(-0.5, -0.2, 0.9), radius=0.4)
    stomach = bpy.context.object
    stomach.name = "Organ_Stomach"
    stomach.scale = (1.3, 1.0, 0.9)
    stomach.hide_viewport = True
    
    # Kidneys (paired organs)
    kidney_positions = [(-1.0, 0.4, 1.0), (-1.0, -0.4, 1.0)]
    for i, pos in enumerate(kidney_positions):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos, radius=0.22)
        kidney = bpy.context.object
        kidney.name = f"Organ_Kidney_{i+1}"
        kidney.scale = (0.6, 1.2, 0.9)  # Kidney bean shape
        kidney.hide_viewport = True

def create_visualization_modes():
    """Create material groups for different medical modes"""
    print("   Setting up visualization modes...")
    
    xray_mat, ultrasound_mat, thermal_mat, mri_mat = create_medical_shaders()
    
    # Normal materials for different body parts
    body_mat = bpy.data.materials.new(name="Normal_Body")
    body_mat.use_nodes = True
    body_bsdf = body_mat.node_tree.nodes['Principled BSDF']
    body_bsdf.inputs[0].default_value = (0.85, 0.65, 0.35, 1.0)  # Golden fur
    body_bsdf.inputs[9].default_value = 0.8  # Roughness
    
    # Organ-specific materials (for educational coloring)
    organ_materials = {
        'heart': (0.8, 0.2, 0.2, 0.9),     # Red
        'lung': (0.9, 0.7, 0.8, 0.8),      # Pink
        'liver': (0.6, 0.3, 0.1, 0.9),     # Brown
        'stomach': (0.9, 0.8, 0.6, 0.8),   # Yellow-beige
        'kidney': (0.7, 0.3, 0.3, 0.9)     # Dark red
    }
    
    for organ, color in organ_materials.items():
        mat = bpy.data.materials.new(name=f"Organ_{organ.title()}")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes['Principled BSDF']
        bsdf.inputs[0].default_value = color
        bsdf.inputs[21].default_value = color[3]  # Alpha
        mat.blend_method = 'BLEND'

def create_animation_system():
    """Create basic animations for living tissue"""
    print("   Adding life-like animations...")
    
    # Heart beating animation
    if "Organ_Heart" in bpy.data.objects:
        heart = bpy.data.objects["Organ_Heart"]
        
        # Add keyframes for heartbeat
        heart.scale = (0.8, 1.3, 1.1)
        heart.keyframe_insert(data_path="scale", frame=1)
        
        heart.scale = (0.9, 1.4, 1.2)  # Expanded
        heart.keyframe_insert(data_path="scale", frame=30)
        
        heart.scale = (0.8, 1.3, 1.1)  # Back to normal
        heart.keyframe_insert(data_path="scale", frame=60)
        
        # Set interpolation to ease in/out for natural heartbeat
        if heart.animation_data:
            for fcurve in heart.animation_data.action.fcurves:
                for keyframe in fcurve.keyframe_points:
                    keyframe.interpolation = 'BEZIER'

def setup_medical_lighting():
    """Create medical-grade lighting setup"""
    print("   Configuring medical lighting...")
    
    # Main examination light (bright, clinical)
    bpy.ops.object.light_add(type='AREA', location=(3, 3, 8))
    exam_light = bpy.context.object
    exam_light.name = "Medical_ExamLight"
    exam_light.data.energy = 150
    exam_light.data.size = 2.0
    exam_light.data.color = (1.0, 0.98, 0.95)  # Slightly warm white
    
    # Fill light to reduce harsh shadows
    bpy.ops.object.light_add(type='AREA', location=(-2, -2, 6))
    fill_light = bpy.context.object
    fill_light.name = "Medical_FillLight"
    fill_light.data.energy = 80
    fill_light.data.size = 3.0
    
    # Rim light for definition
    bpy.ops.object.light_add(type='SPOT', location=(0, 6, 4))
    rim_light = bpy.context.object
    rim_light.name = "Medical_RimLight"
    rim_light.data.energy = 100
    rim_light.data.spot_size = 1.2
    rim_light.rotation_euler = (1.2, 0, 0)

# Execute medical visualization setup
create_visualization_collections()
setup_skeleton_for_xray()
create_organ_system()
create_visualization_modes()
create_animation_system()
setup_medical_lighting()

print("✅ Medical Visualization System Complete!")
print("🔬 Available modes:")
print("   - Normal: Regular veterinary examination")
print("   - X-Ray: Skeletal system visible")
print("   - Ultrasound: Internal organs highlighted")
print("   - Thermal: Heat signature visualization")
print("   - MRI: Tissue differentiation")
print("💡 Toggle visibility collections to switch modes!")