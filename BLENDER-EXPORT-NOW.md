# 🐕 **JETZT: Exportiere dein Blender-Modell!**

## ✅ **Option A: Automatischer Export (EMPFOHLEN)**

### In Blender:
1. **Öffne Scripting Tab** (oben in Blender)
2. **Text → New** (im Text Editor)
3. **Kopiere diesen Pfad:**
   ```
   /Users/doriangrey/Desktop/coding/tierarztspiel/scripts/blender_auto_export.py
   ```
4. **Text → Open** → Navigiere zu obigem Script
5. **Run Script** (Play-Button oder Alt+P)

**→ Modell wird automatisch exportiert!**

---

## ✅ **Option B: Manueller Export**

### In Blender:
1. **File → Export → glTF 2.0 (.glb/.gltf)**

2. **Export Settings:**
   ```
   Format: glTF Binary (.glb) ✓
   Include → Materials ✓
   Include → Textures ✓
   Transform → +Y Up ✓
   ```

3. **SPEICHERE IN:**
   ```
   /Users/doriangrey/Desktop/coding/tierarztspiel/watched_exports/
   ```
   
4. **Dateiname**: `bello_export.glb` (oder beliebig)

---

## 🚀 **Was dann passiert:**

1. **Export-Watcher erkennt neue Datei** (läuft im Hintergrund)
2. **Automatischer Import** nach `models/animals/dog/medium/`
3. **Browser-Test bereit** auf http://localhost:8081/vetscan-bello-3d-v7.html

---

## 📊 **Status Check:**

```bash
# Ist der lokale Server noch an?
curl -I http://localhost:8081/vetscan-bello-3d-v7.html

# Wo ist das Modell?
ls -la models/animals/dog/medium/
```

---

## 🎯 **Erwartetes Ergebnis:**

Nach Export solltest du sehen:
- ✅ Dein echter Bello im Browser (nicht der prozedurale)
- ✅ Medical Shaders funktionieren
- ✅ Interaktive Anatomie-Punkte

---

## 🆘 **Falls nichts passiert:**

1. **Check Export-Ordner:**
   ```bash
   ls -la watched_exports/
   ```

2. **Manuell kopieren:**
   ```bash
   cp watched_exports/*.glb models/animals/dog/medium/bello_claude_desktop.glb
   ```

3. **Browser Hard-Reload:**
   - Chrome: Cmd+Shift+R
   - Developer Console: F12

---

**🔴 WICHTIG: KEINE neuen Blender-Instanzen öffnen! Nutze deine existierende GUI!**