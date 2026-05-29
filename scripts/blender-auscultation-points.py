"""
Blender Script: Auskultationspunkte-Marker
Erstellt 3D-Marker an den korrekten Auskultationsstellen
fuer Herz- und Lungenauskultation bei Hund, Katze und Pferd.

Die Marker werden als farbcodierte Kugeln platziert:
- Rot: Herz-Auskultationspunkte
- Blau: Lungen-Auskultationspunkte

Ausfuehrung: Blender -> Scripting -> Open -> Run Script
Voraussetzung: Tiermodell muss bereits in der Szene sein.
"""

import bpy
import os
from mathutils import Vector

EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/"
)


def create_marker_material(name, color, emission_strength=2.0):
    """Erstelle leuchtendes Marker-Material."""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (400, 0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (0, 100)
    emission.inputs[0].default_value = (*color, 1.0)
    emission.inputs[1].default_value = emission_strength

    glass = nodes.new("ShaderNodeBsdfGlass")
    glass.location = (0, -100)
    glass.inputs["Color"].default_value = (*color, 1.0)

    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (200, 0)
    mix.inputs[0].default_value = 0.3

    links.new(glass.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])

    return mat


def create_marker(name, location, material, size=0.03, collection=None):
    """Erstelle einen einzelnen Auskultationsmarker."""
    bpy.ops.mesh.primitive_uv_sphere_add(
        segments=16, ring_count=8,
        radius=size, location=location
    )
    marker = bpy.context.active_object
    marker.name = name
    marker.data.materials.append(material)
    for face in marker.data.polygons:
        face.use_smooth = True

    if collection:
        for col in marker.users_collection:
            col.objects.unlink(marker)
        collection.objects.link(marker)

    return marker


def create_text_label(text, location, size=0.02, collection=None):
    """Erstelle ein 3D-Textlabel."""
    bpy.ops.object.text_add(location=location)
    label = bpy.context.active_object
    label.data.body = text
    label.data.size = size
    label.name = f"Label_{text.replace(' ', '_')}"

    if collection:
        for col in label.users_collection:
            col.objects.unlink(label)
        collection.objects.link(label)

    return label


def create_dog_auscultation_points():
    """Auskultationspunkte Hund."""
    col = bpy.data.collections.new("Hund_Auskultation")
    bpy.context.scene.collection.children.link(col)

    mat_heart = create_marker_material("Herz_Marker", (1.0, 0.2, 0.2))
    mat_lung = create_marker_material("Lunge_Marker", (0.2, 0.4, 1.0))
    mat_special = create_marker_material("Spezial_Marker", (0.2, 0.8, 0.3))

    # Hund-Proportionen (Seitenansicht, links)
    # ICR = Interkostalraum (Rippenzwischenraum)
    # Referenzpunkt: Schultergelenk ca. bei (0.6, 0.25, 0.7)

    heart_points = [
        # (Name, Position, Klinische Bedeutung)
        ("Mitralklappe_5ICR", (0.35, 0.25, 0.6),
         "Mitralklappe: Links, 5. ICR, Hoehe Ellbogengelenk. "
         "Haeufigster Auskultationspunkt fuer Mitralinsuffizienz."),
        ("Aortenklappe_4ICR", (0.4, 0.25, 0.7),
         "Aortenklappe: Links, 4. ICR cranial. "
         "Subaortenstenose hoerbar."),
        ("Pulmonalklappe_3ICR", (0.45, 0.25, 0.75),
         "Pulmonalklappe: Links, 3. ICR. "
         "Pulmonalstenose, PDA."),
        ("Trikuspidalklappe_rechts", (0.4, -0.25, 0.6),
         "Trikuspidalklappe: Rechts, 3.-4. ICR. "
         "Trikuspidalinsuffizienz."),
    ]

    lung_points = [
        ("Lunge_cranio_dorsal_L", (0.5, 0.3, 0.8),
         "Cranio-dorsal links: Normales Vesikulaeratmen. "
         "Verschaerft bei Bronchitis."),
        ("Lunge_cranio_ventral_L", (0.5, 0.3, 0.55),
         "Cranio-ventral links: Lungenoedem beginnt hier. "
         "Knistern bei Oedem/Pneumonie."),
        ("Lunge_caudo_dorsal_L", (0.2, 0.3, 0.8),
         "Caudo-dorsal links: Verschaerftes Atemgeraeusch "
         "bei Pneumonie/Neoplasie."),
        ("Lunge_cranio_dorsal_R", (0.5, -0.3, 0.8),
         "Cranio-dorsal rechts: Vergleichsseite. "
         "Asymmetrie beachten!"),
        ("Lunge_caudo_dorsal_R", (0.2, -0.3, 0.8),
         "Caudo-dorsal rechts: Bei Pleuraerguss "
         "Daempfung ventral."),
    ]

    for name, loc, desc in heart_points:
        marker = create_marker(f"Hund_{name}", loc, mat_heart, size=0.025,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    for name, loc, desc in lung_points:
        marker = create_marker(f"Hund_{name}", loc, mat_lung, size=0.02,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    print(f"Hund: {len(heart_points)} Herz- und {len(lung_points)} Lungenpunkte erstellt")
    return col


def create_cat_auscultation_points():
    """Auskultationspunkte Katze."""
    col = bpy.data.collections.new("Katze_Auskultation")
    bpy.context.scene.collection.children.link(col)

    mat_heart = create_marker_material("Katze_Herz_Marker", (1.0, 0.3, 0.3))
    mat_lung = create_marker_material("Katze_Lunge_Marker", (0.3, 0.5, 1.0))

    # Katze: Herz etwas weiter cranial, kleinerer Thorax
    heart_points = [
        ("Mitralklappe", (0.28, 0.18, 0.48),
         "Mitralklappe: Links, 5.-6. ICR. "
         "Bei HCM: systolisches Geraeusch, ggf. Galopprhythmus (S3)."),
        ("Aortenklappe", (0.32, 0.18, 0.55),
         "Aortenklappe: Links, 4. ICR. "
         "Dynamische LVOT-Obstruktion bei HCM."),
        ("Pulmonalklappe", (0.35, 0.18, 0.58),
         "Pulmonalklappe: Links, 2.-3. ICR. "
         "Katze: KEINE respiratorische Sinusarrhythmie normal!"),
        ("Trikuspidalklappe", (0.3, -0.18, 0.48),
         "Trikuspidalklappe: Rechts, 3.-4. ICR."),
    ]

    lung_points = [
        ("Lunge_L_cranial", (0.38, 0.2, 0.6),
         "Craniales Lungenfeld links. "
         "Giemen bei felinem Asthma."),
        ("Lunge_L_caudal", (0.15, 0.2, 0.6),
         "Caudales Lungenfeld links. "
         "Daempfung bei Pleuraerguss (haeufig bei FIP, Lymphom)."),
        ("Lunge_R_cranial", (0.38, -0.2, 0.6),
         "Craniales Lungenfeld rechts."),
        ("Lunge_R_caudal", (0.15, -0.2, 0.6),
         "Caudales Lungenfeld rechts."),
    ]

    for name, loc, desc in heart_points:
        marker = create_marker(f"Katze_{name}", loc, mat_heart, size=0.018,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    for name, loc, desc in lung_points:
        marker = create_marker(f"Katze_{name}", loc, mat_lung, size=0.015,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    print(f"Katze: {len(heart_points)} Herz- und {len(lung_points)} Lungenpunkte")
    return col


def create_horse_auscultation_points():
    """Auskultationspunkte Pferd."""
    col = bpy.data.collections.new("Pferd_Auskultation")
    bpy.context.scene.collection.children.link(col)

    mat_heart = create_marker_material("Pferd_Herz_Marker", (0.9, 0.15, 0.15))
    mat_lung = create_marker_material("Pferd_Lunge_Marker", (0.15, 0.35, 0.9))
    mat_gi = create_marker_material("Pferd_GI_Marker", (0.8, 0.6, 0.1))

    heart_points = [
        ("Mitralklappe", (0.8, 0.4, 1.65),
         "Mitralklappe: Links, 5. ICR. "
         "Haeufigste Klappeninsuffizienz beim Pferd."),
        ("Aortenklappe", (0.9, 0.4, 1.75),
         "Aortenklappe: Links, 4. ICR. "
         "Physiologisches systolisches Geraeusch moeglich!"),
        ("Pulmonalklappe", (1.0, 0.4, 1.8),
         "Pulmonalklappe: Links, 3. ICR. "
         "S3 und S4 koennen beim Pferd NORMAL sein!"),
        ("Trikuspidalklappe", (0.85, -0.4, 1.65),
         "Trikuspidalklappe: Rechts, 3.-4. ICR."),
    ]

    lung_points = [
        ("Lunge_L_dorsal", (0.5, 0.45, 2.0),
         "Dorsales Lungenfeld links: "
         "Pfeifen bei RAO (Recurrent Airway Obstruction)."),
        ("Lunge_L_ventral", (0.5, 0.45, 1.5),
         "Ventrales Lungenfeld links. "
         "Daempfung bei Pleuritis/Erguss."),
        ("Lunge_R_dorsal", (0.5, -0.45, 2.0),
         "Dorsales Lungenfeld rechts."),
        ("Lunge_rebreathing", (0.7, 0.45, 1.8),
         "Rebreathing-Stelle: Normales Atemgeraeusch "
         "erst nach Plastiktuete hoerbar (atemstimulierende Probe)."),
    ]

    # GI-Auskultation (beim Pferd wichtig fuer Kolik!)
    gi_points = [
        ("Caecum", (-0.3, -0.4, 1.5),
         "Caecum: Rechte Flanke, Hungergrube. "
         "Normaler Caecum-Klang: 'Wasserfall-Geraeusch'. "
         "Fehlen = Alarmsignal bei Kolik!"),
        ("Grosses_Kolon_ventral", (-0.5, 0.4, 1.2),
         "Ventrales grosses Kolon links. "
         "Darmgeraeusche bei Kolik beurteilen: "
         "erhoehte, reduziert oder fehlend."),
        ("Grosses_Kolon_dorsal", (-0.5, 0.4, 1.6),
         "Dorsales grosses Kolon links. "
         "Metallische Klingelgeraeusche = Gas im Darm."),
        ("Duenndarm", (-0.2, -0.4, 1.3),
         "Duenndarm-Auskultation rechts. "
         "Hochfrequente Geraeusche bei Ileus."),
    ]

    for name, loc, desc in heart_points:
        marker = create_marker(f"Pferd_{name}", loc, mat_heart, size=0.05,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    for name, loc, desc in lung_points:
        marker = create_marker(f"Pferd_{name}", loc, mat_lung, size=0.04,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    for name, loc, desc in gi_points:
        marker = create_marker(f"Pferd_{name}", loc, mat_gi, size=0.04,
                               collection=col)
        marker["klinische_bedeutung"] = desc

    print(f"Pferd: {len(heart_points)} Herz-, {len(lung_points)} Lungen-, "
          f"{len(gi_points)} GI-Punkte")
    return col


def main():
    print("=== VetScan Auskultationspunkte ===")

    create_dog_auscultation_points()
    create_cat_auscultation_points()
    create_horse_auscultation_points()

    print("")
    print("Alle Auskultationspunkte erstellt!")
    print("Jeder Marker hat ein Custom Property 'klinische_bedeutung'")
    print("mit der klinischen Beschreibung.")
    print("")
    print("Tipp: Im Outliner die Collections ein-/ausblenden")
    print("um nach Tierart zu filtern.")


if __name__ == "__main__":
    main()
