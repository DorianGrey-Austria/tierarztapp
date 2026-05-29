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

  // --- Init ---
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function() {
      VetScan.initTheme();
      injectNavigation();
    });
  } else {
    VetScan.initTheme();
    injectNavigation();
  }

})();
