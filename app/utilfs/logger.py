
import os
import sys

from loguru import logger
from app.core.config import settings


# OopCompanion:suppressRename
# 定义日志文件的存储路径
os.makedirs(settings.LOG_DIR, exist_ok=True)

# 配置 loguru 日志记录器
logger.add(
    os.path.join(settings.LOG_DIR, "info_{time}.log"),
    rotation=settings.LOG_ROTATION,  # 或者你希望的任何轮换策略
    retention=settings.LOG_RETENTION,  # 日志文件保留策略
    level="INFO",  # 记录 INFO 及以上级别的日志
    format=settings.LOG_FORMAT,
)
logger.add(
    os.path.join(settings.LOG_DIR, "error_{time}.log"),
    rotation=settings.LOG_ROTATION,  # 或者你希望的任何轮换策略
    retention=settings.LOG_RETENTION,  # 日志文件保留策略
    level="ERROR",  # 记录 error 及以上级别的日志
    format=settings.LOG_FORMAT,
)

# 配置控制台输出
logger.remove(0)  # 移除默认的控制台处理器
logger.add(
    sink=sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    filter=lambda record: record["level"].name != "INFO"  # 只显示非INFO级别的日志
)