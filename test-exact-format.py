#!/usr/bin/env python3
"""
Test exact format that works with health check
"""

import socket
import json
import time

def send_exact_health_check_format():
    """Send exactly what the health check sends"""
    
    print("🔬 Sending EXACT health check format")
    print("="*50)
    
    host = 'localhost'
    port = 9876
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((host, port))
        print("✅ Connected to localhost:9876")
        
        # Exact format from health check
        test_command = {
            "method": "get_scene_info",
            "params": {}
        }
        
        message = json.dumps(test_command) + '\n'
        print(f"📤 Sending: {message.strip()}")
        
        sock.send(message.encode())
        
        # Wait for response
        response = sock.recv(4096).decode()
        sock.close()
        
        print(f"📊 Raw response: {response}")
        
        if response:
            try:
                data = json.loads(response)
                print("\n📋 Parsed response:")
                print(json.dumps(data, indent=2))
                
                # The response says "Unknown command type: None"
                # This means it's looking for a "command_type" field
                print("\n💡 Analysis:")
                print("Server expects a 'command_type' field")
                print("Let's try with different command types...")
                
                return True
            except:
                pass
                
    except Exception as e:
        print(f"❌ Error: {e}")
    
    return False

def test_command_types():
    """Test different command_type values"""
    
    print("\n🔍 Testing different command_type values")
    print("="*50)
    
    command_types = [
        "get_scene_info",
        "scene_info", 
        "query",
        "blender",
        "mcp",
        "execute",
        "python",
        "tool"
    ]
    
    for cmd_type in command_types:
        print(f"\n📤 Testing command_type: '{cmd_type}'")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            sock.connect(('localhost', 9876))
            
            test_command = {
                "command_type": cmd_type,
                "method": "get_scene_info",
                "params": {}
            }
            
            message = json.dumps(test_command) + '\n'
            sock.send(message.encode())
            
            response = sock.recv(4096).decode()
            sock.close()
            
            if response:
                try:
                    data = json.loads(response)
                    status = data.get('status', '')
                    
                    if status == 'success':
                        print(f"   ✅ SUCCESS with command_type='{cmd_type}'!")
                        print(f"   Response: {json.dumps(data, indent=2)}")
                        return cmd_type
                    elif status == 'error':
                        error_msg = data.get('message', '')
                        if 'Unknown command type' not in error_msg:
                            print(f"   ⚠️ Different error: {error_msg}")
                        else:
                            print(f"   ❌ Unknown command type: {cmd_type}")
                    else:
                        print(f"   📊 Response: {data}")
                        
                except json.JSONDecodeError:
                    print(f"   📝 Non-JSON response: {response[:100]}")
                    
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    return None

if __name__ == "__main__":
    print("🧪 Exact Format Test")
    print("="*50)
    
    # First, replicate exact health check
    send_exact_health_check_format()
    
    # Then test command types
    working_type = test_command_types()
    
    print("\n" + "="*50)
    if working_type:
        print(f"✅ SUCCESS! Working command_type: '{working_type}'")
        print("\nUse this format:")
        print(json.dumps({
            "command_type": working_type,
            "method": "get_scene_info",
            "params": {}
        }, indent=2))
    else:
        print("❌ Could not find working command_type")
        print("\n📝 The Blender MCP addon might use a custom protocol")
        print("   Check the addon source code for the exact format")