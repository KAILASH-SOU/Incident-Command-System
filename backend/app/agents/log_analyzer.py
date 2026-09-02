from app.core.llm_provider import llm_provider
from app.services.ingestion_queue import ingestion_queue
import json

class LogAnalyzerAgent:
    def __init__(self):
        self.name = "LogAnalyzer"
        
    async def analyze(self, incident_description: str) -> dict:
        await ingestion_queue.push_agent_thought(self.name, "Starting log analysis for incident.", {"incident": incident_description})
        
        system_prompt = "You are a Log Analyzer agent. Given the incident description, suggest what logs you would look for. Return a JSON object with 'anomalies_detected' (list of strings) and 'summary' (string)."
        
        await ingestion_queue.push_agent_thought(self.name, "Querying LLM for log patterns...")
        response_str = await llm_provider.generate_response(system_prompt, incident_description, require_json=True)
        
        try:
            result = json.loads(response_str)
        except json.JSONDecodeError:
            result = {"anomalies_detected": ["Failed to parse anomalies"], "summary": response_str}
            
        await ingestion_queue.push_agent_thought(self.name, "Completed log analysis.", result)
        return result

log_analyzer = LogAnalyzerAgent()
