from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings


SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@'
    f'{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
)



def create_engine_and_session():
    try:
        # 创建异步数据库引擎
        engine = create_async_engine(
            SQLALCHEMY_DATABASE_URL,
            echo=settings.MYSQL_ECHO,
            future=True,
            pool_pre_ping=True
        )
        logger.info("数据库引擎创建成功")

        # 创建异步会话工厂
        async_session = async_sessionmaker(
            engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        logger.info("数据库异步会话工厂创建成功")
        return engine, async_session
    except Exception as e:
        logger.error(f"创建数据库引擎或会话工厂失败: {e}")
        raise










