from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


class Settings(BaseSettings):
    APP_NAME: Optional[str] = None
    APP_VERSION: Optional[str] = None
    APP_DESCRIPTION: Optional[str] = None
    PORT: Optional[int] = 8009
    BASE_API_V1: Optional[str] = None
    PYTHON_ENV: Optional[str] = None
    DOCS_ENABLED: Optional[bool] = False
    LPU_LIVE_TOKEN: Optional[str] = None
    REG_NO: Optional[str] = None
    PASSWORD: Optional[str] = None

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
