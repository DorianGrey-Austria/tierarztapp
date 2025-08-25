#!/usr/bin/env python3
"""
Blender Export Watcher - Überwacht Export-Ordner für neue GLB Dateien
LÄUFT AUSSERHALB von Blender und importiert automatisch neue Exports

Workflow:
1. User exportiert aus Blender GUI nach watched_exports/
2. Dieses Script erkennt neue GLB Datei
3. Kopiert automatisch nach models/animals/dog/medium/
4. Aktualisiert bello_claude_desktop.glb
"""

import os
import shutil
import time
from pathlib import Path
from datetime import datetime
import hashlib

# Konfiguration
WATCH_DIR = Path("/Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports")
TARGET_DIR = Path("/Users/doriangrey/Desktop/coding/tierarztspiel/models/animals/dog/medium")
TARGET_FILE = TARGET_DIR / "bello_claude_desktop.glb"
CHECK_INTERVAL = 2  # Sekunden

def setup_directories():
    """Erstelle benötigte Ordner"""
    WATCH_DIR.mkdir(exist_ok=True)
    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    print(f"📁 Watch directory: {WATCH_DIR}")
    print(f"📁 Target directory: {TARGET_DIR}")

def get_file_hash(filepath):
    """Berechne MD5 Hash einer Datei"""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def watch_for_exports():
    """Überwache Ordner für neue GLB Exports"""
    print("👀 Watching for Blender exports...")
    print(f"💡 Export from Blender to: {WATCH_DIR}")
    print("🔄 Press Ctrl+C to stop\n")
    
    seen_files = {}
    
    while True:
        try:
            # Finde alle GLB Dateien im Watch-Ordner
            glb_files = list(WATCH_DIR.glob("*.glb")) + list(WATCH_DIR.glob("*.gltf"))
            
            for glb_file in glb_files:
                file_hash = get_file_hash(glb_file)
                
                # Neue oder geänderte Datei?
                if glb_file.name not in seen_files or seen_files[glb_file.name] != file_hash:
                    print(f"\n🎯 New export detected: {glb_file.name}")
                    print(f"📊 Size: {glb_file.stat().st_size / 1024:.1f} KB")
                    
                    # Backup alte Version falls vorhanden
                    if TARGET_FILE.exists():
                        backup_name = TARGET_FILE.parent / f"bello_backup_{datetime.now():%Y%m%d_%H%M%S}.glb"
                        shutil.copy2(TARGET_FILE, backup_name)
                        print(f"💾 Backup created: {backup_name.name}")
                    
                    # Kopiere neue Datei
                    shutil.copy2(glb_file, TARGET_FILE)
                    print(f"✅ Imported as: {TARGET_FILE.name}")
                    
                    # Optional: Kopiere auch nach verschiedene Qualitätsstufen
                    for quality in ["high", "low"]:
                        quality_dir = TARGET_DIR.parent / quality
                        quality_dir.mkdir(exist_ok=True)
                        quality_file = quality_dir / "bello_claude_desktop.glb"
                        shutil.copy2(glb_file, quality_file)
                        print(f"📦 Also copied to: {quality}/{quality_file.name}")
                    
                    # Update Hash
                    seen_files[glb_file.name] = file_hash
                    
                    print(f"🌐 Ready for browser testing!")
                    print(f"🔗 http://localhost:8081/vetscan-bello-3d-v7.html")
                    print("-" * 50)
            
            time.sleep(CHECK_INTERVAL)
            
        except KeyboardInterrupt:
            print("\n👋 Export watcher stopped")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            time.sleep(CHECK_INTERVAL)

def create_export_instruction():
    """Erstelle Anleitung für User"""
    instruction_file = WATCH_DIR / "HOW_TO_EXPORT.txt"
    instruction_content = f"""
🐕 BLENDER EXPORT ANLEITUNG
============================

1. In Blender (mit deinem Modell):
   File → Export → glTF 2.0 (.glb/.gltf)

2. Export Settings:
   - Format: glTF Binary (.glb) ✓
   - Include: Selected Objects ✓
   - Include: Materials ✓
   - Transform: +Y Up ✓

3. SPEICHERN IN DIESEM ORDNER:
   {WATCH_DIR}
   
4. Dateiname (egal welcher):
   - bello_export.glb
   - dog_model.glb
   - current_work.glb
   (Script erkennt automatisch alle .glb Dateien)

5. Script übernimmt automatisch:
   - Import nach models/animals/dog/
   - Backup alter Versionen
   - Bereit für Browser-Test

WATCHER LÄUFT! Exportiere einfach hierher.
"""
    
    with open(instruction_file, 'w') as f:
        f.write(instruction_content)
    
    print(f"📝 Instructions created: {instruction_file}")

if __name__ == "__main__":
    print("🚀 Blender Export Watcher v1.0")
    print("=" * 50)
    
    setup_directories()
    create_export_instruction()
    
    print("\n" + "=" * 50)
    print("📋 ANLEITUNG FÜR DICH:")
    print("1. Öffne Blender mit deinem Modell")
    print(f"2. File → Export → glTF 2.0")
    print(f"3. Speichere in: {WATCH_DIR}")
    print("4. Script importiert automatisch!")
    print("=" * 50 + "\n")
    
    watch_for_exports()