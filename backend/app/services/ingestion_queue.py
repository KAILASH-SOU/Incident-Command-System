import asyncio
from typing import Dict, Any

class IngestionQueue:
    def __init__(self):
        self.logs_queue = asyncio.Queue()
        self.metrics_queue = asyncio.Queue()
        self.spans_queue = asyncio.Queue()
        self.stream_queue = asyncio.Queue() # For SSE to frontend
        self.agent_queue = asyncio.Queue()  # For agent timeline SSE
        
    async def push_log(self, data: Dict[str, Any]):
        await self.logs_queue.put(data)
        await self.stream_queue.put({"type": "log", "data": data})
        
    async def push_metric(self, data: Dict[str, Any]):
        await self.metrics_queue.put(data)
        await self.stream_queue.put({"type": "metric", "data": data})
        
    async def push_span(self, data: Dict[str, Any]):
        await self.spans_queue.put(data)
        
    async def push_agent_thought(self, agent: str, message: str, data: Dict[str, Any] = None):
        payload = {"agent": agent, "message": message, "data": data or {}}
        await self.agent_queue.put(payload)

ingestion_queue = IngestionQueue()
