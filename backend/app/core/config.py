from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "SentinelCore"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # LLM Provider
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama3.1:8b" # Default fallback
    OPENAI_API_KEY: str = "" # Expected in env if using cloud
    OPENAI_MODEL: str = "gpt-4o"
    
    class Config:
        env_file = ".env"

settings = Settings()
