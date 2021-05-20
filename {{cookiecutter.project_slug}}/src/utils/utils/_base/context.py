from contextvars import ContextVar

CORRELATION_ID_CTX_KEY = 'correlation_id'
REQUEST_ID_CTX_KEY = 'request_id'
correlation_id_ctx_var: ContextVar[str] = ContextVar(CORRELATION_ID_CTX_KEY,
                                                     default=None)
request_id_ctx_var: ContextVar[str] = ContextVar(REQUEST_ID_CTX_KEY,
                                                 default=None)


def get_correlation_id() -> str:
    return correlation_id_ctx_var.get()


def get_request_id() -> str:
    return request_id_ctx_var.get()
