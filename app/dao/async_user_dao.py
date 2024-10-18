from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.model.user import User
from app.schema.user import CreateUserReq
from app.utilfs import jwt

async def get_user_by_id(db_session: AsyncSession, user_id):
    user = await db_session.execute(select(User).filter(User.id==user_id))
    return user.scalars().first()

async def get_user_by_email(db_session: AsyncSession, email):
    user = await db_session.execute(select(User).filter(User.email==email))
    return user.scalars().first()

async def get_user_by_username(db_session: AsyncSession, username):
    user = await db_session.execute(select(User).filter(User.username==username))
    return user.scalars().first()


async def create_user(db_session: AsyncSession, user: CreateUserReq):
    hash_password = await jwt.get_hash_password(user.password)
    db_user = User(username=user.username, password=hash_password, email=user.email)
    db_session.add(db_user)
    await db_session.commit()
    await db_session.refresh(db_user)
    return db_user
