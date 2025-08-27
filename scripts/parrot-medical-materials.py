#!/usr/bin/env python3
"""
Parrot Medical Visualization Materials - VetScan Pro 3000
Creates 5 medical visualization materials for the parrot model
"""

import bpy

def create_medical_materials():
    """Create all 5 medical visualization materials for parrot"""
    
    materials = {}
    
    # 1. Normal Material (Scarlet Macaw)
    normal_mat = bpy.data.materials.new(name="Parrot_Normal")
    normal_mat.use_nodes = True
    nodes = normal_mat.node_tree.nodes
    links = normal_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    principled = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Vibrant scarlet macaw colors
    principled.inputs['Base Color'].default_value = (0.9, 0.1, 0.1, 1.0)
    principled.inputs['Metallic'].default_value = 0.0
    principled.inputs['Roughness'].default_value = 0.3
    
    links.new(principled.outputs['BSDF'], output.inputs['Surface'])
    materials['normal'] = normal_mat
    
    # 2. X-Ray Material (Transparent with bone structure)
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
    
    # X-ray blue-white appearance
    emission.inputs['Color'].default_value = (0.6, 0.8, 1.0, 1.0)
    emission.inputs['Strength'].default_value = 1.2
    transparent.inputs['Color'].default_value = (0.8, 0.9, 1.0, 0.2)
    
    mix.data_type = 'RGBA'
    mix.inputs['Factor'].default_value = 0.7
    
    links.new(fresnel.outputs['Fac'], mix.inputs['Factor'])
    links.new(transparent.outputs['BSDF'], mix.inputs['A'])
    links.new(emission.outputs['Emission'], mix.inputs['B'])
    links.new(mix.outputs['Result'], output.inputs['Surface'])
    materials['xray'] = xray_mat
    
    # 3. Ultrasound Material (Grayscale with scan lines)
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
    
    # Ultrasound appearance
    emission.inputs['Color'].default_value = (0.7, 0.7, 0.7, 1.0)
    emission.inputs['Strength'].default_value = 1.0
    noise.inputs['Scale'].default_value = 12.0
    wave.inputs['Scale'].default_value = 40.0
    
    mix.data_type = 'RGBA'
    links.new(noise.outputs['Color'], mix.inputs['A'])
    links.new(wave.outputs['Color'], mix.inputs['B'])
    links.new(mix.outputs['Result'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['ultrasound'] = ultrasound_mat
    
    # 4. Thermal Material (Heat gradient)
    thermal_mat = bpy.data.materials.new(name="Parrot_Thermal")
    thermal_mat.use_nodes = True
    nodes = thermal_mat.node_tree.nodes
    links = thermal_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    colorramp = nodes.new('ShaderNodeValToRGB')
    noise = nodes.new('ShaderNodeTexNoise')
    
    # Thermal gradient setup
    emission.inputs['Strength'].default_value = 1.5
    
    # Create thermal color gradient
    colorramp.color_ramp.elements[0].color = (0.0, 0.0, 1.0, 1.0)  # Cold blue
    colorramp.color_ramp.elements[1].color = (1.0, 0.0, 0.0, 1.0)  # Hot red
    
    # Add intermediate colors
    colorramp.color_ramp.elements.new(0.25)
    colorramp.color_ramp.elements[1].color = (0.0, 0.5, 1.0, 1.0)  # Light blue
    colorramp.color_ramp.elements.new(0.5)
    colorramp.color_ramp.elements[2].color = (0.0, 1.0, 0.0, 1.0)  # Green
    colorramp.color_ramp.elements.new(0.75)
    colorramp.color_ramp.elements[3].color = (1.0, 1.0, 0.0, 1.0)  # Yellow
    
    noise.inputs['Scale'].default_value = 8.0
    
    links.new(noise.outputs['Fac'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['thermal'] = thermal_mat
    
    # 5. MRI Material (Tissue differentiation)
    mri_mat = bpy.data.materials.new(name="Parrot_MRI")
    mri_mat.use_nodes = True
    nodes = mri_mat.node_tree.nodes
    links = mri_mat.node_tree.links
    nodes.clear()
    
    output = nodes.new('ShaderNodeOutputMaterial')
    emission = nodes.new('ShaderNodeEmission')
    colorramp = nodes.new('ShaderNodeValToRGB')
    geometry = nodes.new('ShaderNodeNewGeometry')
    
    # MRI appearance based on geometry
    emission.inputs['Strength'].default_value = 0.9
    
    # MRI grayscale gradient
    colorramp.color_ramp.elements[0].color = (0.1, 0.1, 0.1, 1.0)  # Dark tissue
    colorramp.color_ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)  # Light tissue
    
    # Add intermediate gray
    colorramp.color_ramp.elements.new(0.5)
    colorramp.color_ramp.elements[1].color = (0.5, 0.5, 0.5, 1.0)  # Medium gray
    
    links.new(geometry.outputs['Pointiness'], colorramp.inputs['Fac'])
    links.new(colorramp.outputs['Color'], emission.inputs['Color'])
    links.new(emission.outputs['Emission'], output.inputs['Surface'])
    materials['mri'] = mri_mat
    
    return materials

def apply_materials_to_parrot():
    """Apply the normal material by default, create others for switching"""
    
    print("Creating medical visualization materials...")
    materials = create_medical_materials()
    
    # Apply normal material to all mesh objects
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            if len(obj.data.materials) == 0:
                obj.data.materials.append(materials['normal'])
            else:
                obj.data.materials[0] = materials['normal']
    
    print("✅ Medical materials created:")
    for name, mat in materials.items():
        print(f"   - {name.capitalize()}: {mat.name}")
    
    return materials

def create_material_switching_script():
    """Create a script for switching between medical materials"""
    
    switch_script = '''
# Parrot Medical Material Switching Script for VetScan Pro 3000
# Use this script to switch between different medical visualization modes

import bpy

def switch_to_material(material_name):
    """Switch all parrot objects to specified material"""
    
    if material_name not in bpy.data.materials:
        print(f"Material {material_name} not found!")
        return False
    
    material = bpy.data.materials[material_name]
    
    # Apply to all mesh objects
    for obj in bpy.context.scene.objects:
        if obj.type == 'MESH':
            if len(obj.data.materials) == 0:
                obj.data.materials.append(material)
            else:
                obj.data.materials[0] = material
    
    print(f"Switched to {material_name} visualization mode")
    return True

# Usage examples:
# switch_to_material("Parrot_Normal")     # Scarlet macaw colors
# switch_to_material("Parrot_XRay")       # X-ray visualization
# switch_to_material("Parrot_Ultrasound") # Ultrasound visualization
# switch_to_material("Parrot_Thermal")    # Thermal imaging
# switch_to_material("Parrot_MRI")        # MRI visualization

def show_available_materials():
    """Show all available medical materials"""
    medical_materials = [mat.name for mat in bpy.data.materials if mat.name.startswith("Parrot_")]
    print("Available medical visualization modes:")
    for mat in medical_materials:
        print(f"  - {mat}")

# Uncomment to see available materials:
# show_available_materials()
'''
    
    return switch_script

def main():
    """Main function to create medical materials"""
    
    print("🦜 Creating Parrot Medical Visualization Materials...")
    
    # Create and apply materials
    materials = apply_materials_to_parrot()
    
    # Create switching script
    switch_script = create_material_switching_script()
    
    print("📝 Material switching script created (can be used in Blender console)")
    print("🦜 Medical visualization system complete!")
    print("")
    print("Available visualization modes:")
    print("  1. Normal - Realistic scarlet macaw coloring")
    print("  2. X-Ray - Transparent with bone structure highlighting")
    print("  3. Ultrasound - Grayscale with scan line patterns")
    print("  4. Thermal - Heat gradient from blue (cold) to red (hot)")
    print("  5. MRI - Tissue differentiation in grayscale")

if __name__ == "__main__":
    main()
'''