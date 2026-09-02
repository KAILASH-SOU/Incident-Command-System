from app.core.llm_provider import llm_provider
from app.services.ingestion_queue import ingestion_queue
import json

class MetricsAgent:
    def __init__(self):
        self.name = "MetricsAgent"
        
    async def analyze(self, incident_description: str) -> dict:
        await ingestion_queue.push_agent_thought(self.name, "Evaluating infrastructure metrics.")
        
        system_prompt = "You are an Infrastructure Metrics Agent. Based on the incident, identify likely metric bottlenecks (CPU, Memory, Latency). Return a JSON object with 'bottlenecks' (list of strings) and 'severity' (high/medium/low)."
        
        response_str = await llm_provider.generate_response(system_prompt, incident_description, require_json=True)
        
        try:
            result = json.loads(response_str)
        except json.JSONDecodeError:
            result = {"bottlenecks": ["Unknown"], "severity": "medium"}
            
        await ingestion_queue.push_agent_thought(self.name, "Metrics evaluation complete.", result)
        return result

metrics_agent = MetricsAgent()
