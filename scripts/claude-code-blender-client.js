/**
 * Claude Code Blender Client
 * WebSocket client für die Kommunikation mit dem Blender MCP Bridge
 * 
 * Löst das Problem: Claude Code kann nicht direkt mit Blender kommunizieren
 * Lösung: WebSocket Bridge als Vermittler
 */

class BlenderMCPClient {
    constructor(host = 'localhost', port = 8765) {
        this.host = host;
        this.port = port;
        this.websocket = null;
        this.commandId = 0;
        this.pendingCommands = new Map();
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
    }

    /**
     * Connect to Blender MCP Bridge WebSocket Server
     */
    async connect() {
        return new Promise((resolve, reject) => {
            try {
                const wsUrl = `ws://${this.host}:${this.port}`;
                console.log(`🔌 Connecting to Blender MCP Bridge: ${wsUrl}`);
                
                this.websocket = new WebSocket(wsUrl);
                
                this.websocket.onopen = (event) => {
                    console.log('✅ Connected to Blender MCP Bridge');
                    this.isConnected = true;
                    this.reconnectAttempts = 0;
                    resolve(true);
                };
                
                this.websocket.onmessage = (event) => {
                    this.handleMessage(event.data);
                };
                
                this.websocket.onclose = (event) => {
                    console.log('🔌 Connection closed:', event.code, event.reason);
                    this.isConnected = false;
                    this.attemptReconnect();
                };
                
                this.websocket.onerror = (error) => {
                    console.error('❌ WebSocket error:', error);
                    reject(error);
                };
                
            } catch (error) {
                reject(error);
            }
        });
    }

    /**
     * Attempt to reconnect to the bridge server
     */
    async attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`🔄 Reconnect attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
            
            setTimeout(() => {
                this.connect().catch(err => {
                    console.error('Reconnect failed:', err);
                });
            }, 2000 * this.reconnectAttempts);
        } else {
            console.error('❌ Max reconnect attempts reached');
        }
    }

    /**
     * Handle incoming WebSocket messages
     */
    handleMessage(data) {
        try {
            const response = JSON.parse(data);
            const commandId = response.command_id;
            
            if (this.pendingCommands.has(commandId)) {
                const { resolve, reject } = this.pendingCommands.get(commandId);
                this.pendingCommands.delete(commandId);
                
                if (response.success) {
                    resolve(response);
                } else {
                    reject(new Error(response.error || 'Command failed'));
                }
            }
        } catch (error) {
            console.error('❌ Error parsing message:', error);
        }
    }

    /**
     * Send command to Blender via bridge
     */
    async sendCommand(commandData) {
        if (!this.isConnected) {
            throw new Error('Not connected to Blender MCP Bridge');
        }
        
        this.commandId++;
        commandData.command_id = this.commandId;
        
        return new Promise((resolve, reject) => {
            this.pendingCommands.set(this.commandId, { resolve, reject });
            
            // Set timeout for command
            setTimeout(() => {
                if (this.pendingCommands.has(this.commandId)) {
                    this.pendingCommands.delete(this.commandId);
                    reject(new Error('Command timeout'));
                }
            }, 30000); // 30 second timeout
            
            this.websocket.send(JSON.stringify(commandData));
        });
    }

    /**
     * Get current Blender scene information
     */
    async getSceneInfo() {
        return await this.sendCommand({
            type: 'get_scene_info'
        });
    }

    /**
     * Create object in Blender
     */
    async createObject(objectType = 'cube', location = [0, 0, 0], name = null) {
        return await this.sendCommand({
            type: 'create_object',
            object_type: objectType,
            location: location,
            name: name || `Object_${Date.now()}`
        });
    }

    /**
     * Execute Python script in Blender
     */
    async executePython(script) {
        return await this.sendCommand({
            type: 'execute_python',
            script: script
        });
    }

    /**
     * Export scene as GLB
     */
    async exportGLB(outputPath = null) {
        return await this.sendCommand({
            type: 'export_glb',
            output_path: outputPath || `export_${Date.now()}.glb`
        });
    }

    /**
     * Take screenshot of Blender viewport
     */
    async takeScreenshot(outputPath = null) {
        return await this.sendCommand({
            type: 'take_screenshot',
            output_path: outputPath || `screenshot_${Date.now()}.png`
        });
    }

    /**
     * Create Bello dog model using the bridge
     */
    async createBelloModel() {
        const belloScript = `
import bpy
from mathutils import Vector

print("🐕 Creating Bello - Advanced Version via Bridge")

# Clean up scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create main body
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = 'Bello_Body'
body.scale = (2.5, 1.2, 1.0)

# Create head
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, -2.5, 1.5))
head = bpy.context.object
head.name = 'Bello_Head'
head.scale = (1.2, 1.0, 1.0)

# Create legs
leg_positions = [
    (1.2, 0.8, 0), (1.2, -0.8, 0),   # Front legs
    (-1.2, 0.8, 0), (-1.2, -0.8, 0)  # Back legs
]

for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.5, location=pos)
    leg = bpy.context.object
    leg.name = f'Bello_Leg_{i+1}'

# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.5, location=(2.5, 0, 1.2))
tail = bpy.context.object
tail.name = 'Bello_Tail'
tail.rotation_euler = (0, 1.2, 0)

# Create ears
for i, side in enumerate([0.8, -0.8]):
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(side*0.7, -3, 2.2))
    ear = bpy.context.object
    ear.name = f'Bello_Ear_{i+1}'
    ear.scale = (0.3, 0.8, 1.2)

# Add basic material
material = bpy.data.materials.new(name="BelloFur")
material.use_nodes = True
material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.6, 0.4, 1.0)  # Golden brown

# Apply material to all objects
for obj in bpy.context.scene.objects:
    if obj.name.startswith('Bello_'):
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

# Select all Bello parts for grouping
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.context.scene.objects:
    if obj.name.startswith('Bello_'):
        obj.select_set(True)

print(f"✅ Bello created with {len([o for o in bpy.context.scene.objects if o.name.startswith('Bello_')])} parts")
`;

        return await this.executePython(belloScript);
    }

    /**
     * Disconnect from the bridge
     */
    disconnect() {
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
            this.isConnected = false;
        }
    }

    /**
     * Check if bridge server is available
     */
    static async checkBridgeAvailable(host = 'localhost', port = 8765) {
        return new Promise((resolve) => {
            try {
                const wsUrl = `ws://${host}:${port}`;
                const testWs = new WebSocket(wsUrl);
                
                testWs.onopen = () => {
                    testWs.close();
                    resolve(true);
                };
                
                testWs.onerror = () => {
                    resolve(false);
                };
                
                // Timeout after 3 seconds
                setTimeout(() => {
                    testWs.close();
                    resolve(false);
                }, 3000);
                
            } catch (error) {
                resolve(false);
            }
        });
    }
}

// Node.js export for server-side usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = BlenderMCPClient;
}

// Browser export for client-side usage
if (typeof window !== 'undefined') {
    window.BlenderMCPClient = BlenderMCPClient;
}

// Example usage for testing
async function testBlenderBridge() {
    console.log('🧪 Testing Blender MCP Bridge...');
    
    // Check if bridge is available
    const isAvailable = await BlenderMCPClient.checkBridgeAvailable();
    if (!isAvailable) {
        console.error('❌ Blender MCP Bridge not available on ws://localhost:8765');
        console.log('💡 Run: python3 scripts/websocket-mcp-bridge.py');
        return;
    }
    
    const client = new BlenderMCPClient();
    
    try {
        // Connect to bridge
        await client.connect();
        
        // Get scene info
        console.log('📊 Getting scene info...');
        const sceneInfo = await client.getSceneInfo();
        console.log('Scene:', sceneInfo.data);
        
        // Create Bello model
        console.log('🐕 Creating Bello model...');
        const belloResult = await client.createBelloModel();
        console.log('Bello creation result:', belloResult.success ? '✅' : '❌');
        
        // Take screenshot
        console.log('📸 Taking screenshot...');
        const screenshot = await client.takeScreenshot();
        console.log('Screenshot:', screenshot.data);
        
        console.log('✅ All tests completed successfully!');
        
    } catch (error) {
        console.error('❌ Test failed:', error);
    } finally {
        client.disconnect();
    }
}

// Auto-run test if this script is executed directly
if (typeof window === 'undefined' && require.main === module) {
    testBlenderBridge();
}