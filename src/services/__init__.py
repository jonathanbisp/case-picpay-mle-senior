from typing import Annotated

from fastapi import Depends

from core.settings import AppSettings, get_settings
from repositories import BaseRepository, get_repository

from .nlp import NLPService


async def get_nlp_service(
    settings: Annotated[AppSettings, Depends(get_settings)],
    repository: Annotated[BaseRepository, Depends(get_repository)],
) -> NLPService:
    return NLPService(settings=settings, repository=repository)
