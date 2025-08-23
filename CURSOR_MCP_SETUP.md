# 🎯 CURSOR MCP SETUP - Blender Integration für VetScan Pro

**WICHTIG: Kopiere den exakten JSON-Code unten in deine Cursor MCP-Einstellungen**

## 📋 **SETUP ANLEITUNG**

### **Step 1: Blender MCP installieren**
```bash
npm install -g blender-mcp
```

### **Step 2: Cursor MCP konfigurieren**
1. **Öffne Cursor Settings** (Cmd + ,)
2. **Klicke "MCP" in der linken Sidebar** 
3. **Klicke "+ MCP Server"**
4. **LÖSCHE den gesamten Inhalt und kopiere EXAKT diesen JSON-Code:**

---

## 📄 **KOPIERE DIESEN TEXT IN CURSOR:**

```json
{
  "mcpServers": {
    "godot-mcp": {
      "command": "node",
      "args": ["/Users/doriangrey/EndlessRunner/godot-mcp/build/index.js"],
      "env": {
        "GODOT_PATH": "/Applications/Godot.app/Contents/MacOS/Godot",
        "DEBUG": "true"
      },
      "autoApprove": [
        "launch_editor",
        "run_project",
        "get_debug_output",
        "stop_project",
        "get_godot_version",
        "list_projects",
        "get_project_info",
        "create_scene",
        "add_node",
        "load_sprite",
        "export_mesh_library",
        "save_scene",
        "get_uid",
        "update_project_uids"
      ]
    },
    "blender-mcp": {
      "command": "npx",
      "args": ["-y", "blender-mcp"],
      "env": {
        "BLENDER_PATH": "/Applications/Blender.app/Contents/MacOS/Blender",
        "PROJECT_ROOT": "/Users/doriangrey/Desktop/coding/tierarztspiel",
        "DEBUG": "true"
      },
      "autoApprove": [
        "execute_blender_code",
        "get_scene_info",
        "get_object_info",
        "get_viewport_screenshot",
        "export_gltf",
        "create_material",
        "set_texture",
        "generate_model",
        "download_polyhaven_asset",
        "generate_hyper3d_model_via_text"
      ]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/doriangrey/Desktop/coding/tierarztspiel"],
      "autoApprove": [
        "read_file",
        "write_file",
        "list_directory",
        "create_directory",
        "get_file_info",
        "move_file",
        "delete_file"
      ]
    }
  }
}
```

---

### **Step 3: Cursor komplett neustarten**
```bash
# Terminal Befehl:
killall Cursor && sleep 2 && open -a Cursor
```

### **Step 4: Verbindung testen**
```bash
# Im Cursor Terminal (in deinem VetScan Pro Projekt):
node scripts/test-mcp-connection.js
```

**Erwartetes Ergebnis:**
```
✅ Blender MCP: Connected (X objects in scene)
✅ Filesystem MCP: Project directory accessible
✅ Development Environment: tierarztspiel v3.1.0
✅ Local Server: Python available for HTTP server

🎯 Success Rate: 4/4 (100%)
🚀 All systems ready! VetScan Pro 3D pipeline is fully operational.
```

---

## 🎯 **CLAUDE CODE BEFEHLE NACH SETUP**

**Nach erfolgreichem Setup kann Claude Code direkt diese Befehle verwenden:**

```python
# Blender Scene Info
scene = get_scene_info()
print(f"Objects in Blender: {scene}")

# Bello Object Details  
bello = get_object_info("Bello")
print(f"Bello info: {bello}")

# Python Code in Blender ausführen
execute_blender_code(code="""
import bpy
print(f"Blender version: {bpy.app.version}")
for obj in bpy.data.objects:
    print(f"Object: {obj.name}")
""")

# Screenshot machen
screenshot = get_viewport_screenshot(max_size=1024)
print("Screenshot created")
```

---

## 🔧 **TROUBLESHOOTING**

### Problem: `get_scene_info is not defined`
**Lösung:**
1. Prüfe Blender Installation:
```bash
ls -la "/Applications/Blender.app/Contents/MacOS/Blender"
```

2. Prüfe MCP Installation:
```bash
npm list -g blender-mcp
```

3. Prüfe Cursor Config:
```bash
cat ~/.cursor/mcp.json
```

### Problem: Blender not found
**Lösung:** 
```bash
# Finde Blender Installation
find /Applications -name "*lender*" -type d
# Passe BLENDER_PATH in der Config an
```

### Problem: Permission denied
**Lösung:**
```bash
chmod +x "/Applications/Blender.app/Contents/MacOS/Blender"
```

---

## 📚 **NACH DEM SETUP**

**Claude Code kann dann automatisch:**
- ✅ Bello 3D-Modell aus Blender exportieren
- ✅ Multi-Quality GLB-Dateien erstellen  
- ✅ Medical Visualization Materials anwenden
- ✅ Screenshots für Validierung machen
- ✅ Live-Integration mit vibecoding.company

**Das komplette 3D-Pipeline-System wird aktiviert! 🚀🐕**