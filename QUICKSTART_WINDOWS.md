# Windows Quickstart (PowerShell)

This guide shows the exact commands to run the RAG FastAPI app on Windows.

## 1) Open PowerShell in repo root

```powershell
cd C:\path\to\CRAG-Demo-workflow
```

## 2) Create and activate a virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## 3) Install dependencies

```powershell
.\scripts\setup.ps1
```

## 4) Set Dynaconf environment

```powershell
$env:ENV_FOR_DYNACONF = "development"
```

## 5) Run the API

```powershell
.\scripts\run.ps1
```

Now open:
- Swagger UI: http://localhost:8000/docs
- Health check: http://localhost:8000/health

## 6) Validate lint/tests

```powershell
.\scripts\validate.ps1
```

## 7) Use CLI

```powershell
python -m app.cli ingest doc1 README.md
python -m app.cli query "What is this project?"
```

## Optional: Run with Docker Desktop (Windows)

```powershell
docker build -t rag-fastapi-app .
docker run --rm -p 8000:8000 rag-fastapi-app
```

## Proxy troubleshooting

If your network requires a proxy:

```powershell
$env:HTTPS_PROXY = "http://user:pass@proxy:port"
$env:HTTP_PROXY = "http://user:pass@proxy:port"
.\scripts\setup.ps1
```
