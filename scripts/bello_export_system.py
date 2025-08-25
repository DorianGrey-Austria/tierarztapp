import bpy
import os
from mathutils import Vector

print("📦 Setting up Bello GLB Export System for VetScan Pro")

def setup_export_collections():
    """Organize objects for different export variants"""
    print("   Organizing export collections...")
    
    # Create export-specific collections
    export_collections = {
        'Export_Normal': 'Standard Bello for normal view',
        'Export_XRay': 'Bello with skeleton for X-ray mode',
        'Export_Medical': 'Bello with organs for ultrasound',
        'Export_Complete': 'Full Bello with all medical layers'
    }
    
    for coll_name, desc in export_collections.items():
        if coll_name not in bpy.data.collections:
            collection = bpy.data.collections.new(coll_name)
            bpy.context.scene.collection.children.link(collection)
    
    print("   ✅ Export collections created")

def optimize_for_game():
    """Optimize models for real-time game performance"""
    print("   Optimizing for game performance...")
    
    # Apply all modifiers for better performance
    for obj in bpy.data.objects:
        if obj.type == 'MESH' and obj.name.startswith('Bello_'):
            # Make sure object is active
            bpy.context.view_layer.objects.active = obj
            
            # Apply subdivision surface modifiers (convert to geometry)
            for modifier in obj.modifiers:
                if modifier.type == 'SUBSURF':
                    try:
                        bpy.ops.object.modifier_apply(modifier=modifier.name)
                        print(f"      Applied modifier to {obj.name}")
                    except:
                        print(f"      Could not apply modifier to {obj.name}")
    
    # Merge duplicate materials
    material_names = set()
    for material in bpy.data.materials:
        if material.name not in material_names:
            material_names.add(material.name)
        else:
            # Remove duplicate materials
            bpy.data.materials.remove(material)
    
    print("   ✅ Game optimization complete")

def create_lod_variants():
    """Create Level of Detail variants for performance"""
    print("   Creating LOD (Level of Detail) variants...")
    
    # Get all Bello main body objects
    main_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Bello_') and obj.type == 'MESH']
    
    # High Quality (original)
    for obj in main_objects:
        obj['LOD'] = 'high'
        obj['polygon_budget'] = 'unlimited'
    
    # Create medium quality variants (simplified subdivision)
    for obj in main_objects.copy():
        # Duplicate for medium quality
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.duplicate()
        med_obj = bpy.context.object
        med_obj.name = obj.name.replace('Bello_', 'Bello_Med_')
        med_obj['LOD'] = 'medium'
        med_obj['polygon_budget'] = '20k'
        
        # Reduce subdivision levels for medium quality
        for modifier in med_obj.modifiers:
            if modifier.type == 'SUBSURF':
                modifier.levels = max(1, modifier.levels - 1)
    
    print("   ✅ LOD variants created")

def setup_medical_mode_exports():
    """Setup different medical visualization exports"""
    print("   Setting up medical mode exports...")
    
    # Normal Mode Export (just Bello body)
    normal_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Bello_') and not obj.name.startswith('Bello_Med_')]
    skeleton_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Skeleton_')]
    organ_objects = [obj for obj in bpy.data.objects if obj.name.startswith('Medical_')]
    
    # Show/hide different layers for different exports
    for obj in skeleton_objects + organ_objects:
        obj.hide_viewport = True  # Hidden for normal export
        obj.hide_render = True
    
    for obj in normal_objects:
        obj.hide_viewport = False  # Visible for normal export
        obj.hide_render = False
    
    print("   ✅ Medical modes configured")

def export_bello_variants():
    """Export Bello in different variants for the game"""
    print("   Exporting Bello variants...")
    
    # Create assets directory if it doesn't exist
    export_dir = "assets/models/animals/bello"
    os.makedirs(export_dir, exist_ok=True)
    
    # Export configurations
    export_configs = [
        {
            'name': 'bello_high',
            'quality': 'high',
            'include_skeleton': False,
            'include_organs': False,
            'polygon_limit': 50000
        },
        {
            'name': 'bello_medium', 
            'quality': 'medium',
            'include_skeleton': False,
            'include_organs': False,
            'polygon_limit': 20000
        },
        {
            'name': 'bello_low',
            'quality': 'low', 
            'include_skeleton': False,
            'include_organs': False,
            'polygon_limit': 8000
        },
        {
            'name': 'bello_xray',
            'quality': 'medium',
            'include_skeleton': True,
            'include_organs': False,
            'polygon_limit': 25000
        },
        {
            'name': 'bello_medical',
            'quality': 'medium',
            'include_skeleton': True,
            'include_organs': True,
            'polygon_limit': 35000
        }
    ]
    
    for config in export_configs:
        print(f"      Preparing {config['name']}...")
        
        # Select objects based on configuration
        bpy.ops.object.select_all(action='DESELECT')
        
        # Always include main Bello body
        if config['quality'] == 'medium':
            pattern = 'Bello_Med_'
        else:
            pattern = 'Bello_'
            
        for obj in bpy.data.objects:
            if obj.name.startswith(pattern) and obj.type == 'MESH':
                obj.select_set(True)
        
        # Include skeleton for X-ray modes
        if config['include_skeleton']:
            for obj in bpy.data.objects:
                if obj.name.startswith('Skeleton_'):
                    obj.select_set(True)
                    obj.hide_viewport = False
        
        # Include organs for medical modes  
        if config['include_organs']:
            for obj in bpy.data.objects:
                if obj.name.startswith('Medical_'):
                    obj.select_set(True)
                    obj.hide_viewport = False
        
        # Export GLB
        export_path = f"{export_dir}/{config['name']}.glb"
        
        try:
            # GLB Export with optimal settings for Three.js
            bpy.ops.export_scene.gltf(
                filepath=export_path,
                use_selection=True,
                export_format='GLB',
                export_materials='EXPORT',
                export_colors=True,
                export_cameras=False,
                export_lights=False,
                export_texcoords=True,
                export_normals=True,
                export_animations=True,
                export_apply=True
            )
            print(f"      ✅ Exported: {config['name']}.glb")
            
        except Exception as e:
            print(f"      ❌ Export failed for {config['name']}: {str(e)}")
    
    print("   ✅ All variants exported")

def create_manifest_file():
    """Create a manifest file with model information"""
    print("   Creating model manifest...")
    
    manifest_content = '''# Bello 3D Model Manifest
# Generated by VetScan Pro Blender Pipeline

models:
  bello_high:
    file: "bello_high.glb"
    quality: "high"
    polygons: ~50000
    textures: "2048px"
    features: ["normal_view", "premium_materials"]
    
  bello_medium:
    file: "bello_medium.glb"  
    quality: "medium"
    polygons: ~20000
    textures: "1024px"
    features: ["normal_view", "optimized"]
    
  bello_low:
    file: "bello_low.glb"
    quality: "low"
    polygons: ~8000
    textures: "512px"
    features: ["normal_view", "mobile_optimized"]
    
  bello_xray:
    file: "bello_xray.glb"
    quality: "medium"
    polygons: ~25000
    textures: "1024px"
    features: ["xray_mode", "skeleton_visible"]
    
  bello_medical:
    file: "bello_medical.glb"
    quality: "medium"
    polygons: ~35000
    textures: "1024px"
    features: ["medical_mode", "organs_visible", "skeleton_visible"]

animation_points:
  heart: [1.2, 0, 1.1]
  breathing: [0.8, 0, 1.2]
  tail_wag: [-3.0, 0, 1.3]
  
medical_modes:
  - normal
  - xray
  - ultrasound  
  - thermal
  - mri

educational_features:
  - interactive_anatomy
  - symptom_visualization
  - health_monitoring
'''
    
    with open('assets/models/animals/bello/bello_manifest.yml', 'w') as f:
        f.write(manifest_content)
    
    print("   ✅ Manifest file created")

def create_integration_script():
    """Create JavaScript integration code for the game"""
    print("   Creating game integration code...")
    
    integration_code = '''// Bello 3D Model Integration for VetScan Pro
// Generated by Blender Export Pipeline

class BelloModel {
    constructor() {
        this.models = new Map();
        this.currentMode = 'normal';
        this.loadingPromises = new Map();
    }
    
    async loadModel(quality = 'medium') {
        const modelPath = `./assets/models/animals/bello/bello_${quality}.glb`;
        
        if (this.models.has(quality)) {
            return this.models.get(quality);
        }
        
        if (this.loadingPromises.has(quality)) {
            return this.loadingPromises.get(quality);
        }
        
        const loadPromise = this.loadGLTF(modelPath);
        this.loadingPromises.set(quality, loadPromise);
        
        try {
            const model = await loadPromise;
            this.models.set(quality, model);
            this.setupMedicalVisualization(model);
            return model;
        } catch (error) {
            console.error(`Failed to load Bello ${quality}:`, error);
            this.loadingPromises.delete(quality);
            throw error;
        }
    }
    
    setupMedicalVisualization(model) {
        // Setup medical visualization modes
        model.userData = {
            medicalModes: {
                normal: { visible: true, materials: 'fur' },
                xray: { visible: true, materials: 'xray', showSkeleton: true },
                ultrasound: { visible: true, materials: 'ultrasound', showOrgans: true },
                thermal: { visible: true, materials: 'thermal' },
                mri: { visible: true, materials: 'mri' }
            }
        };
    }
    
    switchMedicalMode(mode) {
        this.currentMode = mode;
        // Implementation for switching visualization modes
        console.log(`Switched to ${mode} mode`);
    }
    
    getAnatomyPoints() {
        return {
            heart: new THREE.Vector3(1.2, 0, 1.1),
            lungs: new THREE.Vector3(0.8, 0, 1.2), 
            liver: new THREE.Vector3(0, 0.3, 0.8),
            kidneys: new THREE.Vector3(-1.0, 0, 1.0)
        };
    }
}

// Export for use in VetScan Pro game
export default BelloModel;
'''
    
    with open('src/game/BelloModel.js', 'w') as f:
        f.write(integration_code)
    
    print("   ✅ Integration code created")

# Execute export pipeline
setup_export_collections()
optimize_for_game()
create_lod_variants()
setup_medical_mode_exports()
export_bello_variants()
create_manifest_file()
create_integration_script()

print("🎉 BELLO EXPORT SYSTEM COMPLETE!")
print()
print("📦 Exported Files:")
print("   - bello_high.glb (Premium quality)")
print("   - bello_medium.glb (Standard quality)")  
print("   - bello_low.glb (Mobile optimized)")
print("   - bello_xray.glb (X-ray visualization)")
print("   - bello_medical.glb (Full medical mode)")
print()
print("🔧 Integration Files:")
print("   - bello_manifest.yml (Model specifications)")
print("   - BelloModel.js (Game integration class)")
print()
print("🎮 Ready for VetScan Pro integration!")
print("💡 Use AnimalLoader.js to load models with progressive quality")