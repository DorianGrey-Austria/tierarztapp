#!/usr/bin/env python3
"""
VetScan Pro 3000 - Enhanced Blender MCP Server
Multi-Species 3D Asset Generation Pipeline
Professional veterinary simulator backend
"""

import asyncio
import websockets
import json
import subprocess
import os
import sys
from datetime import datetime
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/blender-mcp.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BlenderMCPServer:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.clients = set()
        self.generation_queue = asyncio.Queue()
        self.active_jobs = {}
        
        # Setup paths
        self.blender_path = os.environ.get('BLENDER_PATH', '/usr/bin/blender')
        self.project_root = os.environ.get('PROJECT_ROOT', '/app')
        self.export_path = f"{self.project_root}/exports"
        self.scripts_path = f"{self.project_root}/scripts"
        
        # Create necessary directories
        os.makedirs(self.export_path, exist_ok=True)
        os.makedirs(f"{self.project_root}/logs", exist_ok=True)
        
        logger.info(f"🚀 VetScan Pro MCP Server initializing...")
        logger.info(f"📁 Export path: {self.export_path}")
        logger.info(f"🔧 Blender path: {self.blender_path}")

    async def register_client(self, websocket):
        """Register new WebSocket client"""
        self.clients.add(websocket)
        client_info = f"{websocket.remote_address[0]}:{websocket.remote_address[1]}"
        logger.info(f"📡 Client connected: {client_info}")
        
        # Send welcome message with server capabilities
        welcome = {
            "type": "welcome",
            "server": "VetScan Pro Blender MCP",
            "version": "2.0",
            "capabilities": [
                "generate_single_animal",
                "generate_all_animals", 
                "get_generation_status",
                "list_available_species",
                "get_model_info",
                "health_check"
            ],
            "timestamp": datetime.now().isoformat()
        }
        await websocket.send(json.dumps(welcome))

    async def handle_message(self, websocket, message):
        """Handle incoming WebSocket messages"""
        try:
            data = json.loads(message)
            method = data.get('method', '')
            params = data.get('params', {})
            request_id = data.get('id', 'unknown')
            
            logger.info(f"📨 Received: {method} (ID: {request_id})")
            
            # Route to appropriate handler
            if method == 'generate_single_animal':
                response = await self.generate_single_animal(params)
            elif method == 'generate_all_animals':
                response = await self.generate_all_animals(params)
            elif method == 'health_check':
                response = await self.health_check()
            else:
                response = {
                    "error": f"Unknown method: {method}",
                    "available_methods": [
                        "generate_single_animal", "generate_all_animals", "health_check"
                    ]
                }
            
            # Send response
            response_msg = {
                "id": request_id,
                "result": response,
                "timestamp": datetime.now().isoformat()
            }
            
            await websocket.send(json.dumps(response_msg))
            
        except Exception as e:
            logger.error(f"❌ Error handling message: {str(e)}")

    async def generate_single_animal(self, params):
        """Generate a single animal species"""
        species_id = params.get('species_id', 'dog')
        
        logger.info(f"🐕 Starting generation: {species_id}")
        
        job_id = f"{species_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            # Run Blender script
            script_path = f"{self.scripts_path}/generate_all_animals.py"
            cmd = [
                self.blender_path,
                '--background',
                '--python', script_path,
                '--', species_id
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"✅ Generation completed: {species_id}")
                return {
                    "job_id": job_id,
                    "status": "completed",
                    "species_id": species_id
                }
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                logger.error(f"❌ Generation failed: {error_msg}")
                return {
                    "job_id": job_id,
                    "status": "failed",
                    "error": error_msg
                }
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def generate_all_animals(self, params):
        """Generate all 20 animal species"""
        logger.info(f"🌟 Starting mass generation")
        
        try:
            script_path = f"{self.scripts_path}/generate_all_animals.py"
            cmd = [
                self.blender_path,
                '--background', 
                '--python', script_path,
                '--', 'all'
            ]
            
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=self.project_root
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                logger.info(f"✅ Mass generation completed")
                return {"status": "completed", "message": "All animals generated"}
            else:
                error_msg = stderr.decode() if stderr else "Unknown error"
                return {"status": "failed", "error": error_msg}
                
        except Exception as e:
            return {"status": "failed", "error": str(e)}

    async def health_check(self):
        """Health check endpoint"""
        return {
            "status": "healthy",
            "server": "VetScan Pro Blender MCP",
            "version": "2.0",
            "timestamp": datetime.now().isoformat()
        }

    async def handle_client(self, websocket, path):
        """Handle individual WebSocket client"""
        self.clients.add(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except Exception as e:
            logger.error(f"❌ Client error: {str(e)}")
        finally:
            self.clients.discard(websocket)

    async def start_server(self):
        """Start the WebSocket server"""
        logger.info(f"🚀 Starting VetScan Pro Blender MCP Server on {self.host}:{self.port}")
        
        server = await websockets.serve(
            self.handle_client,
            self.host,
            self.port
        )
        
        return server

async def main():
    """Main server entry point"""
    server = BlenderMCPServer()
    websocket_server = await server.start_server()
    
    try:
        await websocket_server.wait_closed()
    except KeyboardInterrupt:
        logger.info("🛑 Server shutdown")
    finally:
        websocket_server.close()

if __name__ == "__main__":
    os.makedirs('/app/logs', exist_ok=True)
    asyncio.run(main())
- get_viewport_screenshot: Viewport Screenshot
- generate_bello_model: Bello 3D-Modell generieren
"""

import asyncio
import websockets
import json
import logging
import os
import sys
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional

# Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/blender-mcp.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('BlenderMCP')

class BlenderMCPServer:
    def __init__(self, host='0.0.0.0', port=8765):
        self.host = host
        self.port = port
        self.blender_process = None
        self.clients = set()
        
    async def start_blender_headless(self):
        """Startet Blender im Headless-Modus mit Python Server"""
        try:
            # Blender Python Script für interaktive Session
            blender_script = """
import bpy
import json
import sys
import os
from mathutils import Vector

# Cleanup default scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Add basic lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
light = bpy.context.object
light.data.energy = 3

# Add camera
bpy.ops.object.camera_add(location=(7, -7, 5))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0.785)

# Create Bello base model (simple dog shape)
def create_bello_base():
    # Add cube for body
    bpy.ops.mesh.primitive_cube_add(scale=(2, 1, 0.8), location=(0, 0, 0.8))
    body = bpy.context.object
    body.name = "Bello_Body"
    
    # Add cylinder for head
    bpy.ops.mesh.primitive_uv_sphere_add(scale=(0.8, 0.8, 0.8), location=(2.2, 0, 0.8))
    head = bpy.context.object
    head.name = "Bello_Head"
    
    # Add cylinders for legs
    locations = [(1.2, 0.6, 0), (1.2, -0.6, 0), (-0.8, 0.6, 0), (-0.8, -0.6, 0)]
    for i, loc in enumerate(locations):
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.8, location=loc)
        leg = bpy.context.object
        leg.name = f"Bello_Leg_{i+1}"
    
    # Add tail
    bpy.ops.mesh.primitive_cylinder_add(radius=0.1, depth=1.5, location=(-2.2, 0, 0.8))
    tail = bpy.context.object
    tail.name = "Bello_Tail"
    tail.rotation_euler = (0, 1.3, 0)
    
    # Join all parts
    bpy.ops.object.select_all(action='DESELECT')
    for obj_name in ["Bello_Body", "Bello_Head", "Bello_Leg_1", "Bello_Leg_2", 
                     "Bello_Leg_3", "Bello_Leg_4", "Bello_Tail"]:
        if obj_name in bpy.data.objects:
            bpy.data.objects[obj_name].select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects["Bello_Body"]
    bpy.ops.object.join()
    
    # Rename final object
    bello = bpy.context.object
    bello.name = "Bello"
    
    # Add basic material
    mat = bpy.data.materials.new(name="Bello_Fur")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.6, 0.3, 1.0)  # Brown fur
    bello.data.materials.append(mat)
    
    print("✅ Bello base model created successfully")
    return bello

# Create Bello if not exists
if "Bello" not in bpy.data.objects:
    create_bello_base()

print("🎯 Blender MCP Server ready - Bello model loaded")
print("📊 Scene objects:", [obj.name for obj in bpy.data.objects])

# Keep Blender running
import time
while True:
    time.sleep(1)
"""
            
            # Start Blender with our script
            cmd = [
                'blender', 
                '--background',
                '--python-expr', blender_script
            ]
            
            logger.info(f"Starting Blender: {' '.join(cmd)}")
            self.blender_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env={**os.environ, 'DISPLAY': ':99'}
            )
            
            # Wait a bit for Blender to start
            await asyncio.sleep(5)
            logger.info("✅ Blender started successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start Blender: {e}")
            raise
    
    def execute_blender_python(self, code: str) -> Dict[str, Any]:
        """Execute Python code in Blender and return result"""
        try:
            # Create temp script file
            script_file = f"/app/temp/exec_{hash(code) % 10000}.py"
            with open(script_file, 'w') as f:
                f.write(f"""
import bpy
import json
import sys

try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
    result = "success"
except Exception as e:
    result = str(e)
    print(f"Error: {{e}}")

print(f"Result: {{result}}")
""")
            
            # Execute in Blender
            result = subprocess.run([
                'blender', '--background', 
                '--python', script_file
            ], capture_output=True, text=True, timeout=30)
            
            # Clean up
            os.remove(script_file)
            
            return {
                "success": result.returncode == 0,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_scene_info(self) -> Dict[str, Any]:
        """Get current scene information"""
        code = """
import bpy
scene_info = {
    'objects': [obj.name for obj in bpy.data.objects],
    'meshes': [mesh.name for mesh in bpy.data.meshes],
    'materials': [mat.name for mat in bpy.data.materials],
    'cameras': [cam.name for cam in bpy.data.cameras],
    'lights': [light.name for light in bpy.data.lights]
}
print("SCENE_INFO:", json.dumps(scene_info))
"""
        result = self.execute_blender_python(code)
        
        # Extract scene info from output
        try:
            for line in result['output'].split('\n'):
                if line.startswith('SCENE_INFO:'):
                    return json.loads(line[11:])
        except:
            pass
            
        return {"objects": [], "error": "Could not retrieve scene info"}
    
    def get_object_info(self, object_name: str) -> Dict[str, Any]:
        """Get detailed information about specific object"""
        code = f"""
import bpy
import bmesh

obj_info = {{"exists": False}}

if "{object_name}" in bpy.data.objects:
    obj = bpy.data.objects["{object_name}"]
    obj_info = {{
        "exists": True,
        "name": obj.name,
        "type": obj.type,
        "location": list(obj.location),
        "rotation": list(obj.rotation_euler),
        "scale": list(obj.scale)
    }}
    
    if obj.type == 'MESH' and obj.data:
        # Get mesh statistics
        mesh = obj.data
        obj_info.update({{
            "vertices": len(mesh.vertices),
            "edges": len(mesh.edges), 
            "faces": len(mesh.polygons),
            "polygon_count": len(mesh.polygons),
            "materials": [mat.name for mat in mesh.materials]
        }})

print("OBJECT_INFO:", json.dumps(obj_info))
"""
        result = self.execute_blender_python(code)
        
        # Extract object info from output
        try:
            for line in result['output'].split('\n'):
                if line.startswith('OBJECT_INFO:'):
                    return json.loads(line[12:])
        except:
            pass
            
        return {"exists": False, "error": f"Object '{object_name}' not found"}
    
    def export_gltf(self, filepath: str, selected_only: bool = True, quality: str = "high") -> Dict[str, Any]:
        """Export scene or selection to GLB format"""
        
        # Quality settings
        quality_settings = {
            "high": {"draco_level": 6, "texture_size": 2048},
            "medium": {"draco_level": 4, "texture_size": 1024}, 
            "low": {"draco_level": 2, "texture_size": 512}
        }
        
        settings = quality_settings.get(quality, quality_settings["high"])
        
        code = f"""
import bpy
import os

# Export settings
export_path = "{filepath}"
os.makedirs(os.path.dirname(export_path), exist_ok=True)

try:
    # Select objects for export
    if {selected_only} and "Bello" in bpy.data.objects:
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["Bello"].select_set(True)
        bpy.context.view_layer.objects.active = bpy.data.objects["Bello"]
    
    # Export GLB
    bpy.ops.export_scene.gltf(
        filepath=export_path,
        export_format='GLB',
        export_selected={selected_only},
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level={settings['draco_level']},
        export_materials='EXPORT',
        export_animations=True,
        export_cameras=False,
        export_lights=False
    )
    
    file_size = os.path.getsize(export_path) if os.path.exists(export_path) else 0
    print("EXPORT_RESULT:", json.dumps({{
        "success": True,
        "filepath": export_path,
        "file_size": file_size,
        "quality": "{quality}"
    }}))
    
except Exception as e:
    print("EXPORT_RESULT:", json.dumps({{
        "success": False,
        "error": str(e)
    }}))
"""
        
        result = self.execute_blender_python(code)
        
        # Extract export result
        try:
            for line in result['output'].split('\n'):
                if line.startswith('EXPORT_RESULT:'):
                    return json.loads(line[14:])
        except:
            pass
            
        return {"success": False, "error": "Export failed"}

    def get_viewport_screenshot(self, filepath: str = "/app/exports/viewport.png", max_size: int = 800) -> Dict[str, Any]:
        """Render a screenshot from the active camera and save to a PNG file.

        Note: In headless mode there is no viewport; we perform an off-screen render
        using the active camera. Returns file path and size.
        """
        # Clamp resolution to a sensible range
        clamped_size = max(64, min(int(max_size), 4096))

        code = f"""
import bpy
import os
import json

output_path = r"{filepath}"
os.makedirs(os.path.dirname(output_path), exist_ok=True)

scene = bpy.context.scene

# Ensure a camera exists
if not bpy.data.cameras:
    bpy.ops.object.camera_add(location=(7, -7, 5))
    cam = bpy.context.object
    cam.rotation_euler = (1.1, 0, 0.785)
    scene.camera = cam
elif scene.camera is None:
    # Pick any existing camera
    for obj in bpy.data.objects:
        if obj.type == 'CAMERA':
            scene.camera = obj
            break

# Set render settings
scene.render.resolution_x = {clamped_size}
scene.render.resolution_y = {clamped_size}
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = 'PNG'
scene.render.filepath = output_path

try:
    bpy.ops.render.render(write_still=True)
    file_size = os.path.getsize(output_path) if os.path.exists(output_path) else 0
    print("SCREENSHOT_RESULT:", json.dumps({
        "success": True,
        "filepath": output_path,
        "file_size": file_size,
        "width": scene.render.resolution_x,
        "height": scene.render.resolution_y
    }))
except Exception as e:
    print("SCREENSHOT_RESULT:", json.dumps({
        "success": False,
        "error": str(e)
    }))
"""

        result = self.execute_blender_python(code)

        try:
            for line in result['output'].split('\n'):
                if line.startswith('SCREENSHOT_RESULT:'):
                    return json.loads(line[len('SCREENSHOT_RESULT:'):].strip())
        except Exception as e:
            return {"success": False, "error": f"Failed to parse screenshot result: {e}"}

        return {"success": False, "error": "Screenshot failed"}
    
    async def handle_mcp_request(self, websocket, path):
        """Handle MCP WebSocket requests"""
        try:
            self.clients.add(websocket)
            logger.info(f"Client connected from {websocket.remote_address}")
            
            async for message in websocket:
                try:
                    request = json.loads(message)
                    response = await self.process_request(request)
                    await websocket.send(json.dumps(response))
                    
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "error": "Invalid JSON", 
                        "id": None
                    }))
                except Exception as e:
                    await websocket.send(json.dumps({
                        "error": str(e),
                        "id": request.get("id", None)
                    }))
                    
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            self.clients.discard(websocket)
    
    async def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process individual MCP request"""
        method = request.get("method")
        params = request.get("params", {})
        request_id = request.get("id")
        
        logger.info(f"Processing request: {method}")
        
        if method == "get_scene_info":
            result = self.get_scene_info()
        elif method == "get_object_info":
            object_name = params.get("object_name", "Bello")
            result = self.get_object_info(object_name)
        elif method == "execute_blender_code":
            code = params.get("code", "")
            result = self.execute_blender_python(code)
        elif method == "export_gltf":
            filepath = params.get("filepath", "/app/exports/bello.glb")
            quality = params.get("quality", "high")
            result = self.export_gltf(filepath, quality=quality)
        elif method == "get_viewport_screenshot":
            filepath = params.get("filepath", "/app/exports/viewport.png")
            max_size = params.get("max_size", 800)
            result = self.get_viewport_screenshot(filepath=filepath, max_size=max_size)
        elif method == "ping":
            result = {"pong": "Blender MCP Server is running"}
        else:
            result = {"error": f"Unknown method: {method}"}
        
        return {
            "id": request_id,
            "result": result
        }
    
    async def start_server(self):
        """Start the MCP WebSocket server"""
        # Start Blender first
        await self.start_blender_headless()
        
        # Start health server in background
        health_process = subprocess.Popen([
            'python3', '/app/health-server.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Start WebSocket server
        logger.info(f"Starting MCP Server on {self.host}:{self.port}")
        server = await websockets.serve(
            self.handle_mcp_request,
            self.host,
            self.port
        )
        
        logger.info("🚀 Blender MCP Server is running!")
        logger.info(f"WebSocket: ws://{self.host}:{self.port}")
        logger.info(f"Health Check: http://{self.host}:8080/health")
        
        # Keep server running
        await server.wait_closed()

if __name__ == "__main__":
    # Create logs directory
    os.makedirs('/app/logs', exist_ok=True)
    os.makedirs('/app/temp', exist_ok=True)
    os.makedirs('/app/exports', exist_ok=True)
    
    # Start server
    server = BlenderMCPServer()
    asyncio.run(server.start_server())