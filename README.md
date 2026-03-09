# RAG FastAPI Application

A complete, modular Retrieval-Augmented Generation (RAG) application built with FastAPI and Dynaconf.

## Features
- **Configuration & Environment**: Dynaconf + YAML settings with environment switching via `ENV_FOR_DYNACONF`.
- **Coding Standards**: PEP8-style Python layout and `pyproject.toml`-based project configuration.
- **Dependency Management**: All dependencies managed in `pyproject.toml`.
- **Build & Runtime**: Dockerized runtime + setup/run/validate scripts.
- **Logging**: Centralized YAML logging configuration writing to `logs/` and console.
- **Testing**: Unit/API tests with `pytest` and validation via `ruff`.
- **Documentation**: `README.md` + `AGENT_GUIDE.md`.
- **Version Control Hygiene**: `.gitignore` configured for Python/Dynaconf/log artifacts.
- **Extensibility**: Modular packages for API, agents, tools, domains, and RAG core.
- **API & CLI**: FastAPI endpoints and Typer-based CLI.

## Project Structure

```text
app/
  api/routes/rag.py
  agents/
  core/
  domains/
  models/
  rag/
  tools/
  cli.py
  main.py
configs/
  settings.yaml
  logging.yaml
scripts/
tests/
Dockerfile
pyproject.toml
```

## Quick Start

### 1) Install
```bash
./scripts/setup.sh
```

### 2) Configure env
```bash
export ENV_FOR_DYNACONF=development
```

### 3) Run API
```bash
./scripts/run.sh
```

### 4) Test
```bash
./scripts/validate.sh
```

## API
- `GET /health`
- `POST /rag/documents`
- `POST /rag/query`

### Example
```bash
curl -X POST http://localhost:8000/rag/documents \
  -H "Content-Type: application/json" \
  -d '{"document_id":"doc1","text":"FastAPI is for building APIs.","metadata":{}}'

curl -X POST http://localhost:8000/rag/query \
  -H "Content-Type: application/json" \
  -d '{"query":"What is FastAPI?","top_k":1}'
```

## CLI
```bash
rag-cli ingest doc1 README.md
rag-cli query "What is this project?"
```

## Docker
```bash
docker build -t rag-fastapi-app .
docker run --rm -p 8000:8000 rag-fastapi-app
```
