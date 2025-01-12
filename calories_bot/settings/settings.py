from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent.parent / '.env',
        env_file_encoding='utf-8',
    )

    telegram_token: str
    openweathermap_token: str
    test_mode: bool


settings = Settings()
