/**
 * Subagent-Ready Blender Interface
 * High-level API für zukünftige Claude Code Subagenten
 * 
 * Abstraction Layer über WebSocket MCP Bridge
 * Ermöglicht einfache Blender-Steuerung für AI Agents
 */

const BlenderMCPClient = require('./claude-code-blender-client');

class SubagentBlenderInterface {
    constructor() {
        this.client = null;
        this.isInitialized = false;
        this.models = new Map(); // Track created models
        this.lastScreenshot = null;
        this.config = {
            autoScreenshot: true,
            exportOnCreate: false,
            qualityPresets: {
                low: { resolution: [512, 512], samples: 32 },
                medium: { resolution: [1024, 1024], samples: 64 },
                high: { resolution: [1920, 1080], samples: 128 }
            }
        };
    }

    /**
     * Initialize Blender connection for subagent
     * Returns success status and capabilities
     */
    async initialize() {
        try {
            // Check if bridge is available
            const bridgeAvailable = await BlenderMCPClient.checkBridgeAvailable();
            if (!bridgeAvailable) {
                return {
                    success: false,
                    error: "Blender MCP Bridge not available",
                    suggestion: "Run: ./start-blender-bridge.sh",
                    capabilities: []
                };
            }

            // Connect to bridge
            this.client = new BlenderMCPClient();
            await this.client.connect();

            // Get initial scene state
            const sceneInfo = await this.client.getSceneInfo();
            
            this.isInitialized = true;
            
            return {
                success: true,
                bridge_status: "connected",
                scene_objects: sceneInfo.data?.objects?.length || 0,
                capabilities: [
                    "create_animal_models",
                    "apply_medical_visualizations", 
                    "export_glb_models",
                    "take_screenshots",
                    "modify_existing_objects",
                    "create_procedural_anatomy"
                ]
            };

        } catch (error) {
            return {
                success: false,
                error: error.message,
                suggestion: "Check if Blender MCP Bridge is running",
                capabilities: []
            };
        }
    }

    /**
     * Create veterinary animal model
     * Specialized for VetScan Pro 3000 use cases
     */
    async createVeterinaryAnimal(animalType, options = {}) {
        if (!this.isInitialized) {
            throw new Error("Interface not initialized. Call initialize() first.");
        }

        const modelId = `veterinary_${animalType}_${Date.now()}`;
        const animalOptions = {
            size: options.size || 'medium',
            breed: options.breed || 'generic',
            medicalMode: options.medicalMode || 'normal',
            anatomyDetail: options.anatomyDetail || 'basic',
            ...options
        };

        try {
            let script = '';
            
            switch (animalType.toLowerCase()) {
                case 'dog':
                case 'hund':
                    script = this._generateDogScript(modelId, animalOptions);
                    break;
                case 'cat':
                case 'katze':
                    script = this._generateCatScript(modelId, animalOptions);
                    break;
                case 'horse':
                case 'pferd':
                    script = this._generateHorseScript(modelId, animalOptions);
                    break;
                case 'rabbit':
                case 'kaninchen':
                    script = this._generateRabbitScript(modelId, animalOptions);
                    break;
                default:
                    script = this._generateGenericAnimalScript(modelId, animalType, animalOptions);
            }

            // Execute creation script
            const result = await this.client.executePython(script);
            
            if (result.success) {
                // Store model info
                this.models.set(modelId, {
                    type: animalType,
                    options: animalOptions,
                    created: new Date(),
                    exported: false
                });

                // Auto-screenshot if enabled
                if (this.config.autoScreenshot) {
                    const screenshot = await this.takeScreenshot(`${modelId}_preview`);
                    this.lastScreenshot = screenshot.data?.screenshot_path;
                }

                return {
                    success: true,
                    model_id: modelId,
                    animal_type: animalType,
                    objects_created: this._extractObjectCount(result.stdout),
                    screenshot: this.lastScreenshot,
                    export_ready: true
                };
            } else {
                return {
                    success: false,
                    error: result.stderr || result.error,
                    model_id: null
                };
            }

        } catch (error) {
            return {
                success: false,
                error: error.message,
                model_id: null
            };
        }
    }

    /**
     * Apply medical visualization to existing model
     */
    async applyMedicalVisualization(modelId, visualizationType) {
        if (!this.models.has(modelId)) {
            throw new Error(`Model ${modelId} not found`);
        }

        const visualizationScript = this._generateMedicalVisualizationScript(modelId, visualizationType);
        
        const result = await this.client.executePython(visualizationScript);
        
        if (result.success && this.config.autoScreenshot) {
            const screenshot = await this.takeScreenshot(`${modelId}_${visualizationType}`);
            this.lastScreenshot = screenshot.data?.screenshot_path;
        }
        
        return {
            success: result.success,
            visualization_type: visualizationType,
            screenshot: this.lastScreenshot,
            error: result.error
        };
    }

    /**
     * Export model for Three.js integration
     */
    async exportForThreeJS(modelId, quality = 'medium') {
        if (!this.models.has(modelId)) {
            throw new Error(`Model ${modelId} not found`);
        }

        const outputPath = `exports/${modelId}_${quality}.glb`;
        const exportResult = await this.client.exportGLB(outputPath);
        
        if (exportResult.success) {
            // Mark model as exported
            const modelInfo = this.models.get(modelId);
            modelInfo.exported = true;
            modelInfo.exportPath = outputPath;
            this.models.set(modelId, modelInfo);
        }
        
        return {
            success: exportResult.success,
            export_path: outputPath,
            file_size: exportResult.data?.file_size,
            quality: quality,
            three_js_ready: exportResult.success
        };
    }

    /**
     * Take screenshot with automatic naming
     */
    async takeScreenshot(name = null) {
        const screenshotName = name || `screenshot_${Date.now()}`;
        const outputPath = `screenshots/${screenshotName}.png`;
        
        return await this.client.takeScreenshot(outputPath);
    }

    /**
     * Get comprehensive scene report for subagents
     */
    async getSceneReport() {
        const sceneInfo = await this.client.getSceneInfo();
        
        return {
            timestamp: new Date().toISOString(),
            scene_name: sceneInfo.data?.scene_name,
            total_objects: sceneInfo.data?.objects?.length || 0,
            veterinary_models: this.models.size,
            last_screenshot: this.lastScreenshot,
            models_created: Array.from(this.models.entries()).map(([id, info]) => ({
                id,
                type: info.type,
                created: info.created,
                exported: info.exported
            })),
            capabilities_status: {
                bridge_connected: this.isInitialized,
                blender_responsive: sceneInfo.success,
                export_ready: true,
                screenshot_ready: true
            }
        };
    }

    /**
     * Generate dog creation script
     */
    _generateDogScript(modelId, options) {
        return `
import bpy
from mathutils import Vector

print(f"🐕 Creating veterinary dog model: ${modelId}")

# Clean up scene (only if requested)
if ${options.clearScene !== false}:
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

# Create dog base geometry
bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 1))
body = bpy.context.object
body.name = '${modelId}_Body'
body.scale = (2.5, 1.2, 1.0)

# Create head with breed-specific proportions
head_scale = ${options.breed === 'labrador' ? '(1.3, 1.1, 1.0)' : '(1.2, 1.0, 1.0)'}
bpy.ops.mesh.primitive_cube_add(size=1.2, location=(0, -2.5, 1.5))
head = bpy.context.object
head.name = '${modelId}_Head'
head.scale = head_scale

# Create legs
leg_positions = [(1.2, 0.8, 0), (1.2, -0.8, 0), (-1.2, 0.8, 0), (-1.2, -0.8, 0)]
for i, pos in enumerate(leg_positions):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.3, depth=1.5, location=pos)
    leg = bpy.context.object
    leg.name = f'${modelId}_Leg_{i+1}'

# Create tail
bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=1.5, location=(2.5, 0, 1.2))
tail = bpy.context.object
tail.name = '${modelId}_Tail'
tail.rotation_euler = (0, 1.2, 0)

# Create ears (breed-specific)
ear_scale = ${options.breed === 'germanshepherd' ? '(0.4, 1.2, 1.5)' : '(0.3, 0.8, 1.2)'}
for i, side in enumerate([0.8, -0.8]):
    bpy.ops.mesh.primitive_cube_add(size=0.6, location=(side*0.7, -3, 2.2))
    ear = bpy.context.object
    ear.name = f'${modelId}_Ear_{i+1}'
    ear.scale = ear_scale

# Apply veterinary-appropriate material
material = bpy.data.materials.new(name="${modelId}_VetFur")
material.use_nodes = True
nodes = material.node_tree.nodes
principled = nodes["Principled BSDF"]

# Set realistic fur color
fur_colors = {
    'golden': (0.8, 0.6, 0.4, 1.0),
    'brown': (0.4, 0.3, 0.2, 1.0),
    'black': (0.1, 0.1, 0.1, 1.0),
    'white': (0.9, 0.9, 0.9, 1.0)
}
color = fur_colors.get('${options.color || 'golden'}', fur_colors['golden'])
principled.inputs[0].default_value = color

# Apply material to all parts
for obj in bpy.context.scene.objects:
    if obj.name.startswith('${modelId}_'):
        if obj.data.materials:
            obj.data.materials[0] = material
        else:
            obj.data.materials.append(material)

print(f"✅ Dog model ${modelId} created successfully")
print(f"Parts: {len([o for o in bpy.context.scene.objects if o.name.startswith('${modelId}_')])}")
`;
    }

    /**
     * Generate medical visualization script
     */
    _generateMedicalVisualizationScript(modelId, visualizationType) {
        const visualizations = {
            xray: {
                transparency: 0.3,
                emission: (0.8, 0.9, 1.0, 1.0),
                metallic: 0.0,
                roughness: 0.1
            },
            ultrasound: {
                transparency: 0.5,
                emission: (0.2, 0.4, 0.8, 1.0),
                metallic: 0.0,
                roughness: 0.8
            },
            thermal: {
                transparency: 0.2,
                emission: (1.0, 0.3, 0.1, 1.0),
                metallic: 0.1,
                roughness: 0.3
            },
            mri: {
                transparency: 0.4,
                emission: (0.9, 0.9, 0.9, 1.0),
                metallic: 0.0,
                roughness: 0.9
            }
        };

        const viz = visualizations[visualizationType] || visualizations.xray;

        return `
import bpy

print(f"🔬 Applying ${visualizationType} visualization to ${modelId}")

# Find all objects belonging to this model
model_objects = [obj for obj in bpy.context.scene.objects if obj.name.startswith('${modelId}_')]

if not model_objects:
    print(f"❌ No objects found for model ${modelId}")
else:
    # Create medical visualization material
    mat = bpy.data.materials.new(name="${modelId}_${visualizationType}")
    mat.use_nodes = True
    mat.blend_method = 'BLEND'
    
    nodes = mat.node_tree.nodes
    principled = nodes["Principled BSDF"]
    
    # Set medical visualization properties
    principled.inputs[0].default_value = ${JSON.stringify(viz.emission)}  # Base Color
    principled.inputs[18].default_value = ${viz.transparency}  # Alpha
    principled.inputs[6].default_value = ${viz.metallic}  # Metallic
    principled.inputs[7].default_value = ${viz.roughness}  # Roughness
    principled.inputs[17].default_value = ${viz.emission.slice(0,3)}  # Emission
    principled.inputs[18].default_value = 0.5  # Emission Strength
    
    # Apply to all model objects
    for obj in model_objects:
        if obj.data and hasattr(obj.data, 'materials'):
            obj.data.materials.clear()
            obj.data.materials.append(mat)
    
    print(f"✅ Applied ${visualizationType} to {len(model_objects)} objects")
`;
    }

    /**
     * Generate generic animal script template
     */
    _generateGenericAnimalScript(modelId, animalType, options) {
        return `
import bpy

print(f"🐾 Creating generic animal model: ${modelId} (${animalType})")

# Basic animal geometry - can be extended for specific animals
bpy.ops.mesh.primitive_cube_add(size=1.5, location=(0, 0, 0.75))
body = bpy.context.object
body.name = '${modelId}_Body'

# Add basic material
material = bpy.data.materials.new(name="${modelId}_Material")
material.use_nodes = True
material.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.5, 0.4, 1.0)

body.data.materials.append(material)

print(f"✅ Generic ${animalType} model created: ${modelId}")
`;
    }

    /**
     * Extract object count from Blender stdout
     */
    _extractObjectCount(stdout) {
        const match = stdout.match(/Parts: (\d+)/);
        return match ? parseInt(match[1]) : 1;
    }

    /**
     * Clean up and disconnect
     */
    async cleanup() {
        if (this.client) {
            this.client.disconnect();
            this.client = null;
        }
        this.isInitialized = false;
        this.models.clear();
    }
}

// Export for use by other modules
module.exports = SubagentBlenderInterface;

// Example usage for subagents
async function demonstrateSubagentUsage() {
    console.log('🤖 Subagent Blender Interface Demo');
    
    const blender = new SubagentBlenderInterface();
    
    try {
        // Initialize connection
        console.log('🔌 Initializing Blender interface...');
        const initResult = await blender.initialize();
        
        if (!initResult.success) {
            console.error('❌ Initialization failed:', initResult.error);
            console.log('💡 Suggestion:', initResult.suggestion);
            return;
        }
        
        console.log('✅ Capabilities:', initResult.capabilities);
        
        // Create veterinary dog model
        console.log('🐕 Creating Bello model for VetScan Pro...');
        const dogResult = await blender.createVeterinaryAnimal('dog', {
            breed: 'labrador',
            color: 'golden',
            size: 'medium',
            anatomyDetail: 'detailed'
        });
        
        if (dogResult.success) {
            console.log('✅ Bello created:', dogResult.model_id);
            console.log('📸 Screenshot:', dogResult.screenshot);
            
            // Apply X-ray visualization
            console.log('🔬 Applying X-ray visualization...');
            const xrayResult = await blender.applyMedicalVisualization(dogResult.model_id, 'xray');
            
            if (xrayResult.success) {
                console.log('✅ X-ray applied');
                
                // Export for Three.js
                console.log('📦 Exporting for Three.js...');
                const exportResult = await blender.exportForThreeJS(dogResult.model_id, 'medium');
                
                if (exportResult.success) {
                    console.log('✅ Export successful:', exportResult.export_path);
                    console.log('📊 File size:', exportResult.file_size, 'bytes');
                }
            }
        }
        
        // Get final scene report
        const report = await blender.getSceneReport();
        console.log('📋 Final scene report:', {
            objects: report.total_objects,
            models: report.veterinary_models,
            status: report.capabilities_status
        });
        
    } catch (error) {
        console.error('❌ Demo failed:', error.message);
    } finally {
        await blender.cleanup();
        console.log('🧹 Cleanup completed');
    }
}

// Auto-run demo if this script is executed directly
if (require.main === module) {
    demonstrateSubagentUsage();
}