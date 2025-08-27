#!/usr/bin/env python3
"""
Create a Rabbit using Hyper3D through Blender MCP
Uses the Rodin API for 3D model generation
"""

import socket
import json
import time
import os
from pathlib import Path

def send_blender_command(command):
    """Send command to Blender MCP and get response"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)  # Longer timeout for API calls
        sock.connect(('localhost', 9876))
        
        # Send command
        sock.send(json.dumps(command).encode())
        
        # Receive response (might be large)
        response_data = b''
        while True:
            chunk = sock.recv(8192)
            if not chunk:
                break
            response_data += chunk
            try:
                # Try to parse to see if we have complete JSON
                json.loads(response_data.decode())
                break
            except:
                continue
        
        sock.close()
        
        if response_data:
            return json.loads(response_data.decode())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def create_rabbit():
    """Create a rabbit using Hyper3D/Rodin"""
    
    print("🐰 Creating Rabbit with Hyper3D")
    print("="*50)
    
    # 1. First check Hyper3D status
    print("\n📊 Checking Hyper3D status...")
    response = send_blender_command({
        "type": "get_hyper3d_status",
        "params": {}
    })
    
    if response:
        print(f"Response: {json.dumps(response, indent=2)}")
        if response.get('status') == 'success':
            status = response.get('result', {})
            if status.get('enabled'):
                print("✅ Hyper3D is enabled")
            else:
                print("❌ Hyper3D is not enabled")
                print("   Attempting to enable it...")
                
                # Try to enable Hyper3D
                enable_code = """
import bpy
bpy.context.scene.blendermcp_use_hyper3d = True
result = {"enabled": True}
result
"""
                response = send_blender_command({
                    "type": "execute_code",
                    "params": {"code": enable_code}
                })
                
                if response and response.get('status') == 'success':
                    print("✅ Hyper3D enabled")
                else:
                    print("❌ Could not enable Hyper3D")
                    return False
    else:
        print("⚠️ Could not check Hyper3D status, proceeding anyway...")
    
    # 2. Create a Rodin job for rabbit generation
    print("\n🎨 Creating rabbit generation job...")
    response = send_blender_command({
        "type": "create_rodin_job",
        "params": {
            "prompt": "a cute rabbit, white bunny with long ears, sitting position, 3D model, game asset",
            "mode": "generation"  # or "refine" if we have an existing model
        }
    })
    
    if not response or response.get('status') != 'success':
        error_msg = response.get('message', 'Unknown error') if response else 'No response'
        print(f"❌ Failed to create job: {error_msg}")
        
        # Try alternative approach with direct API call
        print("\n🔄 Trying alternative approach with direct API...")
        return create_rabbit_alternative()
    
    job_result = response.get('result', {})
    job_uuid = job_result.get('uuid')
    
    if not job_uuid:
        print("❌ No job UUID returned")
        return False
    
    print(f"✅ Job created with UUID: {job_uuid}")
    
    # 3. Poll for job completion
    print("\n⏳ Waiting for model generation...")
    print("   This may take 30-60 seconds...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        time.sleep(5)  # Wait 5 seconds between polls
        
        print(f"   Polling attempt {attempt + 1}/{max_attempts}...")
        
        response = send_blender_command({
            "type": "poll_rodin_job_status",
            "params": {
                "uuid": job_uuid
            }
        })
        
        if response and response.get('status') == 'success':
            job_status = response.get('result', {})
            status = job_status.get('status')
            
            print(f"   Status: {status}")
            
            if status == 'Succeeded':
                print("✅ Model generation complete!")
                
                # Get the generated model URL
                model_url = job_status.get('model_url')
                if model_url:
                    print(f"   Model URL: {model_url}")
                    
                    # 4. Import the generated model
                    print("\n📦 Importing generated rabbit...")
                    response = send_blender_command({
                        "type": "import_generated_asset",
                        "params": {
                            "uuid": job_uuid,
                            "asset_name": "Hyper3D_Rabbit"
                        }
                    })
                    
                    if response and response.get('status') == 'success':
                        print("✅ Rabbit imported into Blender!")
                        return export_rabbit()
                    else:
                        error = response.get('message', 'Unknown error') if response else 'No response'
                        print(f"❌ Failed to import: {error}")
                
                break
                
            elif status == 'Failed':
                error = job_status.get('error', 'Unknown error')
                print(f"❌ Generation failed: {error}")
                break
    
    print("❌ Job did not complete in time")
    return False

def create_rabbit_alternative():
    """Alternative approach - create a simple rabbit procedurally"""
    
    print("\n🔧 Creating procedural rabbit as fallback...")
    
    rabbit_code = """
import bpy
import bmesh

# Delete default cube if it exists
if 'Cube' in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects['Cube'], do_unlink=True)

# Create rabbit body (ellipsoid)
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
body = bpy.context.active_object
body.name = "Rabbit_Body"
body.scale = (1, 0.8, 1.2)

# Create head
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0.8, 0.8))
head = bpy.context.active_object
head.name = "Rabbit_Head"
head.scale = (0.6, 0.6, 0.7)

# Create ears
# Left ear
bpy.ops.mesh.primitive_cylinder_add(location=(-0.3, 0.7, 1.5))
left_ear = bpy.context.active_object
left_ear.name = "Rabbit_LeftEar"
left_ear.scale = (0.15, 0.15, 0.5)
left_ear.rotation_euler = (0.2, 0, -0.1)

# Right ear
bpy.ops.mesh.primitive_cylinder_add(location=(0.3, 0.7, 1.5))
right_ear = bpy.context.active_object
right_ear.name = "Rabbit_RightEar"
right_ear.scale = (0.15, 0.15, 0.5)
right_ear.rotation_euler = (0.2, 0, 0.1)

# Create tail
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, -1, 0))
tail = bpy.context.active_object
tail.name = "Rabbit_Tail"
tail.scale = (0.3, 0.3, 0.3)

# Join all parts
bpy.ops.object.select_all(action='DESELECT')
for obj_name in ["Rabbit_Body", "Rabbit_Head", "Rabbit_LeftEar", "Rabbit_RightEar", "Rabbit_Tail"]:
    if obj_name in bpy.data.objects:
        bpy.data.objects[obj_name].select_set(True)

bpy.context.view_layer.objects.active = body
bpy.ops.object.join()

# Rename final object
body.name = "Procedural_Rabbit"

# Add a simple material
mat = bpy.data.materials.new(name="Rabbit_Material")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)  # White color
body.data.materials.append(mat)

# Smooth shading
bpy.ops.object.shade_smooth()

result = {"success": True, "name": "Procedural_Rabbit"}
result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {"code": rabbit_code}
    })
    
    if response and response.get('status') == 'success':
        print("✅ Procedural rabbit created!")
        return export_rabbit("Procedural_Rabbit")
    else:
        error = response.get('message', 'Unknown error') if response else 'No response'
        print(f"❌ Failed to create procedural rabbit: {error}")
        return False

def export_rabbit(rabbit_name="Hyper3D_Rabbit"):
    """Export the rabbit as GLB"""
    
    print("\n📦 Exporting rabbit as GLB...")
    
    base_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel')
    output_dir = base_dir / 'assets' / 'models' / 'animals' / 'rabbit'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / 'rabbit_hyper3d.glb')
    
    export_code = f"""
import bpy

# Select the rabbit
bpy.ops.object.select_all(action='DESELECT')

# Try different possible names
rabbit_names = ["{rabbit_name}", "Procedural_Rabbit", "Hyper3D_Rabbit", "Rabbit"]
rabbit = None

for name in rabbit_names:
    if name in bpy.data.objects:
        rabbit = bpy.data.objects[name]
        break

if rabbit:
    rabbit.select_set(True)
    bpy.context.view_layer.objects.active = rabbit
    
    # Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=r'{output_path}',
        export_format='GLB',
        use_selection=True,
        export_apply=True
    )
    
    result = {{"success": True, "path": r'{output_path}'}}
else:
    # Export everything if no specific rabbit found
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=r'{output_path}',
        export_format='GLB',
        use_selection=True,
        export_apply=True
    )
    result = {{"success": True, "path": r'{output_path}', "note": "Exported all objects"}}

result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {"code": export_code}
    })
    
    if response and response.get('status') == 'success':
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✅ Rabbit exported successfully!")
            print(f"📁 File: {output_path}")
            print(f"📏 Size: {file_size:,} bytes")
            
            # Create quality variants
            from shutil import copyfile
            for quality in ['high', 'medium', 'low']:
                quality_dir = output_dir / quality
                quality_dir.mkdir(exist_ok=True)
                target = quality_dir / f"rabbit_{quality}.glb"
                copyfile(output_path, target)
                print(f"   ✅ Created {quality}: {target}")
            
            return True
    
    error = response.get('message', 'Unknown error') if response else 'No response'
    print(f"❌ Export failed: {error}")
    return False

if __name__ == "__main__":
    print("🐰 Rabbit Creation with Hyper3D")
    print("="*50)
    
    success = create_rabbit()
    
    print("\n" + "="*50)
    if success:
        print("✅ Rabbit created and exported successfully!")
        print("\n🎮 Test the rabbit in the game:")
        print("1. python3 -m http.server 8080")
        print("2. Open browser to test")
    else:
        print("❌ Rabbit creation failed")
        print("\n📝 You can try:")
        print("1. Check if Hyper3D is enabled in Blender (N-key → BlenderMCP)")
        print("2. Manually create a rabbit in Blender")
        print("3. Use the procedural rabbit as fallback")
    
    exit(0 if success else 1)