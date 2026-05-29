"""
Blender Script: Anatomische Schichten Pferd
Erzeugt ein 4-Schichten-Modell fuer die Pferde-Anatomie.

Pferd-spezifische Anatomie:
- 18 BWK (statt 13 beim Hund), 6 LWK, 5 SWK
- Caecum sehr gross (30-35L Fassungsvermoegen)
- Grosses Kolon mit 4 Lagen
- Hufmechanismus (Huf statt Pfoten)
- Kein Schluesselbein

Ausfuehrung: Blender -> Scripting -> Open -> Run Script
"""

import bpy
import math
import os

EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/horse/"
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
    """Pferdekoerper -- gross, muskuloes, laengliche Proportionen."""
    mat = create_material("Pferd_Haut", (0.55, 0.35, 0.2), alpha=0.6)

    # Rumpf (deutlich groesser als Hund/Katze)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=32, ring_count=16, radius=1.0, location=(0, 0, 1.8)
    )
    body = bpy.context.active_object
    body.name = "Pferd_Rumpf"
    body.scale = (2.5, 0.9, 0.85)
    body.data.materials.append(mat)
    set_smooth(body)
    add_to_collection(body, collection)

    # Hals (lang, gebogen)
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=16, radius=0.35, depth=1.5,
        location=(2.2, 0, 2.3)
    )
    neck = bpy.context.active_object
    neck.name = "Pferd_Hals"
    neck.rotation_euler = (0, 0.8, 0)
    neck.data.materials.append(mat)
    set_smooth(neck)
    add_to_collection(neck, collection)

    # Kopf (lang, schmal)
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=24, ring_count=12, radius=0.3, location=(3.0, 0, 2.9)
    )
    head = bpy.context.active_object
    head.name = "Pferd_Kopf"
    head.scale = (1.8, 0.5, 0.6)
    head.data.materials.append(mat)
    set_smooth(head)
    add_to_collection(head, collection)

    # Nuestern/Maul
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6, radius=0.12, location=(3.55, 0, 2.75)
    )
    muzzle = bpy.context.active_object
    muzzle.name = "Pferd_Maul"
    muzzle.scale = (1.2, 0.8, 0.7)
    muzzle.data.materials.append(mat)
    set_smooth(muzzle)
    add_to_collection(muzzle, collection)

    # Ohren
    for side, y in [("L", 0.15), ("R", -0.15)]:
        bpy.ops.mesh.primitive_cone_add(
            vertices=10, radius1=0.06, depth=0.25,
            location=(2.95, y, 3.2)
        )
        ear = bpy.context.active_object
        ear.name = f"Pferd_Ohr_{side}"
        ear.data.materials.append(mat)
        set_smooth(ear)
        add_to_collection(ear, collection)

    # Schweif
    bpy.ops.mesh.primitive_cylinder_add(
        vertices=12, radius=0.06, depth=1.0,
        location=(-2.6, 0, 1.5)
    )
    tail = bpy.context.active_object
    tail.name = "Pferd_Schweif"
    tail.rotation_euler = (0, 0.5, 0)
    tail.data.materials.append(mat)
    set_smooth(tail)
    add_to_collection(tail, collection)

    # Beine (lang, kraeftig)
    leg_positions = [
        ("VL", 1.5, 0.4, 0.8),
        ("VR", 1.5, -0.4, 0.8),
        ("HL", -1.5, 0.4, 0.8),
        ("HR", -1.5, -0.4, 0.8),
    ]
    for name, x, y, z in leg_positions:
        # Oberschenkel/Oberarm
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=14, radius=0.15, depth=0.8,
            location=(x, y, z + 0.2)
        )
        upper = bpy.context.active_object
        upper.name = f"Pferd_Oberbein_{name}"
        upper.data.materials.append(mat)
        set_smooth(upper)
        add_to_collection(upper, collection)

        # Unterschenkel
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=14, radius=0.1, depth=0.8,
            location=(x, y, z - 0.5)
        )
        lower = bpy.context.active_object
        lower.name = f"Pferd_Unterbein_{name}"
        lower.data.materials.append(mat)
        set_smooth(lower)
        add_to_collection(lower, collection)

    # Hufe (statt Pfoten)
    mat_hoof = create_material("Pferd_Huf", (0.2, 0.15, 0.1), alpha=0.8)
    for name, x, y, _ in leg_positions:
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=16, radius=0.1, depth=0.12,
            location=(x, y, 0.06)
        )
        hoof = bpy.context.active_object
        hoof.name = f"Pferd_Huf_{name}"
        hoof.data.materials.append(mat_hoof)
        add_to_collection(hoof, collection)


def create_muscle_layer(collection):
    """Pferdemuskulatur -- stark ausgepraegt."""
    mat = create_material("Pferd_Muskel", (0.7, 0.2, 0.15), alpha=0.7)

    muscles = [
        ("Pferd_M_Trapezius", (0.5, 0, 2.1), (0.6, 0.6, 0.2)),
        ("Pferd_M_Latissimus", (-0.2, 0, 2.0), (0.8, 0.65, 0.15)),
        ("Pferd_M_Brachiocephalicus", (2.0, 0.15, 2.3), (0.5, 0.1, 0.12)),
        ("Pferd_M_Brachiocephalicus_R", (2.0, -0.15, 2.3), (0.5, 0.1, 0.12)),
        ("Pferd_M_Pectoralis", (1.2, 0, 1.3), (0.5, 0.5, 0.12)),
        ("Pferd_M_Serratus", (0.3, 0.3, 1.6), (0.6, 0.1, 0.3)),
        ("Pferd_M_Serratus_R", (0.3, -0.3, 1.6), (0.6, 0.1, 0.3)),
        ("Pferd_M_Obliquus", (-0.3, 0.25, 1.5), (0.5, 0.1, 0.25)),
        ("Pferd_M_Obliquus_R", (-0.3, -0.25, 1.5), (0.5, 0.1, 0.25)),
        ("Pferd_M_Gluteus_Med", (-1.3, 0.25, 2.0), (0.3, 0.15, 0.2)),
        ("Pferd_M_Gluteus_Med_R", (-1.3, -0.25, 2.0), (0.3, 0.15, 0.2)),
        ("Pferd_M_Semitendinosus", (-1.5, 0.3, 1.3), (0.1, 0.08, 0.35)),
        ("Pferd_M_Semitendinosus_R", (-1.5, -0.3, 1.3), (0.1, 0.08, 0.35)),
        ("Pferd_M_Gastrocnemius_L", (-1.5, 0.35, 0.7), (0.08, 0.06, 0.25)),
        ("Pferd_M_Gastrocnemius_R", (-1.5, -0.35, 0.7), (0.08, 0.06, 0.25)),
        ("Pferd_M_Deltoideus_L", (1.5, 0.3, 1.5), (0.12, 0.08, 0.15)),
        ("Pferd_M_Deltoideus_R", (1.5, -0.3, 1.5), (0.12, 0.08, 0.15)),
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
    """Pferdeorgane -- besonders grosser GI-Trakt."""
    organs = {
        "Pferd_Herz": {
            "color": (0.8, 0.1, 0.1), "loc": (1.0, 0.1, 1.7),
            "scale": (0.2, 0.15, 0.25)
        },
        "Pferd_Lunge_L": {
            "color": (0.85, 0.55, 0.6), "loc": (0.8, 0.3, 1.85),
            "scale": (0.5, 0.2, 0.35)
        },
        "Pferd_Lunge_R": {
            "color": (0.85, 0.55, 0.6), "loc": (0.8, -0.3, 1.85),
            "scale": (0.55, 0.22, 0.35)
        },
        "Pferd_Leber": {
            "color": (0.5, 0.15, 0.1), "loc": (0.4, 0, 1.5),
            "scale": (0.25, 0.4, 0.15)
        },
        "Pferd_Magen": {
            "color": (0.85, 0.7, 0.6), "loc": (0.3, 0.15, 1.5),
            "scale": (0.15, 0.12, 0.1)
        },
        "Pferd_Milz": {
            "color": (0.5, 0.1, 0.2), "loc": (0.2, 0.35, 1.5),
            "scale": (0.2, 0.06, 0.12)
        },
        # Grosses Caecum (30-35L!)
        "Pferd_Caecum": {
            "color": (0.7, 0.55, 0.4), "loc": (-0.3, 0.2, 1.3),
            "scale": (0.35, 0.2, 0.25)
        },
        # Grosses Kolon (4-lagig)
        "Pferd_Grosses_Kolon_Ventral": {
            "color": (0.75, 0.6, 0.5), "loc": (-0.2, 0, 1.15),
            "scale": (0.7, 0.3, 0.15)
        },
        "Pferd_Grosses_Kolon_Dorsal": {
            "color": (0.72, 0.58, 0.48), "loc": (-0.2, 0, 1.55),
            "scale": (0.65, 0.25, 0.12)
        },
        "Pferd_Kleines_Kolon": {
            "color": (0.68, 0.55, 0.45), "loc": (-0.5, 0, 1.35),
            "scale": (0.3, 0.2, 0.15)
        },
        "Pferd_Duenndarm": {
            "color": (0.9, 0.75, 0.65), "loc": (0.0, -0.1, 1.35),
            "scale": (0.4, 0.25, 0.15)
        },
        "Pferd_Niere_L": {
            "color": (0.6, 0.25, 0.2), "loc": (-0.1, 0.25, 1.85),
            "scale": (0.1, 0.07, 0.08)
        },
        "Pferd_Niere_R": {
            "color": (0.6, 0.25, 0.2), "loc": (0.1, -0.25, 1.88),
            "scale": (0.1, 0.07, 0.08)
        },
        "Pferd_Blase": {
            "color": (0.7, 0.7, 0.3), "loc": (-1.3, 0, 1.1),
            "scale": (0.12, 0.1, 0.1)
        },
    }

    for name, props in organs.items():
        mat = create_material(f"Organ_{name}", props["color"], alpha=0.85)
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=16, ring_count=8, radius=1.0, location=props["loc"]
        )
        obj = bpy.context.active_object
        obj.name = name
        obj.scale = props["scale"]
        obj.data.materials.append(mat)
        set_smooth(obj)
        add_to_collection(obj, collection)


def create_skeleton_layer(collection):
    """Pferdeskelett -- 18 BWK, 6 LWK, kein Schluesselbein."""
    mat = create_material("Pferd_Knochen", (0.95, 0.92, 0.85), alpha=0.9)

    # Wirbelsaeule: 7 HWK + 18 BWK + 6 LWK + 5 SWK = 36
    for i in range(36):
        x = 2.0 - i * 0.11
        z = 2.05 + math.sin(i * 0.08) * 0.05
        r = 0.04 if i < 7 else 0.05
        bpy.ops.mesh.primitive_cylinder_add(
            vertices=8, radius=r, depth=0.09,
            location=(x, 0, z)
        )
        vert = bpy.context.active_object
        region = "HWK" if i < 7 else "BWK" if i < 25 else "LWK" if i < 31 else "SWK"
        num = (i + 1) if i < 7 else (i - 6) if i < 25 else (i - 24) if i < 31 else (i - 30)
        vert.name = f"Pferd_{region}_{num}"
        vert.rotation_euler = (0, math.pi / 2, 0)
        vert.data.materials.append(mat)
        add_to_collection(vert, collection)

    # Schaedel
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8, radius=0.25, location=(2.95, 0, 2.9)
    )
    skull = bpy.context.active_object
    skull.name = "Pferd_Schaedel"
    skull.scale = (1.8, 0.5, 0.65)
    skull.data.materials.append(mat)
    set_smooth(skull)
    add_to_collection(skull, collection)

    # Rippen (18 Paare!)
    for i in range(18):
        x = 1.1 - i * 0.1
        for side, y_sign in [("L", 1), ("R", -1)]:
            bpy.ops.mesh.primitive_torus_add(
                major_radius=0.4, minor_radius=0.015,
                major_segments=24, minor_segments=6,
                location=(x, 0, 1.7)
            )
            rib = bpy.context.active_object
            rib.name = f"Pferd_Rippe_{i+1}_{side}"
            rib.scale = (0.2, 0.7 * y_sign, 0.9)
            rib.data.materials.append(mat)
            add_to_collection(rib, collection)

    # Scapula (gross, dreieckig)
    for side, y in [("L", 0.35), ("R", -0.35)]:
        bpy.ops.mesh.primitive_cone_add(
            vertices=12, radius1=0.25, depth=0.03,
            location=(1.4, y, 2.1)
        )
        scap = bpy.context.active_object
        scap.name = f"Pferd_Scapula_{side}"
        scap.rotation_euler = (0, 0.3, 0)
        scap.data.materials.append(mat)
        add_to_collection(scap, collection)

    # Vorderbein-Knochen
    for side, y in [("L", 0.35), ("R", -0.35)]:
        bones = [
            (f"Pferd_Humerus_{side}", (1.5, y, 1.3), 0.6, 0.06),
            (f"Pferd_Radius_{side}", (1.5, y, 0.7), 0.55, 0.04),
            (f"Pferd_Metacarpus_{side}", (1.5, y, 0.3), 0.3, 0.03),
        ]
        for name, loc, length, radius in bones:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8, radius=radius, depth=length, location=loc
            )
            bone = bpy.context.active_object
            bone.name = name
            bone.data.materials.append(mat)
            add_to_collection(bone, collection)

    # Hinterbein-Knochen
    for side, y in [("L", 0.35), ("R", -0.35)]:
        bones = [
            (f"Pferd_Femur_{side}", (-1.5, y, 1.3), 0.65, 0.07),
            (f"Pferd_Tibia_{side}", (-1.5, y, 0.65), 0.6, 0.045),
            (f"Pferd_Metatarsus_{side}", (-1.5, y, 0.25), 0.35, 0.035),
        ]
        for name, loc, length, radius in bones:
            bpy.ops.mesh.primitive_cylinder_add(
                vertices=8, radius=radius, depth=length, location=loc
            )
            bone = bpy.context.active_object
            bone.name = name
            bone.data.materials.append(mat)
            add_to_collection(bone, collection)

    # Pelvis
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6, radius=0.2, location=(-1.4, 0, 1.9)
    )
    pelvis = bpy.context.active_object
    pelvis.name = "Pferd_Pelvis"
    pelvis.scale = (0.8, 1.6, 0.5)
    pelvis.data.materials.append(mat)
    set_smooth(pelvis)
    add_to_collection(pelvis, collection)

    # Hufbein (in jedem Huf)
    mat_hoof = create_material("Pferd_Hufbein", (0.9, 0.88, 0.82), alpha=0.9)
    for name, x, y in [("VL", 1.5, 0.35), ("VR", 1.5, -0.35),
                        ("HL", -1.5, 0.35), ("HR", -1.5, -0.35)]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            segments=10, ring_count=5, radius=0.06, location=(x, y, 0.08)
        )
        hb = bpy.context.active_object
        hb.name = f"Pferd_Hufbein_{name}"
        hb.scale = (1.2, 0.8, 0.5)
        hb.data.materials.append(mat_hoof)
        set_smooth(hb)
        add_to_collection(hb, collection)


def main():
    print("=== VetScan Anatomy Layers: Pferd ===")
    clear_scene()

    col_skin = create_collection("Pferd_Haut")
    col_muscles = create_collection("Pferd_Muskulatur")
    col_organs = create_collection("Pferd_Organe")
    col_skeleton = create_collection("Pferd_Skelett")

    create_skin_layer(col_skin)
    create_muscle_layer(col_muscles)
    create_organ_layer(col_organs)
    create_skeleton_layer(col_skeleton)

    bpy.ops.object.camera_add(location=(5, -4, 3))
    cam = bpy.context.active_object
    cam.name = "Horse_Camera"
    cam.rotation_euler = (1.1, 0, 0.7)
    bpy.context.scene.camera = cam

    bpy.ops.object.light_add(type='SUN', location=(3, -2, 5))
    light = bpy.context.active_object
    light.name = "Horse_Light"
    light.data.energy = 4.0

    if EXPORT_ENABLED:
        os.makedirs(EXPORT_PATH, exist_ok=True)
        layers = [
            ("Pferd_Haut", "horse_skin.glb"),
            ("Pferd_Muskulatur", "horse_muscles.glb"),
            ("Pferd_Organe", "horse_organs.glb"),
            ("Pferd_Skelett", "horse_skeleton.glb"),
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
                )
                print(f"  Exportiert: {filepath}")

        bpy.ops.object.select_all(action='SELECT')
        filepath = os.path.join(EXPORT_PATH, "horse_anatomy_complete.glb")
        bpy.ops.export_scene.gltf(
            filepath=filepath, export_format="GLB",
            use_selection=True,
            export_draco_mesh_compression_enable=True,
        )
        print(f"  Exportiert: {filepath}")

    print("=== Pferd fertig! ===")
    print(f"Objekte: {len(bpy.data.objects)}")


if __name__ == "__main__":
    main()
