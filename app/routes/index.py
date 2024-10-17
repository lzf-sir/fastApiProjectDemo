
from app.api.home import home_router
from fastapi import APIRouter
from app.api.user import user_router

route = APIRouter()

route.include_router(home_router)
route.include_router(user_router)

