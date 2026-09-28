.PHONY: help dev build up down test lint clean

help:
	@echo "SentinelCore - Available commands:"
	@echo "  make dev      - Start development environment (backend + frontend)"
	@echo "  make build    - Build Docker images"
	@echo "  make up       - Start all services with Docker Compose"
	@echo "  make down     - Stop all services"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run linting"
	@echo "  make clean    - Clean build artifacts"

dev:
	docker-compose up --build

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

test:
	cd backend && python -m pytest tests/ -v

lint:
	cd backend && ruff check app/
	cd frontend && python -m py_compile app.py

clean:
	docker-compose down -v
	rm -rf backend/app/__pycache__ backend/app/*/__pycache__
	rm -rf frontend/__pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true