# MCP Server für Claude Desktop: Komplettguide mit optimierter Konfiguration

Das Model Context Protocol (MCP) erweitert Claude Desktop um leistungsstarke Integrationen mit lokalen und externen Ressourcen. Dieser Guide präsentiert die wichtigsten MCP Server, Best Practices für Docker-basierte Deployments und eine produktionsreife Konfiguration, die sofort einsatzbereit ist.

## Die essentiellen MCP Server im Überblick

MCP Server ermöglichen Claude Desktop die kontrollierte Interaktion mit Datenbanken, APIs, Entwicklungstools und kreativen Anwendungen. Die wichtigsten Server lassen sich in sieben Kategorien unterteilen, wobei jede spezifische Workflows und Anwendungsfälle abdeckt.

### Kreative Tools revolutionieren den Workflow

**Blender MCP** transformiert 3D-Modellierung durch natürlichsprachliche Befehle. Der Server ermöglicht die Erstellung und Manipulation von 3D-Objekten, Material-Anpassungen und Scene-Analysen direkt aus Claude heraus. Mit Integration zu Poly Haven Assets und bidirektionaler Kommunikation versteht Claude Blender-Szenen und kann präzise Änderungen vornehmen. Die Installation erfolgt via `uvx blender-mcp` und erfordert ein separates Blender-Addon.

**Godot MCP** automatisiert Game-Development-Prozesse durch direkte Engine-Integration. Der Server kann Godot-Projekte starten, Debug-Output erfassen, Szenen und Nodes erstellen sowie GDScript-Code generieren. Die kommerzielle GDAI MCP-Version bietet erweiterte Features wie Screenshot-Capabilities. Beide Versionen basieren auf Node.js und setzen Godot 4.2+ voraus.

### Infrastructure MCPs als technisches Fundament

**Docker MCP** bildet das Herzstück containerisierter Deployments. Der in Docker Desktop integrierte MCP Toolkit ermöglicht Container-Lifecycle-Management, Docker Compose Stack-Deployments und sichere Ressourcen-Limitierung. Mit über 100 verifizierten Servern im Docker MCP Catalog bietet diese Lösung maximale Skalierbarkeit bei minimaler Komplexität.

**Filesystem MCP** gewährleistet sicheren Dateizugriff mit konfigurierbaren Zugriffskontrollen. Der Server unterstützt alle Standard-Dateioperationen, Content-Suche und Directory-Exploration mit permission-basiertem Sicherheitsmodell. Als offizieller Reference-Server definiert er den Standard für lokale Ressourcen-Integration.

### Development Tools für professionelle Workflows

**Git und GitHub MCPs** revolutionieren Version Control durch AI-gestützte Automatisierung. Der Git MCP analysiert Repository-Status, führt Commits aus und unterstützt bei Merge-Konflikten. GitHub MCP erweitert dies um Issue-Management, PR-Automation und CI/CD-Monitoring mit dynamischen Toolsets für fokussierte Operationen. **Beide erfordern Personal Access Tokens** für sichere API-Zugriffe.

**Context7 MCP** eliminiert veraltete Code-Generierung durch Echtzeit-Dokumentations-Injection. Der Server erkennt automatisch verwendete Frameworks und liefert versionsSpezifische, aktuelle Dokumentation ohne API-Key-Anforderung. Die Integration erfolgt simpel durch "use context7" in Prompts.

### Datenbank-Integration für komplexe Analysen

**SQLite MCP** eignet sich perfekt für lokale Datenanalysen und Prototyping. Mit Business Intelligence Capabilities und Datenexport-Funktionen bietet er professionelle Features für kleinere Projekte. Die Installation erfolgt via `npx @executeautomation/database-server`.

**PostgreSQL MCP** bringt Enterprise-Features wie Query-Optimierung, Index-Empfehlungen und Performance-Analysen. Crystal DBA's Postgres MCP Pro bietet erweiterte Health-Checks und Execution-Plan-Analysen. Die Docker-basierte Deployment-Option gewährleistet maximale Isolation und Sicherheit.

## Docker-basierte MCP Deployments: Best Practices

Docker-Container bieten entscheidende Vorteile für MCP-Server-Deployments: **Umgebungsisolation** eliminiert Dependency-Konflikte, **Sicherheits-Sandboxing** schützt vor unauthorisierten Zugriffen, und **vereinfachte Distribution** ermöglicht Cross-Platform-Kompatibilität.

### Performance-Optimierung durch Ressourcen-Management

Die Docker MCP Toolkit Standardlimits von 1 CPU-Core und 2GB RAM pro Container lassen sich granular anpassen. Multi-Stage Builds reduzieren Image-Größen, während Alpine-basierte Images minimalen Overhead garantieren. Container-Prewarming für häufig genutzte MCPs und Health-Checks sichern optimale Response-Zeiten.

```yaml
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 256M
    reservations:
      cpus: '0.25'
      memory: 128M
```

### Sicherheit durch Defense-in-Depth

Docker MCP Server laufen mit **restricted privileges** und **no-new-privileges** Security-Options. Network-Isolation verhindert unauthorisierte Kommunikation, während Read-Only Root-Filesystems und Capability-Dropping maximalen Schutz bieten. Secrets werden via Docker Secrets oder externe Manager wie Vault verwaltet - niemals hardcoded in Images.

Die Zero-Trust Networking-Architektur blockiert standardmäßig alle externen Netzwerkzugriffe. Nur explizit freigegebene Domains oder IPs erhalten Zugang. Interne Container-zu-Container-Kommunikation erfolgt über isolierte Bridge-Networks mit definierten Subnets.

### Multi-Container-Orchestrierung

Docker Compose ermöglicht elegante Multi-MCP-Stacks mit Service-Dependencies und automatischen Restarts. Die MCP-Compose Tool-Integration generiert Claude Desktop Konfigurationen automatisch aus YAML-Definitionen. Gateway-basierte Architekturen zentralisieren Authentication und Monitoring bei gleichzeitiger Service-Isolation.

## Konfiguration und Installation

Die claude_desktop_config.json liegt unter **macOS** in `~/Library/Application Support/Claude/` und unter **Windows** in `%APPDATA%\Claude\`. Die JSON-Struktur definiert Server mit Command, Arguments und optionalen Environment-Variablen.

### Platform-spezifische Besonderheiten

**Windows** erfordert doppelte Backslashes in Pfaden (`C:\\\\Users\\\\`) und profitiert von globalen npm-Installationen. Der `cmd /c` Prefix löst Execution-Probleme bei manchen Servern. Administrator-Rechte sind oft notwendig für Docker-Integration.

**macOS/Linux** nutzen Standard Unix-Pfade mit Forward-Slashes. Die Installation via npx funktioniert meist out-of-the-box. System Preferences Security-Einstellungen müssen gegebenenfalls angepasst werden.

### Troubleshooting häufiger Probleme

**Connection-Probleme** resultieren meist aus fehlenden Node.js-Installationen oder falschen Pfaden. Die Lösung: Absolute Pfade verwenden und Node/npm-Versionen verifizieren.

**Permission-Errors** erfordern Administrator-Rechte (Windows) oder Anpassungen in System-Security-Settings (macOS). Directory-Permissions müssen explizit gesetzt sein.

**Docker-Networking-Issues** lösen sich durch `host.docker.internal` für lokale Verbindungen und korrekte Port-Mappings. Firewall-Einstellungen blockieren oft Container-Kommunikation.

**JSON-Syntax-Fehler** entstehen durch trailing Commas oder falsche Escaping-Sequenzen. Online-Validatoren und sorgfältiges Bracket-Matching verhindern Parse-Errors.

## Die optimierte Komplett-Konfiguration

Diese produktionsreife Konfiguration kombiniert die wichtigsten MCP Server mit Best Practices für Sicherheit und Performance. Die Mischung aus Docker-basierten und direkt installierten Servern maximiert Stabilität bei minimaler Komplexität.

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/IHR_USERNAME/Desktop",
        "/Users/IHR_USERNAME/Documents",
        "/Users/IHR_USERNAME/Projects"
      ]
    },
    
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_IHR_GITHUB_TOKEN_HIER"
      }
    },
    
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    
    "docker-postgres": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--name", "mcp-postgres",
        "--memory", "512m",
        "--cpus", "0.5",
        "--security-opt", "no-new-privileges",
        "-e", "DATABASE_URL",
        "crystaldba/postgres-mcp:latest"
      ],
      "env": {
        "DATABASE_URL": "postgresql://user:password@localhost:5432/dbname"
      }
    },
    
    "docker-blender": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--name", "mcp-blender",
        "--mount", "type=bind,src=/Users/IHR_USERNAME/Blender,dst=/workspace",
        "--memory", "1g",
        "--cpus", "1.0",
        "ahujasid/blender-mcp:latest"
      ]
    },
    
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "IHR_BRAVE_API_KEY_HIER"
      }
    },
    
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    },
    
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@executeautomation/database-server",
        "--sqlite",
        "/Users/IHR_USERNAME/databases/local.db"
      ]
    },
    
    "docker-godot": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--name", "mcp-godot",
        "--mount", "type=bind,src=/Users/IHR_USERNAME/GodotProjects,dst=/projects",
        "--memory", "512m",
        "godot-mcp:latest"
      ]
    }
  }
}
```

### Windows-spezifische Anpassungen

Für Windows-Nutzer müssen Pfade angepasst werden:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "C:\\\\Users\\\\IHR_USERNAME\\\\Desktop",
        "C:\\\\Users\\\\IHR_USERNAME\\\\Documents",
        "C:\\\\Users\\\\IHR_USERNAME\\\\Projects"
      ]
    },
    
    "sqlite": {
      "command": "npx",
      "args": [
        "-y",
        "@executeautomation/database-server",
        "--sqlite",
        "C:\\\\Users\\\\IHR_USERNAME\\\\databases\\\\local.db"
      ]
    }
  }
}
```

### Setup-Anleitung

**1. Vorbereitung:**
- Node.js 18+ installieren
- Docker Desktop mit aktiviertem MCP Toolkit
- GitHub Personal Access Token generieren
- Brave Search API Key besorgen (optional)

**2. Konfiguration anpassen:**
- Alle `IHR_USERNAME` durch tatsächlichen Benutzernamen ersetzen
- API-Keys und Tokens einfügen
- Pfade an lokale Gegebenheiten anpassen
- Nicht benötigte Server entfernen

**3. Installation:**
- Konfiguration in claude_desktop_config.json speichern
- Claude Desktop komplett neu starten
- Hammer-Icon im Chat-Input verifiziert erfolgreiche Aktivierung

**4. Docker-Server vorbereiten:**
```bash
# Docker Images vorab pullen für schnelleren Start
docker pull crystaldba/postgres-mcp:latest
docker pull ahujasid/blender-mcp:latest

# Verzeichnisse für Volume-Mounts erstellen
mkdir -p ~/Blender ~/GodotProjects ~/databases
```

**5. Funktionstest:**
- "use context7" testet Documentation-Injection
- Filesystem-Operationen verifizieren Dateizugriff
- GitHub-Integration prüft API-Verbindung

## Performance-Empfehlungen

Die optimale Konfiguration balanciert Funktionalität mit Ressourcen-Effizienz. **Limitieren Sie Filesystem-Zugriffe** auf notwendige Verzeichnisse. **Docker-Container** sollten mit expliziten Memory- und CPU-Limits laufen. **Connection-Pooling** für Datenbank-MCPs reduziert Overhead. **Regelmäßige Updates** der MCP-Server garantieren Security-Patches und Performance-Verbesserungen.

Für High-Traffic-Szenarien empfiehlt sich der MCP Gateway-Modus mit zentralisiertem Request-Handling. Container-Prewarming eliminiert Cold-Start-Delays. Health-Checks mit automatischen Restarts sichern Verfügbarkeit. Log-Aggregation über Docker's JSON-File-Driver ermöglicht zentrales Monitoring.

Diese Konfiguration bietet maximale Flexibilität bei minimaler Komplexität. Die Kombination aus nativen und Docker-basierten Servern nutzt die Stärken beider Welten: schnelle lokale Execution für einfache Tools, sichere Isolation für komplexe Integrationen. Mit dieser Setup sind Sie optimal für AI-gestütztes Development, kreative Workflows und Datenanalysen gerüstet.

---

## 🎯 Projektspezifische MCP-Auswahl für VetScan Pro 3000

Basierend auf unserem **Tierarztspiel-Projekt** mit 3D-Visualisierung, WebGL, und Deployment auf vibecoding.company sind folgende MCPs besonders relevant:

### 🔥 Essenzielle MCPs für unser Projekt

#### 1. **Blender MCP** (KRITISCH für 3D-Workflow)
- **Warum**: Direkte Integration mit Blender für Bello 3D-Modell
- **Nutzen**: Automatisches Export von GLB-Files, Material-Anpassungen, Medical Shader Generation
- **Installation**: `uvx blender-mcp` oder Docker-Version

#### 2. **Filesystem MCP** (UNVERZICHTBAR)
- **Warum**: Zugriff auf Projektdateien, HTML-Versionen, Assets
- **Nutzen**: Direkte Dateimanipulation ohne manuelle Eingaben
- **Pfade**: `/Desktop/coding/tierarztspiel`, `/Desktop`, `/Documents`

#### 3. **Git MCP** (WICHTIG für Versionierung)
- **Warum**: Automatische Commits nach jeder Änderung (siehe CLAUDE.md Rules)
- **Nutzen**: Version Tracking, Deployment Trigger
- **Integration**: Arbeitet mit lokalem Git Repository

#### 4. **GitHub MCP** (DEPLOYMENT AUTOMATION)
- **Warum**: GitHub Actions triggern, Issues verwalten
- **Nutzen**: Automatisches Deployment zu vibecoding.company
- **Requirement**: GitHub Personal Access Token

#### 5. **Context7 MCP** (CODE QUALITY)
- **Warum**: Aktuelle Three.js, React, Vite Dokumentation
- **Nutzen**: Verhindert veraltete Code-Patterns
- **Vorteil**: Kein API-Key nötig

### 🎨 Nice-to-Have MCPs

#### 6. **Memory MCP** (PROJEKTKONTEXT)
- **Warum**: Speichert Kontext über Sessions hinweg
- **Nutzen**: Merkt sich Versionsnummern, TODOs, Probleme

#### 7. **Fetch MCP** (TESTING)
- **Warum**: Testen der Live-Version auf vibecoding.company
- **Nutzen**: Verifiziert Deployment-Status

#### 8. **SQLite MCP** (FUTURE FEATURE)
- **Warum**: Für geplante Highscore/Progress-Speicherung
- **Nutzen**: Lokale Datenbank für Spielstände

### 📝 Optimierte MCP-Konfiguration für unser Projekt

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/Users/doriangrey/Desktop/coding/tierarztspiel",
        "/Users/doriangrey/Desktop",
        "/Users/doriangrey/Documents"
      ]
    },
    
    "blender": {
      "command": "uvx",
      "args": ["blender-mcp"]
    },
    
    "git": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-git"]
    },
    
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_YOUR_TOKEN_HERE"
      }
    },
    
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"]
    },
    
    "fetch": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-fetch"]
    }
  }
}
```

### 🚀 Installation Steps für unser Projekt

1. **GitHub Token generieren**:
   - GitHub → Settings → Developer Settings → Personal Access Tokens
   - Scopes: repo, workflow, read:org

2. **Blender MCP Setup**:
   ```bash
   # Installation
   pip install --user blender-mcp
   
   # Oder via uvx (empfohlen)
   uvx blender-mcp
   ```

3. **Config File Location** (macOS):
   ```bash
   ~/Library/Application Support/Claude/claude_desktop_config.json
   ```

4. **Restart Claude Desktop** nach Config-Änderung

### ⚠️ Projektspezifische Hinweise

- **Blender MCP** ist KRITISCH für den 3D-Workflow mit Bello
- **Filesystem** muss Zugriff auf `/Desktop/coding/tierarztspiel` haben
- **Git/GitHub** MCPs automatisieren Deployment-Prozess
- **Context7** verhindert Three.js CDN-Fehler durch aktuelle Docs
- **Memory** speichert Versionsnummern (wichtig laut User-Feedback!)

### 🎯 Priorisierung

**MUST HAVE**:
1. Filesystem (bereits aktiv)
2. Git (für Auto-Commits)
3. Blender (für 3D-Pipeline)

**SHOULD HAVE**:
4. GitHub (für Deployment)
5. Context7 (für Code-Qualität)

**NICE TO HAVE**:
6. Memory (für Kontext)
7. Fetch (für Testing)

Diese Konfiguration ist optimal auf unser VetScan Pro Projekt zugeschnitten und vermeidet unnötigen Overhead durch nicht benötigte MCPs wie Postgres, Godot oder Brave Search.