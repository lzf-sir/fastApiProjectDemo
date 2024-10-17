import sys
import uuid
from loguru import logger
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.core.config import settings
from app.model.base_model import Base


SQLALCHEMY_DATABASE_URL = (
    f'mysql+asyncmy://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@'
    f'{settings.MYSQL_HOST}:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}?charset={settings.MYSQL_CHARSET}'
)


def create_engine_and_session(url: str):
    try:
        # 创建异步数据库引擎
        engine = create_async_engine(
            url, echo=settings.MYSQL_ECHO, future=True, pool_pre_ping=True
        )
        logger.success("数据库连接成功")
    except Exception as e:
        logger.error(f"数据库连接失败: {e}")
        sys.exit(1)
    else:
        # 创建异步会话工厂
        db_session = async_sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
        return engine, db_session

async_engine, async_db_session = create_engine_and_session(SQLALCHEMY_DATABASE_URL)



async def get_db():
    """异步数据库会话生成器"""
    # 创建一个新的数据库会话
    async with async_db_session() as db_session:
        try:
            yield db_session
        except Exception:
            await db_session.rollback()
            raise
        finally:
            # 确保会话在操作完成后关闭
            await db_session.close()


async def create_tables():
    """创建数据库表"""
    try:
        # 使用异步引擎的连接来执行同步的create_all方法
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            logger.info("数据库表创建成功。")
    except Exception as e:
        logger.error(f"创建数据库表失败：{e}")
        raise


def get_uuid4_str():
    """生成UUID字符串"""
    return str(uuid.uuid4())