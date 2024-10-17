import datetime

from pydantic import BaseModel, EmailStr, HttpUrl, Field
from typing import Optional
from uuid import UUID


# OopCompanion:suppressRename
class Auth(BaseModel):
    """认证信息模型"""
    username: str
    password: str

class CreateUserReq(BaseModel):
    """创建用户请求模型"""
    username: str
    password: str
    email: EmailStr

class UpdateUser(BaseModel):
    """更新用户信息模型"""
    username: str
    email: EmailStr
    phone: Optional[str] = None

class Avatar(BaseModel):
    """头像模型"""
    url: HttpUrl = Field(..., description='头像 http 地址')

class GetUserInfo(BaseModel):
    """获取用户信息模型"""
    id: int
    uuid: UUID
    username: str
    email: EmailStr
    status: int
    is_superuser: bool
    avatar: Optional[str] = None
    phone: Optional[str] = None
    join_time: datetime.datetime
    last_login_time: Optional[datetime.datetime] = None

class ResetPassword(BaseModel):
    """重置密码模型"""
    username: str
    new_password: str
    confirm_password: str