from app.core.llm_provider import llm_provider
from app.services.ingestion_queue import ingestion_queue
from app.agents.log_analyzer import log_analyzer
from app.agents.metrics_agent import metrics_agent
from app.agents.diff_context_agent import diff_context_agent
import asyncio
import json

class OrchestratorAgent:
    def __init__(self):
        self.name = "LeadOrchestrator"
        
    async def run_incident_workflow(self, incident_description: str):
        await ingestion_queue.push_agent_thought(self.name, f"Initializing RCA workflow for: {incident_description}")
        
        # Run sub-agents concurrently
        await ingestion_queue.push_agent_thought(self.name, "Delegating tasks to sub-agents...")
        results = await asyncio.gather(
            log_analyzer.analyze(incident_description),
            metrics_agent.analyze(incident_description),
            diff_context_agent.analyze(incident_description)
        )
        
        log_res, met_res, diff_res = results
        
        await ingestion_queue.push_agent_thought(self.name, "Aggregating sub-agent findings...")
        
        # Generate final RCA
        system_prompt = """You are the Lead Diagnostic Orchestrator Agent. 
        Compile the sub-agent findings into a final Markdown Root Cause Analysis (RCA) report.
        Also provide an overall incident confidence score (0-100).
        Return JSON with 'rca_markdown' (string) and 'confidence_score' (number)."""
        
        user_prompt = f"Incident: {incident_description}\nLog Findings: {json.dumps(log_res)}\nMetrics: {json.dumps(met_res)}\nContext: {json.dumps(diff_res)}"
        
        response_str = await llm_provider.generate_response(system_prompt, user_prompt, require_json=True)
        
        try:
            final_report = json.loads(response_str)
        except:
            final_report = {"rca_markdown": "# RCA Failed\nCould not generate RCA.", "confidence_score": 0}
            
        await ingestion_queue.push_agent_thought(self.name, "Final RCA Report Generated.", final_report)
        return final_report

orchestrator = OrchestratorAgent()
