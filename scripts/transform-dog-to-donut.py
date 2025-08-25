#!/usr/bin/env python3
"""
🍩 DONUT TRANSFORMATION SCRIPT - DER GLÜCKSFALL REPRODUZIEREN!

Dieses Script verwandelt den Hund zurück in einen Donut,
um den glücklichen Zufall von gestern zu reproduzieren.

Das ist der Moment, wo aus einem 3D-Hund ein perfekter Donut wird!
"""

import asyncio
import websockets
import json
import time
from datetime import datetime

class DonutTransformer:
    def __init__(self):
        self.ws_url = "ws://localhost:9876"
        self.transformation_steps = []
        
    async def connect_and_transform(self):
        print("🍩 DONUT TRANSFORMATION - Der Glücksfall wird reproduziert!")
        print("=" * 60)
        print(f"Zeit: {datetime.now().strftime('%H:%M:%S')}")
        print("Verbinde mit Blender MCP auf Port 9876...")
        
        try:
            async with websockets.connect(self.ws_url) as websocket:
                print("✅ Verbindung hergestellt!")
                
                # Schritt 1: Scene analysieren
                print("\n📊 Analysiere aktuelle Scene...")
                await self.analyze_scene(websocket)
                
                # Schritt 2: Den Hund finden und löschen
                print("\n🐕 Suche und entferne Hund...")
                await self.remove_dog(websocket)
                
                # Schritt 3: Donut erstellen
                print("\n🍩 Erstelle perfekten Donut...")
                await self.create_donut(websocket)
                
                # Schritt 4: Donut-Details hinzufügen
                print("\n🎨 Füge Donut-Details hinzu...")
                await self.add_donut_details(websocket)
                
                # Schritt 5: Finale Touches
                print("\n✨ Finale Anpassungen...")
                await self.final_touches(websocket)
                
                print("\n" + "=" * 60)
                print("🎉 TRANSFORMATION ABGESCHLOSSEN!")
                print("Der Glücksfall wurde erfolgreich reproduziert!")
                print("\n💡 Nächster Schritt: Manueller Export via BLENDER-EXPORT-MANUAL.py")
                
        except Exception as e:
            print(f"\n❌ Fehler bei der Transformation: {e}")
            print("Stelle sicher, dass Blender läuft und MCP aktiv ist!")
    
    async def send_command(self, websocket, method, params=None):
        """Sendet einen Befehl an Blender MCP"""
        command = {
            "jsonrpc": "2.0",
            "id": f"donut_{int(time.time() * 1000)}",
            "method": method,
            "params": params or {}
        }
        
        await websocket.send(json.dumps(command))
        response = await websocket.recv()
        return json.loads(response)
    
    async def analyze_scene(self, websocket):
        """Analysiert die aktuelle Scene"""
        result = await self.send_command(websocket, "get_scene_info")
        if "result" in result:
            objects = result["result"].get("objects", [])
            print(f"  Gefundene Objekte: {len(objects)}")
            for obj in objects[:5]:  # Zeige erste 5
                print(f"    - {obj}")
    
    async def remove_dog(self, websocket):
        """Entfernt den Hund aus der Scene"""
        # Lösche alle existierenden Objekte (außer Kamera und Licht)
        code = """
import bpy

# Alle Mesh-Objekte löschen
for obj in bpy.data.objects:
    if obj.type == 'MESH':
        bpy.data.objects.remove(obj, do_unlink=True)
        
print("Alle Mesh-Objekte entfernt!")
"""
        result = await self.send_command(websocket, "execute_blender_code", {"code": code})
        print("  ✅ Hund und andere Meshes entfernt")
    
    async def create_donut(self, websocket):
        """Erstellt einen perfekten Donut"""
        code = """
import bpy
import math

# Torus (Donut-Form) erstellen
bpy.ops.mesh.primitive_torus_add(
    location=(0, 0, 1),
    major_radius=1.5,
    minor_radius=0.6,
    major_segments=48,
    minor_segments=24
)

donut = bpy.context.active_object
donut.name = "GLÜCKSFALL_DONUT"

# Subdivision Surface für smooth look
subsurf = donut.modifiers.new(name="Subdivision", type='SUBSURF')
subsurf.levels = 2
subsurf.render_levels = 2

# Donut leicht rotieren für besseren Winkel
donut.rotation_euler[0] = math.radians(15)
donut.rotation_euler[1] = math.radians(30)

print(f"Donut '{donut.name}' erstellt!")
"""
        result = await self.send_command(websocket, "execute_blender_code", {"code": code})
        print("  ✅ Donut-Grundform erstellt")
        self.transformation_steps.append("Donut-Base erstellt")
    
    async def add_donut_details(self, websocket):
        """Fügt realistische Donut-Details hinzu"""
        
        # Material für den Donut
        print("  🎨 Erstelle Donut-Material...")
        code_material = """
import bpy

# Donut Material
donut = bpy.data.objects.get("GLÜCKSFALL_DONUT")
if donut:
    # Basis-Material (goldbraun)
    mat_base = bpy.data.materials.new(name="Donut_Teig")
    mat_base.use_nodes = True
    mat_base.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.5, 0.2, 1.0)  # Goldbraun
    mat_base.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.6  # Roughness
    
    donut.data.materials.clear()
    donut.data.materials.append(mat_base)
    
    print("Donut-Material angewendet!")
"""
        await self.send_command(websocket, "execute_blender_code", {"code": code_material})
        print("    ✅ Goldbraunes Teig-Material")
        
        # Glasur hinzufügen
        print("  🍫 Füge Schokoladen-Glasur hinzu...")
        code_icing = """
import bpy
import math

# Duplikat für Glasur erstellen
donut = bpy.data.objects.get("GLÜCKSFALL_DONUT")
if donut:
    # Glasur als separates Objekt
    bpy.ops.mesh.primitive_torus_add(
        location=(0, 0, 1.15),
        major_radius=1.52,
        minor_radius=0.58,
        major_segments=48,
        minor_segments=24
    )
    
    icing = bpy.context.active_object
    icing.name = "Donut_Glasur"
    
    # Gleiche Rotation wie Donut
    icing.rotation_euler[0] = math.radians(15)
    icing.rotation_euler[1] = math.radians(30)
    
    # Glasur nur oben (mit Wave Modifier für tropfenden Effekt)
    wave = icing.modifiers.new(name="Drip", type='WAVE')
    wave.height = 0.05
    wave.width = 0.3
    wave.speed = 0
    wave.offset = 0
    
    # Schokoladen-Material
    mat_choco = bpy.data.materials.new(name="Schokolade")
    mat_choco.use_nodes = True
    mat_choco.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.15, 0.05, 0.02, 1.0)  # Dunkelbraun
    mat_choco.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2  # Glossy
    mat_choco.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.5  # Transmission für Glanz
    
    icing.data.materials.clear()
    icing.data.materials.append(mat_choco)
    
    print("Schokoladen-Glasur hinzugefügt!")
"""
        await self.send_command(websocket, "execute_blender_code", {"code": code_icing})
        print("    ✅ Schokoladen-Glasur")
        
        # Streusel hinzufügen
        print("  🌈 Füge bunte Streusel hinzu...")
        code_sprinkles = """
import bpy
import random
import math

# Bunte Streusel auf der Glasur
colors = [
    (1, 0.2, 0.2, 1),  # Rot
    (0.2, 1, 0.2, 1),  # Grün
    (0.2, 0.2, 1, 1),  # Blau
    (1, 1, 0.2, 1),    # Gelb
    (1, 0.2, 1, 1),    # Pink
    (1, 0.6, 0.2, 1)   # Orange
]

# Erstelle 30 Streusel
for i in range(30):
    # Zufällige Position auf dem Donut
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0.8, 1.5)
    
    x = radius * math.cos(angle)
    y = radius * math.sin(angle)
    z = random.uniform(1.4, 1.7)
    
    # Kleiner Zylinder als Streusel
    bpy.ops.mesh.primitive_cylinder_add(
        location=(x, y, z),
        radius=0.03,
        depth=0.15
    )
    
    sprinkle = bpy.context.active_object
    sprinkle.name = f"Streusel_{i:02d}"
    
    # Zufällige Rotation
    sprinkle.rotation_euler[0] = random.uniform(0, math.pi)
    sprinkle.rotation_euler[1] = random.uniform(0, math.pi)
    sprinkle.rotation_euler[2] = random.uniform(0, math.pi)
    
    # Zufällige Farbe
    mat = bpy.data.materials.new(name=f"Streusel_Color_{i}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = random.choice(colors)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0  # Emission für Leuchten
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.1  # Leichte Emission
    
    sprinkle.data.materials.clear()
    sprinkle.data.materials.append(mat)

print("30 bunte Streusel hinzugefügt!")
"""
        await self.send_command(websocket, "execute_blender_code", {"code": code_sprinkles})
        print("    ✅ 30 bunte Streusel")
        self.transformation_steps.append("Donut-Details komplett")
    
    async def final_touches(self, websocket):
        """Finale Anpassungen für den perfekten Donut"""
        code = """
import bpy

# Stelle sicher, dass der Donut im Fokus ist
donut = bpy.data.objects.get("GLÜCKSFALL_DONUT")
if donut:
    # Setze Donut als aktives Objekt
    bpy.context.view_layer.objects.active = donut
    donut.select_set(True)
    
    # Zoom auf den Donut
    for area in bpy.context.screen.areas:
        if area.type == 'VIEW_3D':
            for region in area.regions:
                if region.type == 'WINDOW':
                    override = {'area': area, 'region': region}
                    bpy.ops.view3d.view_selected(override)
                    break
    
    print("🍩 DER GLÜCKSFALL IST KOMPLETT!")
    print("Ein perfekter Donut mit Schokoladen-Glasur und bunten Streuseln!")
    print("")
    print("Dies ist der Moment, wo aus einem Hund ein Donut wurde.")
    print("Der Glücksfall von gestern wurde erfolgreich reproduziert!")
"""
        result = await self.send_command(websocket, "execute_blender_code", {"code": code})
        print("  ✅ Finale Anpassungen abgeschlossen")
        self.transformation_steps.append("Glücksfall reproduziert!")

def main():
    transformer = DonutTransformer()
    
    print("\n" + "=" * 60)
    print("🍩 DONUT TRANSFORMATION SCRIPT")
    print("Reproduziere den Glücksfall von gestern!")
    print("=" * 60)
    print()
    print("Dieser Moment ist historisch:")
    print("Gestern verwandelte sich versehentlich ein Hund in einen Donut.")
    print("Heute machen wir es absichtlich!")
    print()
    
    # Führe die Transformation aus
    asyncio.run(transformer.connect_and_transform())
    
    print("\n" + "=" * 60)
    print("📝 ZUSAMMENFASSUNG:")
    for i, step in enumerate(transformer.transformation_steps, 1):
        print(f"  {i}. {step}")
    print("\n💾 Vergiss nicht den manuellen Export:")
    print("  1. Blender → Scripting Tab")
    print("  2. Text → Open → BLENDER-EXPORT-MANUAL.py")
    print("  3. Run Script (▶️ Button)")
    print("=" * 60)

if __name__ == "__main__":
    main()