from typing import AsyncGenerator

import pytest

from core.settings import AppSettings
from repositories.base import BaseRepository
from services.nlp import NLPService


@pytest.fixture
async def mocked_nlp_service(
    mocked_app_settings: AppSettings, mocked_repository: BaseRepository
) -> AsyncGenerator[NLPService, None]:
    yield NLPService(settings=mocked_app_settings, repository=mocked_repository)
