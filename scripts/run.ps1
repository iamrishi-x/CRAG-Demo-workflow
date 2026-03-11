$ErrorActionPreference = 'Stop'
if (-not $env:ENV_FOR_DYNACONF) { $env:ENV_FOR_DYNACONF = 'development' }
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
