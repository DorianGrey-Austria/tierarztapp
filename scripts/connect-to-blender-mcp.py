#!/usr/bin/env python3
"""
Connect to Blender MCP Addon and Export Model
==============================================
This script connects to the running Blender instance via the MCP addon
and triggers an export of the current model.
"""

import socket
import json
import time
import os
from pathlib import Path

# Configuration
MCP_HOST = 'localhost'
MCP_PORT = 9876
OUTPUT_DIR = Path(__file__).parent.parent / "assets" / "models" / "animals" / "bello"

def send_mcp_command(command, params=None):
    """Send command to Blender MCP server"""
    try:
        # Create socket connection
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((MCP_HOST, MCP_PORT))
        
        # Prepare request
        request = {
            'command': command,
            'params': params or {}
        }
        
        # Send request
        sock.send(json.dumps(request).encode('utf-8'))
        
        # Receive response
        response = sock.recv(4096).decode('utf-8')
        sock.close()
        
        return json.loads(response)
        
    except socket.timeout:
        print(f"❌ Connection timeout - Is Blender MCP addon running on port {MCP_PORT}?")
        return None
    except ConnectionRefusedError:
        print(f"❌ Connection refused - Blender MCP addon not running on port {MCP_PORT}")
        print("💡 In Blender: Run the blender_mcp_addon.py script in Text Editor")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("🐕 VetScan Pro - Blender MCP Client")
    print("=" * 50)
    print(f"📡 Connecting to Blender MCP on {MCP_HOST}:{MCP_PORT}...")
    
    # Test connection with scene info
    print("\n📊 Getting scene information...")
    scene_info = send_mcp_command('get_scene_info')
    
    if scene_info:
        print(f"✅ Connected! Found {scene_info.get('total', 0)} mesh objects")
        
        if scene_info.get('objects'):
            print("\n📋 Scene objects:")
            for obj in scene_info['objects']:
                selected = "✓" if obj.get('selected') else " "
                print(f"  [{selected}] {obj['name']}: {obj['vertices']} vertices")
        
        # Get selected objects
        print("\n🎯 Getting selected objects...")
        selected = send_mcp_command('get_selected')
        
        if selected and selected.get('selected'):
            print(f"Selected objects: {[obj['name'] for obj in selected['selected']]}")
        else:
            print("No objects selected - will export largest mesh")
        
        # Trigger live export
        print("\n📦 Triggering live export...")
        export_result = send_mcp_command('live_export')
        
        if export_result and export_result.get('success'):
            print(f"✅ Export successful!")
            print(f"   Path: {export_result['path']}")
            print(f"   Size: {export_result['size']:,} bytes")
            print(f"\n🎮 Model exported! Refresh your browser to see changes.")
            
            # Send WebSocket notification (optional)
            try:
                import asyncio
                import websockets
                
                async def notify_browser():
                    uri = "ws://localhost:8765"
                    try:
                        async with websockets.connect(uri) as ws:
                            await ws.send(json.dumps({
                                'type': 'model_updated',
                                'path': export_result['path'],
                                'timestamp': time.time()
                            }))
                            print("📱 Browser notified via WebSocket")
                    except:
                        pass
                
                asyncio.run(notify_browser())
            except ImportError:
                print("💡 Install websockets for browser notification: pip install websockets")
            
        else:
            print("❌ Export failed")
            if export_result:
                print(f"   Error: {export_result.get('error', 'Unknown')}")
    else:
        print("\n❌ Could not connect to Blender MCP")
        print("\n📝 Instructions:")
        print("1. Open Blender with your dog model")
        print("2. Switch to 'Scripting' workspace")
        print("3. Open scripts/blender_mcp_addon.py in Text Editor")
        print("4. Click 'Run Script'")
        print("5. Look for 'MCP Server started' message")
        print("6. Run this script again")

if __name__ == "__main__":
    main()