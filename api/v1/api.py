from fastapi import APIRouter

from api.v1.routers import search


api_router = APIRouter()

api_router.include_router(search.router, prefix="/search")
