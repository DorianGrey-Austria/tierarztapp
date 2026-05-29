"""
Blender Script: Chirurgische Landmarken und Inzisionslinien
Erstellt 3D-Markierungen fuer haeufige chirurgische Zugaenge
auf einem Hundemodell.

Beinhaltet:
- Inzisionslinien (Bezier-Kurven)
- Anatomische Landmarken (Marker-Kugeln)
- Gefaess-/Nervenverlaeufe (farbige Linien)
- OP-Gebiet-Markierungen (transparente Flaechen)

Ausfuehrung: Blender -> Scripting -> Open -> Run Script
"""

import bpy
import math
import os

EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/dog/"
)


def create_material(name, color, alpha=1.0, emission=0.0):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    mat.blend_method = 'ALPHA_BLEND' if alpha < 1.0 else 'OPAQUE'
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()
    output = nodes.new("ShaderNodeOutputMaterial")
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)
    bsdf.inputs["Alpha"].default_value = alpha
    if emission > 0:
        bsdf.inputs["Emission Strength"].default_value = emission
        bsdf.inputs["Emission Color"].default_value = (*color, 1.0)
    links.new(bsdf.outputs["BSDF"], output.inputs["Surface"])
    return mat


def create_incision_line(name, points, color=(1, 0.3, 0.1), width=0.008):
    """Erstelle eine Inzisionslinie als Bezier-Kurve."""
    curve_data = bpy.data.curves.new(name=name, type='CURVE')
    curve_data.dimensions = '3D'
    curve_data.resolution_u = 12
    curve_data.bevel_depth = width
    curve_data.bevel_resolution = 4

    spline = curve_data.splines.new('BEZIER')
    spline.bezier_points.add(len(points) - 1)

    for i, point in enumerate(points):
        bp = spline.bezier_points[i]
        bp.co = point
        bp.handle_type_left = 'AUTO'
        bp.handle_type_right = 'AUTO'

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)

    mat = create_material(f"Mat_{name}", color, emission=1.5)
    obj.data.materials.append(mat)

    return obj


def create_landmark(name, location, color=(1, 1, 0), size=0.015):
    """Erstelle einen anatomischen Landmarken-Marker."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=12, ring_count=6, radius=size, location=location
    )
    obj = bpy.context.active_object
    obj.name = name
    mat = create_material(f"Mat_{name}", color, emission=2.0)
    obj.data.materials.append(mat)
    for face in obj.data.polygons:
        face.use_smooth = True
    return obj


def create_op_zone(name, location, scale, color=(0.2, 0.8, 0.3)):
    """Erstelle eine transparente OP-Gebiet-Markierung."""
    bpy.ops.mesh.primitive_plane_add(size=1.0, location=location)
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = scale
    mat = create_material(f"Mat_{name}", color, alpha=0.25, emission=0.5)
    obj.data.materials.append(mat)
    return obj


def create_median_laparotomy():
    """Mediane Laparotomie -- Standardzugang Abdomen."""
    col = bpy.data.collections.new("OP_Mediane_Laparotomie")
    bpy.context.scene.collection.children.link(col)

    # Inzisionslinie entlang Linea alba (ventral, Mittellinie)
    incision = create_incision_line(
        "Inzision_Median",
        points=[
            (0.3, 0, 0.35),   # Processus xiphoideus
            (0.1, 0, 0.35),   # Mitte
            (-0.2, 0, 0.35),  # Nabel
            (-0.5, 0, 0.35),  # Kaudal
        ],
        color=(1.0, 0.2, 0.1),
        width=0.005,
    )
    for c in incision.users_collection:
        c.objects.unlink(incision)
    col.objects.link(incision)

    # Landmarken
    landmarks = [
        ("Processus_xiphoideus", (0.35, 0, 0.38), (1, 1, 0)),
        ("Nabel", (-0.2, 0, 0.38), (1, 1, 0)),
        ("Pubis", (-0.6, 0, 0.38), (1, 1, 0)),
    ]
    for name, loc, color in landmarks:
        lm = create_landmark(name, loc, color)
        for c in lm.users_collection:
            c.objects.unlink(lm)
        col.objects.link(lm)

    # OP-Zone
    zone = create_op_zone("Zone_Median", (0, 0, 0.34), (0.9, 0.08, 1))
    for c in zone.users_collection:
        c.objects.unlink(zone)
    col.objects.link(zone)

    print("Mediane Laparotomie erstellt")


def create_lateral_approach_femur():
    """Lateraler Zugang Femur -- Orthopaedischer Standard."""
    col = bpy.data.collections.new("OP_Lateraler_Femur")
    bpy.context.scene.collection.children.link(col)

    # Inzisionslinie lateral am Oberschenkel
    incision = create_incision_line(
        "Inzision_Femur_Lateral",
        points=[
            (-0.45, 0.28, 0.7),  # Proximal (Trochanter major)
            (-0.5, 0.28, 0.55),  # Mitte
            (-0.55, 0.28, 0.4),  # Distal (Kniegelenk)
        ],
        color=(1.0, 0.2, 0.1),
    )
    for c in incision.users_collection:
        c.objects.unlink(incision)
    col.objects.link(incision)

    # Trochanter major Landmarke
    lm = create_landmark("Trochanter_major", (-0.45, 0.28, 0.72), (1, 1, 0))
    for c in lm.users_collection:
        c.objects.unlink(lm)
    col.objects.link(lm)

    # N. ischiadicus Verlauf (CAVE!)
    nerve = create_incision_line(
        "N_Ischiadicus_CAVE",
        points=[
            (-0.42, 0.22, 0.72),
            (-0.48, 0.2, 0.55),
            (-0.52, 0.18, 0.4),
        ],
        color=(1.0, 1.0, 0.0),  # Gelb fuer Nerven
        width=0.004,
    )
    for c in nerve.users_collection:
        c.objects.unlink(nerve)
    col.objects.link(nerve)
    nerve["CAVE"] = "N. ischiadicus: Dorsal/kaudal des Femurschafts. Bei Verletzung: Hinterhandlaehmung!"

    print("Lateraler Femur-Zugang erstellt")


def create_ovh_approach():
    """OVH (Ovariohysterektomie) -- Haeufigste Weichteil-OP."""
    col = bpy.data.collections.new("OP_OVH")
    bpy.context.scene.collection.children.link(col)

    # Inzision: kaudal des Nabels, Mittellinie
    incision = create_incision_line(
        "Inzision_OVH",
        points=[
            (-0.15, 0, 0.35),
            (-0.35, 0, 0.35),
        ],
        color=(1.0, 0.2, 0.1),
        width=0.005,
    )
    for c in incision.users_collection:
        c.objects.unlink(incision)
    col.objects.link(incision)

    # Nabel-Landmarke
    lm = create_landmark("Nabel_OVH", (-0.2, 0, 0.38), (1, 1, 0))
    for c in lm.users_collection:
        c.objects.unlink(lm)
    col.objects.link(lm)

    # A. ovarica (Arterie rot)
    artery_l = create_incision_line(
        "A_Ovarica_Links",
        points=[
            (-0.15, 0.15, 0.6),
            (-0.25, 0.1, 0.5),
        ],
        color=(0.9, 0.1, 0.1),
        width=0.003,
    )
    for c in artery_l.users_collection:
        c.objects.unlink(artery_l)
    col.objects.link(artery_l)

    artery_r = create_incision_line(
        "A_Ovarica_Rechts",
        points=[
            (-0.15, -0.15, 0.6),
            (-0.25, -0.1, 0.5),
        ],
        color=(0.9, 0.1, 0.1),
        width=0.003,
    )
    for c in artery_r.users_collection:
        c.objects.unlink(artery_r)
    col.objects.link(artery_r)

    # Uterus-Schema
    uterus = create_incision_line(
        "Uterus_Schema",
        points=[
            (-0.2, 0.12, 0.45),
            (-0.3, 0.08, 0.42),
            (-0.4, 0, 0.4),
            (-0.3, -0.08, 0.42),
            (-0.2, -0.12, 0.45),
        ],
        color=(0.9, 0.5, 0.6),
        width=0.006,
    )
    for c in uterus.users_collection:
        c.objects.unlink(uterus)
    col.objects.link(uterus)

    # CAVE: Ureter
    ureter = create_incision_line(
        "Ureter_CAVE",
        points=[
            (-0.15, 0.13, 0.6),
            (-0.45, 0.05, 0.4),
        ],
        color=(0.2, 0.8, 0.2),
        width=0.002,
    )
    for c in ureter.users_collection:
        c.objects.unlink(ureter)
    col.objects.link(ureter)
    ureter["CAVE"] = "Ureter: Bei Uterusstumpf-Ligatur NICHT mitfassen! Kaudal des Ovars verlaufen."

    print("OVH-Zugang erstellt")


def create_tracheotomy_approach():
    """Ventraler Hals-Zugang fuer Laryngotomie/Tracheotomie."""
    col = bpy.data.collections.new("OP_Tracheotomie")
    bpy.context.scene.collection.children.link(col)

    # Ventrale Halsinzision
    incision = create_incision_line(
        "Inzision_Hals_Ventral",
        points=[
            (0.9, 0, 0.7),
            (0.75, 0, 0.65),
            (0.6, 0, 0.6),
        ],
        color=(1.0, 0.2, 0.1),
        width=0.005,
    )
    for c in incision.users_collection:
        c.objects.unlink(incision)
    col.objects.link(incision)

    # Trachealringe
    for i in range(6):
        x = 0.85 - i * 0.04
        bpy.ops.mesh.primitive_torus_add(
            major_radius=0.035, minor_radius=0.005,
            location=(x, 0, 0.66)
        )
        ring = bpy.context.active_object
        ring.name = f"Trachealring_{i+1}"
        ring.rotation_euler = (0, math.pi / 2, 0)
        mat = create_material(f"Trachea_{i}", (0.9, 0.85, 0.8))
        ring.data.materials.append(mat)
        for c in ring.users_collection:
            c.objects.unlink(ring)
        col.objects.link(ring)

    # V. jugularis (CAVE!)
    for side, y in [("L", 0.08), ("R", -0.08)]:
        vein = create_incision_line(
            f"V_Jugularis_{side}",
            points=[
                (0.95, y, 0.72),
                (0.7, y, 0.62),
                (0.5, y, 0.55),
            ],
            color=(0.2, 0.2, 0.9),  # Blau fuer Venen
            width=0.004,
        )
        for c in vein.users_collection:
            c.objects.unlink(vein)
        col.objects.link(vein)
        vein["CAVE"] = "V. jugularis: Lateral der Inzision! Nicht verletzen."

    # N. recurrens (CAVE!)
    nerve = create_incision_line(
        "N_Recurrens_CAVE",
        points=[
            (0.9, 0.03, 0.68),
            (0.7, 0.03, 0.63),
        ],
        color=(1.0, 1.0, 0.0),
        width=0.003,
    )
    for c in nerve.users_collection:
        c.objects.unlink(nerve)
    col.objects.link(nerve)
    nerve["CAVE"] = "N. laryngeus recurrens: Verlaeuft dorsolateral der Trachea. Schonung essentiell!"

    print("Tracheotomie-Zugang erstellt")


def main():
    print("=== VetScan Chirurgische Landmarken ===")

    create_median_laparotomy()
    create_lateral_approach_femur()
    create_ovh_approach()
    create_tracheotomy_approach()

    print("")
    print("4 chirurgische Zugaenge mit Landmarken erstellt:")
    print("  1. Mediane Laparotomie")
    print("  2. Lateraler Femur-Zugang")
    print("  3. OVH (Ovariohysterektomie)")
    print("  4. Tracheotomie / Laryngotomie")
    print("")
    print("Farbcodierung:")
    print("  Rot = Inzisionslinien")
    print("  Gelb = Nerven (CAVE!)")
    print("  Blau = Venen")
    print("  Gruen = OP-Zone / Ureter")

    # Export
    if os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH, exist_ok=True)
        bpy.ops.object.select_all(action='SELECT')
        filepath = os.path.join(EXPORT_PATH, "dog_surgical_landmarks.glb")
        bpy.ops.export_scene.gltf(
            filepath=filepath, export_format="GLB",
            use_selection=True,
            export_draco_mesh_compression_enable=True,
        )
        print(f"Exportiert: {filepath}")


if __name__ == "__main__":
    main()
