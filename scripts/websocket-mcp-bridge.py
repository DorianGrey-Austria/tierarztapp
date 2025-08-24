#!/usr/bin/env python3
"""
WebSocket MCP Bridge Server für Blender-Claude Code Integration
Löst das Problem: subprocess Blender ≠ GUI Blender Instanz

Community-basierte Lösung:
Blender (GUI) ←→ WebSocket Server ←→ Claude Code (Cursor)
"""

import asyncio
import websockets
import json
import subprocess
import os
from pathlib import Path
import sys
from datetime import datetime

# Configuration
WEBSOCKET_HOST = "localhost"  
WEBSOCKET_PORT = 8765
BLENDER_PATH = "/Applications/Blender.app/Contents/MacOS/Blender"
PROJECT_ROOT = Path(__file__).parent.parent

class BlenderMCPBridge:
    def __init__(self):
        self.connected_clients = set()
        self.blender_process = None
        self.command_id = 0
        
    async def register_client(self, websocket):
        """Register new WebSocket client"""
        self.connected_clients.add(websocket)
        print(f"🔌 Client connected: {websocket.remote_address}")
        
    async def unregister_client(self, websocket):
        """Unregister WebSocket client"""
        self.connected_clients.discard(websocket)
        print(f"🔌 Client disconnected: {websocket.remote_address}")

    async def execute_blender_command(self, command_data):
        """Execute command in Blender via CLI and return results"""
        self.command_id += 1
        command_type = command_data.get("type", "unknown")
        
        try:
            if command_type == "get_scene_info":
                return await self._get_scene_info()
            elif command_type == "create_object":
                return await self._create_object(command_data)
            elif command_type == "execute_python":
                return await self._execute_python_script(command_data)
            elif command_type == "export_glb":
                return await self._export_glb(command_data)
            elif command_type == "take_screenshot":
                return await self._take_screenshot(command_data)
            else:
                return {
                    "success": False,
                    "error": f"Unknown command type: {command_type}",
                    "command_id": self.command_id
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command_id": self.command_id
            }

    async def _get_scene_info(self):
        """Get current Blender scene information"""
        script_content = '''
import bpy
import json

scene_info = {
    "objects": [],
    "active_object": None,
    "scene_name": bpy.context.scene.name
}

for obj in bpy.context.scene.objects:
    scene_info["objects"].append({
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "visible": obj.visible_get()
    })

if bpy.context.active_object:
    scene_info["active_object"] = bpy.context.active_object.name

print("SCENE_INFO_JSON:" + json.dumps(scene_info))
'''
        
        result = await self._run_blender_script(script_content)
        if result["success"]:
            # Extract JSON from stdout
            lines = result["stdout"].split("\n")
            for line in lines:
                if line.startswith("SCENE_INFO_JSON:"):
                    scene_data = json.loads(line[16:])
                    return {
                        "success": True,
                        "data": scene_data,
                        "command_id": self.command_id
                    }
        
        return result

    async def _create_object(self, command_data):
        """Create object in Blender"""
        object_type = command_data.get("object_type", "cube")
        location = command_data.get("location", [0, 0, 0])
        name = command_data.get("name", f"Object_{self.command_id}")
        
        script_content = f'''
import bpy

# Clear existing default objects if this is first run
if len(bpy.context.scene.objects) <= 3:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Create object based on type
if "{object_type}" == "cube":
    bpy.ops.mesh.primitive_cube_add(location={location})
elif "{object_type}" == "sphere":
    bpy.ops.mesh.primitive_uv_sphere_add(location={location})
elif "{object_type}" == "cylinder":
    bpy.ops.mesh.primitive_cylinder_add(location={location})
else:
    bpy.ops.mesh.primitive_cube_add(location={location})

# Name the object
if bpy.context.active_object:
    bpy.context.active_object.name = "{name}"
    print(f"Created object: {{bpy.context.active_object.name}}")
else:
    print("ERROR: No active object after creation")
'''
        
        return await self._run_blender_script(script_content)

    async def _execute_python_script(self, command_data):
        """Execute custom Python script in Blender"""
        script = command_data.get("script", "")
        if not script:
            return {
                "success": False,
                "error": "No script provided",
                "command_id": self.command_id
            }
            
        return await self._run_blender_script(script)

    async def _export_glb(self, command_data):
        """Export current scene as GLB"""
        output_path = command_data.get("output_path", f"export_{self.command_id}.glb")
        
        script_content = f'''
import bpy
import os

output_file = "{output_path}"
try:
    bpy.ops.export_scene.gltf(
        filepath=output_file,
        export_format='GLB',
        ui_tab='GENERAL',
        export_copyright="VetScan Pro 3000",
        export_image_format='JPEG',
        export_materials='EXPORT',
        export_colors=True,
        use_mesh_edges=False,
        use_mesh_vertices=False,
        export_cameras=False,
        export_extras=False,
        will_save_settings=False,
        filter_glob="*.glb"
    )
    
    if os.path.exists(output_file):
        print(f"SUCCESS: Exported to {{output_file}}")
        print(f"File size: {{os.path.getsize(output_file)}} bytes")
    else:
        print("ERROR: Export failed - file not created")
except Exception as e:
    print(f"ERROR: Export failed - {{str(e)}}")
'''
        
        result = await self._run_blender_script(script_content)
        if result["success"] and os.path.exists(output_path):
            result["data"] = {
                "output_path": output_path,
                "file_size": os.path.getsize(output_path)
            }
        
        return result

    async def _take_screenshot(self, command_data):
        """Take screenshot of Blender viewport"""
        output_path = command_data.get("output_path", f"screenshot_{self.command_id}.png")
        
        script_content = f'''
import bpy

# Set render settings for screenshot
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.filepath = "{output_path}"
bpy.context.scene.render.resolution_x = 1920
bpy.context.scene.render.resolution_y = 1080

# Render current frame
bpy.ops.render.render(write_still=True)
print(f"Screenshot saved to: {output_path}")
'''
        
        result = await self._run_blender_script(script_content)
        if result["success"] and os.path.exists(output_path):
            result["data"] = {
                "screenshot_path": output_path,
                "file_size": os.path.getsize(output_path)
            }
        
        return result

    async def _run_blender_script(self, script_content):
        """Execute Python script in Blender via CLI"""
        script_file = PROJECT_ROOT / "temp" / f"bridge_script_{self.command_id}.py"
        script_file.parent.mkdir(exist_ok=True)
        
        try:
            # Write script to file
            with open(script_file, 'w') as f:
                f.write(script_content)
            
            # Run Blender with script
            cmd = [
                BLENDER_PATH,
                "--background",
                "--factory-startup", 
                "--python", str(script_file)
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            result = {
                "success": process.returncode == 0,
                "stdout": stdout.decode('utf-8'),
                "stderr": stderr.decode('utf-8'),
                "return_code": process.returncode,
                "command_id": self.command_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Clean up temp file
            if script_file.exists():
                script_file.unlink()
                
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "command_id": self.command_id
            }

    async def handle_message(self, websocket, message):
        """Handle incoming WebSocket message"""
        try:
            data = json.loads(message)
            response = await self.execute_blender_command(data)
            await websocket.send(json.dumps(response))
            
        except json.JSONDecodeError:
            error_response = {
                "success": False,
                "error": "Invalid JSON format",
                "command_id": self.command_id
            }
            await websocket.send(json.dumps(error_response))
            
        except Exception as e:
            error_response = {
                "success": False,
                "error": str(e),
                "command_id": self.command_id
            }
            await websocket.send(json.dumps(error_response))

    async def websocket_handler(self, websocket, path):
        """Main WebSocket connection handler"""
        await self.register_client(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await self.unregister_client(websocket)

    async def start_server(self):
        """Start the WebSocket MCP Bridge Server"""
        print(f"🚀 Starting Blender MCP Bridge Server...")
        print(f"📡 WebSocket: ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        print(f"🎭 Blender Path: {BLENDER_PATH}")
        print(f"📁 Project Root: {PROJECT_ROOT}")
        print("=" * 60)
        
        # Create temp directory
        (PROJECT_ROOT / "temp").mkdir(exist_ok=True)
        
        server = await websockets.serve(
            self.websocket_handler,
            WEBSOCKET_HOST,
            WEBSOCKET_PORT
        )
        
        print(f"✅ Server running on ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}")
        print("💡 Ready for Claude Code connections!")
        print("🔄 Send JSON commands to control Blender...")
        
        await server.wait_closed()

# Example client code for testing
async def test_client():
    """Test client for the WebSocket MCP Bridge"""
    uri = f"ws://{WEBSOCKET_HOST}:{WEBSOCKET_PORT}"
    
    async with websockets.connect(uri) as websocket:
        # Test 1: Get scene info
        command = {"type": "get_scene_info"}
        await websocket.send(json.dumps(command))
        response = await websocket.recv()
        print(f"Scene Info: {json.loads(response)}")
        
        # Test 2: Create a cube
        command = {
            "type": "create_object",
            "object_type": "cube", 
            "location": [2, 0, 0],
            "name": "TestCube"
        }
        await websocket.send(json.dumps(command))
        response = await websocket.recv()
        print(f"Create Object: {json.loads(response)}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Run test client
        asyncio.run(test_client())
    else:
        # Run server
        bridge = BlenderMCPBridge()
        asyncio.run(bridge.start_server())