from datetime import datetime
from typing import Optional
from sqlalchemy import String, Column, Integer, Boolean, DateTime

from app.core.db import get_uuid4_str
from app.model.base_model import BaseModel
from app.utilfs.time_zone import timezone


class User(BaseModel):
    """用户表"""
    __tablename__ = 'tb_user'

    uuid: str = Column(String(50), primary_key=True, unique=True, default=get_uuid4_str())
    username: str = Column(String(20), unique=True, index=True, comment='用户名')
    password: str = Column(String(255), comment='密码')
    email: str = Column(String(50), unique=True, index=True, comment='邮箱')
    status: int = Column(Integer, default=1, comment='用户账号状态(0停用 1正常)')
    is_superuser: bool = Column(Boolean, default=False, comment='超级权限(0否 1是)')
    avatar: Optional[str] = Column(String(255), default=None, comment='头像')
    phone: Optional[str] = Column(String(11), default=None, comment='手机号')
    is_delete: int = Column(Integer, default=0, comment="删除标识：0-正常 1-已删除")
    join_time: datetime = Column(DateTime, default=timezone.now, comment='注册时间')
    last_login_time: Optional[datetime] = Column(DateTime, onupdate=timezone.now, comment='上次登录')