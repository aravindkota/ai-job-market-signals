#!/usr/bin/env python3
"""
Developer CLI for Upwork AI Job Intelligence Service.

Commands:
  - setup        Create venv, install deps, prepare .env
  - api          Run FastAPI app via uvicorn
  - scheduler    Run scheduler entrypoint
  - test         Run pytest

Usage examples:
  python scripts/dev.py setup
  python scripts/dev.py api --port 8000 --reload
  python scripts/dev.py scheduler
  python scripts/dev.py test
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VENV_DIR = ROOT / ".venv"
REQS_FILE = ROOT / "requirements.txt"
ENV_EXAMPLE = ROOT / ".env.example"
ENV_FILE = ROOT / ".env"


def is_windows() -> bool:
    return os.name == "nt"


def venv_python() -> Path:
    if is_windows():
        return VENV_DIR / "Scripts" / "python.exe"
    return VENV_DIR / "bin" / "python"


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> None:
    print(f"$ {' '.join(cmd)}")
    subprocess.run(cmd, cwd=str(cwd or ROOT), env=env or os.environ, check=True)


def ensure_python() -> None:
    try:
        subprocess.run([sys.executable, "--version"], check=True, stdout=subprocess.DEVNULL)
    except Exception as e:
        raise SystemExit(f"Python is required but not found: {e}")


def ensure_venv() -> None:
    if not VENV_DIR.exists():
        print(f"Creating venv at {VENV_DIR} ...")
        run([sys.executable, "-m", "venv", str(VENV_DIR)])
    else:
        print("Virtual environment already exists. Skipping creation.")


def install_requirements() -> None:
    if not REQS_FILE.exists():
        raise SystemExit(f"Missing requirements file: {REQS_FILE}")
    py = venv_python()
    if not py.exists():
        raise SystemExit("Venv Python not found; run 'setup' first.")
    run([str(py), "-m", "pip", "install", "--upgrade", "pip"])  # keep pip recent
    run([str(py), "-m", "pip", "install", "-r", str(REQS_FILE)])


def ensure_env_file() -> None:
    if ENV_FILE.exists():
        print(f"Found {ENV_FILE.name}.")
        return
    if ENV_EXAMPLE.exists():
        print(f"Creating {ENV_FILE.name} from template.")
        shutil.copyfile(ENV_EXAMPLE, ENV_FILE)
    else:
        print("No .env.example found; creating empty .env.")
        ENV_FILE.write_text("", encoding="utf-8")


def cmd_setup(_args: argparse.Namespace) -> None:
    ensure_python()
    ensure_venv()
    install_requirements()
    ensure_env_file()
    print("\nSetup complete. Edit .env before running the app.")


def cmd_api(args: argparse.Namespace) -> None:
    py = venv_python()
    if not py.exists():
        raise SystemExit("Venv not found. Run 'python scripts/dev.py setup' first.")
    uvicorn_args = [
        str(py),
        "-m",
        "uvicorn",
        "app.api.main:app",
        "--host",
        args.host,
        "--port",
        str(args.port),
    ]
    if args.reload:
        uvicorn_args.append("--reload")
    run(uvicorn_args)


def cmd_scheduler(_args: argparse.Namespace) -> None:
    py = venv_python()
    if not py.exists():
        raise SystemExit("Venv not found. Run 'python scripts/dev.py setup' first.")
    run([str(py), "-m", "app.scheduler.cron"])


def cmd_test(_args: argparse.Namespace) -> None:
    py = venv_python()
    if not py.exists():
        raise SystemExit("Venv not found. Run 'python scripts/dev.py setup' first.")
    run([str(py), "-m", "pytest", "-q"])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Dev utility for running the service")
    sub = p.add_subparsers(dest="command", required=True)

    s_setup = sub.add_parser("setup", help="Create venv, install deps, create .env")
    s_setup.set_defaults(func=cmd_setup)

    s_api = sub.add_parser("api", help="Run FastAPI app via uvicorn")
    s_api.add_argument("--host", default="127.0.0.1", help="Bind host (default: 127.0.0.1)")
    s_api.add_argument("--port", type=int, default=8000, help="Port (default: 8000)")
    s_api.add_argument("--reload", action="store_true", help="Auto-reload on code changes")
    s_api.set_defaults(func=cmd_api)

    s_sched = sub.add_parser("scheduler", help="Run scheduler entrypoint")
    s_sched.set_defaults(func=cmd_scheduler)

    s_test = sub.add_parser("test", help="Run pytest")
    s_test.set_defaults(func=cmd_test)

    return p


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

