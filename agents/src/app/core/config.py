from functools import lru_cache
from typing import Literal

from pydantic import SecretStr
from pydantic_ai import UsageLimits
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_ignore_empty=True, extra="ignore"
    )

    cors_origins: str = ""
    model_provider: Literal["opencode", "ollama"] = "opencode"
    agent_model: str = "gpt-6-luna"
    agent_request_limit: int = 20
    agent_total_tokens_limit: int = 200_000
    opencode_api_key: str = ""
    opencode_base_url: str = ""
    ollama_base_url: str = ""
    logfire_token: SecretStr = SecretStr("")
    logfire_service_name: str = "agents"
    logfire_environment: str = "development"
    logfire_include_content: bool = False

    @property
    def usage_limits(self) -> UsageLimits:
        return UsageLimits(
            request_limit=self.agent_request_limit,
            total_tokens_limit=self.agent_total_tokens_limit,
        )

    @property
    def model_configured(self) -> bool:
        if self.model_provider == "ollama":
            return bool(self.ollama_base_url)

        has_api_key = bool(self.opencode_api_key)
        has_base_url = bool(self.opencode_base_url)
        return has_api_key and has_base_url

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
