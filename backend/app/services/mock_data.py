import asyncio
from datetime import datetime
from app.services.ingestion_queue import ingestion_queue
import random

async def simulate_incident():
    # Simulate some logs
    levels = ["INFO", "WARN", "ERROR", "FATAL"]
    services = ["auth-service", "payment-gateway", "user-db", "frontend-proxy"]
    
    for _ in range(20):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": random.choice(levels),
            "service": random.choice(services),
            "message": "Simulated log message...",
            "trace_id": f"trace-{random.randint(1000, 9999)}",
            "privacy_level": "normal"
        }
        await ingestion_queue.push_log(log)
        await asyncio.sleep(0.5)
        
    for _ in range(5):
        metric = {
            "timestamp": datetime.utcnow().isoformat(),
            "service": "payment-gateway",
            "cpu_usage": random.uniform(80.0, 99.9),
            "memory_usage": random.uniform(70.0, 95.0),
            "latency_p99": random.uniform(1.0, 5.0),
            "error_rate_5xx": random.uniform(0.1, 0.5)
        }
        await ingestion_queue.push_metric(metric)
        await asyncio.sleep(1)
