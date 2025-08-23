# 🚀 Claude Code Professional Workflow Tips

> **Disclaimer**: Dies sind **Empfehlungen und Tipps** aus der Community und von Anthropic Teams - keine fixen Regeln! Adaptiere sie an deinen persönlichen Workflow. Diese Sammlung basiert auf Best Practices von erfahrenen Claude Code Nutzern.

## 📌 Must-Know Basics

### Keyboard Shortcuts & Time-Savers
- **ESC 2x**: Editiere deine letzte Nachricht
- **ESC**: Stoppe Claude (nicht Ctrl+C - das beendet die Session!)
- **Shift+Tab**: Toggle zwischen Normal-Modus, Auto-Accept und Plan Mode
- **Cmd+Ctrl+Shift+4** (Mac): Screenshot direkt in Clipboard
- **Ctrl+V**: Paste Images (nicht Cmd+V auf Mac!)
- **/clear**: Neue Session starten (spart Tokens)

### Permission Management
```bash
# Skip Permissions für schnelleres Arbeiten (mit Vorsicht!)
claude --dangerously-skip-permissions

# Oder nutze Auto-Accept Mode mit Shift+Tab während der Session
```

### Session Management
```bash
# Letzte Conversation fortsetzen
claude --continue

# Spezifische Session wieder aufnehmen
claude --resume <session-id>
```

## 🎯 Core Workflow Patterns

### 1. The Planning Mode Approach
```bash
# Für komplexe Tasks - lass Claude erst denken!
claude "Plan the implementation of [feature]"
# Review den Plan
# Dann: "Now implement the plan"
```

### 2. Test-Driven Development (TDD)
```bash
# Claude LIEBT TDD - es reduziert Halluzinationen!
claude "Write failing tests for [feature]"
claude "Now implement to make tests pass"
claude "Verify all tests are green"
```

### 3. Visual Context Workflow
```bash
# Perfekt für UI-Arbeit
# 1. Screenshot machen (Cmd+Ctrl+Shift+4)
# 2. In Claude pasten (Ctrl+V)
claude "Match this design exactly"
```

### 4. One Task Per Session
```bash
# Vermeide Token-Verschwendung
claude "Implement feature A"
/clear  # Neue Session
claude "Implement feature B"
```

## 🧠 Advanced Thinking Techniques

### Ultrathink für Architektur-Entscheidungen
```bash
# Magische Wörter für mehr Denkzeit:
"think"        # ~4.000 Token
"think hard"   # ~10.000 Token  
"think harder" # ~31.999 Token
"ultrathink"   # 31.999 Token (Maximum)

# Beispiel:
claude "Ultrathink about the best architecture for our microservices"
```

## 🛠️ Professional Setup

### Custom Commands (.claude/commands/)
```bash
# Erstelle wiederverwendbare Templates
mkdir -p .claude/commands

# Beispiel: fix-github-issue.md
cat > .claude/commands/fix-github-issue.md << 'EOF'
Please fix GitHub issue: $ARGUMENTS
1. Use gh issue view for details
2. Search relevant files  
3. Implement fix with tests
4. Create PR
EOF

# Nutze mit: /fix-github-issue #42
```

### MCP (Model Context Protocol) Integration
```bash
# Essential MCPs für Profis:
# - Context7: Holt Dokumentation on-the-fly
# - Filesystem: Besserer File-Zugriff
# - GitHub: Direkte Repo-Integration

# Installation in Claude Desktop settings.json:
# Mac: ~/Library/Application Support/Claude/claude_desktop_config.json
# Add to mcpServers:
{
  "context7": {
    "command": "npx",
    "args": ["-y", "@context7/mcp-server"]
  }
}
```

### Git Worktrees für Parallel-Entwicklung
```bash
# Mehrere Claude Sessions parallel
git worktree add ../project-auth feature/auth
git worktree add ../project-ui feature/ui

# Separate Claude Instanzen
cd ../project-auth && claude "Implement auth"
cd ../project-ui && claude "Build UI components"
```

## 📊 Productivity Multipliers

### 1. GitHub Integration
```bash
# Einmalig installieren
/install-github-app

# Claude reviewed dann automatisch PRs!
# Customize in settings für fokussierte Reviews
```

### 2. Automated Testing mit Playwright
```bash
# Installation
npm install -D @playwright/test
npx playwright install

# Self-Testing Workflow
claude "Write Playwright tests, run them, analyze results, fix issues"
```

### 3. IDE Side-by-Side Setup
```
[ VS Code mit Code ] [ Claude Code Terminal ]
        50%                    50%
```

### 4. The @-Reference Power
```bash
# Schnelle File-Referenzen
claude "Update @src/components/Header.tsx to match @design.png"

# Directory-Referenzen  
claude "Refactor all files in @src/api/"
```

## 🎨 Specialized Workflows

### Codebase Onboarding (3 Wochen → 3 Tage)
```bash
claude "Analyze the architecture of this codebase"
claude "What are the main patterns and conventions?"
claude "Create a mental model diagram"
```

### Legacy Code Modernization
```bash
claude "Identify deprecated patterns in @src/"
claude "Create modernization plan with priorities"
claude "Refactor incrementally with tests"
```

### Bug Fixing Workflow
```bash
# Share Error + Context
claude "Error: [paste error]. Reproduction: [steps]. Fix this"

# Incremental Fixes
claude "Apply fix step by step with verification"
```

## 💰 Cost Optimization

### Token Management
- **Clear Sessions**: Nutze `/clear` zwischen unrelated Tasks
- **Specific Instructions**: Klare Anweisungen beim ersten Mal
- **Reuse Patterns**: Speichere wiederkehrende Prompts als Commands

### The $100/Month Max Plan
- Unlimited Tokens ohne Counting
- Kein Stoppen wegen Limits
- Fokus auf Produktivität statt Kosten

## 🚦 Pro Tips von Anthropic Teams

### 1. "Fast Intern" Mental Model
Behandle Claude wie einen schnellen Junior Developer:
- Gib klare, spezifische Anweisungen
- Review den Output
- Iteriere schnell

### 2. Subagents für Spezialisierung
```bash
# Claude kann automatisch Subagents spawnen
claude "Use specialized agents for: frontend, backend, testing"
```

### 3. Hooks für Automation
```bash
# In settings.json
{
  "hooks": {
    "preToolUse": {
      "command": "python3",
      "args": ["./hooks/pre_check.py"]
    }
  }
}
```

## 🎯 Workflow Beispiele

### Der Ultimate Feature Flow
```bash
# 1. Planning
claude "Ultrathink and plan feature X"

# 2. TDD
claude "Write comprehensive tests first"

# 3. Implementation  
# Shift+Tab für Auto-Accept
claude "Implement with best practices"

# 4. Visual Verification
claude "Screenshot and verify UI"

# 5. Performance
claude "Measure and optimize if needed"

# 6. Ship It
claude "commit, push, create PR with detailed message"
```

### Rapid Prototyping
```bash
# Mit Bildern arbeiten
# 1. Mockup screenshotten
# 2. Paste in Claude
claude "Build this as working prototype in 10 minutes"
```

## 🔧 Troubleshooting

### Session läuft aus dem Ruder?
```bash
/clear  # Neustart
claude --continue  # Oder vorherige Session fortsetzen
```

### Claude versteht den Context nicht?
```bash
# Nutze CLAUDE.md für Project Context
claude "Read CLAUDE.md first, then [task]"
```

### Performance Probleme?
```bash
# Nutze Git Worktrees statt Branch-Switching
# Parallel Sessions sind effizienter
```

## 📈 Messbare Erfolge

Nutzer berichten:
- **10-20% Produktivitätssteigerung** mit diesen Workflows
- **3 Wochen → 3 Tage** Onboarding Zeit
- **10+ parallele Agents** für große Projekte
- **60% weniger Bugs** mit TDD Approach

## 🎓 Weiterführende Ressourcen

- [Anthropic Claude Code Docs](https://docs.anthropic.com/en/docs/claude-code)
- [GitHub: awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Community Best Practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

**Remember**: Claude Code ist ein Tool, das deine Fähigkeiten erweitert - nicht ersetzt. Die besten Ergebnisse entstehen durch die Kombination von menschlicher Kreativität und AI-Unterstützung! 🚀

*Diese Tipps werden kontinuierlich von der Community erweitert und verbessert.*