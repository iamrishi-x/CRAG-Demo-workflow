# AGENT_GUIDE.md

## Overview
This repository contains a modular, config-driven Retrieval-Augmented Generation (RAG) system.

## Configuration
- Main config: `configs/settings.yaml`
- Environment selection: `ENV_FOR_DYNACONF` (`development`, `production`, `default`)
- Secrets template: `configs/.secrets.yaml.example`

## Architecture
- API: `app/main.py`, `app/api/routes/rag.py`
- Core: `app/core/*`
- RAG components: `app/rag/*`
- Agents (optional orchestration layer): `app/agents/*`
- Domain presets: `app/domains/*`
- Utilities/tools: `app/tools/*`

## Logging
- Logging config: `configs/logging.yaml`
- Output: `logs/app.log`

## Local commands
- Install: `./scripts/setup.sh`
- Run API: `./scripts/run.sh`
- Validate: `./scripts/validate.sh`
- CLI examples:
  - `rag-cli ingest my-doc ./README.md`
  - `rag-cli query "What does the app do?"`

## Extension points
1. Replace the in-memory store in `app/rag/store.py` with an external vector DB.
2. Replace `GenerationAgent` with an LLM client.
3. Add domain-specific prompts/config in `app/domains/` and `configs/settings.yaml`.


## Windows quick commands (PowerShell)
- Setup: `.\scripts\setup.ps1`
- Run API: `.\scripts\run.ps1`
- Validate: `.\scripts\validate.ps1`


## Multi backend/LLM config
- Vector backends are defined in `configs/settings.yaml` under `vector_backends` (supported types: `in_memory`, `sqlite`).
- LLM providers are defined under `llm.providers`; default is `llm.default_provider`.
- Runtime overrides are available via API payload (`backends`, `llm_provider`) and CLI options.
