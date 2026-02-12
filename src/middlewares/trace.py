from uuid import uuid4

from fastapi import Request
from starlette.datastructures import State
from starlette.middleware.base import BaseHTTPMiddleware

from core.logging import trace_id_ctx_var


class TraceIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request: Request[State], call_next):
        trace_id = request.headers.get("X-Request-ID", uuid4().hex)
        token = trace_id_ctx_var.set(trace_id)
        request.state.trace_id = trace_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = trace_id
        trace_id_ctx_var.reset(token)
        return response
