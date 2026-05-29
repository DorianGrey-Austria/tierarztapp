"""
Blender Script: Anatomische Schichten Hund
Erzeugt ein 4-Schichten-Modell (Haut, Muskulatur, Organe, Skelett)
fuer den VetScan Anatomy Layer Viewer.

Ausfuehrung in Blender:
  1. Blender oeffnen
  2. Scripting-Tab -> Open -> dieses Script
  3. Run Script
  4. Export: File -> Export -> glTF 2.0 (.glb)

Exportiert automatisch nach assets/models/animals/dog/ wenn EXPORT_PATH gesetzt.
"""

import bpy
import math
import os
from mathutils import Vector

# --- Konfiguration ---
EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/dog/"
)
EXPORT_ENABLED = True

# --- Hilfsfunktionen ---

def clear_scene():
    """Loesche alle Objekte in der Szene."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)


def create_collection(name):
    """Erstelle eine neue Collection."""
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def create_material(name, color, alpha=1.0, emission=0.0):
    """Erstelle ein Material mit gegebener Farbe und Transparenz."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.blend_method = 'ALPHA_BLEND' if alpha < 1.0 else 'OPAQUE'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Alpha"].default_value = alpha
    if emission > 0:
        bsdf.inputs["Emission Strength"].default_value = emission
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)

    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat


def add_to_collection(obj, collection):
    """Verschiebe Objekt in eine Collection."""
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)


def set_smooth(obj):
    """Smooth Shading aktivieren."""
    for face in obj.data.polygons:
        face.use_smooth = True


# --- Schicht 1: Haut / Integument ---

def create_skin_layer(collection):
    """Erstelle die Hautschicht als Hundekoerper-Silhouette."""
    mat = create_material("Haut_Material", (0.85, 0.75, 0.60), alpha=0.6)

    # Koerper (Hauptform)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32, ring_count=16,
        radius=0.45, location=(0, 0, 0.7)
    )
    body = bpy.context.active_object
    body.name = "Haut_Koerper"
    body.scale = (1.8, 0.7, 0.75)
    body.data.materials.append(mat)
    set_smooth(body)
    add_to_collection(body, collection)

    # Kopf
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24, ring_count=12,
        radius=0.25, location=(1.2, 0, 0.95)
    )
    head = bpy.context.active_object
    head.name = "Haut_Kopf"
    head.scale = (1.2, 0.8, 0.9)
    head.data.materials.append(mat)
    set_smooth(head)
    add_to_collection(head, collection)

    # Schnauze
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8,
        radius=0.12, location=(1.55, 0, 0.85)
    )
    snout = bpy.context.active_object
    snout.name = "Haut_Schnauze"
    snout.scale = (1.5, 0.7, 0.6)
    snout.data.materials.append(mat)
    set_smooth(snout)
    add_to_collection(snout, collection)

    # Ohren
    for side, y in [("Links", 0.18), ("Rechts", -0.18)]:
        bpy.ops.mesh.primitive_cone_add(
            vertices=12, radius1=0.08, depth=0.2,
            location=(1.15, y, 1.2)
        )
        ear = bpy.context.active_object
        ear.name = f"Haut_Ohr_{side}"
        ear.rotation_euler = (0.3 if y > 0 else -0.3, 0.2, 0)
        ear.data.materials.append(mat)
        set_smooth(ear)
        add_to_collection(ear, collection)

    # Schwanz
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12, radius=0.04, depth=0.5,
        location=(-1.0, 0, 0.85)
    )
    tail = bpy.context.active_object
    tail.name = "Haut_Schwanz"
    tail.rotation_euler = (0, 0.8, 0)
    tail.data.materials.append(mat)
    set_smooth(tail)
    add_to_collection(tail, collection)

    # Beine (4 Stueck)
    leg_positions = [
        ("VL", 0.6, 0.25, 0.3),   # Vorne links
        ("VR", 0.6, -0.25, 0.3),  # Vorne rechts
        ("HL", -0.6, 0.25, 0.3),  # Hinten links
        ("HR", -0.6, -0.25, 0.3), # Hinten rechts
    ]
    for name, x, y, z in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12, radius=0.07, depth=0.6,
            location=(x, y, z)
        )
        leg = bpy.context.active_object
        leg.name = f"Haut_Bein_{name}"
        leg.data.materials.append(mat)
        set_smooth(leg)
        add_to_collection(leg, collection)

    # Pfoten
    for name, x, y in leg_positions:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=12, ring_count=6,
            radius=0.08, location=(x, y, 0.02)
        )
        paw = bpy.context.active_object
        paw.name = f"Haut_Pfote_{name}"
        paw.scale = (1.2, 0.8, 0.5)
        paw.data.materials.append(mat)
        set_smooth(paw)
        add_to_collection(paw, collection)


# --- Schicht 2: Muskulatur ---

def create_muscle_layer(collection):
    """Erstelle die Muskelschicht."""
    mat_muscle = create_material("Muskel_Material", (0.7, 0.2, 0.15), alpha=0.7)
    mat_tendon = create_material("Sehne_Material", (0.9, 0.85, 0.8), alpha=0.7)

    muscles = [
        # (Name, Position, Skalierung, Rotation)
        ("M_Trapezius", (0.3, 0, 0.9), (0.4, 0.5, 0.15), (0, 0, 0)),
        ("M_Latissimus_Dorsi", (0.0, 0, 0.85), (0.5, 0.55, 0.12), (0, 0, 0)),
        ("M_Deltoideus", (0.7, 0.2, 0.75), (0.15, 0.1, 0.12), (0, 0, 0.3)),
        ("M_Deltoideus_R", (0.7, -0.2, 0.75), (0.15, 0.1, 0.12), (0, 0, -0.3)),
        ("M_Biceps", (0.6, 0.22, 0.5), (0.08, 0.06, 0.2), (0, 0, 0)),
        ("M_Biceps_R", (0.6, -0.22, 0.5), (0.08, 0.06, 0.2), (0, 0, 0)),
        ("M_Triceps", (0.55, 0.23, 0.55), (0.12, 0.08, 0.18), (0, 0, 0)),
        ("M_Triceps_R", (0.55, -0.23, 0.55), (0.12, 0.08, 0.18), (0, 0, 0)),
        ("M_Pectoralis", (0.5, 0, 0.5), (0.3, 0.35, 0.08), (0, 0, 0)),
        ("M_Obliquus_Ext", (-0.1, 0.15, 0.6), (0.35, 0.08, 0.2), (0, 0, 0.1)),
        ("M_Obliquus_Ext_R", (-0.1, -0.15, 0.6), (0.35, 0.08, 0.2), (0, 0, -0.1)),
        ("M_Gluteus", (-0.5, 0.18, 0.8), (0.2, 0.12, 0.15), (0, 0, 0)),
        ("M_Gluteus_R", (-0.5, -0.18, 0.8), (0.2, 0.12, 0.15), (0, 0, 0)),
        ("M_Quadriceps", (-0.55, 0.22, 0.5), (0.1, 0.08, 0.22), (0, 0, 0)),
        ("M_Quadriceps_R", (-0.55, -0.22, 0.5), (0.1, 0.08, 0.22), (0, 0, 0)),
        ("M_Gastrocnemius", (-0.6, 0.22, 0.25), (0.07, 0.05, 0.15), (0, 0, 0)),
        ("M_Gastrocnemius_R", (-0.6, -0.22, 0.25), (0.07, 0.05, 0.15), (0, 0, 0)),
        # Kopfmuskeln
        ("M_Masseter", (1.2, 0.15, 0.85), (0.08, 0.06, 0.08), (0, 0, 0)),
        ("M_Masseter_R", (1.2, -0.15, 0.85), (0.08, 0.06, 0.08), (0, 0, 0)),
        ("M_Temporalis", (1.15, 0.1, 1.05), (0.1, 0.08, 0.06), (0, 0, 0)),
        ("M_Temporalis_R", (1.15, -0.1, 1.05), (0.1, 0.08, 0.06), (0, 0, 0)),
    ]

    for name, loc, scale, rot in muscles:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8,
            radius=1.0, location=loc
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        obj.rotation_euler = rot
        obj.data.materials.append(mat_muscle)
        set_smooth(obj)
        add_to_collection(obj, collection)


# --- Schicht 3: Organe ---

def create_organ_layer(collection):
    """Erstelle die Organschicht mit individuellen Farben."""

    organs = {
        "Herz": {
            "color": (0.8, 0.1, 0.1), "loc": (0.4, 0.05, 0.65),
            "scale": (0.1, 0.08, 0.12), "segments": 16
        },
        "Lunge_Links": {
            "color": (0.85, 0.55, 0.6), "loc": (0.35, 0.15, 0.7),
            "scale": (0.2, 0.12, 0.18), "segments": 16
        },
        "Lunge_Rechts": {
            "color": (0.85, 0.55, 0.6), "loc": (0.35, -0.15, 0.7),
            "scale": (0.22, 0.14, 0.18), "segments": 16
        },
        "Leber": {
            "color": (0.5, 0.15, 0.1), "loc": (0.15, 0, 0.55),
            "scale": (0.15, 0.25, 0.1), "segments": 16
        },
        "Magen": {
            "color": (0.85, 0.7, 0.6), "loc": (0.05, 0.08, 0.55),
            "scale": (0.12, 0.1, 0.08), "segments": 16
        },
        "Milz": {
            "color": (0.5, 0.1, 0.2), "loc": (0.0, 0.2, 0.55),
            "scale": (0.12, 0.04, 0.06), "segments": 12
        },
        "Niere_Links": {
            "color": (0.6, 0.25, 0.2), "loc": (-0.15, 0.15, 0.7),
            "scale": (0.06, 0.04, 0.05), "segments": 12
        },
        "Niere_Rechts": {
            "color": (0.6, 0.25, 0.2), "loc": (-0.1, -0.15, 0.72),
            "scale": (0.06, 0.04, 0.05), "segments": 12
        },
        "Duenndarm": {
            "color": (0.9, 0.75, 0.65), "loc": (-0.15, 0, 0.5),
            "scale": (0.25, 0.18, 0.1), "segments": 16
        },
        "Dickdarm": {
            "color": (0.75, 0.6, 0.5), "loc": (-0.3, 0, 0.55),
            "scale": (0.15, 0.2, 0.08), "segments": 12
        },
        "Blase": {
            "color": (0.7, 0.7, 0.3), "loc": (-0.55, 0, 0.45),
            "scale": (0.07, 0.05, 0.06), "segments": 12
        },
        "Zwerchfell": {
            "color": (0.8, 0.5, 0.5), "loc": (0.2, 0, 0.6),
            "scale": (0.02, 0.3, 0.2), "segments": 12
        },
        "Trachea": {
            "color": (0.9, 0.85, 0.8), "loc": (0.8, 0, 0.9),
            "scale": (0.35, 0.03, 0.03), "segments": 8
        },
        "Oesophagus": {
            "color": (0.85, 0.7, 0.65), "loc": (0.6, 0.03, 0.85),
            "scale": (0.4, 0.02, 0.02), "segments": 8
        },
    }

    for name, props in organs.items():
        mat = create_material(f"Organ_{name}", props["color"], alpha=0.85)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=props["segments"], ring_count=props["segments"] // 2,
            radius=1.0, location=props["loc"]
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = props["scale"]
        obj.data.materials.append(mat)
        set_smooth(obj)
        add_to_collection(obj, collection)


# --- Schicht 4: Skelett ---

def create_skeleton_layer(collection):
    """Erstelle das Skelett."""
    mat_bone = create_material("Knochen_Material", (0.95, 0.92, 0.85), alpha=0.9)
    mat_joint = create_material("Gelenk_Material", (0.85, 0.82, 0.75), alpha=0.9)

    # Wirbelsaeule (vereinfacht als Segmente)
    for i in range(25):
        x = 0.9 - i * 0.075
        z = 0.85 + math.sin(i * 0.15) * 0.03
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.025, depth=0.06,
            location=(x, 0, z)
        )
        vert = bpy.context.active_object
        vert.name = f"Wirbel_{i+1}"
        vert.rotation_euler = (0, math.pi / 2, 0)
        vert.data.materials.append(mat_bone)
        add_to_collection(vert, collection)

    # Schaedel
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8,
        radius=0.18, location=(1.15, 0, 0.95)
    )
    skull = bpy.context.active_object
    skull.name = "Schaedel"
    skull.scale = (1.3, 0.7, 0.8)
    skull.data.materials.append(mat_bone)
    set_smooth(skull)
    add_to_collection(skull, collection)

    # Mandibula (Unterkiefer)
    bpy.ops.mesh.primitive_cube_add(size=0.15, location=(1.35, 0, 0.82))
    mandible = bpy.context.active_object
    mandible.name = "Mandibula"
    mandible.scale = (1.8, 0.5, 0.3)
    mandible.data.materials.append(mat_bone)
    add_to_collection(mandible, collection)

    # Rippen (13 Paare, vereinfacht)
    for i in range(13):
        x = 0.55 - i * 0.065
        for side, y_sign in [("L", 1), ("R", -1)]:
            bpy.ops.mesh.primitive_torus_add(
                major_radius=0.2, minor_radius=0.012,
                major_segments=24, minor_segments=8,
                location=(x, 0, 0.65)
            )
            rib = bpy.context.active_object
            rib.name = f"Rippe_{i+1}_{side}"
            rib.scale = (0.3, 0.8 * y_sign, 1.0)
            rib.rotation_euler = (0, 0.1, 0)
            rib.data.materials.append(mat_bone)
            add_to_collection(rib, collection)

    # Scapula (Schulterblatt)
    for side, y in [("L", 0.2), ("R", -0.2)]:
        bpy.ops.mesh.primitive_cone_add(
            vertices=12, radius1=0.12, depth=0.02,
            location=(0.6, y, 0.85)
        )
        scap = bpy.context.active_object
        scap.name = f"Scapula_{side}"
        scap.rotation_euler = (0, 0.3, 0)
        scap.data.materials.append(mat_bone)
        add_to_collection(scap, collection)

    # Humerus, Radius/Ulna (Vorderbeine)
    for side, y in [("L", 0.22), ("R", -0.22)]:
        # Humerus
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.025, depth=0.25,
            location=(0.6, y, 0.55)
        )
        hum = bpy.context.active_object
        hum.name = f"Humerus_{side}"
        hum.data.materials.append(mat_bone)
        add_to_collection(hum, collection)

        # Radius/Ulna
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.02, depth=0.25,
            location=(0.6, y, 0.3)
        )
        rad = bpy.context.active_object
        rad.name = f"Radius_{side}"
        rad.data.materials.append(mat_bone)
        add_to_collection(rad, collection)

    # Pelvis
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6,
        radius=0.12, location=(-0.55, 0, 0.75)
    )
    pelvis = bpy.context.active_object
    pelvis.name = "Pelvis"
    pelvis.scale = (0.8, 1.5, 0.6)
    pelvis.data.materials.append(mat_bone)
    set_smooth(pelvis)
    add_to_collection(pelvis, collection)

    # Femur, Tibia/Fibula (Hinterbeine)
    for side, y in [("L", 0.22), ("R", -0.22)]:
        # Femur
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.03, depth=0.28,
            location=(-0.55, y, 0.5)
        )
        fem = bpy.context.active_object
        fem.name = f"Femur_{side}"
        fem.rotation_euler = (0, 0.15, 0)
        fem.data.materials.append(mat_bone)
        add_to_collection(fem, collection)

        # Patella
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=8, ring_count=4,
            radius=0.02, location=(-0.58, y, 0.38)
        )
        pat = bpy.context.active_object
        pat.name = f"Patella_{side}"
        pat.data.materials.append(mat_joint)
        add_to_collection(pat, collection)

        # Tibia
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.022, depth=0.28,
            location=(-0.6, y, 0.22)
        )
        tib = bpy.context.active_object
        tib.name = f"Tibia_{side}"
        tib.data.materials.append(mat_bone)
        add_to_collection(tib, collection)


# --- Hauptprogramm ---

def main():
    print("=== VetScan Anatomy Layers: Hund ===")
    clear_scene()

    # Collections fuer Schichten erstellen
    col_skin = create_collection("Schicht_1_Haut")
    col_muscles = create_collection("Schicht_2_Muskulatur")
    col_organs = create_collection("Schicht_3_Organe")
    col_skeleton = create_collection("Schicht_4_Skelett")

    print("Erstelle Schicht 1: Haut...")
    create_skin_layer(col_skin)

    print("Erstelle Schicht 2: Muskulatur...")
    create_muscle_layer(col_muscles)

    print("Erstelle Schicht 3: Organe...")
    create_organ_layer(col_organs)

    print("Erstelle Schicht 4: Skelett...")
    create_skeleton_layer(col_skeleton)

    # Kamera und Licht
    bpy.ops.object.camera_add(location=(3, -2, 1.5))
    cam = bpy.context.active_object
    cam.name = "Anatomy_Camera"
    cam.rotation_euler = (1.2, 0, 0.8)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type='SUN', location=(2, -1, 3))
    light = bpy.context.active_object
    light.name = "Anatomy_Light"
    light.data.energy = 3.0

    # Export
    if EXPORT_ENABLED:
        os.makedirs(EXPORT_PATH, exist_ok=True)

        # Alle Schichten einzeln exportieren
        layers = [
            ("Schicht_1_Haut", "dog_skin.glb"),
            ("Schicht_2_Muskulatur", "dog_muscles.glb"),
            ("Schicht_3_Organe", "dog_organs.glb"),
            ("Schicht_4_Skelett", "dog_skeleton.glb"),
        ]

        for col_name, filename in layers:
            # Alle Objekte deselektieren
            bpy.ops.object.select_all(action='DESELECT')
            # Nur Objekte dieser Collection selektieren
            col = bpy.data.collections.get(col_name)
            if col:
                for obj in col.objects:
                    obj.select_set(True)
                bpy.context.view_layer.objects.active = col.objects[0]

                filepath = os.path.join(EXPORT_PATH, filename)
                bpy.ops.export_scene.gltf(
                    filepath=filepath,
                    export_format="GLB",
                    use_selection=True,
                    export_draco_mesh_compression_enable=True,
                    export_draco_mesh_compression_level=6,
                    export_materials='EXPORT',
                )
                print(f"  Exportiert: {filepath}")

        # Gesamtmodell exportieren
        bpy.ops.object.select_all(action='SELECT')
        filepath = os.path.join(EXPORT_PATH, "dog_anatomy_complete.glb")
        bpy.ops.export_scene.gltf(
            filepath=filepath,
            export_format="GLB",
            use_selection=True,
            export_draco_mesh_compression_enable=True,
            export_draco_mesh_compression_level=6,
            export_materials='EXPORT',
        )
        print(f"  Exportiert: {filepath}")

    print("=== Fertig! ===")
    print(f"Objekte gesamt: {len(bpy.data.objects)}")
    print("Schichten: Haut, Muskulatur, Organe, Skelett")
    print("Nutze die Collections im Outliner um Schichten ein-/auszublenden.")


if __name__ == "__main__":
    main()
