# RAG FastAPI Application

A **production-ready Retrieval-Augmented Generation (RAG) system** built with **FastAPI**, **Dynaconf**, and a modular Python architecture.

This project provides a scalable foundation for building **enterprise GenAI systems**, supporting document ingestion, embedding generation, semantic retrieval, and LLM-powered responses.

The system is designed for **high performance, modular extensibility, and production deployment**.

---

# System Overview

The application provides:

• FastAPI backend for serving RAG APIs  
• Modular architecture for agents, tools, and domains  
• Configurable environment management via Dynaconf  
• CLI utilities for ingestion and querying  
• Containerized deployment via Docker  

---

# Features

### Configuration Management
- Dynaconf + YAML configuration
- Environment switching using `ENV_FOR_DYNACONF`
- Centralized configuration in `configs/settings.yaml`

### Scalable Architecture
- Modular project structure
- Separation of concerns:
  - API Layer
  - Agents
  - RAG Pipeline
  - Domain Logic
  - Tools

### FastAPI Backend
- Async API endpoints
- Automatic OpenAPI documentation
- High performance request handling

### Logging
- Centralized YAML logging configuration
- Logs written to:
  - Console
  - `logs/` directory

### CLI Support
Typer CLI provides commands for:

- Document ingestion
- Querying RAG system

### Testing & Code Quality
- pytest for testing
- ruff for linting
- PEP8 compliant structure

### Containerization
- Dockerized runtime
- Easily deployable in cloud or Kubernetes

---

# Project Structure

```
rag-fastapi-app
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       └── rag.py
│   │
│   ├── agents/
│   │
│   ├── core/
│   │
│   ├── domains/
│   │
│   ├── models/
│   │
│   ├── rag/
│   │
│   ├── tools/
│   │
│   ├── cli.py
│   └── main.py
│
├── configs/
│   ├── settings.yaml
│   └── logging.yaml
│
├── scripts/
│
├── tests/
│
├── Dockerfile
├── pyproject.toml
└── README.md
```

---

# High Level Architecture

```
                 ┌──────────────────────┐
                 │      Client / UI     │
                 │  Web App / CLI / API │
                 └──────────┬───────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │    FastAPI API    │
                  │  (app/main.py)    │
                  └─────────┬─────────┘
                            │
                ┌───────────▼───────────┐
                │     RAG Service       │
                │ Retrieval + Generate  │
                └───────────┬───────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
  Vector Database      Embedding Model      LLM Model
   (FAISS/PGVector)      (OpenAI etc)       (GPT/Mistral)
```

---

# RAG Pipeline

The system follows a **standard RAG workflow**.

```
        Document
           │
           ▼
     Text Chunking
           │
           ▼
     Embedding Model
           │
           ▼
      Vector Store
   (FAISS / PGVector)
           │
           ▼
        User Query
           │
           ▼
     Query Embedding
           │
           ▼
   Similarity Retrieval
           │
           ▼
   Context Construction
           │
           ▼
          LLM
           │
           ▼
      Generated Answer
```

---

# Agent Workflow (Optional Extension)

If agents are enabled, the architecture becomes:

```
          User Query
              │
              ▼
        Query Router
              │
     ┌────────┼────────┐
     ▼        ▼        ▼
 SQL Agent  RAG Agent  Tool Agent
     │        │        │
     ▼        ▼        ▼
 Database   VectorDB   External API
     │        │        │
     └────────┴────────┘
              │
              ▼
          Response
```

---

# Deployment Architecture

```
              Internet
                  │
                  ▼
          ┌──────────────┐
          │   API Gateway │
          └──────┬───────┘
                 │
                 ▼
           FastAPI Service
                 │
     ┌───────────┼───────────┐
     ▼           ▼           ▼
 Vector DB     Redis       LLM API
 (PGVector)   Cache/Queue  (OpenAI)
```

---

# Installation

## Clone the repository

```
git clone https://github.com/your-repo/rag-fastapi-app.git
cd rag-fastapi-app
```

---

# Environment Configuration

### Linux / Mac

```
export ENV_FOR_DYNACONF=development
```

### Windows PowerShell

```
$env:ENV_FOR_DYNACONF="development"
```

### Windows CMD

```
set ENV_FOR_DYNACONF=development
```

---

# Setup

Create virtual environment

```
python -m venv .venv
```

Activate environment

Windows

```
.venv\Scripts\activate
```

Linux / Mac

```
source .venv/bin/activate
```

Install dependencies

```
pip install -e .
```

---

# Run the API

```
uvicorn app.main:app --reload --port 8000
```

Server

```
http://localhost:8000
```

---

# API Documentation

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# API Endpoints

### Health

```
GET /health
```

---

### Ingest Document

```
POST /rag/documents
```

Example

```
curl -X POST http://localhost:8000/rag/documents \
-H "Content-Type: application/json" \
-d '{
  "document_id": "doc1",
  "text": "FastAPI is a modern web framework for building APIs.",
  "metadata": {}
}'
```

---

### Query RAG

```
POST /rag/query
```

Example

```
curl -X POST http://localhost:8000/rag/query \
-H "Content-Type: application/json" \
-d '{
  "query": "What is FastAPI?",
  "top_k": 1
}'
```

---

# CLI Usage

Ingest document

```
rag-cli ingest doc1 README.md
```

Query

```
rag-cli query "What is this project?"
```

---

# Testing

Run tests

```
pytest
```

Linting

```
ruff check .
```

---

# Docker

Build image

```
docker build -t rag-fastapi-app .
```

Run container

```
docker run --rm -p 8000:8000 rag-fastapi-app
```

---

# Logging

Logging configuration

```
configs/logging.yaml
```

Logs

```
logs/
```

---

# Future Enhancements

Possible improvements:

- LangGraph agent workflows
- Streaming responses
- Observability (OpenTelemetry)
- Redis caching
- Background jobs with Celery
- Authentication & RBAC
- Kubernetes deployment

---

# License

MIT License
