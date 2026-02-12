from typing import Any

from pymongo import AsyncMongoClient
from pymongo.asynchronous.collection import AsyncCollection

from core.settings import AppSettings

from .base import BaseRepository


class MongoRepository(BaseRepository):
    def __init__(self, settings: AppSettings) -> None:
        self.client: AsyncMongoClient = AsyncMongoClient(settings.MONGO_URI)  # type: ignore
        self.database_name = settings.MONGO_DATABASE_NAME

    def collection(self, collection_name: str) -> AsyncCollection:
        db = self.client[self.database_name]
        return db[collection_name]

    async def find(self, collection: str, query: dict) -> Any | None:
        return await self.collection(collection).find_one(query)

    async def write(self, collection: str, data: dict) -> dict:
        result = await self.collection(collection).insert_one(data)
        data["_id"] = result.inserted_id
        return data

    async def update(self, collection: str, query: dict, data: dict) -> Any | None:
        return await self.collection(collection).find_one_and_update(
            query, {"$set": data}, return_document=True
        )

    async def delete(self, collection: str, query: dict) -> Any | None:
        return await self.collection(collection).find_one_and_delete(query)

    async def list(self, collection: str, query: dict) -> list[dict]:
        async with self.collection(collection).find(query) as cursor:
            return [doc async for doc in cursor]

    async def close(self):
        await self.client.aclose()

    async def is_healthy(self) -> bool:
        try:
            await self.client.admin.command("ping")
            return True
        except Exception:
            return False
