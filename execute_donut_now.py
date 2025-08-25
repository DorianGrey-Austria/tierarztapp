#!/usr/bin/env python3
"""
Execute Donut Creation in Running Blender Instance
This attempts to execute the donut creation script in the already running Blender GUI
"""

import os
import subprocess
import sys
from pathlib import Path

# Path to the script we created
script_path = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/scripts/glucksfall_donut_creation.py')

print("🍩 Executing Glücksfall Donut Creation in Running Blender...")
print(f"Script: {script_path}")

# Method 1: Try to execute via Blender's Python API in the running instance
print("\n=== Attempting to execute via Blender's Python console ===")

# Create a simpler execution script that tells the user exactly what to do
execution_instructions = f"""
🍩 GLÜCKSFALL DONUT CREATION - MANUAL EXECUTION REQUIRED
{'='*65}

Since I don't have direct MCP tools available in Claude Code, 
and the WebSocket MCP server isn't currently running, here's 
how to execute the donut creation in your running Blender:

STEP-BY-STEP INSTRUCTIONS:
{'='*30}

1. 📋 COPY THE FOLLOWING PYTHON CODE:
   (Select all text between the --- lines and copy)

---COPY FROM HERE---
import bpy
import bmesh
import mathutils
from mathutils import Vector
import random

print("\\n=== 🍩 GLÜCKSFALL DONUT CREATION 🍩 ===")

# Clear scene
bpy.ops.object.select_all(action='DESELECT')
mesh_objects = [obj for obj in bpy.data.objects if obj.type == 'MESH']
for obj in mesh_objects:
    bpy.data.objects.remove(obj, do_unlink=True)

# Create donut
bpy.ops.mesh.primitive_torus_add(location=(0,0,0), major_radius=2.0, minor_radius=0.8, major_segments=48, minor_segments=24)
donut = bpy.context.active_object
donut.name = "Glücksfall_Donut"

# Chocolate material
mat = bpy.data.materials.new(name="Chocolate_Icing")
mat.use_nodes = True
mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.1, 0.05, 1.0)
mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.8
donut.data.materials.append(mat)

# Sprinkles
colors = [(1,0.2,0.2,1), (0.2,1,0.2,1), (0.2,0.2,1,1), (1,1,0.2,1), (1,0.2,1,1), (0.2,1,1,1)]
for i in range(50):
    bpy.ops.mesh.primitive_cylinder_add(radius=0.02, depth=0.15)
    sprinkle = bpy.context.active_object
    angle = random.uniform(0, 6.28)
    dist = random.uniform(1.2, 2.8)
    x = dist * mathutils.Matrix.Rotation(angle, 4, 'Z')[0][0]
    y = dist * mathutils.Matrix.Rotation(angle, 4, 'Z')[1][0]
    sprinkle.location = (x, y, 0.9)
    sprinkle.rotation_euler = (random.uniform(0,6.28), random.uniform(0,6.28), random.uniform(0,6.28))
    sprinkle_mat = bpy.data.materials.new(name="Sprinkle_" + str(i))
    sprinkle_mat.use_nodes = True
    sprinkle_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = random.choice(colors)
    sprinkle.data.materials.append(sprinkle_mat)

# Lighting and camera
bpy.ops.object.light_add(type='SUN', location=(5,5,10))
bpy.context.active_object.data.energy = 5.0
if bpy.data.objects.get("Camera"):
    bpy.data.objects["Camera"].location = (6,-6,4)
    bpy.data.objects["Camera"].rotation_euler = (1.2,0,0.785)

print("🍩 GLÜCKSFALL DONUT COMPLETE! Dog → Donut transformation successful!")
---COPY TO HERE---

2. 🎬 SWITCH TO BLENDER:
   - Click on the Blender application (already running)
   - If not visible, press Cmd+Tab to switch apps

3. 📝 OPEN SCRIPTING WORKSPACE:
   - At the top of Blender, click "Scripting" tab
   - OR press Shift+F11

4. 📋 PASTE AND RUN:
   - Click in the Text Editor (main area with >>> )
   - Paste the copied Python code (Cmd+V)
   - Click "Run Script" button (▷ play icon)
   - OR press Alt+P

5. 🍩 WATCH THE MAGIC:
   - Scene will clear
   - Donut will appear with chocolate material
   - 50 colorful sprinkles will be added
   - Lighting will be set up
   - Camera will position for perfect view

6. 🎨 BEST VIEW:
   - Press Numpad 0 to see through camera
   - Press Z and choose "Material Preview"
   - OR press Numpad 7 for top view

7. 💾 EXPORT (OPTIONAL):
   Run this in Scripting to export:
   
   import bpy
   from pathlib import Path
   export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
   export_dir.mkdir(exist_ok=True)
   bpy.ops.object.select_all(action='SELECT')
   bpy.ops.export_scene.gltf(filepath=str(export_dir/'glucksfall_donut.glb'), export_format='GLB')

🎉 RESULT: You will have successfully reproduced the "Glücksfall" 
where the dog accidentally turned into a delicious chocolate donut 
with colorful sprinkles!

TROUBLESHOOTING:
- If Blender isn't running: Launch it first
- If script errors: Make sure you're in Scripting workspace
- If no donut appears: Check the 3D viewport and try pressing 'A' to deselect all

{'='*65}
"""

print(execution_instructions)

# Also save this to a file for reference
instructions_file = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/DONUT_CREATION_INSTRUCTIONS.txt')
with open(instructions_file, 'w') as f:
    f.write(execution_instructions)

print(f"\n📄 Instructions also saved to: {instructions_file}")
print("\nOpen this file if you need to reference the instructions later!")

# Try to open the instructions file
try:
    subprocess.run(['open', str(instructions_file)])
    print("📖 Instructions file opened automatically!")
except:
    print("💡 You can manually open the instructions file if needed.")

print(f"\n✅ All ready! The Glücksfall donut creation is waiting for you in Blender!")
print("🐕 → 🍩 Let's turn that dog into a donut!")