# Deployment

Production: https://vibecoding.company (Hostinger shared hosting, `/public_html/`).

One workflow deploys on every push to `main`: `.github/workflows/deploy.yml`.
It builds a `deploy/` folder (standalone HTML + `js/` + `assets/` + PWA files) and
uploads it. `landing.html` is published; the curated `index.html` is the entry page.

## Deploy strategy (2026 best practice)

1. **SFTP (primary)** — encrypted, SSH-based, Hostinger port **65002**.
2. **FTPS (fallback)** — FTP over TLS, runs only if SFTP fails (`security: loose`
   is required for Hostinger's cert chain).

Plain unencrypted FTP is deliberately not used. The two previously racing
workflows (`deploy.yml` + `deploy-to-root.yml`) were consolidated into one.

## Required GitHub secrets

Settings -> Secrets and variables -> Actions.

### SFTP (primary) — provide the host/user plus EITHER key OR password

| Secret | Value |
|--------|-------|
| `SSH_HOST` | Server hostname (Hostinger hPanel -> SSH access) |
| `SSH_USERNAME` | SSH username (e.g. `u123456789`) |
| `SSH_PORT` | `65002` (optional; defaults to 65002) |
| `SSH_PRIVATE_KEY` | Private key contents (preferred) |
| `SSH_PASSWORD` | SSH password (used if no key) |

Generate a key pair and register the public key with Hostinger:

```bash
ssh-keygen -t ed25519 -C "github-actions-deploy" -f vetscan_deploy -N ""
# paste vetscan_deploy.pub in hPanel -> Advanced -> SSH Access -> Manage SSH Keys
# paste the private key (vetscan_deploy) into the SSH_PRIVATE_KEY secret
```

### FTPS (fallback)

| Secret | Value |
|--------|-------|
| `FTP_SERVER` | FTP hostname |
| `FTP_USERNAME` | FTP account username |
| `FTP_PASSWORD` | FTP account password |

## Known blocker (2026-07)

The previous FTP credentials were rejected with `530 Login incorrect` (failing
since June). Deploys will keep failing until the secrets above are set with valid
values in the Hostinger hPanel. This cannot be fixed from code.

## Manual trigger

Actions -> "Deploy to Hostinger - vibecoding.company" -> Run workflow (`main`).
