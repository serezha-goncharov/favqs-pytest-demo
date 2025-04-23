import os
from dotenv import load_dotenv

from pydantic import HttpUrl, SecretStr, Field
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    BASE_URL: HttpUrl = Field(default=os.getenv("BASE_URL"))
    API_KEY: SecretStr = Field(default=os.getenv("API_KEY"))


settings = Settings()
