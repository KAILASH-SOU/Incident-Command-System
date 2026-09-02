from app.agents.orchestrator import orchestrator

class IncidentWorkflow:
    async def run(self, incident_description: str):
        return await orchestrator.run_incident_workflow(incident_description)

incident_workflow = IncidentWorkflow()
