import pytest
import asyncio
from app.services.ingestion_queue import IngestionQueue

@pytest.mark.asyncio
async def test_ingestion_queue_push_log():
    queue = IngestionQueue()
    log_data = {
        "timestamp": "2024-01-01T00:00:00",
        "level": "INFO",
        "service": "test-service",
        "message": "Test log"
    }
    await queue.push_log(log_data)
    assert not queue.logs_queue.empty()
    item = await queue.logs_queue.get()
    assert item == log_data

@pytest.mark.asyncio
async def test_ingestion_queue_push_metric():
    queue = IngestionQueue()
    metric_data = {
        "timestamp": "2024-01-01T00:00:00",
        "service": "test-service",
        "cpu_usage": 50.0,
        "memory_usage": 60.0,
        "latency_p99": 100.0,
        "error_rate_5xx": 0.01
    }
    await queue.push_metric(metric_data)
    assert not queue.metrics_queue.empty()
    item = await queue.metrics_queue.get()
    assert item == metric_data

@pytest.mark.asyncio
async def test_ingestion_queue_stream_queue():
    queue = IngestionQueue()
    log_data = {"timestamp": "2024-01-01T00:00:00", "level": "ERROR", "service": "test", "message": "err"}
    await queue.push_log(log_data)
    assert not queue.stream_queue.empty()
    item = await queue.stream_queue.get()
    assert item["type"] == "log"
    assert item["data"] == log_data