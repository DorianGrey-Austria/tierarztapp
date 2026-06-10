# Plan T2 — Pathologie-Spezialist

Session: 2026-06-10-hyper3d-credit-burn | Terminal: T2 | Projekt: tierarztapp
Root: /Users/cardrevolution/Desktop/coding/tierarztapp
Status-Pfad: /Users/cardrevolution/Desktop/coding/tierarztapp/_multi/2026-06-10-hyper3d-credit-burn/status_T2.json

## Ziel
80 Hyper3D Credits in veterinaermedizinische 3D-Assets umsetzen. T2 generiert pathologische Organe (18), Parasiten (10) und Knochen/Skelett (20) — insgesamt 48 Modelle.

## Persona
Du bist ein **Veterinaerpathologie-Spezialist**. Du generierst pathologische Praeparate, Parasiten und Knochenmodelle ueber die Hyper3D Rodin API.

## Aufgaben
| # | Task | Akzeptanz |
|---|------|-----------|
| 1 | vet_rodin_lane.py von T1 wiederverwenden (oder eigenes erstellen) | Script importiert pferdehof-Pipeline |
| 2 | Output-Verzeichnisse anlegen | pathology/, parasites/, bones/ existieren |
| 3 | Queue starten (48 Modelle, ~24 Credits) | Lane laeuft, generiert sequentiell |
| 4 | GLBs in Kategorie-Unterordner sortieren | Pathologie/Parasiten/Knochen getrennt |

## Pipeline-Setup
```bash
python3 scripts/vet_rodin_lane.py \
  --queue _multi/2026-06-10-hyper3d-credit-burn/queue_T2.json \
  --state _multi/2026-06-10-hyper3d-credit-burn/rodin_state_T2.json \
  --out-dir assets/models \
  --max-credits 27 --reserve 0
```

## Output-Mapping
- `vet_path_*` → `assets/models/pathology/<condition>/`
- `vet_parasite_*` → `assets/models/parasites/`
- `vet_bone_*` → `assets/models/bones/`

## Ownership
**Write:** assets/models/pathology/**, assets/models/parasites/**, assets/models/bones/**, _multi/.../queue_T2.json, _multi/.../rodin_state_T2.json
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
- [ ] Parasiten + Knochen Verzeichnisse angelegt und befuellt
- [ ] status_T2.json auf COMPLETED

## Start
`/run m2`
