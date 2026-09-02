from fastapi import APIRouter, BackgroundTasks
from pydantic import BaseModel
from app.agents.workflow import incident_workflow

router = APIRouter()

class TriggerRequest(BaseModel):
    incident_description: str
    time_window: str = "last_15m"

@router.post("/trigger")
async def trigger_workflow(req: TriggerRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(incident_workflow.run, req.incident_description)
    return {"status": "Workflow triggered", "incident_description": req.incident_description}
