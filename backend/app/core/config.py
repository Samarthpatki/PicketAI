from pydantic_settings import  BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME:str = "PicketAI"
    MONGODB_URL: str
    DATABASE_NAME:str = "PicketAI-DB"
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 


    mode_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()