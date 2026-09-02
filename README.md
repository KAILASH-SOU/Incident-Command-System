# SentinelCore

A production-grade, local-first Incident Command & Root Cause Analysis system.

## Architecture

- **Backend:** FastAPI, Python, Uvicorn, ChromaDB, Sentence-Transformers, Dual-LLM support (OpenAI + Ollama).
- **Frontend:** React, Vite, Tailwind CSS v4, Recharts, Lucide Icons.

## Quick Start

### Docker Compose
```bash
docker-compose up --build
```

### Manual Run

**Backend:**
```bash
./run_backend.sh
```

**Frontend:**
```bash
./run_frontend.sh
```
