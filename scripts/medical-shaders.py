#!/usr/bin/env python3
"""
Medical Shaders für VetScan Pro 3000 Bello Model
Erstellt verschiedene medizinische Visualisierungs-Materialien
"""

import bpy
import json
from mathutils import Vector, Color

class MedicalShaderGenerator:
    """Erstellt medizinische Visualisierungs-Shader für Bello"""
    
    def __init__(self, target_object="Bello"):
        self.target_object = target_object
        
    def clear_materials(self):
        """Entfernt alle bestehenden Materialien vom Target Object"""
        if self.target_object in bpy.data.objects:
            obj = bpy.data.objects[self.target_object]
            obj.data.materials.clear()
    
    def create_xray_material(self) -> str:
        """Erstellt X-Ray Material mit Fresnel-basierter Transparenz"""
        mat = bpy.data.materials.new(name=f"{self.target_object}_XRay")
        mat.use_nodes = True
        mat.blend_method = 'BLEND'
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        mix_shader = nodes.new('ShaderNodeMixShader')
        mix_shader.location = (200, 0)
        
        emission = nodes.new('ShaderNodeEmission') 
        emission.location = (0, 100)
        emission.inputs['Strength'].default_value = 2.0
        
        transparent = nodes.new('ShaderNodeBsdfTransparent')
        transparent.location = (0, -100)
        
        fresnel = nodes.new('ShaderNodeFresnel')
        fresnel.location = (-200, 0)
        fresnel.inputs['IOR'].default_value = 1.8
        
        colorramp = nodes.new('ShaderNodeValToRGB')
        colorramp.location = (-150, 100)
        
        # Configure ColorRamp for bone/tissue differentiation
        ramp = colorramp.color_ramp
        ramp.elements[0].position = 0.3
        ramp.elements[0].color = (0.1, 0.1, 0.4, 0.8)  # Tissue - Dark blue
        ramp.elements[1].position = 0.8
        ramp.elements[1].color = (0.9, 0.9, 1.0, 1.0)  # Bone - Bright white
        
        # Link nodes
        links.new(fresnel.outputs['Fac'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], emission.inputs['Color'])
        links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        links.new(emission.outputs['Emission'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
        
        return mat.name
    
    def create_ultrasound_material(self) -> str:
        """Erstellt Ultraschall Material mit procedural noise"""
        mat = bpy.data.materials.new(name=f"{self.target_object}_Ultrasound")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (200, 0)
        emission.inputs['Strength'].default_value = 1.2
        
        mix_color = nodes.new('ShaderNodeMixRGB')
        mix_color.location = (0, 0)
        mix_color.blend_type = 'MULTIPLY'
        mix_color.inputs['Fac'].default_value = 0.7
        
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (-200, 100)
        noise.inputs['Scale'].default_value = 80.0
        noise.inputs['Detail'].default_value = 12.0
        noise.inputs['Roughness'].default_value = 0.7
        
        wave = nodes.new('ShaderNodeTexWave') 
        wave.location = (-200, -100)
        wave.inputs['Scale'].default_value = 25.0
        wave.inputs['Distortion'].default_value = 1.5
        wave.wave_type = 'BANDS'
        
        coord = nodes.new('ShaderNodeTexCoord')
        coord.location = (-400, 0)
        
        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-300, 0)
        
        # Ultrasound characteristic colors (grayscale with slight blue tint)
        colorramp = nodes.new('ShaderNodeValToRGB')
        colorramp.location = (50, 100)
        ramp = colorramp.color_ramp
        ramp.elements[0].position = 0.0
        ramp.elements[0].color = (0.05, 0.1, 0.15, 1.0)  # Dark blue-gray
        ramp.elements[1].position = 1.0
        ramp.elements[1].color = (0.8, 0.85, 0.9, 1.0)   # Light blue-white
        
        # Link nodes
        links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], noise.inputs['Vector'])
        links.new(mapping.outputs['Vector'], wave.inputs['Vector'])
        links.new(noise.outputs['Color'], mix_color.inputs['Color1'])
        links.new(wave.outputs['Color'], mix_color.inputs['Color2'])
        links.new(mix_color.outputs['Color'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        return mat.name
    
    def create_thermal_material(self) -> str:
        """Erstellt Wärmebild Material mit Temperatur-Gradient"""
        mat = bpy.data.materials.new(name=f"{self.target_object}_Thermal")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (100, 0)
        emission.inputs['Strength'].default_value = 1.5
        
        # Thermal color gradient
        colorramp = nodes.new('ShaderNodeValToRGB')
        colorramp.location = (-100, 0)
        
        # Configure thermal gradient (cold to hot)
        ramp = colorramp.color_ramp
        # Clear existing elements
        for elem in ramp.elements[2:]:
            ramp.elements.remove(elem)
        
        # Add thermal gradient points
        ramp.elements.new(0.2)
        ramp.elements.new(0.4) 
        ramp.elements.new(0.6)
        ramp.elements.new(0.8)
        
        # Set colors (cold to hot: blue -> cyan -> green -> yellow -> red)
        ramp.elements[0].position = 0.0
        ramp.elements[0].color = (0.0, 0.0, 0.5, 1.0)  # Cold - Dark Blue
        
        ramp.elements[1].position = 0.2
        ramp.elements[1].color = (0.0, 0.5, 1.0, 1.0)  # Cool - Cyan
        
        ramp.elements[2].position = 0.4
        ramp.elements[2].color = (0.0, 1.0, 0.5, 1.0)  # Normal - Green
        
        ramp.elements[3].position = 0.6
        ramp.elements[3].color = (1.0, 1.0, 0.0, 1.0)  # Warm - Yellow
        
        ramp.elements[4].position = 0.8
        ramp.elements[4].color = (1.0, 0.5, 0.0, 1.0)  # Hot - Orange
        
        ramp.elements[5].position = 1.0
        ramp.elements[5].color = (1.0, 0.0, 0.0, 1.0)  # Very Hot - Red
        
        # Temperature gradient based on geometry
        gradient = nodes.new('ShaderNodeTexGradient')
        gradient.location = (-300, 0)
        gradient.gradient_type = 'SPHERICAL'
        
        coord = nodes.new('ShaderNodeTexCoord')
        coord.location = (-500, 0)
        
        mapping = nodes.new('ShaderNodeMapping')
        mapping.location = (-400, 0)
        mapping.inputs['Scale'].default_value = (0.8, 0.8, 1.2)  # Scale for body heat distribution
        
        # Link nodes
        links.new(coord.outputs['Generated'], mapping.inputs['Vector'])
        links.new(mapping.outputs['Vector'], gradient.inputs['Vector'])
        links.new(gradient.outputs['Color'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        return mat.name
    
    def create_mri_material(self) -> str:
        """Erstellt MRI Material mit Grayscale Gewebe-Differenzierung"""
        mat = bpy.data.materials.new(name=f"{self.target_object}_MRI")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        nodes.clear()
        
        # Create nodes
        output = nodes.new('ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        emission = nodes.new('ShaderNodeEmission')
        emission.location = (100, 0)
        emission.inputs['Strength'].default_value = 1.0
        
        # MRI characteristic grayscale with tissue differentiation
        colorramp = nodes.new('ShaderNodeValToRGB')
        colorramp.location = (-100, 0)
        
        ramp = colorramp.color_ramp
        ramp.elements[0].position = 0.2
        ramp.elements[0].color = (0.1, 0.1, 0.1, 1.0)  # Bone - Dark
        ramp.elements[1].position = 0.8
        ramp.elements[1].color = (0.9, 0.9, 0.9, 1.0)  # Soft tissue - Light
        
        # Add intermediate tissue types
        ramp.elements.new(0.4)
        ramp.elements[1].position = 0.4
        ramp.elements[1].color = (0.3, 0.3, 0.3, 1.0)  # Dense tissue - Medium dark
        
        ramp.elements.new(0.6)
        ramp.elements[2].position = 0.6  
        ramp.elements[2].color = (0.6, 0.6, 0.6, 1.0)  # Organs - Medium light
        
        # Use vertex colors or procedural for tissue differentiation
        vertex_color = nodes.new('ShaderNodeVertexColor')
        vertex_color.location = (-300, 100)
        
        noise = nodes.new('ShaderNodeTexNoise')
        noise.location = (-300, -100)
        noise.inputs['Scale'].default_value = 15.0
        noise.inputs['Detail'].default_value = 3.0
        
        mix = nodes.new('ShaderNodeMixRGB')
        mix.location = (-200, 0)
        mix.blend_type = 'MIX'
        mix.inputs['Fac'].default_value = 0.3
        
        coord = nodes.new('ShaderNodeTexCoord')
        coord.location = (-400, -100)
        
        # Link nodes
        links.new(coord.outputs['Generated'], noise.inputs['Vector'])
        links.new(vertex_color.outputs['Color'], mix.inputs['Color1'])
        links.new(noise.outputs['Color'], mix.inputs['Color2'])
        links.new(mix.outputs['Color'], colorramp.inputs['Fac'])
        links.new(colorramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        return mat.name
    
    def create_normal_material(self) -> str:
        """Erstellt normales Fell-Material für Bello"""
        mat = bpy.data.materials.new(name=f"{self.target_object}_Normal")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Use default principled BSDF
        principled = nodes["Principled BSDF"]
        
        # Brown fur color
        principled.inputs['Base Color'].default_value = (0.6, 0.4, 0.2, 1.0)
        principled.inputs['Roughness'].default_value = 0.8
        principled.inputs['Subsurface'].default_value = 0.1  # Slight subsurface for fur
        principled.inputs['Subsurface Color'].default_value = (0.8, 0.6, 0.3, 1.0)
        
        return mat.name
    
    def apply_material_to_object(self, material_name: str):
        """Wendet Material auf das Target Object an"""
        if self.target_object in bpy.data.objects and material_name in bpy.data.materials:
            obj = bpy.data.objects[self.target_object]
            mat = bpy.data.materials[material_name]
            
            # Clear existing materials
            obj.data.materials.clear()
            
            # Add new material
            obj.data.materials.append(mat)
            
            return True
        return False
    
    def create_all_medical_materials(self) -> dict:
        """Erstellt alle medizinischen Materialien für Bello"""
        materials = {}
        
        try:
            materials['normal'] = self.create_normal_material()
            materials['xray'] = self.create_xray_material()
            materials['ultrasound'] = self.create_ultrasound_material()
            materials['thermal'] = self.create_thermal_material()
            materials['mri'] = self.create_mri_material()
            
            print(f"✅ Created {len(materials)} medical materials for {self.target_object}")
            return materials
            
        except Exception as e:
            print(f"❌ Error creating medical materials: {e}")
            return {}
    
    def export_material_variants(self, export_path="/app/exports") -> dict:
        """Exportiert Bello mit verschiedenen Material-Varianten"""
        import os
        
        materials = self.create_all_medical_materials()
        exports = {}
        
        for variant, material_name in materials.items():
            try:
                # Apply material
                self.apply_material_to_object(material_name)
                
                # Export GLB
                export_file = os.path.join(export_path, f"bello_{variant}.glb")
                os.makedirs(export_path, exist_ok=True)
                
                # Select Bello for export
                bpy.ops.object.select_all(action='DESELECT')
                if self.target_object in bpy.data.objects:
                    bpy.data.objects[self.target_object].select_set(True)
                    bpy.context.view_layer.objects.active = bpy.data.objects[self.target_object]
                
                    bpy.ops.export_scene.gltf(
                        filepath=export_file,
                        export_format='GLB',
                        export_selected=True,
                        export_draco_mesh_compression_enable=True,
                        export_draco_mesh_compression_level=4,
                        export_materials='EXPORT',
                        export_cameras=False,
                        export_lights=False
                    )
                    
                    exports[variant] = {
                        "filepath": export_file,
                        "exists": os.path.exists(export_file),
                        "size": os.path.getsize(export_file) if os.path.exists(export_file) else 0
                    }
                    
                    print(f"✅ Exported {variant}: {export_file}")
                
            except Exception as e:
                exports[variant] = {"error": str(e)}
                print(f"❌ Failed to export {variant}: {e}")
        
        return exports

# Main execution function for use in Blender
def main():
    """Main function to create all medical materials"""
    generator = MedicalShaderGenerator("Bello")
    
    # Create all materials
    materials = generator.create_all_medical_materials()
    
    # Export all variants
    exports = generator.export_material_variants()
    
    print("MEDICAL_MATERIALS_RESULT:", json.dumps({
        "materials_created": materials,
        "exports": exports,
        "success": len(materials) > 0
    }))

if __name__ == "__main__":
    main()