#!/usr/bin/env python3
"""
Test with correct 'type' field based on addon code
"""

import socket
import json
import time

def test_with_type_field():
    """Test using 'type' field as expected by the addon"""
    
    print("🔧 Testing with 'type' field")
    print("="*50)
    
    host = 'localhost'
    port = 9876
    
    # Test different type values
    test_commands = [
        {
            "type": "get_scene_info",
            "params": {}
        },
        {
            "type": "python",
            "params": {
                "code": "import bpy; [obj.name for obj in bpy.data.objects]"
            }
        },
        {
            "type": "execute_python",
            "params": {
                "code": "import bpy; print('Hello from Blender')"
            }
        },
        {
            "type": "list_objects",
            "params": {}
        }
    ]
    
    for i, command in enumerate(test_commands, 1):
        print(f"\n📤 Test {i}: type='{command.get('type')}'")
        print(f"   Command: {json.dumps(command)}")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect((host, port))
            
            # Send command
            message = json.dumps(command)
            sock.send(message.encode())
            
            # Receive response
            response_data = b''
            start_time = time.time()
            
            while time.time() - start_time < 3:
                try:
                    chunk = sock.recv(4096)
                    if chunk:
                        response_data += chunk
                        # Check if we have a complete JSON response
                        try:
                            json.loads(response_data.decode())
                            break
                        except:
                            continue
                except socket.timeout:
                    break
            
            sock.close()
            
            if response_data:
                try:
                    response = json.loads(response_data.decode())
                    status = response.get('status', 'unknown')
                    
                    if status == 'success':
                        print(f"   ✅ SUCCESS!")
                        if 'result' in response:
                            print(f"   Result: {response['result']}")
                        return True
                    else:
                        print(f"   ⚠️ Status: {status}")
                        if 'message' in response:
                            print(f"   Message: {response['message']}")
                            
                except json.JSONDecodeError as e:
                    print(f"   📝 Raw response: {response_data.decode()[:200]}")
            else:
                print(f"   ❌ No response")
                
        except ConnectionRefusedError:
            print(f"   ❌ Connection refused")
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return False

def test_get_objects():
    """Test getting objects from Blender scene"""
    
    print("\n🎯 Getting Blender scene objects")
    print("="*50)
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(('localhost', 9876))
        
        # Try to get objects
        command = {
            "type": "get_objects",
            "params": {}
        }
        
        print(f"📤 Sending: {json.dumps(command)}")
        sock.send(json.dumps(command).encode())
        
        response_data = sock.recv(8192)
        sock.close()
        
        if response_data:
            response = json.loads(response_data.decode())
            print(f"📊 Response: {json.dumps(response, indent=2)}")
            
            if response.get('status') == 'success':
                return True
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    print("🧪 Correct Format Test - Using 'type' field")
    print("="*50)
    
    # Test with type field
    success = test_with_type_field()
    
    if not success:
        # Try specific get_objects command
        success = test_get_objects()
    
    print("\n" + "="*50)
    if success:
        print("✅ SUCCESS! Communication established with Blender")
        print("\n📝 Use format:")
        print(json.dumps({
            "type": "command_name",
            "params": {}
        }, indent=2))
    else:
        print("❌ Still cannot communicate properly")
        print("   The addon might have specific command types")
        print("   Check what 'type' values are supported in the addon code")