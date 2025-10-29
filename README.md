# Upwork AI Job Intelligence Service

Automatically discover and monitor Upwork jobs in key AI domains (e.g., GenAI Agents, Traditional ML, Computer Vision) using the official Upwork GraphQL API. This repo ships a scaffolded FastAPI service with OAuth2 placeholders, pagination-ready client stubs, a simple domain classifier, persistence primitives, and optional alerting hooks.

Status: scaffolded. Several modules contain TODOs and `NotImplementedError` for you to complete.

---

## Features
- OAuth2 flow placeholders for Upwork's GraphQL API
- Domain targeting (search expressions/skills) and basic keyword classification
- Pagination-ready client design and dedupe/persistence primitives
- FastAPI app with `/health` endpoint and room for `/jobs`, `/stats`
- Optional alerts (Slack/webhooks) and a simple scheduler entrypoint

---

## Project Structure

```
.
├─ app/
│  ├─ api/               # FastAPI app (main.py)
│  ├─ alerts/            # Notification hooks (notifier.py)
│  ├─ auth/              # OAuth2 flow (oauth.py)
│  ├─ clients/           # Upwork GraphQL client (upwork_gql.py)
│  ├─ jobs/              # Fetcher + classifier
│  ├─ scheduler/         # Cron/scheduling entrypoint
│  ├─ storage/           # DB engine and models
│  ├─ utils/             # Logging helpers
│  ├─ config.py          # Settings via env/.env
│  └─ __init__.py
├─ scripts/
│  ├─ dev.py             # Developer CLI (setup, api, scheduler, test)
│  ├─ setup.ps1/.sh      # Setup helpers (PowerShell/Bash)
│  ├─ run_api.ps1/.sh    # Run API helpers
│  ├─ run_scheduler.ps1/.sh
│  ├─ run_tests.ps1/.sh
│  └─ scaffold.py        # (Re)generate scaffolded files
├─ tests/
│  ├─ __init__.py
│  └─ test_smoke.py
├─ .env.example
├─ requirements.txt
├─ Dockerfile
└─ .gitignore
```

---

## Requirements
- Python 3.11+
- PowerShell (Windows) or Bash (macOS/Linux)

---

## Quickstart

1) Setup environment and dependencies

- PowerShell (Windows):
```powershell
./scripts/setup.ps1
```

- Bash (macOS/Linux):
```bash
./scripts/setup.sh
```

This creates `.venv`, installs from `requirements.txt`, and copies `.env.example` to `.env` (edit it next).

2) Configure environment

Copy `.env.example` to `.env` (if not already created) and set values:

```
UPWORK_CLIENT_ID=
UPWORK_CLIENT_SECRET=
UPWORK_REDIRECT_URI=
UPWORK_TENANT_ID=
UPWORK_AUTH_CODE=
DATABASE_URL=sqlite:///./local.db
SLACK_WEBHOOK_URL=
```

3) Run the API

- PowerShell:
```powershell
./scripts/run_api.ps1 --reload --port 8000
```

- Bash:
```bash
./scripts/run_api.sh --reload --port 8000
```

Open http://127.0.0.1:8000/health to verify.

4) Run the scheduler (placeholder)

- PowerShell:
```powershell
./scripts/run_scheduler.ps1
```

- Bash:
```bash
./scripts/run_scheduler.sh
```

5) Run tests

- PowerShell:
```powershell
./scripts/run_tests.ps1
```

- Bash:
```bash
./scripts/run_tests.sh
```

---

## Developer CLI (alternative to scripts)
All wrappers call the same Python CLI. You can invoke it directly:

```bash
python scripts/dev.py setup
python scripts/dev.py api --host 127.0.0.1 --port 8000 --reload
python scripts/dev.py scheduler
python scripts/dev.py test
```

---

## Implementation Notes
- OAuth: implement authorization code exchange and refresh in `app/auth/oauth.py`.
- GraphQL client: add queries/pagination in `app/clients/upwork_gql.py`.
- Fetching: orchestrate domain searches + persistence in `app/jobs/fetcher.py`.
- Classification: extend keyword rules or move to ontology IDs in `app/jobs/classifier.py`.
- Storage: configure engine/session in `app/storage/db.py` and models in `app/storage/models.py`.
- Alerts: implement Slack/webhook integration in `app/alerts/notifier.py`.
- API: add routes like `/jobs`, `/stats` in `app/api/main.py`.
- Scheduler: wire periodic runs in `app/scheduler/cron.py`.

---

## Docker

Build and run locally:

```bash
docker build -t upwork-ai-job-intel:dev .
docker run --env-file .env -p 8000:8000 upwork-ai-job-intel:dev
```

---

## Troubleshooting
- PowerShell execution policy blocks scripts: start a new PowerShell and run
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
  ```
- Missing venv Python when running commands: run `python scripts/dev.py setup` first.
- Network/API calls are not implemented yet: several modules intentionally raise `NotImplementedError` until you complete them.

---

## Notes
- Use the official Upwork API; avoid scraping.
- Respect rate limits; add retry/backoff in the GraphQL client when implementing.

