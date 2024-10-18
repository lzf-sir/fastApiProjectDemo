from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schema.user import CreateUserReq
from app.service.login_service import LoginService
user_router = APIRouter(prefix='/user')



@user_router.post("/add/", summary='用户注册')
async def register_user(obj: CreateUserReq, db: AsyncSession = Depends(get_db)):

    res_data = await LoginService.register(obj=obj, db_session=db)
    return res_data


