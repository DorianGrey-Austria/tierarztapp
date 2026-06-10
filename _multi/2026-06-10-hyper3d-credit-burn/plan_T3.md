# Plan T3 — Equipment-Spezialist

Session: 2026-06-10-hyper3d-credit-burn | Terminal: T3 | Projekt: tierarztapp
Root: /Users/cardrevolution/Desktop/coding/tierarztapp
Status-Pfad: /Users/cardrevolution/Desktop/coding/tierarztapp/_multi/2026-06-10-hyper3d-credit-burn/status_T3.json

## Ziel
80 Hyper3D Credits in veterinaermedizinische 3D-Assets umsetzen. T3 generiert Diagnose-Instrumente (11), chirurgische Instrumente (10), Behandlungs-Equipment (9), grosse Geraete (7) und fehlende Tierarten (7) — insgesamt 44 Modelle.

## Persona
Du bist ein **Veterinaer-Equipment-Spezialist**. Du generierst medizinische Instrumente, Geraete und fehlende Tiermodelle ueber die Hyper3D Rodin API.

## Aufgaben
| # | Task | Akzeptanz |
|---|------|-----------|
| 1 | vet_rodin_lane.py von T1 wiederverwenden (oder eigenes erstellen) | Script importiert pferdehof-Pipeline |
| 2 | Output-Verzeichnisse anlegen | instruments/<category>/, animals/<species>/ |
| 3 | Queue starten (44 Modelle, ~22 Credits) | Lane laeuft, generiert sequentiell |
| 4 | GLBs in Kategorie-Unterordner sortieren | Instruments/Equipment/Animals getrennt |
| 5 | Fehlende Tierarten in Manifest registrieren | manifest.json aktualisiert |

## Pipeline-Setup
```bash
python3 scripts/vet_rodin_lane.py \
  --queue _multi/2026-06-10-hyper3d-credit-burn/queue_T3.json \
  --state _multi/2026-06-10-hyper3d-credit-burn/rodin_state_T3.json \
  --out-dir assets/models \
  --max-credits 26 --reserve 0
```

## Output-Mapping
- `vet_equip_*` → `assets/models/instruments/<category>/` oder `assets/models/equipment/`
- `vet_animal_*` → `assets/models/animals/<species>/`

## Ownership
**Write:** assets/models/instruments/**, assets/models/equipment/**, assets/models/animals/chicken/**, assets/models/animals/sugar-glider/**, assets/models/animals/mouse/**, assets/models/animals/gecko/**, assets/models/animals/bearded-dragon/**, assets/models/animals/rooster/**, assets/models/animals/duckling/**, _multi/.../queue_T3.json, _multi/.../rodin_state_T3.json
**Read-Only:** alles andere

## Gates
Keine — sofort starten.

## Regeln
1. NUR eigene Dateien editieren
2. Status-JSON nach jeder Aufgabe aktualisieren
3. Bestehende GLBs NICHT ueberschreiben
4. Error Budget: 3 gleiche Fails → STOP
5. Reserve: 0 (Credits verfallen morgen)

## Done
- [ ] Alle Queue-Eintraege abgearbeitet (oder Budget erschoepft)
- [ ] GLBs validiert
- [ ] Fehlende Tiere (chicken, sugar_glider, mouse, gecko, bearded_dragon, rooster, duckling) generiert
- [ ] status_T3.json auf COMPLETED

## Start
`/run m3`
