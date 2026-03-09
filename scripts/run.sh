#!/usr/bin/env bash
set -euo pipefail
export ENV_FOR_DYNACONF=${ENV_FOR_DYNACONF:-development}
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
