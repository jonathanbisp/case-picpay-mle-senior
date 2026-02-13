from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient

from core.settings import AppSettings, get_settings
from main import app
from repositories import MongoRepository, get_repository
from services import NLPService, get_nlp_service


@pytest.fixture
async def mocked_app_settings() -> AsyncGenerator[AppSettings, None]:
    yield AppSettings(
        MONGO_URI="mongodb://test:27017",
        MONGO_DATABASE_NAME="case",
        MONGO_COLLECTION_MODELS="models",
        MONGO_COLLECTION_PREDICTIONS="predictions",
    )


@pytest.fixture
async def mocked_api_client(
    mocked_app_settings: AppSettings,
    mocked_repository: MongoRepository,
    mocked_nlp_service: NLPService,
) -> AsyncGenerator[TestClient, None]:
    app.dependency_overrides[get_repository] = lambda: mocked_repository
    app.dependency_overrides[get_settings] = lambda: mocked_app_settings
    app.dependency_overrides[get_nlp_service] = lambda: mocked_nlp_service

    yield TestClient(app)

    app.dependency_overrides.clear()
