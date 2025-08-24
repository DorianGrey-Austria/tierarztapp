#!/usr/bin/env python3
"""
Create Placeholder GLB for Testing Claude Desktop Import
Generates a simple test GLB to verify the import pipeline works
"""

import struct
import json
import base64

def create_simple_cube_gltf():
    """Create a simple cube GLTF/GLB for testing"""
    
    # Vertices for a simple cube (positions)
    vertices = [
        # Front face
        -1.0, -1.0,  1.0,  # 0
         1.0, -1.0,  1.0,  # 1
         1.0,  1.0,  1.0,  # 2
        -1.0,  1.0,  1.0,  # 3
        # Back face
        -1.0, -1.0, -1.0,  # 4
         1.0, -1.0, -1.0,  # 5
         1.0,  1.0, -1.0,  # 6
        -1.0,  1.0, -1.0   # 7
    ]
    
    # Indices for cube triangles
    indices = [
        # Front
        0, 1, 2,  0, 2, 3,
        # Back
        4, 6, 5,  4, 7, 6,
        # Left
        4, 3, 7,  4, 0, 3,
        # Right
        1, 5, 6,  1, 6, 2,
        # Top
        3, 2, 6,  3, 6, 7,
        # Bottom
        4, 1, 0,  4, 5, 1
    ]
    
    # Normals for cube faces
    normals = [
        # Front face normals
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        0.0, 0.0, 1.0,
        # Back face normals
        0.0, 0.0, -1.0,
        0.0, 0.0, -1.0,
        0.0, 0.0, -1.0,
        0.0, 0.0, -1.0
    ]
    
    # Convert to bytes
    vertex_data = struct.pack(f'{len(vertices)}f', *vertices)
    index_data = struct.pack(f'{len(indices)}H', *indices)
    normal_data = struct.pack(f'{len(normals)}f', *normals)
    
    # Combine all binary data
    buffer_data = vertex_data + normal_data + index_data
    
    # Create GLTF JSON structure
    gltf = {
        "asset": {
            "version": "2.0",
            "generator": "VetScan Pro - Claude Desktop Placeholder"
        },
        "scene": 0,
        "scenes": [
            {
                "nodes": [0]
            }
        ],
        "nodes": [
            {
                "mesh": 0,
                "name": "PlaceholderBello"
            }
        ],
        "meshes": [
            {
                "primitives": [
                    {
                        "attributes": {
                            "POSITION": 0,
                            "NORMAL": 1
                        },
                        "indices": 2,
                        "material": 0
                    }
                ],
                "name": "BelloPlaceholder"
            }
        ],
        "materials": [
            {
                "name": "BelloFur",
                "pbrMetallicRoughness": {
                    "baseColorFactor": [0.8, 0.6, 0.4, 1.0],
                    "metallicFactor": 0.0,
                    "roughnessFactor": 0.8
                }
            }
        ],
        "accessors": [
            {
                "bufferView": 0,
                "componentType": 5126,  # FLOAT
                "count": 8,
                "type": "VEC3",
                "min": [-1.0, -1.0, -1.0],
                "max": [1.0, 1.0, 1.0]
            },
            {
                "bufferView": 1,
                "componentType": 5126,  # FLOAT
                "count": 8,
                "type": "VEC3"
            },
            {
                "bufferView": 2,
                "componentType": 5123,  # UNSIGNED_SHORT
                "count": 36,
                "type": "SCALAR"
            }
        ],
        "bufferViews": [
            {
                "buffer": 0,
                "byteOffset": 0,
                "byteLength": len(vertex_data)
            },
            {
                "buffer": 0,
                "byteOffset": len(vertex_data),
                "byteLength": len(normal_data)
            },
            {
                "buffer": 0,
                "byteOffset": len(vertex_data) + len(normal_data),
                "byteLength": len(index_data)
            }
        ],
        "buffers": [
            {
                "byteLength": len(buffer_data)
            }
        ]
    }
    
    return gltf, buffer_data

def create_glb_file(output_path):
    """Create a GLB file with placeholder dog model"""
    
    gltf_json, binary_data = create_simple_cube_gltf()
    
    # Convert JSON to bytes
    json_data = json.dumps(gltf_json, separators=(',', ':')).encode('utf-8')
    
    # Pad JSON to 4-byte boundary
    json_padding = (4 - (len(json_data) % 4)) % 4
    json_data += b' ' * json_padding
    
    # Pad binary data to 4-byte boundary  
    binary_padding = (4 - (len(binary_data) % 4)) % 4
    binary_data += b'\x00' * binary_padding
    
    # GLB header
    glb_header = struct.pack('<4sII', b'glTF', 2, 12 + 8 + len(json_data) + 8 + len(binary_data))
    
    # JSON chunk header
    json_chunk_header = struct.pack('<II4s', len(json_data), 0x4E4F534A, b'')  # JSON
    
    # Binary chunk header
    binary_chunk_header = struct.pack('<II4s', len(binary_data), 0x004E4942, b'')  # BIN
    
    # Write GLB file
    with open(output_path, 'wb') as f:
        f.write(glb_header)
        f.write(json_chunk_header)
        f.write(json_data)
        f.write(binary_chunk_header)
        f.write(binary_data)
    
    return True

if __name__ == "__main__":
    import os
    
    # Create placeholder for testing
    output_dir = "public/models/animals/dog/medium"
    os.makedirs(output_dir, exist_ok=True)
    
    output_path = f"{output_dir}/placeholder_test.glb"
    
    try:
        success = create_glb_file(output_path)
        if success:
            file_size = os.path.getsize(output_path)
            print(f"✅ Placeholder GLB created: {output_path}")
            print(f"📊 File size: {file_size} bytes")
            print(f"🎯 Purpose: Test Claude Desktop import pipeline")
            print(f"💡 Replace with real bello_claude_desktop.glb when ready")
        else:
            print("❌ Failed to create placeholder GLB")
    except Exception as e:
        print(f"❌ Error creating placeholder: {e}")