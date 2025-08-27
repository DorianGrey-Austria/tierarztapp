#!/usr/bin/env python3
"""
BLENDER MCP ANIMAL GENERATOR - MASTER SCRIPT
=============================================
Complete integration for realistic animal generation via Blender MCP
Combines procedural generation, PolyHaven textures, and medical layers
Execute via Blender MCP on port 9876
"""

import json
import socket
from typing import Dict, Any

class BlenderMCPAnimalClient:
    """Client to control Blender animal generation via MCP"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        
    def send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to Blender MCP and get response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.host, self.port))
            
            # Send command
            message = json.dumps(command).encode('utf-8')
            sock.send(message)
            
            # Receive response
            response = sock.recv(8192).decode('utf-8')
            sock.close()
            
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}
            
    def execute_code(self, code: str) -> Dict[str, Any]:
        """Execute Python code in Blender"""
        command = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        return self.send_command(command)
        
    def create_realistic_animal(self, 
                              animal_type: str = "dog",
                              breed: str = "labrador", 
                              medical_view: str = "normal",
                              use_polyhaven: bool = True) -> Dict[str, Any]:
        """Create a realistic animal with all features"""
        
        # Build the generation code
        code = f"""
import bpy
import sys
import os

# Add script path
script_path = '/Users/doriangrey/Desktop/coding/tierarztspiel/scripts'
if script_path not in sys.path:
    sys.path.append(script_path)

# Import our modules
from blender_parametric_animals import ParametricAnimalGenerator
from polyhaven_integration import PolyHavenTextureManager

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create generator
generator = ParametricAnimalGenerator()

# Generate animal
if '{animal_type}' == 'dog':
    animal = generator.create_parametric_dog(
        breed='{breed}',
        medical_view='{medical_view}',
        fur_length='medium',
        pose='standing'
    )
elif '{animal_type}' == 'cat':
    # Add cat generation
    animal = generator.create_parametric_cat(
        breed='persian',
        medical_view='{medical_view}'
    )
else:
    # Generic animal
    animal = generator.create_generic_animal(
        animal_type='{animal_type}',
        medical_view='{medical_view}'
    )

# Apply realistic textures if requested
if {use_polyhaven}:
    texture_manager = PolyHavenTextureManager()
    
    if '{medical_view}' == 'normal':
        # Only apply textures in normal view
        material_type = 'fur' if '{animal_type}' in ['dog', 'cat'] else 'skin'
        texture_manager.apply_realistic_animal_material(
            animal, 
            material_type=material_type,
            breed='{breed}' if '{animal_type}' == 'dog' else None
        )

# Export for web
export_path = generator.export_for_web(optimization_level='medium')

# Return info
result = {{
    'animal_type': '{animal_type}',
    'breed': '{breed}',
    'medical_view': '{medical_view}',
    'export_path': export_path,
    'vertex_count': sum(len(obj.data.vertices) for obj in bpy.data.objects if obj.type == 'MESH'),
    'face_count': sum(len(obj.data.polygons) for obj in bpy.data.objects if obj.type == 'MESH')
}}

print(json.dumps(result))
"""
        
        return self.execute_code(code)
        
    def batch_generate_animals(self, animals_config: list) -> list:
        """Generate multiple animals in batch"""
        results = []
        
        for config in animals_config:
            print(f"🐾 Generating {config.get('animal_type', 'unknown')}...")
            result = self.create_realistic_animal(**config)
            results.append(result)
            
        return results
        
    def create_animal_with_variations(self, animal_type: str) -> list:
        """Create an animal with all medical view variations"""
        
        views = ["normal", "xray", "skeleton", "organs", "thermal", "nervous"]
        results = []
        
        for view in views:
            print(f"  Creating {view} view...")
            result = self.create_realistic_animal(
                animal_type=animal_type,
                medical_view=view,
                use_polyhaven=(view == "normal")  # Only use textures for normal view
            )
            results.append(result)
            
        return results

def main():
    """Main execution - Generate all animals for VetScan Pro"""
    
    print("="*60)
    print("🏥 VETSCAN PRO - REALISTIC ANIMAL GENERATOR")
    print("="*60)
    
    # Initialize client
    client = BlenderMCPAnimalClient()
    
    # Test connection
    test_result = client.execute_code("import bpy; print('Blender MCP Connected!')")
    if "error" in test_result:
        print(f"❌ Connection failed: {test_result['error']}")
        print("\nMake sure:")
        print("1. Blender is running")
        print("2. Blender MCP addon is installed")
        print("3. Server is running on port 9876")
        return
        
    print("✅ Connected to Blender MCP")
    
    # Animal configurations
    animals = [
        {"animal_type": "dog", "breed": "labrador"},
        {"animal_type": "dog", "breed": "german_shepherd"},
        {"animal_type": "cat", "breed": "persian"},
        {"animal_type": "rabbit", "breed": "dutch"},
        {"animal_type": "horse", "breed": "arabian"},
        {"animal_type": "parrot", "breed": "macaw"},
        {"animal_type": "turtle", "breed": "red_eared"},
        {"animal_type": "snake", "breed": "python"},
        {"animal_type": "hamster", "breed": "syrian"},
        {"animal_type": "goldfish", "breed": "common"},
    ]
    
    # Generate each animal with all medical views
    for animal_config in animals:
        animal_type = animal_config["animal_type"]
        breed = animal_config.get("breed", "generic")
        
        print(f"\n{'='*40}")
        print(f"🐾 Generating {animal_type} ({breed})")
        print('='*40)
        
        # Create all variations
        results = client.create_animal_with_variations(animal_type)
        
        # Summary
        successful = sum(1 for r in results if "error" not in r)
        print(f"✅ Generated {successful}/{len(results)} variations")
        
    print("\n" + "="*60)
    print("🎉 GENERATION COMPLETE!")
    print("="*60)
    print("\nGenerated animals are ready for import into VetScan Pro")
    print("Export location: /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/generated/")

if __name__ == "__main__":
    main()