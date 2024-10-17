from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.user import User
from app.schema.user import CreateUserReq
from app.utilfs import jwt


async def create_user(db_session: AsyncSession, user_data: CreateUserReq) -> User:
    hash_password = jwt.get_hash_password(user_data.password)
    db_user = User(username=user_data.username, password=hash_password, email=user_data.email)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user

async def get_user_by_id(db_session: AsyncSession, user_id):
    user = await db_session.execute(select(User).filter(User.id==user_id))
    return user.scalars().first()

async def get_user_by_username(db_session: AsyncSession, username):
    user = await db_session.execute(select(User).filter(User.username==username))
    return user.scalars().first()

async def update_user(db_session: AsyncSession, user_id, username=None, email=None):
    users = await get_user_by_id(db_session, user_id)
    if username:
        users.username = username
    if email:
        users.email = email
    await db_session.commit()
    return users

async def delete_user(db_session: AsyncSession, user_id):
    user = await get_user_by_id(db_session, user_id)
    await db_session.delete(user)
    await db_session.commit()

async def check_email(db_session: AsyncSession, email):
    user = await db_session.execute(select(User).filter(User.email==email))
    return user.scalars().first()