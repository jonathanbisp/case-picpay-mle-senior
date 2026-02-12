from fastapi import FastAPI, Request

from core.settings import AppSettings
from repositories.base import BaseRepository
from repositories.mongo import MongoRepository


async def startup_repository(app: FastAPI, settings: AppSettings) -> None:
    app.state.repository = MongoRepository(settings)


async def shutdown_repository(app: FastAPI) -> None:
    repository: BaseRepository = app.state.repository
    await repository.close()


async def get_repository(request: Request) -> BaseRepository:
    return request.app.state.repository
