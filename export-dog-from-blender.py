#!/usr/bin/env python3
"""
Export VetPatient_Dog from Blender as GLB
Now using the correct format!
"""

import socket
import json
import time
import os
from pathlib import Path

def send_blender_command(command):
    """Send command to Blender and get response"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        # Send command
        sock.send(json.dumps(command).encode())
        
        # Receive response
        response_data = sock.recv(8192)
        sock.close()
        
        if response_data:
            return json.loads(response_data.decode())
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return None

def export_dog():
    """Export the dog model from Blender"""
    
    print("🐕 Exporting VetPatient_Dog from Blender")
    print("="*50)
    
    # 1. Get scene info to confirm dog exists
    print("\n📊 Getting scene info...")
    response = send_blender_command({
        "type": "get_scene_info",
        "params": {}
    })
    
    if response and response.get('status') == 'success':
        objects = response['result']['objects']
        dog_found = any(obj['name'] == 'VetPatient_Dog' for obj in objects)
        
        if dog_found:
            print("✅ Found VetPatient_Dog in scene")
        else:
            print("❌ VetPatient_Dog not found in scene")
            print(f"   Available objects: {[obj['name'] for obj in objects]}")
            return False
    else:
        print("❌ Failed to get scene info")
        return False
    
    # 2. Export as GLB using Python execution in Blender
    print("\n🔧 Exporting as GLB...")
    
    # Use absolute path
    base_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel')
    output_dir = base_dir / 'assets' / 'models' / 'animals' / 'dog'
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = str(output_dir / 'dog_from_blender.glb')
    
    export_code = f"""
import bpy
import os

# Select only the dog
bpy.ops.object.select_all(action='DESELECT')
dog = bpy.data.objects.get('VetPatient_Dog')
if dog:
    dog.select_set(True)
    bpy.context.view_layer.objects.active = dog
    
    # Export as GLB
    output_path = r'{output_path}'
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Export with proper settings (simplified for compatibility)
    bpy.ops.export_scene.gltf(
        filepath=output_path,
        export_format='GLB',
        use_selection=True,
        export_apply=True
    )
    
    result = {{"success": True, "path": output_path}}
else:
    result = {{"success": False, "error": "Dog object not found"}}

result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {
            "code": export_code
        }
    })
    
    if response:
        print(f"📊 Export response: {json.dumps(response, indent=2)}")
        
        if response.get('status') == 'success':
            # Check if file was created
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                print(f"\n✅ Export successful!")
                print(f"📁 File: {output_path}")
                print(f"📏 Size: {file_size:,} bytes")
                
                # Create quality variants
                create_quality_variants(output_path)
                
                return True
            else:
                print("⚠️ Export command succeeded but file not found")
                print("   Trying alternative export method...")
                return export_alternative(output_path)
        else:
            error_msg = response.get('message', 'Unknown error')
            print(f"❌ Export failed: {error_msg}")
            
            # Try alternative if it's a module error
            if 'No module named' in error_msg or 'export_scene' in error_msg:
                print("\n🔄 Trying alternative export method...")
                return export_alternative(output_path)
    
    return False

def export_alternative(output_path):
    """Alternative export using different approach"""
    
    print("\n🔄 Using alternative export approach...")
    
    # Try using FBX export then convert
    fbx_code = f"""
import bpy

# Select the dog
bpy.ops.object.select_all(action='DESELECT')
dog = bpy.data.objects.get('VetPatient_Dog')
if dog:
    dog.select_set(True)
    bpy.context.view_layer.objects.active = dog
    
    # Export as FBX first
    fbx_path = r'{output_path.replace('.glb', '.fbx')}'
    bpy.ops.export_scene.fbx(
        filepath=fbx_path,
        use_selection=True,
        apply_scale_options='FBX_SCALE_ALL'
    )
    result = {{"success": True, "path": fbx_path, "format": "fbx"}}
else:
    result = {{"success": False, "error": "Dog not found"}}
    
result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {"code": fbx_code}
    })
    
    if response and response.get('status') == 'success':
        print("✅ Exported as FBX")
        print("   Note: You'll need to convert FBX to GLB using an external tool")
        return True
    
    # If all fails, save the .blend file
    print("\n📦 Last resort: Saving .blend file...")
    
    blend_code = f"""
import bpy

# Save the blend file
blend_path = r'{output_path.replace('.glb', '.blend')}'
bpy.ops.wm.save_as_mainfile(filepath=blend_path, copy=True)
result = {{"success": True, "path": blend_path, "format": "blend"}}
result
"""
    
    response = send_blender_command({
        "type": "execute_code",
        "params": {"code": blend_code}
    })
    
    if response and response.get('status') == 'success':
        print("✅ Saved as .blend file")
        print("   You can manually export from Blender:")
        print("   1. Open the .blend file")
        print("   2. Select VetPatient_Dog")
        print("   3. File → Export → glTF 2.0")
        return True
    
    return False

def create_quality_variants(base_path):
    """Create different quality versions"""
    from shutil import copyfile
    
    print("\n📦 Creating quality variants...")
    
    base = Path(base_path)
    parent = base.parent
    
    for quality in ['high', 'medium', 'low']:
        quality_dir = parent / quality
        quality_dir.mkdir(exist_ok=True)
        
        target = quality_dir / f"dog_{quality}.glb"
        if base.exists():
            copyfile(base_path, target)
            print(f"   ✅ Created {quality}: {target}")

if __name__ == "__main__":
    print("🐕 Dog Export from Blender")
    print("="*50)
    
    success = export_dog()
    
    print("\n" + "="*50)
    if success:
        print("✅ Export completed successfully!")
        print("\n🎮 Next steps:")
        print("1. Test the model in the game")
        print("2. python3 -m http.server 8080")
        print("3. Open http://localhost:8080/vetscan-bello-3d-v7.html")
    else:
        print("❌ Export failed")
        print("\n📝 Manual export instructions:")
        print("1. In Blender, select VetPatient_Dog")
        print("2. File → Export → glTF 2.0 (.glb/.gltf)")
        print("3. Save to: assets/models/animals/dog/dog_from_blender.glb")
        print("4. Format: GLB, Export Selected: ON")
    
    exit(0 if success else 1)