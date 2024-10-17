from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.database.db_mysql import create_tables
from app.routes.index import route
from app.core.config import settings


def register_router(app: FastAPI):
    app.include_router(route)


def register_middleware(app):
    # 跨域
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_app():
    app = FastAPI(
        tille=settings.TITLE,
        version = settings.VERSION,
        description = settings.DESCRIPTION,
        docs_url = settings.DOCS_URL,
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


    # 在应用启动时创建数据库表
    @app.on_event("startup")
    async def startup_event():
        await create_tables()

    return app


