from functools import lru_cache
from src.config.base import _MyBase
from src.config.general import Settings
from src.config.email import EmailSettings
from src.config.tracing import TracingSettings


@lru_cache(maxsize=128)
def get_settings(my_class: _MyBase):
    new_settings = my_class()
    new_settings.update_os_env()
    return new_settings


settings: Settings = get_settings(Settings)
email_settings: EmailSettings = get_settings(EmailSettings)
tracing_settings: TracingSettings = get_settings(TracingSettings)
