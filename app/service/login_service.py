
from app.dao.async_user_dao import get_user_by_username, check_email, create_user
from app.database.db_mysql import async_db_session
from app.model.user import User
from app.schema.user import CreateUserReq
from app.utilfs import jwt, errors
from app.utilfs.errors import ForbiddenError


class LoginService:

    @staticmethod
    async def user_verify(username: str, password: str):
        async with async_db_session as db:
            users = await get_user_by_username(db, username=username)
            if not users:
                raise errors.NotFoundError(msg='用户名不存在')
            elif not jwt.password_verify(password, users.password):
                raise errors.AuthorizationError(msg='密码错误')
            elif not users.status:
                raise errors.AuthorizationError(msg='该用户已被锁定，无法登录')
            return users

    @staticmethod
    async def register(*, obj: CreateUserReq) -> ForbiddenError | User:
        async with async_db_session.begin() as db:
            username = await get_user_by_username(db, obj.username)
            if username:
                return errors.ForbiddenError(msg='该用户名已被注册')
            email = await check_email(db, obj.email)
            if email:
                return errors.ForbiddenError(msg='该邮箱已被注册')
            return await create_user(db, obj)
