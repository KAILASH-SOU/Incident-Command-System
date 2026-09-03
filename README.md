# SentinelCore

A production-grade, local-first Incident Command and Root Cause Analysis system.

SentinelCore is designed to ingest telemetry streams, parse historical post-mortem documents, and orchestrate autonomous AI agents to diagnose active incidents. By leveraging a hybrid retrieval-augmented generation (RAG) engine alongside dual-LLM support, it provides fast, reliable, and context-aware debugging for engineering teams.

## Project Architecture

The system is separated into a high-performance Python backend and a reactive single-page frontend application.

### Backend Overview
Built with **FastAPI** and Python, the backend is responsible for data ingestion, agent orchestration, and serving Server-Sent Events (SSE) to the frontend.

- **Agent Workflow Engine**: An orchestrator that manages specialized diagnostic agents. When an incident is triggered, agents investigate logs and metrics autonomously.
- **Hybrid RAG Engine**: Utilizes **ChromaDB** for vector storage and **BM25** for keyword search. It embeds historical post-mortems and incident logs using **Sentence-Transformers** to provide context to the LLMs.
- **Dual-LLM Support**: Configured to run entirely locally using **Ollama** (e.g., Llama 3) for privacy, with a seamless fallback or primary switch to the **OpenAI API** for cloud-based inference.
- **Telemetry Streaming**: Real-time event streaming via SSE to push logs and agent status updates directly to the client.

### Frontend Overview
A modern, responsive user interface built with **React** and **Vite**.

- **Styling**: Uses **Tailwind CSS v4** for utility-first styling and a clean, dark-mode native interface.
- **Visualization**: Integrates **Recharts** for real-time telemetry graphs and system health metrics.
- **Icons**: Uses **Lucide React** for consistent iconography.

## API Endpoints

The API is structured under the `/api/v1` prefix:

- `POST /api/v1/ingest/log`: Ingest new system logs or alerts.
- `GET /api/v1/stream/telemetry`: Connects a Server-Sent Events (SSE) stream for real-time frontend updates.
- `POST /api/v1/agents/trigger`: Triggers the autonomous incident diagnostic workflow based on a given incident description.

## Setup and Installation

### Prerequisites
- Docker and Docker Compose
- Node.js (v18+)
- Python 3.10+ (if running manually)
- Ollama (if running local LLMs)

### Quick Start with Docker
The easiest way to get the entire stack running is via Docker Compose. This will build both the frontend and backend containers and attach them to a shared network.

```bash
docker-compose up --build
```
- Frontend will be available at `http://localhost:5173`
- Backend API will be available at `http://localhost:8000`

### Manual Development Setup

If you prefer to run the services bare-metal for development:

**1. Start the Backend**
The backend requires a Python virtual environment and its dependencies. We provide a convenience script:
```bash
./run_backend.sh
```
Alternatively, navigate to `/backend`, run `pip install -r requirements.txt`, and start the server with `uvicorn app.main:app --reload`.

**2. Start the Frontend**
The frontend requires Node modules to be installed. We provide a convenience script:
```bash
./run_frontend.sh
```
Alternatively, navigate to `/frontend`, run `npm install`, and start the development server with `npm run dev`.

## Configuration

Environment variables can be configured to alter the behavior of the LLM provider and API endpoints.

- `OLLAMA_BASE_URL`: The URL pointing to your local Ollama instance (defaults to `http://localhost:11434` or `http://host.docker.internal:11434` in Docker).
- `OPENAI_API_KEY`: If provided, the system can utilize OpenAI models for inference instead of local models.
