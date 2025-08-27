#!/usr/bin/env python3
"""
Verify that the turtle model was successfully exported.
"""

import os
import sys
from pathlib import Path

def verify_turtle_export():
    """Check if turtle model was successfully exported"""
    
    export_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/turtle/turtle_medical.glb"
    
    print("🔍 Checking turtle model export...")
    print("=" * 50)
    
    # Check if file exists
    if os.path.exists(export_path):
        file_stats = os.stat(export_path)
        file_size = file_stats.st_size
        
        print(f"✅ Turtle model successfully exported!")
        print(f"📍 Location: {export_path}")
        print(f"📏 File size: {file_size:,} bytes ({file_size / 1024 / 1024:.2f} MB)")
        print(f"🕒 Modified: {os.path.getmtime(export_path)}")
        
        # Basic size validation
        if file_size > 1000:  # At least 1KB
            print("✅ File size looks valid (>1KB)")
            
            # Check if it's likely a valid GLB file
            with open(export_path, 'rb') as f:
                header = f.read(4)
                if header == b'glTF':
                    print("✅ GLB file header validated")
                else:
                    print("⚠️  GLB header not found - file may be corrupted")
            
            return True
        else:
            print("❌ File too small - likely export failed")
            return False
    else:
        print(f"❌ Turtle model not found at: {export_path}")
        print("💡 Make sure to run the Blender script first!")
        print("📂 To run the script:")
        print("   1. Open Blender (running on PID 784)")
        print("   2. Go to Scripting tab")
        print("   3. Open BLENDER-TURTLE-SCRIPT.py")
        print("   4. Click 'Run Script'")
        return False

def check_directory_structure():
    """Verify directory structure is correct"""
    base_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals"
    turtle_dir = os.path.join(base_path, "turtle")
    
    print(f"\n📁 Directory structure check:")
    print(f"   Base: {'✅' if os.path.exists(base_path) else '❌'} {base_path}")
    print(f"   Turtle: {'✅' if os.path.exists(turtle_dir) else '❌'} {turtle_dir}")
    
    if os.path.exists(turtle_dir):
        contents = os.listdir(turtle_dir)
        print(f"   Contents: {contents}")

if __name__ == "__main__":
    check_directory_structure()
    success = verify_turtle_export()
    sys.exit(0 if success else 1)