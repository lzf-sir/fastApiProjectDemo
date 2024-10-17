import os
from functools import lru_cache
from pydantic.v1 import BaseSettings



# OopCompanion:suppressRename


class Settings(BaseSettings):
    # fastapi
    TITLE: str = 'FastApi'
    VERSION: str = '0.0.1'
    DESCRIPTION: str = 'FastAPI Project Demo'
    DOCS_URL: str | None = '/docs'
    REDOCS_URL: str | None = '/redocs'
    OPENAPI_URL: str | None = '/openapi'

    # DateTime
    DATETIME_TIMEZONE: str = 'Asia/Shanghai'
    DATETIME_FORMAT: str = '%Y-%m-%d %H:%M:%S'

    # Token
    TOKEN_SECRET_KEY: str
    TOKEN_ALGORITHM: str = 'HS256'
    TOKEN_URL_SWAGGER: str = f'/auth/login/swagger'
    TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3  # 单位：m

    # mysql
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_ECHO: bool = False
    MYSQL_DATABASE: str = 'utf8mb4'
    MYSQL_CHARSET: str = 'fastdemo'


    class Config:
        # 指定 .env 文件的绝对路径
        env_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),'.env')
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings():
    """读取配置优化写法"""
    return Settings()

# 创建一个全局的 settings 实例
settings = get_settings()


