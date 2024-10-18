from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core.config import settings
from app.core.db import get_db
from app.model.user import User
from app.schema.response import ErrorResponse
from app.utilfs.response.response_tool import ResponseTool

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL_SWAGGER)

async def get_hash_password(password: str) -> str:
    """
    使用 hash 算法加密密码

    :param password: 密码
    :return: 加密后的密码
    """
    return pwd_context.hash(password)

def password_verify(plain_password: str, hashed_password: str) -> bool:
    """
    密码校验

    :param plain_password: 要验证的密码
    :param hashed_password: 要比较的hash密码
    :return: 比较密码之后的结果
    """
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(subject: str, expires_delta: timedelta | None = None):
    """
    生成访问令牌
    :param subject: 令牌的主题，通常是用户ID
    :param expires_delta: 过期时间（秒）
    :return: 加密token
    """

    if expires_delta:
        expires = datetime.utcnow() + expires_delta
    else:
        expires = datetime.utcnow() + timedelta(settings.TOKEN_EXPIRE_MINUTES)
    payload = {
        'exp': expires,
        'sub': subject
    }
    encoded_jwt = jwt.encode(payload, settings.TOKEN_SECRET_KEY, algorithm=settings.TOKEN_ALGORITHM)
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, settings.TOKEN_SECRET_KEY, algorithms=settings.TOKEN_ALGORITHM)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id
    except JWTError:
        raise credentials_exception


# 获取当前用户
async def get_current_user(db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user_id: str = verify_token(token, settings.TOKEN_ALGORITHM)
        if user_id is None:
            raise credentials_exception
        from app.dao.async_user_dao import get_user_by_id
        user = await get_user_by_id(db, user_id)
        if user is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return user

def superuser_verify(user: User):
    """
    验证当前用户是否为超级用户

    :param user:
    :return:
    """
    is_superuser = user.is_superuser
    if not is_superuser:
        raise "not superuser"
    return is_superuser