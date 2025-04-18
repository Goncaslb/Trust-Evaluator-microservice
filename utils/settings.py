from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    trust_metric_aggregator_host: str
    trust_metric_aggregator_port: int

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
