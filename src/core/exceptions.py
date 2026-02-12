from fastapi import Request
from loguru import logger
from starlette.datastructures import State
from starlette.responses import JSONResponse


async def value_error_handler(request: Request[State], exc: ValueError) -> JSONResponse:
    logger.warning(f"ValueError: {exc}")
    return JSONResponse(
        status_code=400, content={"error": "invalid_request", "message": str(exc)}
    )
