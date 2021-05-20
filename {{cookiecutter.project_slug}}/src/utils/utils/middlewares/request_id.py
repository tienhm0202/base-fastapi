from src.utils import get_logger, unique_id
from src.utils._base import context
from src.config import tracing_settings

from starlette.middleware.base import BaseHTTPMiddleware, \
    RequestResponseEndpoint
from starlette.requests import Request

logger = get_logger(__name__)


def init_app(app):
    if getattr(tracing_settings, "TRACING_ENABLE", False):
        logger.info("Middleware enabled: RequestId")
        app.add_middleware(RequestContextLogMiddleware)


class RequestContextLogMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request,
                       call_next: RequestResponseEndpoint):
        correlation_id = context.correlation_id_ctx_var.set(
            request.headers.get('X-Correlation-ID', unique_id(32, "CID")))

        passed_request_id = _get_request_id(request)
        request_id = context.request_id_ctx_var.set(passed_request_id)

        try:
            response = await call_next(request)
            response.headers['X-Correlation-ID'] = context.get_correlation_id()
            response.headers['X-Request-ID'] = context.get_request_id()
            logger.info("{ip} - \"{method} {path}\" {status}".format(
                ip=f"{request.client.host}:{request.client.port}",
                method=request.scope["method"],
                path=request.url.path,
                status=response.status_code))
        finally:
            context.correlation_id_ctx_var.reset(correlation_id)
            context.request_id_ctx_var.reset(request_id)

        return response


def _get_request_id(request: Request):
    if request.headers.get("X-Request-ID"):
        return request.headers.get("X-Request-ID")
    elif request.headers.get("X-Request-Id"):  # Heroku
        return request.headers.get("X-Request-Id")
    return unique_id(32, "RID")
