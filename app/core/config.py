from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ASYNC_DATABASE_URL: str
    SYNC_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()

