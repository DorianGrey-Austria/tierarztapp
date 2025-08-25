
import bpy
from pathlib import Path

# Export the donut scene
export_dir = Path('/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports')
export_dir.mkdir(exist_ok=True)

# Select all objects for export
bpy.ops.object.select_all(action='SELECT')

# Export as GLB
export_file = export_dir / 'glucksfall_donut.glb'
bpy.ops.export_scene.gltf(
    filepath=str(export_file),
    export_format='GLB',
    export_apply=True,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6
)

print(f"✅ Glücksfall donut exported to: {export_file}")

# Also render an image
render_file = export_dir / 'glucksfall_donut_render.png'
bpy.context.scene.render.filepath = str(render_file)
bpy.context.scene.render.resolution_x = 1024
bpy.context.scene.render.resolution_y = 1024
bpy.ops.render.render(write_still=True)

print(f"✅ Donut rendered to: {render_file}")
