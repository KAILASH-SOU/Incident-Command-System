from app.core.llm_provider import llm_provider
from app.services.ingestion_queue import ingestion_queue
from app.rag.engine import rag_engine
import json

class DiffContextAgent:
    def __init__(self):
        self.name = "DiffContextAgent"
        
    async def analyze(self, incident_description: str) -> dict:
        await ingestion_queue.push_agent_thought(self.name, "Searching historical post-mortems via Hybrid RAG...")
        
        rag_results = rag_engine.search(incident_description)
        rag_context = "\n".join([r["content"] for r in rag_results]) if rag_results else "No historical post-mortems found."
        
        await ingestion_queue.push_agent_thought(self.name, f"Found {len(rag_results)} relevant historical docs.")
        
        system_prompt = f"You are a Code Diff & Context Agent. Use this historical context:\n{rag_context}\n\nGiven the incident, identify potential recent commit regressions. Return a JSON object with 'suspect_commits' (list of strings) and 'historical_precedents' (list of strings)."
        
        response_str = await llm_provider.generate_response(system_prompt, incident_description, require_json=True)
        
        try:
            result = json.loads(response_str)
        except json.JSONDecodeError:
            result = {"suspect_commits": [], "historical_precedents": []}
            
        await ingestion_queue.push_agent_thought(self.name, "Contextual analysis complete.", result)
        return result

diff_context_agent = DiffContextAgent()
