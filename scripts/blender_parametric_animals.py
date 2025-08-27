#!/usr/bin/env python3
"""
BLENDER PARAMETRIC ANIMAL GENERATOR
=====================================
Advanced procedural animal generation with medical layers
Uses Geometry Nodes, PolyHaven textures, and full parametric control
Designed for VetScan Pro 3D Medical Education System
"""

import bpy
import bmesh
import math
import random
from mathutils import Vector, Matrix, noise
import requests
import json

class ParametricAnimalGenerator:
    """Advanced animal generator with medical visualization capabilities"""
    
    def __init__(self):
        self.setup_scene()
        self.polyhaven_materials = {}
        self.medical_layers = {}
        
    def setup_scene(self):
        """Clean scene and setup lighting"""
        # Clear existing objects
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Setup lighting for medical visualization
        self.add_medical_lighting()
        
        # Set viewport shading
        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                for space in area.spaces:
                    if space.type == 'VIEW_3D':
                        space.shading.type = 'MATERIAL'
                        space.shading.use_scene_lights = True
                        
    def add_medical_lighting(self):
        """Add professional medical visualization lighting"""
        # Key light (surgical lamp style)
        bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
        key_light = bpy.context.object
        key_light.name = "Medical_KeyLight"
        key_light.data.energy = 2
        key_light.data.color = (1.0, 0.98, 0.95)
        
        # Fill light (soft ambient)
        bpy.ops.object.light_add(type='AREA', location=(-5, -5, 8))
        fill_light = bpy.context.object
        fill_light.name = "Medical_FillLight"
        fill_light.data.energy = 50
        fill_light.data.size = 10
        fill_light.data.color = (0.9, 0.95, 1.0)
        
        # Rim light (for edge definition)
        bpy.ops.object.light_add(type='SPOT', location=(0, -8, 5))
        rim_light = bpy.context.object
        rim_light.name = "Medical_RimLight"
        rim_light.data.energy = 100
        rim_light.rotation_euler = (math.radians(60), 0, 0)
        
    def create_parametric_dog(self, 
                             breed="labrador",
                             size_factor=1.0,
                             age="adult",
                             medical_view="normal",
                             fur_length="medium",
                             pose="standing"):
        """Create a fully parametric dog with medical layers"""
        
        print(f"🐕 Creating parametric {breed} dog...")
        
        # Create base mesh with proper topology
        body = self.create_dog_base_mesh(breed, size_factor, age)
        
        # Add Geometry Nodes modifier for parametric control
        self.add_geometry_nodes_modifier(body, "dog", breed)
        
        # Apply realistic materials
        if medical_view == "normal":
            self.apply_realistic_fur(body, breed, fur_length)
        elif medical_view == "xray":
            self.apply_xray_material(body)
        elif medical_view == "organs":
            self.create_organ_system(body, "dog")
        elif medical_view == "skeleton":
            self.create_skeleton_system(body, "dog")
        elif medical_view == "thermal":
            self.apply_thermal_material(body)
        elif medical_view == "nervous":
            self.create_nervous_system(body, "dog")
            
        # Add pose if needed
        if pose != "standing":
            self.apply_pose(body, pose)
            
        return body
        
    def create_dog_base_mesh(self, breed, size_factor, age):
        """Create anatomically correct dog base mesh"""
        
        # Breed-specific proportions
        breed_params = {
            "labrador": {"body_length": 2.5, "body_height": 1.2, "head_size": 0.8},
            "german_shepherd": {"body_length": 2.7, "body_height": 1.3, "head_size": 0.85},
            "chihuahua": {"body_length": 1.5, "body_height": 0.6, "head_size": 0.6},
            "golden_retriever": {"body_length": 2.6, "body_height": 1.25, "head_size": 0.82},
        }
        
        params = breed_params.get(breed, breed_params["labrador"])
        
        # Age adjustments
        if age == "puppy":
            size_factor *= 0.4
            params["head_size"] *= 1.2  # Puppies have proportionally larger heads
        elif age == "senior":
            params["body_height"] *= 0.95  # Slightly lower stance
            
        # Create body using metaballs for organic shape
        bpy.ops.object.metaball_add(type='BALL', location=(0, 0, 0))
        mball = bpy.context.object
        mball.name = f"Dog_{breed}_Body"
        
        # Add body segments
        mb = mball.data
        
        # Main body
        body_element = mb.elements.new()
        body_element.co = (0, 0, 0)
        body_element.radius = params["body_height"] * size_factor
        body_element.stiffness = 1.0
        
        # Chest
        chest = mb.elements.new()
        chest.co = (params["body_length"] * 0.3 * size_factor, 0, 0.1)
        chest.radius = params["body_height"] * 1.1 * size_factor
        
        # Hindquarters
        hind = mb.elements.new()
        hind.co = (-params["body_length"] * 0.3 * size_factor, 0, 0)
        hind.radius = params["body_height"] * 0.9 * size_factor
        
        # Head
        head = mb.elements.new()
        head.co = (params["body_length"] * 0.5 * size_factor, 0, params["body_height"] * 0.3)
        head.radius = params["head_size"] * size_factor
        
        # Snout
        snout = mb.elements.new()
        snout.co = (params["body_length"] * 0.7 * size_factor, 0, params["body_height"] * 0.2)
        snout.radius = params["head_size"] * 0.5 * size_factor
        
        # Convert to mesh
        bpy.ops.object.convert(target='MESH')
        
        # Add legs using modifiers
        self.add_dog_legs(mball, params, size_factor)
        
        # Add ears and tail
        self.add_dog_features(mball, breed, size_factor)
        
        return mball
        
    def add_dog_legs(self, body, params, size_factor):
        """Add procedural legs to dog body"""
        
        leg_positions = [
            (params["body_length"] * 0.3, params["body_height"] * 0.4, -params["body_height"] * 0.8),
            (params["body_length"] * 0.3, -params["body_height"] * 0.4, -params["body_height"] * 0.8),
            (-params["body_length"] * 0.25, params["body_height"] * 0.4, -params["body_height"] * 0.8),
            (-params["body_length"] * 0.25, -params["body_height"] * 0.4, -params["body_height"] * 0.8),
        ]
        
        for i, pos in enumerate(leg_positions):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=0.15 * size_factor,
                depth=params["body_height"] * size_factor,
                location=(pos[0] * size_factor, pos[1] * size_factor, pos[2] * size_factor)
            )
            leg = bpy.context.object
            leg.name = f"Dog_Leg_{i+1}"
            
            # Add subdivision for smoothness
            modifier = leg.modifiers.new(name='Subdivision', type='SUBSURF')
            modifier.levels = 2
            
            # Join with body
            leg.select_set(True)
            body.select_set(True)
            bpy.context.view_layer.objects.active = body
            bpy.ops.object.join()
            
    def add_dog_features(self, body, breed, size_factor):
        """Add breed-specific features like ears and tail"""
        
        # Ears based on breed
        ear_types = {
            "labrador": "floppy",
            "german_shepherd": "erect", 
            "chihuahua": "erect_small",
            "golden_retriever": "floppy"
        }
        
        ear_type = ear_types.get(breed, "floppy")
        
        if ear_type == "floppy":
            # Create floppy ears
            for side in [1, -1]:
                bpy.ops.mesh.primitive_cube_add(
                    size=0.4 * size_factor,
                    location=(1.8 * size_factor, 0.3 * side * size_factor, 0.8 * size_factor)
                )
                ear = bpy.context.object
                ear.scale = (0.8, 0.3, 1.2)
                ear.rotation_euler = (0.3, 0, -0.2 * side)
                
                # Smooth it
                modifier = ear.modifiers.new(name='Subdivision', type='SUBSURF')
                modifier.levels = 2
                
                # Join with body
                ear.select_set(True)
                body.select_set(True)
                bpy.context.view_layer.objects.active = body
                bpy.ops.object.join()
                
        # Add tail
        bpy.ops.mesh.primitive_cylinder_add(
            radius=0.08 * size_factor,
            depth=1.5 * size_factor,
            location=(-1.5 * size_factor, 0, 0.3 * size_factor)
        )
        tail = bpy.context.object
        tail.rotation_euler = (0, 0.5, 0)
        
        # Add curve modifier for wagging
        modifier = tail.modifiers.new(name='Subdivision', type='SUBSURF')
        modifier.levels = 2
        
        tail.select_set(True)
        body.select_set(True)
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.join()
        
    def add_geometry_nodes_modifier(self, obj, animal_type, breed):
        """Add Geometry Nodes for parametric control"""
        
        # Add Geometry Nodes modifier
        modifier = obj.modifiers.new(name="Parametric_Control", type='NODES')
        
        # Create node group
        node_group = bpy.data.node_groups.new(name=f"{animal_type}_{breed}_params", type='GeometryNodeTree')
        modifier.node_group = node_group
        
        # Add input/output nodes
        input_node = node_group.nodes.new('NodeGroupInput')
        output_node = node_group.nodes.new('NodeGroupOutput')
        
        input_node.location = (-200, 0)
        output_node.location = (200, 0)
        
        # Add geometry socket
        node_group.interface.new_socket(name='Geometry', in_out='INPUT', socket_type='NodeSocketGeometry')
        node_group.interface.new_socket(name='Geometry', in_out='OUTPUT', socket_type='NodeSocketGeometry')
        
        # Add parameter controls
        node_group.interface.new_socket(name='Body Size', in_out='INPUT', socket_type='NodeSocketFloat')
        node_group.interface.new_socket(name='Leg Length', in_out='INPUT', socket_type='NodeSocketFloat')
        node_group.interface.new_socket(name='Head Size', in_out='INPUT', socket_type='NodeSocketFloat')
        node_group.interface.new_socket(name='Fur Density', in_out='INPUT', socket_type='NodeSocketFloat')
        
        # Connect basic pass-through for now
        node_group.links.new(input_node.outputs['Geometry'], output_node.inputs['Geometry'])
        
    def apply_realistic_fur(self, obj, breed, fur_length):
        """Apply realistic fur using particle system and shaders"""
        
        # Create fur material
        fur_mat = bpy.data.materials.new(name=f"Fur_{breed}")
        fur_mat.use_nodes = True
        
        nodes = fur_mat.node_tree.nodes
        links = fur_mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Add Principled Hair BSDF for realistic fur
        hair_bsdf = nodes.new(type='ShaderNodeBsdfHairPrincipled')
        hair_bsdf.location = (0, 0)
        
        # Set fur color based on breed
        breed_colors = {
            "labrador": (0.85, 0.65, 0.35, 1.0),  # Golden
            "german_shepherd": (0.3, 0.2, 0.1, 1.0),  # Dark brown
            "chihuahua": (0.7, 0.5, 0.3, 1.0),  # Light brown
            "golden_retriever": (0.9, 0.7, 0.4, 1.0),  # Golden
        }
        
        color = breed_colors.get(breed, (0.5, 0.4, 0.3, 1.0))
        hair_bsdf.inputs['Color'].default_value = color
        hair_bsdf.inputs['Roughness'].default_value = 0.3
        
        # Add output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        # Connect
        links.new(hair_bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        # Apply material
        obj.data.materials.append(fur_mat)
        
        # Add particle system for actual fur
        if fur_length != "none":
            self.add_fur_particles(obj, fur_length)
            
    def add_fur_particles(self, obj, fur_length):
        """Add realistic fur using particle system"""
        
        # Add particle system
        obj.modifiers.new(name="Fur", type='PARTICLE_SYSTEM')
        psys = obj.particle_systems[-1]
        
        # Configure particles
        psys.settings.type = 'HAIR'
        psys.settings.count = 10000 if fur_length == "long" else 5000
        psys.settings.hair_length = 0.1 if fur_length == "short" else 0.2 if fur_length == "medium" else 0.3
        psys.settings.child_type = 'INTERPOLATED'
        psys.settings.child_nbr = 10
        psys.settings.rendered_child_count = 100
        
        # Add randomness
        psys.settings.hair_step = 5
        psys.settings.brownian_factor = 0.03
        psys.settings.roughness_1 = 0.1
        
    def apply_xray_material(self, obj):
        """Apply X-ray visualization material"""
        
        xray_mat = bpy.data.materials.new(name="XRay_Material")
        xray_mat.use_nodes = True
        
        nodes = xray_mat.node_tree.nodes
        links = xray_mat.node_tree.links
        
        # Clear and create X-ray shader
        nodes.clear()
        
        # Fresnel for edge detection
        fresnel = nodes.new(type='ShaderNodeFresnel')
        fresnel.location = (-200, 0)
        fresnel.inputs['IOR'].default_value = 1.1
        
        # Emission for X-ray glow
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (0, 0)
        emission.inputs['Color'].default_value = (0.5, 1.0, 0.8, 1.0)
        emission.inputs['Strength'].default_value = 2
        
        # Mix with transparency
        mix_shader = nodes.new(type='ShaderNodeMixShader')
        mix_shader.location = (200, 0)
        
        transparent = nodes.new(type='ShaderNodeBsdfTransparent')
        transparent.location = (0, -200)
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (400, 0)
        
        # Connect nodes
        links.new(fresnel.outputs['Fac'], mix_shader.inputs['Fac'])
        links.new(transparent.outputs['BSDF'], mix_shader.inputs[1])
        links.new(emission.outputs['Emission'], mix_shader.inputs[2])
        links.new(mix_shader.outputs['Shader'], output.inputs['Surface'])
        
        # Apply material
        obj.data.materials.clear()
        obj.data.materials.append(xray_mat)
        
        # Set blend mode
        xray_mat.blend_method = 'BLEND'
        xray_mat.show_transparent_back = False
        
    def apply_thermal_material(self, obj):
        """Apply thermal imaging material"""
        
        thermal_mat = bpy.data.materials.new(name="Thermal_Material")
        thermal_mat.use_nodes = True
        
        nodes = thermal_mat.node_tree.nodes
        links = thermal_mat.node_tree.links
        
        nodes.clear()
        
        # ColorRamp for heat gradient
        color_ramp = nodes.new(type='ShaderNodeValToRGB')
        color_ramp.location = (-200, 0)
        
        # Setup thermal gradient (cold to hot)
        color_ramp.color_ramp.elements[0].color = (0, 0, 1, 1)  # Cold - Blue
        color_ramp.color_ramp.elements[1].color = (1, 0, 0, 1)  # Hot - Red
        
        # Add middle colors
        color_ramp.color_ramp.elements.new(0.33)
        color_ramp.color_ramp.elements[1].color = (0, 1, 1, 1)  # Cyan
        color_ramp.color_ramp.elements.new(0.66)
        color_ramp.color_ramp.elements[2].color = (1, 1, 0, 1)  # Yellow
        
        # Noise for variation
        noise = nodes.new(type='ShaderNodeTexNoise')
        noise.location = (-400, 0)
        noise.inputs['Scale'].default_value = 10
        
        # Emission
        emission = nodes.new(type='ShaderNodeEmission')
        emission.location = (0, 0)
        emission.inputs['Strength'].default_value = 1
        
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (200, 0)
        
        # Connect
        links.new(noise.outputs['Color'], color_ramp.inputs['Fac'])
        links.new(color_ramp.outputs['Color'], emission.inputs['Color'])
        links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        # Apply
        obj.data.materials.clear()
        obj.data.materials.append(thermal_mat)
        
    def create_skeleton_system(self, obj, animal_type):
        """Create anatomically correct skeleton"""
        
        print(f"   Creating skeleton for {animal_type}...")
        
        # Create armature
        bpy.ops.object.armature_add(location=(0, 0, 0))
        armature = bpy.context.object
        armature.name = f"{animal_type}_Skeleton"
        
        # Enter edit mode
        bpy.ops.object.mode_set(mode='EDIT')
        
        # Get armature data
        arm_data = armature.data
        edit_bones = arm_data.edit_bones
        
        # Create spine
        spine_positions = [
            (0, 0, 0),      # Base
            (0.5, 0, 0.2),  # Lower back
            (1, 0, 0.3),    # Mid back
            (1.5, 0, 0.4),  # Upper back
            (2, 0, 0.5),    # Neck base
            (2.3, 0, 0.6),  # Neck
            (2.6, 0, 0.7),  # Head
        ]
        
        prev_bone = None
        for i, pos in enumerate(spine_positions[:-1]):
            bone = edit_bones.new(f"Spine_{i+1}")
            bone.head = pos
            bone.tail = spine_positions[i+1]
            
            if prev_bone:
                bone.parent = prev_bone
            prev_bone = bone
            
        # Add ribs
        for i in range(1, 5):
            for side in [1, -1]:
                rib = edit_bones.new(f"Rib_{i}_{'+' if side > 0 else '-'}")
                rib.head = (0.5 + i * 0.3, 0, 0.3)
                rib.tail = (0.5 + i * 0.3, side * 0.5, 0.2)
                rib.parent = edit_bones[f"Spine_{i+1}"]
                
        # Add legs
        leg_bones = ["Femur", "Tibia", "Foot"]
        leg_positions = {
            "front_left": (1.5, 0.3, 0),
            "front_right": (1.5, -0.3, 0),
            "back_left": (0, 0.3, 0),
            "back_right": (0, -0.3, 0),
        }
        
        for leg_name, base_pos in leg_positions.items():
            prev_bone = None
            for i, bone_name in enumerate(leg_bones):
                bone = edit_bones.new(f"{leg_name}_{bone_name}")
                bone.head = (base_pos[0], base_pos[1], base_pos[2] - i * 0.4)
                bone.tail = (base_pos[0], base_pos[1], base_pos[2] - (i + 1) * 0.4)
                
                if prev_bone:
                    bone.parent = prev_bone
                elif "front" in leg_name:
                    bone.parent = edit_bones["Spine_4"]
                else:
                    bone.parent = edit_bones["Spine_1"]
                prev_bone = bone
                
        # Exit edit mode
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Apply bone material
        bone_mat = bpy.data.materials.new(name="Bone_Material")
        bone_mat.use_nodes = True
        nodes = bone_mat.node_tree.nodes
        bsdf = nodes["Principled BSDF"]
        bsdf.inputs['Base Color'].default_value = (0.9, 0.9, 0.8, 1.0)
        bsdf.inputs['Roughness'].default_value = 0.4
        bsdf.inputs['Subsurface Weight'].default_value = 0.3
        
        # Parent skeleton to body
        armature.parent = obj
        
        return armature
        
    def create_organ_system(self, obj, animal_type):
        """Create simplified organ system for medical visualization"""
        
        print(f"   Creating organs for {animal_type}...")
        
        organs = {
            "heart": {"pos": (1.2, 0, 0.2), "size": 0.15, "color": (0.8, 0.2, 0.2, 1.0)},
            "lungs": {"pos": (1.0, 0, 0.3), "size": 0.3, "color": (0.9, 0.5, 0.5, 1.0)},
            "liver": {"pos": (0.5, 0, 0), "size": 0.25, "color": (0.4, 0.2, 0.1, 1.0)},
            "stomach": {"pos": (0, 0, -0.1), "size": 0.2, "color": (0.9, 0.7, 0.6, 1.0)},
            "kidneys": {"pos": (-0.3, 0, 0), "size": 0.1, "color": (0.5, 0.2, 0.2, 1.0)},
        }
        
        organ_group = bpy.data.collections.new(f"{animal_type}_Organs")
        bpy.context.scene.collection.children.link(organ_group)
        
        for organ_name, params in organs.items():
            # Create organ mesh
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=params["size"],
                location=params["pos"]
            )
            organ = bpy.context.object
            organ.name = f"{animal_type}_{organ_name}"
            
            # Deform for more organic shape
            if organ_name == "heart":
                organ.scale = (1, 0.8, 1.2)
            elif organ_name == "lungs":
                organ.scale = (0.8, 1.2, 1)
            elif organ_name == "liver":
                organ.scale = (1.3, 0.7, 0.8)
                
            # Create material
            mat = bpy.data.materials.new(name=f"{organ_name}_Material")
            mat.use_nodes = True
            
            nodes = mat.node_tree.nodes
            bsdf = nodes["Principled BSDF"]
            bsdf.inputs['Base Color'].default_value = params["color"]
            bsdf.inputs['Subsurface Weight'].default_value = 0.8
            bsdf.inputs['Subsurface Color'].default_value = params["color"]
            bsdf.inputs['Roughness'].default_value = 0.3
            
            # Apply material
            organ.data.materials.append(mat)
            
            # Add to collection
            organ_group.objects.link(organ)
            bpy.context.scene.collection.objects.unlink(organ)
            
            # Parent to body
            organ.parent = obj
            
    def create_nervous_system(self, obj, animal_type):
        """Create nervous system visualization"""
        
        print(f"   Creating nervous system for {animal_type}...")
        
        # Create main nerve paths using curves
        bpy.ops.curve.primitive_bezier_curve_add(location=(0, 0, 0))
        spine_nerve = bpy.context.object
        spine_nerve.name = f"{animal_type}_SpinalCord"
        
        # Set curve properties
        spine_nerve.data.dimensions = '3D'
        spine_nerve.data.fill_mode = 'FULL'
        spine_nerve.data.bevel_depth = 0.02
        spine_nerve.data.bevel_resolution = 4
        
        # Create nerve material
        nerve_mat = bpy.data.materials.new(name="Nerve_Material")
        nerve_mat.use_nodes = True
        
        nodes = nerve_mat.node_tree.nodes
        emission = nodes.new(type='ShaderNodeEmission')
        emission.inputs['Color'].default_value = (0.5, 0.8, 1.0, 1.0)
        emission.inputs['Strength'].default_value = 3
        
        output = nodes["Material Output"]
        nerve_mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
        
        spine_nerve.data.materials.append(nerve_mat)
        spine_nerve.parent = obj
        
    def export_for_web(self, filepath=None, optimization_level="medium"):
        """Export optimized model for Three.js"""
        
        if not filepath:
            filepath = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/generated/"
            
        print(f"📦 Exporting for web...")
        
        # Select all mesh objects
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                obj.select_set(True)
                
        # Apply optimizations based on level
        if optimization_level in ["medium", "high"]:
            # Decimate for lower poly count
            bpy.ops.object.modifier_add(type='DECIMATE')
            bpy.context.object.modifiers["Decimate"].ratio = 0.5 if optimization_level == "medium" else 0.3
            
        # Export as GLB
        export_path = f"{filepath}/generated_animal.glb"
        bpy.ops.export_scene.gltf(
            filepath=export_path,
            export_format='GLB',
            use_selection=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
            export_apply_modifiers=True,
            export_animations=False,
            export_optimize_animation_size=True
        )
        
        print(f"✅ Exported to: {export_path}")
        return export_path

# Main execution
if __name__ == "__main__":
    generator = ParametricAnimalGenerator()
    
    # Create example dog with different medical views
    views = ["normal", "xray", "skeleton", "organs", "thermal", "nervous"]
    
    for view in views:
        print(f"\n{'='*50}")
        print(f"Creating dog with {view} view...")
        print('='*50)
        
        dog = generator.create_parametric_dog(
            breed="labrador",
            size_factor=1.0,
            age="adult",
            medical_view=view,
            fur_length="medium",
            pose="standing"
        )
        
        # Export
        generator.export_for_web(optimization_level="medium")
        
        print(f"✅ {view.capitalize()} view complete!")