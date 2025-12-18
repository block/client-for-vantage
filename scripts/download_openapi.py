import json
from pathlib import Path

import httpx
from pydantic_settings import BaseSettings, SettingsConfigDict

from vantage_sdk import VantageSDK

SCRIPT_DIR = Path(__file__).resolve().parent.parent
ENV_FILE = SCRIPT_DIR / ".env"


class Settings(BaseSettings):
    """Settings for dotfile - avoiding global env variables"""
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        extra="ignore",
    )
    vantage_api_key: str


if __name__ == "__main__":
    if not ENV_FILE.exists():
        raise FileNotFoundError(f"Environment file not found")

    settings = Settings()

    client = VantageSDK(api_key=settings.vantage_api_key)

    result: httpx.Response = client.get_openapi_spec()

    with open("openapi_spec.json", "w") as f:
        json.dump(result, f, indent=2)
