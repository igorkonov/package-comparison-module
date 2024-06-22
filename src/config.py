from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_url: str = "https://rdb.altlinux.org/api"


config = Config()
