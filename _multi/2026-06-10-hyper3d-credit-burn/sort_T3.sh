#!/usr/bin/env bash
# sort_T3.sh — Sort generated GLBs into category subdirectories
# Run from project root after generation completes.

set -uo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SRC="$ROOT/assets/models"

moved=0
skipped=0
missing=0

move_glb() {
  local file="$1" dest="$2"
  local base; base="$(basename "$file")"
  if [[ -f "$file" ]]; then
    mkdir -p "$dest"
    if [[ -f "$dest/$base" ]]; then
      echo "  SKIP $base (already in $dest)"
      skipped=$((skipped + 1))
    else
      mv "$file" "$dest/$base"
      echo "  MOVE $base -> $dest/"
      moved=$((moved + 1))
    fi
  else
    missing=$((missing + 1))
  fi
}

echo "=== Sorting T3 GLBs ==="

# --- Diagnostic Instruments (11) ---
DIAG="$SRC/instruments/diagnostic"
for name in blood_pressure reflex_hammer penlight pulse_oximeter glucometer \
            microscope centrifuge test_tubes blood_smear urine_dipstick xray_viewer; do
  move_glb "$SRC/vet_equip_${name}.glb" "$DIAG"
done

# --- Surgical Instruments (10) ---
SURG="$SRC/instruments/surgical"
for name in hemostats scissors_metzenbaum needle_holder retractor_balfour \
            suture_needle electrocautery surgical_drape iv_catheter \
            endotracheal_tube laryngoscope; do
  move_glb "$SRC/vet_equip_${name}.glb" "$SURG"
done

# --- Treatment Equipment (9) ---
TREAT="$SRC/instruments/treatment"
for name in iv_fluid_bag bandage_roll splint e_collar muzzle \
            nail_clippers dental_scaler feeding_tube wound_care_kit; do
  move_glb "$SRC/vet_equip_${name}.glb" "$TREAT"
done

# --- Large Equipment (7) ---
EQUIP="$SRC/equipment"
for name in xray_machine ultrasound_machine surgery_table anesthesia_machine \
            dental_unit autoclave examination_table; do
  move_glb "$SRC/vet_equip_${name}.glb" "$EQUIP"
done

# --- Animals (7) ---
move_glb "$SRC/vet_animal_chicken.glb"        "$SRC/animals/chicken"
move_glb "$SRC/vet_animal_rooster.glb"        "$SRC/animals/rooster"
move_glb "$SRC/vet_animal_sugar_glider.glb"   "$SRC/animals/sugar-glider"
move_glb "$SRC/vet_animal_mouse.glb"          "$SRC/animals/mouse"
move_glb "$SRC/vet_animal_duckling.glb"       "$SRC/animals/duckling"
move_glb "$SRC/vet_animal_gecko.glb"          "$SRC/animals/gecko"
move_glb "$SRC/vet_animal_bearded_dragon.glb" "$SRC/animals/bearded-dragon"

echo ""
echo "Done: $moved moved, $skipped skipped, $missing missing (not generated)"
