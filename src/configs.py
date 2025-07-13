from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    my_id: int

    model_config = SettingsConfigDict(env_file="./.env")
