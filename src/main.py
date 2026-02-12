from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.logging import setup_logging
from core.settings import AppSettings, get_settings
from middlewares import LogMiddleware, TraceIdMiddleware
from repositories import shutdown_repository, startup_repository
from routing import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: AppSettings = get_settings()
    # Startup actions
    await startup_repository(app, settings)

    yield

    # Shutdown actions
    await shutdown_repository(app)


def get_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="PicPay Case API", lifespan=lifespan)

    app.include_router(routes)
    app.add_middleware(TraceIdMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],  # Allows all methods
        allow_headers=["*"],  # Allows all headers
    )
    app.add_middleware(LogMiddleware)

    return app


app = get_app()
