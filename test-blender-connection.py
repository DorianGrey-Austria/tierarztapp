#!/usr/bin/env python3
"""
Simple Blender MCP Connection Test
Testet ob wir überhaupt mit Blender kommunizieren können
"""

import socket
import json
import time

def test_blender_connection():
    print("🔌 Testing Blender MCP Connection on port 9876...")
    print("="*50)
    
    host = 'localhost'
    port = 9876
    
    try:
        # Create socket
        print(f"📡 Connecting to {host}:{port}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        
        # Connect
        sock.connect((host, port))
        print("✅ Connected successfully!")
        
        # Send simple get_scene_info command
        command = {
            "method": "get_scene_info",
            "params": {}
        }
        
        message = json.dumps(command) + '\n'
        print(f"\n📤 Sending command: {command['method']}")
        sock.send(message.encode())
        
        # Receive response
        print("⏳ Waiting for response...")
        response_data = b''
        start_time = time.time()
        
        while time.time() - start_time < 5:  # 5 second timeout
            try:
                chunk = sock.recv(4096)
                if chunk:
                    response_data += chunk
                    if b'\n' in chunk:  # Complete message received
                        break
            except socket.timeout:
                continue
        
        sock.close()
        
        if response_data:
            print("✅ Received response!")
            try:
                response = json.loads(response_data.decode().strip())
                print("\n📊 Response Details:")
                print(json.dumps(response, indent=2))
                
                if 'result' in response:
                    result = response['result']
                    if 'objects' in result:
                        print(f"\n🎯 Found {len(result['objects'])} objects in Blender:")
                        for obj in result['objects']:
                            print(f"   - {obj}")
                    
                    return True
                elif 'error' in response:
                    print(f"\n❌ Error from Blender: {response['error']}")
                    return False
                    
            except json.JSONDecodeError as e:
                print(f"❌ Failed to decode response: {e}")
                print(f"Raw response: {response_data.decode()[:200]}")
                return False
        else:
            print("❌ No response received")
            return False
            
    except ConnectionRefusedError:
        print(f"❌ Connection refused on port {port}")
        print("   Make sure Blender MCP is running on port 9876")
        return False
        
    except socket.timeout:
        print("❌ Connection timeout")
        print("   The connection was established but no response received")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Blender MCP Connection Test")
    print("="*50)
    
    success = test_blender_connection()
    
    print("\n" + "="*50)
    if success:
        print("✅ SUCCESS: Blender MCP connection is working!")
        print("🎯 You can communicate with Blender")
    else:
        print("❌ FAILED: Cannot communicate with Blender MCP")
        print("\n📝 Troubleshooting steps:")
        print("1. Check if Blender is running")
        print("2. Check if MCP addon is activated in Blender")
        print("3. Check if MCP server is started (N-key → BlenderMCP tab)")
        print("4. Verify port 9876 is not blocked")
        print("5. Run: python3 scripts/blender-mcp-health-check.py")
    
    exit(0 if success else 1)