from pathlib import Path

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# services/py-engine/.env.local, found from this file's location,
# not from the folder you happen to run Python in.
ENV_FILE = Path(__file__).resolve().parent.parent / ".env.local"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE, env_file_encoding="utf-8", extra="ignore"
    )

    environment: str = "local"
    redis_url: str = "redis://localhost:6379/0"
    railkit_base_url: str = "https://api.railkit.in"
    railkit_api_key: SecretStr = SecretStr("")
    use_mock_railkit: bool = True
    cors_allowed_origins: str = "http://localhost:3000"
    telemetry_stale_after_seconds: int = 60
    telemetry_ttl_seconds: int = 86400
    ingest_interval_seconds: int = 600

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.cors_allowed_origins.split(",") if o.strip()]


settings = Settings()
