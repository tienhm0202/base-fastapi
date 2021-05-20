"""
Initiate logger and its all injection and format

SHOULD not using `logging.getLogger(__name__)` to get logger but using
`middlewares.logger.get_logger(__name__)` instead.
"""
import logging

from fastapi import logger as fastapi_logger
from src.config import tracing_settings

from ._base import context, package_name

gunicorn_error_logger = logging.getLogger("gunicorn.error")


def init_app():
    """Init uvicorn and fastapi logger to unify log template with gunicorn"""
    uvicorn_access_logger = logging.getLogger("uvicorn.access")
    uvicorn_access_logger.addFilter(NameInjectionFilter())
    uvicorn_access_logger.handlers = gunicorn_error_logger.handlers
    uvicorn_access_logger.setLevel(logging.CRITICAL)
    fastapi_logger.handlers = gunicorn_error_logger.handlers


def get_base_logger(name: str):
    """Function to get logger"""
    logger = logging.getLogger(name)
    logger.handlers = gunicorn_error_logger.handlers
    logger.addFilter(NameInjectionFilter())
    if getattr(tracing_settings, "TRACING_ENABLE", False):
        logger.addFilter(TracingInjectionFilter())
    return logger


class NameInjectionFilter(logging.Filter):
    """Add module name to log line. But shorten it like Logback"""

    def filter(self, record: logging.LogRecord):
        name = package_name.shorten(record.name, 35)
        record.msg = name + " | " + str(record.msg)
        return True


class TracingInjectionFilter(logging.Filter):
    """Add tracing information to log"""

    def filter(self, record: logging.LogRecord):
        rid = context.get_request_id()
        cid = context.get_correlation_id()
        record.msg = f"RID: {rid} | CID: {cid} | {str(record.msg)}"
        return True
