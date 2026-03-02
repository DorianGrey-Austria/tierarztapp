#!/usr/bin/env python3
"""
DIRECT 3D MODEL GENERATION - WORKING METHOD
===========================================
This script demonstrates the EXACT method that works for generating 3D models
directly through Blender MCP without manual intervention.

Usage: python3 direct_3d_generation.py "Golden Retriever dog, friendly pose"
"""

import json
import socket
import sys
from typing import Dict, Any

class Direct3DGenerator:
    """Direct 3D model generator using the working MCP approach"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
    
    def generate_model(self, prompt: str) -> Dict[str, Any]:
        """Generate a 3D model directly from text prompt"""
        
        print(f"🚀 Generating 3D model: '{prompt}'")
        
        # Analyze prompt for animal type
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['dog', 'retriever', 'labrador', 'shepherd']):
            animal_code = self._get_dog_code(prompt)
        elif any(word in prompt_lower for word in ['cat', 'kitten', 'feline']):
            animal_code = self._get_cat_code(prompt)
        elif any(word in prompt_lower for word in ['horse', 'pony']):
            animal_code = self._get_horse_code(prompt)
        else:
            animal_code = self._get_generic_animal_code(prompt)
        
        # Send to Blender via MCP
        command = {
            "type": "execute_code",
            "params": {
                "code": animal_code
            }
        }
        
        return self._send_command(command)
    
    def _send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to Blender MCP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.host, self.port))
            
            message = json.dumps(command).encode('utf-8')
            sock.send(message)
            
            response = sock.recv(16384).decode('utf-8')
            sock.close()
            
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}
    
    def _get_dog_code(self, prompt: str) -> str:
        """Generate code for dog model based on prompt"""
        
        # Determine breed characteristics from prompt
        if 'labrador' in prompt.lower() or 'retriever' in prompt.lower():
            body_scale = "(2.8, 1.4, 1.1)"
            head_scale = "(1.2, 1.0, 0.9)"
            ear_style = "floppy"
            color = "(0.85, 0.65, 0.35, 1.0)"  # Golden
        elif 'german' in prompt.lower() or 'shepherd' in prompt.lower():
            body_scale = "(2.6, 1.3, 1.2)"
            head_scale = "(1.4, 0.9, 0.9)"
            ear_style = "erect"
            color = "(0.4, 0.25, 0.15, 1.0)"  # Brown
        else:
            body_scale = "(2.5, 1.2, 1.0)"
            head_scale = "(1.3, 0.9, 0.9)"
            ear_style = "floppy"
            color = "(0.8, 0.6, 0.3, 1.0)"  # Default brown
        
        return f'''
import bpy
import json

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create dog body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = "AI_Dog_Body"
body.scale = {body_scale}
bpy.ops.object.transform_apply(scale=True)

# Add subdivision for organic look
modifier = body.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Create head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(3.2, 0, 1.2))
head = bpy.context.object
head.name = "AI_Dog_Head"
head.scale = {head_scale}
bpy.ops.object.transform_apply(scale=True)

modifier = head.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Create legs
leg_positions = [(1.8, 0.8, 0.4), (1.8, -0.8, 0.4), (-1.5, 0.8, 0.4), (-1.5, -0.8, 0.4)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.2, location=pos)
    leg = bpy.context.object
    leg.name = f"AI_Dog_Leg_{{i+1}}"
    modifier = leg.modifiers.new(name='Organic', type='SUBSURF')
    modifier.levels = 1

# Create ears based on breed
ear_positions = [(4.2, 0.6, 1.8), (4.2, -0.6, 1.8)]
for i, pos in enumerate(ear_positions):
    if "{ear_style}" == "floppy":
        bpy.ops.mesh.primitive_cube_add(size=0.8, location=pos)
        ear = bpy.context.object
        ear.scale = (0.8, 0.3, 1.2)
        ear.rotation_euler = (0.3, 0, -0.2)
    else:
        bpy.ops.mesh.primitive_cone_add(radius1=0.3, depth=1.0, location=pos)
        ear = bpy.context.object
        ear.rotation_euler = (0.1, 0, 0.1)
    
    ear.name = f"AI_Dog_Ear_{{i+1}}"
    modifier = ear.modifiers.new(name='Organic', type='SUBSURF')
    modifier.levels = 2

# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2.0, location=(-2.8, 0, 1.2))
tail = bpy.context.object
tail.name = "AI_Dog_Tail"
tail.rotation_euler = (0, 0.5, 0.2)  # Happy position

modifier = tail.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 1

# Create material
material = bpy.data.materials.new(name="AI_Dog_Fur")
material.use_nodes = True
bsdf = material.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = {color}
bsdf.inputs['Roughness'].default_value = 0.85

# Apply material to all parts
for obj in bpy.data.objects:
    if obj.name.startswith('AI_Dog_') and obj.type == 'MESH':
        obj.data.materials.append(material)

# Export model
export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/direct_generated_dog.glb"
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')

# Return result
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
result = {{
    "status": "success",
    "prompt": "{prompt}",
    "animal_type": "dog",
    "objects_created": len(mesh_objects),
    "export_path": export_path,
    "method": "direct_procedural_generation"
}}

print("GENERATION_RESULT:", json.dumps(result))
'''
    
    def _get_cat_code(self, prompt: str) -> str:
        """Generate code for cat model"""
        return '''
import bpy
import json

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create cat body (more compact than dog)
bpy.ops.mesh.primitive_cube_add(size=1.8, location=(0, 0, 0.6))
body = bpy.context.object
body.name = "AI_Cat_Body"
body.scale = (2.0, 1.0, 0.8)
bpy.ops.object.transform_apply(scale=True)

modifier = body.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Cat head (more triangular)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.6, location=(2.2, 0, 0.8))
head = bpy.context.object
head.name = "AI_Cat_Head"
head.scale = (1.1, 0.8, 0.8)
bpy.ops.object.transform_apply(scale=True)

modifier = head.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Cat legs (more delicate)
leg_positions = [(1.0, 0.6, 0.15), (1.0, -0.6, 0.15), (-0.8, 0.6, 0.15), (-0.8, -0.6, 0.15)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.6, location=pos)
    leg = bpy.context.object
    leg.name = f"AI_Cat_Leg_{i+1}"

# Pointed ears
ear_positions = [(2.8, 0.4, 1.2), (2.8, -0.4, 1.2)]
for i, pos in enumerate(ear_positions):
    bpy.ops.mesh.primitive_cone_add(radius1=0.2, depth=0.4, location=pos)
    ear = bpy.context.object
    ear.name = f"AI_Cat_Ear_{i+1}"

# Cat tail (long and flexible)
bpy.ops.mesh.primitive_cylinder_add(radius=0.08, depth=2.5, location=(-2.0, 0, 0.8))
tail = bpy.context.object
tail.name = "AI_Cat_Tail"
tail.rotation_euler = (0, 0.8, 0.2)

# Create material
material = bpy.data.materials.new(name="AI_Cat_Fur")
material.use_nodes = True
bsdf = material.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.6, 0.6, 0.6, 1.0)  # Gray
bsdf.inputs['Roughness'].default_value = 0.8

# Apply material
for obj in bpy.data.objects:
    if obj.name.startswith('AI_Cat_') and obj.type == 'MESH':
        obj.data.materials.append(material)

# Export
export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/direct_generated_cat.glb"
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')

mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
result = {
    "status": "success",
    "prompt": "''' + prompt + '''",
    "animal_type": "cat",
    "objects_created": len(mesh_objects),
    "export_path": export_path,
    "method": "direct_procedural_generation"
}

print("GENERATION_RESULT:", json.dumps(result))
'''
    
    def _get_generic_animal_code(self, prompt: str) -> str:
        """Generate code for generic animal"""
        return '''
import bpy
import json

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Generic quadruped body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = "AI_Animal_Body"
body.scale = (2.2, 1.1, 0.9)
bpy.ops.object.transform_apply(scale=True)

modifier = body.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Generic head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.7, location=(2.8, 0, 1.1))
head = bpy.context.object
head.name = "AI_Animal_Head"

modifier = head.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Four legs
leg_positions = [(1.4, 0.7, 0.4), (1.4, -0.7, 0.4), (-1.0, 0.7, 0.4), (-1.0, -0.7, 0.4)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.0, location=pos)
    leg = bpy.context.object
    leg.name = f"AI_Animal_Leg_{i+1}"

# Export
export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/direct_generated_animal.glb"
bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')

mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
result = {
    "status": "success", 
    "prompt": "''' + prompt + '''",
    "animal_type": "generic",
    "objects_created": len(mesh_objects),
    "export_path": export_path,
    "method": "direct_procedural_generation"
}

print("GENERATION_RESULT:", json.dumps(result))
'''
    
    def _get_horse_code(self, prompt: str) -> str:
        """Generate code for horse model (placeholder)"""
        return self._get_generic_animal_code(prompt).replace("generic", "horse")

def main():
    """Main function - generate model from command line or interactive"""
    
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = input("Enter model description (e.g., 'Golden Retriever dog, friendly pose'): ")
    
    print("=" * 60)
    print("🎯 DIRECT 3D MODEL GENERATION")
    print("=" * 60)
    
    generator = Direct3DGenerator()
    result = generator.generate_model(prompt)
    
    print("\\n" + "=" * 60)
    print("📊 GENERATION RESULTS")
    print("=" * 60)
    
    if result.get('status') == 'success':
        print("✅ SUCCESS! Model generated and exported.")
        
        # Try to extract result details
        result_str = result.get('result', {}).get('result', '')
        if 'GENERATION_RESULT:' in result_str:
            try:
                json_start = result_str.find('GENERATION_RESULT:') + len('GENERATION_RESULT:')
                json_data = json.loads(result_str[json_start:].strip())
                print(f"   📁 Export path: {json_data.get('export_path')}")
                print(f"   🎨 Objects created: {json_data.get('objects_created')}")
                print(f"   🐾 Animal type: {json_data.get('animal_type')}")
            except:
                pass
    else:
        print(f"❌ FAILED: {result}")
    
    print("\\n💡 This method works because:")
    print("   1. Uses execute_code (confirmed working command)")
    print("   2. Pure procedural generation in Blender")
    print("   3. No dependency on external AI services")
    print("   4. Direct export to GLB format")

if __name__ == "__main__":
    main()