from ..config import _MyBase


class TracingSettings(_MyBase):
    TRACING_ENABLE: bool = True
    TRACING_REQUEST_ID: str = "X-Request-ID"
    TRACING_CORRELATION_ID: str = "X-Correlation-ID"

    class Config:
        case_sensitive = True
        env_prefix = "TRACING_"
