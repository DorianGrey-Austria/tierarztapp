"""
Blender Master Pipeline: VetScan Pro 3D-Asset-Generierung
Orchestriert alle Blender-Skripte fuer die komplette 3D-Pipeline.

Dieses Script ruft alle anderen Blender-Skripte auf und
exportiert das Gesamtpaket in das assets/-Verzeichnis.

Ausfuehrung:
  Blender --background --python scripts/blender-master-pipeline.py

Oder interaktiv:
  Blender -> Scripting -> Open -> Run Script
"""

import bpy
import os
import sys
import importlib.util
import time
import json

SCRIPT_DIR = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/scripts/"
)
EXPORT_ROOT = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/animals/"
)
REPORT_PATH = os.path.expanduser(
    "~/Desktop/coding/tierarztapp/assets/models/pipeline_report.json"
)


def run_script(script_name):
    """Lade und fuehre ein Blender-Python-Script aus."""
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if not os.path.exists(script_path):
        print(f"WARNUNG: Script nicht gefunden: {script_path}")
        return False

    print(f"\n{'='*60}")
    print(f"Starte: {script_name}")
    print(f"{'='*60}")

    start = time.time()

    try:
        spec = importlib.util.spec_from_file_location(
            script_name.replace(".py", ""), script_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, 'main'):
            module.main()

        elapsed = time.time() - start
        print(f"Fertig: {script_name} ({elapsed:.1f}s)")
        return True

    except Exception as e:
        elapsed = time.time() - start
        print(f"FEHLER in {script_name} ({elapsed:.1f}s): {e}")
        return False


def count_objects():
    """Zaehle alle Objekte in der Szene."""
    meshes = sum(1 for o in bpy.data.objects if o.type == 'MESH')
    curves = sum(1 for o in bpy.data.objects if o.type == 'CURVE')
    lights = sum(1 for o in bpy.data.objects if o.type == 'LIGHT')
    cameras = sum(1 for o in bpy.data.objects if o.type == 'CAMERA')
    return {
        "meshes": meshes,
        "curves": curves,
        "lights": lights,
        "cameras": cameras,
        "total": len(bpy.data.objects),
    }


def count_exported_files():
    """Zaehle exportierte GLB-Dateien."""
    count = 0
    total_size = 0
    files = []
    for root, dirs, filenames in os.walk(EXPORT_ROOT):
        for f in filenames:
            if f.endswith('.glb'):
                path = os.path.join(root, f)
                size = os.path.getsize(path)
                count += 1
                total_size += size
                files.append({
                    "file": os.path.relpath(path, EXPORT_ROOT),
                    "size_kb": round(size / 1024, 1),
                })
    return count, total_size, files


def generate_report(results, duration):
    """Erstelle einen Pipeline-Report."""
    obj_counts = count_objects()
    glb_count, glb_size, glb_files = count_exported_files()

    report = {
        "pipeline": "VetScan Pro 3D Master Pipeline",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_seconds": round(duration, 1),
        "scripts": results,
        "scene_objects": obj_counts,
        "exported_files": {
            "count": glb_count,
            "total_size_mb": round(glb_size / (1024 * 1024), 2),
            "files": glb_files,
        },
        "status": "SUCCESS" if all(r["success"] for r in results) else "PARTIAL",
    }

    os.makedirs(os.path.dirname(REPORT_PATH), exist_ok=True)
    with open(REPORT_PATH, 'w') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    return report


def main():
    print("=" * 60)
    print("VetScan Pro 3D Master Pipeline")
    print("=" * 60)
    print(f"Script-Verzeichnis: {SCRIPT_DIR}")
    print(f"Export-Verzeichnis:  {EXPORT_ROOT}")
    print("")

    pipeline_start = time.time()

    # Pipeline-Reihenfolge:
    # 1. Anatomische Schichtmodelle (Hund, Katze, Pferd)
    # 2. Medizinische Materialien
    # 3. Auskultationspunkte
    # 4. Chirurgische Landmarken

    scripts = [
        {
            "file": "blender-anatomy-layers-dog.py",
            "description": "Anatomische Schichten Hund (4 Layer)",
            "phase": "anatomy",
        },
        {
            "file": "blender-anatomy-layers-cat.py",
            "description": "Anatomische Schichten Katze (4 Layer)",
            "phase": "anatomy",
        },
        {
            "file": "blender-anatomy-layers-horse.py",
            "description": "Anatomische Schichten Pferd (4 Layer)",
            "phase": "anatomy",
        },
        {
            "file": "blender-medical-materials.py",
            "description": "Medizinische Visualisierungsmaterialien (X-Ray, US, Thermal, MRI)",
            "phase": "materials",
        },
        {
            "file": "blender-auscultation-points.py",
            "description": "Auskultationspunkte (Hund, Katze, Pferd)",
            "phase": "clinical",
        },
        {
            "file": "blender-surgical-landmarks.py",
            "description": "Chirurgische Landmarken und Inzisionslinien",
            "phase": "surgical",
        },
    ]

    results = []
    for script_info in scripts:
        # Szene zwischen Scripts zuruecksetzen
        # (jedes Script erstellt seine eigene Szene)
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

        start = time.time()
        success = run_script(script_info["file"])
        elapsed = time.time() - start

        results.append({
            "file": script_info["file"],
            "description": script_info["description"],
            "phase": script_info["phase"],
            "success": success,
            "duration_seconds": round(elapsed, 1),
        })

    pipeline_duration = time.time() - pipeline_start

    # Report generieren
    report = generate_report(results, pipeline_duration)

    # Zusammenfassung
    print("\n" + "=" * 60)
    print("PIPELINE ZUSAMMENFASSUNG")
    print("=" * 60)
    print(f"Dauer: {pipeline_duration:.1f}s")
    print(f"Scripts: {len(results)}")
    print(f"Erfolgreich: {sum(1 for r in results if r['success'])}")
    print(f"Fehlgeschlagen: {sum(1 for r in results if not r['success'])}")
    print(f"")
    print(f"Exportierte GLB-Dateien: {report['exported_files']['count']}")
    print(f"Gesamtgroesse: {report['exported_files']['total_size_mb']} MB")
    print(f"")
    print(f"Report: {REPORT_PATH}")
    print("=" * 60)

    if report["status"] == "PARTIAL":
        print("\nWARNUNG: Nicht alle Scripts waren erfolgreich!")
        for r in results:
            if not r["success"]:
                print(f"  FEHLER: {r['file']} ({r['description']})")


if __name__ == "__main__":
    main()
