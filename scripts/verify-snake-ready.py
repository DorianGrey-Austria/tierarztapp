#!/usr/bin/env python3
"""
Verification script to ensure snake model creation is ready
"""

import os

def verify_directories():
    """Verify all required directories exist"""
    directories = [
        "/Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/snake",
        "/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports",
        "/Users/doriangrey/Desktop/coding/tierarztspiel/scripts"
    ]
    
    print("🔍 Verifying directory structure...")
    all_good = True
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - MISSING!")
            all_good = False
    
    return all_good

def verify_scripts():
    """Verify required scripts exist"""
    scripts = [
        "/Users/doriangrey/Desktop/coding/tierarztspiel/BLENDER-EXPORT-SNAKE-MANUAL.py",
        "/Users/doriangrey/Desktop/coding/tierarztspiel/scripts/create-medical-snake.py"
    ]
    
    print("\n🐍 Verifying snake creation scripts...")
    all_good = True
    
    for script in scripts:
        if os.path.exists(script):
            print(f"✅ {os.path.basename(script)}")
        else:
            print(f"❌ {os.path.basename(script)} - MISSING!")
            all_good = False
    
    return all_good

def main():
    print("🐍 MEDICAL SNAKE MODEL VERIFICATION")
    print("="*50)
    
    dir_ok = verify_directories()
    script_ok = verify_scripts()
    
    print("\n📋 MEDICAL SNAKE SPECIFICATIONS:")
    print("- 120+ vertebrae segments (anatomically accurate)")
    print("- Forked tongue with detailed structure")
    print("- Flexible jaw for swallowing mechanism")
    print("- Elongated internal organs (heart, stomach, liver, kidneys)")
    print("- 5000-8000 polygon optimization")
    print("- 5 Medical visualization materials:")
    print("  • Python Pattern (realistic scales)")
    print("  • X-Ray (vertebral column visibility)")
    print("  • Ultrasound (medical scanning)")
    print("  • Thermal (heat sensing - infrared detection)")
    print("  • MRI (tissue differentiation)")
    
    print("\n🎯 NEXT STEPS:")
    print("1. Open Blender GUI")
    print("2. Go to Scripting tab")
    print("3. Text → New")
    print("4. Copy content from: BLENDER-EXPORT-SNAKE-MANUAL.py")
    print("5. Run Script (▶️)")
    print("6. Model will be exported to:")
    print("   - /Users/doriangrey/Desktop/coding/tierarztspiel/assets/models/animals/snake/snake_medical.glb")
    print("   - /Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/snake_medical.glb")
    
    if dir_ok and script_ok:
        print("\n🎉 ALL SYSTEMS READY FOR MEDICAL SNAKE CREATION!")
    else:
        print("\n⚠️ Some components missing - check errors above")
    
    print("="*50)

if __name__ == "__main__":
    main()