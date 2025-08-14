from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str = "postgresql+psycopg2://username:password@localhost:5432/ai_content_db"
    
    # JWT Settings
    jwt_secret_key: str = "your-super-secret-jwt-key-here"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 10
    
    # MCP Server URLs with correct API keys
    mcp_tavily_url: str = "https://server.smithery.ai/@Jeetanshu18/tavily-mcp/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b&profile=cautious-peafowl-9gzmmK"
    mcp_flux_url: str = "https://server.smithery.ai/@falahgs/flux-imagegen-mcp-server/mcp?api_key=f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"

    # Optional API Keys
    mcp_tavily_api_key: Optional[str] = "f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"
    mcp_flux_api_token: Optional[str] = "f1f6c5a8-b3d0-4815-81c3-8fa253314e6b"
    
    # App Settings
    debug: bool = True
    allowed_hosts: str = "localhost,127.0.0.1"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Create settings instance here, at top-level (no indentation)
settings = Settings()

# Print debug info, also at top-level (no indentation)
print("Loaded MCP URLs:")
print(f"Tavily URL: {settings.mcp_tavily_url}")
print(f"Flux URL: {settings.mcp_flux_url}")
