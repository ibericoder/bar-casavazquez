from pydantic_settings import BaseSettings
from typing import Optional, List

class Settings(BaseSettings):
    # Database
    database_url: str = "sqlite:///./casavazquez.db"
    database_url_async: Optional[str] = None
    
    # API
    api_v1_str: str = "/api/v1"
    project_name: str = "Casa Vazquez API"
    
    # Security
    secret_key: str = "your-secret-key-here"
    access_token_expire_minutes: int = 30
    
    # CORS - using str instead of list to avoid parsing issues
    allowed_origins: str = "*"
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    # Features
    enable_chatbot: bool = True
    
    # MCP Configuration
    mcp_model_name: str = "gpt-4"
    mcp_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def async_database_url(self) -> str:
        if self.database_url_async:
            return self.database_url_async
        # Convert sqlite URL to async version
        if self.database_url.startswith("sqlite"):
            return self.database_url.replace("sqlite://", "sqlite+aiosqlite://")
        # For PostgreSQL
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://")
        return self.database_url

    @property
    def cors_origins(self) -> List[str]:
        if self.allowed_origins == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",")]

settings = Settings()