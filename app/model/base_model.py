from sqlalchemy import Column, Integer, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

# OopCompanion:suppressRename

Base = declarative_base()

class TimestampMixin:
    """时间戳混入类，提供create_time和update_time字段"""
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间')


class BaseModel(Base,TimestampMixin):
    __abstract__ = True  # 标记为抽象基类，不能直接实例化
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    class Config:
        orm_mode = True



