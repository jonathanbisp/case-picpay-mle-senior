import logging
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException

from repositories import BaseRepository, get_repository

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=dict)
async def health_check(
    repository: Annotated[BaseRepository, Depends(get_repository)],
) -> dict:
    is_healthy = await repository.is_healthy()
    if not is_healthy:
        raise HTTPException(detail="Repository is not healthy", status_code=500)
    logging.info("Repository is healthy")
    return {"status": "healthy"}
