"""This file contains constants to configure the application"""
from pydantic import BaseSettings
# ------------------------------------------------------------------------


class Settings(BaseSettings):
    """This class serves to get environment variables"""
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    SERVER_HOST: str
    SERVER_PORT: int
    CLEAR_DB: bool
    SERVER_HOST: str
    SERVER_PORT: int
    API_VERSION: str
    API_TITLE: str
    API_DESCRIPTION: str

    class Config:
        env_file = '.env'


sets = Settings()

DB_URI = (f'postgresql+asyncpg://{sets.POSTGRES_USER}'
          f':{sets.POSTGRES_PASSWORD}@' 
          f'{sets.POSTGRES_HOST}:{sets.POSTGRES_PORT}/{sets.POSTGRES_DB}')

HOST = sets.SERVER_HOST
PORT = sets.SERVER_PORT

CLEAR_DB = sets.CLEAR_DB

API_VERSION = sets.API_VERSION
API_TITLE = sets.API_TITLE
API_DESCRIPTION = sets.API_DESCRIPTION

MEDIA_PATH = 'uploads'

BASE_URL = f'http://{HOST}:{PORT}/record?'
