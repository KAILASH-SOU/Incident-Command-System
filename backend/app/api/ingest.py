from fastapi import APIRouter, BackgroundTasks, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List
from app.services.ingestion_queue import ingestion_queue

router = APIRouter()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str
    trace_id: str = None
    stack_trace: str = None
    privacy_level: str = "normal"

class MetricEntry(BaseModel):
    timestamp: str
    service: str
    cpu_usage: float
    memory_usage: float
    latency_p99: float
    error_rate_5xx: float

@router.post("/logs")
async def ingest_logs(log: LogEntry, background_tasks: BackgroundTasks):
    await ingestion_queue.push_log(log.model_dump())
    return {"status": "ok"}

@router.post("/metrics")
async def ingest_metrics(metric: MetricEntry):
    await ingestion_queue.push_metric(metric.model_dump())
    return {"status": "ok"}

@router.post("/spans")
async def ingest_spans(span: Dict[str, Any]):
    await ingestion_queue.push_span(span)
    return {"status": "ok"}
