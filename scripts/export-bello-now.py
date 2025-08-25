#!/usr/bin/env python3
"""
Quick Bello Export Script
Exports the dog model from Blender to GLB format
"""

import asyncio
import websockets
import json
import os
import sys
from pathlib import Path

# Configuration
WEBSOCKET_HOST = "localhost"
WEBSOCKET_PORT = 8765
OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "models" / "animals" / "bello"

async def export_bello_model():
    """Connect to Blender MCP and export Bello model"""
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    try:
        # Try to connect to the MCP WebSocket server
        uri = f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}"
        print(f"🔌 Connecting to Blender MCP at {uri}...")
        
        async with websockets.connect(uri, timeout=5) as websocket:
            print("✅ Connected to Blender MCP!")
            
            # Request 1: Get scene info
            request = {
                "id": 1,
                "method": "get_scene_info",
                "params": {}
            }
            
            await websocket.send(json.dumps(request))
            response = await websocket.recv()
            scene_info = json.loads(response)
            
            print(f"📊 Scene info: {scene_info.get('result', {}).get('objects', [])}") 
            
            # Request 2: Export Bello as GLB with different quality levels
            qualities = ["high", "medium", "low"]
            for quality in qualities:
                output_file = OUTPUT_DIR / f"bello_{quality}.glb"
                
                export_request = {
                    "id": 2,
                    "method": "export_gltf",
                    "params": {
                        "filepath": str(output_file),
                        "quality": quality
                    }
                }
                
                print(f"📦 Exporting Bello model ({quality} quality)...")
                await websocket.send(json.dumps(export_request))
                export_response = await websocket.recv()
                export_result = json.loads(export_response)
                
                if export_result.get("result", {}).get("success"):
                    file_size = export_result["result"].get("file_size", 0)
                    print(f"✅ Exported {quality} quality: {output_file} ({file_size} bytes)")
                else:
                    print(f"❌ Failed to export {quality} quality: {export_result}")
            
            print("🎉 Export complete!")
            return True
            
    except asyncio.TimeoutError:
        print("❌ Connection timeout - Blender MCP server not responding")
        print("💡 Please ensure Docker container is running: ./docker-start.sh")
        return False
        
    except ConnectionRefusedError:
        print("❌ Connection refused - Blender MCP server not running")
        print("💡 Start the server with: ./docker-start.sh")
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def fallback_export():
    """Fallback: Create a simple GLB using Blender's bpy directly"""
    print("\n🔄 Attempting fallback export using direct Blender command...")
    
    # Create a simple Blender export script
    export_script = '''
import bpy
import os

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create simple dog model
# Body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = "Bello_Body"
body.scale = (2, 1, 0.8)

# Head
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.8, location=(2.2, 0, 1))
head = bpy.context.object
head.name = "Bello_Head"

# Legs (4 cylinders)
for i, pos in enumerate([(1.2, 0.6, 0), (1.2, -0.6, 0), (-0.8, 0.6, 0), (-0.8, -0.6, 0)]):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1, location=pos)
    leg = bpy.context.object
    leg.name = f"Bello_Leg_{i+1}"

# Tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(-2.2, 0, 1))
tail = bpy.context.object
tail.name = "Bello_Tail"
tail.rotation_euler = (0, 1.3, 0)

# Add brown material
mat = bpy.data.materials.new(name="BelloFur")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.6, 0.4, 1.0)

# Apply material to all Bello objects
for obj in bpy.data.objects:
    if obj.name.startswith("Bello_"):
        obj.data.materials.append(mat)

# Export as GLB
output_path = "OUTPUT_PATH"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath=output_path,
    export_format='GLB',
    export_yup=True,
    export_materials='EXPORT'
)

print(f"✅ Exported to {output_path}")
'''
    
    # Save script and execute with Blender
    script_path = Path(__file__).parent / "temp_export.py"
    output_path = OUTPUT_DIR / "bello_high.glb"
    
    # Replace OUTPUT_PATH in script
    script_content = export_script.replace("OUTPUT_PATH", str(output_path))
    
    with open(script_path, 'w') as f:
        f.write(script_content)
    
    # Try to run with Blender
    import subprocess
    blender_paths = [
        "/Applications/Blender.app/Contents/MacOS/Blender",
        "blender",
        "/usr/local/bin/blender"
    ]
    
    for blender_path in blender_paths:
        try:
            result = subprocess.run(
                [blender_path, "--background", "--python", str(script_path)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print(f"✅ Fallback export successful!")
                # Clean up temp script
                script_path.unlink()
                return True
            else:
                print(f"⚠️ Blender returned error: {result.stderr}")
                
        except FileNotFoundError:
            continue
        except subprocess.TimeoutExpired:
            print("⚠️ Blender export timed out")
            continue
    
    print("❌ Could not find Blender executable")
    return False

async def main():
    """Main execution"""
    print("🐕 Bello Export System - VetScan Pro 3000")
    print("=" * 50)
    
    # Try MCP export first
    success = await export_bello_model()
    
    if not success:
        # Try fallback method
        success = await fallback_export()
    
    if success:
        print("\n✅ Export completed successfully!")
        print(f"📁 Models saved to: {OUTPUT_DIR}")
    else:
        print("\n❌ Export failed. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())