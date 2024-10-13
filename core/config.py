import os
from functools import lru_cache

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True)

    # fastapi
    TITLE: str = 'FastApi'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI SQLAlchemy MySQL'
    DOCS_URL: str | None = '/docs'
    REDOCS_URL: str | None = '/redocs'
    OPENAPI_URL: str | None = '/openapi'

    # mysql
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str



@lru_cache
def get_settings():
    """读取配置优化写法"""
    return Settings()

# 创建一个全局的 settings 实例
settings = get_settings()
