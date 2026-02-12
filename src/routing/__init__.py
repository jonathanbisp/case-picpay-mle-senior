from fastapi import APIRouter

from .health import router as health_router
from .v1 import routes as v1_routes

routes = APIRouter()
routes.include_router(health_router)
routes.include_router(v1_routes)
