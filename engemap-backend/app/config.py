"""Configuracoes da aplicacao lidas a partir de variaveis de ambiente."""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuracoes do backend. Valores podem ser sobrescritos via .env ou env vars."""

    database_url: str = "postgresql+psycopg2://engemap:engemap@localhost:5432/engemap"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="ENGEMAP_")


settings = Settings()