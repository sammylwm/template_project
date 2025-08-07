from fastapi import APIRouter
from . import common


def setup_routers() -> APIRouter:
    router = APIRouter()
    router.include_router(common.router)
    return router
