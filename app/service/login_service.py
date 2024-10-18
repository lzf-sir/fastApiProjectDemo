from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_db_session
from app.dao.async_user_dao import get_user_by_username, get_user_by_email, create_user
from app.schema.response import ErrorResponse, SuccessResponse
from app.schema.user import CreateUserReq
from app.utilfs import jwt
from app.utilfs.response.response_tool import ResponseTool

response = ResponseTool()

class LoginService:

    @classmethod
    async def user_verify(cls, username: str, password: str) -> ErrorResponse | SuccessResponse:
        async with async_db_session as db:
            users = await get_user_by_username(db, username=username)
            if not users:
                return response.not_found(msg='用户名不存在', error=username)
            elif not jwt.password_verify(password, users.password):
                return response.unauthorized(msg='密码错误',  error=password)
            elif not users.status:
                return response.unauthorized(msg='该用户已被锁定，无法登录', error=None)
            return response.success(data=users)


    @classmethod
    async def register(cls, obj: CreateUserReq, db_session: AsyncSession,) -> ErrorResponse | SuccessResponse:
        username = await get_user_by_username(db_session, obj.username)
        if username:
            return response.forbidden(msg='该用户名已被注册', error=None)
        email = await get_user_by_email(db_session, obj.email)
        if email:
            return response.forbidden(msg='该邮箱已被注册', error=None)
        res = await create_user(db_session, obj)
        return response.success(data=res)
