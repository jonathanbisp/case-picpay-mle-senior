from fastapi import APIRouter

from .model import router as model_router

routes = APIRouter(prefix="/v1")
routes.include_router(model_router)
