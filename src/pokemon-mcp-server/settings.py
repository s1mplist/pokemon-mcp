from functools import cache

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str = Field(
        description="OpenAI API key for accessing the OpenAI API",
        env="OPENAI_API_KEY",
    )
    pokemon_api_base: str = Field(
        description="Base URL for the Pokemon API",
        env="POKEMON_API_BASE",
    )
    log_level: str = Field(
        description="Log level for the server", default="INFO", env="LOG_LEVEL"
    )

    host: str = Field(
        description="Host to bind the server to", default="localhost", env="HOST"
    )
    port: int = Field(
        description="Port to bind the server to", default=8000, env="PORT"
    )

    @model_validator(mode="before")
    def validate_port(cls, values):
        port = values.get("port")
        if isinstance(port, str):
            try:
                values["port"] = int(port)
            except ValueError:
                raise ValueError(f"Invalid port value: {port}")
        return values


@cache
def get_settings() -> Settings:
    return Settings()
