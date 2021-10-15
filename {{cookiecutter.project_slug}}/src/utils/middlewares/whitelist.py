"""
Whitelist middlewares

Help project to enable protected policy for path. Only whitelist IP can
access API path. Whitelist can be applied for some specific path, only
whitelisted IP can access - others will raise 403.

Configs:
    - WHITELIST_ENABLE bool: enable for Whitelist middleware
    - WHITELIST_SUITE dict: contains path and list of whitelist IP
"""
from ipaddress import ip_address, ip_network
from typing import Dict

import pydantic
import ujson
from fastapi import FastAPI, Request
from starlette.middleware.base import (BaseHTTPMiddleware,
                                       RequestResponseEndpoint)
from starlette.types import ASGIApp

from .. import get_logger
from . import exceptions

logger = get_logger(__name__)


def init_app(app: FastAPI, settings: pydantic.BaseSettings) -> None:
    if getattr(settings, "WHITELIST_ENABLE", False):
        logger.info("Middleware enabled: WhitelistMiddleware")
        app.add_middleware(WhitelistMiddleware, suite=settings.WHITELIST_SUITE)


class WhitelistMiddleware(BaseHTTPMiddleware):

    def __init__(self, app: ASGIApp, suite: Dict):
        self.suite = self.gen_whitelist_suite(suite)
        super().__init__(app, dispatch=self.dispatch)

    async def dispatch(self, request: Request,
                       call_next: RequestResponseEndpoint):
        if request.headers.get("X-Forwarded-For"):    # behind proxy
            client_ip = ip_address(request.headers.get("X-Forwarded-For"))
        else:
            client_ip = ip_address(request.client.host)

        valid = False
        if request.url.path in self.suite.keys():
            for ip in self.suite[request.url.path]:
                if "/" in ip and client_ip in ip_network(ip):
                    valid = True
                    break
                if "/" not in ip and client_ip == ip_address(ip):
                    valid = True
                    break
            if not valid:
                logger.error("IP: " + str(client_ip) +
                             " is blocked while accessing to " +
                             request.url.path)
                return exceptions.PermissionDenied().to_response()
        return await call_next(request)

    @staticmethod
    def gen_whitelist_suite(suite):
        if isinstance(suite, str):
            return ujson.loads(suite)
