# 🐕 Blender MCP Integration für VetScan Pro

## ✅ INTEGRATION ERFOLGREICH! (25.08.2025)
**DURCHBRUCH: Cursor IDE kann jetzt direkt mit Blender kommunizieren!**
Siehe `BLENDER-MCP-SUCCESS.md` für die funktionierende Konfiguration.

## 🔴 KRITISCHE KONFIGURATION FÜR CURSOR
**WICHTIG: Verwende `.cursor/mcp.json` mit `uvx` command (NICHT npx!)**

## 🚀 Quick Start - So exportierst du dein Modell:

### Methode 1: Direkter Export (Empfohlen)
1. **In Blender:**
   - Öffne Blender mit deinem Hundemodell
   - Wechsle zum "Scripting" Workspace (oben)
   - Klicke "New" im Text Editor
   - Öffne: `scripts/export-from-gui-blender.py`
   - Klicke "Run Script" ▶️
   - Die Modelle werden automatisch exportiert!

2. **Im Browser:**
   - Öffne: http://localhost:8082/vetscan-bello-3d-v7.html
   - Dein realistisches Modell wird geladen!

### Methode 2: MCP Live-Export (Fortgeschritten)
1. **MCP Addon in Blender aktivieren:**
   - Text Editor → Open → `scripts/blender_mcp_addon.py`
   - Run Script ▶️
   - Sidebar → VetScan Tab erscheint

2. **Live Export:**
   - Wähle dein Hundemodell
   - Klicke "Live Export to VetScan" im VetScan Panel
   - Browser aktualisiert sich automatisch!

3. **Oder via Python:**
   ```bash
   python3 scripts/connect-to-blender-mcp.py
   ```

## 📁 Exportierte Dateien:
```
assets/models/animals/bello/
├── bello_realistic_high.glb    # Hochqualität mit Draco
├── bello_realistic_medium.glb  # Mittlere Qualität
├── bello_realistic_low.glb     # Niedrige Qualität
├── bello_complete.glb          # Alle Teile zusammen
└── bello_live.glb              # Live-Export vom Addon
```

## 🔄 Live-Reload Workflow:
1. Modell in Blender bearbeiten
2. "Live Export" klicken
3. Browser lädt automatisch neu!
4. WebSocket-Verbindung zeigt Status

## 🎮 Medical Visualizations:
Die medizinischen Modi (X-Ray, Ultrasound, Thermal, MRI, CT) funktionieren jetzt mit deinem realistischen Modell!

## 🛠️ Troubleshooting:

### "Primitives Box-Model statt realistischer Hund"
→ Exportiere mit `export-from-gui-blender.py` statt Background-Script

### "Connection refused"
→ MCP Addon in Blender nicht gestartet - Run `blender_mcp_addon.py`

### "No suitable model found"
→ Wähle dein Hundemodell in Blender aus und run Script erneut

### "WebSocket not connected"
→ Normal - Live-Reload ist optional, Modell lädt trotzdem

## 🎯 Architektur:
```
Blender GUI (dein Modell)
    ↓ Export Script / MCP Addon
GLB Files (optimiert für Three.js)
    ↓ Progressive Loading
Browser (VetScan Pro v7.3.0)
    ↓ WebSocket Live-Reload
Automatische Updates!
```

## 📊 Verbesserungen gegenüber v7.1:
- ✅ Lädt ECHTES Modell aus Blender GUI (nicht procedural)
- ✅ Live-Reload via WebSocket
- ✅ MCP Addon für Blender Integration
- ✅ Progressive LOD Loading
- ✅ Medical Shaders funktionieren mit realistischem Modell

## 🔥 Pro-Tipps:
1. **Selektiere dein Modell** bevor du exportierst
2. **Nutze das VetScan Panel** in Blender für schnellen Export
3. **Browser Console** zeigt Debug-Infos (F12)
4. **Port 9876** für Blender MCP
5. **Port 8082** für lokalen HTTP Server

---
*Version 7.3.0 - Build 2025.08.24.003*
*Mit professioneller MCP-Blender Integration*