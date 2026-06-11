from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    algorithm:str="HS256"
    secret_key:str
    access_token_time:int=15
    database_url:str | None=None

    model_config=SettingsConfigDict(env_file=".env",extra="ignore")

settings=Settings()