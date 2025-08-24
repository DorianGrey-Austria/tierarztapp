#!/bin/bash

# Start Blender MCP Bridge Server
# Community-basierte Lösung für Claude Code ←→ Blender Integration

echo "🚀 Starting Blender MCP Bridge Server..."
echo "📁 Project: VetScan Pro 3000 Tierarztspiel"
echo "🎯 Purpose: Enable Claude Code to control Blender"
echo "=" 

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3."
    exit 1
fi

# Check if Blender is available
BLENDER_PATH="/Applications/Blender.app/Contents/MacOS/Blender"
if [ ! -f "$BLENDER_PATH" ]; then
    echo "❌ Blender not found at: $BLENDER_PATH"
    echo "💡 Please install Blender or update BLENDER_PATH in websocket-mcp-bridge.py"
    exit 1
fi

# Install required Python packages
echo "📦 Installing required packages..."
pip3 install websockets || {
    echo "❌ Failed to install websockets. Try: pip3 install --user websockets"
    exit 1
}

# Create temp directory
mkdir -p temp

# Start the bridge server
echo "🌉 Starting WebSocket MCP Bridge..."
echo "🔗 WebSocket URL: ws://localhost:8765"
echo "🎭 Blender Path: $BLENDER_PATH"
echo ""
echo "🔄 Ready for Claude Code connections!"
echo "📝 To test: node scripts/claude-code-blender-client.js"
echo "🛑 To stop: Press Ctrl+C"
echo "="

# Run the Python bridge server
python3 scripts/websocket-mcp-bridge.py