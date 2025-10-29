$ErrorActionPreference = 'Stop'
# Pass any additional args through, e.g. --port 8000 --reload
python -u "$(Join-Path $PSScriptRoot dev.py)" api @args

