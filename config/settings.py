from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    google_client_secret_file: Path = Path("secrets/client_secret.json")
    google_token_file: Path = Path("secrets/token.json")
    google_oauth_port: int = 8765

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
