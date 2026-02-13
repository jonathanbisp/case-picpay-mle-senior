from fastapi import FastAPI, Request
from pymongo import AsyncMongoClient

from core.settings import AppSettings
from repositories.base import BaseRepository
from repositories.mongo import MongoRepository


async def startup_repository(app: FastAPI, settings: AppSettings) -> None:
    client = AsyncMongoClient(settings.MONGO_URI)  # type: ignore
    app.state.repository = MongoRepository(client=client, settings=settings)


async def shutdown_repository(app: FastAPI) -> None:
    repository: BaseRepository = app.state.repository
    await repository.close()


async def get_repository(request: Request) -> BaseRepository:
    return request.app.state.repository
