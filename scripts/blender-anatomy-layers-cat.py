"""
Blender Script: Anatomische Schichten Katze
Erzeugt ein 4-Schichten-Modell angepasst an Katzen-Anatomie.

Unterschiede zum Hund:
- Flexiblere Wirbelsaeule (mehr LWK: 7 vs 7, aber beweglicher)
- Rudimentaeres Schluesselbein (Clavicula)
- Kleineres Caecum
- Andere Koerperproportionen (kompakter, laengerer Schwanz relativ)

Ausfuehrung: Blender -> Scripting -> Open -> Run Script
"""

import bpy
import math
import os

EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/cat/"
)
EXPORT_ENABLED = True


def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for col in bpy.data.collections:
        bpy.data.collections.remove(col)


def create_collection(name):
    col = bpy.data.collections.new(name)
    bpy.context.scene.collection.children.link(col)
    return col


def create_material(name, color, alpha=1.0):
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
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat


def add_to_collection(obj, collection):
    for col in obj.users_collection:
        col.objects.unlink(obj)
    collection.objects.link(obj)


def set_smooth(obj):
    for face in obj.data.polygons:
        face.use_smooth = True


def create_skin_layer(collection):
    """Katzenkoerper -- kompakter und geschmeidiger als Hund."""
    mat = create_material("Katze_Haut", (0.65, 0.55, 0.45), alpha=0.6)

    # Koerper (schlanker als Hund)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32, ring_count=16, radius=0.35, location=(0, 0, 0.55)
    )
    body = bpy.context.active_object
    body.name = "Katze_Haut_Koerper"
    body.scale = (1.6, 0.55, 0.6)
    body.data.materials.append(mat)
    set_smooth(body)
    add_to_collection(body, collection)

    # Kopf (runder als Hund)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24, ring_count=12, radius=0.2, location=(0.95, 0, 0.8)
    )
    head = bpy.context.active_object
    head.name = "Katze_Haut_Kopf"
    head.scale = (1.0, 0.9, 0.95)
    head.data.materials.append(mat)
    set_smooth(head)
    add_to_collection(head, collection)

    # Schnauze (kuerzer als Hund)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6, radius=0.08, location=(1.18, 0, 0.72)
    )
    snout = bpy.context.active_object
    snout.name = "Katze_Haut_Schnauze"
    snout.scale = (1.0, 0.8, 0.6)
    snout.data.materials.append(mat)
    set_smooth(snout)
    add_to_collection(snout, collection)

    # Spitze Ohren (dreieckig, groesser relativ zum Kopf)
    for side, y in [("Links", 0.12), ("Rechts", -0.12)]:
        bpy.ops.mesh.primitive_cone_add(
            vertices=12, radius1=0.06, depth=0.18,
            location=(0.92, y, 1.0)
        )
        ear = bpy.context.active_object
        ear.name = f"Katze_Ohr_{side}"
        ear.rotation_euler = (0.15 if y > 0 else -0.15, 0.1, 0)
        ear.data.materials.append(mat)
        set_smooth(ear)
        add_to_collection(ear, collection)

    # Langer Schwanz
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12, radius=0.025, depth=0.6,
        location=(-0.9, 0, 0.7)
    )
    tail = bpy.context.active_object
    tail.name = "Katze_Schwanz"
    tail.rotation_euler = (0, 0.6, 0)
    tail.data.materials.append(mat)
    set_smooth(tail)
    add_to_collection(tail, collection)

    # Beine (duenner als Hund)
    leg_positions = [
        ("VL", 0.45, 0.18, 0.22),
        ("VR", 0.45, -0.18, 0.22),
        ("HL", -0.5, 0.18, 0.22),
        ("HR", -0.5, -0.18, 0.22),
    ]
    for name, x, y, z in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=12, radius=0.045, depth=0.45,
            location=(x, y, z)
        )
        leg = bpy.context.active_object
        leg.name = f"Katze_Bein_{name}"
        leg.data.materials.append(mat)
        set_smooth(leg)
        add_to_collection(leg, collection)

    # Pfoten (kleiner, zierlicher)
    for name, x, y, _ in leg_positions:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10, ring_count=5,
            radius=0.05, location=(x, y, 0.01)
        )
        paw = bpy.context.active_object
        paw.name = f"Katze_Pfote_{name}"
        paw.scale = (1.1, 0.7, 0.4)
        paw.data.materials.append(mat)
        set_smooth(paw)
        add_to_collection(paw, collection)


def create_muscle_layer(collection):
    """Katzenmuskulatur -- schlanker und flexibler."""
    mat = create_material("Katze_Muskel", (0.7, 0.2, 0.15), alpha=0.7)

    muscles = [
        ("Katze_M_Trapezius", (0.2, 0, 0.72), (0.3, 0.4, 0.1)),
        ("Katze_M_Latissimus", (-0.05, 0, 0.68), (0.4, 0.42, 0.08)),
        ("Katze_M_Pectoralis", (0.35, 0, 0.4), (0.2, 0.28, 0.06)),
        ("Katze_M_Obliquus", (-0.15, 0.12, 0.5), (0.28, 0.06, 0.15)),
        ("Katze_M_Obliquus_R", (-0.15, -0.12, 0.5), (0.28, 0.06, 0.15)),
        ("Katze_M_Gluteus", (-0.4, 0.14, 0.65), (0.15, 0.1, 0.12)),
        ("Katze_M_Gluteus_R", (-0.4, -0.14, 0.65), (0.15, 0.1, 0.12)),
        ("Katze_M_Biceps_L", (0.45, 0.16, 0.38), (0.06, 0.04, 0.15)),
        ("Katze_M_Biceps_R", (0.45, -0.16, 0.38), (0.06, 0.04, 0.15)),
        ("Katze_M_Quadriceps_L", (-0.45, 0.16, 0.38), (0.07, 0.05, 0.16)),
        ("Katze_M_Quadriceps_R", (-0.45, -0.16, 0.38), (0.07, 0.05, 0.16)),
    ]

    for name, loc, scale in muscles:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=14, ring_count=7, radius=1.0, location=loc
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = scale
        obj.data.materials.append(mat)
        set_smooth(obj)
        add_to_collection(obj, collection)


def create_organ_layer(collection):
    """Katzenorgane mit spezifischen Unterschieden zum Hund."""
    organs = {
        "Katze_Herz": {
            "color": (0.8, 0.1, 0.1), "loc": (0.3, 0.04, 0.52),
            "scale": (0.07, 0.06, 0.09)
        },
        "Katze_Lunge_L": {
            "color": (0.85, 0.55, 0.6), "loc": (0.25, 0.12, 0.55),
            "scale": (0.15, 0.09, 0.14)
        },
        "Katze_Lunge_R": {
            "color": (0.85, 0.55, 0.6), "loc": (0.25, -0.12, 0.55),
            "scale": (0.17, 0.11, 0.14)
        },
        "Katze_Leber": {
            "color": (0.5, 0.15, 0.1), "loc": (0.1, 0, 0.45),
            "scale": (0.12, 0.2, 0.08)
        },
        "Katze_Magen": {
            "color": (0.85, 0.7, 0.6), "loc": (0.0, 0.06, 0.45),
            "scale": (0.09, 0.07, 0.06)
        },
        "Katze_Milz": {
            "color": (0.5, 0.1, 0.2), "loc": (-0.05, 0.15, 0.45),
            "scale": (0.08, 0.03, 0.04)
        },
        "Katze_Niere_L": {
            "color": (0.6, 0.25, 0.2), "loc": (-0.1, 0.12, 0.55),
            "scale": (0.05, 0.035, 0.04)
        },
        "Katze_Niere_R": {
            "color": (0.6, 0.25, 0.2), "loc": (-0.05, -0.12, 0.57),
            "scale": (0.05, 0.035, 0.04)
        },
        "Katze_Duenndarm": {
            "color": (0.9, 0.75, 0.65), "loc": (-0.15, 0, 0.4),
            "scale": (0.2, 0.14, 0.07)
        },
        # Caecum kleiner als beim Hund
        "Katze_Dickdarm": {
            "color": (0.75, 0.6, 0.5), "loc": (-0.25, 0, 0.45),
            "scale": (0.1, 0.15, 0.06)
        },
        "Katze_Blase": {
            "color": (0.7, 0.7, 0.3), "loc": (-0.42, 0, 0.35),
            "scale": (0.05, 0.04, 0.04)
        },
        "Katze_Schilddruese_L": {
            "color": (0.8, 0.4, 0.4), "loc": (0.82, 0.04, 0.7),
            "scale": (0.02, 0.01, 0.015)
        },
        "Katze_Schilddruese_R": {
            "color": (0.8, 0.4, 0.4), "loc": (0.82, -0.04, 0.7),
            "scale": (0.02, 0.01, 0.015)
        },
    }

    for name, props in organs.items():
        mat = create_material(f"Organ_{name}", props["color"], alpha=0.85)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=14, ring_count=7, radius=1.0, location=props["loc"]
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = props["scale"]
        obj.data.materials.append(mat)
        set_smooth(obj)
        add_to_collection(obj, collection)


def create_skeleton_layer(collection):
    """Katzenskelett mit rudimentaerer Clavicula."""
    mat = create_material("Katze_Knochen", (0.95, 0.92, 0.85), alpha=0.9)

    # Wirbelsaeule
    for i in range(28):
        x = 0.7 - i * 0.06
        z = 0.7 + math.sin(i * 0.12) * 0.02
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.018, depth=0.05,
            location=(x, 0, z)
        )
        vert = bpy.context.active_object
        vert.name = f"Katze_Wirbel_{i+1}"
        vert.rotation_euler = (0, math.pi / 2, 0)
        vert.data.materials.append(mat)
        add_to_collection(vert, collection)

    # Schwanzwirbel (mehr als beim Hund, flexibler)
    for i in range(18):
        x = -0.98 - i * 0.035
        z = 0.68 + i * 0.015
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.01 - i * 0.0004, depth=0.03,
            location=(x, 0, z)
        )
        sv = bpy.context.active_object
        sv.name = f"Katze_Schwanzwirbel_{i+1}"
        sv.rotation_euler = (0, math.pi / 2 + i * 0.03, 0)
        sv.data.materials.append(mat)
        add_to_collection(sv, collection)

    # Schaedel (runder als beim Hund)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8, radius=0.15, location=(0.9, 0, 0.8)
    )
    skull = bpy.context.active_object
    skull.name = "Katze_Schaedel"
    skull.scale = (1.1, 0.85, 0.9)
    skull.data.materials.append(mat)
    set_smooth(skull)
    add_to_collection(skull, collection)

    # Rudimentaere Clavicula (katzenspezifisch!)
    for side, y in [("L", 0.12), ("R", -0.12)]:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=6, radius=0.008, depth=0.04,
            location=(0.45, y, 0.58)
        )
        clav = bpy.context.active_object
        clav.name = f"Katze_Clavicula_{side}"
        clav.rotation_euler = (0, 0, 0.5)
        clav.data.materials.append(mat)
        add_to_collection(clav, collection)

    # Rippen (13 Paare)
    for i in range(13):
        x = 0.4 - i * 0.055
        for side, y_sign in [("L", 1), ("R", -1)]:
            bpy.ops.mesh.primitive_torus_add(
                major_radius=0.15, minor_radius=0.008,
                major_segments=20, minor_segments=6,
                location=(x, 0, 0.52)
            )
            rib = bpy.context.active_object
            rib.name = f"Katze_Rippe_{i+1}_{side}"
            rib.scale = (0.25, 0.65 * y_sign, 0.85)
            rib.data.materials.append(mat)
            add_to_collection(rib, collection)

    # Extremitaetenknochen (vereinfacht)
    limb_bones = [
        ("Katze_Humerus_L", (0.45, 0.16, 0.38), 0.2),
        ("Katze_Humerus_R", (0.45, -0.16, 0.38), 0.2),
        ("Katze_Radius_L", (0.45, 0.16, 0.18), 0.18),
        ("Katze_Radius_R", (0.45, -0.16, 0.18), 0.18),
        ("Katze_Femur_L", (-0.45, 0.16, 0.38), 0.22),
        ("Katze_Femur_R", (-0.45, -0.16, 0.38), 0.22),
        ("Katze_Tibia_L", (-0.48, 0.16, 0.15), 0.2),
        ("Katze_Tibia_R", (-0.48, -0.16, 0.15), 0.2),
    ]

    for name, loc, length in limb_bones:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=0.015, depth=length, location=loc
        )
        bone = bpy.context.active_object
        bone.name = name
        bone.data.materials.append(mat)
        add_to_collection(bone, collection)

    # Pelvis
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=10, ring_count=5, radius=0.09, location=(-0.42, 0, 0.6)
    )
    pelvis = bpy.context.active_object
    pelvis.name = "Katze_Pelvis"
    pelvis.scale = (0.7, 1.3, 0.5)
    pelvis.data.materials.append(mat)
    set_smooth(pelvis)
    add_to_collection(pelvis, collection)


def main():
    print("=== VetScan Anatomy Layers: Katze ===")
    clear_scene()

    col_skin = create_collection("Katze_Haut")
    col_muscles = create_collection("Katze_Muskulatur")
    col_organs = create_collection("Katze_Organe")
    col_skeleton = create_collection("Katze_Skelett")

    create_skin_layer(col_skin)
    create_muscle_layer(col_muscles)
    create_organ_layer(col_organs)
    create_skeleton_layer(col_skeleton)

    # Kamera + Licht
    bpy.ops.object.camera_add(location=(2.5, -1.8, 1.2))
    cam = bpy.context.active_object
    cam.name = "Cat_Camera"
    cam.rotation_euler = (1.2, 0, 0.8)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type='SUN', location=(2, -1, 3))
    light = bpy.context.active_object
    light.name = "Cat_Light"
    light.data.energy = 3.0

    if EXPORT_ENABLED:
        os.makedirs(EXPORT_PATH, exist_ok=True)
        layers = [
            ("Katze_Haut", "cat_skin.glb"),
            ("Katze_Muskulatur", "cat_muscles.glb"),
            ("Katze_Organe", "cat_organs.glb"),
            ("Katze_Skelett", "cat_skeleton.glb"),
        ]
        for col_name, filename in layers:
            bpy.ops.object.select_all(action='DESELECT')
            col = bpy.data.collections.get(col_name)
            if col and col.objects:
                for obj in col.objects:
                    obj.select_set(True)
                bpy.context.view_layer.objects.active = col.objects[0]
                filepath = os.path.join(EXPORT_PATH, filename)
                bpy.ops.export_scene.gltf(
                    filepath=filepath, export_format="GLB",
                    use_selection=True,
                    export_draco_mesh_compression_enable=True,
                    export_draco_mesh_compression_level=6,
                )
                print(f"  Exportiert: {filepath}")

        # Komplett
        bpy.ops.object.select_all(action='SELECT')
        filepath = os.path.join(EXPORT_PATH, "cat_anatomy_complete.glb")
        bpy.ops.export_scene.gltf(
            filepath=filepath, export_format="GLB",
            use_selection=True,
            export_draco_mesh_compression_enable=True,
        )
        print(f"  Exportiert: {filepath}")

    print("=== Katze fertig! ===")


if __name__ == "__main__":
    main()
