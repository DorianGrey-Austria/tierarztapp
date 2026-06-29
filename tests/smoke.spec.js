// VetScan Pro - Smoke Test
// Loads every registered professional learning tool and asserts the page boots
// cleanly: no uncaught exceptions, the shared nav is present, and the modern-app
// head (favicon + manifest + theme-color) is injected.
//
// Run: npm run test:smoke
import { test, expect } from '@playwright/test';

// The 19 tools registered in js/vetscan-shared.js (source of truth).
const TOOLS = [
  'vetscan-clinical-exam.html',
  'vetscan-ddx-trainer.html',
  'vetscan-lab-interpreter.html',
  'vetscan-emergency-triage.html',
  'vetscan-pharma-calc.html',
  'vetscan-auscultation.html',
  'vetscan-radiology.html',
  'vetscan-surgical-approaches.html',
  'vetscan-pathology-cases.html',
  'vetscan-anatomy-layers.html',
  'vetscan-quick-reference.html',
  'vetscan-glossary.html',
  'vetscan-3d-viewer.html',
  'vetscan-organ-explorer.html',
  'vetscan-animated-showcase.html',
  'vetscan-pathology-scanner.html',
  'vetscan-parasite-atlas.html',
  'vetscan-bone-atlas.html',
  'vetscan-dashboard.html',
];

// Network/resource failures we tolerate (3D assets, CDN, optional SW) — these are
// non-blocking by design (loader falls back to procedural geometry, U4).
const SOFT = /\.glb|\.hdr|\.draco|three|cdn|favicon|sw\.js|manifest|404|Failed to load resource|net::ERR/i;

for (const file of TOOLS) {
  test(`boots cleanly: ${file}`, async ({ page }) => {
    const fatal = [];
    page.on('pageerror', (err) => fatal.push(`pageerror: ${err.message}`));
    page.on('console', (msg) => {
      if (msg.type() === 'error' && !SOFT.test(msg.text())) {
        fatal.push(`console.error: ${msg.text()}`);
      }
    });

    await page.goto('/' + file, { waitUntil: 'domcontentloaded' });
    // Give the shared/pro modules a tick to inject nav + head.
    await page.waitForTimeout(400);

    // Shared navigation bar injected by vetscan-shared.js
    await expect(page.locator('nav.vetscan-nav')).toHaveCount(1);

    // Modern-app head: favicon + manifest + theme-color
    await expect(page.locator('link[rel~="icon"]').first()).toHaveCount(1);
    await expect(page.locator('link[rel="manifest"]')).toHaveCount(1);
    await expect(page.locator('meta[name="theme-color"]').first()).toHaveCount(1);

    expect(fatal, `Fatal errors on ${file}:\n${fatal.join('\n')}`).toEqual([]);
  });
}

test('landing hub boots cleanly', async ({ page }) => {
  const fatal = [];
  page.on('pageerror', (err) => fatal.push(`pageerror: ${err.message}`));
  await page.goto('/vetscan-version-selector.html', { waitUntil: 'domcontentloaded' });
  await expect(page.locator('link[rel="manifest"]')).toHaveCount(1);
  await expect(page.locator('link[rel~="icon"]').first()).toHaveCount(1);
  expect(fatal, `Fatal errors on landing hub:\n${fatal.join('\n')}`).toEqual([]);
});
