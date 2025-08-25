
import bpy
print("BLENDER_TEST: Script executed successfully")
print(f"BLENDER_TEST: Scene has {len(bpy.data.objects)} objects")

# Create a simple test object
bpy.ops.mesh.primitive_cube_add(location=(1, 1, 1))
test_obj = bpy.context.object
test_obj.name = "Claude_Test_Cube"

print(f"BLENDER_TEST: Created object {test_obj.name}")
print("BLENDER_TEST: Test completed successfully")
