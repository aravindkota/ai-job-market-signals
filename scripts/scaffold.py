

#!/usr/bin/env python3
"""
scaffold.py
Creates the project structure for the Upwork AI Job Intelligence Service
and writes each file with a short "purpose" comment header.
"""

import os
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[1]

# ------------------------------
# File templates with top comments
# ------------------------------

PY_HEADER = '''"""\
PURPOSE: {purpose}
"""'''

DOCKERFILE = dedent("""\
# PURPOSE: Containerize the service for local/dev/prod environments.
# - Installs dependencies
# - Exposes FastAPI app on port 8000 (adjust as needed)

FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# For local dev you might use: uvicorn app.api.main:app --host 0.0.0.0 --port 8000
EXPOSE 8000

CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

GITIGNORE = dedent("""\
# PURPOSE: Ignore build, cache, and local env files.
__pycache__/
*.pyc
.venv/
.env
.env.*
dist/
build/
*.sqlite
*.db
.pytest_cache/
coverage/
.idea/
.vscode/
.mypy_cache/
""")

ENV_EXAMPLE = dedent("""\
# PURPOSE: Template for required configuration.
UPWORK_CLIENT_ID=
UPWORK_CLIENT_SECRET=
UPWORK_REDIRECT_URI=
UPWORK_TENANT_ID=
UPWORK_AUTH_CODE=
DATABASE_URL=sqlite:///./local.db
SLACK_WEBHOOK_URL=
""")

REQS = dedent("""\
# PURPOSE: Core Python dependencies for the service.
fastapi
uvicorn
httpx
requests
python-dotenv
pydantic
sqlalchemy
alembic
loguru
tenacity
pytest
""")

README_PLACEHOLDER = dedent("""\
# README
# The full README is provided in the ChatGPT response—copy it here or keep this placeholder.
""")

# Python modules to create with their purpose comment
PY_FILES = {
    "app/__init__.py": "Package marker for the application.",
    "app/config.py": "Centralized settings loading (dotenv/env vars), constants, and runtime config.",
    "app/utils/logging.py": "Structured logging setup and helpers.",
    "app/auth/oauth.py": "OAuth2 logic for Upwork (authorization code exchange, token refresh).",
    "app/clients/upwork_gql.py": "GraphQL client for Upwork API: queries, pagination, and response validation.",
    "app/jobs/fetcher.py": "Orchestrates domain-specific job fetching and deduplication.",
    "app/jobs/classifier.py": "Maps jobs to target domains (GenAI agents, Traditional ML, Computer Vision).",
    "app/storage/db.py": "Database engine/session initialization and migrations entrypoints.",
    "app/storage/models.py": "SQLAlchemy models (Job, Domain, FetchLog) and related schemas.",
    "app/alerts/notifier.py": "Slack/email/webhook notification helpers.",
    "app/api/main.py": "FastAPI app with routes for /health, /jobs, /stats.",
    "app/scheduler/cron.py": "Polling/scheduling entrypoint; triggers periodic fetch tasks.",
    "tests/__init__.py": "Test package marker.",
    "tests/test_smoke.py": "Basic smoke test to ensure imports and app bootstrapping.",
}

# Non-Python files
OTHER_FILES = {
    ".gitignore": GITIGNORE,
    ".env.example": ENV_EXAMPLE,
    "requirements.txt": REQS,
    "Dockerfile": DOCKERFILE,
    "README.md": README_PLACEHOLDER,
}

# Minimal content for certain Python files beyond the header
EXTRA_SNIPPETS = {
    "app/api/main.py": dedent("""
        from fastapi import FastAPI

        app = FastAPI(title="Upwork AI Job Intelligence Service")

        @app.get("/health")
        def health():
            return {"status": "ok"}
    """),
    "tests/test_smoke.py": dedent("""
        def test_smoke():
            # PURPOSE: Ensure the test rig is functional; expand later.
            assert True
    """),
    "app/utils/logging.py": dedent("""
        import logging

        # PURPOSE: Configure simple structured logging; replace with loguru or structlog if preferred.
        def get_logger(name: str = "app"):
            logger = logging.getLogger(name)
            if not logger.handlers:
                handler = logging.StreamHandler()
                fmt = logging.Formatter("[%(asctime)s] %(levelname)s %(name)s: %(message)s")
                handler.setFormatter(fmt)
                logger.addHandler(handler)
                logger.setLevel(logging.INFO)
            return logger
    """),
    "app/config.py": dedent("""
        from pydantic import BaseSettings

        # PURPOSE: Centralized settings from environment variables.
        class Settings(BaseSettings):
            upwork_client_id: str | None = None
            upwork_client_secret: str | None = None
            upwork_redirect_uri: str | None = None
            upwork_tenant_id: str | None = None
            upwork_auth_code: str | None = None
            database_url: str = "sqlite:///./local.db"
            slack_webhook_url: str | None = None

            class Config:
                env_file = ".env"

        settings = Settings()
    """),
    "app/storage/db.py": dedent("""
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        from app.config import settings

        # PURPOSE: Initialize database engine and session factory.
        engine = create_engine(settings.database_url, future=True)
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)
    """),
    "app/storage/models.py": dedent("""
        from sqlalchemy.orm import declarative_base, Mapped, mapped_column
        from sqlalchemy import String, Integer, DateTime, JSON, Boolean
        from datetime import datetime

        # PURPOSE: Define core ORM models for job data.
        Base = declarative_base()

        class Job(Base):
            __tablename__ = "jobs"
            id: Mapped[str] = mapped_column(String, primary_key=True)  # Upwork job ID
            title: Mapped[str | None] = mapped_column(String, nullable=True)
            domain: Mapped[str | None] = mapped_column(String, nullable=True)
            description: Mapped[str | None] = mapped_column(String, nullable=True)
            budget_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
            budget_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
            currency: Mapped[str | None] = mapped_column(String, nullable=True)
            verified_client: Mapped[bool] = mapped_column(Boolean, default=False)
            location: Mapped[str | None] = mapped_column(String, nullable=True)
            posted_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
            proposals: Mapped[int | None] = mapped_column(Integer, nullable=True)
            json_raw: Mapped[dict | None] = mapped_column(JSON, nullable=True)
            created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    """),
    "app/jobs/classifier.py": dedent("""
        # PURPOSE: Map free-text jobs to a domain using simple keyword rules (extend with ontology IDs later).

        DOMAIN_KEYWORDS = {
            "GenAI agents": ["genai agent", "agentic ai", "autonomous agent", "langchain", "autogen", "crewai", "rag"],
            "Traditional ML": ["machine learning", "scikit-learn", "xgboost", "catboost", "time series"],
            "Computer Vision": ["computer vision", "opencv", "yolo", "detectron2", "object detection", "ocr"],
        }

        def classify(text: str) -> str | None:
            t = (text or "").lower()
            for domain, words in DOMAIN_KEYWORDS.items():
                if any(w in t for w in words):
                    return domain
            return None
    """),
    "app/jobs/fetcher.py": dedent("""
        # PURPOSE: High-level orchestration to fetch jobs per domain and persist them.

        from app.jobs.classifier import classify
        # from app.clients.upwork_gql import search_jobs  # implement later
        # from app.storage.db import SessionLocal
        # from app.storage.models import Job

        def fetch_and_store():
            # 1) Call Upwork GraphQL client per domain (implement in clients/upwork_gql.py)
            # 2) Classify using classifier.classify()
            # 3) Upsert into DB
            pass
    """),
    "app/clients/upwork_gql.py": dedent("""
        # PURPOSE: Wrap the Upwork GraphQL API queries and pagination.
        # Implement OAuth token usage, headers, and queries here.

        import httpx

        API_URL = "https://api.upwork.com/graphql"

        async def search_jobs(token: str, search_expression: str, days_posted: int = 7, first: int = 25, after: str | None = None):
            # TODO: Implement actual GraphQL query call and return parsed results.
            # Suggested: use httpx.AsyncClient with Authorization: Bearer <token> + X-Upwork-API-TenantId
            raise NotImplementedError
    """),
    "app/auth/oauth.py": dedent("""
        # PURPOSE: OAuth2 authorization code exchange + token refresh for Upwork.
        # Implement the token exchange at:
        #   POST https://www.upwork.com/api/auth/v1/oauth2/token

        import httpx

        async def exchange_code_for_token(client_id: str, client_secret: str, redirect_uri: str, code: str) -> dict:
            # TODO: post to token endpoint and return token payload
            raise NotImplementedError
    """),
    "app/alerts/notifier.py": dedent("""
        # PURPOSE: Send notifications (Slack/email/webhooks) for new jobs or digests.

        def notify(message: str) -> None:
            # TODO: Implement Slack webhook or SMTP
            pass
    """),
    "app/scheduler/cron.py": dedent("""
        # PURPOSE: Entrypoint for scheduled fetches (e.g., every 15 minutes).
        # Wire up a real scheduler or call from external CRON/Cloud Scheduler.

        def run():
            # TODO: import and call fetch_and_store()
            print("Scheduler placeholder")

        if __name__ == "__main__":
            run()
    """),
}

def ensure_dirs():
    dirs = [
        ROOT / "app",
        ROOT / "app" / "utils",
        ROOT / "app" / "auth",
        ROOT / "app" / "clients",
        ROOT / "app" / "jobs",
        ROOT / "app" / "storage",
        ROOT / "app" / "alerts",
        ROOT / "app" / "api",
        ROOT / "app" / "scheduler",
        ROOT / "tests",
        ROOT / "scripts",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(content, encoding="utf-8")
        print(f"Created: {path.relative_to(ROOT)}")
    else:
        print(f"Exists:  {path.relative_to(ROOT)} (skipped)")

def main():
    ensure_dirs()

    # Write Python files with header comments
    for rel_path, purpose in PY_FILES.items():
        path = ROOT / rel_path
        header = PY_HEADER.format(purpose=purpose)
        body = EXTRA_SNIPPETS.get(rel_path, "")
        content = header + ("\n\n" + body if body.strip() else "\n")
        write_file(path, content)

    # Write non-Python files
    for rel_path, content in OTHER_FILES.items():
        path = ROOT / rel_path
        write_file(path, content)

    print("\nAll set! Edit the generated files to add real logic.\n")

if __name__ == "__main__":
    main()
