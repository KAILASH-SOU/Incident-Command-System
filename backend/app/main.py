from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import ingest, stream, agents
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ingest.router, prefix=f"{settings.API_V1_STR}/ingest", tags=["Ingest"])
app.include_router(stream.router, prefix=f"{settings.API_V1_STR}/stream", tags=["Stream"])
app.include_router(agents.router, prefix=f"{settings.API_V1_STR}/agents", tags=["Agents"])

@app.get("/")
def root():
    return {"message": "SentinelCore API is running."}
