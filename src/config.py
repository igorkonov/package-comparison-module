from pydantic_settings import BaseSettings


class Config(BaseSettings):
    base_url: str = "https://rdb.altlinux.org/api"
    branch_p10: str = "p10"
    branch_sisyphus: str = "sisyphus"


config = Config()
