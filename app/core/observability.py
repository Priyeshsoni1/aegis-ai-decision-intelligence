
import logging
from time import perf_counter

from fastapi import Request

logger = logging.getLogger(__name__)


async def observe_request(request: Request, call_next):
    """Log request duration and status without logging sensitive payloads."""
    started = perf_counter()

    try:
        response = await call_next(request)
    except Exception:
        duration_ms = (perf_counter() - started) * 1000
        logger.exception(
            "request_failed method=%s path=%s duration_ms=%.2f",
            request.method,
            request.url.path,
            duration_ms,
        )
        raise

    duration_ms = (perf_counter() - started) * 1000

    logger.info(
        "http_request method=%s path=%s status_code=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )

    response.headers["X-Process-Time-Ms"] = f"{duration_ms:.2f}"
    return response
