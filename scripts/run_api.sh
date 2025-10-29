#!/usr/bin/env bash
set -euo pipefail
# Forward any extra flags like --port 8000 --reload
python3 "$(dirname "$0")/dev.py" api "$@"

