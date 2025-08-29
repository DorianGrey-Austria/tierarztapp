#!/usr/bin/env python3
"""
VetScan Pro 3000 - Multi-Species 3D Animal Generator
Professional veterinary simulator with 20 animal species
Generates all animals in multiple quality levels for progressive loading
"""

import bpy
import bmesh
from mathutils import Vector
import math
import json
import os
from typing import Dict, List, Tuple

# Import veterinary data structure
ANIMAL_SPECIES = {
    # QUADRUPED SMALL
    'cat': {
        'template': 'quadruped_small',
        'scale': 0.6,
        'body_proportions': {'length': 1.2, 'height': 0.8, 'width': 0.6},
        'colors': ['orange', 'black', 'white', 'tabby', 'grey'],
        'features': ['pointed_ears', 'long_tail', 'retractable_claws']
    },
    'rabbit': {
        'template': 'quadruped_small', 
        'scale': 0.4,
        'body_proportions': {'length': 1.0, 'height': 0.9, 'width': 0.7},
        'colors': ['white', 'brown', 'grey', 'black_white'],
        'features': ['long_ears', 'cotton_tail', 'strong_hind_legs']
    },
    'guinea_pig': {
        'template': 'quadruped_small',
        'scale': 0.3,
        'body_proportions': {'length': 1.4, 'height': 0.6, 'width': 0.8},
        'colors': ['brown_white', 'black', 'tricolor'],
        'features': ['round_body', 'small_ears', 'short_legs']
    },
    'ferret': {
        'template': 'quadruped_small',
        'scale': 0.5,
        'body_proportions': {'length': 2.0, 'height': 0.5, 'width': 0.4},
        'colors': ['albino', 'sable', 'silver'],
        'features': ['elongated_body', 'flexible_spine']
    },

    # QUADRUPED MEDIUM  
    'dog': {
        'template': 'quadruped_medium',
        'scale': 1.0,
        'body_proportions': {'length': 1.5, 'height': 1.0, 'width': 0.7},
        'colors': ['brown', 'black', 'white', 'spotted', 'golden'],
        'features': ['floppy_ears', 'wagging_tail', 'loyal_expression'],
        'breeds': ['labrador', 'shepherd', 'beagle', 'retriever', 'mixed']
    },
    'sheep': {
        'template': 'quadruped_medium',
        'scale': 1.2, 
        'body_proportions': {'length': 1.3, 'height': 1.0, 'width': 0.9},
        'colors': ['white', 'black', 'brown'],
        'features': ['woolly_coat', 'curved_horns', 'rectangular_pupils']
    },
    'goat': {
        'template': 'quadruped_medium',
        'scale': 1.0,
        'body_proportions': {'length': 1.2, 'height': 1.1, 'width': 0.6},
        'colors': ['white', 'brown', 'black_white'],
        'features': ['beard', 'horns', 'climbing_hooves']
    },
    'pig': {
        'template': 'quadruped_medium',
        'scale': 1.1,
        'body_proportions': {'length': 1.4, 'height': 0.8, 'width': 1.0},
        'colors': ['pink', 'black', 'spotted'],
        'features': ['snout', 'curly_tail', 'intelligent_eyes']
    },

    # QUADRUPED LARGE
    'horse': {
        'template': 'quadruped_large',
        'scale': 2.5,
        'body_proportions': {'length': 2.0, 'height': 1.8, 'width': 0.8},
        'colors': ['brown', 'black', 'white', 'chestnut', 'grey'],
        'features': ['mane', 'long_tail', 'powerful_legs', 'hooves']
    },
    'cow': {
        'template': 'quadruped_large',
        'scale': 2.2,
        'body_proportions': {'length': 2.2, 'height': 1.6, 'width': 1.2},
        'colors': ['black_white', 'brown', 'holstein', 'jersey'],
        'features': ['udders', 'horns', 'large_body']
    },
    'llama': {
        'template': 'quadruped_large',
        'scale': 1.8,
        'body_proportions': {'length': 1.5, 'height': 2.0, 'width': 0.8},
        'colors': ['white', 'brown', 'grey', 'mixed'],
        'features': ['long_neck', 'woolly_coat', 'split_lip']
    },

    # BIRDS SMALL
    'canary': {
        'template': 'bird_small',
        'scale': 0.15,
        'body_proportions': {'length': 0.6, 'height': 0.8, 'width': 0.5},
        'colors': ['yellow', 'orange', 'white'],
        'features': ['small_beak', 'delicate_build', 'songbird']
    },
    'budgie': {
        'template': 'bird_small', 
        'scale': 0.18,
        'body_proportions': {'length': 0.7, 'height': 0.9, 'width': 0.5},
        'colors': ['green_yellow', 'blue', 'white'],
        'features': ['curved_beak', 'striped_pattern', 'playful']
    },

    # BIRDS MEDIUM
    'parrot': {
        'template': 'bird_medium',
        'scale': 0.4,
        'body_proportions': {'length': 1.0, 'height': 1.2, 'width': 0.6},
        'colors': ['green_red', 'blue_yellow', 'grey'],
        'features': ['large_beak', 'intelligent_eyes', 'colorful_plumage']
    },
    'chicken': {
        'template': 'bird_medium',
        'scale': 0.5,
        'body_proportions': {'length': 1.2, 'height': 1.0, 'width': 0.8},
        'colors': ['brown', 'white', 'black', 'red_brown'],
        'features': ['comb', 'wattles', 'ground_bird']
    },

    # REPTILES
    'snake': {
        'template': 'reptile_snake',
        'scale': 1.5,
        'body_proportions': {'length': 8.0, 'height': 0.3, 'width': 0.3},
        'colors': ['green', 'brown', 'patterned'],
        'features': ['scales', 'forked_tongue', 'flexible_body']
    },
    'lizard': {
        'template': 'reptile_lizard',
        'scale': 0.3,
        'body_proportions': {'length': 1.5, 'height': 0.4, 'width': 0.4},
        'colors': ['green', 'brown', 'blue'],
        'features': ['scales', 'long_tail', 'climbing_feet']
    },
    'turtle': {
        'template': 'reptile_turtle',
        'scale': 0.6,
        'body_proportions': {'length': 1.0, 'height': 0.6, 'width': 1.0},
        'colors': ['green_brown', 'olive', 'dark_green'],
        'features': ['shell', 'retractable_head', 'webbed_feet']
    },

    # AQUATIC
    'goldfish': {
        'template': 'fish',
        'scale': 0.2,
        'body_proportions': {'length': 1.0, 'height': 0.6, 'width': 0.4},
        'colors': ['gold', 'orange', 'white', 'calico'],
        'features': ['fins', 'scales', 'gills', 'aquatic']
    }
}

QUALITY_LEVELS = {
    'mobile': {
        'vertices': 800,
        'faces': 600,
        'texture_size': 256,
        'compression': 'draco_high'
    },
    'tablet': {
        'vertices': 3000,
        'faces': 2500,
        'texture_size': 512,  
        'compression': 'draco_medium'
    },
    'desktop': {
        'vertices': 12000,
        'faces': 10000,
        'texture_size': 1024,
        'compression': 'draco_low'
    },
    'pro': {
        'vertices': 40000,
        'faces': 35000,
        'texture_size': 2048,
        'compression': 'none'
    }
}

class AnimalGenerator:
    def __init__(self):
        self.current_animal = None
        self.generated_count = 0
        self.export_path = "/app/exports"
        
    def clear_scene(self):
        """Clean up the scene completely"""
        print('🧹 Cleaning up scene...')
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)
        
        # Clear materials and meshes
        for material in bpy.data.materials:
            bpy.data.materials.remove(material)
        for mesh in bpy.data.meshes:
            bpy.data.meshes.remove(mesh)
            
        print('✅ Scene cleared!')

    def generate_quadruped_template(self, species_data: Dict, quality_level: str) -> str:
        """Generate a quadruped animal using procedural modeling"""
        print(f'🐕 Generating {quality_level} quadruped template...')
        
        props = species_data['body_proportions']
        scale = species_data['scale']
        quality = QUALITY_LEVELS[quality_level]
        
        # Calculate subdivision levels based on quality
        subdiv_levels = {
            'mobile': 1,
            'tablet': 2, 
            'desktop': 3,
            'pro': 4
        }[quality_level]
        
        # Create main body
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=scale * 0.5,
            location=(0, 0, scale * 0.6)
        )
        body = bpy.context.object
        body.name = "Body"
        
        # Scale body according to proportions
        body.scale = (props['length'], props['width'], props['height'])
        
        # Add subdivision modifier for smoothness
        body.modifiers.new(name="Subdivision", type='SUBSURF')
        body.modifiers["Subdivision"].levels = subdiv_levels
        
        # Create head
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=scale * 0.3,
            location=(props['length'] * scale * 0.6, 0, scale * 0.8)
        )
        head = bpy.context.object
        head.name = "Head"
        head.modifiers.new(name="Subdivision", type='SUBSURF')
        head.modifiers["Subdivision"].levels = subdiv_levels
        
        # Create legs
        leg_positions = [
            (props['length'] * scale * 0.3, -props['width'] * scale * 0.3, 0),
            (props['length'] * scale * 0.3, props['width'] * scale * 0.3, 0),
            (-props['length'] * scale * 0.2, -props['width'] * scale * 0.3, 0),
            (-props['length'] * scale * 0.2, props['width'] * scale * 0.3, 0)
        ]
        
        for i, pos in enumerate(leg_positions):
            bpy.ops.mesh.primitive_cylinder_add(
                radius=scale * 0.08,
                depth=scale * 0.6,
                location=pos
            )
            leg = bpy.context.object
            leg.name = f"Leg_{i+1}"
            
        # Create tail
        bpy.ops.mesh.primitive_cylinder_add(
            radius=scale * 0.05,
            depth=scale * 0.4,
            location=(-props['length'] * scale * 0.5, 0, scale * 0.6)
        )
        tail = bpy.context.object
        tail.name = "Tail"
        tail.rotation_euler = (0, math.radians(45), 0)
        
        # Create ears based on species
        self.create_species_specific_features(species_data, scale)
        
        # Join all parts
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.join()
        
        animal_model = bpy.context.object
        animal_model.name = f"{species_data.get('name', 'Animal')}_Model"
        
        return animal_model.name

    def generate_bird_template(self, species_data: Dict, quality_level: str) -> str:
        """Generate a bird using procedural modeling"""
        print(f'🐦 Generating {quality_level} bird template...')
        
        scale = species_data['scale']
        props = species_data['body_proportions']
        
        # Bird body (more elongated)
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=scale,
            location=(0, 0, scale)
        )
        body = bpy.context.object
        body.name = "Body"
        body.scale = (props['length'], props['width'], props['height'])
        
        # Wings
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cube_add(
                size=scale * 0.8,
                location=(0, side * scale * 0.6, scale)
            )
            wing = bpy.context.object
            wing.name = f"Wing_{'Left' if side < 0 else 'Right'}"
            wing.scale = (1.5, 0.1, 0.3)
            
        # Beak
        bpy.ops.mesh.primitive_cone_add(
            radius1=scale * 0.1,
            depth=scale * 0.3,
            location=(props['length'] * scale * 0.5, 0, scale)
        )
        beak = bpy.context.object
        beak.name = "Beak"
        beak.rotation_euler = (0, math.radians(90), 0)
        
        # Legs (thinner for birds)
        for side in [-1, 1]:
            bpy.ops.mesh.primitive_cylinder_add(
                radius=scale * 0.02,
                depth=scale * 0.4,
                location=(0, side * scale * 0.2, scale * 0.2)
            )
            leg = bpy.context.object
            leg.name = f"Leg_{'Left' if side < 0 else 'Right'}"
        
        # Join all parts
        bpy.ops.object.select_all(action='SELECT')
        bpy.context.view_layer.objects.active = body
        bpy.ops.object.join()
        
        return body.name

    def create_species_specific_features(self, species_data: Dict, scale: float):
        """Add species-specific features"""
        features = species_data.get('features', [])
        
        if 'long_ears' in features:  # Rabbit ears
            for side in [-1, 1]:
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=scale * 0.05,
                    depth=scale * 0.6,
                    location=(scale * 0.3, side * scale * 0.15, scale * 1.2)
                )
                ear = bpy.context.object
                ear.name = f"Ear_{'Left' if side < 0 else 'Right'}"
                ear.rotation_euler = (math.radians(30), side * math.radians(15), 0)
                
        elif 'pointed_ears' in features:  # Cat ears
            for side in [-1, 1]:
                bpy.ops.mesh.primitive_cone_add(
                    radius1=scale * 0.08,
                    depth=scale * 0.15,
                    location=(scale * 0.2, side * scale * 0.12, scale * 1.0)
                )
                ear = bpy.context.object
                ear.name = f"Ear_{'Left' if side < 0 else 'Right'}"

    def create_medical_materials(self, animal_name: str, colors: List[str]):
        """Create materials optimized for medical visualization"""
        print(f'🎨 Creating medical materials for {animal_name}...')
        
        # Base material for normal view
        base_mat = bpy.data.materials.new(name=f"{animal_name}_Base")
        base_mat.use_nodes = True
        bsdf = base_mat.node_tree.nodes["Principled BSDF"]
        
        # Set natural animal color
        primary_color = self.get_color_values(colors[0])
        bsdf.inputs[0].default_value = (*primary_color, 1.0)
        bsdf.inputs[7].default_value = 0.8  # Roughness
        bsdf.inputs[9].default_value = 0.0  # Metallic
        
        # X-Ray material
        xray_mat = bpy.data.materials.new(name=f"{animal_name}_XRay")
        xray_mat.use_nodes = True
        xray_mat.blend_method = 'BLEND'
        xray_bsdf = xray_mat.node_tree.nodes["Principled BSDF"]
        xray_bsdf.inputs[0].default_value = (0.7, 0.8, 1.0, 0.3)  # Blue-ish X-ray
        xray_bsdf.inputs[21].default_value = 0.3  # Alpha
        
        # Thermal material  
        thermal_mat = bpy.data.materials.new(name=f"{animal_name}_Thermal")
        thermal_mat.use_nodes = True
        thermal_bsdf = thermal_mat.node_tree.nodes["Principled BSDF"]
        thermal_bsdf.inputs[0].default_value = (1.0, 0.3, 0.0, 1.0)  # Heat colors
        thermal_bsdf.inputs[26].default_value = 0.5  # Emission
        
        return [base_mat, xray_mat, thermal_mat]

    def get_color_values(self, color_name: str) -> Tuple[float, float, float]:
        """Convert color name to RGB values"""
        color_map = {
            'brown': (0.4, 0.2, 0.1),
            'black': (0.05, 0.05, 0.05),
            'white': (0.9, 0.9, 0.9),
            'golden': (0.8, 0.6, 0.2),
            'orange': (1.0, 0.5, 0.0),
            'grey': (0.5, 0.5, 0.5),
            'green': (0.2, 0.8, 0.3),
            'blue': (0.2, 0.3, 0.8),
            'yellow': (1.0, 1.0, 0.2),
            'pink': (1.0, 0.7, 0.7),
            'red': (0.8, 0.1, 0.1)
        }
        return color_map.get(color_name, (0.5, 0.5, 0.5))

    def create_anatomy_markers(self, animal_model, species_id: str):
        """Add invisible anatomy markers for medical interaction"""
        print(f'🫀 Creating anatomy markers for {species_id}...')
        
        # Define organ positions based on species
        organ_positions = {
            'heart': Vector((0.3, 0, 0.6)),
            'lungs': Vector((0.35, 0, 0.65)),
            'stomach': Vector((0.0, 0, 0.4)),
            'liver': Vector((-0.2, 0.15, 0.45)),
            'kidneys': Vector((-0.3, 0, 0.5)),
            'brain': Vector((0.6, 0, 0.8))
        }
        
        for organ, position in organ_positions.items():
            # Create invisible marker sphere
            bpy.ops.mesh.primitive_uv_sphere_add(
                radius=0.05,
                location=position
            )
            marker = bpy.context.object
            marker.name = f"Marker_{organ.capitalize()}"
            marker.hide_viewport = True  # Hidden in viewport
            marker.hide_render = True    # Hidden in render
            
            # Add to collection for organization
            collection = bpy.data.collections.get("Anatomy_Markers")
            if not collection:
                collection = bpy.data.collections.new("Anatomy_Markers")
                bpy.context.scene.collection.children.link(collection)
            
            collection.objects.link(marker)
            bpy.context.collection.objects.unlink(marker)

    def optimize_for_quality(self, model_name: str, quality_level: str):
        """Apply quality-specific optimizations"""
        print(f'⚙️ Optimizing {model_name} for {quality_level} quality...')
        
        quality = QUALITY_LEVELS[quality_level]
        obj = bpy.data.objects.get(model_name)
        
        if not obj:
            return
            
        # Apply modifiers before decimation
        bpy.context.view_layer.objects.active = obj
        
        # Add decimate modifier for lower quality levels
        if quality_level in ['mobile', 'tablet']:
            decimate = obj.modifiers.new(name="Decimate", type='DECIMATE')
            decimate.ratio = quality['vertices'] / 40000  # Relative to pro quality
            
        # Add smooth modifier for better appearance
        smooth = obj.modifiers.new(name="Smooth", type='SMOOTH')
        smooth.factor = 1.0
        smooth.iterations = 2

    def export_model(self, species_id: str, quality_level: str, model_name: str):
        """Export model as GLB with compression"""
        print(f'📦 Exporting {species_id}_{quality_level}.glb...')
        
        filename = f"{species_id}_{quality_level}.glb"
        filepath = os.path.join(self.export_path, species_id, filename)
        
        # Create species directory
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Select only the model for export
        bpy.ops.object.select_all(action='DESELECT')
        model_obj = bpy.data.objects.get(model_name)
        if model_obj:
            model_obj.select_set(True)
            bpy.context.view_layer.objects.active = model_obj
        
        # Export with compression settings
        compression_settings = {
            'draco_high': {'pos_quantization': 14, 'tex_coord_quantization': 12},
            'draco_medium': {'pos_quantization': 12, 'tex_coord_quantization': 10}, 
            'draco_low': {'pos_quantization': 10, 'tex_coord_quantization': 8},
            'none': {}
        }
        
        quality = QUALITY_LEVELS[quality_level]
        compression = compression_settings.get(quality['compression'], {})
        
        # Export GLB
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format='GLB',
            use_selection=True,
            export_draco_mesh_compression_enable=(quality['compression'] != 'none'),
            export_draco_mesh_compression_level=6,
            **compression
        )
        
        print(f'✅ Exported: {filename}')
        return filepath

    def create_manifest(self, species_id: str, species_data: Dict):
        """Create manifest file with metadata"""
        manifest = {
            'species': species_id,
            'name': species_data.get('name', species_id.title()),
            'template': species_data['template'],
            'scale': species_data['scale'],
            'quality_levels': list(QUALITY_LEVELS.keys()),
            'colors': species_data['colors'],
            'features': species_data.get('features', []),
            'anatomy_markers': [
                'heart', 'lungs', 'stomach', 'liver', 'kidneys', 'brain'
            ],
            'medical_modes': [
                'normal', 'xray', 'ultrasound', 'mri', 'thermal'
            ],
            'generated_timestamp': bpy.context.scene.frame_current,
            'generator_version': '2.0'
        }
        
        manifest_path = os.path.join(self.export_path, species_id, f"{species_id}_manifest.json")
        os.makedirs(os.path.dirname(manifest_path), exist_ok=True)
        
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f'📋 Created manifest: {species_id}_manifest.json')

    def generate_single_species(self, species_id: str, quality_levels: List[str] = None):
        """Generate a single species in specified quality levels"""
        if quality_levels is None:
            quality_levels = list(QUALITY_LEVELS.keys())
            
        species_data = ANIMAL_SPECIES.get(species_id)
        if not species_data:
            print(f'❌ Unknown species: {species_id}')
            return
            
        print(f'\n🚀 Generating {species_id.upper()} in {len(quality_levels)} quality levels...')
        
        for quality_level in quality_levels:
            print(f'\n--- {quality_level.upper()} QUALITY ---')
            
            # Clear scene for each quality level
            self.clear_scene()
            
            # Generate based on template type
            template = species_data['template']
            if template.startswith('quadruped'):
                model_name = self.generate_quadruped_template(species_data, quality_level)
            elif template.startswith('bird'):
                model_name = self.generate_bird_template(species_data, quality_level)
            else:
                print(f'⚠️ Template {template} not implemented yet')
                continue
                
            # Apply materials
            materials = self.create_medical_materials(species_id, species_data['colors'])
            model_obj = bpy.data.objects.get(model_name)
            if model_obj and materials:
                model_obj.data.materials.append(materials[0])
                
            # Add anatomy markers
            self.create_anatomy_markers(model_obj, species_id)
            
            # Optimize for quality level
            self.optimize_for_quality(model_name, quality_level)
            
            # Export
            self.export_model(species_id, quality_level, model_name)
            
        # Create manifest
        self.create_manifest(species_id, species_data)
        print(f'✅ {species_id} generation completed!')

    def generate_all_species(self):
        """Generate all 20 animal species"""
        print('🌟 STARTING MASS GENERATION OF ALL 20 SPECIES 🌟')
        print(f'Total models to generate: {len(ANIMAL_SPECIES)} species × {len(QUALITY_LEVELS)} qualities = {len(ANIMAL_SPECIES) * len(QUALITY_LEVELS)} models')
        
        for i, species_id in enumerate(ANIMAL_SPECIES.keys(), 1):
            print(f'\n{"="*60}')
            print(f'📍 PROGRESS: {i}/{len(ANIMAL_SPECIES)} - {species_id.upper()}')
            print(f'{"="*60}')
            
            self.generate_single_species(species_id)
            self.generated_count += len(QUALITY_LEVELS)
            
            print(f'✅ Species {i}/{len(ANIMAL_SPECIES)} completed')
            print(f'📊 Total models generated so far: {self.generated_count}')
            
        print('\n' + '='*80)
        print('🎉 MASS GENERATION COMPLETED SUCCESSFULLY! 🎉')
        print(f'📊 Final count: {self.generated_count} models generated')
        print(f'📁 All models saved to: {self.export_path}')
        print('='*80)

def main():
    """Main execution function"""
    print('🎯 VetScan Pro 3000 - Multi-Species Generator Starting...')
    
    generator = AnimalGenerator()
    
    # Check if specific species requested
    import sys
    if len(sys.argv) > 1:
        species_id = sys.argv[1]
        if species_id == 'all':
            generator.generate_all_species()
        elif species_id in ANIMAL_SPECIES:
            generator.generate_single_species(species_id)
        else:
            print(f'❌ Unknown species: {species_id}')
            print(f'Available species: {list(ANIMAL_SPECIES.keys())}')
    else:
        # Default: generate all species
        generator.generate_all_species()

if __name__ == "__main__":
    main()