"""PURPOSE: Centralized settings loading (dotenv/env vars), constants, and runtime config.
"""


from pydantic import BaseSettings

# PURPOSE: Centralized settings from environment variables.
class Settings(BaseSettings):
    upwork_client_id: str | None = None
    upwork_client_secret: str | None = None
    upwork_redirect_uri: str | None = None
    upwork_tenant_id: str | None = None
    upwork_auth_code: str | None = None
    database_url: str = "sqlite:///./local.db"
    slack_webhook_url: str | None = None

    class Config:
        env_file = ".env"

settings = Settings()
