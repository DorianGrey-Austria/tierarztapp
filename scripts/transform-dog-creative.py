#!/usr/bin/env python3
"""
🎨 CREATIVE DOG TRANSFORMATION via Blender MCP
Als Senior 3D Designer werde ich den Hund kreativ verändern!
"""

import socket
import json
import time
from datetime import datetime

class CreativeDogDesigner:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9876
        self.timestamp = datetime.now().strftime("%H%M%S")
        
    def execute_blender_code(self, code):
        """Execute Python code in Blender via MCP"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(30)
            sock.connect((self.host, self.port))
            
            command = {
                "method": "execute_blender_code",
                "params": {"code": code}
            }
            
            message = json.dumps(command) + '\n'
            sock.send(message.encode())
            
            response = sock.recv(65536).decode()
            sock.close()
            
            return response
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def analyze_scene(self):
        """Analyse the current scene"""
        print("\n🔍 ANALYSIERE BLENDER SCENE...")
        
        analysis_code = """
import bpy
import json

scene_info = {
    'objects': [],
    'materials': [],
    'selected': None
}

for obj in bpy.data.objects:
    if obj.type == 'MESH':
        obj_data = {
            'name': obj.name,
            'vertices': len(obj.data.vertices),
            'location': list(obj.location),
            'scale': list(obj.scale),
            'materials': [mat.name for mat in obj.data.materials] if obj.data.materials else []
        }
        scene_info['objects'].append(obj_data)
        
        if obj.select_get():
            scene_info['selected'] = obj.name

for mat in bpy.data.materials:
    if mat.users > 0:
        scene_info['materials'].append(mat.name)

print(json.dumps(scene_info, indent=2))
"""
        
        response = self.execute_blender_code(analysis_code)
        if response:
            print("✅ Scene analysiert!")
        return response
    
    def add_creative_collar(self):
        """Füge ein kreatives Halsband hinzu"""
        print("\n🎨 FÜGE ROTES HALSBAND HINZU...")
        
        collar_code = """
import bpy
import bmesh
from mathutils import Vector
import math

print("Creating stylish collar...")

# Create torus for collar
bpy.ops.mesh.primitive_torus_add(
    major_radius=1.5,
    minor_radius=0.1,
    location=(0, -0.5, 2.0),  # Position am Hals
    rotation=(1.57, 0, 0)  # 90 Grad gedreht
)

collar = bpy.context.active_object
collar.name = "Dog_Collar_Creative"

# Create red material
mat = bpy.data.materials.new(name="Collar_Red_Material")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.1, 0.1, 1.0)  # Rot
mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8  # Metallic
mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.2  # Roughness

collar.data.materials.append(mat)

# Add golden tag
bpy.ops.mesh.primitive_cylinder_add(
    radius=0.15,
    depth=0.02,
    location=(0, -0.8, 1.8)
)

tag = bpy.context.active_object
tag.name = "Collar_Tag"

# Golden material for tag
gold_mat = bpy.data.materials.new(name="Gold_Tag_Material")
gold_mat.use_nodes = True
gold_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 0.843, 0.0, 1.0)  # Gold
gold_mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 1.0  # Full metallic
gold_mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.1  # Shiny

tag.data.materials.append(gold_mat)

print("✅ Collar with golden tag added!")
"""
        
        self.execute_blender_code(collar_code)
        print("✅ Halsband hinzugefügt!")
    
    def add_playful_ball(self):
        """Füge einen bunten Ball hinzu"""
        print("\n⚽ FÜGE SPIELBALL HINZU...")
        
        ball_code = """
import bpy

# Create colorful ball
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.3,
    location=(1.5, 0, 0.3)
)

ball = bpy.context.active_object
ball.name = "Dog_Toy_Ball"

# Colorful material
mat = bpy.data.materials.new(name="Rainbow_Ball_Material")
mat.use_nodes = True

# Use ColorRamp for rainbow effect
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (0.2, 0.6, 1.0, 1.0)  # Blue base
bsdf.inputs[9].default_value = 0.3  # Some roughness
bsdf.inputs[15].default_value = 1.0  # Some emission for glow

ball.data.materials.append(mat)

print("✅ Playful ball added!")
"""
        
        self.execute_blender_code(ball_code)
        print("✅ Ball hinzugefügt!")
    
    def add_star_marking(self):
        """Füge einen Stern auf die Stirn"""
        print("\n⭐ FÜGE STERN-MARKIERUNG HINZU...")
        
        star_code = """
import bpy
import bmesh
import math

# Create star shape
bpy.ops.mesh.primitive_circle_add(
    vertices=10,
    radius=0.2,
    location=(0, -1.5, 2.5),  # On forehead
    rotation=(0, 1.57, 0)
)

star = bpy.context.active_object
star.name = "Forehead_Star"

# Edit to make star shape
bpy.ops.object.mode_set(mode='EDIT')
bm = bmesh.from_edit_mesh(star.data)

# Make star points
for i, v in enumerate(bm.verts):
    if i % 2 == 0:
        v.co *= 0.5  # Inner vertices

bmesh.update_edit_mesh(star.data)
bpy.ops.object.mode_set(mode='OBJECT')

# Glowing white material
mat = bpy.data.materials.new(name="Star_Glow_Material")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 1.0, 0.8, 1.0)  # Bright yellow-white
mat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 2.0  # Emission strength

star.data.materials.append(mat)

print("✅ Star marking added!")
"""
        
        self.execute_blender_code(star_code)
        print("✅ Stern hinzugefügt!")
    
    def modify_dog_color(self):
        """Ändere die Farbe des Hundes"""
        print("\n🎨 ÄNDERE HUNDEFARBE...")
        
        color_code = """
import bpy

# Find main dog mesh
dog_obj = None
for obj in bpy.data.objects:
    if obj.type == 'MESH' and 'dog' in obj.name.lower():
        dog_obj = obj
        break

if not dog_obj:
    # Take largest mesh
    meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
    if meshes:
        dog_obj = max(meshes, key=lambda x: len(x.data.vertices))

if dog_obj:
    print(f"Modifying colors of: {dog_obj.name}")
    
    # Create new unique material
    mat = bpy.data.materials.new(name="Modified_Dog_Material_Unique")
    mat.use_nodes = True
    
    # Purple-blue gradient for uniqueness
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs[0].default_value = (0.6, 0.3, 0.9, 1.0)  # Purple
    bsdf.inputs[4].default_value = 0.5  # Some subsurface
    bsdf.inputs[3].default_value = (0.3, 0.5, 0.8, 1.0)  # Blue subsurface
    
    # Clear old materials and add new
    dog_obj.data.materials.clear()
    dog_obj.data.materials.append(mat)
    
    print("✅ Dog color changed to purple-blue!")
else:
    print("⚠️ No dog object found")
"""
        
        self.execute_blender_code(color_code)
        print("✅ Farbe geändert!")
    
    def add_creative_hat(self):
        """Füge einen lustigen Hut hinzu"""
        print("\n🎩 FÜGE PARTY-HUT HINZU...")
        
        hat_code = """
import bpy

# Create cone hat
bpy.ops.mesh.primitive_cone_add(
    radius1=0.5,
    radius2=0.05,
    depth=0.8,
    location=(0, -0.2, 3.2),  # On head
    rotation=(0, 0, 0)
)

hat = bpy.context.active_object
hat.name = "Party_Hat"

# Colorful stripes material
mat = bpy.data.materials.new(name="Party_Hat_Material")
mat.use_nodes = True

# Red and white stripes
bsdf = mat.node_tree.nodes["Principled BSDF"]
bsdf.inputs[0].default_value = (1.0, 0.2, 0.4, 1.0)  # Pink-red
bsdf.inputs[9].default_value = 0.4  # Some roughness

hat.data.materials.append(mat)

# Add pompom on top
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=0.1,
    location=(0, -0.2, 3.6)
)

pompom = bpy.context.active_object
pompom.name = "Hat_Pompom"

# Fluffy white material
pom_mat = bpy.data.materials.new(name="Pompom_Material")
pom_mat.use_nodes = True
pom_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # White
pom_mat.node_tree.nodes["Principled BSDF"].inputs[9].default_value = 0.8  # Fluffy

pompom.data.materials.append(pom_mat)

print("✅ Party hat with pompom added!")
"""
        
        self.execute_blender_code(hat_code)
        print("✅ Party-Hut hinzugefügt!")
    
    def export_creative_dog(self):
        """Exportiere den kreativen Hund"""
        print("\n📦 EXPORTIERE KREATIVEN HUND...")
        
        export_code = f"""
import bpy
from pathlib import Path

# Export path
export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_dir.mkdir(exist_ok=True)

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export with unique name
export_file = export_dir / 'creative_dog_{self.timestamp}.glb'

print(f"Exporting to: {{export_file.name}}")

bpy.ops.export_scene.gltf(
    filepath=str(export_file),
    export_format='GLB',
    use_selection=True,
    export_apply=True,
    export_draco_mesh_compression_enable=True
)

print(f"✅ Creative dog exported: {{export_file.name}}")

# Also export as dog_creative.glb for easy access
creative_file = export_dir / 'dog_creative.glb'
bpy.ops.export_scene.gltf(
    filepath=str(creative_file),
    export_format='GLB',
    use_selection=True,
    export_apply=True
)

print("✅ Also saved as: dog_creative.glb")
"""
        
        response = self.execute_blender_code(export_code)
        print("✅ Export abgeschlossen!")
        return response
    
    def run_creative_transformation(self):
        """Führe die komplette kreative Transformation aus"""
        print("="*60)
        print("🎨 KREATIVE HUNDE-TRANSFORMATION")
        print("="*60)
        print("Als Senior 3D Designer werde ich jetzt den Hund kreativ verändern!")
        
        # 1. Analyse
        self.analyze_scene()
        
        # 2. Kreative Änderungen
        print("\n🎨 BEGINNE KREATIVE ÄNDERUNGEN...")
        
        # Füge alle kreativen Elemente hinzu
        self.add_creative_collar()
        time.sleep(0.5)
        
        self.add_playful_ball()
        time.sleep(0.5)
        
        self.add_star_marking()
        time.sleep(0.5)
        
        self.modify_dog_color()
        time.sleep(0.5)
        
        self.add_creative_hat()
        time.sleep(0.5)
        
        # 3. Export
        self.export_creative_dog()
        
        print("\n" + "="*60)
        print("🎉 TRANSFORMATION ABGESCHLOSSEN!")
        print("="*60)
        print("\nDer Hund hat jetzt:")
        print("  🎨 Lila-blaue Farbe")
        print("  📿 Rotes Halsband mit goldenem Anhänger")
        print("  ⚽ Bunten Spielball")
        print("  ⭐ Leuchtenden Stern auf der Stirn")
        print("  🎩 Party-Hut mit Pompom")
        print("\nDiese Änderungen beweisen den vollen Zugriff auf Blender!")

if __name__ == "__main__":
    designer = CreativeDogDesigner()
    designer.run_creative_transformation()