from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    my_id: int
    rtsp_host: str
    rtsp_port: str
    rtsp_suffix: str
    model_config = SettingsConfigDict(env_file="./.env")
