from fastapi import APIRouter

from app.schema.user import CreateUserReq
from app.service.login_service import LoginService
from app.utilfs.response_code import response

user_router = APIRouter()


@user_router.post("/add/", summary='用户注册')
async def register_user(obj: CreateUserReq):
    await LoginService.register(obj=obj)
    return await response.success()


