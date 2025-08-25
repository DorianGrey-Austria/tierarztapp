# 🔧 TROUBLESHOOTING - VetScan Pro 3000
**Letzte Aktualisierung: 25.08.2025 - Post Blender MCP Breakthrough**

---

## 🚀 QUICK FIXES - Die häufigsten Probleme

### Problem: "Blender MCP funktioniert nicht"
```bash
# LÖSUNG in 3 Schritten:
1. echo '{"mcpServers":{"blender-mcp":{"command":"uvx","args":["blender-mcp"]}}}' > .cursor/mcp.json
2. Cursor neustarten
3. python3 scripts/blender-mcp-health-check.py  # Sollte 6/6 zeigen
```

### Problem: "Export aus Blender schlägt fehl"
```bash
# WORKAROUND (bis automatischer Export funktioniert):
1. In Blender: Scripting Tab öffnen
2. Text → Open → BLENDER-EXPORT-MANUAL.py
3. Run Script (▶️)
# Dateien landen in assets/models/animals/dog/
```

### Problem: "Mehrere Blender-Instanzen offen"
```bash
# SOFORT FIXEN:
killall Blender  # Alle schließen
open -a Blender  # Eine neue öffnen
# NIE WIEDER: subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender"])
```

### Problem: "Port 8080 bereits belegt"
```bash
# Quick Fix:
kill $(lsof -t -i:8080)  # Port freimachen
python3 -m http.server 8080  # Server neu starten
# Alternative: Port 8081 nutzen
```

---

## ✅ GELÖSTE PROBLEME (Stand: 25.08.2025)

### 🎯 BLENDER MCP INTEGRATION - 90% ERFOLG

#### Was funktioniert:
| Feature | Status | Command/Method |
|---------|--------|----------------|
| MCP Connection | ✅ | Port 9876 WebSocket |
| Object Creation | ✅ | `bpy.ops.mesh.primitive_*` |
| Material Changes | ✅ | `bpy.data.materials.new()` |
| Transformations | ✅ | Position, Scale, Rotation |
| Python Execution | ✅ | `execute_blender_code()` |
| Scene Info | ✅ | `get_scene_info()` |

#### Einzige Limitation:
| Feature | Status | Workaround |
|---------|--------|------------|
| Auto-Export | ❌ | Manual Script: `BLENDER-EXPORT-MANUAL.py` |

---

## 🔴 KRITISCHE FEHLER - NIE WIEDER!

### 1️⃣ **Der 10-Stunden-Fehler: Falsche Config**

#### ❌ FALSCH (funktioniert NICHT):
```json
// In .cursor/settings.json
{
  "mcp.servers": {
    "blender-mcp": {
      "command": "npx",  // FALSCH! blender-mcp ist nicht auf npm!
      "args": ["blender-mcp"]
    }
  }
}
```

#### ✅ RICHTIG (funktioniert SOFORT):
```json
// In .cursor/mcp.json (ANDERE DATEI!)
{
  "mcpServers": {
    "blender-mcp": {
      "command": "uvx",  // RICHTIG! Python package manager
      "args": ["blender-mcp"]
    }
  }
}
```

### 2️⃣ **Der RAM-Killer: Mehrere Blender-Instanzen**

#### ❌ Was wir falsch gemacht haben:
```python
# Öffnet NEUE Blender-Instanz (2GB RAM!)
subprocess.run(["/Applications/Blender.app/Contents/MacOS/Blender", "--python", "script.py"])
# Resultat: 4 Instanzen = 8GB RAM verschwendet!
```

#### ✅ Richtige Vorgehensweise:
```python
# Nutze existierende Blender GUI via MCP
# Port 9876, keine neue Instanz!
```

### 3️⃣ **Package Manager Verwirrung**

| Package | ❌ Falsch | ✅ Richtig | Warum |
|---------|-----------|------------|-------|
| blender-mcp | npx | uvx | Python package, nicht npm! |
| @modelcontextprotocol/* | uvx | npx | npm package, nicht Python! |
| filesystem MCP | pip | npx | Official MCP, nur npm! |

---

## 📋 TÄGLICHE CHECKLISTE

### Morgen-Routine:
```bash
# 1. Blender Status prüfen
ps aux | grep Blender  # Sollte nur 1 Instanz zeigen

# 2. MCP Health Check
python3 scripts/blender-mcp-health-check.py
# Erwartung: 6/6 Tests bestanden

# 3. Port-Check
lsof -i:9876  # MCP Port
lsof -i:8080  # HTTP Server

# 4. Export-Watcher prüfen
ps aux | grep export-watcher
# Falls nicht läuft: python3 scripts/blender-export-watcher.py &
```

---

## 🛠️ OPTIMALER WORKFLOW

### Für 3D-Änderungen:
```python
# 1. Scene analysieren
python3 scripts/analyze_scene.py

# 2. Kreative Änderungen
python3 scripts/transform-dog-creative.py

# 3. Export (noch manuell)
# In Blender: Scripting → BLENDER-EXPORT-MANUAL.py → Run

# 4. Testen
open http://localhost:8080/vetscan-bello-3d-v7.html
```

---

## 📊 DEBUGGING TOOLS

### Health Check Script:
```bash
python3 scripts/blender-mcp-health-check.py
```
Prüft:
- ✅ Blender läuft (PID)
- ✅ uvx installiert
- ✅ .cursor/mcp.json korrekt
- ✅ Port 9876 offen
- ✅ blender-mcp Prozesse
- ✅ Test-Command funktioniert

### Quick Debug Commands:
```bash
# MCP Status
curl http://localhost:9876/status

# Blender Prozesse
ps aux | grep -E "(Blender|blender-mcp)"

# Ports
netstat -an | grep -E "(9876|8080)"

# Cursor Config prüfen
cat .cursor/mcp.json | jq .
```

---

## 💡 LESSONS LEARNED

### Was wir gelernt haben:
1. **Config-Datei ist KRITISCH**: `.cursor/mcp.json` nicht settings.json
2. **Package Manager MUSS stimmen**: uvx für Python, npx für npm
3. **Blender Instanzen**: Eine reicht, mehr ist RAM-Verschwendung
4. **MCP kann fast alles**: Nur Export muss (noch) manuell
5. **Tests müssen ECHT sein**: Nicht nur "connection success"

### Zeit-Investment:
- 15 Stunden Debugging
- 10+ Fehlversuche
- 1 Config-Zeile war die Lösung
- **Learning: Unbezahlbar**

---

## 🚀 NÄCHSTE SCHRITTE

### Priorität 1: Export Automation
- [ ] WebSocket File Transfer implementieren
- [ ] Blender Addon mit Auto-Export
- [ ] Alternative zu `bpy.ops.export_scene`

### Priorität 2: Skalierung
- [ ] 20 Tiere als 3D-Modelle
- [ ] Batch-Processing Pipeline
- [ ] Medical Layers für alle

### Priorität 3: Features
- [ ] Minispiele Integration
- [ ] Multiplayer Support
- [ ] Achievement System

---

## 📞 SUPPORT

### Bei Problemen:
1. Dieses Troubleshooting durchgehen
2. Health-Check Script ausführen
3. `BLENDER-MCP-FINAL-STATUS.md` lesen
4. GitHub Issue erstellen mit Health-Check Output

---

**Remember: Der Unterschied zwischen 10 Stunden Debugging und sofortigem Erfolg?**
**`.cursor/settings.json` vs `.cursor/mcp.json` 🎯**