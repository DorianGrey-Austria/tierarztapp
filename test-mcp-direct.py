#!/usr/bin/env python3
"""
Direct MCP Protocol Test
Tests using the exact MCP JSON-RPC format
"""

import json
import sys
import subprocess
import time

def test_mcp_direct():
    """Test MCP using subprocess to communicate with blender-mcp"""
    
    print("🔧 Testing MCP Direct Communication")
    print("="*50)
    
    # Create proper MCP request
    request = {
        "jsonrpc": "2.0",
        "method": "tools/list",
        "id": 1
    }
    
    print(f"📤 Sending MCP request: {request['method']}")
    
    try:
        # Try to communicate with blender-mcp via stdin/stdout
        process = subprocess.Popen(
            ['uvx', 'blender-mcp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send request
        request_str = json.dumps(request)
        print(f"📝 Request: {request_str}")
        
        stdout, stderr = process.communicate(input=request_str + '\n', timeout=5)
        
        if stdout:
            print("\n✅ Got response!")
            print("📊 Response:")
            
            # Parse response lines
            for line in stdout.strip().split('\n'):
                if line.strip():
                    try:
                        response = json.loads(line)
                        print(json.dumps(response, indent=2))
                        
                        if 'result' in response:
                            tools = response.get('result', {}).get('tools', [])
                            if tools:
                                print(f"\n🛠️ Available MCP Tools ({len(tools)}):")
                                for tool in tools[:5]:  # Show first 5 tools
                                    name = tool.get('name', 'unknown')
                                    desc = tool.get('description', '')[:50]
                                    print(f"   - {name}: {desc}...")
                                return True
                    except json.JSONDecodeError:
                        continue
        
        if stderr:
            print(f"\n⚠️ Stderr: {stderr}")
        
        return False
        
    except subprocess.TimeoutExpired:
        print("❌ Process timeout")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_blender_tools():
    """Test specific Blender MCP tools"""
    
    print("\n🎯 Testing Blender-specific MCP tools")
    print("="*50)
    
    # Test get_scene_info tool
    request = {
        "jsonrpc": "2.0",
        "method": "tools/call",
        "params": {
            "name": "get_scene_info",
            "arguments": {}
        },
        "id": 2
    }
    
    print(f"📤 Calling tool: get_scene_info")
    
    try:
        process = subprocess.Popen(
            ['uvx', 'blender-mcp'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        stdout, stderr = process.communicate(
            input=json.dumps(request) + '\n',
            timeout=10
        )
        
        if stdout:
            print("\n📊 Scene Info Response:")
            for line in stdout.strip().split('\n'):
                if line.strip():
                    try:
                        response = json.loads(line)
                        if 'result' in response:
                            result = response['result']
                            print(json.dumps(result, indent=2))
                            return True
                        elif 'error' in response:
                            print(f"❌ Error: {response['error']}")
                            return False
                    except json.JSONDecodeError:
                        continue
        
        if stderr:
            print(f"⚠️ Stderr: {stderr}")
        
        return False
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 MCP Direct Communication Test")
    print("="*50)
    
    # Test 1: List available tools
    success1 = test_mcp_direct()
    
    # Test 2: Try Blender-specific tools
    if success1:
        success2 = test_blender_tools()
    else:
        success2 = False
    
    print("\n" + "="*50)
    if success1 and success2:
        print("✅ SUCCESS: MCP communication is working!")
        print("🎯 Blender MCP tools are accessible")
    elif success1:
        print("⚠️ PARTIAL SUCCESS: MCP works but Blender tools failed")
        print("   Blender might not be connected properly")
    else:
        print("❌ FAILED: Cannot communicate with MCP")
        print("\n📝 Check:")
        print("1. Is Blender running?")
        print("2. Is the MCP addon activated in Blender?")
        print("3. Check .cursor/mcp.json configuration")
    
    exit(0 if (success1 and success2) else 1)