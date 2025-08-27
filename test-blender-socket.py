#!/usr/bin/env python3
"""
Direct Socket Test to Blender on port 9876
Test what's actually running on port 9876
"""

import socket
import json
import time

def test_socket_communication():
    """Test different message formats to understand what Blender expects"""
    
    print("🔌 Testing direct socket to Blender on port 9876")
    print("="*50)
    
    host = 'localhost'
    port = 9876
    
    # Different message formats to try
    test_messages = [
        # Format 1: Simple command (as health check uses)
        {
            "method": "get_scene_info",
            "params": {}
        },
        # Format 2: With command type
        {
            "command_type": "query",
            "method": "get_scene_info",
            "params": {}
        },
        # Format 3: JSON-RPC style
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "get_scene_info",
            "params": {}
        },
        # Format 4: Direct Blender Python
        {
            "type": "python",
            "code": "import bpy; [obj.name for obj in bpy.data.objects]"
        }
    ]
    
    for i, msg in enumerate(test_messages, 1):
        print(f"\n📤 Test {i}: {list(msg.keys())}")
        
        try:
            # Create new socket for each test
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))
            
            # Send message
            message = json.dumps(msg) + '\n'
            sock.send(message.encode())
            
            # Try to receive response
            response_data = b''
            start_time = time.time()
            
            while time.time() - start_time < 2:
                try:
                    chunk = sock.recv(4096)
                    if chunk:
                        response_data += chunk
                        if b'\n' in chunk or len(chunk) < 4096:
                            break
                except socket.timeout:
                    break
            
            sock.close()
            
            if response_data:
                try:
                    # Try to decode as JSON
                    response_text = response_data.decode().strip()
                    response = json.loads(response_text)
                    
                    status = response.get('status', 'unknown')
                    if status == 'success':
                        print(f"   ✅ SUCCESS!")
                        print(f"   Response: {json.dumps(response, indent=2)}")
                        return True
                    else:
                        print(f"   ⚠️ Status: {status}")
                        if 'message' in response:
                            print(f"   Message: {response['message']}")
                        if 'error' in response:
                            print(f"   Error: {response['error']}")
                            
                except json.JSONDecodeError:
                    print(f"   📝 Raw response: {response_data.decode()[:100]}")
            else:
                print(f"   ❌ No response")
                
        except ConnectionRefusedError:
            print(f"   ❌ Connection refused")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_raw_python_execution():
    """Try to execute Python code directly in Blender"""
    
    print("\n🐍 Testing Python code execution")
    print("="*50)
    
    code = """
import bpy
objects = [obj.name for obj in bpy.data.objects]
{'status': 'success', 'objects': objects}
"""
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('localhost', 9876))
        
        # Try sending raw Python code
        sock.send(code.encode())
        
        response_data = sock.recv(4096)
        sock.close()
        
        if response_data:
            print("📊 Got response:")
            print(response_data.decode()[:200])
            return True
        else:
            print("❌ No response")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Blender Socket Communication Test")
    print("="*50)
    
    # Test different message formats
    success = test_socket_communication()
    
    if not success:
        # Try raw Python
        success = test_raw_python_execution()
    
    print("\n" + "="*50)
    if success:
        print("✅ Found working communication method!")
    else:
        print("❌ Could not establish proper communication")
        print("\n📝 The server is responding but expects a specific format")
        print("   The health check script works, so the format exists")
        print("   Need to match exact protocol used by Blender MCP addon")