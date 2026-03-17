"""Configuration management for the agentic system"""

from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    google_api_key: Optional[str] = os.getenv("GOOGLE_API_KEY")
    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = os.getenv("ANTHROPIC_API_KEY")

    # Agent Models
    agent_model_frontend: str = os.getenv("AGENT_MODEL_FRONTEND", "gemini-pro")
    agent_model_backend: str = os.getenv("AGENT_MODEL_BACKEND", "gpt-4")
    agent_model_orchestrator: str = os.getenv("AGENT_MODEL_ORCHESTRATOR", "claude-3-opus-20240229")

    # Logging
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "logs/agentic.log")

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
