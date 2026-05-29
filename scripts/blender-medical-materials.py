"""
Blender Script: Medizinische Visualisierungsmaterialien
Erstellt X-Ray, Ultrasound, Thermal und MRI Materialien
fuer alle VetScan 3D-Modelle.

Anwendung: Nach dem Laden eines Tiermodells dieses Script ausfuehren.
Es erstellt Materialkopien fuer jeden Visualisierungsmodus und
exportiert separate GLB-Dateien.

Ausfuehrung: Blender -> Scripting -> Open -> Run Script
"""

import bpy
import os

EXPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/"
)


def create_xray_material():
    """Roentgen-Material: Semi-transparent, blaeulich-weiss, Fresnel-Effekt."""
    mat = bpy.data.materials.new(name="VetScan_XRay")
    mat.use_nodes = True
    mat.blend_method = 'ALPHA_BLEND'
    mat.shadow_method = 'NONE'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (600, 0)

    # Fresnel fuer Kantenhervorhebung (wie echtes Roentgen)
    fresnel = nodes.new("ShaderNodeFresnel")
    fresnel.location = (-200, 200)
    fresnel.inputs[0].default_value = 1.8

    # Emission fuer den Leuchteffekt
    emission = nodes.new("ShaderNodeEmission")
    emission.location = (0, 200)
    emission.inputs[0].default_value = (0.75, 0.85, 1.0, 1.0)  # Blaeulich-weiss
    emission.inputs[1].default_value = 2.5  # Staerke

    # Transparent fuer den Durchsicht-Effekt
    transparent = nodes.new("ShaderNodeBsdfTransparent")
    transparent.location = (0, -100)

    # Mix: Fresnel steuert Transparenz vs. Emission
    mix = nodes.new("ShaderNodeMixShader")
    mix.location = (300, 0)

    # Invertieren fuer richtigen Effekt (Kanten hell, Mitte transparent)
    invert = nodes.new("ShaderNodeInvert")
    invert.location = (0, 100)

    links.new(fresnel.outputs[0], invert.inputs[1])
    links.new(invert.outputs[0], mix.inputs[0])
    links.new(transparent.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])

    return mat


def create_ultrasound_material():
    """Ultraschall-Material: Graustufen mit koerniger Textur."""
    mat = bpy.data.materials.new(name="VetScan_Ultrasound")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (800, 0)

    # Noise-Textur fuer Ultraschall-typisches Rauschen (Speckle)
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-400, 0)
    noise.inputs["Scale"].default_value = 50.0
    noise.inputs["Detail"].default_value = 8.0
    noise.inputs["Roughness"].default_value = 0.7

    # Zweite Noise-Ebene fuer feineres Rauschen
    noise2 = nodes.new("ShaderNodeTexNoise")
    noise2.location = (-400, -200)
    noise2.inputs["Scale"].default_value = 200.0
    noise2.inputs["Detail"].default_value = 4.0

    # Mix der beiden Rauschebenen
    mix_noise = nodes.new("ShaderNodeMixRGB")
    mix_noise.location = (-100, -100)
    mix_noise.inputs[0].default_value = 0.3
    mix_noise.blend_type = 'OVERLAY'

    # Graustufen-Mapping
    colorramp = nodes.new("ShaderNodeValToRGB")
    colorramp.location = (200, 0)
    # Dunkelgrau bis Hellgrau (Ultraschall-typisch)
    colorramp.color_ramp.elements[0].color = (0.05, 0.05, 0.08, 1.0)
    colorramp.color_ramp.elements[1].color = (0.6, 0.6, 0.65, 1.0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (500, 0)
    bsdf.inputs["Roughness"].default_value = 0.9
    bsdf.inputs["Specular IOR Level"].default_value = 0.0

    links.new(noise.outputs["Fac"], mix_noise.inputs[1])
    links.new(noise2.outputs["Fac"], mix_noise.inputs[2])
    links.new(mix_noise.outputs[0], colorramp.inputs[0])
    links.new(colorramp.outputs[0], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output.inputs[0])

    return mat


def create_thermal_material():
    """Thermographie-Material: Waermefarben (blau->gruen->gelb->rot->weiss)."""
    mat = bpy.data.materials.new(name="VetScan_Thermal")
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (800, 0)

    # Gradient basierend auf Objekthoehe (simuliert Waermeverteilung)
    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-600, 0)

    separate = nodes.new("ShaderNodeSeparateXYZ")
    separate.location = (-400, 0)

    # Noise fuer natuerliche Waermevariation
    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-400, -200)
    noise.inputs["Scale"].default_value = 8.0
    noise.inputs["Detail"].default_value = 4.0

    mix_val = nodes.new("ShaderNodeMixRGB")
    mix_val.location = (-100, 0)
    mix_val.inputs[0].default_value = 0.15

    # Waermefarbskala
    colorramp = nodes.new("ShaderNodeValToRGB")
    colorramp.location = (200, 0)

    ramp = colorramp.color_ramp
    # Blau (kalt)
    ramp.elements[0].position = 0.0
    ramp.elements[0].color = (0.0, 0.0, 0.5, 1.0)
    # Cyan
    e1 = ramp.elements.new(0.2)
    e1.color = (0.0, 0.5, 0.8, 1.0)
    # Gruen
    e2 = ramp.elements.new(0.4)
    e2.color = (0.0, 0.8, 0.2, 1.0)
    # Gelb
    e3 = ramp.elements.new(0.6)
    e3.color = (1.0, 0.9, 0.0, 1.0)
    # Rot
    e4 = ramp.elements.new(0.8)
    e4.color = (1.0, 0.2, 0.0, 1.0)
    # Weiss (heiss)
    ramp.elements[1].position = 1.0
    ramp.elements[1].color = (1.0, 1.0, 0.9, 1.0)

    emission = nodes.new("ShaderNodeEmission")
    emission.location = (500, 0)
    emission.inputs[1].default_value = 1.5

    links.new(texcoord.outputs["Object"], separate.inputs[0])
    links.new(separate.outputs["Z"], mix_val.inputs[1])
    links.new(noise.outputs["Fac"], mix_val.inputs[2])
    links.new(mix_val.outputs[0], colorramp.inputs[0])
    links.new(colorramp.outputs[0], emission.inputs[0])
    links.new(emission.outputs[0], output.inputs[0])

    return mat


def create_mri_material():
    """MRI-Material: Hoher Kontrast, Weichteil-Differenzierung."""
    mat = bpy.data.materials.new(name="VetScan_MRI")
    mat.use_nodes = True
    mat.blend_method = 'ALPHA_BLEND'

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    output = nodes.new("ShaderNodeOutputMaterial")
    output.location = (800, 0)

    # MRI zeigt Wasserstoffatome -> wasserreiches Gewebe hell
    texcoord = nodes.new("ShaderNodeTexCoord")
    texcoord.location = (-600, 0)

    noise = nodes.new("ShaderNodeTexNoise")
    noise.location = (-400, 0)
    noise.inputs["Scale"].default_value = 15.0
    noise.inputs["Detail"].default_value = 6.0
    noise.inputs["Roughness"].default_value = 0.5

    # MRI-typische Graustufen mit hohem Kontrast
    colorramp = nodes.new("ShaderNodeValToRGB")
    colorramp.location = (0, 0)

    ramp = colorramp.color_ramp
    ramp.elements[0].position = 0.0
    ramp.elements[0].color = (0.0, 0.0, 0.0, 1.0)
    e1 = ramp.elements.new(0.3)
    e1.color = (0.15, 0.15, 0.18, 1.0)
    e2 = ramp.elements.new(0.5)
    e2.color = (0.4, 0.4, 0.45, 1.0)
    e3 = ramp.elements.new(0.7)
    e3.color = (0.7, 0.7, 0.75, 1.0)
    ramp.elements[1].position = 1.0
    ramp.elements[1].color = (0.95, 0.95, 1.0, 1.0)

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (400, 0)
    bsdf.inputs["Roughness"].default_value = 1.0
    bsdf.inputs["Specular IOR Level"].default_value = 0.0
    bsdf.inputs["Alpha"].default_value = 0.85

    links.new(texcoord.outputs["Object"], noise.inputs["Vector"])
    links.new(noise.outputs["Fac"], colorramp.inputs[0])
    links.new(colorramp.outputs[0], bsdf.inputs["Base Color"])
    links.new(bsdf.outputs["BSDF"], output.inputs[0])

    return mat


def apply_material_to_all(material, prefix=""):
    """Wende Material auf alle Mesh-Objekte an."""
    for obj in bpy.data.objects:
        if obj.type == 'MESH':
            if prefix and not obj.name.startswith(prefix):
                continue
            if obj.data.materials:
                obj.data.materials[0] = material
            else:
                obj.data.materials.append(material)


def export_variant(species, variant_name, material):
    """Exportiere Modell mit spezifischem Material."""
    apply_material_to_all(material)

    species_dir = os.path.join(EXPORT_PATH, species)
    os.makedirs(species_dir, exist_ok=True)

    filepath = os.path.join(species_dir, f"{species}_{variant_name}.glb")

    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.export_scene.gltf(
        filepath=filepath,
        export_format="GLB",
        use_selection=True,
        export_draco_mesh_compression_enable=True,
        export_draco_mesh_compression_level=6,
    )
    print(f"Exportiert: {filepath}")


def main():
    """Erstelle alle medizinischen Materialien."""
    print("=== VetScan Medical Materials ===")

    xray = create_xray_material()
    ultrasound = create_ultrasound_material()
    thermal = create_thermal_material()
    mri = create_mri_material()

    print("Materialien erstellt:")
    print("  - VetScan_XRay (Roentgen)")
    print("  - VetScan_Ultrasound (Ultraschall)")
    print("  - VetScan_Thermal (Thermografie)")
    print("  - VetScan_MRI (Magnetresonanztomografie)")
    print("")
    print("Nutzung:")
    print("  1. Lade ein Tiermodell")
    print("  2. Waehle das Objekt")
    print("  3. Material-Tab -> Material zuweisen")
    print("  4. Waehle VetScan_XRay / _Ultrasound / _Thermal / _MRI")
    print("")
    print("Fuer automatischen Export aller Varianten:")
    print("  Kommentiere die export_variant() Aufrufe unten ein")
    print("  und passe den species-Namen an.")

    # Automatischer Export (auskommentiert - nach Bedarf aktivieren):
    # export_variant("bello", "xray", xray)
    # export_variant("bello", "ultrasound", ultrasound)
    # export_variant("bello", "thermal", thermal)
    # export_variant("bello", "mri", mri)

    print("=== Fertig! ===")


if __name__ == "__main__":
    main()
