import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, HttpUrl, PostgresDsn, validator

from ..config import _MyBase


class Settings(_MyBase):
    PROJECT_NAME: str

    SERVER_NAME: Optional[str] = None
    SERVER_HOST: AnyHttpUrl
    SERVER_VERSION: str
    SERVER_ENV: str
    SERVER_TZ: str = "Asia/Ho_Chi_Minh"
    SERVER_SECRET: str
    TOKEN_EXPIRES: int = 30
    LOG_LEVEL: str = "DEBUG"

    PRODUCT_NAME: str

    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_INCLUDE: Optional[List[str]] = ["src"]
    SENTRY_SAMPLE_RATE: Optional[float] = 0.5

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str
    POSTGRES_PORT: Optional[str] = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    SECURITY_CSRF: bool = False
    RATE_LIMIT: int = 100
    RATE_LIMIT_TIME_SPAN: int = 30
    RATE_LIMIT_BLOCK_DURATION: int = 300

    PROMETHEUS_ENABLE: bool = True
    PROMETHEUS_PATH: str = "/metrics"

    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    WHITELIST_ENABLE: bool = False
    WHITELIST_SUITE: Dict[str, List] = {
        PROMETHEUS_PATH: ["127.0.0.1", "172.21.0.0/25", "14.162.67.6"],
        "/docs": ["127.0.0.1", "172.21.0.0/25", "14.162.67.6"]
    }

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) \
            -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    @classmethod
    @validator("SENTRY_DSN", pre=True)
    def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
        if len(v) == 0:
            return None
        return v

    @classmethod
    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) \
            -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASS"),
            host=values.get("POSTGRES_HOST"),
            port=values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    @classmethod
    @validator("SERVER_NAME", pre=True)
    def get_host_name(cls, v: Optional[Any]) -> Optional[str]:
        if len(v):
            return v
        return os.getenv("hostname")

    def update_os_env(self):
        super().update_os_env()
        self.generate_sql_alchemy_uri()

    def generate_sql_alchemy_uri(self):
        self.SQLALCHEMY_DATABASE_URI = PostgresDsn.build(
            scheme="postgresql",
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASS,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=f"/{self.POSTGRES_DB or ''}",
        )

    class Config:
        case_sensitive = True
        env_file = ".env"
