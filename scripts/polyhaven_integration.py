#!/usr/bin/env python3
"""
POLYHAVEN TEXTURE INTEGRATION
==============================
Automatically download and apply realistic textures from PolyHaven
Free, high-quality PBR materials for photorealistic animals
"""

import bpy
import requests
import json
import os
from pathlib import Path

class PolyHavenTextureManager:
    """Manager for PolyHaven textures and materials"""
    
    def __init__(self):
        self.api_base = "https://api.polyhaven.com"
        self.texture_cache = Path("/Users/doriangrey/Desktop/coding/tierarztspiel/assets/textures/polyhaven")
        self.texture_cache.mkdir(parents=True, exist_ok=True)
        
    def search_textures(self, category=None, search_term=None):
        """Search for textures on PolyHaven"""
        
        url = f"{self.api_base}/assets"
        params = {"type": "textures"}
        
        if category:
            params["categories"] = category
            
        response = requests.get(url, params=params)
        if response.status_code == 200:
            assets = response.json()
            
            # Filter by search term if provided
            if search_term:
                filtered = {}
                for asset_id, asset_data in assets.items():
                    if search_term.lower() in asset_data.get("name", "").lower():
                        filtered[asset_id] = asset_data
                return filtered
            return assets
        return {}
        
    def download_texture(self, texture_id, resolution="2k"):
        """Download a specific texture from PolyHaven"""
        
        print(f"📥 Downloading {texture_id} at {resolution} resolution...")
        
        # Get asset info
        info_url = f"{self.api_base}/info/{texture_id}"
        response = requests.get(info_url)
        
        if response.status_code != 200:
            print(f"❌ Failed to get info for {texture_id}")
            return None
            
        # Get file list
        files_url = f"{self.api_base}/files/{texture_id}"
        response = requests.get(files_url)
        
        if response.status_code != 200:
            print(f"❌ Failed to get files for {texture_id}")
            return None
            
        files = response.json()
        
        # Download texture maps
        texture_files = {}
        maps_to_download = ["diffuse", "normal", "roughness", "displacement"]
        
        for map_type in maps_to_download:
            if map_type in files.get("Textures", {}).get(resolution, {}):
                file_info = files["Textures"][resolution][map_type]
                
                # Get URL (handle different response formats)
                if isinstance(file_info, dict):
                    url = file_info.get("url", "")
                else:
                    url = file_info
                    
                if url:
                    # Download file
                    local_path = self.texture_cache / f"{texture_id}_{map_type}_{resolution}.jpg"
                    
                    if not local_path.exists():
                        print(f"   Downloading {map_type} map...")
                        r = requests.get(url)
                        if r.status_code == 200:
                            with open(local_path, 'wb') as f:
                                f.write(r.content)
                            texture_files[map_type] = str(local_path)
                    else:
                        print(f"   Using cached {map_type} map")
                        texture_files[map_type] = str(local_path)
                        
        return texture_files
        
    def create_pbr_material(self, name, texture_files):
        """Create a PBR material with downloaded textures"""
        
        mat = bpy.data.materials.new(name=name)
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        # Clear default nodes
        nodes.clear()
        
        # Create Principled BSDF
        bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
        bsdf.location = (0, 0)
        
        # Create output
        output = nodes.new(type='ShaderNodeOutputMaterial')
        output.location = (300, 0)
        
        # Connect BSDF to output
        links.new(bsdf.outputs['BSDF'], output.inputs['Surface'])
        
        x_offset = -800
        
        # Add texture nodes
        if "diffuse" in texture_files:
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.location = (x_offset, 300)
            tex_node.image = bpy.data.images.load(texture_files["diffuse"])
            tex_node.label = "Diffuse"
            links.new(tex_node.outputs['Color'], bsdf.inputs['Base Color'])
            
        if "normal" in texture_files:
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.location = (x_offset, 0)
            tex_node.image = bpy.data.images.load(texture_files["normal"])
            tex_node.image.colorspace_settings.name = 'Non-Color'
            tex_node.label = "Normal"
            
            # Add normal map node
            normal_map = nodes.new(type='ShaderNodeNormalMap')
            normal_map.location = (x_offset + 300, 0)
            links.new(tex_node.outputs['Color'], normal_map.inputs['Color'])
            links.new(normal_map.outputs['Normal'], bsdf.inputs['Normal'])
            
        if "roughness" in texture_files:
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.location = (x_offset, -300)
            tex_node.image = bpy.data.images.load(texture_files["roughness"])
            tex_node.image.colorspace_settings.name = 'Non-Color'
            tex_node.label = "Roughness"
            links.new(tex_node.outputs['Color'], bsdf.inputs['Roughness'])
            
        if "displacement" in texture_files:
            tex_node = nodes.new(type='ShaderNodeTexImage')
            tex_node.location = (x_offset, -600)
            tex_node.image = bpy.data.images.load(texture_files["displacement"])
            tex_node.image.colorspace_settings.name = 'Non-Color'
            tex_node.label = "Displacement"
            
            # Add displacement node
            displacement = nodes.new(type='ShaderNodeDisplacement')
            displacement.location = (100, -300)
            links.new(tex_node.outputs['Color'], displacement.inputs['Height'])
            links.new(displacement.outputs['Displacement'], output.inputs['Displacement'])
            
        return mat
        
    def get_animal_textures(self):
        """Get recommended textures for animal materials"""
        
        animal_textures = {
            "fur": [
                "animal_fur_001",
                "fabric_leather_02", 
                "carpet_001",
                "moss_001"  # Can work for fuzzy textures
            ],
            "skin": [
                "leather_red_02",
                "leather_white_02",
                "concrete_floor_02"  # Works for rough skin
            ],
            "scales": [
                "roof_tiles_14",
                "rock_boulder_cracked_001",
                "bark_brown_02"
            ],
            "feathers": [
                "fabric_pattern_07",
                "thatch_001"
            ]
        }
        
        return animal_textures
        
    def apply_realistic_animal_material(self, obj, material_type="fur", breed=None):
        """Apply realistic animal material using PolyHaven textures"""
        
        print(f"🎨 Applying {material_type} material to {obj.name}...")
        
        # Get appropriate textures
        texture_recommendations = self.get_animal_textures()
        texture_ids = texture_recommendations.get(material_type, ["fabric_leather_02"])
        
        # Try to download first available texture
        for texture_id in texture_ids:
            texture_files = self.download_texture(texture_id, resolution="2k")
            if texture_files:
                # Create PBR material
                mat = self.create_pbr_material(f"{material_type}_{texture_id}", texture_files)
                
                # Customize for animal type
                if material_type == "fur":
                    # Adjust for fur appearance
                    nodes = mat.node_tree.nodes
                    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
                    bsdf.inputs['Sheen Weight'].default_value = 0.5
                    bsdf.inputs['Roughness'].default_value = 0.8
                    
                    # Add color variation based on breed
                    if breed:
                        self.add_breed_color_variation(mat, breed)
                        
                elif material_type == "scales":
                    # Make it more metallic for scales
                    nodes = mat.node_tree.nodes
                    bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
                    bsdf.inputs['Metallic'].default_value = 0.3
                    bsdf.inputs['Roughness'].default_value = 0.4
                    
                # Apply to object
                obj.data.materials.clear()
                obj.data.materials.append(mat)
                
                print(f"✅ Applied {texture_id} texture")
                return mat
                
        print(f"⚠️ Could not download textures, using procedural material")
        return self.create_procedural_animal_material(obj, material_type)
        
    def add_breed_color_variation(self, mat, breed):
        """Add breed-specific color variation to material"""
        
        breed_colors = {
            "labrador": (0.85, 0.65, 0.35),  # Golden
            "german_shepherd": (0.3, 0.2, 0.1),  # Dark
            "dalmatian": (0.95, 0.95, 0.95),  # White
            "golden_retriever": (0.9, 0.7, 0.4),  # Golden
        }
        
        if breed in breed_colors:
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            
            # Find BSDF
            bsdf = next(n for n in nodes if n.type == 'BSDF_PRINCIPLED')
            
            # Add ColorRamp to modulate the texture
            color_ramp = nodes.new(type='ShaderNodeValToRGB')
            color_ramp.location = (-400, 300)
            
            # Set breed colors
            base_color = breed_colors[breed]
            color_ramp.color_ramp.elements[0].color = (*base_color, 1.0)
            color_ramp.color_ramp.elements[1].color = tuple(c * 1.2 for c in base_color) + (1.0,)
            
            # Mix with existing texture
            mix_rgb = nodes.new(type='ShaderNodeMix')
            mix_rgb.location = (-200, 300)
            mix_rgb.data_type = 'RGBA'
            mix_rgb.inputs['Factor'].default_value = 0.5
            
            # Reconnect
            for link in list(links):
                if link.to_socket == bsdf.inputs['Base Color']:
                    links.new(link.from_socket, mix_rgb.inputs['A'])
                    links.remove(link)
                    
            links.new(color_ramp.outputs['Color'], mix_rgb.inputs['B'])
            links.new(mix_rgb.outputs['Result'], bsdf.inputs['Base Color'])
            
    def create_procedural_animal_material(self, obj, material_type):
        """Create procedural material as fallback"""
        
        mat = bpy.data.materials.new(name=f"Procedural_{material_type}")
        mat.use_nodes = True
        
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links
        
        bsdf = nodes["Principled BSDF"]
        
        if material_type == "fur":
            # Procedural fur
            noise_tex = nodes.new(type='ShaderNodeTexNoise')
            noise_tex.location = (-300, 0)
            noise_tex.inputs['Scale'].default_value = 50
            noise_tex.inputs['Detail'].default_value = 10
            
            links.new(noise_tex.outputs['Fac'], bsdf.inputs['Roughness'])
            bsdf.inputs['Base Color'].default_value = (0.5, 0.4, 0.3, 1.0)
            bsdf.inputs['Sheen Weight'].default_value = 0.5
            
        elif material_type == "scales":
            # Procedural scales
            voronoi = nodes.new(type='ShaderNodeTexVoronoi')
            voronoi.location = (-300, 0)
            voronoi.inputs['Scale'].default_value = 100
            
            links.new(voronoi.outputs['Distance'], bsdf.inputs['Roughness'])
            links.new(voronoi.outputs['Color'], bsdf.inputs['Base Color'])
            bsdf.inputs['Metallic'].default_value = 0.3
            
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        return mat

# Example usage
if __name__ == "__main__":
    manager = PolyHavenTextureManager()
    
    # Search for animal-related textures
    print("🔍 Searching for fur textures...")
    textures = manager.search_textures(search_term="fabric")
    
    print(f"Found {len(textures)} textures")
    
    # Apply to selected object
    if bpy.context.selected_objects:
        obj = bpy.context.selected_objects[0]
        manager.apply_realistic_animal_material(obj, material_type="fur", breed="labrador")
    else:
        print("⚠️ No object selected!")