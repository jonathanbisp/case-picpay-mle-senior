import json
from datetime import UTC, datetime
from time import time

from fastapi import Request
from starlette.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware


class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request[State], call_next):
        start_time = time()
        method = request.method
        url = str(request.url)
        response = await call_next(request)

        trace_id = (
            request.state.trace_id if hasattr(request.state, "trace_id") else None
        )
        process_time = time() - start_time
        print(
            json.dumps(
                {
                    "timestamp": datetime.now(tz=UTC).isoformat(),
                    "method": method,
                    "url": url,
                    "status_code": response.status_code,
                    "trace_id": trace_id,
                    "process_time": process_time // 1000,
                }
            )
        )
        return response
