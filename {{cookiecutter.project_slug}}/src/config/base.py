import os

from pydantic import BaseSettings


class _MyBase(BaseSettings):
    def update_os_env(self):
        for key, value in os.environ.items():
            if hasattr(self, key):
                setattr(self, key, value)
