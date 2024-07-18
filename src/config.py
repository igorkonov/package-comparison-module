class Config:
    def __init__(self):
        self.base_url: str = "https://rdb.altlinux.org/api"
        self.branches: set = {"p10", "sisyphus"}


config: Config = Config()
