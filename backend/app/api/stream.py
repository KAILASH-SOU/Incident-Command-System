from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
import asyncio
import json
from app.services.ingestion_queue import ingestion_queue

router = APIRouter()

@router.get("/telemetry")
async def stream_telemetry():
    async def event_generator():
        while True:
            item = await ingestion_queue.stream_queue.get()
            yield {"data": json.dumps(item)}
    return EventSourceResponse(event_generator())

@router.get("/agents")
async def stream_agents():
    async def event_generator():
        while True:
            item = await ingestion_queue.agent_queue.get()
            yield {"data": json.dumps(item)}
    return EventSourceResponse(event_generator())
