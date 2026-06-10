# Plan T1 — Organ-Spezialist

Session: 2026-06-10-hyper3d-credit-burn | Terminal: T1 | Projekt: tierarztapp
Root: /Users/cardrevolution/Desktop/coding/tierarztapp
Status-Pfad: /Users/cardrevolution/Desktop/coding/tierarztapp/_multi/2026-06-10-hyper3d-credit-burn/status_T1.json

## Ziel
80 Hyper3D Credits in veterinaermedizinische 3D-Assets umsetzen. T1 generiert gesunde Organe fuer 9 Spezies (cat, horse, cow, rabbit, bird, pig, sheep, goat, guinea_pig). Dog-Organe existieren bereits.

## Persona
Du bist ein **Veterinaeranatomie-Spezialist**. Du generierst anatomisch korrekte Organ-3D-Modelle ueber die Hyper3D Rodin API.

## Aufgaben
| # | Task | Akzeptanz |
|---|------|-----------|
| 1 | Lane-Script adaptieren (vet_rodin_lane.py) | Script laeuft, importiert aus pferdehof |
| 2 | Output-Verzeichnisse anlegen | assets/models/organs/{species}/ existieren |
| 3 | Queue starten (54 Modelle, ~27 Credits) | Lane laeuft, generiert sequentiell |
| 4 | GLBs in Spezies-Unterordner sortieren | Jede GLB in richtigem Ordner |
| 5 | Manifest aktualisieren | manifest.json oder Inventar-Log |

## Pipeline-Setup
```bash
# vet_rodin_lane.py erstellen — importiert aus pferdehof
# Kern-Funktionen: submit_generation, poll_until_done, download_glb, compress_glb, validate_glb
# Quelle: /Users/cardrevolution/Desktop/coding/pferdehof/scripts/rodin_batch_generate.py

# Starten:
python3 scripts/vet_rodin_lane.py \
  --queue _multi/2026-06-10-hyper3d-credit-burn/queue_T1.json \
  --state _multi/2026-06-10-hyper3d-credit-burn/rodin_state_T1.json \
  --out-dir assets/models/organs \
  --max-credits 27 --reserve 0
```

## Output-Mapping
GLBs landen als `assets/models/organs/vet_organ_<species>_<organ>.glb`, dann sortieren:
- `vet_organ_cat_*` → `assets/models/organs/heart/cat_heart.glb` etc.
- Oder flach in `assets/models/organs/<organ>/` belassen (bestehende Struktur)

## Ownership
**Write:** assets/models/organs/**, _multi/.../queue_T1.json, _multi/.../rodin_state_T1.json, scripts/vet_rodin_lane.py
**Read-Only:** alles andere
**Lock-Files:** nur T1

## Gates
Keine — sofort starten.

## Regeln
1. NUR eigene Dateien editieren
2. Status-JSON nach jeder Aufgabe aktualisieren
3. Bestehende GLBs NICHT ueberschreiben (skip wenn exists)
4. Error Budget: 3 gleiche Fails → STOP
5. Reserve: 0 (Credits verfallen morgen)

## Done
- [ ] vet_rodin_lane.py erstellt und funktionsfaehig
- [ ] Alle 54 Queue-Eintraege abgearbeitet (oder Budget erschoepft)
- [ ] GLBs validiert (magic bytes + size check)
- [ ] status_T1.json auf COMPLETED

## Start
`/run m1`
