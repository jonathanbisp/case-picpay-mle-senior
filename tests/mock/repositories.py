from typing import AsyncGenerator
from unittest.mock import patch

import pytest
from mongomock_motor import AsyncMongoMockClient

from core.settings import AppSettings
from repositories.mongo import MongoRepository


@pytest.fixture
async def mocked_mongo_client(
    mocked_app_settings: AppSettings,
) -> AsyncGenerator[AsyncMongoMockClient, None]:
    yield AsyncMongoMockClient(mocked_app_settings.MONGO_URI)


@pytest.fixture
async def mocked_repository(
    mocked_mongo_client: AsyncMongoMockClient, mocked_app_settings: AppSettings
) -> AsyncGenerator[MongoRepository, None]:
    with patch("repositories.mongo.AsyncMongoClient"):
        repo = MongoRepository(client=mocked_mongo_client, settings=mocked_app_settings)

        yield repo
