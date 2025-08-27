#!/usr/bin/env python3
"""
Create a Rabbit using Hyper3D through Blender MCP - Corrected version
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
        sock.settimeout(60)  # Longer timeout for API calls
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
                if len(response_data) > 100000:  # Safety limit
                    break
                continue
        
        sock.close()
        
        if response_data:
            return json.loads(response_data.decode())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def create_rabbit_with_hyper3d():
    """Create a rabbit using the actual Hyper3D API"""
    
    print("🐰 Creating Rabbit with Hyper3D (Corrected)")
    print("="*50)
    
    # 1. Check Hyper3D status
    print("\n📊 Checking Hyper3D status...")
    response = send_blender_command({
        "type": "get_hyper3d_status",
        "params": {}
    })
    
    if response and response.get('status') == 'success':
        status = response.get('result', {})
        print(f"✅ Hyper3D Status: {status.get('message', 'Ready')}")
    
    # 2. Create Rodin job with CORRECT parameters
    print("\n🎨 Creating rabbit with Hyper3D Rodin...")
    print("   Using text prompt for 3D generation")
    
    response = send_blender_command({
        "type": "create_rodin_job",
        "params": {
            "text_prompt": "a cute white rabbit with long ears, sitting, 3D model",
            "images": []  # No reference images for pure text-to-3D
        }
    })
    
    if not response:
        print("❌ No response from Blender")
        return False
    
    print(f"Response: {json.dumps(response, indent=2)}")
    
    if response.get('status') != 'success':
        error_msg = response.get('message', 'Unknown error')
        print(f"❌ Failed to create Rodin job: {error_msg}")
        
        # If it's an API key issue, provide guidance
        if 'API' in error_msg or 'key' in error_msg.lower():
            print("\n📝 Note: Hyper3D requires an API key")
            print("   1. Sign up at https://hyperhuman.deemos.com")
            print("   2. Get your API key")
            print("   3. Add it in Blender: N-key → BlenderMCP → Hyper3D API Key")
        
        return False
    
    # Get job details
    result = response.get('result', {})
    job_uuid = result.get('uuid')
    subscription_key = result.get('subscription_key')
    
    if not job_uuid:
        print("❌ No job UUID returned")
        print(f"   Result: {result}")
        return False
    
    print(f"✅ Job created!")
    print(f"   UUID: {job_uuid}")
    print(f"   Key: {subscription_key[:10]}..." if subscription_key else "")
    
    # 3. Poll for completion
    print("\n⏳ Waiting for 3D generation to complete...")
    print("   This typically takes 30-60 seconds")
    
    max_attempts = 60  # 5 minutes max
    poll_interval = 5  # seconds
    
    for attempt in range(max_attempts):
        time.sleep(poll_interval)
        
        # Show progress
        elapsed = (attempt + 1) * poll_interval
        print(f"   [{elapsed:3d}s] Polling status...")
        
        response = send_blender_command({
            "type": "poll_rodin_job_status",
            "params": {
                "uuid": job_uuid
            }
        })
        
        if not response or response.get('status') != 'success':
            print(f"   ⚠️ Poll failed: {response}")
            continue
        
        job_status = response.get('result', {})
        status = job_status.get('status', 'Unknown')
        progress = job_status.get('progress', 0)
        
        print(f"   Status: {status} ({progress}%)")
        
        if status == 'Succeeded' or status == 'succeeded':
            print("✅ 3D generation complete!")
            
            # 4. Import the generated model
            print("\n📦 Importing generated rabbit into Blender...")
            
            response = send_blender_command({
                "type": "import_generated_asset",
                "params": {
                    "uuid": job_uuid,
                    "asset_name": "Hyper3D_Rabbit"
                }
            })
            
            if response and response.get('status') == 'success':
                print("✅ Rabbit imported successfully!")
                return True
            else:
                error = response.get('message', 'Unknown error') if response else 'No response'
                print(f"❌ Failed to import: {error}")
                
                # Try to get the URL directly
                model_url = job_status.get('output', {}).get('model')
                if model_url:
                    print(f"\n📝 Model URL: {model_url}")
                    print("   You can download and import manually")
            
            break
        
        elif status == 'Failed' or status == 'failed':
            error = job_status.get('error', 'Unknown error')
            print(f"❌ Generation failed: {error}")
            break
    
    else:
        print("❌ Timeout waiting for generation")
    
    return False

def export_generated_rabbit():
    """Export the Hyper3D rabbit"""
    
    print("\n📦 Exporting Hyper3D rabbit...")
    
    base_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel')
    output_dir = base_dir / 'assets' / 'models' / 'animals' / 'rabbit'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / 'rabbit_hyper3d_real.glb')
    
    export_code = f"""
import bpy

# Find the Hyper3D rabbit
rabbit_names = ["Hyper3D_Rabbit", "imported_mesh", "RodinGenerated"]
rabbit = None

for name in rabbit_names:
    if name in bpy.data.objects:
        rabbit = bpy.data.objects[name]
        break

# Also check for any newly imported meshes
if not rabbit:
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and 'import' in obj.name.lower():
            rabbit = obj
            break

if rabbit:
    bpy.ops.object.select_all(action='DESELECT')
    rabbit.select_set(True)
    bpy.context.view_layer.objects.active = rabbit
    
    # Export as GLB
    bpy.ops.export_scene.gltf(
        filepath=r'{output_path}',
        export_format='GLB',
        use_selection=True,
        export_apply=True
    )
    
    result = {{"success": True, "path": r'{output_path}', "object": rabbit.name}}
else:
    result = {{"success": False, "error": "No Hyper3D rabbit found in scene"}}

result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {"code": export_code}
    })
    
    if response and response.get('status') == 'success':
        result = response.get('result', {}).get('result', {})
        if result.get('success'):
            print(f"✅ Exported: {result.get('path')}")
            print(f"   Object: {result.get('object')}")
            return True
        else:
            print(f"❌ Export failed: {result.get('error')}")
    
    return False

if __name__ == "__main__":
    print("🐰 Hyper3D Rabbit Generation")
    print("="*50)
    
    success = create_rabbit_with_hyper3d()
    
    if success:
        # Try to export it
        export_success = export_generated_rabbit()
        
        if export_success:
            print("\n✅ Complete success!")
            print("   Rabbit generated by Hyper3D and exported")
        else:
            print("\n⚠️ Rabbit generated but export failed")
            print("   Export manually from Blender")
    else:
        print("\n❌ Hyper3D generation failed")
        print("\n📝 Alternatives:")
        print("1. Check API key in Blender settings")
        print("2. Use the procedural rabbit already created")
        print("3. Try with an image reference instead of text prompt")
    
    exit(0 if success else 1)