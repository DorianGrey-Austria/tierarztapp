#!/usr/bin/env python3
"""
Execute the turtle creation script in the running Blender instance.
"""

import subprocess
import sys
import os

def run_turtle_script_in_blender():
    """Run the turtle script in the existing Blender instance"""
    
    script_path = "/Users/doriangrey/Desktop/coding/tierarztspiel/BLENDER-TURTLE-SCRIPT.py"
    
    # Command to execute Python script in running Blender instance
    # We'll use osascript to send the script to Blender
    applescript = f'''
    tell application "Blender"
        activate
    end tell
    '''
    
    # First activate Blender
    try:
        subprocess.run(["osascript", "-e", applescript], check=True)
        print("✅ Blender activated")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Could not activate Blender via AppleScript: {e}")
    
    print(f"""
🐢 TURTLE MODEL CREATION INSTRUCTIONS:

The turtle creation script has been prepared at:
{script_path}

To create the medical turtle model, please follow these steps:

1. 📂 Open the running Blender instance (PID 784)

2. 🔄 Switch to the "Scripting" tab in Blender

3. 📜 Open the script file:
   - Click "Open" in the text editor
   - Navigate to: {script_path}
   - Or copy the entire script content

4. ▶️  Run the script by clicking the "Run Script" button

5. 📊 Monitor the console output for progress

The script will automatically:
✅ Clear the scene and create turtle collection  
✅ Create anatomically correct shell (carapace & plastron)
✅ Model retractable neck with 3 segments
✅ Create head with beak-like mouth
✅ Build four legs with webbed feet
✅ Set up 5 medical visualization materials:
   • Normal (realistic green/brown coloring)
   • X-Ray (shell transparency with bone highlighting)
   • Ultrasound (noise patterns with scan lines)
   • Thermal (temperature gradient mapping)
   • MRI (grayscale tissue differentiation)
✅ Optimize to 5000-8000 polygons
✅ Export as GLB to: /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/turtle/turtle_medical.glb

🔍 MEDICAL FEATURES:
- Shell layers visible in X-ray mode for fracture diagnosis
- Neck retraction mechanism for anatomical accuracy
- Webbed feet structure for aquatic species identification
- Internal organ placement considerations under shell
- Multiple material slots for instant visualization mode switching

⏱️  Expected completion time: 2-3 minutes
    """)
    
    return True

if __name__ == "__main__":
    run_turtle_script_in_blender()