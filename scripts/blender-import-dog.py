#!/usr/bin/env python3
"""
Blender Dog Import Script
Nutzt MCP um den Hund aus Blender zu exportieren und ins Spiel zu importieren
"""

import socket
import json
import time
import os
import shutil
from datetime import datetime
from pathlib import Path

class BlenderDogImporter:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9876
        self.project_root = Path('/Users/doriangrey/Desktop/coding/tierarztspiel')
        self.export_dir = self.project_root / 'watched_exports'
        self.target_dir = self.project_root / 'assets/models/animals/dog'
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def send_mcp_command(self, command):
        """Send command to Blender via MCP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            sock.connect((self.host, self.port))
            
            message = json.dumps(command) + '\n'
            sock.send(message.encode())
            
            response = sock.recv(8192).decode()
            sock.close()
            
            return json.loads(response) if response else None
        except Exception as e:
            print(f"❌ MCP Command failed: {e}")
            return None
    
    def get_scene_info(self):
        """Get current scene information from Blender"""
        print("\n📊 Getting Blender Scene Info...")
        
        command = {
            "method": "execute_blender_code",
            "params": {
                "code": """
import bpy
import json

# Sammle Scene-Informationen
scene_data = {
    'objects': [],
    'total_vertices': 0,
    'total_faces': 0,
    'materials': []
}

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj_info = {
            'name': obj.name,
            'vertices': len(obj.data.vertices),
            'faces': len(obj.data.polygons),
            'location': list(obj.location),
            'has_armature': any(mod.type == 'ARMATURE' for mod in obj.modifiers)
        }
        scene_data['objects'].append(obj_info)
        scene_data['total_vertices'] += obj_info['vertices']
        scene_data['total_faces'] += obj_info['faces']

# Materials sammeln
for mat in bpy.data.materials:
    if mat.users > 0:
        scene_data['materials'].append(mat.name)

print(json.dumps(scene_data, indent=2))
"""
            }
        }
        
        response = self.send_mcp_command(command)
        if response:
            print("✅ Scene Info received!")
            # Parse the printed JSON from Blender output
            try:
                # Response enthält den print output
                return response
            except:
                return response
        return None
    
    def identify_dog_object(self, scene_info):
        """Identify the dog object in the scene"""
        print("\n🔍 Identifying Dog Object...")
        
        if not scene_info:
            print("❌ No scene info available")
            return None
        
        # Suche nach Hund-ähnlichen Objekten
        dog_keywords = ['dog', 'hund', 'bello', 'canine', 'puppy', 'welpe']
        dog_object = None
        
        # Prüfe ob objects im response enthalten sind
        objects = scene_info.get('result', {}).get('objects', []) if isinstance(scene_info, dict) else []
        
        if not objects:
            # Fallback: Nehme das größte Mesh-Objekt
            command = {
                "method": "get_scene_info",
                "params": {}
            }
            response = self.send_mcp_command(command)
            if response:
                objects = response.get('result', {}).get('objects', [])
        
        for obj in objects:
            obj_name_lower = obj.get('name', '').lower()
            for keyword in dog_keywords:
                if keyword in obj_name_lower:
                    dog_object = obj
                    print(f"✅ Found dog object: {obj['name']}")
                    print(f"   - Vertices: {obj.get('vertices', 'unknown')}")
                    print(f"   - Faces: {obj.get('faces', 'unknown')}")
                    return obj
        
        # Wenn kein Hund gefunden, nimm das größte Objekt
        if not dog_object and objects:
            dog_object = max(objects, key=lambda x: x.get('vertices', 0))
            print(f"⚠️ No dog-named object found, using largest mesh: {dog_object.get('name')}")
            print(f"   - Vertices: {dog_object.get('vertices', 'unknown')}")
            print(f"   - Faces: {dog_object.get('faces', 'unknown')}")
        
        return dog_object
    
    def create_export_script(self, dog_object_name=None):
        """Create Blender export script for multi-quality versions"""
        print("\n📝 Creating Export Script...")
        
        # Wenn kein spezifisches Objekt, exportiere alles
        select_code = ""
        if dog_object_name:
            select_code = f"""
# Wähle nur den Hund
bpy.ops.object.select_all(action='DESELECT')
if '{dog_object_name}' in bpy.data.objects:
    bpy.data.objects['{dog_object_name}'].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects['{dog_object_name}']
"""
        
        export_script = f"""
import bpy
import os
from pathlib import Path

print("🐕 Starting Dog Export for VetScan Pro...")

# Export-Verzeichnis
export_dir = Path('{self.export_dir}')
export_dir.mkdir(exist_ok=True)

{select_code}

# Qualitätsstufen definieren
quality_levels = {{
    'high': {{'decimate': 1.0, 'texture_size': 2048}},
    'medium': {{'decimate': 0.5, 'texture_size': 1024}},
    'low': {{'decimate': 0.25, 'texture_size': 512}}
}}

# Original-Zustand speichern
original_objects = {{obj.name: obj.location.copy() for obj in bpy.context.selected_objects}}

for quality, settings in quality_levels.items():
    print(f"\\n📦 Exporting {{quality}} quality...")
    
    # Kopiere Objekte für diese Qualität
    for obj in list(bpy.context.selected_objects):
        if obj.type == 'MESH':
            # Decimate wenn nötig
            if settings['decimate'] < 1.0:
                # Füge Decimate Modifier hinzu
                decimate = obj.modifiers.new('DECIMATE_EXPORT', 'DECIMATE')
                decimate.ratio = settings['decimate']
    
    # Export-Pfad
    export_file = export_dir / f'dog_{{quality}}_{self.timestamp}.glb'
    
    # Export mit optimalen Settings
    bpy.ops.export_scene.gltf(
        filepath=str(export_file),
        export_format='GLB',
        use_selection=True if '{dog_object_name}' else False,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
        export_image_format='AUTO',
        export_texture_dir='',
        export_cameras=False,
        export_lights=False,
        export_apply=True,
        export_animations=True,
        export_frame_range=False,
        export_nla_strips=False,
        export_morph=True,
        export_skins=True,
        export_colors=True,
        export_attributes=True
    )
    
    print(f"✅ Exported: {{export_file.name}}")
    
    # Entferne temporäre Modifiers
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            for modifier in obj.modifiers:
                if 'DECIMATE_EXPORT' in modifier.name:
                    obj.modifiers.remove(modifier)

# Spezieller Medical Export mit Layern
print("\\n🏥 Exporting Medical Visualization Layers...")

# Medical Export (mit allen Layern für verschiedene Modi)
medical_file = export_dir / f'dog_medical_{self.timestamp}.glb'
bpy.ops.export_scene.gltf(
    filepath=str(medical_file),
    export_format='GLB',
    use_selection=False,  # Alles exportieren für medical
    export_draco_mesh_compression_enable=True
)

print(f"✅ Medical export complete: {{medical_file.name}}")
print("\\n🎉 All exports completed successfully!")
"""
        
        return export_script
    
    def execute_export(self, dog_object_name=None):
        """Execute the export script in Blender"""
        print("\n🚀 Executing Export in Blender...")
        
        export_script = self.create_export_script(dog_object_name)
        
        command = {
            "method": "execute_blender_code",
            "params": {
                "code": export_script
            }
        }
        
        response = self.send_mcp_command(command)
        if response:
            print("✅ Export command sent to Blender!")
            
            # Warte kurz auf Export-Completion
            time.sleep(3)
            
            # Prüfe ob Dateien erstellt wurden
            if self.check_exported_files():
                return True
        
        print("⚠️ Export might have failed, checking for files...")
        return self.check_exported_files()
    
    def check_exported_files(self):
        """Check if export files were created"""
        print("\n📁 Checking for exported files...")
        
        exported_files = []
        for file in self.export_dir.glob(f"dog_*_{self.timestamp}.glb"):
            exported_files.append(file)
            print(f"   ✅ Found: {file.name} ({file.stat().st_size / 1024:.1f} KB)")
        
        return len(exported_files) > 0
    
    def copy_to_game_assets(self):
        """Copy exported files to game assets directory"""
        print("\n📋 Copying to game assets...")
        
        # Erstelle Zielverzeichnis wenn nötig
        self.target_dir.mkdir(parents=True, exist_ok=True)
        
        copied_files = []
        for quality in ['high', 'medium', 'low', 'medical']:
            source_file = self.export_dir / f"dog_{quality}_{self.timestamp}.glb"
            if source_file.exists():
                target_file = self.target_dir / f"dog_{quality}.glb"
                shutil.copy2(source_file, target_file)
                print(f"   ✅ Copied: dog_{quality}.glb")
                copied_files.append(target_file)
                
                # Erstelle auch eine "latest" Version
                if quality == 'medium':
                    latest_file = self.target_dir / "dog_latest.glb"
                    shutil.copy2(source_file, latest_file)
                    print(f"   ✅ Created: dog_latest.glb (from medium)")
        
        return copied_files
    
    def create_manifest(self, dog_info):
        """Create a manifest file with model information"""
        manifest = {
            "name": "Dog Model",
            "source": "Blender Export",
            "timestamp": self.timestamp,
            "object_info": dog_info,
            "quality_levels": {
                "high": "dog_high.glb",
                "medium": "dog_medium.glb",
                "low": "dog_low.glb",
                "medical": "dog_medical.glb"
            },
            "medical_modes": [
                "normal",
                "xray",
                "ultrasound",
                "thermal",
                "mri"
            ]
        }
        
        manifest_file = self.target_dir / "dog_manifest.json"
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
        
        print(f"\n📄 Created manifest: {manifest_file.name}")
        return manifest_file
    
    def run_import_pipeline(self):
        """Run the complete import pipeline"""
        print("="*60)
        print("🐕 BLENDER DOG IMPORT PIPELINE")
        print("="*60)
        
        # 1. Get Scene Info
        scene_info = self.get_scene_info()
        
        # 2. Identify Dog Object
        dog_object = self.identify_dog_object(scene_info)
        dog_name = dog_object.get('name') if dog_object else None
        
        # 3. Execute Export
        export_success = self.execute_export(dog_name)
        
        if not export_success:
            print("\n⚠️ No files exported. Trying manual export approach...")
            print("Please run the export script manually in Blender:")
            print(f"1. Open Scripting tab")
            print(f"2. Load: scripts/blender_auto_export.py")
            print(f"3. Run Script")
            return False
        
        # 4. Copy to Game Assets
        copied_files = self.copy_to_game_assets()
        
        if not copied_files:
            print("❌ No files were copied to game assets")
            return False
        
        # 5. Create Manifest
        self.create_manifest(dog_object if dog_object else {})
        
        # Success!
        print("\n" + "="*60)
        print("🎉 DOG IMPORT COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\n📁 Files available at: {self.target_dir}")
        print("\n🌐 Test in browser:")
        print("   http://localhost:8080/vetscan-bello-3d-v7.html")
        print("\n🚀 Next steps:")
        print("   1. Start local server: python3 -m http.server 8080")
        print("   2. Open browser and test")
        print("   3. Deploy to production when ready")
        
        return True

if __name__ == "__main__":
    importer = BlenderDogImporter()
    success = importer.run_import_pipeline()
    exit(0 if success else 1)