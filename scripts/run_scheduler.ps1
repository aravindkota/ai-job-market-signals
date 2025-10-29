$ErrorActionPreference = 'Stop'
python -u "$(Join-Path $PSScriptRoot dev.py)" scheduler

