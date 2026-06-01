/**
 * VetScan Pro - Shared Module
 * Wird von allen Lernwerkzeugen eingebunden.
 * Bietet: Navigation, localStorage, Dark Mode, Print, Progress Tracking
 *
 * Einbindung: <script src="js/vetscan-shared.js"></script>
 * (vor </body>)
 */

(function() {
  'use strict';

  // --- Konfiguration ---
  const TOOLS = [
    { id: 'clinical-exam', name: 'Klinische Untersuchung', file: 'vetscan-clinical-exam.html', icon: '\u2695', category: 'Grundlagen' },
    { id: 'ddx-trainer', name: 'DDx-Trainer', file: 'vetscan-ddx-trainer.html', icon: '\u{1F9E9}', category: 'Diagnostik' },
    { id: 'lab-interpreter', name: 'Laborwerte', file: 'vetscan-lab-interpreter.html', icon: '\u{1F9EA}', category: 'Diagnostik' },
    { id: 'emergency-triage', name: 'Notfall-Triage', file: 'vetscan-emergency-triage.html', icon: '\u{1F6A8}', category: 'Notfall' },
    { id: 'pharma-calc', name: 'Pharmakologie', file: 'vetscan-pharma-calc.html', icon: '\u{1F48A}', category: 'Therapie' },
    { id: 'auscultation', name: 'Auskultation', file: 'vetscan-auscultation.html', icon: '\u{1FA7A}', category: 'Grundlagen' },
    { id: 'radiology', name: 'Radiologie', file: 'vetscan-radiology.html', icon: '\u2622', category: 'Diagnostik' },
    { id: 'surgical-approaches', name: 'Chirurgie', file: 'vetscan-surgical-approaches.html', icon: '\u2702', category: 'Chirurgie' },
    { id: 'pathology-cases', name: 'Pathologie-Faelle', file: 'vetscan-pathology-cases.html', icon: '\u{1F4CB}', category: 'Klinik' },
    { id: 'anatomy-layers', name: 'Anatomie-Atlas', file: 'vetscan-anatomy-layers.html', icon: '\u{1F9B4}', category: 'Grundlagen' },
    { id: 'quick-reference', name: 'Normalwerte', file: 'vetscan-quick-reference.html', icon: '\u{1F4CA}', category: 'Referenz' },
    { id: 'glossary', name: 'Glossar', file: 'vetscan-glossary.html', icon: '\u{1F4D6}', category: 'Referenz' },
    { id: '3d-viewer', name: '3D Anatomie-Viewer', file: 'vetscan-3d-viewer.html', icon: '\u{1F9B4}', category: '3D' },
    { id: 'dashboard', name: 'Dashboard', file: 'vetscan-dashboard.html', icon: '\u{1F3E0}', category: 'System' },
  ];

  const STORAGE_KEY = 'vetscan_progress';
  const THEME_KEY = 'vetscan_theme';

  // --- Hilfsfunktionen ---
  function getCurrentToolId() {
    const path = window.location.pathname.split('/').pop();
    const tool = TOOLS.find(t => t.file === path);
    return tool ? tool.id : null;
  }

  // --- Progress Tracking ---
  window.VetScan = window.VetScan || {};

  VetScan.getProgress = function() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
    } catch { return {}; }
  };

  VetScan.saveProgress = function(toolId, data) {
    const progress = VetScan.getProgress();
    progress[toolId] = {
      ...progress[toolId],
      ...data,
      lastAccess: new Date().toISOString()
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(progress));
    } catch(e) { /* localStorage voll */ }
  };

  VetScan.getToolProgress = function(toolId) {
    return VetScan.getProgress()[toolId] || {};
  };

  VetScan.saveScore = function(toolId, score, maxScore) {
    const prev = VetScan.getToolProgress(toolId);
    const bestScore = Math.max(prev.bestScore || 0, score);
    VetScan.saveProgress(toolId, {
      score: score,
      maxScore: maxScore,
      bestScore: bestScore,
      attempts: (prev.attempts || 0) + 1
    });
  };

  // --- Design Tokens (consistent across all tools) ---
  function injectDesignTokens() {
    var style = document.createElement('style');
    style.textContent = ':root {' +
      '--vs-primary: #818cf8;--vs-primary-hover: #6366f1;' +
      '--vs-success: #22c55e;--vs-warning: #f59e0b;--vs-danger: #ef4444;' +
      '--vs-bg-dark: #0f172a;--vs-bg-card: #1e293b;--vs-bg-input: #334155;' +
      '--vs-text: #f1f5f9;--vs-text-muted: #94a3b8;--vs-text-dim: #64748b;' +
      '--vs-border: rgba(255,255,255,0.1);--vs-radius: 12px;--vs-radius-sm: 8px;' +
      '}' +
      '.vetscan-light {' +
      '--vs-bg-dark: #f8fafc;--vs-bg-card: #ffffff;--vs-bg-input: #f1f5f9;' +
      '--vs-text: #0f172a;--vs-text-muted: #475569;--vs-text-dim: #94a3b8;' +
      '--vs-border: rgba(0,0,0,0.1);' +
      '}';
    document.head.insertBefore(style, document.head.firstChild);
  }

  // --- Dark/Light Mode ---
  VetScan.initTheme = function() {
    const saved = localStorage.getItem(THEME_KEY);
    if (saved === 'light') {
      document.documentElement.classList.add('vetscan-light');
    }
  };

  VetScan.toggleTheme = function() {
    const isLight = document.documentElement.classList.toggle('vetscan-light');
    localStorage.setItem(THEME_KEY, isLight ? 'light' : 'dark');
    const btn = document.getElementById('vetscan-theme-toggle');
    if (btn) btn.textContent = isLight ? '\u263E' : '\u2600';
  };

  // --- Navigation Header ---
  function injectNavigation() {
    const currentId = getCurrentToolId();

    // Styles
    const style = document.createElement('style');
    style.textContent = `
      .vetscan-nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 9999;
        background: rgba(15, 23, 42, 0.95); backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.1);
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 16px; height: 48px; font-family: system-ui, sans-serif;
      }
      .vetscan-light .vetscan-nav {
        background: rgba(255, 255, 255, 0.95);
        border-bottom-color: rgba(0,0,0,0.1);
      }
      .vetscan-nav-brand { color: #818cf8; font-weight: 700; font-size: 14px; text-decoration: none; white-space: nowrap; }
      .vetscan-light .vetscan-nav-brand { color: #4f46e5; }
      .vetscan-nav-tools { display: flex; gap: 2px; overflow-x: auto; scrollbar-width: none; -ms-overflow-style: none; flex: 1; margin: 0 12px; }
      .vetscan-nav-tools::-webkit-scrollbar { display: none; }
      .vetscan-nav-link {
        color: rgba(255,255,255,0.6); text-decoration: none; font-size: 11px;
        padding: 6px 8px; border-radius: 6px; white-space: nowrap;
        transition: all 0.2s; display: flex; align-items: center; gap: 4px;
        min-height: 32px;
      }
      .vetscan-light .vetscan-nav-link { color: rgba(0,0,0,0.5); }
      .vetscan-nav-link:hover { background: rgba(255,255,255,0.1); color: rgba(255,255,255,0.9); }
      .vetscan-light .vetscan-nav-link:hover { background: rgba(0,0,0,0.05); color: rgba(0,0,0,0.8); }
      .vetscan-nav-link.active { background: rgba(129,140,248,0.2); color: #818cf8; font-weight: 600; }
      .vetscan-light .vetscan-nav-link.active { background: rgba(79,70,229,0.1); color: #4f46e5; }
      .vetscan-nav-actions { display: flex; gap: 6px; align-items: center; }
      .vetscan-nav-btn {
        background: none; border: 1px solid rgba(255,255,255,0.15); color: rgba(255,255,255,0.7);
        width: 32px; height: 32px; border-radius: 6px; cursor: pointer;
        font-size: 16px; display: flex; align-items: center; justify-content: center;
        transition: all 0.2s;
      }
      .vetscan-light .vetscan-nav-btn { border-color: rgba(0,0,0,0.15); color: rgba(0,0,0,0.6); }
      .vetscan-nav-btn:hover { background: rgba(255,255,255,0.1); }
      .vetscan-light .vetscan-nav-btn:hover { background: rgba(0,0,0,0.05); }
      body { padding-top: 48px !important; }
      @media print { .vetscan-nav { display: none !important; } body { padding-top: 0 !important; } }
      @media (max-width: 768px) {
        .vetscan-nav-link span { display: none; }
        .vetscan-nav-link { font-size: 16px; padding: 6px; }
      }
      @media print {
        body * { color: #000 !important; background: #fff !important; }
        .vetscan-nav, .vetscan-nav * { display: none !important; }
      }
    `;
    document.head.appendChild(style);

    // Navigation HTML
    const nav = document.createElement('nav');
    nav.className = 'vetscan-nav';
    nav.setAttribute('role', 'navigation');
    nav.setAttribute('aria-label', 'VetScan Pro Werkzeugleiste');

    const mainTools = TOOLS.filter(t => t.category !== 'System');

    nav.innerHTML = `
      <a href="vetscan-version-selector.html" class="vetscan-nav-brand" aria-label="Zurueck zur Startseite">VetScan Pro</a>
      <div class="vetscan-nav-tools" role="menubar">
        ${mainTools.map(t => `
          <a href="${t.file}" class="vetscan-nav-link${t.id === currentId ? ' active' : ''}"
             role="menuitem" aria-current="${t.id === currentId ? 'page' : 'false'}"
             title="${t.name}">
            <span aria-hidden="true">${t.icon}</span>
            <span>${t.name}</span>
          </a>
        `).join('')}
      </div>
      <div class="vetscan-nav-actions">
        <button id="vetscan-theme-toggle" class="vetscan-nav-btn" onclick="VetScan.toggleTheme()"
                aria-label="Farbschema wechseln" title="Hell/Dunkel">\u2600</button>
        <button class="vetscan-nav-btn" onclick="window.print()"
                aria-label="Seite drucken" title="Drucken">\u{1F5A8}</button>
        <a href="vetscan-dashboard.html" class="vetscan-nav-btn" style="text-decoration:none"
           aria-label="Lernfortschritt" title="Dashboard">\u{1F3E0}</a>
      </div>
    `;

    document.body.prepend(nav);

    // Track page visit
    if (currentId) {
      const prev = VetScan.getToolProgress(currentId);
      VetScan.saveProgress(currentId, {
        visits: (prev.visits || 0) + 1
      });
    }
  }

  // --- Keyboard Shortcuts ---
  function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
      // Don't trigger in input fields
      if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA' || e.target.tagName === 'SELECT') return;

      // ? = show shortcuts help
      if (e.key === '?' && !e.ctrlKey && !e.metaKey) {
        e.preventDefault();
        VetScan.toggleShortcutsHelp();
      }
      // D = dashboard
      if (e.key === 'd' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        // Only if no modal/dialog is open
        if (!document.querySelector('.vetscan-shortcuts-overlay')) {
          window.location.href = 'vetscan-dashboard.html';
        }
      }
      // T = toggle theme
      if (e.key === 't' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        VetScan.toggleTheme();
      }
      // P = print
      if (e.key === 'p' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        window.print();
      }
      // Escape = close overlays
      if (e.key === 'Escape') {
        var overlay = document.querySelector('.vetscan-shortcuts-overlay');
        if (overlay) overlay.remove();
      }
    });
  }

  VetScan.toggleShortcutsHelp = function() {
    var existing = document.querySelector('.vetscan-shortcuts-overlay');
    if (existing) { existing.remove(); return; }

    var overlay = document.createElement('div');
    overlay.className = 'vetscan-shortcuts-overlay';
    overlay.style.cssText = 'position:fixed;inset:0;background:rgba(0,0,0,0.7);z-index:10001;display:flex;align-items:center;justify-content:center;backdrop-filter:blur(4px);';
    overlay.onclick = function(e) { if (e.target === overlay) overlay.remove(); };

    overlay.innerHTML = '<div style="background:#1e293b;border-radius:16px;padding:32px;max-width:400px;width:90%;color:#e2e8f0;box-shadow:0 25px 50px rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.1);">' +
      '<h3 style="margin:0 0 20px;font-size:18px;color:#818cf8;">Tastenkuerzel</h3>' +
      '<div style="display:grid;grid-template-columns:60px 1fr;gap:8px 16px;font-size:14px;">' +
      '<kbd style="background:#334155;padding:4px 8px;border-radius:4px;text-align:center;font-family:monospace;">?</kbd><span>Diese Hilfe</span>' +
      '<kbd style="background:#334155;padding:4px 8px;border-radius:4px;text-align:center;font-family:monospace;">D</kbd><span>Dashboard</span>' +
      '<kbd style="background:#334155;padding:4px 8px;border-radius:4px;text-align:center;font-family:monospace;">T</kbd><span>Hell/Dunkel umschalten</span>' +
      '<kbd style="background:#334155;padding:4px 8px;border-radius:4px;text-align:center;font-family:monospace;">P</kbd><span>Drucken</span>' +
      '<kbd style="background:#334155;padding:4px 8px;border-radius:4px;text-align:center;font-family:monospace;">Esc</kbd><span>Overlay schliessen</span>' +
      '</div>' +
      '<p style="margin:20px 0 0;font-size:12px;color:#64748b;">Druecke <kbd style="background:#334155;padding:2px 6px;border-radius:3px;font-family:monospace;">?</kbd> um diese Hilfe zu schliessen</p>' +
      '</div>';

    document.body.appendChild(overlay);
  };

  // --- Touch Target Enhancement ---
  function enhanceTouchTargets() {
    var style = document.createElement('style');
    style.textContent = 'button, a, input, select, [role="button"], [onclick] { min-height: 44px; min-width: 44px; }' +
      '@media (pointer: coarse) { button, a[href], [role="button"] { min-height: 48px; } }';
    document.head.appendChild(style);
  }

  // --- Meta Tags ---
  function ensureMetaTags() {
    if (!document.querySelector('meta[name="theme-color"]')) {
      var meta = document.createElement('meta');
      meta.name = 'theme-color';
      meta.content = '#0f172a';
      document.head.appendChild(meta);
    }
    if (!document.querySelector('meta[name="description"]')) {
      var meta = document.createElement('meta');
      meta.name = 'description';
      var currentId = getCurrentToolId();
      var tool = TOOLS.find(function(t) { return t.id === currentId; });
      meta.content = tool
        ? 'VetScan Pro: ' + tool.name + ' - Professionelles Lernwerkzeug fuer Veterinaermedizin-Studierende'
        : 'VetScan Pro - Professionelle Lernwerkzeuge fuer Veterinaermedizin-Studierende';
      document.head.appendChild(meta);
    }
  }

  // --- Onboarding Hint (first visit) ---
  function showOnboardingHint() {
    var currentId = getCurrentToolId();
    if (!currentId) return;
    var key = 'vetscan_onboarded_' + currentId;
    if (localStorage.getItem(key)) return;

    var hints = {
      'clinical-exam': 'Folge der Checkliste Schritt fuer Schritt. Markiere jeden Punkt als normal oder abweichend.',
      'ddx-trainer': 'Waehle die wahrscheinlichsten Diagnosen aus und bringe sie in die richtige Reihenfolge.',
      'lab-interpreter': 'Gib die Blutwerte deines Patienten ein. Das System erkennt automatisch klinische Muster.',
      'emergency-triage': 'Zeitdruck! Beurteile die Triage-Kategorie und fuehre das ABC-Schema durch.',
      'pharma-calc': 'Waehle Spezies und Gewicht, dann berechnet der Rechner die korrekte Dosierung.',
      'auscultation': 'Klicke auf die Auskultationspunkte am Tiermodell fuer Befunddetails.',
      'radiology': 'Befunde systematisch: Qualitaet, Thoraxwand, Pleura, Lunge, Mediastinum, Herz, Zwerchfell.',
      'surgical-approaches': 'Klicke auf einen Zugang und oeffne die Schichten nacheinander.',
      'pathology-cases': 'Arbeite jeden Fall schrittweise durch: Anamnese, Untersuchung, Diagnostik, Diagnose, Therapie.',
      'anatomy-layers': 'Nutze die Slider um einzelne Schichten ein- und auszublenden. Klicke Strukturen fuer Details.'
    };

    var hint = hints[currentId];
    if (!hint) return;

    var toast = document.createElement('div');
    toast.style.cssText = 'position:fixed;bottom:24px;left:50%;transform:translateX(-50%);max-width:500px;width:90%;background:#1e293b;color:#e2e8f0;padding:16px 20px;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.4);z-index:10000;display:flex;align-items:flex-start;gap:12px;border:1px solid rgba(129,140,248,0.2);font-size:14px;line-height:1.5;font-family:system-ui,sans-serif;animation:slideUp 0.3s ease;';
    toast.innerHTML = '<div style="flex-shrink:0;font-size:20px;">💡</div><div style="flex:1;"><strong style="color:#818cf8;">Tipp:</strong> ' + hint + '</div><button onclick="this.parentElement.remove();localStorage.setItem(\'' + key + '\',\'1\')" style="flex-shrink:0;background:none;border:none;color:#64748b;cursor:pointer;font-size:18px;padding:4px;" aria-label="Schliessen">&times;</button>';

    var styleEl = document.createElement('style');
    styleEl.textContent = '@keyframes slideUp{from{opacity:0;transform:translateX(-50%) translateY(20px)}to{opacity:1;transform:translateX(-50%) translateY(0)}}';
    document.head.appendChild(styleEl);

    document.body.appendChild(toast);
    localStorage.setItem(key, '1');

    // Auto-close after 8 seconds
    setTimeout(function() { if (toast.parentElement) toast.remove(); }, 8000);
  }

  // --- Init ---
  function init() {
    injectDesignTokens();
    VetScan.initTheme();
    injectNavigation();
    initKeyboardShortcuts();
    enhanceTouchTargets();
    ensureMetaTags();
    setTimeout(showOnboardingHint, 1000);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
