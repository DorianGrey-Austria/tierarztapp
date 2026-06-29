// Playwright config for VetScan Pro standalone HTML smoke tests.
// Serves the repo root on :8080 and runs the smoke suite against it.
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: 0,
  reporter: [['list']],
  use: {
    baseURL: 'http://localhost:8080',
    trace: 'on-first-retry',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
  webServer: {
    command: 'python3 -m http.server 8080',
    url: 'http://localhost:8080/vetscan-version-selector.html',
    reuseExistingServer: !process.env.CI,
    timeout: 30000,
  },
});
