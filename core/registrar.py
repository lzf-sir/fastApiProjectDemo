from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from core.config import settings


async def register_middleware(app):
    # 跨域
    if settings.MIDDLEWARE_CORS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


async def register_app():
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

    return app


