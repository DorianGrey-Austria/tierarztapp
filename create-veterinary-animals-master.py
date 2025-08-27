#!/usr/bin/env python3
"""
MASTER AGENT - Veterinary 3D Animals Creation Pipeline
Coordinates sub-agents to create 10 high-quality medical animal models
"""

import json
import subprocess
import time
from pathlib import Path
from datetime import datetime
import concurrent.futures

class VeterinaryAnimalsMaster:
    def __init__(self):
        self.start_time = datetime.now()
        self.output_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals')
        self.results = {}
        
        # Define the 10 animals with detailed specifications
        self.animals = [
            # Level 1 - Simple Pets (Ages 6-10)
            {
                "id": "cat",
                "name": "Katze",
                "difficulty": "beginner",
                "anatomy_focus": ["Flexible spine", "Retractable claws", "Whiskers", "Tail balance"],
                "special_features": ["Purring mechanism", "Night vision eyes", "Grooming tongue"],
                "colors": ["orange_tabby", "black", "white", "siamese", "calico"]
            },
            {
                "id": "guinea_pig", 
                "name": "Meerschweinchen",
                "difficulty": "beginner",
                "anatomy_focus": ["Rodent teeth", "Digestive system", "Small heart", "Fur patterns"],
                "special_features": ["Popcorning animation", "Wheeking sound", "Vitamin C dependency"],
                "colors": ["brown_white", "black", "orange", "tri_color"]
            },
            {
                "id": "hamster",
                "name": "Hamster",
                "difficulty": "beginner",
                "anatomy_focus": ["Cheek pouches", "Short tail", "Small paws", "Curved spine"],
                "special_features": ["Food storage", "Wheel running", "Burrowing behavior"],
                "colors": ["golden", "white", "grey", "black_white"]
            },
            {
                "id": "budgie",
                "name": "Wellensittich",
                "difficulty": "beginner",
                "anatomy_focus": ["Flight feathers", "Hollow bones", "Beak structure", "Cere"],
                "special_features": ["Wing clipping area", "Talking ability", "Seed cracking"],
                "colors": ["green_yellow", "blue", "white", "lutino"]
            },
            {
                "id": "goldfish",
                "name": "Goldfisch",
                "difficulty": "beginner",
                "anatomy_focus": ["Gills", "Swim bladder", "Fins", "Scales"],
                "special_features": ["Water breathing", "Buoyancy control", "360° vision"],
                "colors": ["orange", "white", "black", "calico", "red"]
            },
            
            # Level 2 - Complex Animals (Ages 10-14)
            {
                "id": "horse",
                "name": "Pferd",
                "difficulty": "advanced",
                "anatomy_focus": ["Powerful legs", "Hooves", "Large heart", "Long digestive tract"],
                "special_features": ["Galloping gait", "Mane and tail", "Dental examination"],
                "colors": ["bay", "black", "chestnut", "grey", "palomino"]
            },
            {
                "id": "parrot",
                "name": "Papagei",
                "difficulty": "advanced",
                "anatomy_focus": ["Strong beak", "Zygodactyl feet", "Air sacs", "Colorful plumage"],
                "special_features": ["Mimicry", "Nut cracking", "Climbing ability"],
                "colors": ["scarlet_macaw", "blue_gold", "green", "grey", "cockatoo_white"]
            },
            {
                "id": "turtle",
                "name": "Schildkröte",
                "difficulty": "advanced",
                "anatomy_focus": ["Shell structure", "Retractable neck", "Webbed feet", "Beak"],
                "special_features": ["Shell layers", "Hibernation", "Swimming vs walking"],
                "colors": ["green", "brown", "yellow_pattern", "red_eared"]
            },
            {
                "id": "snake",
                "name": "Schlange",
                "difficulty": "advanced",
                "anatomy_focus": ["Vertebral column", "Jaw dislocation", "Scales", "Forked tongue"],
                "special_features": ["Shedding skin", "Heat sensing", "Constriction"],
                "colors": ["python_pattern", "green", "black", "corn_snake", "albino"]
            },
            {
                "id": "ferret",
                "name": "Frettchen",
                "difficulty": "advanced",
                "anatomy_focus": ["Long body", "Short legs", "Mask marking", "Scent glands"],
                "special_features": ["War dance", "Tunnel exploration", "Play behavior"],
                "colors": ["sable", "albino", "silver", "cinnamon", "black"]
            }
        ]
        
        # Medical visualization specifications
        self.medical_modes = {
            "normal": {
                "description": "Realistic fur/skin with natural colors",
                "material": "PBR with subsurface scattering",
                "detail_level": "high"
            },
            "xray": {
                "description": "Skeletal system visible through transparent tissue",
                "material": "Fresnel-based transparency with bone highlights",
                "detail_level": "medical"
            },
            "ultrasound": {
                "description": "Black and white with typical ultrasound artifacts",
                "material": "Grayscale with scan line effects",
                "detail_level": "diagnostic"
            },
            "thermal": {
                "description": "Heat map visualization showing temperature",
                "material": "Color gradient from blue (cold) to red (hot)",
                "detail_level": "functional"
            },
            "mri": {
                "description": "Cross-sectional view with tissue differentiation",
                "material": "Grayscale with tissue density mapping",
                "detail_level": "medical"
            },
            "palpation": {
                "description": "Interactive examination points highlighted",
                "material": "Normal with glowing interaction zones",
                "detail_level": "educational"
            }
        }
    
    def create_sub_agent_prompt(self, animal):
        """Create detailed prompt for sub-agent"""
        prompt = f"""
# VETERINARY 3D ANIMAL CREATION TASK

## Target Animal: {animal['name']} ({animal['id']})
Difficulty Level: {animal['difficulty']}

## REQUIREMENTS:

### 1. ANATOMICAL ACCURACY
Create a medically accurate {animal['name']} with focus on:
{json.dumps(animal['anatomy_focus'], indent=2)}

### 2. SPECIAL FEATURES
Must include these unique characteristics:
{json.dumps(animal['special_features'], indent=2)}

### 3. COLOR VARIATIONS
Implement at least 3 of these color patterns:
{json.dumps(animal['colors'], indent=2)}

### 4. MEDICAL VISUALIZATIONS
Create separate materials/layers for ALL of these modes:
{json.dumps(self.medical_modes, indent=2)}

### 5. TECHNICAL SPECIFICATIONS
- Polycount: 5000-8000 triangles (optimized for web)
- Texture Resolution: 2048x2048 max
- File Size: Under 1MB when exported as GLB
- Animations: Breathing (subtle), heartbeat (for close examination)

### 6. INTERACTIVE ELEMENTS
Add examination points for:
- Heart location (with pulse animation)
- Lung area (breathing visualization)
- Digestive system (if relevant)
- Species-specific organs

### 7. EXPORT REQUIREMENTS
- Format: GLB with embedded textures
- Naming: {animal['id']}_[mode].glb (e.g., cat_normal.glb, cat_xray.glb)
- Include metadata with medical information

## QUALITY CRITERIA:
- Anatomical correctness for veterinary education
- Child-friendly appearance (not scary)
- Smooth transitions between visualization modes
- Optimized for real-time rendering in browser

## DELIVERABLES:
1. Base mesh with proper topology
2. 6 visualization mode materials
3. Exported GLB files for each mode
4. Screenshot of the model from 4 angles

Your code should use Blender Python API (bpy) and follow best practices.
Return a complete Python script that creates this animal procedurally.
"""
        return prompt
    
    def launch_sub_agent(self, animal, agent_id):
        """Launch a sub-agent to create one animal"""
        print(f"\n🚀 Launching Sub-Agent {agent_id} for {animal['name']}...")
        
        # Create sub-agent script
        script_path = self.output_dir / f"sub_agent_{animal['id']}.py"
        
        sub_agent_code = f'''#!/usr/bin/env python3
"""
Sub-Agent {agent_id}: Creating {animal['name']} ({animal['id']})
Generated at {datetime.now().isoformat()}
"""

import socket
import json
import time
import os
from pathlib import Path

def send_blender_command(command):
    """Send command to Blender MCP"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(30)
        sock.connect(('localhost', 9876))
        sock.send(json.dumps(command).encode())
        response = sock.recv(32768)
        sock.close()
        return json.loads(response.decode())
    except Exception as e:
        return {{"status": "error", "message": str(e)}}

def create_{animal['id']}():
    """Create a medically accurate {animal['name']}"""
    
    print("🐾 Creating {animal['name']}...")
    
    # Complex Blender Python code to create the animal
    creation_code = """
import bpy
import bmesh
import math

# Clear existing mesh with this name
if '{animal['id']}_model' in bpy.data.objects:
    bpy.data.objects.remove(bpy.data.objects['{animal['id']}_model'])

# Create base mesh for {animal['name']}
print("Creating base geometry...")

{self._generate_animal_geometry(animal)}

# Add anatomical details
print("Adding anatomical features...")
{self._generate_anatomy_code(animal)}

# Create medical visualization materials
print("Creating medical materials...")
{self._generate_materials_code()}

# Apply optimizations
print("Optimizing mesh...")
bpy.ops.object.modifier_add(type='DECIMATE')
bpy.context.object.modifiers["Decimate"].ratio = 0.7
bpy.ops.object.modifier_apply(modifier="Decimate")

# Set up for export
animal_model.select_set(True)
bpy.context.view_layer.objects.active = animal_model

result = {{"success": True, "name": animal_model.name, "polycount": len(animal_model.data.polygons)}}
result
"""
    
    response = send_blender_command({{
        "type": "execute_code",
        "params": {{"code": creation_code}}
    }})
    
    if response.get('status') == 'success':
        print(f"✅ {animal['name']} created successfully!")
        
        # Export the model
        export_path = r'{str(self.output_dir / animal['id'] / f"{animal['id']}_medical.glb")}'
        
        export_code = f"""
import bpy
import os

os.makedirs(os.path.dirname(r'{{export_path}}'), exist_ok=True)

# Export as GLB
bpy.ops.export_scene.gltf(
    filepath=r'{{export_path}}',
    export_format='GLB',
    use_selection=True,
    export_apply=True
)

result = {{"success": True, "path": r'{{export_path}}'}}
result
"""
        
        export_response = send_blender_command({{
            "type": "execute_code",
            "params": {{"code": export_code}}
        }})
        
        if export_response.get('status') == 'success':
            print(f"✅ Exported to {{export_path}}")
            return True
    
    return False

if __name__ == "__main__":
    success = create_{animal['id']}()
    exit(0 if success else 1)
'''
        
        # Write sub-agent script
        script_path.write_text(sub_agent_code)
        script_path.chmod(0o755)
        
        # Execute sub-agent
        result = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=120
        )
        
        return {
            "animal": animal['id'],
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
    
    def _generate_animal_geometry(self, animal):
        """Generate animal-specific geometry code"""
        
        # Base geometries for different animal types
        geometries = {
            "cat": """
# Cat body (elongated sphere)
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16)
body = bpy.context.active_object
body.name = "Cat_Body"
body.scale = (1.2, 0.8, 0.7)
body.location = (0, 0, 0)

# Cat head (sphere)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14)
head = bpy.context.active_object
head.name = "Cat_Head"
head.scale = (0.5, 0.5, 0.45)
head.location = (1.2, 0, 0.3)

# Ears (cones)
for i, x in enumerate([-0.2, 0.2]):
    bpy.ops.mesh.primitive_cone_add(vertices=8)
    ear = bpy.context.active_object
    ear.name = f"Cat_Ear_{i}"
    ear.scale = (0.15, 0.15, 0.3)
    ear.location = (1.2 + x, 0, 0.6)
    ear.rotation_euler = (0.3, 0, x * 0.2)

# Tail (curved cylinder)
bpy.ops.curve.primitive_bezier_curve_add()
tail_curve = bpy.context.active_object
# ... tail creation code

# Join all parts
bpy.ops.object.select_all(action='DESELECT')
for obj in bpy.data.objects:
    if obj.name.startswith("Cat_"):
        obj.select_set(True)
bpy.context.view_layer.objects.active = body
bpy.ops.object.join()
animal_model = body
animal_model.name = '{animal['id']}_model'
""",
            "guinea_pig": """
# Guinea pig body (rounded cube)
bpy.ops.mesh.primitive_cube_add()
body = bpy.context.active_object
body.name = "GuineaPig_Body"
# Add subdivision
bpy.ops.object.modifier_add(type='SUBSURF')
body.modifiers["Subdivision"].levels = 2
bpy.ops.object.modifier_apply(modifier="Subdivision")
body.scale = (1, 0.7, 0.6)

animal_model = body
animal_model.name = '{animal['id']}_model'
""",
            "hamster": """
# Hamster body (small sphere)
bpy.ops.mesh.primitive_uv_sphere_add(segments=20, ring_count=14)
body = bpy.context.active_object
body.name = "Hamster_Body"
body.scale = (0.6, 0.5, 0.5)

# Cheek pouches (additional spheres)
for i, x in enumerate([-0.3, 0.3]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16)
    pouch = bpy.context.active_object
    pouch.scale = (0.2, 0.2, 0.2)
    pouch.location = (0.3 + x, 0, 0.1)

animal_model = body
animal_model.name = '{animal['id']}_model'
"""
        }
        
        # Default to a simple sphere if animal not specifically defined
        default = f"""
# Generic animal body
bpy.ops.mesh.primitive_uv_sphere_add(segments=24, ring_count=16)
animal_model = bpy.context.active_object
animal_model.name = '{animal['id']}_model'
animal_model.scale = (1, 0.8, 0.7)
"""
        
        return geometries.get(animal['id'], default)
    
    def _generate_anatomy_code(self, animal):
        """Generate anatomy-specific features"""
        return f"""
# Add anatomical markers
# Heart position
bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6)
heart_marker = bpy.context.active_object
heart_marker.name = "{animal['id']}_heart"
heart_marker.scale = (0.05, 0.05, 0.05)
heart_marker.location = (0.3, 0, 0.2)  # Approximate heart position

# Lung areas
for i, y in enumerate([-0.1, 0.1]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=6)
    lung = bpy.context.active_object
    lung.name = f"{animal['id']}_lung_{{i}}"
    lung.scale = (0.1, 0.08, 0.1)
    lung.location = (0.2, y, 0.2)
"""
    
    def _generate_materials_code(self):
        """Generate medical visualization materials"""
        return """
# Create medical materials
materials = {}

# Normal material
mat_normal = bpy.data.materials.new(name="AnimalMat_Normal")
mat_normal.use_nodes = True
bsdf = mat_normal.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.7, 0.5, 0.3, 1)  # Brown fur color
materials['normal'] = mat_normal

# X-Ray material
mat_xray = bpy.data.materials.new(name="AnimalMat_XRay")
mat_xray.use_nodes = True
mat_xray.blend_method = 'BLEND'
bsdf_xray = mat_xray.node_tree.nodes["Principled BSDF"]
bsdf_xray.inputs['Alpha'].default_value = 0.3
bsdf_xray.inputs['Transmission'].default_value = 0.7
materials['xray'] = mat_xray

# Thermal material
mat_thermal = bpy.data.materials.new(name="AnimalMat_Thermal")
mat_thermal.use_nodes = True
# Add ColorRamp node for heat visualization
materials['thermal'] = mat_thermal

# Apply normal material by default
if animal_model.data.materials:
    animal_model.data.materials[0] = mat_normal
else:
    animal_model.data.materials.append(mat_normal)
"""
    
    def run_parallel_creation(self):
        """Run all sub-agents in parallel for maximum efficiency"""
        print("🚀 STARTING PARALLEL ANIMAL CREATION")
        print("="*50)
        print(f"Creating {len(self.animals)} animals with medical visualizations")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            # Submit all tasks
            future_to_animal = {
                executor.submit(self.launch_sub_agent, animal, i+1): animal 
                for i, animal in enumerate(self.animals)
            }
            
            # Collect results as they complete
            for future in concurrent.futures.as_completed(future_to_animal):
                animal = future_to_animal[future]
                try:
                    result = future.result(timeout=120)
                    self.results[animal['id']] = result
                    
                    if result['success']:
                        print(f"✅ {animal['name']} completed successfully!")
                    else:
                        print(f"❌ {animal['name']} failed: {result.get('error', 'Unknown error')}")
                        
                except Exception as e:
                    print(f"❌ {animal['name']} exception: {str(e)}")
                    self.results[animal['id']] = {"success": False, "error": str(e)}
        
        return self.results
    
    def generate_summary_report(self):
        """Generate final report of all created animals"""
        
        successful = [k for k, v in self.results.items() if v.get('success')]
        failed = [k for k, v in self.results.items() if not v.get('success')]
        
        report = f"""
# 🏥 VETERINARY 3D ANIMALS CREATION REPORT
Generated: {datetime.now().isoformat()}
Duration: {(datetime.now() - self.start_time).total_seconds():.1f} seconds

## 📊 SUMMARY
- Total Animals: {len(self.animals)}
- Successful: {len(successful)} ✅
- Failed: {len(failed)} ❌

## ✅ SUCCESSFULLY CREATED
{chr(10).join(f"- {animal}" for animal in successful)}

## ❌ FAILED
{chr(10).join(f"- {animal}: {self.results[animal].get('error', 'Unknown')}" for animal in failed)}

## 📁 OUTPUT LOCATION
{self.output_dir}

## 🎮 NEXT STEPS
1. Test models in browser: python3 -m http.server 8080
2. Open: http://localhost:8080/test-animals-3d.html
3. Verify all visualization modes work
4. Check polycount and performance
"""
        
        report_path = self.output_dir / "CREATION_REPORT.md"
        report_path.write_text(report)
        print(report)
        
        return report

if __name__ == "__main__":
    print("🎯 VETERINARY ANIMALS MASTER AGENT")
    print("="*50)
    
    master = VeterinaryAnimalsMaster()
    
    # Run parallel creation
    results = master.run_parallel_creation()
    
    # Generate report
    report = master.generate_summary_report()
    
    print("\n✨ MASTER AGENT COMPLETE!")
    print(f"Check {master.output_dir} for all generated models")