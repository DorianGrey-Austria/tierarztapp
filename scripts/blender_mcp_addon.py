"""
Blender MCP Addon for VetScan Pro
==================================
This addon creates a socket server in Blender for real-time communication

INSTALLATION:
1. In Blender: Edit → Preferences → Add-ons
2. Click "Install..." and select this file
3. Enable "VetScan Pro MCP Bridge"
4. The server starts automatically on port 9876

Or run directly in Blender's Text Editor for testing
"""

bl_info = {
    "name": "VetScan Pro MCP Bridge",
    "author": "VetScan Team",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > VetScan",
    "description": "Real-time model export bridge for VetScan Pro",
    "category": "Import-Export",
}

import bpy
import socket
import threading
import json
import os
from pathlib import Path

class MCPServer:
    def __init__(self, host='localhost', port=9876):
        self.host = host
        self.port = port
        self.socket = None
        self.thread = None
        self.running = False
        
    def start(self):
        """Start the MCP server"""
        if self.running:
            print("MCP Server already running")
            return
            
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            self.running = True
            
            # Start server thread
            self.thread = threading.Thread(target=self.serve_forever)
            self.thread.daemon = True
            self.thread.start()
            
            print(f"✅ MCP Server started on {self.host}:{self.port}")
            
        except Exception as e:
            print(f"❌ Failed to start server: {e}")
            
    def serve_forever(self):
        """Main server loop"""
        while self.running:
            try:
                conn, addr = self.socket.accept()
                print(f"📱 Connection from {addr}")
                
                # Handle request in separate thread
                handler = threading.Thread(target=self.handle_client, args=(conn,))
                handler.daemon = True
                handler.start()
                
            except Exception as e:
                if self.running:
                    print(f"Server error: {e}")
                    
    def handle_client(self, conn):
        """Handle individual client connection"""
        try:
            data = conn.recv(1024).decode('utf-8')
            if not data:
                return
                
            request = json.loads(data)
            response = self.process_request(request)
            
            conn.send(json.dumps(response).encode('utf-8'))
            
        except Exception as e:
            error_response = {"error": str(e)}
            conn.send(json.dumps(error_response).encode('utf-8'))
            
        finally:
            conn.close()
            
    def process_request(self, request):
        """Process MCP requests"""
        cmd = request.get('command', '')
        
        if cmd == 'get_scene_info':
            return self.get_scene_info()
        elif cmd == 'export_model':
            return self.export_model(request.get('params', {}))
        elif cmd == 'get_selected':
            return self.get_selected_objects()
        elif cmd == 'live_export':
            return self.live_export()
        else:
            return {"error": f"Unknown command: {cmd}"}
            
    def get_scene_info(self):
        """Get current scene information"""
        objects = []
        for obj in bpy.context.scene.objects:
            if obj.type == 'MESH':
                objects.append({
                    'name': obj.name,
                    'vertices': len(obj.data.vertices) if obj.data else 0,
                    'location': list(obj.location),
                    'selected': obj.select_get()
                })
                
        return {
            'success': True,
            'objects': objects,
            'total': len(objects)
        }
        
    def get_selected_objects(self):
        """Get selected objects"""
        selected = []
        for obj in bpy.context.selected_objects:
            if obj.type == 'MESH':
                selected.append({
                    'name': obj.name,
                    'vertices': len(obj.data.vertices) if obj.data else 0
                })
                
        return {
            'success': True,
            'selected': selected
        }
        
    def export_model(self, params):
        """Export model with given parameters"""
        output_path = params.get('output_path', '/tmp/export.glb')
        selected_only = params.get('selected_only', True)
        
        try:
            bpy.ops.export_scene.gltf(
                filepath=output_path,
                export_format='GLB',
                export_selected=selected_only,
                export_yup=True,
                export_draco_mesh_compression_enable=True,
                export_draco_mesh_compression_level=6
            )
            
            return {
                'success': True,
                'output_path': output_path,
                'size': os.path.getsize(output_path) if os.path.exists(output_path) else 0
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def live_export(self):
        """Export current selection/scene immediately"""
        export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/bello/bello_live.glb"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        
        # Export selected or all
        selected = bpy.context.selected_objects
        mesh_objects = [obj for obj in selected if obj.type == 'MESH']
        
        if not mesh_objects:
            # No selection, export largest mesh
            meshes = [obj for obj in bpy.context.scene.objects if obj.type == 'MESH']
            if meshes:
                meshes.sort(key=lambda x: len(x.data.vertices) if x.data else 0, reverse=True)
                bpy.ops.object.select_all(action='DESELECT')
                meshes[0].select_set(True)
                bpy.context.view_layer.objects.active = meshes[0]
                
        try:
            bpy.ops.export_scene.gltf(
                filepath=export_path,
                export_format='GLB',
                export_selected=True,
                export_yup=True,
                export_draco_mesh_compression_enable=True,
                export_draco_mesh_compression_level=6
            )
            
            size = os.path.getsize(export_path) if os.path.exists(export_path) else 0
            
            # Notify connected clients
            print(f"✅ Live export: {size:,} bytes → {export_path}")
            
            return {
                'success': True,
                'path': export_path,
                'size': size,
                'timestamp': bpy.context.scene.frame_current
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
            
    def stop(self):
        """Stop the MCP server"""
        self.running = False
        if self.socket:
            self.socket.close()
        print("MCP Server stopped")

# Global server instance
mcp_server = None

class VETSCAN_OT_start_server(bpy.types.Operator):
    """Start MCP Server"""
    bl_idname = "vetscan.start_server"
    bl_label = "Start MCP Server"
    
    def execute(self, context):
        global mcp_server
        if not mcp_server:
            mcp_server = MCPServer()
        mcp_server.start()
        return {'FINISHED'}

class VETSCAN_OT_stop_server(bpy.types.Operator):
    """Stop MCP Server"""
    bl_idname = "vetscan.stop_server"
    bl_label = "Stop MCP Server"
    
    def execute(self, context):
        global mcp_server
        if mcp_server:
            mcp_server.stop()
        return {'FINISHED'}

class VETSCAN_OT_live_export(bpy.types.Operator):
    """Export current model immediately"""
    bl_idname = "vetscan.live_export"
    bl_label = "Live Export to VetScan"
    
    def execute(self, context):
        global mcp_server
        if not mcp_server:
            mcp_server = MCPServer()
            mcp_server.start()
            
        result = mcp_server.live_export()
        
        if result['success']:
            self.report({'INFO'}, f"Exported: {result['size']:,} bytes")
        else:
            self.report({'ERROR'}, f"Export failed: {result.get('error', 'Unknown')}")
            
        return {'FINISHED'}

class VETSCAN_PT_panel(bpy.types.Panel):
    """VetScan Pro MCP Panel"""
    bl_label = "VetScan Pro Export"
    bl_idname = "VETSCAN_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "VetScan"
    
    def draw(self, context):
        layout = self.layout
        
        col = layout.column()
        col.label(text="MCP Server Control:")
        
        row = col.row()
        row.operator("vetscan.start_server", icon='PLAY')
        row.operator("vetscan.stop_server", icon='PAUSE')
        
        col.separator()
        col.operator("vetscan.live_export", icon='EXPORT')
        
        col.separator()
        col.label(text="Server: localhost:9876")
        
        # Show selected objects
        col.separator()
        col.label(text="Selected Objects:")
        for obj in context.selected_objects:
            if obj.type == 'MESH':
                col.label(text=f"  • {obj.name}", icon='MESH_DATA')

# Registration
classes = [
    VETSCAN_OT_start_server,
    VETSCAN_OT_stop_server,
    VETSCAN_OT_live_export,
    VETSCAN_PT_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Auto-start server
    global mcp_server
    mcp_server = MCPServer()
    mcp_server.start()
    
    print("✅ VetScan Pro MCP Addon registered")

def unregister():
    global mcp_server
    if mcp_server:
        mcp_server.stop()
        
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
    print("VetScan Pro MCP Addon unregistered")

if __name__ == "__main__":
    # For testing in Text Editor
    register()
    print("\n🚀 MCP Server is running!")
    print("📡 Port: 9876")
    print("💡 Use the VetScan panel in the sidebar to export")