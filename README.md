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

For a full step-by-step guide, see `QUICKSTART_WINDOWS.md`.

## Running on Windows (PowerShell)

> Recommended: Python 3.11+ and a virtual environment.

```powershell
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install deps
.\scripts\setup.ps1

# Pick Dynaconf environment
$env:ENV_FOR_DYNACONF = "development"

# Run API
.\scripts\run.ps1
```

Open Swagger UI at: `http://localhost:8000/docs`

### Windows validation
```powershell
.\scripts\validate.ps1
```

### Windows CLI examples
```powershell
python -m app.cli ingest doc1 README.md
python -m app.cli query "What is this project?"
```

### Common Windows issues
- If script execution is blocked, run:
  `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
- If `pip install` fails behind a corporate proxy, set proxy env vars before install:
  - `$env:HTTPS_PROXY = "http://user:pass@proxy:port"`
  - `$env:HTTP_PROXY = "http://user:pass@proxy:port"`


## Multi-DB and Multi-LLM configuration

This project now supports **multiple vector DB inputs** and **multiple LLM providers**, configured in `configs/settings.yaml`.

### Vector backends
Configure one or more backends under `vector_backends`:

```yaml
vector_backends:
  - name: "memory"
    type: "in_memory"
    enabled: true
  - name: "sqlite_local"
    type: "sqlite"
    enabled: true
    path: "data/vector.db"
```

- `in_memory`: fast local runtime store.
- `sqlite`: local file-backed DB input.

You can target specific backends in API/CLI calls.

### LLM providers
Configure provider set under `llm.providers` and choose default via `llm.default_provider`:

```yaml
llm:
  default_provider: "echo"
  providers:
    echo: {}
    extractive: {}
    template:
      template: "Q: {query}\nRetrieved:\n{context}\nA: {answer_hint}"
```

Override provider per request using `llm_provider` in `/rag/query`.

### API payload examples
```json
{
  "document_id": "doc1",
  "text": "your content",
  "backends": ["memory", "sqlite_local"]
}
```

```json
{
  "query": "What is ...?",
  "top_k": 3,
  "backends": ["sqlite_local"],
  "llm_provider": "extractive"
}
```
