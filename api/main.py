from fastapi import FastAPI
from mongoengine import connect, disconnect
from starlette.middleware.cors import CORSMiddleware

from api.settings import Settings
from api.v1 import api_router
from api.v1.dependencies import warm_cache


settings = Settings()

app = FastAPI(
    title=settings.project_title,
    on_startup=[
        lambda: connect(settings.mongo.db_name, host=settings.mongo.url),
        warm_cache
    ],
    on_shutdown=[disconnect]
)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["GET"])

app.include_router(api_router, prefix=settings.v1_prefix)
