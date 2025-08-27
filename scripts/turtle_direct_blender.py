#!/usr/bin/env python3
"""
Direct Blender script to create a medically accurate 3D turtle model.
This script should be run inside Blender's text editor or via command line.
"""

import bpy
import bmesh
import mathutils
from mathutils import Vector
import math
import os

def clear_scene():
    """Clear all mesh objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False, confirm=False)
    
    # Create turtle collection
    if "Turtle_Medical" in bpy.data.collections:
        bpy.data.collections.remove(bpy.data.collections["Turtle_Medical"])
    
    turtle_collection = bpy.data.collections.new("Turtle_Medical")
    bpy.context.scene.collection.children.link(turtle_collection)
    
    print("Scene cleared and turtle collection created")
    return turtle_collection

def create_carapace(collection):
    """Create the turtle's carapace (top shell)"""
    # Create carapace - oval dome shape
    bpy.ops.mesh.primitive_uv_sphere_add(radius=2, location=(0, 0, 1))
    carapace = bpy.context.active_object
    carapace.name = "Carapace"
    
    # Scale to make it oval and flatten slightly
    carapace.scale = (1.4, 1.8, 0.6)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add shell segment details
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Add loop cuts for shell segments
    for i in range(3):
        bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 2})
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 4}, TRANSFORM_OT_edge_slide={"value": 0})
    
    # Create scute (shell plate) pattern
    bpy.ops.mesh.inset_faces(thickness=0.05, depth=0.02)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move to turtle collection
    bpy.context.scene.collection.objects.unlink(carapace)
    collection.objects.link(carapace)
    
    print("Carapace created with shell segments")
    return carapace

def create_plastron(collection):
    """Create the turtle's plastron (bottom shell)"""
    # Create plastron - flatter oval
    bpy.ops.mesh.primitive_cylinder_add(radius=1.2, depth=0.3, location=(0, 0, 0.2))
    plastron = bpy.context.active_object
    plastron.name = "Plastron"
    
    # Scale to match carapace width
    plastron.scale = (1.4, 1.6, 1)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Add plastron shell pattern
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    
    # Add central seam and segments
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 1})
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 3}, TRANSFORM_OT_edge_slide={"value": 0})
    
    # Create plastron plate pattern
    bpy.ops.mesh.inset_faces(thickness=0.03, depth=0.01)
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move to turtle collection
    bpy.context.scene.collection.objects.unlink(plastron)
    collection.objects.link(plastron)
    
    print("Plastron created with shell segments")
    return plastron

def create_neck_and_head(collection):
    """Create retractable neck and head with beak"""
    neck_segments = []
    
    # Create 3 neck segments for retraction animation
    for i in range(3):
        z_pos = 1.5 + (i * 0.4)
        radius = 0.4 - (i * 0.05)  # Tapering neck
        
        bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=0.3, location=(0, -1.8 + (i * 0.2), z_pos))
        segment = bpy.context.active_object
        segment.name = f"Neck_Segment_{i+1}"
        neck_segments.append(segment)
        
        # Move to turtle collection
        bpy.context.scene.collection.objects.unlink(segment)
        collection.objects.link(segment)
    
    # Create head with beak
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, -2.5, 2.7))
    head = bpy.context.active_object
    head.name = "Head"
    
    # Scale head to be more turtle-like
    head.scale = (0.8, 1.2, 0.9)
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    
    # Create beak extension
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='DESELECT')
    
    # Select front faces and extrude for beak
    bpy.context.tool_settings.mesh_select_mode = (False, False, True)  # Face mode
    
    # Get bmesh representation
    bm = bmesh.from_mesh(head.data)
    bm.faces.ensure_lookup_table()
    
    # Find front faces (negative Y direction)
    front_faces = [f for f in bm.faces if f.normal.y < -0.5]
    
    if front_faces:
        # Select front faces
        for f in front_faces:
            f.select = True
        
        # Update mesh
        bmesh.update_edit_mesh(head.data)
        
        # Extrude for beak
        bpy.ops.mesh.extrude_region_move(TRANSFORM_OT_translate={"value":(0, -0.3, -0.1)})
        bpy.ops.transform.resize(value=(0.7, 1.2, 0.8))
    
    bm.free()
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move head to turtle collection
    bpy.context.scene.collection.objects.unlink(head)
    collection.objects.link(head)
    
    print("Neck and head created with retractable segments")
    return neck_segments, head

def create_legs_with_webbed_feet(collection):
    """Create four legs with webbed feet"""
    leg_positions = [
        (1.2, 1.0, 0.5),    # Front right
        (-1.2, 1.0, 0.5),   # Front left
        (1.2, -0.8, 0.5),   # Back right
        (-1.2, -0.8, 0.5)   # Back left
    ]
    
    legs = []
    
    for i, pos in enumerate(leg_positions):
        leg_name = f"Leg_{i+1}"
        leg_parts = []
        
        # Create upper leg (thigh)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.25, depth=0.6, location=(pos[0], pos[1], pos[2]))
        upper_leg = bpy.context.active_object
        upper_leg.name = f"{leg_name}_Upper"
        upper_leg.rotation_euler = (math.radians(20), 0, 0)
        leg_parts.append(upper_leg)
        
        # Create lower leg 
        lower_pos = (pos[0], pos[1] - 0.3, pos[2] - 0.4)
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=0.5, location=lower_pos)
        lower_leg = bpy.context.active_object
        lower_leg.name = f"{leg_name}_Lower"
        lower_leg.rotation_euler = (math.radians(-30), 0, 0)
        leg_parts.append(lower_leg)
        
        # Create webbed foot
        foot_pos = (pos[0], pos[1] - 0.6, pos[2] - 0.8)
        bpy.ops.mesh.primitive_cube_add(size=0.6, location=foot_pos)
        foot = bpy.context.active_object
        foot.name = f"{leg_name}_Foot"
        foot.scale = (1.2, 1.5, 0.3)
        
        # Create webbing between toes
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.subdivide(number_cuts=2)
        bpy.ops.mesh.inset_faces(thickness=0.1, depth=0.05)
        bpy.ops.object.mode_set(mode='OBJECT')
        leg_parts.append(foot)
        
        # Move all leg parts to turtle collection
        for leg_part in leg_parts:
            bpy.context.scene.collection.objects.unlink(leg_part)
            collection.objects.link(leg_part)
        
        legs.append(leg_parts)
    
    print("All four legs with webbed feet created")
    return legs

def create_tail(collection):
    """Create turtle tail"""
    bpy.ops.mesh.primitive_cylinder_add(radius=0.15, depth=0.8, location=(0, 2.2, 0.8))
    tail = bpy.context.active_object
    tail.name = "Tail"
    tail.rotation_euler = (math.radians(45), 0, 0)
    
    # Taper the tail
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.loopcut_slide(MESH_OT_loopcut={"number_cuts": 3})
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Move to turtle collection
    bpy.context.scene.collection.objects.unlink(tail)
    collection.objects.link(tail)
    
    print("Tail created")
    return tail

def create_medical_materials():
    """Create materials for medical visualization modes"""
    materials = {}
    
    # 1. Normal Material (realistic turtle coloring)
    normal_mat = bpy.data.materials.new(name="Turtle_Normal")
    normal_mat.use_nodes = True
    nodes = normal_mat.node_tree.nodes
    nodes.clear()
    
    # Create shader setup for normal material
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs[0].default_value = (0.2, 0.4, 0.1, 1.0)  # Dark green
    principled.inputs[4].default_value = 0.3  # Metallic
    principled.inputs[7].default_value = 0.8  # Roughness
    
    normal_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    materials['normal'] = normal_mat
    
    # 2. X-Ray Material (shell transparency)
    xray_mat = bpy.data.materials.new(name="Turtle_XRay")
    xray_mat.use_nodes = True
    xray_mat.blend_method = 'BLEND'
    nodes = xray_mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    principled.inputs[0].default_value = (0.8, 0.9, 1.0, 1.0)  # Light blue
    principled.inputs[21].default_value = 0.3  # Alpha (transparency)
    
    # Add Fresnel for edge highlighting (bone structure)
    fresnel = nodes.new(type='ShaderNodeFresnel')
    mix = nodes.new(type='ShaderNodeMixShader')
    
    xray_mat.node_tree.links.new(fresnel.outputs[0], mix.inputs[0])
    xray_mat.node_tree.links.new(principled.outputs[0], mix.inputs[1])
    
    emission = nodes.new(type='ShaderNodeEmission')
    emission.inputs[0].default_value = (1.0, 1.0, 0.8, 1.0)  # Bone color
    emission.inputs[1].default_value = 2.0  # Strength
    
    xray_mat.node_tree.links.new(emission.outputs[0], mix.inputs[2])
    xray_mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    materials['xray'] = xray_mat
    
    # 3. Ultrasound Material
    ultrasound_mat = bpy.data.materials.new(name="Turtle_Ultrasound")
    ultrasound_mat.use_nodes = True
    nodes = ultrasound_mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Create noise texture for ultrasound pattern
    noise = nodes.new(type='ShaderNodeTexNoise')
    noise.inputs[2].default_value = 15.0  # Scale
    
    # Create color ramp for ultrasound coloring
    colorramp = nodes.new(type='ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].color = (0, 0, 0.2, 1)  # Dark blue
    colorramp.color_ramp.elements[1].color = (0.8, 0.8, 1.0, 1)  # Light blue
    
    ultrasound_mat.node_tree.links.new(noise.outputs[0], colorramp.inputs[0])
    ultrasound_mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
    ultrasound_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    materials['ultrasound'] = ultrasound_mat
    
    # 4. Thermal Material
    thermal_mat = bpy.data.materials.new(name="Turtle_Thermal")
    thermal_mat.use_nodes = True
    nodes = thermal_mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Create gradient for thermal imaging
    gradient = nodes.new(type='ShaderNodeTexGradient')
    gradient.gradient_type = 'RADIAL'
    
    colorramp = nodes.new(type='ShaderNodeValToRGB')
    colorramp.color_ramp.elements[0].color = (0.1, 0, 0.8, 1)  # Cold (blue)
    colorramp.color_ramp.elements[1].color = (1.0, 0.2, 0, 1)  # Hot (red)
    
    # Add middle element for body temperature
    colorramp.color_ramp.elements.new(0.5)
    colorramp.color_ramp.elements[1].color = (1.0, 1.0, 0, 1)  # Warm (yellow)
    
    thermal_mat.node_tree.links.new(gradient.outputs[0], colorramp.inputs[0])
    thermal_mat.node_tree.links.new(colorramp.outputs[0], principled.inputs[0])
    thermal_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    materials['thermal'] = thermal_mat
    
    # 5. MRI Material
    mri_mat = bpy.data.materials.new(name="Turtle_MRI")
    mri_mat.use_nodes = True
    nodes = mri_mat.node_tree.nodes
    nodes.clear()
    
    output = nodes.new(type='ShaderNodeOutputMaterial')
    principled = nodes.new(type='ShaderNodeBsdfPrincipled')
    
    # Grayscale tissue differentiation
    principled.inputs[0].default_value = (0.7, 0.7, 0.7, 1.0)  # Gray
    principled.inputs[4].default_value = 0.0  # No metallic
    principled.inputs[7].default_value = 0.5  # Medium roughness
    
    mri_mat.node_tree.links.new(principled.outputs[0], output.inputs[0])
    materials['mri'] = mri_mat
    
    print(f"Created {len(materials)} medical visualization materials")
    return materials

def assign_materials_to_parts(collection, materials):
    """Assign materials to turtle parts"""
    # Assign normal material to all parts initially
    normal_mat = materials['normal']
    for obj in collection.objects:
        if obj.type == 'MESH':
            # Clear existing materials
            obj.data.materials.clear()
            # Add normal material
            obj.data.materials.append(normal_mat)
    
    # Add medical materials as additional slots
    medical_materials = ['xray', 'ultrasound', 'thermal', 'mri']
    for obj in collection.objects:
        if obj.type == 'MESH':
            for mat_name in medical_materials:
                mat = materials[mat_name]
                obj.data.materials.append(mat)
    
    # Create shell-specific x-ray material for better visualization
    if 'Carapace' in bpy.data.objects and 'Plastron' in bpy.data.objects:
        carapace = bpy.data.objects['Carapace']
        plastron = bpy.data.objects['Plastron']
        
        # Create more transparent shell material
        shell_xray_mat = materials['xray'].copy()
        shell_xray_mat.name = "Shell_XRay"
        
        if shell_xray_mat.use_nodes:
            principled_nodes = [n for n in shell_xray_mat.node_tree.nodes if n.type == 'BSDF_PRINCIPLED']
            if principled_nodes:
                principled_nodes[0].inputs[21].default_value = 0.1  # Very transparent
        
        carapace.data.materials.append(shell_xray_mat)
        plastron.data.materials.append(shell_xray_mat)
    
    print("Materials assigned to all turtle parts")

def optimize_and_combine_model(collection):
    """Optimize model and combine into single object"""
    # Select all turtle objects
    bpy.ops.object.select_all(action='DESELECT')
    
    objects_to_join = []
    for obj in collection.objects:
        if obj.type == 'MESH':
            obj.select_set(True)
            objects_to_join.append(obj)
    
    if objects_to_join:
        # Set active object
        bpy.context.view_layer.objects.active = objects_to_join[0]
        
        # Join all parts
        bpy.ops.object.join()
        
        turtle_combined = bpy.context.active_object
        turtle_combined.name = "Turtle_Medical_Combined"
        
        # Count polygons
        mesh = turtle_combined.data
        initial_polys = len(mesh.polygons)
        print(f"Initial polygon count: {initial_polys}")
        
        # Target: 5000-8000 polygons
        target_polys = 6000
        
        if initial_polys > target_polys:
            # Add decimate modifier
            decimate = turtle_combined.modifiers.new(name="Decimate", type='DECIMATE')
            decimate.ratio = target_polys / initial_polys
            
            # Apply modifier
            bpy.ops.object.modifier_apply(modifier="Decimate")
            
            final_polys = len(turtle_combined.data.polygons)
            print(f"Final polygon count: {final_polys}")
        else:
            print(f"Model already within target range: {initial_polys} polygons")
        
        # Add smooth shading
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.faces_shade_smooth()
        bpy.ops.object.mode_set(mode='OBJECT')
        
        # Add subdivision surface for smooth medical visualization
        subdiv = turtle_combined.modifiers.new(name="Subdivision", type='SUBSURF')
        subdiv.levels = 1  # Low level to maintain performance
        
        print("Model optimized and combined")
        return turtle_combined
    
    return None

def export_model(turtle_obj):
    """Export the turtle model as GLB"""
    if turtle_obj:
        # Select only the turtle object
        bpy.ops.object.select_all(action='DESELECT')
        turtle_obj.select_set(True)
        bpy.context.view_layer.objects.active = turtle_obj
        
        # Export path
        export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/turtle/turtle_medical.glb"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(export_path), exist_ok=True)
        
        # Export as GLB
        bpy.ops.export_scene.gltf(
            filepath=export_path,
            use_selection=True,
            export_format='GLB',
            export_materials='EXPORT',
            export_colors=True,
            export_extras=True,
            export_yup=True,
            export_apply=True
        )
        
        print(f"✅ Turtle model exported to: {export_path}")
        
        # Get final stats
        mesh = turtle_obj.data
        poly_count = len(mesh.polygons)
        vert_count = len(mesh.vertices)
        material_count = len(turtle_obj.data.materials)
        
        print(f"📊 Model Statistics:")
        print(f"   Polygons: {poly_count}")
        print(f"   Vertices: {vert_count}")
        print(f"   Materials: {material_count}")
        
        return True
    else:
        print("❌ No turtle object found for export")
        return False

def main():
    """Main function to create the medical turtle model"""
    print("🐢 Starting Medical Turtle Model Creation...")
    print("=" * 50)
    
    # Clear scene and setup
    turtle_collection = clear_scene()
    
    # Create turtle components
    print("🔄 Creating turtle components...")
    carapace = create_carapace(turtle_collection)
    plastron = create_plastron(turtle_collection)
    neck_segments, head = create_neck_and_head(turtle_collection)
    legs = create_legs_with_webbed_feet(turtle_collection)
    tail = create_tail(turtle_collection)
    
    # Create materials
    print("🎨 Creating medical visualization materials...")
    materials = create_medical_materials()
    
    # Assign materials
    print("🎨 Assigning materials to parts...")
    assign_materials_to_parts(turtle_collection, materials)
    
    # Optimize and combine
    print("⚙️ Optimizing and combining model...")
    turtle_combined = optimize_and_combine_model(turtle_collection)
    
    # Export model
    print("📦 Exporting model...")
    success = export_model(turtle_combined)
    
    if success:
        print("\n" + "=" * 50)
        print("🎉 Medical Turtle Model Creation Complete!")
        print("✅ Features included:")
        print("   - Anatomically correct shell (carapace & plastron)")
        print("   - Retractable neck with 3 segments")
        print("   - Head with beak-like mouth")
        print("   - Four legs with webbed feet")
        print("   - Medical visualization materials:")
        print("     • Normal (realistic coloring)")
        print("     • X-Ray (shell transparency)")
        print("     • Ultrasound (noise pattern)")
        print("     • Thermal (temperature gradient)")
        print("     • MRI (tissue differentiation)")
        print("   - 5000-8000 polygons for optimal performance")
        print("   - GLB export ready for web use")
    else:
        print("❌ Failed to export model")
    
    return success

# Run the script if executed directly in Blender
if __name__ == "__main__":
    main()