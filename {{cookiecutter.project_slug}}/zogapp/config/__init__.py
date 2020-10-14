import os
import secrets
from functools import lru_cache
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, \
    PostgresDsn, validator


class Settings(BaseSettings):
    PROJECT_NAME: str

    SERVER_NAME: Optional[str] = None
    SERVER_HOST: AnyHttpUrl
    SERVER_VERSION: str
    SERVER_ENV: str
    LOG_LEVEL: str = "DEBUG"

    SENTRY_DSN: Optional[HttpUrl] = None
    SENTRY_INCLUDE: Optional[List[str]] = ["zogapp"]

    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASS: str
    POSTGRES_DB: str
    POSTGRES_PORT: Optional[int] = 5432
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    SECURITY_CSRF: bool = False
    RATE_LIMIT: int = 100
    RATE_LIMIT_TIME_SPAN: int = 30
    RATE_LIMIT_BLOCK_DURATION: int = 300

    PROMETHEUS_ENABLE: bool = True
    PROMETHEUS_PATH: str = "/metrics/"

    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    EMAILS_ENABLED: bool = False
    EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore

    API_V1_STR: str = "/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

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
    def get_host_name(cls, v: Optional) -> Optional[str]:
        if len(v):
            return v
        return os.getenv("hostname")

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache(maxsize=128)
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
