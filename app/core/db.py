import uuid
from app.database.db_mysql import create_engine_and_session


async_engine, async_db_session = create_engine_and_session()



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


def get_uuid4_str():
    """生成UUID字符串"""
    return str(uuid.uuid4())