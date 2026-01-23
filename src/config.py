from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# определяем абсолютный путь до корня проекта
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    DB_NAME: str
    DB_PORT: int
    DB_HOST: str
    DB_USER: str
    DB_PASS: str
    model_config = SettingsConfigDict(env_file=BASE_DIR / '.env', extra='ignore')

    # DSN (data source name) - стандартный адрес для подключения к БД
    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
