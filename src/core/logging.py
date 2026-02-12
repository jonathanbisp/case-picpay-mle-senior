import json
import logging
import sys
from contextvars import ContextVar
from datetime import UTC, datetime

from loguru import logger

# ContextVar para armazenar trace_id por request
trace_id_ctx_var: ContextVar[str | None] = ContextVar("trace_id", default=None)


def get_trace_id() -> str | None:
    return trace_id_ctx_var.get()


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        trace_id = get_trace_id()

        log_payload = {
            "timestamp": datetime.now(tz=UTC).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "location": f"{record.pathname}:{record.lineno} | {record.funcName}",
            "trace_id": trace_id,
        }

        # Envia JSON puro para stdout
        logger.opt(exception=record.exc_info).log(
            record.levelname,
            json.dumps(log_payload),
        )


def setup_logging() -> None:
    # Remove handlers padrão
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(logging.INFO)

    # Remove logger default do loguru
    logger.remove()

    # Remove handlers padrão do uvicorn para evitar logs duplicados
    logging.getLogger("uvicorn.error").handlers = []
    logging.getLogger("uvicorn.error").propagate = False

    logging.getLogger("uvicorn.access").handlers = []
    logging.getLogger("uvicorn.access").propagate = False

    logging.getLogger("uvicorn.asgi").handlers = []
    logging.getLogger("uvicorn.asgi").propagate = True

    # Logger simples (sem serialize automático)
    logger.add(
        sys.stdout,
        level="INFO",
        backtrace=False,
        diagnose=False,
        format="{message}",  # já estamos serializando manualmente
    )
