#!/usr/bin/env python3
"""
Direct Hyper3D Test Script
Tests the generate_hyper3d_model_via_text functionality through MCP
"""

import json
import socket
from typing import Dict, Any

class DirectHyper3DTest:
    """Test client for Hyper3D generation via MCP"""
    
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        
    def send_command(self, command: Dict[str, Any]) -> Dict[str, Any]:
        """Send command to Blender MCP and get response"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)  # 30 second timeout
            sock.connect((self.host, self.port))
            
            # Send command
            message = json.dumps(command).encode('utf-8')
            sock.send(message)
            
            # Receive response
            response = sock.recv(16384).decode('utf-8')  # Larger buffer
            sock.close()
            
            return json.loads(response)
        except Exception as e:
            return {"error": str(e)}
    
    def test_hyper3d_generation(self, prompt: str) -> Dict[str, Any]:
        """Test the generate_hyper3d_model_via_text function"""
        
        print(f"🚀 Testing Hyper3D generation with prompt: '{prompt}'")
        
        # Method 1: Try direct hyper3d command
        command = {
            "type": "generate_hyper3d_model_via_text",
            "params": {
                "prompt": prompt
            }
        }
        
        result1 = self.send_command(command)
        print(f"✅ Method 1 (direct command): {result1}")
        
        # Method 2: Try execute_code with hyper3d function call
        code = f"""
import sys
import os

# Try to import any hyper3d modules
try:
    import hyper3d
    print("Found hyper3d module")
    result = hyper3d.generate_model_via_text("{prompt}")
    print(f"Hyper3D result: {{result}}")
except ImportError as e:
    print(f"No hyper3d module: {{e}}")

# Try pseudo-hyper3d approach
try:
    script_path = '/Users/doriangrey/Desktop/coding/tierarztspiel/scripts'
    if script_path not in sys.path:
        sys.path.append(script_path)
    
    from pseudo_hyper3d import generate_hyper3d_model_via_text_fallback
    generate_hyper3d_model_via_text_fallback("{prompt}")
    print("✅ Pseudo-Hyper3D generation successful!")
    
except Exception as e:
    print(f"❌ Pseudo-Hyper3D failed: {{e}}")

print("Model generation test complete")
"""
        
        command2 = {
            "type": "execute_code",
            "params": {
                "code": code
            }
        }
        
        result2 = self.send_command(command2)
        print(f"✅ Method 2 (execute_code): {result2}")
        
        return {"method1": result1, "method2": result2}
    
    def test_basic_model_creation(self):
        """Test basic model creation to ensure MCP is working"""
        
        print("\n🔧 Testing basic model creation...")
        
        code = """
import bpy

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a simple Golden Retriever-like model
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = "GoldenRetriever_Body"
body.scale = (2.8, 1.4, 1.1)

# Apply transformations
bpy.ops.object.transform_apply(scale=True)

# Add subdivision for organic look
modifier = body.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Create head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(3.2, 0, 1.2))
head = bpy.context.object
head.name = "GoldenRetriever_Head"
head.scale = (1.2, 1.0, 0.9)
bpy.ops.object.transform_apply(scale=True)

# Add head subdivision
modifier = head.modifiers.new(name='Organic', type='SUBSURF')
modifier.levels = 2

# Create legs
leg_positions = [(1.8, 0.8, 0.4), (1.8, -0.8, 0.4), (-1.5, 0.8, 0.4), (-1.5, -0.8, 0.4)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=1.2, location=pos)
    leg = bpy.context.object
    leg.name = f"GoldenRetriever_Leg_{i+1}"

# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=2.0, location=(-2.8, 0, 1.2))
tail = bpy.context.object
tail.name = "GoldenRetriever_Tail"
tail.rotation_euler = (0, 0.5, 0.2)  # Happy position

# Create material
material = bpy.data.materials.new(name="GoldenRetriever_Fur")
material.use_nodes = True
bsdf = material.node_tree.nodes['Principled BSDF']
bsdf.inputs['Base Color'].default_value = (0.85, 0.65, 0.35, 1.0)  # Golden color
bsdf.inputs['Roughness'].default_value = 0.85

# Apply material to all parts
for obj in bpy.data.objects:
    if obj.name.startswith('GoldenRetriever_') and obj.type == 'MESH':
        obj.data.materials.append(material)

print("✅ Golden Retriever model created successfully!")

# Get object count
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
print(f"Created {len(mesh_objects)} mesh objects")

# Try to export (optional)
try:
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/golden_retriever_test.glb"
    bpy.ops.export_scene.gltf(filepath=export_path, export_format='GLB')
    print(f"✅ Exported to: {export_path}")
except Exception as e:
    print(f"Export failed: {e}")
"""
        
        command = {
            "type": "execute_code", 
            "params": {
                "code": code
            }
        }
        
        result = self.send_command(command)
        print(f"Basic creation result: {result}")
        return result

def main():
    """Main test function"""
    
    print("=" * 60)
    print("🧪 HYPER3D DIRECT TEST")
    print("=" * 60)
    
    # Initialize test client
    tester = DirectHyper3DTest()
    
    # Test 1: Basic model creation (should work)
    basic_result = tester.test_basic_model_creation()
    
    # Test 2: Hyper3D generation (test what commands work)
    hyper3d_result = tester.test_hyper3d_generation(
        "Golden Retriever dog, friendly pose, detailed fur texture"
    )
    
    print("\n" + "=" * 60)
    print("🔍 TEST RESULTS SUMMARY")
    print("=" * 60)
    
    print(f"Basic Model Creation: {'✅ SUCCESS' if 'error' not in basic_result else '❌ FAILED'}")
    print(f"Method 1 (direct hyper3d): {'✅ SUCCESS' if 'error' not in hyper3d_result['method1'] else '❌ FAILED'}")
    print(f"Method 2 (execute_code): {'✅ SUCCESS' if 'error' not in hyper3d_result['method2'] else '❌ FAILED'}")
    
    # Detailed analysis
    if 'error' in hyper3d_result['method1']:
        print(f"\nMethod 1 Error: {hyper3d_result['method1']['error']}")
    
    if 'error' in hyper3d_result['method2']:
        print(f"Method 2 Error: {hyper3d_result['method2']['error']}")
    else:
        print(f"\nMethod 2 Output: {hyper3d_result['method2']}")

if __name__ == "__main__":
    main()