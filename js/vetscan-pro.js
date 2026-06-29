/**
 * VetScan Pro - Professional Enhancement Module
 * Adds: Toast notifications, keyboard help, ARIA, OG tags,
 * service worker registration, micro-interactions, loading UX
 *
 * Einbindung: <script src="js/vetscan-pro.js"></script>
 * (nach vetscan-shared.js, vor </body>)
 */
(function() {
  'use strict';

  // === 1. INJECT PROFESSIONAL CSS ===
  const proCSS = document.createElement('style');
  proCSS.textContent = `
/* === WCAG Fixes === */
:root {
  --vp-muted: #94a3b8;       /* Adjusted for 4.5:1 on dark */
  --vp-muted-dark: #a1a1aa;  /* For dark backgrounds */
  --vp-focus: #3b82f6;
  --vp-success: #10b981;
  --vp-error: #f87171;
  --vp-warning: #fbbf24;
  --vp-info: #38bdf8;
}

/* Touch target minimum 48px */
button, a, [role="button"], input[type="checkbox"], input[type="radio"],
select, .scan-btn, .scan-type-btn, .ctrl-btn, .sp-btn, .organ-btn,
.species-btn, .view-mode-btn, .dx-option, .pt-btn {
  min-height: 44px;
  min-width: 44px;
}

/* Focus-visible for all interactive elements */
:focus-visible {
  outline: 2px solid var(--vp-focus) !important;
  outline-offset: 2px !important;
  border-radius: 4px;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* Skip to content link */
.vp-skip-link {
  position: fixed; top: -100px; left: 16px;
  padding: 12px 24px; background: var(--vp-focus); color: #fff;
  border-radius: 0 0 8px 8px; font-size: 14px; font-weight: 600;
  text-decoration: none; z-index: 10000;
  transition: top 0.2s;
}
.vp-skip-link:focus { top: 0; }

/* === Toast Notification System === */
.vp-toast-container {
  position: fixed; top: 16px; right: 16px;
  display: flex; flex-direction: column; gap: 8px;
  z-index: 9999; pointer-events: none;
  max-width: 400px;
}
.vp-toast {
  padding: 12px 16px; border-radius: 10px;
  background: rgba(30, 41, 59, 0.95); backdrop-filter: blur(12px);
  border: 1px solid rgba(100, 116, 139, 0.2);
  color: #e2e8f0; font-size: 13px; line-height: 1.4;
  pointer-events: auto; display: flex; align-items: flex-start; gap: 10px;
  animation: vp-toast-in 0.3s ease-out;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}
.vp-toast.vp-toast-out { animation: vp-toast-out 0.3s ease-in forwards; }
.vp-toast-icon { font-size: 18px; flex-shrink: 0; margin-top: 1px; }
.vp-toast-body { flex: 1; }
.vp-toast-title { font-weight: 600; margin-bottom: 2px; }
.vp-toast-msg { color: #94a3b8; font-size: 12px; }
.vp-toast-close {
  background: none; border: none; color: #64748b; cursor: pointer;
  font-size: 16px; padding: 0 2px; flex-shrink: 0;
}
.vp-toast-close:hover { color: #e2e8f0; }
.vp-toast.success { border-left: 3px solid var(--vp-success); }
.vp-toast.error { border-left: 3px solid var(--vp-error); }
.vp-toast.warning { border-left: 3px solid var(--vp-warning); }
.vp-toast.info { border-left: 3px solid var(--vp-info); }

@keyframes vp-toast-in {
  from { opacity: 0; transform: translateX(40px); }
  to { opacity: 1; transform: translateX(0); }
}
@keyframes vp-toast-out {
  from { opacity: 1; transform: translateX(0); }
  to { opacity: 0; transform: translateX(40px); }
}

/* === Keyboard Help Overlay === */
.vp-help-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px); z-index: 9998;
  display: none; align-items: center; justify-content: center;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
}
.vp-help-overlay.visible { display: flex; }
.vp-help-card {
  background: #1e293b; border-radius: 16px; padding: 28px 32px;
  max-width: 480px; width: 90%; max-height: 80vh; overflow-y: auto;
  border: 1px solid #334155; box-shadow: 0 20px 60px rgba(0,0,0,0.5);
}
.vp-help-card h2 {
  font-size: 18px; color: #f1f5f9; margin-bottom: 16px;
  display: flex; align-items: center; gap: 8px;
}
.vp-help-card h3 {
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.1em;
  color: #64748b; margin: 16px 0 8px;
}
.vp-help-row {
  display: flex; justify-content: space-between; align-items: center;
  padding: 6px 0; border-bottom: 1px solid #1a2436;
}
.vp-help-row:last-child { border-bottom: none; }
.vp-help-key {
  display: inline-block; padding: 3px 8px; background: #0f172a;
  border: 1px solid #334155; border-radius: 5px; font-family: monospace;
  font-size: 12px; color: #e2e8f0; min-width: 28px; text-align: center;
}
.vp-help-desc { font-size: 13px; color: #94a3b8; }
.vp-help-close {
  position: absolute; top: 16px; right: 20px;
  background: none; border: none; color: #64748b; font-size: 20px;
  cursor: pointer; padding: 4px;
}
.vp-help-footer {
  margin-top: 16px; padding-top: 12px; border-top: 1px solid #1a2436;
  font-size: 11px; color: #475569; text-align: center;
}

/* === Loading Progress Bar === */
.vp-progress-bar {
  position: fixed; top: 0; left: 0; right: 0; height: 3px;
  z-index: 9997; background: transparent;
}
.vp-progress-fill {
  height: 100%; background: linear-gradient(90deg, var(--vp-focus), var(--vp-success));
  width: 0%; transition: width 0.3s ease-out;
  box-shadow: 0 0 8px rgba(59, 130, 246, 0.5);
}

/* === Professional Badge === */
.vp-pro-badge {
  position: fixed; bottom: 12px; left: 12px;
  font-size: 10px; color: #475569; font-family: monospace;
  z-index: 100; opacity: 0.6;
}
.vp-pro-badge:hover { opacity: 1; }
`;
  document.head.appendChild(proCSS);

  // === 2. SKIP-TO-CONTENT LINK ===
  const mainEl = document.querySelector('main, [role="main"], .viewport, .scanner-area, #app');
  if (mainEl) {
    if (!mainEl.id) mainEl.id = 'main-content';
    if (!mainEl.getAttribute('role')) mainEl.setAttribute('role', 'main');
    const skipLink = document.createElement('a');
    skipLink.className = 'vp-skip-link';
    skipLink.href = '#' + mainEl.id;
    skipLink.textContent = 'Zum Inhalt springen';
    document.body.prepend(skipLink);
  }

  // === 3. ARIA LANDMARKS ===
  document.querySelectorAll('nav, .sidebar, .left-panel, [class*="sidebar"]').forEach(el => {
    if (!el.getAttribute('role')) el.setAttribute('role', 'navigation');
    if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', 'Navigation');
  });
  document.querySelectorAll('header, .header').forEach(el => {
    if (!el.getAttribute('role')) el.setAttribute('role', 'banner');
  });
  document.querySelectorAll('footer, .statusbar, .footer').forEach(el => {
    if (!el.getAttribute('role')) el.setAttribute('role', 'contentinfo');
  });
  document.querySelectorAll('aside, .right-panel, .case-panel, [class*="panel"]').forEach(el => {
    if (el.matches('aside') || el.classList.contains('right-panel') || el.classList.contains('case-panel')) {
      if (!el.getAttribute('role')) el.setAttribute('role', 'complementary');
    }
  });

  // === 4. TOAST NOTIFICATION SYSTEM ===
  const toastContainer = document.createElement('div');
  toastContainer.className = 'vp-toast-container';
  toastContainer.setAttribute('role', 'alert');
  toastContainer.setAttribute('aria-live', 'polite');
  document.body.appendChild(toastContainer);

  const TOAST_ICONS = {
    success: '\u2705', error: '\u274C', warning: '\u26A0\uFE0F', info: '\u2139\uFE0F'
  };

  window.VetScanPro = window.VetScanPro || {};

  VetScanPro.toast = function(type, title, message, duration) {
    duration = duration || 5000;
    const toast = document.createElement('div');
    toast.className = `vp-toast ${type}`;
    toast.innerHTML = `
      <span class="vp-toast-icon">${TOAST_ICONS[type] || ''}</span>
      <div class="vp-toast-body">
        <div class="vp-toast-title">${title}</div>
        ${message ? `<div class="vp-toast-msg">${message}</div>` : ''}
      </div>
      <button class="vp-toast-close" aria-label="Schliessen">&times;</button>
    `;
    toast.querySelector('.vp-toast-close').addEventListener('click', () => {
      toast.classList.add('vp-toast-out');
      setTimeout(() => toast.remove(), 300);
    });
    toastContainer.appendChild(toast);
    if (duration > 0) {
      setTimeout(() => {
        if (toast.parentNode) {
          toast.classList.add('vp-toast-out');
          setTimeout(() => toast.remove(), 300);
        }
      }, duration);
    }
    return toast;
  };

  // === 5. KEYBOARD HELP OVERLAY ===
  const defaultShortcuts = {
    'Navigation': [
      { key: '?', desc: 'Diese Hilfe anzeigen' },
      { key: 'Esc', desc: 'Overlay schliessen' },
    ],
    'Ansicht': [
      { key: '1', desc: 'Standard-Ansicht' },
      { key: '2', desc: 'Roentgen / Wireframe' },
      { key: '3', desc: 'Ultraschall / X-Ray' },
      { key: '4', desc: 'Waermebild / Thermal' },
      { key: 'R', desc: 'Auto-Rotation umschalten' },
    ],
    'Aktionen': [
      { key: 'G', desc: 'Gitter ein/aus' },
      { key: 'S', desc: 'Screenshot speichern' },
      { key: 'F', desc: 'Vollbild umschalten' },
      { key: 'D', desc: 'Dark Mode umschalten' },
    ]
  };

  const helpOverlay = document.createElement('div');
  helpOverlay.className = 'vp-help-overlay';
  helpOverlay.setAttribute('role', 'dialog');
  helpOverlay.setAttribute('aria-label', 'Tastaturkuerzel');

  function buildHelpHTML(shortcuts) {
    let html = '<div class="vp-help-card" style="position:relative">';
    html += '<button class="vp-help-close" aria-label="Schliessen">&times;</button>';
    html += '<h2>\u2328\uFE0F Tastaturkuerzel</h2>';
    for (const [section, keys] of Object.entries(shortcuts)) {
      html += `<h3>${section}</h3>`;
      keys.forEach(k => {
        html += `<div class="vp-help-row"><span class="vp-help-desc">${k.desc}</span><span class="vp-help-key">${k.key}</span></div>`;
      });
    }
    html += '<div class="vp-help-footer">Druecke <span class="vp-help-key">?</span> um diese Hilfe zu oeffnen</div>';
    html += '</div>';
    return html;
  }

  helpOverlay.innerHTML = buildHelpHTML(defaultShortcuts);
  document.body.appendChild(helpOverlay);

  // Focus management for the modal (WCAG 2.4.3 / 2.1.2: trap + restore focus).
  let lastFocused = null;
  function openHelp() {
    lastFocused = document.activeElement;
    helpOverlay.classList.add('visible');
    const closeBtn = helpOverlay.querySelector('.vp-help-close');
    if (closeBtn) closeBtn.focus();
  }
  function closeHelp() {
    helpOverlay.classList.remove('visible');
    if (lastFocused && typeof lastFocused.focus === 'function') lastFocused.focus();
  }
  VetScanPro.openHelp = openHelp;
  VetScanPro.closeHelp = closeHelp;

  helpOverlay.querySelector('.vp-help-close').addEventListener('click', closeHelp);
  helpOverlay.addEventListener('click', (e) => {
    if (e.target === helpOverlay) closeHelp();
  });
  // Trap Tab within the overlay while it is open.
  helpOverlay.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab' || !helpOverlay.classList.contains('visible')) return;
    const focusables = helpOverlay.querySelectorAll('button, [href], input, [tabindex]:not([tabindex="-1"])');
    if (!focusables.length) return;
    const first = focusables[0];
    const last = focusables[focusables.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });

  VetScanPro.setShortcuts = function(shortcuts) {
    helpOverlay.innerHTML = buildHelpHTML(shortcuts);
    helpOverlay.querySelector('.vp-help-close').addEventListener('click', () => {
      helpOverlay.classList.remove('visible');
    });
  };

  // Listen for ? key
  document.addEventListener('keydown', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') return;
    if (e.key === '?' || (e.key === '/' && e.shiftKey)) {
      e.preventDefault();
      if (helpOverlay.classList.contains('visible')) closeHelp(); else openHelp();
    }
    if (e.key === 'Escape' && helpOverlay.classList.contains('visible')) {
      closeHelp();
    }
  });

  // === 6. LOADING PROGRESS BAR ===
  const progressBar = document.createElement('div');
  progressBar.className = 'vp-progress-bar';
  progressBar.innerHTML = '<div class="vp-progress-fill" id="vpProgressFill"></div>';
  document.body.prepend(progressBar);

  VetScanPro.setProgress = function(pct) {
    const fill = document.getElementById('vpProgressFill');
    if (fill) {
      fill.style.width = Math.min(100, Math.max(0, pct)) + '%';
      if (pct >= 100) {
        setTimeout(() => { fill.style.opacity = '0'; }, 500);
        setTimeout(() => { fill.style.width = '0%'; fill.style.opacity = '1'; }, 800);
      }
    }
  };

  // === 7. OPEN GRAPH META TAGS ===
  function addMetaTag(property, content) {
    if (!document.querySelector(`meta[property="${property}"]`)) {
      const meta = document.createElement('meta');
      meta.setAttribute('property', property);
      meta.setAttribute('content', content);
      document.head.appendChild(meta);
    }
  }

  const pageTitle = document.title || 'VetScan Pro';
  const pageDesc = document.querySelector('meta[name="description"]')?.content
    || 'Interaktive veterinaermedizinische Lern-App mit 3D-Modellen, Fallstudien und Diagnostik-Tools.';

  addMetaTag('og:title', pageTitle);
  addMetaTag('og:description', pageDesc);
  addMetaTag('og:type', 'website');
  addMetaTag('og:image', 'https://vibecoding.company/assets/og-vetscan.svg');
  addMetaTag('og:site_name', 'VetScan Pro - Veterinaermedizin-Simulation');
  addMetaTag('og:locale', 'de_DE');

  // Twitter card
  if (!document.querySelector('meta[name="twitter:card"]')) {
    const tc = document.createElement('meta');
    tc.name = 'twitter:card';
    tc.content = 'summary_large_image';
    document.head.appendChild(tc);
  }

  // === 7b. PWA HEAD: FAVICON, ICONS, MANIFEST, THEME-COLOR ===
  // Injected centrally so all standalone HTML files become installable apps
  // with a consistent tab/home-screen icon (none ship it inline).
  function addLink(rel, href, attrs) {
    // De-dupe by rel+sizes so we never inject the same icon twice.
    const sel = 'link[rel="' + rel + '"]' + (attrs && attrs.sizes ? '[sizes="' + attrs.sizes + '"]' : '');
    if (document.querySelector(sel)) return;
    const link = document.createElement('link');
    link.rel = rel;
    link.href = href;
    if (attrs) Object.keys(attrs).forEach(k => link.setAttribute(k, attrs[k]));
    document.head.appendChild(link);
  }
  // Performance: preconnect to the Three.js CDN, but only on pages that use it.
  if (document.querySelector('script[src*="cdnjs.cloudflare.com"], script[src*="unpkg.com"]')) {
    if (!document.querySelector('link[rel="preconnect"][href*="cdnjs"]')) {
      const pc = document.createElement('link');
      pc.rel = 'preconnect';
      pc.href = 'https://cdnjs.cloudflare.com';
      pc.crossOrigin = 'anonymous';
      document.head.appendChild(pc);
    }
  }
  addLink('icon', 'assets/icons/favicon.svg', { type: 'image/svg+xml' });
  addLink('icon', 'assets/icons/favicon-32.png', { type: 'image/png', sizes: '32x32' });
  addLink('apple-touch-icon', 'assets/icons/apple-touch-icon.png', { sizes: '180x180' });
  addLink('manifest', 'manifest.json');

  // SEO: canonical URL (strip query/hash) if none present.
  if (!document.querySelector('link[rel="canonical"]')) {
    const canonical = document.createElement('link');
    canonical.rel = 'canonical';
    canonical.href = location.origin + location.pathname;
    document.head.appendChild(canonical);
  }

  // Adaptive theme-color (shared.js already sets a dark default; add a light one).
  if (!document.querySelector('meta[name="theme-color"][media]')) {
    const tcLight = document.createElement('meta');
    tcLight.name = 'theme-color';
    tcLight.media = '(prefers-color-scheme: light)';
    tcLight.content = '#f8fafc';
    document.head.appendChild(tcLight);
    const tcDark = document.createElement('meta');
    tcDark.name = 'theme-color';
    tcDark.media = '(prefers-color-scheme: dark)';
    tcDark.content = '#0f172a';
    document.head.appendChild(tcDark);
  }
  // iOS standalone support
  addMetaTag2('apple-mobile-web-app-capable', 'yes');
  addMetaTag2('apple-mobile-web-app-status-bar-style', 'black-translucent');
  addMetaTag2('apple-mobile-web-app-title', 'VetScan Pro');
  addMetaTag2('mobile-web-app-capable', 'yes');

  function addMetaTag2(name, content) {
    if (document.querySelector('meta[name="' + name + '"]')) return;
    const m = document.createElement('meta');
    m.name = name;
    m.content = content;
    document.head.appendChild(m);
  }

  // === 8. GLB LOAD ERROR INTERCEPTION ===
  // Monkey-patch console.error to catch GLB load failures
  const originalConsoleError = console.error;
  console.error = function(...args) {
    const msg = args.map(a => String(a)).join(' ');
    if (msg.includes('GLB') || msg.includes('glb') || msg.includes('GLTF') ||
        msg.includes('load error') || msg.includes('Load error') || msg.includes('404')) {
      VetScanPro.toast('warning', 'Modell konnte nicht geladen werden',
        'Ein 3D-Modell ist nicht verfuegbar. Es wird ein Platzhalter angezeigt.', 6000);
    }
    originalConsoleError.apply(console, args);
  };

  // === 9. SERVICE WORKER REGISTRATION ===
  // Secure contexts only: https in production, localhost during development.
  const isLocalhost = ['localhost', '127.0.0.1', '[::1]'].includes(location.hostname);
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || isLocalhost)) {
    navigator.serviceWorker.register('sw.js').catch(() => {
      // Silent fail - SW is optional
    });
  }

  // === 9b. INSTALL PROMPT (Add to Home Screen) ===
  // Captures the deferred beforeinstallprompt and offers a dismissable button.
  // No tracking, no auto-popups (DSGVO-friendly): user stays in control.
  let deferredPrompt = null;
  const INSTALL_DISMISSED_KEY = 'vetscan_install_dismissed';

  const installCSS = document.createElement('style');
  installCSS.textContent = `
.vp-install-btn {
  position: fixed; bottom: 16px; right: 16px; z-index: 9996;
  display: none; align-items: center; gap: 8px;
  padding: 10px 16px; min-height: 44px;
  background: linear-gradient(135deg, #6366f1, #818cf8); color: #fff;
  border: none; border-radius: 12px; cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
  font-size: 14px; font-weight: 600;
  box-shadow: 0 8px 24px rgba(99,102,241,0.4);
  animation: vp-install-in 0.3s ease-out;
}
.vp-install-btn.visible { display: flex; }
.vp-install-btn:hover { filter: brightness(1.08); }
.vp-install-btn .vp-install-x {
  margin-left: 4px; opacity: 0.7; font-size: 16px; line-height: 1;
}
@keyframes vp-install-in { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
@media (prefers-reduced-motion: reduce) { .vp-install-btn { animation: none; } }
@media print { .vp-install-btn { display: none !important; } }
`;
  document.head.appendChild(installCSS);

  const installBtn = document.createElement('button');
  installBtn.className = 'vp-install-btn';
  installBtn.setAttribute('aria-label', 'VetScan Pro als App installieren');
  installBtn.innerHTML = '<span aria-hidden="true">⬇️</span><span>App installieren</span><span class="vp-install-x" role="button" aria-label="Hinweis ausblenden" title="Ausblenden">×</span>';
  document.body.appendChild(installBtn);

  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (localStorage.getItem(INSTALL_DISMISSED_KEY) !== '1') {
      installBtn.classList.add('visible');
    }
  });

  installBtn.addEventListener('click', async (e) => {
    // Dismiss handle (the "x") hides without prompting.
    if (e.target.classList.contains('vp-install-x')) {
      e.stopPropagation();
      installBtn.classList.remove('visible');
      localStorage.setItem(INSTALL_DISMISSED_KEY, '1');
      return;
    }
    if (!deferredPrompt) return;
    deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === 'accepted') {
      VetScanPro.toast('success', 'Installation gestartet', 'VetScan Pro wird zu deinem Geraet hinzugefuegt.');
    }
    deferredPrompt = null;
    installBtn.classList.remove('visible');
  });

  window.addEventListener('appinstalled', () => {
    installBtn.classList.remove('visible');
    VetScanPro.toast('success', 'App installiert', 'VetScan Pro ist jetzt offline verfuegbar.');
  });

  // === 10. PROFESSIONAL BADGE ===
  const badge = document.createElement('div');
  badge.className = 'vp-pro-badge';
  badge.textContent = 'VetScan Pro | 97 3D-Modelle | Hyper3D Rodin';
  document.body.appendChild(badge);

  // === INIT COMPLETE ===
  VetScanPro.version = '1.0.0';
  VetScanPro.ready = true;

})();
