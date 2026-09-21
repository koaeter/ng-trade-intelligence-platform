from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    database_url: str = "postgresql+psycopg://trade:trade@localhost:5432/trade_intelligence"
    model_config = SettingsConfigDict(env_prefix="TRADE_", env_file=".env", extra="ignore")


settings = DatabaseSettings()
