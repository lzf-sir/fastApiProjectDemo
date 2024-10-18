import contextvars
import os
import time
import uuid

from fastapi import FastAPI, Request
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from app.core.db import async_engine
from app.model.base_model import Base
from app.routes.index import route
from app.core.config import settings


def register_router(app: FastAPI):
    app.include_router(route)

# 全局位置声明
request_id_context = contextvars.ContextVar("request_id", default="-")

async def log_requests_middleware(request: Request, call_next):
    request_id = uuid.uuid4().hex
    request_id_context.set(request_id)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"Request {request_id} | {request.method} {request.url} | Status code: {response.status_code} | Time: {process_time:.2f}s")
    return response

def register_middleware(app):
    # 跨域
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            log_requests_middleware,
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_app():
    app = FastAPI(
        tille=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOCS_URL,
        openapi_url=settings.OPENAPI_URL,
    )
    # app.mount(
    #     "/static",
    #     StaticFiles(directory=os.path.join(BASE_DIR, "statics")),
    #     name="static",
    # )

    # 路由
    register_router(app)

    @app.middleware('http')
    async def log_requests(request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response



    # 生命周期事件处理器
    @app.on_event("startup")
    async def startup_event():
        # 在应用启动时创建数据库表
        try:
            # 使用异步引擎的连接来执行同步的create_all方法
            async with async_engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
                logger.info("数据库表创建成功。")
        except Exception as e:
            logger.error(f"创建数据库表失败：{e}")
            raise

    @app.on_event("shutdown")
    async def shutdown_event():
        # 在这里执行关闭前的清理工作，例如关闭数据库连接
        pass

    return app
